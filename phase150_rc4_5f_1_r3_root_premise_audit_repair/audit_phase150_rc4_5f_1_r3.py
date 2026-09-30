from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from homotopy_groups import (
  FiniteCyclicGroup,
)
from proof import (
  Relation,
  RelationType,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
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
from toda_rules import (
  TodaHopfInvariantSurjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
)


def _rule_name(proof_step):
  inference_rule = proof_step.inference_rule
  if inference_rule is None:
    return None
  return inference_rule.name


def _is_order_four(statement):
  return (
    isinstance(statement, Relation)
    and statement.relation_type is RelationType.ORDER
    and statement.rhs == 4
  )


def _is_finite_cyclic_order_two(statement):
  return (
    isinstance(statement, Relation)
    and statement.relation_type is RelationType.EQUALITY
    and isinstance(statement.rhs, FiniteCyclicGroup)
    and statement.rhs.order == 2
  )


def main():
  presentation, blocks, _sidecar, _arguments = (
    _method_evidence_data(3, 3)
  )

  root_step = presentation.root_step
  root_statement = root_step.conclusion

  print("=" * 78)
  print("Phase 150 / RC4-5F-1-R3 root-premise reason-chain audit")
  print("=" * 78)

  print("A. Root conclusion")
  print("root type:", type(root_statement).__name__)
  print("root rendered:", _render_generic_narrative_step(root_step))
  print("root rule:", _rule_name(root_step))
  print("root premise count:", len(root_step.premises))

  root_is_expected_finite_cyclic = (
    isinstance(root_statement, Relation)
    and root_statement.relation_type is RelationType.EQUALITY
    and isinstance(root_statement.rhs, FiniteCyclicGroup)
    and root_statement.rhs.order == 4
  )
  print(
    "ROOT_FINITE_CYCLIC_ORDER_FOUR=",
    root_is_expected_finite_cyclic,
  )

  order_steps = tuple(
    premise
    for premise in root_step.premises
    if _is_order_four(premise.conclusion)
  )
  membership_steps = tuple(
    premise
    for premise in root_step.premises
    if isinstance(
      premise.conclusion,
      HomotopyGroupMembershipStatement,
    )
  )
  endpoint_group_steps = tuple(
    premise
    for premise in root_step.premises
    if _is_finite_cyclic_order_two(premise.conclusion)
  )
  injective_steps = tuple(
    premise
    for premise in root_step.premises
    if isinstance(
      premise.conclusion,
      TodaSuspensionInjectiveStatement,
    )
  )
  exactness_steps = tuple(
    premise
    for premise in root_step.premises
    if isinstance(
      premise.conclusion,
      TodaProp42ExactnessStatement,
    )
  )
  surjective_steps = tuple(
    premise
    for premise in root_step.premises
    if isinstance(
      premise.conclusion,
      TodaHopfInvariantSurjectiveStatement,
    )
  )

  print("-" * 78)
  print("B. Root direct premises")
  for index, premise in enumerate(root_step.premises):
    print(
      f"[{index}]",
      type(premise.conclusion).__name__,
      _render_generic_narrative_step(premise),
      "| rule:",
      _rule_name(premise),
    )

  print("-" * 78)
  print("C. Typed direct-premise classification")
  print("DIRECT_ORDER_FOUR_COUNT=", len(order_steps))
  print("DIRECT_MEMBERSHIP_COUNT=", len(membership_steps))
  print("DIRECT_ENDPOINT_Z2_COUNT=", len(endpoint_group_steps))
  print("DIRECT_INJECTIVE_COUNT=", len(injective_steps))
  print("DIRECT_EXACTNESS_COUNT=", len(exactness_steps))
  print("DIRECT_SURJECTIVE_COUNT=", len(surjective_steps))

  short_exact_records = []
  for block_index, block in enumerate(blocks):
    if (
      block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
    ):
      continue

    contributions = (
      extract_toda_group_proof_narrative_exactness_display_contributions(
        presentation,
        block,
      )
    )

    for contribution in contributions:
      if (
        contribution.kind
        is TodaGroupProofNarrativeExactnessDisplayContributionKind
        .DERIVED_SHORT_EXACT_SEQUENCE
      ):
        short_exact_records.append(
          (
            block_index,
            contribution.proof_step,
            contribution.latex,
          )
        )

  print("-" * 78)
  print("D. Derived short-exact contribution")
  print("SHORT_EXACT_COUNT=", len(short_exact_records))
  short_exact_uses_root_exactness = False

  for block_index, proof_step, latex in short_exact_records:
    helper_latex = _generic_short_exact_sequence_latex(
      presentation,
      proof_step,
    )
    root_owned = any(
      proof_step is exactness_step
      for exactness_step in exactness_steps
    )
    short_exact_uses_root_exactness = (
      short_exact_uses_root_exactness
      or root_owned
    )

    print("block:", block_index)
    print("sequence:", latex)
    print("typed helper agrees:", helper_latex == latex)
    print("exactness is root direct premise:", root_owned)

  print(
    "SHORT_EXACT_USES_ROOT_EXACTNESS=",
    short_exact_uses_root_exactness,
  )

  structural_direct_chain = (
    len(endpoint_group_steps) == 2
    and len(injective_steps) == 1
    and len(exactness_steps) == 1
    and len(surjective_steps) == 1
    and len(short_exact_records) == 1
    and short_exact_uses_root_exactness
  )
  generator_direct_chain = (
    len(order_steps) == 1
    and len(membership_steps) == 1
  )

  print("-" * 78)
  print("E. Reason-chain diagnosis")
  print(
    "STRUCTURAL_DIRECT_CHAIN=",
    structural_direct_chain,
  )
  print(
    "GENERATOR_DIRECT_CHAIN=",
    generator_direct_chain,
  )

  print(
    "SHORT_EXACT_TO_GROUP_ORDER="
    + (
      "SAFE_AS_PRESENTATION_REASON_DECOMPOSITION"
      if structural_direct_chain
      else "NOT_CONFIRMED"
    )
  )
  print(
    "INTERMEDIATE_GROUP_ORDER_PROOF_STEP="
    + (
      "ABSENT"
      if structural_direct_chain
      else "UNRESOLVED"
    )
  )
  print(
    "MEMBER_OF_FULL_ORDER_GENERATES="
    + (
      "SAFE_AS_FINAL_REASON_DECOMPOSITION"
      if generator_direct_chain
      else "NOT_CONFIRMED"
    )
  )

  audit_pass = (
    root_is_expected_finite_cyclic
    and structural_direct_chain
    and generator_direct_chain
  )

  print(
    "RC4_5F_2_BOUNDARY="
    "reason sidecar may decompose the existing final rule's typed direct "
    "premises for prose, but must not invent a new group-order ProofStep"
  )
  print("AUDIT_RESULT=" + ("PASS" if audit_pass else "FAIL"))

  if not audit_pass:
    raise SystemExit(1)


if __name__ == "__main__":
  main()
