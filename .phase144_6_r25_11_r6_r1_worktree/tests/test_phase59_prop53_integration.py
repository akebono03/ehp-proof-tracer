from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
)
from homotopy_groups import (
  FiniteCyclicGroup,
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
from test_phase59_eta4_squared_stable_transport import (
  build_phase59_7_data,
)
from test_phase59_pi5_3_eta3_squared import (
  build_phase59_4_data,
)
from test_phase59_pi6_4_eta4_squared import (
  build_phase59_6_data,
)
from toda_rules import (
  TodaProp53FiniteDimensionalStatement,
  toda_eta_family_definition_statement,
  toda_prop53_finite_dimensional_integration_inference_rule,
  toda_prop53_higher_eta_squared_bridge_inference_rule,
  toda_prop53_higher_eta_squared_finite_cyclic_generator_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase59_8_data():
  phase59_4 = (
    build_phase59_4_data()
  )

  phase59_6 = (
    build_phase59_6_data()
  )

  phase59_7 = (
    build_phase59_7_data()
  )

  pi4_2_step = (
    phase59_4[
      "pi4_2_step"
    ]
  )

  pi5_3_step = (
    phase59_4[
      "final_step"
    ]
  )

  pi6_4_step = (
    phase59_6[
      "final_step"
    ]
  )

  higher_transport_step = (
    phase59_7[
      "final_step"
    ]
  )

  n = phase59_7[
    "n"
  ]

  higher_range_step = (
    phase59_7[
      "higher_range_step"
    ]
  )

  eta_n_definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  eta_n_definition_step = ProofStep(
    conclusion=eta_n_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta_4 = HomotopyElement(
    name="η₄",
    dimension=4,
    source=5,
    target=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
  )

  eta_5 = HomotopyElement(
    name="η₅",
    dimension=5,
    source=6,
    target=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )

  eta_4_squared = Composition(
    left=eta_4,
    right=eta_5,
  )

  eta_n = eta_n_definition.element

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

  eta_n_squared = Composition(
    left=eta_n,
    right=eta_n_plus_one,
  )

  transported_generator = (
    IteratedSuspension(
      expression=eta_4_squared,
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=4,
        ),
      ),
    )
  )

  expected_bridge = Relation(
    lhs=transported_generator,
    rhs=eta_n_squared,
    relation_type=RelationType.EQUALITY,
  )

  expected_higher_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=2,
      ),
      sphere_dimension=n,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_n_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  expected_statement = (
    TodaProp53FiniteDimensionalStatement(
      pi4_2_group_relation=(
        pi4_2_step.conclusion
      ),
      pi5_3_group_relation=(
        pi5_3_step.conclusion
      ),
      pi6_4_group_relation=(
        pi6_4_step.conclusion
      ),
      higher_eta_squared_group_relation=(
        expected_higher_relation
      ),
      higher_range=(
        higher_range_step.conclusion
      ),
    )
  )

  bridge_rule = (
    toda_prop53_higher_eta_squared_bridge_inference_rule()
  )

  generator_rule = (
    toda_prop53_higher_eta_squared_finite_cyclic_generator_inference_rule()
  )

  integration_rule = (
    toda_prop53_finite_dimensional_integration_inference_rule()
  )

  rules = (
    bridge_rule,
    generator_rule,
    integration_rule,
  )

  premise_steps = (
    pi4_2_step,
    pi5_3_step,
    pi6_4_step,
    higher_transport_step,
    higher_range_step,
    eta_n_definition_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  bridge_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_bridge
    )
  )

  higher_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_higher_relation
    )
  )

  integration_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase59_4": phase59_4,
    "phase59_6": phase59_6,
    "phase59_7": phase59_7,
    "n": n,
    "pi4_2_step": pi4_2_step,
    "pi5_3_step": pi5_3_step,
    "pi6_4_step": pi6_4_step,
    "higher_transport_step": (
      higher_transport_step
    ),
    "higher_range_step": (
      higher_range_step
    ),
    "eta_n_definition": (
      eta_n_definition
    ),
    "eta_n_definition_step": (
      eta_n_definition_step
    ),
    "eta_n": eta_n,
    "eta_n_plus_one": (
      eta_n_plus_one
    ),
    "eta_n_squared": (
      eta_n_squared
    ),
    "transported_generator": (
      transported_generator
    ),
    "expected_bridge": (
      expected_bridge
    ),
    "expected_higher_relation": (
      expected_higher_relation
    ),
    "expected_statement": (
      expected_statement
    ),
    "bridge_rule": bridge_rule,
    "generator_rule": generator_rule,
    "integration_rule": (
      integration_rule
    ),
    "premise_steps": premise_steps,
    "result": result,
    "bridge_step": bridge_step,
    "higher_step": higher_step,
    "integration_step": (
      integration_step
    ),
  }


def test_phase59_8_reuses_three_low_dimensional_results():
  data = build_phase59_8_data()

  assert (
    data[
      "pi4_2_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi5_3_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi6_4_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase59_8_reuses_phase59_7_transport():
  data = build_phase59_8_data()

  assert (
    data[
      "higher_transport_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase59_8_eta_n_squared_is_composition():
  data = build_phase59_8_data()

  assert (
    data[
      "eta_n_squared"
    ]
    == Composition(
      left=data[
        "eta_n"
      ],
      right=data[
        "eta_n_plus_one"
      ],
    )
  )


def test_phase59_8_bridge_rule_matches_definition_and_range():
  data = build_phase59_8_data()

  assert find_inference_match(
    data[
      "bridge_rule"
    ],
    (
      data[
        "eta_n_definition_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is not None


def test_phase59_8_derives_e_n_minus_4_eta4_squared_equals_eta_n_squared():
  data = build_phase59_8_data()

  assert (
    data[
      "bridge_step"
    ].conclusion
    == data[
      "expected_bridge"
    ]
  )

  assert (
    data[
      "bridge_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase59_8_bridge_preserves_definition_and_scope_provenance():
  data = build_phase59_8_data()

  assert (
    data[
      "bridge_step"
    ].premises
    == (
      data[
        "eta_n_definition_step"
      ],
      data[
        "higher_range_step"
      ],
    )
  )


def test_phase59_8_generator_rule_matches_two_derived_results():
  data = build_phase59_8_data()

  assert find_inference_match(
    data[
      "generator_rule"
    ],
    (
      data[
        "higher_transport_step"
      ],
      data[
        "bridge_step"
      ],
    ),
  ) is not None


def test_phase59_8_derives_higher_eta_squared_group():
  data = build_phase59_8_data()

  assert (
    data[
      "higher_step"
    ].conclusion
    == data[
      "expected_higher_relation"
    ]
  )

  assert (
    data[
      "higher_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase59_8_higher_group_uses_eta_n_squared_not_transport():
  data = build_phase59_8_data()

  generator = (
    data[
      "higher_step"
    ].conclusion.rhs.generator
  )

  assert (
    generator
    == data[
      "eta_n_squared"
    ]
  )

  assert not isinstance(
    generator,
    IteratedSuspension,
  )


def test_phase59_8_higher_group_has_two_derived_premises():
  data = build_phase59_8_data()

  assert (
    data[
      "higher_step"
    ].premises
    == (
      data[
        "higher_transport_step"
      ],
      data[
        "bridge_step"
      ],
    )
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in data[
      "higher_step"
    ].premises
  )


def test_phase59_8_integration_rule_matches_all_cases():
  data = build_phase59_8_data()

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      data[
        "pi4_2_step"
      ],
      data[
        "pi5_3_step"
      ],
      data[
        "pi6_4_step"
      ],
      data[
        "higher_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is not None


def test_phase59_8_derives_prop53_finite_dimensional_statement():
  data = build_phase59_8_data()

  step = data[
    "integration_step"
  ]

  assert isinstance(
    step.conclusion,
    TodaProp53FiniteDimensionalStatement,
  )

  assert (
    step.conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase59_8_statement_preserves_all_branches():
  data = build_phase59_8_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    statement.pi4_2_group_relation
    == data[
      "pi4_2_step"
    ].conclusion
  )

  assert (
    statement.pi5_3_group_relation
    == data[
      "pi5_3_step"
    ].conclusion
  )

  assert (
    statement.pi6_4_group_relation
    == data[
      "pi6_4_step"
    ].conclusion
  )

  assert (
    statement.higher_eta_squared_group_relation
    == data[
      "higher_step"
    ].conclusion
  )

  assert (
    statement.higher_range
    == data[
      "higher_range_step"
    ].conclusion
  )


def test_phase59_8_integration_preserves_derived_branch_provenance():
  data = build_phase59_8_data()

  step = data[
    "integration_step"
  ]

  assert (
    step.premises
    == (
      data[
        "pi4_2_step"
      ],
      data[
        "pi5_3_step"
      ],
      data[
        "pi6_4_step"
      ],
      data[
        "higher_step"
      ],
      data[
        "higher_range_step"
      ],
    )
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in step.premises[
      :4
    ]
  )


def test_phase59_8_rejects_given_higher_relation():
  data = build_phase59_8_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "higher_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      data[
        "pi4_2_step"
      ],
      data[
        "pi5_3_step"
      ],
      data[
        "pi6_4_step"
      ],
      given_step,
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase59_8_rejects_n4_higher_scope():
  data = build_phase59_8_data()

  wrong_range = ProofStep(
    conclusion=type(
      data[
        "higher_range_step"
      ].conclusion
    )(
      left=data[
        "n"
      ],
      right=4,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      data[
        "pi4_2_step"
      ],
      data[
        "pi5_3_step"
      ],
      data[
        "pi6_4_step"
      ],
      data[
        "higher_step"
      ],
      wrong_range,
    ),
  ) is None


def test_phase59_8_final_statement_is_not_given():
  data = build_phase59_8_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_statement"
    ]
    not in initial_conclusions
  )


def test_phase59_8_reaches_fixed_point_in_three_rounds():
  data = build_phase59_8_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    result.round_count
    == 3
  )

  assert (
    data[
      "bridge_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "higher_step"
    ]
    in result.round_results[
      1
    ].new_steps
  )

  assert (
    data[
      "integration_step"
    ]
    in result.round_results[
      2
    ].new_steps
  )




