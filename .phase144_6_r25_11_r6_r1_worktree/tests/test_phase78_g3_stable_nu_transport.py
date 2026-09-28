from functools import lru_cache

from expression import (
  GeneratorSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  StableHomotopyGroup,
  StablePrimaryComponent,
  TodaPrimaryGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase65_nu5_order_pi8_5 import (
  build_phase65_7_data,
)
from toda_rules import (
  Toda45StableTwoPrimaryIdentificationStatement,
  TodaStableNuDefinitionStatement,
  toda_45_stable_two_primary_identification_inference_rule,
  toda_prop56_g3_two_primary_finite_cyclic_inference_rule,
  toda_prop56_stable_nu_definition_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase78_8c_data():
  phase65_7 = (
    build_phase65_7_data()
  )

  nu5_definition_step = (
    phase65_7[
      "nu5_definition_step"
    ]
  )

  pi8_5_step = (
    phase65_7[
      "pi8_5_step"
    ]
  )

  source_group = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=5,
  )

  source_group_step = ProofStep(
    conclusion=source_group,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  identification_rule = (
    toda_45_stable_two_primary_identification_inference_rule()
  )

  stable_nu_rule = (
    toda_prop56_stable_nu_definition_inference_rule()
  )

  transport_rule = (
    toda_prop56_g3_two_primary_finite_cyclic_inference_rule()
  )

  rules = (
    identification_rule,
    stable_nu_rule,
    transport_rule,
  )

  premise_steps = (
    nu5_definition_step,
    pi8_5_step,
    source_group_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  expected_identification = (
    Toda45StableTwoPrimaryIdentificationStatement(
      source_group=source_group,
      target_component=StablePrimaryComponent(
        group=StableHomotopyGroup(
          stem=3,
        ),
        prime=2,
      ),
    )
  )

  identification_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_identification
    )
  )

  stable_nu_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaStableNuDefinitionStatement,
    )
  )

  expected_final = Relation(
    lhs=StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=3,
      ),
      prime=2,
    ),
    rhs=FiniteCyclicGroup(
      order=8,
      generator=(
        stable_nu_step
        .conclusion
        .stable_element
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_final
    )
  )

  return {
    "phase65_7": phase65_7,
    "nu5_definition_step": (
      nu5_definition_step
    ),
    "pi8_5_step": pi8_5_step,
    "source_group": source_group,
    "source_group_step": (
      source_group_step
    ),
    "identification_rule": (
      identification_rule
    ),
    "stable_nu_rule": (
      stable_nu_rule
    ),
    "transport_rule": (
      transport_rule
    ),
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "identification_step": (
      identification_step
    ),
    "stable_nu_step": (
      stable_nu_step
    ),
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase78_8c_reuses_given_nu5_definition():
  data = build_phase78_8c_data()

  assert (
    data[
      "nu5_definition_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "nu5_definition_step"
    ].conclusion.index
    == 5
  )


def test_phase78_8c_nu5_has_expected_structure():
  data = build_phase78_8c_data()

  nu_5 = (
    data[
      "nu5_definition_step"
    ].conclusion
    .element
  )

  assert nu_5.name in (
    "ν₅",
    "ν_5",
  )

  assert nu_5.dimension == 5
  assert nu_5.source == 8
  assert nu_5.target == 5

  assert (
    nu_5.generator
    == GeneratorSymbol(
      family="ν",
      index=5,
    )
  )


def test_phase78_8c_reuses_derived_pi8_5_relation():
  data = build_phase78_8c_data()

  assert (
    data[
      "pi8_5_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi8_5_step"
    ].conclusion
    .lhs
    == TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    )
  )


def test_phase78_8c_pi8_5_has_order_eight():
  data = build_phase78_8c_data()

  assert (
    data[
      "pi8_5_step"
    ].conclusion
    .rhs
    .order
    == 8
  )


def test_phase78_8c_pi8_5_generator_is_nu5():
  data = build_phase78_8c_data()

  assert (
    data[
      "pi8_5_step"
    ].conclusion
    .rhs
    .generator
    == data[
      "nu5_definition_step"
    ].conclusion
    .element
  )


def test_phase78_8c_derives_stable_identification():
  data = build_phase78_8c_data()

  assert (
    data[
      "identification_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "identification_step"
    ].conclusion
    .target_component
    == StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=3,
      ),
      prime=2,
    )
  )


def test_phase78_8c_derives_stable_nu_definition():
  data = build_phase78_8c_data()

  assert (
    data[
      "stable_nu_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "stable_nu_step"
    ].conclusion,
    TodaStableNuDefinitionStatement,
  )


def test_phase78_8c_stable_nu_has_expected_structure():
  data = build_phase78_8c_data()

  stable_nu = (
    data[
      "stable_nu_step"
    ].conclusion
    .stable_element
  )

  assert stable_nu.name == "ν"
  assert stable_nu.dimension == 3
  assert stable_nu.source is None
  assert stable_nu.target is None

  assert (
    stable_nu.generator
    == GeneratorSymbol(
      family="ν",
    )
  )


def test_phase78_8c_stable_nu_preserves_nu5_definition():
  data = build_phase78_8c_data()

  assert (
    data[
      "stable_nu_step"
    ].conclusion
    .source_definition
    == data[
      "nu5_definition_step"
    ].conclusion
  )


def test_phase78_8c_stable_nu_uses_exact_dependencies():
  data = build_phase78_8c_data()

  assert (
    data[
      "stable_nu_step"
    ].premises
    == (
      data[
        "nu5_definition_step"
      ],
      data[
        "identification_step"
      ],
    )
  )


def test_phase78_8c_derives_g3_two_primary_z8_nu():
  data = build_phase78_8c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_final"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase78_8c_final_group_is_g3_two_primary():
  data = build_phase78_8c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    == StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=3,
      ),
      prime=2,
    )
  )


def test_phase78_8c_final_group_has_order_eight():
  data = build_phase78_8c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .order
    == 8
  )


def test_phase78_8c_final_generator_is_stable_nu():
  data = build_phase78_8c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == data[
      "stable_nu_step"
    ].conclusion
    .stable_element
  )


def test_phase78_8c_final_uses_exact_dependencies():
  data = build_phase78_8c_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi8_5_step"
      ],
      data[
        "identification_step"
      ],
      data[
        "stable_nu_step"
      ],
    )
  )


def test_phase78_8c_final_not_present_initially():
  data = build_phase78_8c_data()

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase78_8c_stable_nu_rejects_given_identification():
  data = build_phase78_8c_data()

  given_identification = ProofStep(
    conclusion=(
      data[
        "identification_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "stable_nu_rule"
    ],
    (
      data[
        "nu5_definition_step"
      ],
      given_identification,
    ),
  ) is None


def test_phase78_8c_transport_rejects_given_source_relation():
  data = build_phase78_8c_data()

  given_source_relation = ProofStep(
    conclusion=(
      data[
        "pi8_5_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "transport_rule"
    ],
    (
      given_source_relation,
      data[
        "identification_step"
      ],
      data[
        "stable_nu_step"
      ],
    ),
  ) is None


def test_phase78_8c_transport_rejects_given_stable_nu():
  data = build_phase78_8c_data()

  given_stable_nu = ProofStep(
    conclusion=(
      data[
        "stable_nu_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "transport_rule"
    ],
    (
      data[
        "pi8_5_step"
      ],
      data[
        "identification_step"
      ],
      given_stable_nu,
    ),
  ) is None


def test_phase78_8c_reaches_fixed_point():
  data = build_phase78_8c_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


