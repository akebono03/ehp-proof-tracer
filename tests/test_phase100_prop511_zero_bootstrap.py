from pathlib import Path

from proof import (
  ProofRule,
)
from test_phase73_prop511_finite_dimensional_integration import (
  build_phase73_8e_data,
)
from toda_prop511_zero_bootstrap import (
  build_toda_prop511_zero_argument_step,
)
from toda_rules import (
  TodaProp511FiniteDimensionalStatement,
)


def test_phase100_12b3_zero_argument_bootstrap_derives_prop511():
  step = (
    build_toda_prop511_zero_argument_step()
  )

  assert isinstance(
    step.conclusion,
    TodaProp511FiniteDimensionalStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase100_12b3_zero_argument_bootstrap_matches_existing_prop511():
  expected = build_phase73_8e_data()[
    "final_step"
  ]

  step = (
    build_toda_prop511_zero_argument_step()
  )

  assert (
    step.conclusion
    == expected.conclusion
  )


def test_phase100_12b3_zero_argument_bootstrap_preserves_four_branches():
  expected = build_phase73_8e_data()[
    "final_step"
  ]

  step = (
    build_toda_prop511_zero_argument_step()
  )

  assert tuple(
    premise.conclusion
    for premise in step.premises
  ) == tuple(
    premise.conclusion
    for premise in expected.premises
  )


def test_phase100_12b3_zero_argument_bootstrap_uses_corrected_lemma510_path():
  step = (
    build_toda_prop511_zero_argument_step()
  )

  stack = [
    step
  ]
  visited = set()
  rule_names = set()

  while stack:
    current = stack.pop()

    if id(
      current
    ) in visited:
      continue

    visited.add(
      id(
        current
      )
    )

    if (
      current.inference_rule
      is not None
    ):
      rule_names.add(
        current
        .inference_rule
        .name
      )

    stack.extend(
      current.premises
    )

  assert any(
    "corrected"
    in name.lower()
    for name in rule_names
  )


def test_phase100_12b3_zero_argument_bootstrap_is_fresh():
  first = (
    build_toda_prop511_zero_argument_step()
  )

  second = (
    build_toda_prop511_zero_argument_step()
  )

  assert first is not second

  assert all(
    left is not right
    for left, right in zip(
      first.premises,
      second.premises,
    )
  )


def test_phase100_12b3_production_module_has_no_test_or_probe_import():
  source = Path(
    "toda_prop511_zero_bootstrap.py"
  ).read_text(
    encoding="utf-8",
  )

  assert (
    "from test_phase"
    not in source
  )

  assert (
    "from probes."
    not in source
  )
