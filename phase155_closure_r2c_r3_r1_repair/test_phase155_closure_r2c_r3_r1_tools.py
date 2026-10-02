from apply_phase155_closure_r2c_r3_r1 import (
  REPLACEMENTS,
)


def test_r2c_r3_r1_repairs_exactly_three_functions():
  assert len(
    REPLACEMENTS
  ) == 3


def test_both_phase96_repairs_import_toda_group_query_locally():
  phase96 = tuple(
    text
    for (
      path,
      name,
    ), text in REPLACEMENTS.items()
    if path.endswith(
      "test_phase96_proof_step_source_presentation.py"
    )
  )

  assert len(
    phase96
  ) == 2
  assert all(
    "from toda_group_query import (" in text
    for text in phase96
  )
  assert all(
    "TodaGroupQuery," in text
    for text in phase96
  )


def test_boundary_repair_accepts_phase144_and_phase153_only():
  text = REPLACEMENTS[
    (
      "tests/test_phase155_audit_boundary.py",
      "test_phase155_audit_boundary_contains_only_phase144_tests",
    )
  ]

  assert "test_phase144_" in text
  assert "test_phase153_" in text


def test_boundary_repair_does_not_broaden_to_arbitrary_tests():
  text = REPLACEMENTS[
    (
      "tests/test_phase155_audit_boundary.py",
      "test_phase155_audit_boundary_contains_only_phase144_tests",
    )
  ]

  assert "or nodeid.startswith(" in text
  assert "phase154" not in text


def test_repair_keeps_top_level_imports_unchanged():
  assert all(
    replacement.startswith(
      "def "
    )
    for replacement in REPLACEMENTS.values()
  )
