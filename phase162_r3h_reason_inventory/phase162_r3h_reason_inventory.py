"""Read-only inventory of existing reasons for unexplained Phase 162 R3-G steps.

This is NOT a new proof checker and does NOT attach reasons to output.
Only builder matches with direct-premise identity and a renderable sentence count
as direct reuse candidates. Broad final-result labels do not count as reasons.
"""

from collections import Counter
from dataclasses import dataclass

from proof import ProofRule
from phase162_r3g_existing_reason_bridge import build_phase162_r3g_existing_reason_trace
from toda_group_proof_narrative_reason_renderer import (
    render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
    _exactness_to_kernel_reason,
    _exactness_to_map_property_reason,
    _final_group_structure_reason,
    _final_result_derivation_reason,
    _injective_image_order_reason,
    _multiple_relation_to_order_reason,
)
from toda_group_proof_presentation import TodaGroupProofPresentation


DIRECT_BUILDERS = (
    ('exactness_to_map_property', _exactness_to_map_property_reason),
    ('exactness_to_kernel', _exactness_to_kernel_reason),
    ('injective_image_order', _injective_image_order_reason),
    ('multiple_relation_to_order', _multiple_relation_to_order_reason),
    ('final_group_structure', _final_group_structure_reason),
)


@dataclass(frozen=True)
class R3HEntry:
    index: int
    statement_type: str
    inference_rule: str | None
    premise_indices: tuple[int, ...]
    category: str
    existing_reason_kinds: tuple[str, ...]
    details: tuple[str, ...]


def classify_r3h_unexplained_step(record) -> R3HEntry:
    """Classify without inventing missing mathematical derivations."""
    if record.reason_status != 'UNEXPLAINED' or record.step.rule is not ProofRule.INFERENCE:
        raise ValueError('Only unexplained inference records may be classified')

    step = record.step
    matches = []
    details = []
    invalid_match = False
    unusable_prose = False
    actual_ids = {id(premise) for premise in step.premises}

    for label, builder in DIRECT_BUILDERS:
        try:
            reason = builder(step)
        except (TypeError, ValueError, AttributeError) as exc:
            details.append(label + ': builder_error: ' + type(exc).__name__ + ': ' + str(exc))
            continue
        if reason is None:
            continue
        matches.append(label)
        if reason.conclusion_step is not step or any(
            id(premise) not in actual_ids for premise in reason.premise_steps
        ):
            invalid_match = True
            details.append(label + ': direct_premise_identity_failed')
            continue
        try:
            sentence = render_toda_group_proof_narrative_reason_sentence(reason)
        except (TypeError, ValueError, AttributeError) as exc:
            sentence = None
            details.append(label + ': render_error: ' + type(exc).__name__ + ': ' + str(exc))
        if not isinstance(sentence, str) or not sentence.strip():
            unusable_prose = True
            details.append(label + ': no_renderable_sentence')

    if len(matches) > 1 or invalid_match:
        category = 'AMBIGUOUS_OR_INVALID_DIRECT_MATCH'
    elif len(matches) == 1 and not unusable_prose:
        category = 'DIRECT_REUSE_READY'
    elif matches:
        category = 'MATCHED_BUT_RENDER_UNAVAILABLE'
    else:
        # The existing final-result builder accepts very broad equality shapes,
        # and does not guarantee that a particular mathematical implication was
        # checked. It MUST NOT be considered an explained inference here.
        try:
            broad_result = _final_result_derivation_reason(step)
        except (TypeError, ValueError, AttributeError) as exc:
            broad_result = None
            details.append('generic_final_result_error: ' + type(exc).__name__)
        if broad_result is not None:
            category = 'GENERIC_RESULT_LABEL_ONLY'
            details.append('Broad final-result reason is not premise-validated')
        else:
            category = 'NO_DIRECT_MATCH_REVIEW_REQUIRED'
            details.append('Could require semantic-sidecar context or a new reason; not yet distinguished')

    return R3HEntry(
        index=record.index,
        statement_type=type(step.conclusion).__name__,
        inference_rule=step.inference_rule.name if step.inference_rule is not None else None,
        premise_indices=record.premise_indices,
        category=category,
        existing_reason_kinds=tuple(matches),
        details=tuple(details),
    )


def build_phase162_r3h_inventory(presentation: TodaGroupProofPresentation):
    """Return immutable entries and summary while preserving R3-G ancestry."""
    if not isinstance(presentation, TodaGroupProofPresentation):
        raise TypeError('presentation must be TodaGroupProofPresentation')
    baseline = build_phase162_r3g_existing_reason_trace(presentation)
    entries = tuple(
        classify_r3h_unexplained_step(record)
        for record in baseline.records
        if record.reason_status == 'UNEXPLAINED'
    )
    assert len(entries) == sum(r.reason_status == 'UNEXPLAINED' for r in baseline.records)
    category_counts = Counter(entry.category for entry in entries)
    candidate_counts = Counter(
        kind for entry in entries for kind in entry.existing_reason_kinds
    )
    summary = {
        'status': 'R3H_INVENTORY_ONLY_NOT_FULL_PROOF',
        'node_count': len(baseline.records),
        'edge_count': baseline.checked_edge_count,
        'given_count': sum(r.reason_status == 'GIVEN' for r in baseline.records),
        'already_explained_count': sum(r.reason_status == 'EXPLAINED' for r in baseline.records),
        'unexplained_count': len(entries),
        'category_counts': dict(sorted(category_counts.items())),
        'direct_builder_matches': dict(sorted(candidate_counts.items())),
        'classified_indices': [entry.index for entry in entries],
        'all_nodes_once': len({id(r.step) for r in baseline.records}) == len(baseline.records),
        'dependency_first': all(p < r.index for r in baseline.records for p in r.premise_indices),
        'root_is_last': baseline.records[-1].step is presentation.root_step,
        'historical_markdown_used_as_input': False,
        'public_renderer_changed': False,
        'existing_reason_implementation_changed': False,
        'full_proof_semantic_certification': False,
        'limitations': [
            'NO_DIRECT_MATCH_REVIEW_REQUIRED does not mean a new rule is necessary.',
            'Context-dependent definition/aggregate reasons are not built in this direct-premise audit.',
            'Broad FINAL_RESULT_DERIVATION labels are not evidence of a validated implication.',
            'Builder matches and prose availability are not independent proof validation.',
        ],
    }
    return entries, summary
