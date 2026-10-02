from __future__ import annotations

import ast

from apply_phase155_closure_r2b_r3 import (
  EXPECTED_DELETE_FUNCTIONS,
  EXPECTED_KEEP_FUNCTION,
  REPLACEMENT,
  _remove_functions,
  _replace_function,
)


def test_r2b_r3_has_exactly_eight_reviewed_delete_functions():
  assert len(
    EXPECTED_DELETE_FUNCTIONS
  ) == 8


def test_r2b_r3_has_one_reviewed_lightweight_function():
  assert EXPECTED_KEEP_FUNCTION == (
    "test_phase144_6_r5_43_11_has_no_contribution_duplicates_or_order_violations"
  )


def test_lightweight_replacement_uses_one_representative_group():
  assert "_context(" in REPLACEMENT
  assert "3," in REPLACEMENT
  assert "build_completion_inventory" not in REPLACEMENT


def test_lightweight_replacement_checks_identity_and_dependency_order():
  compact = "".join(
    REPLACEMENT.split()
  )

  assert "len(set(step_ids))" in compact
  assert "reachable(" in REPLACEMENT
  assert "position_by_id" in REPLACEMENT


def test_remove_and_replace_helpers_preserve_parseable_module():
  source = (
    "def first():\n"
    "  assert True\n\n"
    "def second():\n"
    "  assert False\n\n"
    "def third():\n"
    "  return 3\n"
  )

  removed = _remove_functions(
    source,
    {
      "first",
    },
  )

  replaced = _replace_function(
    removed,
    "second",
    (
      "def second():\n"
      "  assert True\n"
    ),
  )

  ast.parse(
    replaced
  )

  assert "def first" not in replaced
  assert "assert False" not in replaced
  assert "def third" in replaced
