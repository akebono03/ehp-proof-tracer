from expression import (
  GeneratorSymbol,
  HomotopyElement,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
)
from proof import (
  ProofRule,
  Relation,
)
from toda_prop56_zero_bootstrap import (
  _build_prop51_step,
)
from toda_rules import (
  TodaProp51FiniteDimensionalStatement,
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


def test_phase160_r5_prop51_uses_generic_finite_cyclic_transport():
  prop51_step = (
    _build_prop51_step()
  )

  generic_transport_steps = tuple(
    step
    for step in _walk_provenance(
      prop51_step
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
    generic_transport_steps
  ) == 1

  transported_step = (
    generic_transport_steps[
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
    == 2
  )

  assert (
    transported_step.rule
    == ProofRule.INFERENCE
  )


def test_phase160_r5_prop51_no_longer_uses_pi4_3_specific_transport():
  prop51_step = (
    _build_prop51_step()
  )

  specific_transport_steps = tuple(
    step
    for step in _walk_provenance(
      prop51_step
    )
    if (
      step.inference_rule
      is not None
      and step.inference_rule.name
      == (
        "Toda 4.5 pi_4^3 "
        "finite-cyclic transport"
      )
    )
  )

  assert (
    specific_transport_steps
    == ()
  )


def test_phase160_r5_prop51_final_higher_eta_group_is_unchanged():
  prop51_step = (
    _build_prop51_step()
  )

  assert isinstance(
    prop51_step.conclusion,
    TodaProp51FiniteDimensionalStatement,
  )

  higher_relation = (
    prop51_step
    .conclusion
    .higher_eta_group_relation
  )

  assert isinstance(
    higher_relation,
    Relation,
  )

  assert isinstance(
    higher_relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    higher_relation.rhs.order
    == 2
  )

  generator = (
    higher_relation
    .rhs
    .generator
  )

  n = ScalarSymbol(
    name="n",
  )

  assert generator == (
    HomotopyElement(
      name="η_n",
      dimension=n,
      source=(
        generator.source
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )
  )
