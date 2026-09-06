from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Suspension,
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
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
  toda_eta3_suspension_relation_inference_rule,
  toda_eta_family_definition_statement,
  toda_pi4_3_eta3_generator_inference_rule,
)


def build_phase50_4e_data():
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

  definition = (
    toda_eta_family_definition_statement(
      3
    )
  )

  eta_relation = Relation(
    lhs=eta_3,
    rhs=Suspension(
      expression=eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  pi_4_3 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )

  e_eta_2_group_relation = Relation(
    lhs=pi_4_3,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=Suspension(
        expression=eta_2,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  eta_3_group_relation = Relation(
    lhs=pi_4_3,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_3,
    ),
    relation_type=RelationType.EQUALITY,
  )

  return {
    "eta_2": eta_2,
    "eta_3": eta_3,
    "definition": definition,
    "eta_relation": eta_relation,
    "pi_4_3": pi_4_3,
    "e_eta_2_group_relation": (
      e_eta_2_group_relation
    ),
    "eta_3_group_relation": (
      eta_3_group_relation
    ),
  }


def test_phase50_4e_eta_family_definition_is_statement():
  data = build_phase50_4e_data()

  assert isinstance(
    data[
      "definition"
    ],
    TodaEtaFamilyDefinitionStatement,
  )


def test_phase50_4e_eta3_definition_preserves_index():
  data = build_phase50_4e_data()

  assert data[
    "definition"
  ].index == 3


def test_phase50_4e_eta3_definition_preserves_eta3():
  data = build_phase50_4e_data()

  assert data[
    "definition"
  ].element == (
    data[
      "eta_3"
    ]
  )


def test_phase50_4e_eta3_definition_uses_iterated_suspension_once():
  data = build_phase50_4e_data()

  assert data[
    "definition"
  ].iterated_suspension == (
    IteratedSuspension(
      expression=data[
        "eta_2"
      ],
      exponent=1,
    )
  )


def test_phase50_4e_eta2_definition_has_exponent_zero():
  definition = (
    toda_eta_family_definition_statement(
      2
    )
  )

  assert definition.iterated_suspension == (
    IteratedSuspension(
      expression=definition.element,
      exponent=0,
    )
  )


def test_phase50_4e_eta_family_rejects_index_below_two():
  try:
    toda_eta_family_definition_statement(
      1
    )
  except ValueError:
    return

  assert False


def test_phase50_4e_eta3_bridge_matches_definition():
  data = build_phase50_4e_data()

  step = ProofStep(
    conclusion=data[
      "definition"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_eta3_suspension_relation_inference_rule(),
    (
      step,
    ),
  ) is not None


def test_phase50_4e_eta3_bridge_derives_eta3_equals_e_eta2():
  data = build_phase50_4e_data()

  step = ProofStep(
    conclusion=data[
      "definition"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      toda_eta3_suspension_relation_inference_rule(),
      (
        step,
      ),
    )
  )

  conclusions = tuple(
    derived.conclusion
    for derived in result.steps
  )

  assert data[
    "eta_relation"
  ] in conclusions


def test_phase50_4e_eta3_bridge_does_not_match_eta2_definition():
  definition = (
    toda_eta_family_definition_statement(
      2
    )
  )

  step = ProofStep(
    conclusion=definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_eta3_suspension_relation_inference_rule(),
    (
      step,
    ),
  ) is None


def test_phase50_4e_generator_rule_matches():
  data = build_phase50_4e_data()

  steps = (
    ProofStep(
      conclusion=data[
        "e_eta_2_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "eta_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi4_3_eta3_generator_inference_rule(),
    steps,
  ) is not None


def test_phase50_4e_generator_rule_derives_pi4_3_on_eta3():
  data = build_phase50_4e_data()

  steps = (
    ProofStep(
      conclusion=data[
        "e_eta_2_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "eta_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  result = (
    run_inference_until_stable_with_history(
      toda_pi4_3_eta3_generator_inference_rule(),
      steps,
    )
  )

  conclusions = tuple(
    derived.conclusion
    for derived in result.steps
  )

  assert data[
    "eta_3_group_relation"
  ] in conclusions


def test_phase50_4e_generator_rule_rejects_wrong_order():
  data = build_phase50_4e_data()

  wrong_group = Relation(
    lhs=data[
      "pi_4_3"
    ],
    rhs=FiniteCyclicGroup(
      order=3,
      generator=Suspension(
        expression=data[
          "eta_2"
        ],
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  steps = (
    ProofStep(
      conclusion=wrong_group,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "eta_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi4_3_eta3_generator_inference_rule(),
    steps,
  ) is None


def test_phase50_4e_generator_rule_rejects_wrong_generator():
  data = build_phase50_4e_data()

  wrong_group = Relation(
    lhs=data[
      "pi_4_3"
    ],
    rhs=FiniteCyclicGroup(
      order=2,
      generator=data[
        "eta_2"
      ],
    ),
    relation_type=RelationType.EQUALITY,
  )

  steps = (
    ProofStep(
      conclusion=wrong_group,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "eta_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_pi4_3_eta3_generator_inference_rule(),
    steps,
  ) is None


def test_phase50_4e_end_to_end_derives_eta3_group():
  data = build_phase50_4e_data()

  initial_steps = (
    ProofStep(
      conclusion=data[
        "definition"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "e_eta_2_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  rules = (
    toda_eta3_suspension_relation_inference_rule(),
    toda_pi4_3_eta3_generator_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      initial_steps,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "eta_relation"
  ] in conclusions

  assert data[
    "eta_3_group_relation"
  ] in conclusions


def test_phase50_4e_end_to_end_reaches_fixed_point_in_two_rounds():
  data = build_phase50_4e_data()

  initial_steps = (
    ProofStep(
      conclusion=data[
        "definition"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "e_eta_2_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  rules = (
    toda_eta3_suspension_relation_inference_rule(),
    toda_pi4_3_eta3_generator_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      initial_steps,
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2


def test_phase50_4e_all_derived_steps_preserve_provenance():
  data = build_phase50_4e_data()

  initial_steps = (
    ProofStep(
      conclusion=data[
        "definition"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "e_eta_2_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  rules = (
    toda_eta3_suspension_relation_inference_rule(),
    toda_pi4_3_eta3_generator_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      initial_steps,
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if step.rule
    == ProofRule.INFERENCE
  )

  assert len(
    derived
  ) == 2

  assert all(
    step.inference_rule
    is not None
    for step in derived
  )


