from expression import Multiple
from proof import Relation, RelationType
from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)


def normalized(text):
  return "".join(text.split())


def main():
  presentation, blocks, semantic_sidecar, arguments = (
    _method_evidence_data(3, 3)
  )
  proof_chains = build_toda_group_proof_narrative_proof_chains(
    presentation,
    semantic_sidecar,
    arguments,
  )
  base_markdown = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )
  ordered_contributions = build_toda_group_proof_narrative_ordered_contributions(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
    current_markdown=base_markdown,
  )
  final_markdown = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  reason_sidecar = build_toda_group_proof_narrative_reason_sidecar(
    presentation,
    semantic_sidecar,
  )
  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind.MULTIPLE_RELATION_TO_ORDER
    )
  )

  order_step = reason.premise_steps[0]
  equality_step = reason.premise_steps[1]
  conclusion_step = reason.conclusion_step

  equality = equality_step.conclusion
  assert isinstance(equality, Relation)
  assert equality.relation_type is RelationType.EQUALITY
  assert isinstance(equality.lhs, Multiple)

  print("=" * 78)
  print("Phase 150 / RC4-5D-4 order reason presentation-order audit")
  print("=" * 78)
  print("A. Typed reason dependency")
  print("order premise:", order_step.conclusion)
  print("equality premise:", equality_step.conclusion)
  print("conclusion:", conclusion_step.conclusion)
  print(
    "direct premise identity:",
    tuple(conclusion_step.premises) == (order_step, equality_step),
  )
  print(
    "presentation contains all:",
    all(
      any(node.proof_step is step for node in presentation.nodes)
      for step in (order_step, equality_step, conclusion_step)
    ),
  )

  equality_line = _render_generic_narrative_step(equality_step)
  order_line = _render_generic_narrative_step(order_step)
  conclusion_line = _render_generic_narrative_step(conclusion_step)
  reason_sentence = render_toda_group_proof_narrative_reason_sentence(reason)

  print("-" * 78)
  print("B. Generic rendered lines")
  print("order line:", order_line)
  print("equality line:", equality_line)
  print("conclusion line:", conclusion_line)
  print("reason sentence:", repr(reason_sentence))

  print("-" * 78)
  print("C. Base Narrative visibility")
  print(
    "order premise already visible:",
    normalized(order_line) in normalized(base_markdown),
  )
  print(
    "equality premise already visible:",
    normalized(equality_line) in normalized(base_markdown),
  )
  print(
    "conclusion already visible:",
    normalized(conclusion_line) in normalized(base_markdown),
  )

  contribution_steps = tuple(
    contribution.proof_step
    for contributions in ordered_contributions
    for contribution in contributions
  )
  print("-" * 78)
  print("D. RC3 ordered contribution membership")
  print(
    "order premise selected contribution:",
    any(step is order_step for step in contribution_steps),
  )
  print(
    "equality premise selected contribution:",
    any(step is equality_step for step in contribution_steps),
  )
  print(
    "conclusion selected contribution:",
    any(step is conclusion_step for step in contribution_steps),
  )
  for argument_index, contributions in enumerate(ordered_contributions):
    if not contributions:
      continue
    print("argument", argument_index)
    for index, contribution in enumerate(contributions):
      print(
        " ",
        index,
        contribution.placement.value,
        _render_generic_narrative_step(contribution.proof_step),
      )

  print("-" * 78)
  print("E. Final Narrative positions")
  order_pos = final_markdown.find(order_line)
  equality_pos = final_markdown.find(equality_line)
  conclusion_pos = final_markdown.find(conclusion_line)
  reason_pos = (
    final_markdown.find(reason_sentence)
    if reason_sentence is not None
    else -1
  )
  print("order position:", order_pos)
  print("equality position:", equality_pos)
  print("reason position:", reason_pos)
  print("conclusion position:", conclusion_pos)
  print(
    "typed dependency order expected:",
    "order/equality before conclusion",
  )
  print(
    "actual equality before conclusion:",
    0 <= equality_pos < conclusion_pos,
  )
  print(
    "reason before conclusion:",
    0 <= reason_pos < conclusion_pos,
  )

  print("-" * 78)
  print("F. Diagnosis")
  equality_visible = normalized(equality_line) in normalized(base_markdown)
  equality_contribution = any(
    step is equality_step
    for step in contribution_steps
  )
  if equality_visible and not equality_contribution and equality_pos > conclusion_pos:
    print(
      "ORDERING_GAP=visible direct premise is outside RC3 hidden-contribution relocation"
    )
    print(
      "RC3_SCOPE=working as designed for hidden explanatory contributions"
    )
    print(
      "NEXT_RULE=reason-aware direct-premise presentation ordering"
    )
    print("SAFE_TO_MOVE_WITHOUT_AUDIT=NO")
    print("AUDIT_RESULT=PASS")
    return

  if equality_pos < conclusion_pos:
    print("ORDERING_GAP=none")
    print("AUDIT_RESULT=PASS")
    return

  print("ORDERING_GAP=unclassified")
  print("AUDIT_RESULT=FAIL")
  raise SystemExit(1)


if __name__ == "__main__":
  main()
