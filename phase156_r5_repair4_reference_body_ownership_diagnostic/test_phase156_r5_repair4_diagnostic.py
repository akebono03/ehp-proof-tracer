from phase156_r5_repair4_reference_body_ownership_diagnostic.diagnose_phase156_r5_repair4 import (
  TARGETS,
  _group_label,
)


def test_phase156_r5_repair4_targets_exact_four_groups():
  assert TARGETS == (
    (
      3,
      3,
    ),
    (
      4,
      6,
    ),
    (
      5,
      7,
    ),
    (
      9,
      7,
    ),
  )


def test_phase156_r5_repair4_group_label():
  assert _group_label(
    3,
    3,
  ) == "pi_6^3"
  assert _group_label(
    9,
    7,
  ) == "pi_16^9"
