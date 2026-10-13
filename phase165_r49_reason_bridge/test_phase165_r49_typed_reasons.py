from pathlib import Path

from phase165_r14_r45_proofstep_rule_audit.audit import audit_proofstep_rules
from phase165_r14_r41_proof_transfer import build_phase165_r41_pi32_common_replay
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_narrative_reasons import (
    TodaGroupProofNarrativeReasonKind,
    build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_reason_renderer import render_toda_group_proof_narrative_reason_sentence


def test_phase165_r49_real_pi32_typed_reason_chain():
    report = build_standard_toda_report(n=2, k=1)
    result = report.candidates[0].source_candidate.group_result
    replay = build_phase165_r41_pi32_common_replay(result, 2, 'narrative')
    presentation = build_toda_group_proof_presentation(replay)
    semantic = build_toda_group_proof_narrative_semantic_sidecar(presentation)
    sidecar = build_toda_group_proof_narrative_reason_sidecar(presentation, semantic)
    by_kind = {reason.kind: reason for reason in sidecar.reasons}
    for kind in (
        TodaGroupProofNarrativeReasonKind.EXACTNESS_TO_DELTA_ZERO,
        TodaGroupProofNarrativeReasonKind.INJECTIVE_SURJECTIVE_TO_ISOMORPHISM,
    ):
        assert kind in by_kind
        reason = by_kind[kind]
        assert len(reason.premise_steps) == 2
        assert all(p in reason.conclusion_step.premises for p in reason.premise_steps)
        assert render_toda_group_proof_narrative_reason_sentence(reason)
