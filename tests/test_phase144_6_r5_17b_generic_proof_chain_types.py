from audit_phase144_6_r5_17b import (
  GenericProofChainType,
  audit_pi6_3,
  generic_chain_type_inventory,
)


def test_phase144_6_r5_17b_extracts_three_argument_chain_sets():
  audits = audit_pi6_3()

  assert len(audits) == 3
  assert tuple(audit.argument_role for audit in audits) == (
    "establish_group_structure",
    "establish_order",
    "establish_definition",
  )


def test_phase144_6_r5_17b_extracts_child_argument_chain_type():
  inventory = generic_chain_type_inventory(audit_pi6_3())

  chain_type = GenericProofChainType(
    claim_role="target",
    provider_kind="child_argument",
    provider_role="establish_order",
  )

  assert inventory[chain_type] == 1


def test_phase144_6_r5_17b_extracts_semantic_definition_chain_type():
  inventory = generic_chain_type_inventory(audit_pi6_3())

  chain_type = GenericProofChainType(
    claim_role="definition",
    provider_kind="supporting_block",
    provider_role="precondition",
  )

  assert inventory[chain_type] == 1


def test_phase144_6_r5_17b_extracts_group_structure_support_roles():
  audits = audit_pi6_3()
  group_audit = audits[0]

  roles = {
    occurrence.chain_type.provider_role
    for occurrence in group_audit.occurrences
    if occurrence.chain_type.provider_kind == "supporting_block"
  }

  assert roles == {
    "membership",
    "group_structure",
    "map_property",
    "exactness",
  }


def test_phase144_6_r5_17b_extracts_order_support_roles():
  audits = audit_pi6_3()
  order_audit = audits[1]

  roles = {
    occurrence.chain_type.provider_role
    for occurrence in order_audit.occurrences
  }

  assert roles == {
    "calculation",
    "group_structure",
    "map_property",
  }


def test_phase144_6_r5_17b_type_identity_ignores_block_size_and_match_counts():
  audits = audit_pi6_3()

  group_structure_occurrences = tuple(
    occurrence
    for audit in audits
    for occurrence in audit.occurrences
    if (
      occurrence.chain_type.claim_role == "target"
      and occurrence.chain_type.provider_kind == "supporting_block"
      and occurrence.chain_type.provider_role == "group_structure"
    )
  )

  assert len(group_structure_occurrences) == 2
  assert len({
    occurrence.chain_type
    for occurrence in group_structure_occurrences
  }) == 1
  assert {
    occurrence.provider_block_step_count
    for occurrence in group_structure_occurrences
  } == {1, 9}
