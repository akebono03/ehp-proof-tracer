from __future__ import annotations

from phase155_closure_r2b_audit import (
  _duration_map,
  _runtime_class,
  _superseded_by,
)


def test_runtime_thresholds_are_explicit():
  assert (
    _runtime_class(
      508.30
    )
    == "EXTREME_120S_PLUS"
  )
  assert (
    _runtime_class(
      45.0
    )
    == "VERY_HEAVY_30S_PLUS"
  )
  assert (
    _runtime_class(
      12.0
    )
    == "HEAVY_10S_PLUS"
  )
  assert (
    _runtime_class(
      6.0
    )
    == "MODERATE_5S_PLUS"
  )
  assert (
    _runtime_class(
      1.0
    )
    == "LIGHT_UNDER_5S"
  )


def test_unmeasured_runtime_is_not_guessed():
  assert (
    _runtime_class(
      None
    )
    == "UNMEASURED_TOP50"
  )


def test_duration_parser_keeps_largest_phase_duration():
  text = (
    "2.00s setup    tests/test_phase144_x.py::test_a\n"
    "15.00s call     tests/test_phase144_x.py::test_a\n"
  )

  result = _duration_map(
    text
  )

  assert result[
    "tests/test_phase144_x.py::test_a"
  ] == 15.0


def test_final_completion_marks_earlier_completion_audit_as_superseded_candidate():
  assert (
    _superseded_by(
      "test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py"
    )
    == (
      "test_phase144_6_r5_43_11d_final_completion_audit.py"
    )
  )


def test_transport_discovery_stages_have_final_completion_comparison_target():
  assert (
    _superseded_by(
      "test_phase144_6_r5_43_8.py"
    )
    == (
      "test_phase144_6_r5_43_11d_final_completion_audit.py"
    )
  )
  assert (
    _superseded_by(
      "test_phase144_6_r5_43_9.py"
    )
    == (
      "test_phase144_6_r5_43_11d_final_completion_audit.py"
    )
  )
