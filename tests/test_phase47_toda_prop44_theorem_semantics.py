from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  MapSymbol,
  Multiple,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
  TodaProp44DecompositionMap,
)
from map_facts import (
  EHP_H_MAP,
)
from map_property_rules import (
  IsomorphismStatement,
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
  TodaProp44IsomorphismStatement,
  toda_prop44_isomorphism_inference_rule,
)


def build_phase47_4b_data(
  i_name="i",
  n_name="n",
  alpha_name="α",
  hopf_sign=1,
):
  i = ScalarSymbol(
    name=i_name,
  )

  n = ScalarSymbol(
    name=n_name,
  )

  i_minus_one = ScalarSum(
    left=i,
    right=-1,
  )

  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  two_n_minus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  alpha = HomotopyElement(
    name=alpha_name,
    dimension=two_n_minus_one,
  )

  beta = HomotopyElement(
    name="β",
    dimension=i_minus_one,
  )

  gamma = HomotopyElement(
    name="γ",
    dimension=i,
  )

  iota = HomotopyElement(
    name="ι_(2n-1)",
    dimension=two_n_minus_one,
    generator=GeneratorSymbol(
      family="ι",
      index=two_n_minus_one,
    ),
  )

  membership = (
    TodaPrimaryGroupMembershipStatement(
      element=alpha,
      group=TodaPrimaryGroup(
        group_dimension=two_n_minus_one,
        sphere_dimension=n,
      ),
    )
  )

  if hopf_sign == 1:
    hopf_value = iota
  else:
    hopf_value = Multiple(
      coefficient=-1,
      expression=iota,
    )

  hopf_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=alpha,
    ),
    rhs=hopf_value,
    relation_type=RelationType.EQUALITY,
  )

  source_group = DirectSumGroup(
    summands=(
      TodaPrimaryGroup(
        group_dimension=i_minus_one,
        sphere_dimension=n_minus_one,
      ),
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=two_n_minus_one,
      ),
    ),
  )

  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=n,
  )

  formula = Sum(
    left=Suspension(
      expression=beta,
    ),
    right=Composition(
      left=alpha,
      right=gamma,
    ),
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=source_group,
      target_group=target_group,
      alpha=alpha,
      beta=beta,
      gamma=gamma,
      formula=formula,
    )
  )

  return {
    "i": i,
    "n": n,
    "i_minus_one": i_minus_one,
    "n_minus_one": n_minus_one,
    "two_n_minus_one": (
      two_n_minus_one
    ),
    "alpha": alpha,
    "beta": beta,
    "gamma": gamma,
    "iota": iota,
    "membership": membership,
    "hopf_relation": hopf_relation,
    "source_group": source_group,
    "target_group": target_group,
    "formula": formula,
    "decomposition_map": (
      decomposition_map
    ),
  }


def build_phase47_4b_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "membership"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "hopf_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase47_4b_statement_preserves_specific_map_instance():
  data = build_phase47_4b_data()

  statement = (
    TodaProp44IsomorphismStatement(
      map=data[
        "decomposition_map"
      ],
    )
  )

  assert statement.map == (
    data[
      "decomposition_map"
    ]
  )


def test_phase47_4b_statement_is_instance_aware():
  first = build_phase47_4b_data()

  second = build_phase47_4b_data(
    alpha_name="α'",
  )

  assert (
    TodaProp44IsomorphismStatement(
      map=first[
        "decomposition_map"
      ],
    )
    != TodaProp44IsomorphismStatement(
      map=second[
        "decomposition_map"
      ],
    )
  )


def test_phase47_4b_statement_is_not_generic_isomorphism():
  data = build_phase47_4b_data()

  statement = (
    TodaProp44IsomorphismStatement(
      map=data[
        "decomposition_map"
      ],
    )
  )

  assert not isinstance(
    statement,
    IsomorphismStatement,
  )


def test_phase47_4b_rule_requires_membership_hopf_relation_and_map():
  rule = (
    toda_prop44_isomorphism_inference_rule()
  )

  assert len(
    rule.premise_patterns
  ) == 3

  assert (
    rule.premise_patterns[
      0
    ].statement_type
    is TodaPrimaryGroupMembershipStatement
  )

  assert (
    rule.premise_patterns[
      1
    ].statement_type
    is Relation
  )

  assert (
    rule.premise_patterns[
      1
    ].relation_type
    is RelationType.EQUALITY
  )

  assert (
    rule.premise_patterns[
      2
    ].statement_type
    is TodaProp44DecompositionMap
  )


def test_phase47_4b_rule_matches_positive_hopf_instance():
  data = build_phase47_4b_data(
    hopf_sign=1,
  )

  steps = build_phase47_4b_steps(
    data
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is not None


def test_phase47_4b_rule_matches_negative_hopf_instance():
  data = build_phase47_4b_data(
    hopf_sign=-1,
  )

  steps = build_phase47_4b_steps(
    data
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is not None


def test_phase47_4b_rule_derives_instance_aware_isomorphism():
  data = build_phase47_4b_data()

  steps = build_phase47_4b_steps(
    data
  )

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_isomorphism_inference_rule(),
      steps,
    )
  )

  expected = (
    TodaProp44IsomorphismStatement(
      map=data[
        "decomposition_map"
      ],
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase47_4b_valid_instance_derives_exactly_one_theorem_statement():
  data = build_phase47_4b_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_isomorphism_inference_rule(),
      build_phase47_4b_steps(
        data
      ),
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44IsomorphismStatement,
    )
  )

  assert len(
    derived
  ) == 1


def test_phase47_4b_derived_step_preserves_all_three_premises():
  data = build_phase47_4b_data()

  steps = build_phase47_4b_steps(
    data
  )

  rule = (
    toda_prop44_isomorphism_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      steps,
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44IsomorphismStatement,
    )
  )

  assert derived.premises == steps

  assert derived.rule == (
    ProofRule.INFERENCE
  )

  assert derived.inference_rule == (
    rule
  )


def test_phase47_4b_valid_instance_reaches_fixed_point_in_one_round():
  data = build_phase47_4b_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_isomorphism_inference_rule(),
      build_phase47_4b_steps(
        data
      ),
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert len(
    result.round_results[
      0
    ].new_steps
  ) == 1


def test_phase47_4b_rule_rejects_missing_membership():
  data = build_phase47_4b_data()

  steps = build_phase47_4b_steps(
    data
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    (
      steps[
        1
      ],
      steps[
        2
      ],
    ),
  ) is None


def test_phase47_4b_rule_rejects_missing_hopf_relation():
  data = build_phase47_4b_data()

  steps = build_phase47_4b_steps(
    data
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    (
      steps[
        0
      ],
      steps[
        2
      ],
    ),
  ) is None


def test_phase47_4b_rule_rejects_missing_map():
  data = build_phase47_4b_data()

  steps = build_phase47_4b_steps(
    data
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    (
      steps[
        0
      ],
      steps[
        1
      ],
    ),
  ) is None


def test_phase47_4b_rule_rejects_wrong_membership_degree():
  data = build_phase47_4b_data()

  wrong_membership = (
    TodaPrimaryGroupMembershipStatement(
      element=data[
        "alpha"
      ],
      group=TodaPrimaryGroup(
        group_dimension=data[
          "i"
        ],
        sphere_dimension=data[
          "n"
        ],
      ),
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_membership,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "hopf_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase47_4b_rule_rejects_different_alpha_in_map():
  data = build_phase47_4b_data()

  other = build_phase47_4b_data(
    alpha_name="α'",
  )

  steps = (
    ProofStep(
      conclusion=data[
        "membership"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "hopf_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=other[
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase47_4b_rule_rejects_hopf_relation_for_different_alpha():
  data = build_phase47_4b_data()

  other = build_phase47_4b_data(
    alpha_name="α'",
  )

  steps = (
    ProofStep(
      conclusion=data[
        "membership"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=other[
        "hopf_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase47_4b_rule_rejects_wrong_hopf_map():
  data = build_phase47_4b_data()

  wrong_relation = Relation(
    lhs=MapApplication(
      map=MapSymbol(
        name="f",
      ),
      expression=data[
        "alpha"
      ],
    ),
    rhs=data[
      "iota"
    ],
    relation_type=RelationType.EQUALITY,
  )

  steps = (
    ProofStep(
      conclusion=data[
        "membership"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_relation,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase47_4b_rule_rejects_wrong_hopf_value():
  data = build_phase47_4b_data()

  wrong_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=data[
        "alpha"
      ],
    ),
    rhs=HomotopyElement(
      name="δ",
      dimension=data[
        "two_n_minus_one"
      ],
    ),
    relation_type=RelationType.EQUALITY,
  )

  steps = (
    ProofStep(
      conclusion=data[
        "membership"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_relation,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase47_4b_rule_rejects_wrong_target_sphere_dimension():
  data = build_phase47_4b_data()

  wrong_map = (
    TodaProp44DecompositionMap(
      source_group=data[
        "source_group"
      ],
      target_group=TodaPrimaryGroup(
        group_dimension=data[
          "i"
        ],
        sphere_dimension=ScalarSymbol(
          name="m",
        ),
      ),
      alpha=data[
        "alpha"
      ],
      beta=data[
        "beta"
      ],
      gamma=data[
        "gamma"
      ],
      formula=data[
        "formula"
      ],
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "membership"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "hopf_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase47_4b_rule_rejects_reversed_source_summands():
  data = build_phase47_4b_data()

  wrong_map = (
    TodaProp44DecompositionMap(
      source_group=DirectSumGroup(
        summands=(
          data[
            "source_group"
          ].summands[
            1
          ],
          data[
            "source_group"
          ].summands[
            0
          ],
        ),
      ),
      target_group=data[
        "target_group"
      ],
      alpha=data[
        "alpha"
      ],
      beta=data[
        "beta"
      ],
      gamma=data[
        "gamma"
      ],
      formula=data[
        "formula"
      ],
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "membership"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "hopf_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase47_4b_rule_rejects_wrong_formula():
  data = build_phase47_4b_data()

  wrong_map = (
    TodaProp44DecompositionMap(
      source_group=data[
        "source_group"
      ],
      target_group=data[
        "target_group"
      ],
      alpha=data[
        "alpha"
      ],
      beta=data[
        "beta"
      ],
      gamma=data[
        "gamma"
      ],
      formula=HomotopyElement(
        name="δ",
        dimension=data[
          "i"
        ],
      ),
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "membership"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "hopf_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase47_4b_statement_does_not_project_to_generic_isomorphism():
  data = build_phase47_4b_data()

  statement = (
    TodaProp44IsomorphismStatement(
      map=data[
        "decomposition_map"
      ],
    )
  )

  assert not hasattr(
    statement,
    "generic_isomorphism",
  )

  assert not hasattr(
    statement,
    "isomorphism_statement",
  )

  assert not hasattr(
    statement,
    "injective",
  )



