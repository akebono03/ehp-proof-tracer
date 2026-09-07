from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  Suspension,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from relation_rules import (
  equality_preserved_under_left_composition_inference_rule,
  equality_preserved_under_right_composition_inference_rule,
  equality_transitivity_inference_rule,
)
from test_phase58_lemma52_specialization import (
  build_phase58_3_data,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
  toda_53_eta4_suspension_bridge_inference_rule,
  toda_eta_family_definition_statement,
)


def build_phase58_5_data():
  phase58_3 = (
    build_phase58_3_data()
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

  eta4_definition_element = (
    HomotopyElement(
      name="η_4",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )
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

  expected_eta4_bridge = Relation(
    lhs=Suspension(
      expression=eta_3,
    ),
    rhs=eta_4,
    relation_type=RelationType.EQUALITY,
  )

  bridge_rule = (
    toda_53_eta4_suspension_bridge_inference_rule()
  )

  bridge_result = (
    run_inference_until_stable_with_history(
      bridge_rule,
      (
        eta3_definition_step,
        eta4_definition_step,
      ),
    )
  )

  bridge_step = next(
    step
    for step in bridge_result.steps
    if (
      step.conclusion
      == expected_eta4_bridge
    )
  )

  right_rule = (
    equality_preserved_under_right_composition_inference_rule(
      eta_5,
    )
  )

  right_match = find_inference_match(
    right_rule,
    (
      bridge_step,
    ),
  )

  if right_match is None:
    raise AssertionError(
      "Phase 58-5 right-composition "
      "rule did not match"
    )

  right_step = (
    apply_inference_match(
      right_match
    )
  )

  expected_right_relation = Relation(
    lhs=Composition(
      left=Suspension(
        expression=eta_3,
      ),
      right=eta_5,
    ),
    rhs=Composition(
      left=eta_4,
      right=eta_5,
    ),
    relation_type=RelationType.EQUALITY,
  )

  left_rule = (
    equality_preserved_under_left_composition_inference_rule(
      eta_3,
    )
  )

  left_match = find_inference_match(
    left_rule,
    (
      right_step,
    ),
  )

  if left_match is None:
    raise AssertionError(
      "Phase 58-5 left-composition "
      "rule did not match"
    )

  composition_step = (
    apply_inference_match(
      left_match
    )
  )

  expected_composition_relation = Relation(
    lhs=Composition(
      left=eta_3,
      right=Composition(
        left=Suspension(
          expression=eta_3,
        ),
        right=eta_5,
      ),
    ),
    rhs=Composition(
      left=eta_3,
      right=Composition(
        left=eta_4,
        right=eta_5,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  double_step = next(
    step
    for step in phase58_3[
      "result"
    ].steps
    if (
      step.conclusion
      == phase58_3[
        "expected_double_relation"
      ]
    )
  )

  nu_prime = (
    phase58_3[
      "phase58_2"
    ][
      "nu_prime"
    ]
  )

  expected_final_relation = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=nu_prime,
    ),
    rhs=Composition(
      left=eta_3,
      right=Composition(
        left=eta_4,
        right=eta_5,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      transitivity_rule,
      (
        double_step,
        composition_step,
      ),
    )
  )

  return {
    "phase58_3": phase58_3,
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
    "eta_3": eta_3,
    "eta4_definition_element": (
      eta4_definition_element
    ),
    "eta_4": eta_4,
    "eta_5": eta_5,
    "expected_eta4_bridge": (
      expected_eta4_bridge
    ),
    "bridge_rule": bridge_rule,
    "bridge_result": bridge_result,
    "bridge_step": bridge_step,
    "right_rule": right_rule,
    "right_match": right_match,
    "expected_right_relation": (
      expected_right_relation
    ),
    "right_step": right_step,
    "left_rule": left_rule,
    "left_match": left_match,
    "expected_composition_relation": (
      expected_composition_relation
    ),
    "composition_step": (
      composition_step
    ),
    "double_step": double_step,
    "expected_final_relation": (
      expected_final_relation
    ),
    "transitivity_rule": (
      transitivity_rule
    ),
    "result": result,
  }


def test_phase58_5_eta4_definition_is_concrete():
  data = build_phase58_5_data()

  definition = data[
    "eta4_definition"
  ]

  assert isinstance(
    definition,
    TodaEtaFamilyDefinitionStatement,
  )

  assert definition.index == 4

  assert (
    definition.element
    == data[
      "eta4_definition_element"
    ]
  )


def test_phase58_5_eta4_definition_preserves_generator_identity():
  data = build_phase58_5_data()

  assert (
    data[
      "eta4_definition"
    ].element.generator
    == data[
      "eta_4"
    ].generator
  )


def test_phase58_5_bridge_rule_matches_concrete_eta_definitions():
  data = build_phase58_5_data()

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


def test_phase58_5_derives_e_eta3_equals_eta4():
  data = build_phase58_5_data()

  assert (
    data[
      "bridge_step"
    ].conclusion
    == data[
      "expected_eta4_bridge"
    ]
  )

  assert (
    data[
      "bridge_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase58_5_eta4_bridge_preserves_definition_provenance():
  data = build_phase58_5_data()

  assert (
    data[
      "bridge_step"
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


def test_phase58_5_reuses_phase58_3_double_value():
  data = build_phase58_5_data()

  assert (
    data[
      "double_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "double_step"
    ].conclusion
    == data[
      "phase58_3"
    ][
      "expected_double_relation"
    ]
  )


def test_phase58_5_right_composition_derives_eta5_relation():
  data = build_phase58_5_data()

  assert (
    data[
      "right_step"
    ].conclusion
    == data[
      "expected_right_relation"
    ]
  )

  assert (
    data[
      "right_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase58_5_left_composition_derives_full_rhs_relation():
  data = build_phase58_5_data()

  assert (
    data[
      "composition_step"
    ].conclusion
    == data[
      "expected_composition_relation"
    ]
  )

  assert (
    data[
      "composition_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase58_5_generic_transitivity_matches():
  data = build_phase58_5_data()

  assert find_inference_match(
    data[
      "transitivity_rule"
    ],
    (
      data[
        "double_step"
      ],
      data[
        "composition_step"
      ],
    ),
  ) is not None


def test_phase58_5_derives_final_double_value():
  data = build_phase58_5_data()

  final_steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_final_relation"
      ]
    )
  )

  assert len(
    final_steps
  ) == 1

  assert (
    final_steps[
      0
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase58_5_final_value_is_eta3_eta4_eta5():
  data = build_phase58_5_data()

  relation = data[
    "expected_final_relation"
  ]

  assert relation.rhs == (
    Composition(
      left=data[
        "eta_3"
      ],
      right=Composition(
        left=data[
          "eta_4"
        ],
        right=data[
          "eta_5"
        ],
      ),
    )
  )


def test_phase58_5_final_value_uses_generic_transitivity():
  data = build_phase58_5_data()

  final_step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_final_relation"
      ]
    )
  )

  assert (
    final_step.inference_rule
    == data[
      "transitivity_rule"
    ]
  )

  assert (
    final_step.premises
    == (
      data[
        "double_step"
      ],
      data[
        "composition_step"
      ],
    )
  )


def test_phase58_5_final_result_is_not_given():
  data = build_phase58_5_data()

  assert (
    data[
      "expected_final_relation"
    ]
    not in (
      data[
        "double_step"
      ].conclusion,
      data[
        "composition_step"
      ].conclusion,
    )
  )


def test_phase58_5_bridge_rejects_wrong_eta4_index():
  data = build_phase58_5_data()

  wrong_definition = (
    toda_eta_family_definition_statement(
      5
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
        "eta3_definition_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase58_5_reaches_fixed_point():
  data = build_phase58_5_data()

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
    == 1
  )





