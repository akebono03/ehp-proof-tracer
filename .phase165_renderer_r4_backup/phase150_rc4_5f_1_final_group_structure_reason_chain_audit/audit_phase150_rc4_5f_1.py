from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_generic_narrative_renderer import (
  _generic_short_exact_sequence_latex,
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  TodaGroupProofNarrativeExactnessDisplayContributionKind,
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from proof import (
  Relation,
  RelationType,
)
from toda_rules import (
  TodaPrimaryGroupMembershipStatement,
  TodaProp42ExactnessStatement,
)


def statement_text(statement):
  try:
    return render_toda_proof_statement_latex(statement)
  except Exception:
    return repr(statement)


def is_order_relation(statement):
  return (
    isinstance(statement, Relation)
    and statement.relation_type is RelationType.ORDER
  )


def is_membership(statement):
  return isinstance(
    statement,
    TodaPrimaryGroupMembershipStatement,
  )


def main():
  presentation, blocks, sidecar, arguments = _method_evidence_data(3, 3)

  print("=" * 78)
  print("Phase 150 / RC4-5F-1 final group-structure reason-chain audit")
  print("=" * 78)

  group_blocks = tuple(
    (index, block)
    for index, block in enumerate(blocks)
    if block.role
    is TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE
  )
  print("GROUP_STRUCTURE block count:", len(group_blocks))

  for index, block in group_blocks:
    print("-" * 78)
    print("GROUP_STRUCTURE block index:", index)
    print("step count:", len(block.steps))
    for step_index, step in enumerate(block.steps):
      print(
        f"  [{step_index}]",
        type(step.conclusion).__name__,
        _render_generic_narrative_step(step),
      )
      print("      rule:", getattr(step.inference_rule, "name", None))
      print("      direct premises:", len(step.premises))
      for premise_index, premise in enumerate(step.premises):
        print(
          f"        ({premise_index})",
          type(premise.conclusion).__name__,
          statement_text(premise.conclusion),
        )

  exactness_records = []
  for block_index, block in enumerate(blocks):
    if block.role is not TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS:
      continue
    contributions = extract_toda_group_proof_narrative_exactness_display_contributions(
      presentation,
      block,
    )
    for contribution in contributions:
      if (
        contribution.kind
        is TodaGroupProofNarrativeExactnessDisplayContributionKind
        .DERIVED_SHORT_EXACT_SEQUENCE
      ):
        exactness_records.append(
          (
            block_index,
            contribution.proof_step,
            contribution.latex,
          )
        )

  print("-" * 78)
  print("A. Short-exact evidence")
  print("derived short exact count:", len(exactness_records))
  for block_index, step, latex in exactness_records:
    print("  block:", block_index)
    print("  exactness type:", type(step.conclusion).__name__)
    print("  sequence:", latex)
    print(
      "  typed helper agrees:",
      _generic_short_exact_sequence_latex(
        presentation,
        step,
      ) == latex,
    )

  order_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if is_order_relation(node.proof_step.conclusion)
  )
  membership_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if is_membership(node.proof_step.conclusion)
  )

  print("-" * 78)
  print("B. Typed order evidence")
  for step in order_steps:
    print(
      " ",
      type(step.conclusion).__name__,
      statement_text(step.conclusion),
      "| rule:",
      getattr(step.inference_rule, "name", None),
    )

  print("-" * 78)
  print("C. Typed membership evidence")
  for step in membership_steps:
    print(
      " ",
      type(step.conclusion).__name__,
      statement_text(step.conclusion),
      "| rule:",
      getattr(step.inference_rule, "name", None),
    )

  print("-" * 78)
  print("D. Final group conclusion direct-premise diagnosis")
  final_candidates = []
  for block_index, block in group_blocks:
    for step in block.steps:
      rendered = _render_generic_narrative_step(step)
      if (
        "\\mathbb{Z}/4" in rendered
        and "\\nu'" in rendered
      ):
        final_candidates.append((block_index, step, rendered))

  print("final candidates:", len(final_candidates))
  direct_has_order = False
  direct_has_membership = False
  direct_has_exactness = False

  for block_index, step, rendered in final_candidates:
    print("  block:", block_index)
    print("  conclusion type:", type(step.conclusion).__name__)
    print("  conclusion:", rendered)
    print("  rule:", getattr(step.inference_rule, "name", None))
    print("  direct premise count:", len(step.premises))
    for premise in step.premises:
      statement = premise.conclusion
      print(
        "    ",
        type(statement).__name__,
        statement_text(statement),
      )
      direct_has_order = direct_has_order or is_order_relation(statement)
      direct_has_membership = direct_has_membership or is_membership(statement)
      direct_has_exactness = direct_has_exactness or isinstance(
        statement,
        TodaProp42ExactnessStatement,
      )

  print("-" * 78)
  print("E. Reason-kind diagnosis")
  short_exact_available = len(exactness_records) >= 1
  order_four_available = any(
    getattr(step.conclusion, "right", None) == 4
    for step in order_steps
  )
  membership_available = len(membership_steps) >= 1

  print("SHORT_EXACT_AVAILABLE=", short_exact_available)
  print("ORDER_FOUR_AVAILABLE=", order_four_available)
  print("MEMBERSHIP_AVAILABLE=", membership_available)
  print("FINAL_DIRECT_HAS_ORDER=", direct_has_order)
  print("FINAL_DIRECT_HAS_MEMBERSHIP=", direct_has_membership)
  print("FINAL_DIRECT_HAS_EXACTNESS=", direct_has_exactness)

  print(
    "SHORT_EXACT_TO_GROUP_ORDER="
    + (
      "PRESENTATION_EVIDENCE_EXISTS_BUT_TYPED_DERIVATION_NOT_YET_CONFIRMED"
      if short_exact_available
      else "NO_EVIDENCE"
    )
  )
  print(
    "MEMBER_OF_FULL_ORDER_GENERATES="
    + (
      "PRESENTATION_EVIDENCE_EXISTS_BUT_FINAL_DIRECT_CHAIN_NOT_YET_CONFIRMED"
      if order_four_available and membership_available
      else "INSUFFICIENT_EVIDENCE"
    )
  )

  audit_pass = (
    len(final_candidates) >= 1
    and short_exact_available
    and order_four_available
    and membership_available
  )
  print(
    "NEXT_DESIGN="
    "do not invent a reason yet; distinguish direct typed premises "
    "from presentation-level evidence before RC4-5F-2"
  )
  print("AUDIT_RESULT=" + ("PASS" if audit_pass else "FAIL"))

  if not audit_pass:
    raise SystemExit(1)


if __name__ == "__main__":
  main()
