from pathlib import Path

from proof import (
  ProofRule,
)
from test_phase68_prop58_integration import (
  build_phase68_11_data,
)
from toda_prop58_zero_bootstrap import (
  build_toda_prop58_zero_argument_step,
)
from toda_rules import (
  TodaProp58FiniteDimensionalStatement,
)


def test_phase100_12b2_zero_argument_bootstrap_derives_prop58():
  step = (
    build_toda_prop58_zero_argument_step()
  )

  assert isinstance(
    step.conclusion,
    TodaProp58FiniteDimensionalStatement,
  )

  assert step.rule == ProofRule.INFERENCE


def test_phase100_12b2_zero_argument_bootstrap_matches_existing_prop58():
  expected = build_phase68_11_data()[
    "integration_step"
  ]

  step = (
    build_toda_prop58_zero_argument_step()
  )

  assert (
    step.conclusion
    == expected.conclusion
  )


def test_phase100_12b2_zero_argument_bootstrap_preserves_six_branches():
  expected = build_phase68_11_data()[
    "integration_step"
  ]

  step = (
    build_toda_prop58_zero_argument_step()
  )

  assert tuple(
    premise.conclusion
    for premise in step.premises
  ) == tuple(
    premise.conclusion
    for premise in expected.premises
  )


def test_phase100_12b2_zero_argument_bootstrap_is_fresh():
  first = (
    build_toda_prop58_zero_argument_step()
  )
  second = (
    build_toda_prop58_zero_argument_step()
  )

  assert first is not second

  assert all(
    left is not right
    for left, right in zip(
      first.premises,
      second.premises,
    )
  )


def test_phase100_12b2_production_module_has_no_test_or_probe_import():
  source = Path(
    "toda_prop58_zero_bootstrap.py"
  ).read_text(
    encoding="utf-8",
  )

  assert "from test_phase" not in source
  assert "from probes." not in source
