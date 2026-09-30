from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_equation_numbering import (
  number_toda_group_proof_narrative_equations,
)
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)


def main():
  presentation, blocks, sidecar, arguments = _method_evidence_data(3, 3)
  reason_sidecar = build_toda_group_proof_narrative_reason_sidecar(
    presentation,
    sidecar,
  )
  reason = next(
    item
    for item in reason_sidecar.reasons
    if (
      item.kind
      is TodaGroupProofNarrativeReasonKind.MULTIPLE_RELATION_TO_ORDER
    )
  )
  order_step = reason.premise_steps[0]
  equality_step = reason.premise_steps[1]
  conclusion_step = reason.conclusion_step

  order_plain = _render_generic_narrative_step(order_step)
  equality_plain = _render_generic_narrative_step(equality_step)
  conclusion_plain = _render_generic_narrative_step(conclusion_step)
  reason_sentence = render_toda_group_proof_narrative_reason_sentence(reason)

  numbered_base = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    sidecar,
    arguments,
  )
  final_markdown = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  tagged_equality = equality_plain[:-1] + r"\tag{3}$"
  connector = "(1) と (2) より、"

  print("=" * 78)
  print("Phase 150 / RC4-5D-4-R1 audit harness repair")
  print("=" * 78)

  print("A. Typed dependency identity")
  print(
    "direct premises are order/equality:",
    tuple(conclusion_step.premises) == (order_step, equality_step),
  )
  print("order plain:", order_plain)
  print("equality plain:", equality_plain)
  print("conclusion plain:", conclusion_plain)

  print("-" * 78)
  print("B. Equation-numbering path")
  print("plain equality in numbered base:", equality_plain in numbered_base)
  print("tagged equality in numbered base:", tagged_equality in numbered_base)
  print("connector in numbered base:", connector in numbered_base)
  print("tagged equality in final:", tagged_equality in final_markdown)
  print("connector in final:", connector in final_markdown)

  print("-" * 78)
  print("C. Final positions")
  order_pos = final_markdown.find(order_plain)
  reason_pos = final_markdown.find(reason_sentence)
  conclusion_pos = final_markdown.find(conclusion_plain)
  connector_pos = final_markdown.find(connector)
  tagged_equality_pos = final_markdown.find(tagged_equality)
  print("order position:", order_pos)
  print("reason position:", reason_pos)
  print("conclusion position:", conclusion_pos)
  print("connector position:", connector_pos)
  print("tagged equality position:", tagged_equality_pos)
  print(
    "reason before conclusion:",
    0 <= reason_pos < conclusion_pos,
  )
  print(
    "tagged equality after conclusion:",
    conclusion_pos < connector_pos < tagged_equality_pos,
  )

  print("-" * 78)
  print("D. Boundary diagnosis")
  if not (
    tuple(conclusion_step.premises) == (order_step, equality_step)
    and tagged_equality in numbered_base
    and connector in numbered_base
    and tagged_equality in final_markdown
    and connector in final_markdown
    and 0 <= reason_pos < conclusion_pos
    and conclusion_pos < connector_pos < tagged_equality_pos
  ):
    print("AUDIT_RESULT=FAIL")
    raise SystemExit(1)

  print(
    "ORDERING_GAP=typed direct equality premise is rendered through the "
    "calculation/equation-numbering stream after the order conclusion"
  )
  print(
    "RC3_SCOPE=hidden contribution ordering does not own this numbered "
    "calculation-chain placement"
  )
  print(
    "EQUATION_PATH=toda_group_proof_narrative_argument_multi_renderer -> "
    "number_toda_group_proof_narrative_equations"
  )
  print(
    "RC4_ACTION=do not move equation tags or calculation-chain numbering"
  )
  print(
    "RC6_BOUNDARY=final equation numbering/prose formatting is downstream "
    "of the selected/ordered Narrative stream"
  )
  print(
    "FOLLOWUP=record the ordering pressure; defer numbered calculation "
    "stream relocation until RC6 unless RC4 reason selection itself "
    "requires a structural prerequisite change"
  )
  print("AUDIT_RESULT=PASS")


if __name__ == "__main__":
  main()
