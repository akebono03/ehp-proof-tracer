from audit_phase144_6_r5_17a import (
  TARGET,
  audit_argument_chain,
  audit_pi6_3,
  build_context,
)


def test_phase144_6_r5_17a_pi6_3_has_three_argument_chain_roots():
  audits = audit_pi6_3()

  assert len(audits) == 3
  assert tuple(audit.argument_role for audit in audits) == (
    "establish_group_structure",
    "establish_order",
    "establish_definition",
  )


def test_phase144_6_r5_17a_starts_from_unique_argument_conclusion_steps():
  presentation, blocks, arguments, contributions = build_context(*TARGET)

  audits = tuple(
    audit_argument_chain(
      presentation,
      blocks,
      arguments,
      contributions,
      argument_index,
    )
    for argument_index in range(len(arguments))
  )

  assert all(audit.reached_step_count >= 1 for audit in audits)
  assert all(audit.edge_count >= 1 for audit in audits)
  assert all(audit.conclusion_statement_type for audit in audits)


def test_phase144_6_r5_17a_uses_semantic_contributions_not_fixed_depth():
  audits = audit_pi6_3()

  observed_contributions = {
    contribution
    for audit in audits
    for contribution, count in audit.contribution_counts
    if count > 0
  }

  assert "establish_group" in observed_contributions
  assert "provide_reference" in observed_contributions
  assert (
    "establish_exactness" in observed_contributions
    or "establish_map" in observed_contributions
    or "establish_relation" in observed_contributions
  )


def test_phase144_6_r5_17a_records_chain_roles_and_statement_types():
  audits = audit_pi6_3()

  assert all(
    edge.parent_role
    and edge.premise_role
    and edge.contribution
    and edge.premise_statement_type
    for audit in audits
    for edge in audit.edges
  )
