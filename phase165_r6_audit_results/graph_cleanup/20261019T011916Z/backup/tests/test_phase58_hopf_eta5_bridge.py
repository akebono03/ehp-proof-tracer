from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
)
from map_facts import (
  EHP_H_MAP,
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
from relation_rules import (
  equality_transitivity_inference_rule,
)
from test_phase58_lemma52_specialization import (
  build_phase58_3_data,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
  toda_53_eta5_iterated_suspension_bridge_inference_rule,
  toda_eta_family_definition_statement,
)


def build_phase58_4_data():
  phase58_3 = (
    build_phase58_3_data()
  )

  eta3_definition = (
    toda_eta_family_definition_statement(
      3
    )
  )

  eta5_definition = (
    toda_eta_family_definition_statement(
      5
    )
  )

  eta3_definition_step = ProofStep(
    conclusion=eta3_definition,
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

  eta5_definition_element = (
    HomotopyElement(
      name="η_5",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )
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

  expected_eta5_bridge = Relation(
    lhs=IteratedSuspension(
      expression=eta_3,
      exponent=2,
    ),
    rhs=eta_5,
    relation_type=RelationType.EQUALITY,
  )

  nu_prime = (
    phase58_3[
      "phase58_2"
    ][
      "nu_prime"
    ]
  )

  expected_hopf_eta5 = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=nu_prime,
    ),
    rhs=eta_5,
    relation_type=RelationType.EQUALITY,
  )

  bridge_rule = (
    toda_53_eta5_iterated_suspension_bridge_inference_rule()
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  bridge_result = (
    run_inference_until_stable_with_history(
      bridge_rule,
      (
        eta3_definition_step,
        eta5_definition_step,
      ),
    )
  )

  bridge_step = next(
    step
    for step in bridge_result.steps
    if (
      step.conclusion
      == expected_eta5_bridge
    )
  )

  hopf_step = next(
    step
    for step in phase58_3[
      "result"
    ].steps
    if (
      step.conclusion
      == phase58_3[
        "expected_hopf_relation"
      ]
    )
  )

  result = (
    run_inference_until_stable_with_history(
      (
        transitivity_rule,
      ),
      (
        hopf_step,
        bridge_step,
      ),
    )
  )

  return {
    "phase58_3": phase58_3,
    "eta3_definition": (
      eta3_definition
    ),
    "eta5_definition": (
      eta5_definition
    ),
    "eta3_definition_step": (
      eta3_definition_step
    ),
    "eta5_definition_step": (
      eta5_definition_step
    ),
    "eta_3": eta_3,
    "eta5_definition_element": (
      eta5_definition_element
    ),
    "eta_5": eta_5,
    "expected_eta5_bridge": (
      expected_eta5_bridge
    ),
    "expected_hopf_eta5": (
      expected_hopf_eta5
    ),
    "bridge_rule": bridge_rule,
    "transitivity_rule": (
      transitivity_rule
    ),
    "bridge_result": bridge_result,
    "bridge_step": bridge_step,
    "hopf_step": hopf_step,
    "result": result,
  }


def test_phase58_4_eta3_definition_is_concrete():
  data = build_phase58_4_data()

  definition = data[
    "eta3_definition"
  ]

  assert isinstance(
    definition,
    TodaEtaFamilyDefinitionStatement,
  )

  assert definition.index == 3

  assert (
    definition.element
    == data[
      "eta_3"
    ]
  )


def test_phase58_4_eta5_definition_is_concrete():
  data = build_phase58_4_data()

  definition = data[
    "eta5_definition"
  ]

  assert isinstance(
    definition,
    TodaEtaFamilyDefinitionStatement,
  )

  assert definition.index == 5

  assert (
    definition.element
    == data[
      "eta5_definition_element"
    ]
  )

  assert (
    definition.element.generator
    == data[
      "eta_5"
    ].generator
  )

  assert (
    definition.element.source
    == data[
      "eta_5"
    ].source
  )

  assert (
    definition.element.target
    == data[
      "eta_5"
    ].target
  )


def test_phase58_4_eta5_definition_is_e3_eta2():
  data = build_phase58_4_data()

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

  assert (
    data[
      "eta5_definition"
    ].iterated_suspension
    == IteratedSuspension(
      expression=eta_2,
      exponent=3,
    )
  )


def test_phase58_4_bridge_rule_matches_concrete_eta_definitions():
  data = build_phase58_4_data()

  assert find_inference_match(
    data[
      "bridge_rule"
    ],
    (
      data[
        "eta3_definition_step"
      ],
      data[
        "eta5_definition_step"
      ],
    ),
  ) is not None


def test_phase58_4_derives_e2_eta3_equals_eta5():
  data = build_phase58_4_data()

  assert (
    data[
      "bridge_step"
    ].conclusion
    == data[
      "expected_eta5_bridge"
    ]
  )

  assert (
    data[
      "bridge_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase58_4_eta5_bridge_preserves_two_definitions():
  data = build_phase58_4_data()

  assert (
    data[
      "bridge_step"
    ].premises
    == (
      data[
        "eta3_definition_step"
      ],
      data[
        "eta5_definition_step"
      ],
    )
  )


def test_phase58_4_bridge_rejects_wrong_eta5_index():
  data = build_phase58_4_data()

  wrong_definition = (
    toda_eta_family_definition_statement(
      4
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


def test_phase58_4_reuses_phase58_3_hopf_result():
  data = build_phase58_4_data()

  assert (
    data[
      "hopf_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "hopf_step"
    ].conclusion
    == data[
      "phase58_3"
    ][
      "expected_hopf_relation"
    ]
  )


def test_phase58_4_generic_transitivity_matches():
  data = build_phase58_4_data()

  assert find_inference_match(
    data[
      "transitivity_rule"
    ],
    (
      data[
        "hopf_step"
      ],
      data[
        "bridge_step"
      ],
    ),
  ) is not None


def test_phase58_4_derives_h_nu_prime_equals_eta5():
  data = build_phase58_4_data()

  final_steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_hopf_eta5"
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


def test_phase58_4_final_hopf_value_uses_generic_transitivity():
  data = build_phase58_4_data()

  final_step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_hopf_eta5"
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
        "hopf_step"
      ],
      data[
        "bridge_step"
      ],
    )
  )


def test_phase58_4_final_result_is_not_given():
  data = build_phase58_4_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in (
      data[
        "hopf_step"
      ],
      data[
        "bridge_step"
      ],
    )
  )

  assert (
    data[
      "expected_hopf_eta5"
    ]
    not in initial_conclusions
  )


def test_phase58_4_reaches_fixed_point():
  data = build_phase58_4_data()

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


