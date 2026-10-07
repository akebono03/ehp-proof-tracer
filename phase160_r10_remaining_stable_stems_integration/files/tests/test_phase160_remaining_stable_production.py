from functools import lru_cache

from expression import (
  Composition,
  IteratedSuspension,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  Relation,
)
from toda_phase65_bootstrap import (
  build_toda_prop56_bootstrap_step,
)
from toda_prop56_zero_bootstrap import (
  build_toda_prop56_zero_argument_step,
)
from toda_prop58_zero_bootstrap import (
  build_toda_prop58_zero_argument_step,
)
from toda_prop511_zero_bootstrap import (
  build_toda_prop511_zero_argument_step,
)


def _ancestry(
  root,
):
  result = []
  seen = set()
  stack = [
    root
  ]

  while stack:
    step = stack.pop()

    if id(
      step
    ) in seen:
      continue

    seen.add(
      id(
        step
      )
    )
    result.append(
      step
    )
    stack.extend(
      step.premises
    )

  return tuple(
    result
  )


def _rule_names(
  root,
) -> tuple[
  str,
  ...,
]:
  return tuple(
    step.inference_rule.name
    for step in _ancestry(
      root
    )
    if step.inference_rule
    is not None
  )


@lru_cache(maxsize=1)
def _prop56_root():
  return (
    build_toda_prop56_zero_argument_step()
  )


@lru_cache(maxsize=1)
def _prop58_root():
  return (
    build_toda_prop58_zero_argument_step()
  )


@lru_cache(maxsize=1)
def _prop511_root():
  return (
    build_toda_prop511_zero_argument_step()
  )


def test_phase160_r10_three_stem_production_uses_generic_transport():
  names = _rule_names(
    _prop56_root()
  )

  assert (
    "Toda 4.5 generic "
    "finite-cyclic transport"
    in names
  )
  assert (
    "Toda Proposition 5.6 "
    "nu_5 stable transport"
    not in names
  )


def test_phase160_r10_four_stem_production_uses_generic_zero_transport():
  root = _prop58_root()
  names = _rule_names(
    root
  )

  assert (
    "Toda 4.5 generic "
    "zero-group transport"
    in names
  )

  n = ScalarSymbol(
    name="n",
  )

  assert any(
    isinstance(
      step.conclusion,
      TodaPrimaryGroupZeroStatement,
    )
    and step.conclusion.group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=4,
      ),
      sphere_dimension=n,
    )
    for step in _ancestry(
      root
    )
  )


def test_phase160_r10_five_stem_production_uses_same_generic_zero_transport():
  root = _prop511_root()
  names = _rule_names(
    root
  )

  assert (
    names.count(
      "Toda 4.5 generic "
      "zero-group transport"
    )
    >= 2
  )

  n = ScalarSymbol(
    name="n",
  )

  assert any(
    isinstance(
      step.conclusion,
      TodaPrimaryGroupZeroStatement,
    )
    and step.conclusion.group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=5,
      ),
      sphere_dimension=n,
    )
    for step in _ancestry(
      root
    )
  )


def test_phase160_r10_six_stem_separates_transport_and_normalization():
  root = _prop511_root()
  names = _rule_names(
    root
  )

  assert (
    "Toda 4.5 generic "
    "finite-cyclic transport"
    in names
  )
  assert (
    "Toda nu-squared "
    "transported-generator normalization"
    in names
  )

  n = ScalarSymbol(
    name="n",
  )

  normalized = tuple(
    step
    for step in _ancestry(
      root
    )
    if (
      step.inference_rule
      is not None
      and step.inference_rule.name
      == (
        "Toda nu-squared "
        "transported-generator normalization"
      )
    )
  )

  assert len(
    normalized
  ) == 1

  step = normalized[
    0
  ]

  assert isinstance(
    step.conclusion,
    Relation,
  )
  assert isinstance(
    step.conclusion.rhs,
    FiniteCyclicGroup,
  )
  assert (
    step.conclusion.rhs.order
    == 2
  )
  assert isinstance(
    step.conclusion.rhs.generator,
    Composition,
  )
  assert any(
    premise.inference_rule
    is not None
    and premise.inference_rule.name
    == (
      "Toda 4.5 generic "
      "finite-cyclic transport"
    )
    and isinstance(
      premise.conclusion.rhs.generator,
      IteratedSuspension,
    )
    for premise in step.premises
  )
