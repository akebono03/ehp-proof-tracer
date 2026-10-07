
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)


def test_phase159_r1_7c_r4_repair8_final_group_reason_has_no_repeated_numeric_equality():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .FINAL_GROUP_STRUCTURE
    )
  )

  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )

  assert sentence is not None
  assert r"\operatorname{ord}(\nu')=4=4" not in sentence
  assert r"\operatorname{ord}(\nu')=4" in sentence


def test_phase159_r1_7c_r4_repair8_visible_reason_matches_public_contract():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .FINAL_GROUP_STRUCTURE
    )
  )

  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )

  assert sentence is not None

  visible_sentence = sentence.removesuffix(
    "\nしたがって, "
  )

  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  assert rendered.count(
    visible_sentence
  ) == 1
