from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
  TodaSuspensionIsomorphismStatement,
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
from test_phase59_n4_suspension_isomorphism import (
  build_phase59_5_data,
)
from test_phase59_pi5_3_eta3_squared import (
  build_phase59_4_data,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
  toda_eta_family_definition_statement,
  toda_prop53_n4_eta_square_suspension_bridge_inference_rule,
  toda_prop53_n4_pi6_4_finite_cyclic_transport_inference_rule,
)


def build_phase59_6_data():
  phase59_4 = (
    build_phase59_4_data()
  )

  phase59_5 = (
    build_phase59_5_data()
  )

  pi5_3_step = (
    phase59_4[
      "final_step"
    ]
  )

  suspension_isomorphism_step = (
    phase59_5[
      "isomorphism_step"
    ]
  )

  eta4_definition = (
    toda_eta_family_definition_statement(
      4
    )
  )

  eta5_definition = (
    toda_eta_family_definition_statement(
      5
    )
  )

  eta4_definition_step = ProofStep(
    conclusion=eta4_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta5_definition_step = ProofStep(
    conclusion=eta5_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
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

  eta_3_squared = Composition(
    left=eta_3,
    right=eta_4,
  )

  eta_4_squared = Composition(
    left=eta_4,
    right=eta_5,
  )

  expected_eta_square_relation = Relation(
    lhs=Suspension(
      expression=eta_3_squared,
    ),
    rhs=eta_4_squared,
    relation_type=RelationType.EQUALITY,
  )

  expected_pi6_4_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=4,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_4_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  bridge_rule = (
    toda_prop53_n4_eta_square_suspension_bridge_inference_rule()
  )

  transport_rule = (
    toda_prop53_n4_pi6_4_finite_cyclic_transport_inference_rule()
  )

  rules = (
    bridge_rule,
    transport_rule,
  )

  premise_steps = (
    pi5_3_step,
    suspension_isomorphism_step,
    eta4_definition_step,
    eta5_definition_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  eta_square_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_eta_square_relation
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_pi6_4_relation
    )
  )

  return {
    "phase59_4": phase59_4,
    "phase59_5": phase59_5,
    "pi5_3_step": pi5_3_step,
    "suspension_isomorphism_step": (
      suspension_isomorphism_step
    ),
    "eta4_definition": (
      eta4_definition
    ),
    "eta5_definition": (
      eta5_definition
    ),
    "eta4_definition_step": (
      eta4_definition_step
    ),
    "eta5_definition_step": (
      eta5_definition_step
    ),
    "eta_3": eta_3,
    "eta_4": eta_4,
    "eta_5": eta_5,
    "eta_3_squared": (
      eta_3_squared
    ),
    "eta_4_squared": (
      eta_4_squared
    ),
    "expected_eta_square_relation": (
      expected_eta_square_relation
    ),
    "expected_pi6_4_relation": (
      expected_pi6_4_relation
    ),
    "bridge_rule": bridge_rule,
    "transport_rule": (
      transport_rule
    ),
    "premise_steps": premise_steps,
    "result": result,
    "eta_square_step": (
      eta_square_step
    ),
    "final_step": final_step,
  }


def test_phase59_6_reuses_phase59_4_pi5_3_relation():
  data = build_phase59_6_data()

  step = data[
    "pi5_3_step"
  ]

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert (
    step.conclusion
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=5,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=data[
          "eta_3_squared"
        ],
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase59_6_reuses_phase59_5_suspension_isomorphism():
  data = build_phase59_6_data()

  step = data[
    "suspension_isomorphism_step"
  ]

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    step.conclusion,
    TodaSuspensionIsomorphismStatement,
  )


def test_phase59_6_eta4_definition_is_existing_definition():
  data = build_phase59_6_data()

  definition = data[
    "eta4_definition"
  ]

  assert isinstance(
    definition,
    TodaEtaFamilyDefinitionStatement,
  )

  assert definition.index == 4

  assert (
    definition.element.generator
    == data[
      "eta_4"
    ].generator
  )


def test_phase59_6_eta5_definition_is_existing_definition():
  data = build_phase59_6_data()

  definition = data[
    "eta5_definition"
  ]

  assert isinstance(
    definition,
    TodaEtaFamilyDefinitionStatement,
  )

  assert definition.index == 5

  assert (
    definition.element.generator
    == data[
      "eta_5"
    ].generator
  )


def test_phase59_6_eta3_squared_uses_composition():
  data = build_phase59_6_data()

  assert (
    data[
      "eta_3_squared"
    ]
    == Composition(
      left=data[
        "eta_3"
      ],
      right=data[
        "eta_4"
      ],
    )
  )


def test_phase59_6_eta4_squared_uses_composition():
  data = build_phase59_6_data()

  assert (
    data[
      "eta_4_squared"
    ]
    == Composition(
      left=data[
        "eta_4"
      ],
      right=data[
        "eta_5"
      ],
    )
  )


def test_phase59_6_bridge_rule_matches_eta_definitions():
  data = build_phase59_6_data()

  assert find_inference_match(
    data[
      "bridge_rule"
    ],
    (
      data[
        "eta4_definition_step"
      ],
      data[
        "eta5_definition_step"
      ],
    ),
  ) is not None


def test_phase59_6_derives_e_eta3_squared_equals_eta4_squared():
  data = build_phase59_6_data()

  step = data[
    "eta_square_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_eta_square_relation"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase59_6_eta_square_bridge_preserves_definition_provenance():
  data = build_phase59_6_data()

  assert (
    data[
      "eta_square_step"
    ].premises
    == (
      data[
        "eta4_definition_step"
      ],
      data[
        "eta5_definition_step"
      ],
    )
  )


def test_phase59_6_transport_rule_matches_derived_dependencies():
  data = build_phase59_6_data()

  assert find_inference_match(
    data[
      "transport_rule"
    ],
    (
      data[
        "pi5_3_step"
      ],
      data[
        "suspension_isomorphism_step"
      ],
      data[
        "eta_square_step"
      ],
    ),
  ) is not None


def test_phase59_6_derives_pi6_4_order_two_eta4_squared():
  data = build_phase59_6_data()

  step = data[
    "final_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_pi6_4_relation"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase59_6_final_generator_is_eta4_squared():
  data = build_phase59_6_data()

  group = (
    data[
      "final_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert group.order == 2

  assert (
    group.generator
    == data[
      "eta_4_squared"
    ]
  )


def test_phase59_6_final_provenance_uses_three_derived_dependencies():
  data = build_phase59_6_data()

  final_step = data[
    "final_step"
  ]

  assert (
    final_step.premises
    == (
      data[
        "pi5_3_step"
      ],
      data[
        "suspension_isomorphism_step"
      ],
      data[
        "eta_square_step"
      ],
    )
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in final_step.premises
  )


def test_phase59_6_rejects_given_pi5_3_relation():
  data = build_phase59_6_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "pi5_3_step"
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
      given_step,
      data[
        "suspension_isomorphism_step"
      ],
      data[
        "eta_square_step"
      ],
    ),
  ) is None


def test_phase59_6_rejects_given_suspension_isomorphism():
  data = build_phase59_6_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "suspension_isomorphism_step"
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
        "pi5_3_step"
      ],
      given_step,
      data[
        "eta_square_step"
      ],
    ),
  ) is None


def test_phase59_6_rejects_given_eta_square_bridge():
  data = build_phase59_6_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "eta_square_step"
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
        "pi5_3_step"
      ],
      data[
        "suspension_isomorphism_step"
      ],
      given_step,
    ),
  ) is None


def test_phase59_6_bridge_rejects_wrong_eta5_index():
  data = build_phase59_6_data()

  wrong_definition = (
    toda_eta_family_definition_statement(
      6
    )
  )

  wrong_step = ProofStep(
    conclusion=wrong_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "bridge_rule"
    ],
    (
      data[
        "eta4_definition_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase59_6_final_result_is_not_given():
  data = build_phase59_6_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_pi6_4_relation"
    ]
    not in initial_conclusions
  )


def test_phase59_6_reaches_fixed_point_in_two_rounds():
  data = build_phase59_6_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    data[
      "result"
    ].round_count
    == 2
  )

  assert (
    data[
      "eta_square_step"
    ]
    in data[
      "result"
    ].round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "final_step"
    ]
    in data[
      "result"
    ].round_results[
      1
    ].new_steps
  )


