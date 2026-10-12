"""Phase 162 R3-J: read-only inference-rule audit of R3-I's 45 unmatched steps.

A successfully replayed inference is not an explanation in mathematical prose.
The trustworthiness of external GIVEN premises is outside this audit.
"""
from collections import Counter
from dataclasses import dataclass

from phase162_r3g_existing_reason_bridge import build_phase162_r3g_existing_reason_trace
from phase162_r3i_semantic_sidecar_audit import build_phase162_r3i_sidecar_audit
from proof import (
    InferenceRule,
    ProofRule,
    ProofStep,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from toda_group_proof_presentation import TodaGroupProofPresentation


@dataclass(frozen=True)
class R3JRuleEntry:
    index: int
    statement_type: str
    inference_rule_name: str | None
    description: str | None
    premise_indices: tuple[int, ...]
    premise_types: tuple[str, ...]
    premise_pattern_count: int
    premise_pattern_types: tuple[str | None, ...]
    has_conclusion_builder: bool
    has_conclusion_pattern: bool
    has_match_guard: bool
    has_literature_reference: bool
    classification: str
    exact_identity_match_count: int
    matching_conclusion_count: int
    details: tuple[str, ...]


def classify_r3j_inference_rule(record) -> R3JRuleEntry:
    """Replay a single existing inference with its original direct premises.

    This reports metadata and replayability; it does not infer any prose reason.
    """
    step = record.step
    if not isinstance(step, ProofStep) or step.rule is not ProofRule.INFERENCE:
        raise TypeError('R3-J requires an INFERENCE ProofStep')
    rule = step.inference_rule
    if rule is not None and not isinstance(rule, InferenceRule):
        raise TypeError('inference_rule must be InferenceRule or None')

    description = rule.description if rule is not None else None
    patterns = tuple(rule.premise_patterns) if rule is not None else ()
    exact_count = 0
    conclusion_count = 0
    details = []
    if rule is None:
        category = 'INFERENCE_RULE_MISSING'
    elif not step.premises:
        category = 'INFERENCE_PREMISES_MISSING'
    else:
        try:
            for match in find_inference_matches_for_rule(rule, step.premises):
                if len(match.premises) != len(step.premises):
                    continue
                if not all(actual is expected for actual, expected in zip(match.premises, step.premises)):
                    continue
                exact_count += 1
                try:
                    derived = apply_inference_match(match)
                except (TypeError, ValueError, AttributeError) as exc:
                    details.append('apply_error:' + type(exc).__name__ + ':' + str(exc))
                    continue
                if derived.conclusion == step.conclusion:
                    conclusion_count += 1
        except (TypeError, ValueError, AttributeError) as exc:
            details.append('match_error:' + type(exc).__name__ + ':' + str(exc))
        if conclusion_count > 0:
            category = 'RULE_REPLAY_VERIFIED_PROSE_UNAUDITED'
        elif details:
            category = 'RULE_REPLAY_ERROR_REVIEW'
        elif exact_count:
            category = 'RULE_CONCLUSION_MISMATCH'
        else:
            category = 'RULE_NO_EXACT_PREMISE_MATCH'

    return R3JRuleEntry(
        index=record.index,
        statement_type=type(step.conclusion).__name__,
        inference_rule_name=rule.name if rule is not None else None,
        description=description,
        premise_indices=record.premise_indices,
        premise_types=tuple(type(p.conclusion).__name__ for p in step.premises),
        premise_pattern_count=len(patterns),
        premise_pattern_types=tuple(
            pattern.statement_type.__name__ if pattern.statement_type is not None else None
            for pattern in patterns
        ),
        has_conclusion_builder=rule.conclusion_builder is not None if rule is not None else False,
        has_conclusion_pattern=rule.conclusion_pattern is not None if rule is not None else False,
        has_match_guard=rule.match_guard is not None if rule is not None else False,
        has_literature_reference=rule.literature_reference is not None if rule is not None else False,
        classification=category,
        exact_identity_match_count=exact_count,
        matching_conclusion_count=conclusion_count,
        details=tuple(details),
    )


def build_phase162_r3j_inference_rule_audit(presentation: TodaGroupProofPresentation):
    """Audit exactly the R3-I entries lacking sidecar reasons or hints."""
    if not isinstance(presentation, TodaGroupProofPresentation):
        raise TypeError('presentation must be TodaGroupProofPresentation')
    r3i_entries, r3i_report = build_phase162_r3i_sidecar_audit(presentation)
    baseline = build_phase162_r3g_existing_reason_trace(presentation)
    records_by_index = {record.index: record for record in baseline.records}
    targets = tuple(
        entry for entry in r3i_entries
        if entry.category == 'NO_SIDECAR_REASON_OR_HINT'
    )
    results = []
    for entry in targets:
        record = records_by_index[entry.index]
        if record.reason_status != 'UNEXPLAINED':
            raise AssertionError('R3-I unresolved classification changed')
        result = classify_r3j_inference_rule(record)
        if result.index != entry.index:
            raise AssertionError('R3-I and R3-J node indexes disagree')
        results.append(result)
    if len({entry.index for entry in results}) != len(results):
        raise AssertionError('Duplicate R3-J target')
    if len(results) != r3i_report['r3i_category_counts'].get('NO_SIDECAR_REASON_OR_HINT', 0):
        raise AssertionError('R3-I unmatched coverage changed')
    category_counts = Counter(entry.classification for entry in results)
    metadata_counts = Counter()
    for entry in results:
        for name in ('has_conclusion_builder', 'has_conclusion_pattern', 'has_match_guard', 'has_literature_reference'):
            if getattr(entry, name):
                metadata_counts[name] += 1
        if entry.description:
            metadata_counts['has_description'] += 1
    report = {
        'status': 'R3J_RULE_REPLAY_AND_METADATA_AUDIT_NOT_PROSE_CERTIFICATION',
        'node_count': len(baseline.records),
        'edge_count': baseline.checked_edge_count,
        'prior_explained_count': r3i_report['prior_explained_count'],
        'r3i_unexplained_count': r3i_report['unexplained_count'],
        'r3i_label_only_count': r3i_report['r3i_category_counts'].get('GENERIC_RESULT_LABEL_ONLY', 0),
        'target_no_sidecar_count': len(targets),
        'classification_counts': dict(sorted(category_counts.items())),
        'rule_metadata_counts': dict(sorted(metadata_counts.items())),
        'classified_indices': [entry.index for entry in results],
        'all_nodes_once': len({id(record.step) for record in baseline.records}) == len(baseline.records),
        'dependency_first': all(p < record.index for record in baseline.records for p in record.premise_indices),
        'root_is_last': baseline.records[-1].step is presentation.root_step,
        'historical_markdown_used_as_input': False,
        'public_renderer_changed': False,
        'inference_rules_changed': False,
        'inference_explanations_added': 0,
        'unexplained_status_preserved': True,
        'full_proof_semantic_certification': False,
        'limitations': [
            'Rule replay verifies that the registered rule derives its recorded conclusion; it is not a prose explanation.',
            'Rule descriptions, guards, and patterns alone do not justify a human-readable proof sentence.',
            'Nine separate generic final-result labels are outside the 45-step R3-J target.',
            'The validity of trusted external GIVEN premises and full mathematical prose remains outside this audit.',
        ],
    }
    return tuple(results), report
