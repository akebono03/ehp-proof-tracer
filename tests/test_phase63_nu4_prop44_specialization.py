from dataclasses import replace

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
)
from homotopy_groups import (
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
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
from test_phase60_lemma54_integration import (
  build_phase60_9_data,
)
from toda_rules import (
  Toda56Nu4Prop44SpecializationStatement,
  toda_56_nu4_prop44_specialization_inference_rule,
)


def build_phase63_2_data():
  phase60_9 = (
    build_phase60_9_data()
  )

  lemma54_step = (
    phase60_9[
      "integration_step"
    ]
  )

  nu_4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  iota_7 = HomotopyElement(
    name="ι_7",
    dimension=7,
    generator=GeneratorSymbol(
      family="ι",
      index=7,
    ),
  )

  expected_membership = (
    TodaPrimaryGroupMembershipStatement(
      element=nu_4,
      group=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=4,
      ),
    )
  )

  expected_hopf_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=nu_4,
    ),
    rhs=iota_7,
    relation_type=RelationType.EQUALITY,
  )

  expected_statement = (
    Toda56Nu4Prop44SpecializationStatement(
      lemma54_statement=(
        lemma54_step.conclusion
      ),
      n=4,
      alpha=nu_4,
      membership=expected_membership,
      hopf_relation=(
        expected_hopf_relation
      ),
    )
  )

  rule = (
    toda_56_nu4_prop44_specialization_inference_rule()
  )

  premise_steps = (
    lemma54_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  specialization_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase60_9": phase60_9,
    "lemma54_step": lemma54_step,
    "nu_4": nu_4,
    "iota_7": iota_7,
    "expected_membership": (
      expected_membership
    ),
    "expected_hopf_relation": (
      expected_hopf_relation
    ),
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "specialization_step": (
      specialization_step
    ),
  }


def test_phase63_2_reuses_derived_lemma54():
  data = build_phase63_2_data()

  assert (
    data[
      "lemma54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase63_2_rule_matches_derived_lemma54():
  data = build_phase63_2_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase63_2_derives_specialization_statement():
  data = build_phase63_2_data()

  assert (
    data[
      "specialization_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "specialization_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase63_2_specialization_records_n_four():
  data = build_phase63_2_data()

  assert (
    data[
      "specialization_step"
    ].conclusion.n
    == 4
  )


def test_phase63_2_specialization_records_alpha_nu4():
  data = build_phase63_2_data()

  assert (
    data[
      "specialization_step"
    ].conclusion.alpha
    == data[
      "nu_4"
    ]
  )


def test_phase63_2_converts_membership_to_toda_primary_group():
  data = build_phase63_2_data()

  statement = (
    data[
      "specialization_step"
    ].conclusion
  )

  assert isinstance(
    statement.membership,
    TodaPrimaryGroupMembershipStatement,
  )

  assert (
    statement.membership
    == data[
      "expected_membership"
    ]
  )

  assert (
    statement.membership.group
    == TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
    )
  )


def test_phase63_2_preserves_hopf_relation():
  data = build_phase63_2_data()

  assert (
    data[
      "specialization_step"
    ].conclusion.hopf_relation
    == data[
      "expected_hopf_relation"
    ]
  )


def test_phase63_2_preserves_lemma54_statement():
  data = build_phase63_2_data()

  assert (
    data[
      "specialization_step"
    ].conclusion.lemma54_statement
    is data[
      "lemma54_step"
    ].conclusion
  )


def test_phase63_2_provenance_uses_exactly_lemma54():
  data = build_phase63_2_data()

  assert (
    data[
      "specialization_step"
    ].premises
    == (
      data[
        "lemma54_step"
      ],
    )
  )


def test_phase63_2_rejects_given_lemma54():
  data = build_phase63_2_data()

  given_lemma54_step = ProofStep(
    conclusion=(
      data[
        "lemma54_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      given_lemma54_step,
    ),
  ) is None


def test_phase63_2_rejects_wrong_nu4():
  data = build_phase63_2_data()

  wrong_nu4 = HomotopyElement(
    name="ν₅",
    dimension=5,
    source=8,
    target=5,
    generator=GeneratorSymbol(
      family="ν",
      index=5,
    ),
  )

  wrong_statement = replace(
    data[
      "lemma54_step"
    ].conclusion,
    nu4=wrong_nu4,
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase63_2_rejects_wrong_membership():
  data = build_phase63_2_data()

  wrong_membership = (
    HomotopyGroupMembershipStatement(
      element=data[
        "nu_4"
      ],
      group_dimension=8,
      sphere_dimension=4,
    )
  )

  wrong_statement = replace(
    data[
      "lemma54_step"
    ].conclusion,
    membership=wrong_membership,
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase63_2_rejects_wrong_hopf_relation():
  data = build_phase63_2_data()

  iota_8 = HomotopyElement(
    name="ι_8",
    dimension=8,
    generator=GeneratorSymbol(
      family="ι",
      index=8,
    ),
  )

  wrong_hopf_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=data[
        "nu_4"
      ],
    ),
    rhs=iota_8,
    relation_type=RelationType.EQUALITY,
  )

  wrong_statement = replace(
    data[
      "lemma54_step"
    ].conclusion,
    hopf_relation=wrong_hopf_relation,
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase63_2_final_result_is_not_given():
  data = build_phase63_2_data()

  assert (
    data[
      "specialization_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "specialization_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase63_2_reaches_fixed_point_in_one_round():
  data = build_phase63_2_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    result.round_count
    == 1
  )

  assert (
    data[
      "specialization_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )


