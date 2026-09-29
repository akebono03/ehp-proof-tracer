from audit_phase144_6_r5_17a_r3 import (
  SupportCorrespondenceKind,
  audit_pi6_3,
)


def test_phase144_6_r5_17a_r3_preserves_three_pi6_3_arguments():
  audits = audit_pi6_3()

  assert len(audits) == 3
  assert tuple(audit.argument_role for audit in audits) == (
    "establish_group_structure",
    "establish_order",
    "establish_definition",
  )


def test_phase144_6_r5_17a_r3_classifies_a03_precondition_as_semantic_only():
  audits = audit_pi6_3()
  definition_audit = audits[2]

  assert definition_audit.direct_presentation_provider_step_count == 0
  assert definition_audit.direct_semantic_provider_step_count == 1
  assert len(definition_audit.supporting_blocks) == 1

  support = definition_audit.supporting_blocks[0]

  assert support.block_role == "precondition"
  assert (
    support.correspondence
    is SupportCorrespondenceKind.SEMANTIC_ONLY_BLOCK
  )
  assert support.direct_presentation_step_count == 0
  assert support.direct_semantic_step_count == 1


def test_phase144_6_r5_17a_r3_classifies_a01_order_as_child_argument_replacement():
  audits = audit_pi6_3()
  group_audit = audits[0]

  assert len(group_audit.child_arguments) == 1
  child = group_audit.child_arguments[0]

  assert child.child_argument_index == 1
  assert child.child_argument_role == "establish_order"
  assert child.child_conclusion_block_role == "order"
  assert (
    child.correspondence
    is SupportCorrespondenceKind.CHILD_ARGUMENT_REPLACEMENT
  )
  assert child.direct_presentation_step_count >= 1


def test_phase144_6_r5_17a_r3_finds_presentation_correspondence_for_nonsemantic_support():
  audits = audit_pi6_3()

  nonsemantic_support = tuple(
    support
    for audit in audits
    for support in audit.supporting_blocks
    if (
      support.correspondence
      is not SupportCorrespondenceKind.SEMANTIC_ONLY_BLOCK
    )
  )

  assert nonsemantic_support
  assert all(
    support.direct_presentation_step_count >= 1
    for support in nonsemantic_support
  )


def test_phase144_6_r5_17a_r3_observes_partial_block_granularity():
  audits = audit_pi6_3()

  partial = tuple(
    support
    for audit in audits
    for support in audit.supporting_blocks
    if (
      support.correspondence
      is SupportCorrespondenceKind.PARTIAL_PRESENTATION_BLOCK
    )
  )

  assert partial
  assert all(
    support.block_step_count
    > support.direct_presentation_step_count
    for support in partial
  )
