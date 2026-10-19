from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)


def _reason_sidecar(n, k):
  presentation, _, semantic_sidecar, _ = (
    _method_evidence_data(n, k)
  )
  return (
    presentation,
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    ),
  )


def test_phase150_rc4_closure_pi10_4_filters_hidden_recursive_reason_steps():
  presentation, reason_sidecar = _reason_sidecar(4, 6)
  visible_step_ids = {
    id(node.proof_step)
    for node in presentation.nodes
  }

  for reason in reason_sidecar.reasons:
    assert id(reason.conclusion_step) in visible_step_ids
    assert all(
      id(premise) in visible_step_ids
      for premise in reason.premise_steps
    )

  internal_pi6_step = presentation.nodes[17].proof_step
  assert not any(
    (
      reason.kind
      is TodaGroupProofNarrativeReasonKind.FINAL_GROUP_STRUCTURE
    )
    and reason.conclusion_step is internal_pi6_step
    for reason in reason_sidecar.reasons
  )


def test_phase150_rc4_closure_pi6_3_keeps_visible_final_group_reason():
  _, reason_sidecar = _reason_sidecar(3, 3)
  final_reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind.FINAL_GROUP_STRUCTURE
    )
  )
  assert len(final_reasons) == 1


def test_phase150_rc4_closure_pi8_5_keeps_visible_final_group_reason():
  _, reason_sidecar = _reason_sidecar(5, 3)
  final_reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind.FINAL_GROUP_STRUCTURE
    )
  )
  assert len(final_reasons) == 1
