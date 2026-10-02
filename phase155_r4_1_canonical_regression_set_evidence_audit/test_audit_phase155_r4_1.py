
from __future__ import annotations

import ast

import audit_phase155_r4_1 as audit


def test_phase_number_parses_phase_file():
  assert (
    audit._phase_number(
      "tests/test_phase154_x.py"
    )
    == 154
  )


def test_phase_number_returns_none_for_core_file():
  assert (
    audit._phase_number(
      "tests/test_set_rules.py"
    )
    is None
  )


def test_historical_classification_has_precedence():
  category, reason, confidence = (
    audit._classify_test(
      "tests/test_phase154_x.py",
      "test_x",
      {
        "tests/test_phase154_x.py::test_x",
      },
      {
        "tests/test_phase154_x.py",
      },
    )
  )

  assert (
    category
    == audit.CATEGORY_HISTORICAL
  )
  assert confidence == 100
  assert "historical_keep" in reason


def test_focused_regression_file_is_canonical():
  category, _, confidence = (
    audit._classify_test(
      "tests/test_phase154_x.py",
      "test_x",
      set(),
      {
        "tests/test_phase154_x.py",
      },
    )
  )

  assert (
    category
    == audit.CATEGORY_CANONICAL
  )
  assert confidence == 100


def test_core_non_phase_is_canonical():
  category, _, confidence = (
    audit._classify_test(
      "tests/test_set_rules.py",
      "test_x",
      set(),
      set(),
    )
  )

  assert (
    category
    == audit.CATEGORY_CANONICAL
  )
  assert confidence == 90


def test_heavy_signal_is_separated():
  category, _, confidence = (
    audit._classify_test(
      "tests/test_phase143_all_groups_full_depth.py",
      "test_x",
      set(),
      set(),
    )
  )

  assert (
    category
    == audit.CATEGORY_HEAVY
  )
  assert confidence == 70


def test_audit_signal_is_separated():
  category, _, confidence = (
    audit._classify_test(
      "tests/test_phase143_reference_audit.py",
      "test_x",
      set(),
      set(),
    )
  )

  assert (
    category
    == audit.CATEGORY_AUDIT
  )
  assert confidence == 70


def test_test_functions_only_returns_top_level_tests(
  tmp_path,
):
  path = tmp_path / "test_x.py"
  path.write_text(
    "def helper():\n"
    "  pass\n"
    "\n"
    "def test_a():\n"
    "  assert True\n",
    encoding="utf-8",
  )

  assert (
    audit._test_functions(
      path
    )
    == [
      "test_a",
    ]
  )
