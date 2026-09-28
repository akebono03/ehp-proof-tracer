from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaIteratedSuspensionMap,
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
from test_phase62_toda55_integration import (
  build_phase62_6_data,
)
from test_phase65_n5_quotient_e2_injectivity import (
  build_phase65_6_data,
)
from test_phase65_nu_prime_order_pi6_3 import (
  build_phase65_4_data,
)
from toda_rules import (
  Toda55NuFamilyFiniteDimensionalStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaNuFamilyDefinitionStatement,
  TodaProp56Pi8_5QuotientStatement,
  toda_nu_family_definition_statement,
  toda_prop56_e2_nu_prime_order_four_inference_rule,
  toda_prop56_nu5_double_relation_inference_rule,
  toda_prop56_nu5_order_eight_inference_rule,
  toda_prop56_pi8_5_finite_cyclic_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase65_7_data():
  phase62 = (
    build_phase62_6_data()
  )

  phase65_4 = (
    build_phase65_4_data()
  )

  phase65_6 = (
    build_phase65_6_data()
  )

  toda55_step = (
    phase62[
      "integration_step"
    ]
  )

  pi6_3_step = (
    phase65_4[
      "pi6_3_step"
    ]
  )

  e2_injective_step = (
    phase65_6[
      "injective_step"
    ]
  )

  quotient_step = (
    phase65_6[
      "quotient_step"
    ]
  )

  nu5_definition = (
    toda_nu_family_definition_statement(
      5
    )
  )

  nu5_definition_step = ProofStep(
    conclusion=nu5_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nu_5 = (
    nu5_definition.element
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  e2_nu_prime = IteratedSuspension(
    expression=nu_prime,
    exponent=2,
  )

  expected_double_relation = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=nu_5,
    ),
    rhs=e2_nu_prime,
    relation_type=RelationType.EQUALITY,
  )

  expected_e2_order = Relation(
    lhs=e2_nu_prime,
    rhs=4,
    relation_type=RelationType.ORDER,
  )

  expected_nu5_order = Relation(
    lhs=nu_5,
    rhs=8,
    relation_type=RelationType.ORDER,
  )

  expected_pi8_5 = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    ),
    rhs=FiniteCyclicGroup(
      order=8,
      generator=nu_5,
    ),
    relation_type=RelationType.EQUALITY,
  )

  double_rule = (
    toda_prop56_nu5_double_relation_inference_rule()
  )

  e2_order_rule = (
    toda_prop56_e2_nu_prime_order_four_inference_rule()
  )

  nu5_order_rule = (
    toda_prop56_nu5_order_eight_inference_rule()
  )

  pi8_5_rule = (
    toda_prop56_pi8_5_finite_cyclic_inference_rule()
  )

  rules = (
    double_rule,
    e2_order_rule,
    nu5_order_rule,
    pi8_5_rule,
  )

  premise_steps = (
    toda55_step,
    nu5_definition_step,
    pi6_3_step,
    e2_injective_step,
    quotient_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  double_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_double_relation
    )
  )

  e2_order_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_e2_order
    )
  )

  nu5_order_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_nu5_order
    )
  )

  pi8_5_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_pi8_5
    )
  )

  return {
    "phase62": phase62,
    "phase65_4": phase65_4,
    "phase65_6": phase65_6,
    "toda55_step": toda55_step,
    "pi6_3_step": pi6_3_step,
    "e2_injective_step": (
      e2_injective_step
    ),
    "quotient_step": quotient_step,
    "nu5_definition": (
      nu5_definition
    ),
    "nu5_definition_step": (
      nu5_definition_step
    ),
    "nu_5": nu_5,
    "nu_prime": nu_prime,
    "e2_nu_prime": e2_nu_prime,
    "expected_double_relation": (
      expected_double_relation
    ),
    "expected_e2_order": (
      expected_e2_order
    ),
    "expected_nu5_order": (
      expected_nu5_order
    ),
    "expected_pi8_5": (
      expected_pi8_5
    ),
    "double_rule": double_rule,
    "e2_order_rule": e2_order_rule,
    "nu5_order_rule": nu5_order_rule,
    "pi8_5_rule": pi8_5_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "double_step": double_step,
    "e2_order_step": e2_order_step,
    "nu5_order_step": nu5_order_step,
    "pi8_5_step": pi8_5_step,
  }


def test_phase65_7_reuses_derived_toda55():
  data = build_phase65_7_data()

  assert isinstance(
    data[
      "toda55_step"
    ].conclusion,
    Toda55NuFamilyFiniteDimensionalStatement,
  )

  assert (
    data[
      "toda55_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_7_nu5_definition_is_given():
  data = build_phase65_7_data()

  assert isinstance(
    data[
      "nu5_definition"
    ],
    TodaNuFamilyDefinitionStatement,
  )

  assert (
    data[
      "nu5_definition_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "nu5_definition"
    ].index
    == 5
  )


def test_phase65_7_nu5_has_expected_typing():
  data = build_phase65_7_data()

  assert (
    data[
      "nu_5"
    ].dimension
    == 5
  )

  assert (
    data[
      "nu_5"
    ].source
    == 8
  )

  assert (
    data[
      "nu_5"
    ].target
    == 5
  )


def test_phase65_7_double_rule_matches():
  data = build_phase65_7_data()

  assert find_inference_match(
    data[
      "double_rule"
    ],
    (
      data[
        "toda55_step"
      ],
      data[
        "nu5_definition_step"
      ],
    ),
  ) is not None


def test_phase65_7_derives_two_nu5_equals_e2_nu_prime():
  data = build_phase65_7_data()

  assert (
    data[
      "double_step"
    ].conclusion
    == data[
      "expected_double_relation"
    ]
  )

  assert (
    data[
      "double_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_7_reuses_phase65_4_pi6_3():
  data = build_phase65_7_data()

  assert (
    data[
      "pi6_3_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi6_3_step"
    ].conclusion.rhs.order
    == 4
  )


def test_phase65_7_reuses_phase65_6_e2_injectivity():
  data = build_phase65_7_data()

  assert isinstance(
    data[
      "e2_injective_step"
    ].conclusion,
    TodaIteratedSuspensionInjectiveStatement,
  )

  assert (
    data[
      "e2_injective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_7_e2_order_rule_matches():
  data = build_phase65_7_data()

  assert find_inference_match(
    data[
      "e2_order_rule"
    ],
    (
      data[
        "pi6_3_step"
      ],
      data[
        "e2_injective_step"
      ],
    ),
  ) is not None


def test_phase65_7_derives_e2_nu_prime_order_four():
  data = build_phase65_7_data()

  assert (
    data[
      "e2_order_step"
    ].conclusion
    == data[
      "expected_e2_order"
    ]
  )

  assert (
    data[
      "e2_order_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_7_nu5_order_rule_matches():
  data = build_phase65_7_data()

  assert find_inference_match(
    data[
      "nu5_order_rule"
    ],
    (
      data[
        "double_step"
      ],
      data[
        "e2_order_step"
      ],
      data[
        "nu5_definition_step"
      ],
    ),
  ) is not None


def test_phase65_7_derives_nu5_order_eight():
  data = build_phase65_7_data()

  assert (
    data[
      "nu5_order_step"
    ].conclusion
    == data[
      "expected_nu5_order"
    ]
  )

  assert (
    data[
      "nu5_order_step"
    ].conclusion.rhs
    == 8
  )

  assert (
    data[
      "nu5_order_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_7_reuses_quotient_order_two():
  data = build_phase65_7_data()

  statement = (
    data[
      "quotient_step"
    ].conclusion
  )

  assert isinstance(
    statement,
    TodaProp56Pi8_5QuotientStatement,
  )

  assert (
    statement.quotient_order
    == 2
  )

  assert (
    data[
      "quotient_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_7_pi8_5_rule_matches():
  data = build_phase65_7_data()

  assert find_inference_match(
    data[
      "pi8_5_rule"
    ],
    (
      data[
        "nu5_order_step"
      ],
      data[
        "nu5_definition_step"
      ],
      data[
        "pi6_3_step"
      ],
      data[
        "e2_injective_step"
      ],
      data[
        "quotient_step"
      ],
    ),
  ) is not None


def test_phase65_7_derives_pi8_5_z8_nu5():
  data = build_phase65_7_data()

  assert (
    data[
      "pi8_5_step"
    ].conclusion
    == data[
      "expected_pi8_5"
    ]
  )

  assert (
    data[
      "pi8_5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_7_final_group_is_cyclic_order_eight():
  data = build_phase65_7_data()

  group = (
    data[
      "pi8_5_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert group.order == 8

  assert (
    group.generator
    == data[
      "nu_5"
    ]
  )


def test_phase65_7_order_provenance():
  data = build_phase65_7_data()

  assert (
    data[
      "double_step"
    ].premises
    == (
      data[
        "toda55_step"
      ],
      data[
        "nu5_definition_step"
      ],
    )
  )

  assert (
    data[
      "e2_order_step"
    ].premises
    == (
      data[
        "pi6_3_step"
      ],
      data[
        "e2_injective_step"
      ],
    )
  )

  assert (
    data[
      "nu5_order_step"
    ].premises
    == (
      data[
        "double_step"
      ],
      data[
        "e2_order_step"
      ],
      data[
        "nu5_definition_step"
      ],
    )
  )


def test_phase65_7_final_provenance():
  data = build_phase65_7_data()

  assert (
    data[
      "pi8_5_step"
    ].premises
    == (
      data[
        "nu5_order_step"
      ],
      data[
        "nu5_definition_step"
      ],
      data[
        "pi6_3_step"
      ],
      data[
        "e2_injective_step"
      ],
      data[
        "quotient_step"
      ],
    )
  )


def test_phase65_7_rejects_given_toda55():
  data = build_phase65_7_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "toda55_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "double_rule"
    ],
    (
      given_step,
      data[
        "nu5_definition_step"
      ],
    ),
  ) is None


def test_phase65_7_rejects_given_e2_injectivity():
  data = build_phase65_7_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "e2_injective_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "e2_order_rule"
    ],
    (
      data[
        "pi6_3_step"
      ],
      given_step,
    ),
  ) is None


def test_phase65_7_final_result_is_not_given():
  data = build_phase65_7_data()

  assert (
    data[
      "pi8_5_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "expected_pi8_5"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase65_7_reaches_fixed_point_in_three_rounds():
  data = build_phase65_7_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3

  assert (
    data[
      "double_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "e2_order_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "nu5_order_step"
    ]
    in result.round_results[
      1
    ].new_steps
  )

  assert (
    data[
      "pi8_5_step"
    ]
    in result.round_results[
      2
    ].new_steps
  )


