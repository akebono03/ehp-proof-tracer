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
















