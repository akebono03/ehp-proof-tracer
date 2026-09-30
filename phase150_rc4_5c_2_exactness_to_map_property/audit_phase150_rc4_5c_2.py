from tests.test_phase143_19_method_evidence import _method_evidence_data
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


def main():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(3, 3)

  sidecar = build_toda_group_proof_narrative_reason_sidecar(
    presentation,
    semantic_sidecar,
  )
  reasons = tuple(
    reason
    for reason in sidecar.reasons
    if reason.kind
    is TodaGroupProofNarrativeReasonKind.EXACTNESS_TO_MAP_PROPERTY
  )

  if len(reasons) != 1:
    raise AssertionError(
      f"expected one EXACTNESS_TO_MAP_PROPERTY reason, found {len(reasons)}"
    )

  sentence = render_toda_group_proof_narrative_reason_sentence(
    reasons[0]
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  print("=" * 78)
  print("Phase 150 / RC4-5C-2 visible Narrative audit")
  print("=" * 78)
  print("reason kind:", reasons[0].kind.value)
  print("premise types:", tuple(
    type(step.conclusion).__name__
    for step in reasons[0].premise_steps
  ))
  print("reason prose:")
  print(sentence)
  print("-" * 78)

  index = rendered.find(sentence)
  if index < 0:
    raise AssertionError("reason prose is not visible")

  start = max(0, index - 350)
  end = min(len(rendered), index + len(sentence) + 350)
  print(rendered[start:end])
  print("-" * 78)

  if rendered.count(sentence) != 1:
    raise AssertionError("reason prose must be visible exactly once")

  print("TYPED_REASON=PASS")
  print("VISIBLE_REASON=PASS")
  print("AUDIT_RESULT=PASS")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
