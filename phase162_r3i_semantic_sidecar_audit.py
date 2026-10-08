"""Read-only alignment of R3-H unexplained steps with existing semantic/reason sidecars.

Sidecar hints and final-result labels are not independent mathematical proofs.
No existing renderer, ProofStep, or public Markdown is modified.
"""
from collections import Counter
from dataclasses import dataclass

from phase162_r3g_existing_reason_bridge import build_phase162_r3g_existing_reason_trace
from phase162_r3h_reason_inventory import build_phase162_r3h_inventory
from toda_group_proof_narrative_aggregate_semantics import (
    build_toda_group_proof_narrative_aggregate_semantic_sidecar,
)
from toda_group_proof_narrative_reason_renderer import (
    render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
    TodaGroupProofNarrativeReasonKind,
    build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import TodaGroupProofPresentation


@dataclass(frozen=True)
class R3ISidecarEntry:
    index: int
    prior_category: str
    statement_type: str
    inference_rule: str | None
    category: str
    reason_kinds: tuple[str, ...]
    direct_premise_reason_kinds: tuple[str, ...]
    contextual_reason_kinds: tuple[str, ...]
    label_only_reason_kinds: tuple[str, ...]
    unrenderable_reason_kinds: tuple[str, ...]
    semantic_hints: tuple[str, ...]
    details: tuple[str, ...]


def classify_r3i_sidecar_entry(entry, record, reasons, semantic_hints) -> R3ISidecarEntry:
    """Classify existing reasons by identity, scope, and prose availability.

    This is NOT a new inference checker. In particular, a final-result label
    never establishes that its premises imply its conclusion.
    """
    if record.index != entry.index or record.reason_status != 'UNEXPLAINED':
        raise ValueError('R3-H entry and unexplained trace record must align')
    direct_ids = {id(premise) for premise in record.step.premises}
    classified = []
    direct = []
    contextual = []
    label_only = []
    unrenderable = []
    details = []
    for reason in reasons:
        if reason.conclusion_step is not record.step:
            raise ValueError('Reason conclusion must be the identical ProofStep')
        kind = reason.kind.value
        classified.append(kind)
        if reason.kind is TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION:
            label_only.append(kind)
            continue
        try:
            sentence = render_toda_group_proof_narrative_reason_sentence(reason)
        except (TypeError, ValueError, AttributeError) as exc:
            sentence = None
            details.append(kind + ': render_error=' + type(exc).__name__)
        if not isinstance(sentence, str) or not sentence.strip():
            unrenderable.append(kind)
            continue
        if all(id(premise) in direct_ids for premise in reason.premise_steps):
            direct.append(kind)
        else:
            contextual.append(kind)
            details.append(kind + ': not_all_premises_are_direct')
    hints = tuple(sorted(set(semantic_hints)))
    if direct:
        category = 'SIDECAR_DIRECT_REASON_CANDIDATE'
    elif contextual:
        category = 'SIDECAR_CONTEXTUAL_REASON_REVIEW'
    elif unrenderable:
        category = 'SIDECAR_REASON_NOT_RENDERABLE'
    elif label_only:
        category = 'GENERIC_RESULT_LABEL_ONLY'
    elif hints:
        category = 'SEMANTIC_HINT_ONLY'
    else:
        category = 'NO_SIDECAR_REASON_OR_HINT'
    if len(direct) + len(contextual) > 1:
        details.append('Multiple renderable reason candidates; selection not audited')
    return R3ISidecarEntry(
        index=entry.index,
        prior_category=entry.category,
        statement_type=entry.statement_type,
        inference_rule=entry.inference_rule,
        category=category,
        reason_kinds=tuple(classified),
        direct_premise_reason_kinds=tuple(direct),
        contextual_reason_kinds=tuple(contextual),
        label_only_reason_kinds=tuple(label_only),
        unrenderable_reason_kinds=tuple(unrenderable),
        semantic_hints=hints,
        details=tuple(details),
    )


def build_phase162_r3i_sidecar_audit(presentation: TodaGroupProofPresentation):
    """Cross-index all 54 R3-H unexplained steps without changing their status."""
    if not isinstance(presentation, TodaGroupProofPresentation):
        raise TypeError('presentation must be TodaGroupProofPresentation')
    inventory, prior = build_phase162_r3h_inventory(presentation)
    baseline = build_phase162_r3g_existing_reason_trace(presentation)
    semantic = build_toda_group_proof_narrative_semantic_sidecar(presentation)
    aggregate = build_toda_group_proof_narrative_aggregate_semantic_sidecar(presentation)
    sidecar = build_toda_group_proof_narrative_reason_sidecar(presentation, semantic)
    if sidecar.presentation is not presentation:
        raise AssertionError('Reason Sidecar presentation identity mismatch')
    records = {record.index: record for record in baseline.records}
    reasons_by_id = {}
    for reason in sidecar.reasons:
        reasons_by_id.setdefault(id(reason.conclusion_step), []).append(reason)
    hints_by_id = {}
    for step_semantic in semantic.step_semantics:
        hints_by_id.setdefault(id(step_semantic.proof_step), []).append('step:' + step_semantic.role.value)
    for dependency in semantic.dependency_semantics:
        hints_by_id.setdefault(id(dependency.dependent_step), []).append('dependency:' + dependency.role.value)
    for application in semantic.reference_application_semantics:
        hints_by_id.setdefault(id(application.dependent_step), []).append('reference_application:' + application.reference.label)
    for step_semantic in aggregate.step_semantics:
        hints_by_id.setdefault(id(step_semantic.proof_step), []).append('aggregate:' + step_semantic.kind.value)
    results = tuple(
        classify_r3i_sidecar_entry(
            entry,
            records[entry.index],
            reasons_by_id.get(id(records[entry.index].step), ()),
            hints_by_id.get(id(records[entry.index].step), ()),
        )
        for entry in inventory
    )
    if len(results) != prior['unexplained_count'] or len({e.index for e in results}) != len(results):
        raise AssertionError('R3-H inventory coverage changed')
    counts = Counter(e.category for e in results)
    kinds = Counter(kind for e in results for kind in e.reason_kinds)
    report = {
        'status': 'R3I_SIDECAR_ALIGNMENT_ONLY_NOT_FULL_PROOF',
        'node_count': len(baseline.records),
        'edge_count': baseline.checked_edge_count,
        'prior_explained_count': prior['already_explained_count'],
        'unexplained_count': len(results),
        'r3h_category_counts': prior['category_counts'],
        'r3i_category_counts': dict(sorted(counts.items())),
        'sidecar_reason_kind_counts': dict(sorted(kinds.items())),
        'semantic_step_count': len(semantic.step_semantics),
        'semantic_dependency_count': len(semantic.dependency_semantics),
        'semantic_reference_application_count': len(semantic.reference_application_semantics),
        'aggregate_step_count': len(aggregate.step_semantics),
        'total_reason_sidecar_count': len(sidecar.reasons),
        'classified_indices': [entry.index for entry in results],
        'all_nodes_once': prior['all_nodes_once'],
        'dependency_first': prior['dependency_first'],
        'root_is_last': prior['root_is_last'],
        'historical_markdown_used_as_input': False,
        'public_renderer_changed': False,
        'reason_implementation_changed': False,
        'unexplained_status_preserved': True,
        'full_proof_semantic_certification': False,
        'limitations': [
            'The semantic and aggregate sidecars are annotation/classification mechanisms, not proof checkers.',
            'Direct-premise sidecar reasons are candidates until their rule-specific mathematical sufficiency is audited.',
            'Contextual reasons can reference non-direct dependencies and must not be attached automatically.',
            'FINAL_RESULT_DERIVATION only labels a result and does not validate the implication.',
            'Unmatched steps may already have non-Reason proof rules; no claim of missing mathematical implementation is made.',
        ],
    }
    return results, report
