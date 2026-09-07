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
from test_phase59_n3_ehp_chain import (
  build_phase59_3_data,
)
from test_phase59_toda52_pi4_2_transport import (
  build_phase59_2_data,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
  toda_eta_family_definition_statement,
  toda_prop53_n3_eta_square_suspension_bridge_inference_rule,
  toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule,
)


def build_phase59_4_data():
  phase59_2 = (
    build_phase59_2_data()
  )

  phase59_3 = (
    build_phase59_3_data()
  )

  pi4_2_step = (
    phase59_2[
      "result_steps"
    ][
      0
    ]
  )

  suspension_isomorphism_step = next(
    step
    for step in phase59_3[
      "result"
    ].steps
    if (
      step.conclusion
      == phase59_3[
        "expected_suspension_isomorphism"
      ]
    )
  )

  eta3_definition = (
    toda_eta_family_definition_statement(
      3
    )
  )

  eta4_definition = (
    toda_eta_family_definition_statement(
      4
    )
  )

  eta3_definition_step = ProofStep(
    conclusion=eta3_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta4_definition_step = ProofStep(
    conclusion=eta4_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
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

  eta_2_squared = Composition(
    left=eta_2,
    right=eta_3,
  )

  eta_3_squared = Composition(
    left=eta_3,
    right=eta_4,
  )

  expected_eta_square_relation = Relation(
    lhs=Suspension(
      expression=eta_2_squared,
    ),
    rhs=eta_3_squared,
    relation_type=RelationType.EQUALITY,
  )

  expected_pi5_3_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_3_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  bridge_rule = (
    toda_prop53_n3_eta_square_suspension_bridge_inference_rule()
  )

  transport_rule = (
    toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule()
  )

  rules = (
    bridge_rule,
    transport_rule,
  )

  premise_steps = (
    pi4_2_step,
    suspension_isomorphism_step,
    eta3_definition_step,
    eta4_definition_step,
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
      == expected_pi5_3_relation
    )
  )

  return {
    "phase59_2": phase59_2,
    "phase59_3": phase59_3,
    "pi4_2_step": pi4_2_step,
    "suspension_isomorphism_step": (
      suspension_isomorphism_step
    ),
    "eta3_definition": (
      eta3_definition
    ),
    "eta4_definition": (
      eta4_definition
    ),
    "eta3_definition_step": (
      eta3_definition_step
    ),
    "eta4_definition_step": (
      eta4_definition_step
    ),
    "eta_2": eta_2,
    "eta_3": eta_3,
    "eta_4": eta_4,
    "eta_2_squared": (
      eta_2_squared
    ),
    "eta_3_squared": (
      eta_3_squared
    ),
    "expected_eta_square_relation": (
      expected_eta_square_relation
    ),
    "expected_pi5_3_relation": (
      expected_pi5_3_relation
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


def test_phase59_4_reuses_phase59_2_pi4_2_relation():
  data = build_phase59_4_data()

  step = data[
    "pi4_2_step"
  ]

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert (
    step.conclusion
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=4,
        sphere_dimension=2,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=data[
          "eta_2_squared"
        ],
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase59_4_reuses_phase59_3_suspension_isomorphism():
  data = build_phase59_4_data()

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


def test_phase59_4_eta3_definition_is_existing_definition():
  data = build_phase59_4_data()

  assert isinstance(
    data[
      "eta3_definition"
    ],
    TodaEtaFamilyDefinitionStatement,
  )

  assert (
    data[
      "eta3_definition"
    ].index
    == 3
  )

  assert (
    data[
      "eta3_definition"
    ].element
    == data[
      "eta_3"
    ]
  )


def test_phase59_4_eta4_definition_preserves_generator_identity():
  data = build_phase59_4_data()

  definition = data[
    "eta4_definition"
  ]

  assert (
    definition.index
    == 4
  )

  assert (
    definition.element.generator
    == data[
      "eta_4"
    ].generator
  )


def test_phase59_4_eta2_squared_uses_composition():
  data = build_phase59_4_data()

  assert (
    data[
      "eta_2_squared"
    ]
    == Composition(
      left=data[
        "eta_2"
      ],
      right=data[
        "eta_3"
      ],
    )
  )


def test_phase59_4_eta3_squared_uses_composition():
  data = build_phase59_4_data()

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


def test_phase59_4_bridge_rule_matches_eta_definitions():
  data = build_phase59_4_data()

  assert find_inference_match(
    data[
      "bridge_rule"
    ],
    (
      data[
        "eta3_definition_step"
      ],
      data[
        "eta4_definition_step"
      ],
    ),
  ) is not None


def test_phase59_4_derives_e_eta2_squared_equals_eta3_squared():
  data = build_phase59_4_data()

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


def test_phase59_4_eta_square_bridge_preserves_definition_provenance():
  data = build_phase59_4_data()

  assert (
    data[
      "eta_square_step"
    ].premises
    == (
      data[
        "eta3_definition_step"
      ],
      data[
        "eta4_definition_step"
      ],
    )
  )


def test_phase59_4_transport_rule_matches_derived_dependencies():
  data = build_phase59_4_data()

  assert find_inference_match(
    data[
      "transport_rule"
    ],
    (
      data[
        "pi4_2_step"
      ],
      data[
        "suspension_isomorphism_step"
      ],
      data[
        "eta_square_step"
      ],
    ),
  ) is not None


def test_phase59_4_derives_pi5_3_order_two_eta3_squared():
  data = build_phase59_4_data()

  step = data[
    "final_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_pi5_3_relation"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase59_4_final_generator_is_eta3_squared():
  data = build_phase59_4_data()

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
      "eta_3_squared"
    ]
  )


def test_phase59_4_final_provenance_uses_three_derived_dependencies():
  data = build_phase59_4_data()

  final_step = data[
    "final_step"
  ]

  assert (
    final_step.premises
    == (
      data[
        "pi4_2_step"
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


def test_phase59_4_rejects_given_pi4_2_relation():
  data = build_phase59_4_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "pi4_2_step"
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


def test_phase59_4_rejects_given_suspension_isomorphism():
  data = build_phase59_4_data()

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
        "pi4_2_step"
      ],
      given_step,
      data[
        "eta_square_step"
      ],
    ),
  ) is None


def test_phase59_4_rejects_given_eta_square_bridge():
  data = build_phase59_4_data()

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
        "pi4_2_step"
      ],
      data[
        "suspension_isomorphism_step"
      ],
      given_step,
    ),
  ) is None


def test_phase59_4_final_result_is_not_given():
  data = build_phase59_4_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_pi5_3_relation"
    ]
    not in initial_conclusions
  )


def test_phase59_4_reaches_fixed_point_in_two_rounds():
  data = build_phase59_4_data()

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



