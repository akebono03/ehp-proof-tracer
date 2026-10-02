from phase155_closure_r2c_r1_audit import (
  _phase_family,
  _runtime_class,
)


def test_runtime_class_marks_extreme_tests():
  assert (
    _runtime_class(
      508.30
    )
    == "EXTREME_120S_PLUS"
  )
  assert (
    _runtime_class(
      281.49
    )
    == "EXTREME_120S_PLUS"
  )
  assert (
    _runtime_class(
      276.88
    )
    == "EXTREME_120S_PLUS"
  )


def test_runtime_class_keeps_ordinary_thresholds():
  assert (
    _runtime_class(
      30.0
    )
    == "VERY_HEAVY_30S_PLUS"
  )
  assert (
    _runtime_class(
      10.0
    )
    == "HEAVY_10S_PLUS"
  )
  assert (
    _runtime_class(
      None
    )
    == "UNMEASURED_TOP50"
  )


def test_phase_family_recognizes_phase95_to_98():
  assert (
    _phase_family(
      "tests/test_phase95_x.py"
    )
    == "PHASE95"
  )
  assert (
    _phase_family(
      "tests/test_phase97_x.py"
    )
    == "PHASE97"
  )
  assert (
    _phase_family(
      "tests/test_phase98_x.py"
    )
    == "PHASE98"
  )


def test_phase_family_recognizes_phase153():
  assert (
    _phase_family(
      "tests/test_phase153_r3_x.py"
    )
    == "PHASE153"
  )


def test_other_phase_is_not_silently_reclassified():
  assert (
    _phase_family(
      "tests/test_phase144_x.py"
    )
    == "OTHER"
  )
