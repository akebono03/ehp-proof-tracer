from expression import (
  Multiple,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_prop56_zero_bootstrap import (
  _build_prop51_step,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaProp51FiniteDimensionalStatement,
)


def test_phase159_repair1c_prop51_builder_uses_direct_phase50_delta():
  prop51_step = _build_prop51_step()

  assert isinstance(
    prop51_step.conclusion,
    TodaProp51FiniteDimensionalStatement,
  )

  delta_relation = (
    prop51_step
    .conclusion
    .delta_iota5_relation
  )

  assert isinstance(
    delta_relation,
    TodaDeltaImageUpToSignStatement,
  )
  assert isinstance(
    delta_relation.positive_value,
    Multiple,
  )
  assert (
    delta_relation
    .positive_value
    .coefficient
    == 2
  )

  delta_premises = tuple(
    premise
    for premise in prop51_step.premises
    if isinstance(
      premise.conclusion,
      TodaDeltaImageUpToSignStatement,
    )
  )

  assert len(
    delta_premises
  ) == 1

  delta_step = (
    delta_premises[0]
  )

  assert (
    delta_step.inference_rule
    is not None
  )
  assert (
    delta_step
    .inference_rule
    .literature_reference
    is not None
  )
  assert (
    delta_step
    .inference_rule
    .literature_reference
    .locator
    == "Proposition 5.1"
  )


def test_phase159_repair1c_standard_production_repository_builds():
  repository = (
    build_standard_production_proof_repository()
  )

  assert repository is not None
