from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase59_pi5_3_eta3_squared import (
  build_phase59_4_data,
)
from test_phase59_pi6_4_eta4_squared import (
  build_phase59_6_data,
)
from toda_midstream_bootstrap import (
  build_phase59_prop53_step,
)
from toda_prop56_zero_bootstrap import (
  _build_higher_eta_transport,
)
from toda_rules import (
  TodaProp53FiniteDimensionalStatement,
  toda_eta_family_definition_statement,
)


def _phase59_low_dimensional_steps():
  phase59_4 = (
    build_phase59_4_data()
  )
  phase59_6 = (
    build_phase59_6_data()
  )

  return (
    phase59_4[
      "pi4_2_step"
    ],
    phase59_4[
      "final_step"
    ],
    phase59_6[
      "final_step"
    ],
  )


def test_phase160_r8_k2_production_helper_uses_generic_finite_cyclic_transport():
  (
    _,
    _,
    pi6_4_step,
  ) = (
    _phase59_low_dimensional_steps()
  )

  (
    higher_transport_step,
    higher_range_step,
  ) = _build_higher_eta_transport(
    pi6_4_step
  )

  assert (
    higher_transport_step.inference_rule
    is not None
  )

  assert (
    higher_transport_step
    .inference_rule
    .name
    == (
      "Toda 4.5 generic "
      "finite-cyclic transport"
    )
  )

  assert (
    higher_transport_step.premises[
      0
    ]
    is pi6_4_step
  )

  assert (
    higher_range_step.conclusion
    == ScalarGreaterEqualStatement(
      left=ScalarSymbol(
        name="n",
      ),
      right=5,
    )
  )


def test_phase160_r8_k2_generic_transport_keeps_suspended_source_generator():
  (
    _,
    _,
    pi6_4_step,
  ) = (
    _phase59_low_dimensional_steps()
  )

  higher_transport_step, _ = (
    _build_higher_eta_transport(
      pi6_4_step
    )
  )

  n = ScalarSymbol(
    name="n",
  )

  transported_relation = (
    higher_transport_step.conclusion
  )

  assert (
    transported_relation.lhs
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=2,
      ),
      sphere_dimension=n,
    )
  )

  assert (
    transported_relation.rhs.order
    == 2
  )

  assert (
    transported_relation.rhs.generator
    == IteratedSuspension(
      expression=(
        pi6_4_step
        .conclusion
        .rhs
        .generator
      ),
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=4,
        ),
      ),
    )
  )


def test_phase160_r8_k2_existing_bridge_normalizes_after_generic_transport():
  (
    pi4_2_step,
    pi5_3_step,
    pi6_4_step,
  ) = (
    _phase59_low_dimensional_steps()
  )

  (
    higher_transport_step,
    higher_range_step,
  ) = _build_higher_eta_transport(
    pi6_4_step
  )

  prop53_step = (
    build_phase59_prop53_step(
      pi4_2_step,
      pi5_3_step,
      pi6_4_step,
      higher_transport_step,
      higher_range_step,
    )
  )

  assert isinstance(
    prop53_step.conclusion,
    TodaProp53FiniteDimensionalStatement,
  )

  higher_relation = (
    prop53_step
    .conclusion
    .higher_eta_squared_group_relation
  )

  n = ScalarSymbol(
    name="n",
  )
  eta_n = (
    toda_eta_family_definition_statement(
      n
    ).element
  )
  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )
  eta_n_plus_one = HomotopyElement(
    name="η_(n+1)",
    dimension=n_plus_one,
    source=ScalarSum(
      left=n,
      right=2,
    ),
    target=n_plus_one,
    generator=GeneratorSymbol(
      family="η",
      index=n_plus_one,
    ),
  )

  assert (
    higher_relation.rhs.order
    == 2
  )

  assert (
    higher_relation.rhs.generator
    == Composition(
      left=eta_n,
      right=eta_n_plus_one,
    )
  )


def test_phase160_r8_k2_normalized_group_depends_on_generic_transport():
  (
    pi4_2_step,
    pi5_3_step,
    pi6_4_step,
  ) = (
    _phase59_low_dimensional_steps()
  )

  (
    higher_transport_step,
    higher_range_step,
  ) = _build_higher_eta_transport(
    pi6_4_step
  )

  prop53_step = (
    build_phase59_prop53_step(
      pi4_2_step,
      pi5_3_step,
      pi6_4_step,
      higher_transport_step,
      higher_range_step,
    )
  )

  normalized_step = next(
    premise
    for premise in prop53_step.premises
    if (
      premise.inference_rule
      is not None
      and premise.inference_rule.name
      == (
        "Toda Proposition 5.3 "
        "higher eta-squared "
        "finite-cyclic generator bridge"
      )
    )
  )

  assert (
    higher_transport_step
    in normalized_step.premises
  )
