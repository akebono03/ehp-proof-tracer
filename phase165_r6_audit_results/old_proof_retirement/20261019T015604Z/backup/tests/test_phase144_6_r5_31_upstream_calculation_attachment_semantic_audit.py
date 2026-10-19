from audit_phase144_6_r5_31 import (
  HOPF_KEYS,
  build_attachment_semantic_records,
  build_pi6_hopf_semantic_records,
)


def test_phase144_6_r5_31_classifies_phase30_attachment_occurrences():
  records = build_attachment_semantic_records()

  assert len(records) == 198


def test_phase144_6_r5_31_all_attachments_are_calculation_statements_with_types():
  records = build_attachment_semantic_records()

  assert records
  assert all(row.statement_type for row in records)


def test_phase144_6_r5_31_records_frontier_visibility_for_every_attachment():
  records = build_attachment_semantic_records()

  assert all(isinstance(row.frontier_hidden, bool) for row in records)


def test_phase144_6_r5_31_records_target_role_for_every_attachment():
  records = build_attachment_semantic_records()

  assert all(row.target_block_role for row in records)


def test_phase144_6_r5_31_pi6_records_both_hopf_keys():
  rows = build_pi6_hopf_semantic_records()

  assert {row.key for row in rows} == set(HOPF_KEYS)


def test_phase144_6_r5_31_pi6_has_required_attached_hopf_occurrences():
  rows = build_pi6_hopf_semantic_records()

  assert any(
    row.key == "hopf_nu_prime"
    and row.argument_index == 0
    and row.attached
    for row in rows
  )
  assert any(
    row.key == "hopf_nu_eta6"
    and row.argument_index == 1
    and row.attached
    for row in rows
  )
