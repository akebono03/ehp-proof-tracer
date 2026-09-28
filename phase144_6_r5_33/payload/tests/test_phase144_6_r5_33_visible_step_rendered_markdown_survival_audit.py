from audit_phase144_6_r5_33 import (
  MISSING6_KEYS,
  build_survival_records,
)


def test_phase144_6_r5_33_records_all_missing6():
  rows = build_survival_records()
  assert {row.key for row in rows} == set(MISSING6_KEYS)


def test_phase144_6_r5_33_records_all_three_pi6_arguments():
  rows = build_survival_records()
  assert {row.argument_index for row in rows} == {0, 1, 2}


def test_phase144_6_r5_33_phase20_missing6_remain_missing_in_final_generic():
  rows = build_survival_records()
  assert all(not row.final_has_requirement for row in rows)


def test_phase144_6_r5_33_hopf_facts_are_visible_and_block_kept_somewhere():
  rows = build_survival_records()
  for key in ("hopf_nu_prime", "hopf_nu_eta6"):
    assert any(
      row.key == key and row.visible and row.block_kept
      for row in rows
    )


def test_phase144_6_r5_33_visible_kept_rows_have_single_step_render_text():
  rows = build_survival_records()
  assert all(
    row.step_render
    for row in rows
    if row.visible and row.block_kept
  )


def test_phase144_6_r5_33_survival_flags_are_boolean():
  rows = build_survival_records()
  assert all(
    isinstance(row.step_render_in_body, bool)
    and isinstance(row.body_has_requirement, bool)
    and isinstance(row.final_has_requirement, bool)
    for row in rows
  )
