"""R3-K: inspect replay-verified inference meaning without inventing reasons.

This module consumes R3-J's exact rule-replay evidence. A rule's description is
metadata, not a proof of why its conclusion follows from the premises.
"""
from collections import Counter, defaultdict
from dataclasses import dataclass

from phase162_r3g_existing_reason_bridge import build_phase162_r3g_existing_reason_trace
from phase162_r3j_inference_rule_audit import build_phase162_r3j_inference_rule_audit
from toda_group_proof_presentation import TodaGroupProofPresentation


@dataclass(frozen=True)
class R3KMeaningEntry:
    index: int
    rule_name: str
    description: str
    premise_indices: tuple[int, ...]
    premise_types: tuple[str, ...]
    statement_type: str
    has_guard: bool
    has_literature_reference: bool
    evidence_status: str
    prose_status: str
    explanation_draft: str


def compose_r3k_explanation_draft(record, rule_entry, records_by_index) -> str:
    """Prepare an explicitly non-certified proof outline from real step identities."""
    if rule_entry.classification != 'RULE_REPLAY_VERIFIED_PROSE_UNAUDITED':
        raise ValueError('Draft requires a replay-verified R3-J step')
    if record.reason_status != 'UNEXPLAINED':
        raise ValueError('Draft must not replace an existing mathematical reason')
    if record.index != rule_entry.index:
        raise ValueError('R3-J index does not match the record')
    if tuple(record.premise_indices) != rule_entry.premise_indices:
        raise ValueError('Premise indices do not match the replay audit')
    if record.step.inference_rule is None:
        raise ValueError('InferenceRule missing')
    rule = record.step.inference_rule
    if rule.name != rule_entry.inference_rule_name:
        raise ValueError('InferenceRule identity changed')
    if not rule.description or not rule.description.strip():
        raise ValueError('Rule description is unavailable')
    premises = []
    for index, step in zip(record.premise_indices, record.step.premises):
        other = records_by_index[index]
        if other.step is not step:
            raise ValueError('Premise ProofStep identity mismatch')
        premises.append('[S' + str(index).zfill(3) + '] ' + other.mathematical_fact)
    return '\n'.join([
        '前提（ProofStep由来）:',
        *(('- ' + fact) for fact in premises),
        '規則: ' + rule.name,
        '規則の登録説明（数学的理由文としては未認証）: ' + rule.description.strip(),
        '結論（同じ前提による規則再適用で一致）: ' + record.mathematical_fact,
        '状態: RULE_REPLAY_VERIFIED / PROSE_NOT_CERTIFIED',
    ])


def build_phase162_r3k_rule_meaning_audit(presentation: TodaGroupProofPresentation):
    """Group 45 verified rule applications by actual structure, not prose guesses."""
    if not isinstance(presentation, TodaGroupProofPresentation):
        raise TypeError('presentation must be TodaGroupProofPresentation')
    r3j_entries, r3j_report = build_phase162_r3j_inference_rule_audit(presentation)
    baseline = build_phase162_r3g_existing_reason_trace(presentation)
    by_index = {record.index: record for record in baseline.records}
    entries = []
    for prior in r3j_entries:
        record = by_index[prior.index]
        if prior.classification != 'RULE_REPLAY_VERIFIED_PROSE_UNAUDITED':
            raise ValueError('R3-K only accepts replay-verified inference steps')
        if not prior.description or not prior.description.strip():
            raise ValueError('R3-K requires a stored description')
        draft = compose_r3k_explanation_draft(record, prior, by_index)
        entries.append(R3KMeaningEntry(
            index=prior.index,
            rule_name=prior.inference_rule_name,
            description=prior.description,
            premise_indices=prior.premise_indices,
            premise_types=prior.premise_types,
            statement_type=prior.statement_type,
            has_guard=prior.has_match_guard,
            has_literature_reference=prior.has_literature_reference,
            evidence_status='RULE_REPLAY_VERIFIED',
            prose_status='RULE_DESCRIPTION_ONLY_NOT_A_PROOF_REASON',
            explanation_draft=draft,
        ))
    if len(entries) != r3j_report['target_no_sidecar_count']:
        raise AssertionError('R3-K and R3-J target coverage differ')
    grouping = defaultdict(list)
    for entry in entries:
        key = (entry.rule_name, entry.premise_types, entry.statement_type)
        grouping[key].append(entry.index)
    groups = [
        {
            'rule_name': key[0],
            'premise_types': list(key[1]),
            'statement_type': key[2],
            'count': len(indices),
            'step_indices': indices,
            'description_variants': sorted({entry.description for entry in entries if entry.index in indices}),
        }
        for key, indices in sorted(grouping.items(), key=lambda item: (item[0][0], item[0][1], item[0][2]))
    ]
    counts = Counter(entry.rule_name for entry in entries)
    report = {
        'status': 'R3K_RULE_MEANING_INVENTORY_NOT_PROSE_CERTIFICATION',
        'node_count': len(baseline.records),
        'edge_count': baseline.checked_edge_count,
        'target_count': len(entries),
        'rule_name_count': len(counts),
        'structural_group_count': len(groups),
        'rules_by_name': dict(sorted(counts.items())),
        'description_based_draft_count': len(entries),
        'new_certified_reason_count': 0,
        'prior_explained_count': sum(record.reason_status == 'EXPLAINED' for record in baseline.records),
        'unexplained_status_preserved': all(by_index[e.index].reason_status == 'UNEXPLAINED' for e in entries),
        'all_nodes_once': len({id(record.step) for record in baseline.records}) == len(baseline.records),
        'dependency_first': all(p < record.index for record in baseline.records for p in record.premise_indices),
        'root_is_last': baseline.records[-1].step is presentation.root_step,
        'historical_markdown_used_as_input': False,
        'public_renderer_changed': False,
        'inference_rules_changed': False,
        'full_proof_semantic_certification': False,
        'limitations': [
            'A registered rule description is metadata, not a rule-specific proof reason.',
            'Drafts are structured evidence outlines only and remain UNEXPLAINED.',
            'Nine generic-result-label steps are outside this 45-step scope.',
            'External GIVEN assumptions are not mathematically validated here.',
        ],
    }
    return tuple(entries), groups, report


def render_phase162_r3k_rule_meaning_markdown(entries: tuple[R3KMeaningEntry, ...]) -> str:
    if not isinstance(entries, tuple) or any(not isinstance(e, R3KMeaningEntry) for e in entries):
        raise TypeError('entries must be tuple[R3KMeaningEntry, ...]')
    lines = [
        '# Phase 162 R3-K: InferenceRule evidence outlines',
        '',
        '**注意：以下は証明本文ではありません。規則再適用の検証結果と登録説明の照合記録です。**',
        '',
    ]
    for entry in entries:
        lines.extend(['## [S' + str(entry.index).zfill(3) + '] ' + entry.rule_name, '', entry.explanation_draft, ''])
    return '\n'.join(lines).rstrip() + '\n'
