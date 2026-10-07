from expression import (
  IteratedSuspension,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
)
from proof import (
  ProofRule,
  Relation,
)
from toda_prop515_upper_bootstrap import (
  build_toda_prop515_upper_bootstrap,
)


def _walk_provenance(
  root,
):
  visited = set()
  stack = [
    root,
  ]

  while stack:
    step = stack.pop()

    if id(step) in visited:
      continue

    visited.add(
      id(step)
    )

    yield step

    stack.extend(
      step.premises
    )


def test_phase160_r6_sigma_production_uses_generic_finite_cyclic_transport():
  result = (
    build_toda_prop515_upper_bootstrap()
  )

  generic_steps = tuple(
    step
    for step in _walk_provenance(
      result.higher_step
    )
    if (
      step.inference_rule
      is not None
      and step.inference_rule.name
      == (
        "Toda 4.5 generic "
        "finite-cyclic transport"
      )
    )
  )

  assert len(
    generic_steps
  ) == 1

  transported_step = (
    generic_steps[
      0
    ]
  )

  assert isinstance(
    transported_step.conclusion,
    Relation,
  )

  assert isinstance(
    transported_step.conclusion.rhs,
    FiniteCyclicGroup,
  )

  assert (
    transported_step
    .conclusion
    .rhs
    .order
    == 16
  )

  assert isinstance(
    transported_step
    .conclusion
    .rhs
    .generator,
    IteratedSuspension,
  )


def test_phase160_r6_sigma_production_uses_separate_generator_normalization():
  result = (
    build_toda_prop515_upper_bootstrap()
  )

  higher_step = (
    result.higher_step
  )

  assert (
    higher_step.inference_rule
    is not None
  )

  assert (
    higher_step
    .inference_rule
    .name
    == (
      "Toda sigma-family "
      "transported-generator normalization"
    )
  )

  assert (
    higher_step.rule
    == ProofRule.INFERENCE
  )


def test_phase160_r6_sigma_production_no_longer_uses_combined_sigma9_transport():
  result = (
    build_toda_prop515_upper_bootstrap()
  )

  old_steps = tuple(
    step
    for step in _walk_provenance(
      result.higher_step
    )
    if (
      step.inference_rule
      is not None
      and step.inference_rule.name
      == (
        "Toda (4.5) sigma_9 "
        "finite cyclic transport"
      )
    )
  )

  assert old_steps == ()


def test_phase160_r6_sigma_final_higher_group_remains_named_sigma_n():
  result = (
    build_toda_prop515_upper_bootstrap()
  )

  relation = (
    result.higher_step.conclusion
  )

  assert isinstance(
    relation,
    Relation,
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 16
  )

  generator = (
    relation.rhs.generator
  )

  n = ScalarSymbol(
    name="n",
  )

  assert (
    generator.generator.family
    == "σ"
  )

  assert (
    generator.generator.index
    == n
  )


def test_phase160_r6_sigma_normalization_depends_on_generic_transport_and_definitions():
  result = (
    build_toda_prop515_upper_bootstrap()
  )

  higher_step = (
    result.higher_step
  )

  assert len(
    higher_step.premises
  ) == 3

  generic_premises = tuple(
    premise
    for premise in higher_step.premises
    if (
      premise.inference_rule
      is not None
      and premise.inference_rule.name
      == (
        "Toda 4.5 generic "
        "finite-cyclic transport"
      )
    )
  )

  assert len(
    generic_premises
  ) == 1

  assert (
    result.sigma_family_step
    in higher_step.premises
  )

  assert (
    result.sigma9_definition_step
    in higher_step.premises
  )
