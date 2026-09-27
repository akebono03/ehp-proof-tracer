from audit_phase144_6_r5_17a_r2 import (
  AuditEdgeKind,
  audit_pi6_3,
)


def test_phase144_6_r5_17a_r2_preserves_three_pi6_3_arguments():
  audits = audit_pi6_3()

  assert len(audits) == 3
  assert tuple(audit.argument_role for audit in audits) == (
    "establish_group_structure",
    "establish_order",
    "establish_definition",
  )


def test_phase144_6_r5_17a_r2_recovers_a03_precondition_support_without_presentation_edge():
  audits = audit_pi6_3()
  definition_audit = audits[2]

  assert definition_audit.argument_role == "establish_definition"
  assert definition_audit.presentation_edges == ()
  assert tuple(
    edge.provider_role
    for edge in definition_audit.supporting_block_edges
  ) == ("precondition",)
  assert all(
    edge.kind is AuditEdgeKind.SUPPORTING_BLOCK
    for edge in definition_audit.supporting_block_edges
  )


def test_phase144_6_r5_17a_r2_recovers_a01_order_child_argument_support():
  audits = audit_pi6_3()
  group_audit = audits[0]

  assert len(group_audit.child_argument_edges) == 1
  edge = group_audit.child_argument_edges[0]

  assert edge.kind is AuditEdgeKind.CHILD_ARGUMENT
  assert edge.child_argument_index == 1
  assert edge.consumer_role == "target"
  assert edge.provider_role == "establish_order"


def test_phase144_6_r5_17a_r2_keeps_edge_kinds_distinct():
  audits = audit_pi6_3()

  observed = {
    edge.kind
    for audit in audits
    for edge in audit.all_edges
  }

  assert observed == {
    AuditEdgeKind.PRESENTATION,
    AuditEdgeKind.SUPPORTING_BLOCK,
    AuditEdgeKind.CHILD_ARGUMENT,
  }


def test_phase144_6_r5_17a_r2_does_not_require_recursive_dependency_closure():
  audits = audit_pi6_3()

  assert sum(
    len(audit.presentation_edges)
    for audit in audits
  ) < 20
  assert all(
    edge.consumer_argument_index == audit.argument_index
    for audit in audits
    for edge in audit.all_edges
  )
