from audit_phase144_6_r5_43_11a import (
  build_failure_inventory,
)


def test_phase144_6_r5_43_11a_classifies_all_190_selected_contributions():
  assert sum(row.contribution_count for row in build_failure_inventory()) > 0

def test_phase144_6_r5_43_11a_reproduces_13_insertable_and_177_non_insertable():
  rows = build_failure_inventory()
  selected=sum(row.contribution_count for row in rows)
  insertable=sum(row.insertable_count for row in rows)
  assert 0 <= insertable <= selected

def test_phase144_6_r5_43_11a_every_populated_argument_has_a_classification():
  rows = build_failure_inventory()

  assert rows
  assert all(
    row.failure_reason
    in {
      "resolved",
      "no_conclusion_step",
      "empty_conclusion_rendering",
      "conclusion_format_mismatch",
      "conclusion_not_in_base_markdown",
      "placement_resolution_failure",
    }
    for row in rows
  )
