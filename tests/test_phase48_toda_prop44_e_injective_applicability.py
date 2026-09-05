from expression import (
  Composition,
  HomotopyElement,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_E_MAP,
)
from map_property_rules import (
  InjectiveMapStatement,
  isomorphism_implies_injective_inference_rule,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaProp44FirstSummandRestrictionStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SuspensionInjectiveStatement,
  toda_prop44_suspension_injective_inference_rule,
)


def build_phase48_5_data(
  i_name="i",
  n_name="n",
  alpha_name="α",
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

  first_summand = TodaPrimaryGroup(
    group_dimension=i_minus_one,
    sphere_dimension=n_minus_one,
  )

  second_summand = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=two_n_minus_one,
  )

  source_group = DirectSumGroup(
    summands=(
      first_summand,
      second_summand,
    ),
  )

  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=n,
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

  suspension_map = TodaSuspensionMap(
    source_group=first_summand,
    target_group=target_group,
  )

  isomorphism = (
    TodaProp44IsomorphismStatement(
      map=decomposition_map,
    )
  )

  restriction = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=decomposition_map,
      suspension_map=suspension_map,
    )
  )

  injectivity = (
    TodaProp44SuspensionInjectiveStatement(
      map=suspension_map,
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
    "first_summand": first_summand,
    "second_summand": second_summand,
    "source_group": source_group,
    "target_group": target_group,
    "alpha": alpha,
    "beta": beta,
    "gamma": gamma,
    "formula": formula,
    "decomposition_map": (
      decomposition_map
    ),
    "suspension_map": suspension_map,
    "isomorphism": isomorphism,
    "restriction": restriction,
    "injectivity": injectivity,
  }


def build_phase48_5_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "restriction"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase48_5_valid_instance_has_inference_match():
  data = build_phase48_5_data()

  match = find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    build_phase48_5_steps(
      data
    ),
  )

  assert match is not None


def test_phase48_5_valid_instance_derives_expected_injectivity():
  data = build_phase48_5_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_suspension_injective_inference_rule(),
      build_phase48_5_steps(
        data
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "injectivity"
  ] in conclusions


def test_phase48_5_valid_instance_derives_exactly_one_injectivity():
  data = build_phase48_5_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_suspension_injective_inference_rule(),
      build_phase48_5_steps(
        data
      ),
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44SuspensionInjectiveStatement,
    )
  )

  assert len(
    derived
  ) == 1


def test_phase48_5_derived_injectivity_preserves_both_premises():
  data = build_phase48_5_data()

  steps = build_phase48_5_steps(
    data
  )

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_suspension_injective_inference_rule(),
      steps,
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44SuspensionInjectiveStatement,
    )
  )

  assert derived.premises == steps


def test_phase48_5_derived_injectivity_preserves_proof_rule():
  data = build_phase48_5_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_suspension_injective_inference_rule(),
      build_phase48_5_steps(
        data
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44SuspensionInjectiveStatement,
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )


def test_phase48_5_derived_injectivity_preserves_inference_rule():
  data = build_phase48_5_data()

  rule = (
    toda_prop44_suspension_injective_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      build_phase48_5_steps(
        data
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44SuspensionInjectiveStatement,
    )
  )

  assert derived.inference_rule == (
    rule
  )


def test_phase48_5_valid_instance_reaches_fixed_point_in_one_round():
  data = build_phase48_5_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_suspension_injective_inference_rule(),
      build_phase48_5_steps(
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


def test_phase48_5_missing_isomorphism_is_rejected():
  data = build_phase48_5_data()

  restriction_step = ProofStep(
    conclusion=data[
      "restriction"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    (
      restriction_step,
    ),
  ) is None


def test_phase48_5_missing_restriction_is_rejected():
  data = build_phase48_5_data()

  isomorphism_step = ProofStep(
    conclusion=data[
      "isomorphism"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    (
      isomorphism_step,
    ),
  ) is None


def test_phase48_5_cross_i_instance_is_rejected():
  first = build_phase48_5_data(
    i_name="i",
  )

  second = build_phase48_5_data(
    i_name="j",
  )

  steps = (
    ProofStep(
      conclusion=first[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=second[
        "restriction"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    steps,
  ) is None


def test_phase48_5_cross_n_instance_is_rejected():
  first = build_phase48_5_data(
    n_name="n",
  )

  second = build_phase48_5_data(
    n_name="m",
  )

  steps = (
    ProofStep(
      conclusion=first[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=second[
        "restriction"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    steps,
  ) is None


def test_phase48_5_cross_alpha_instance_is_rejected():
  first = build_phase48_5_data(
    alpha_name="α",
  )

  second = build_phase48_5_data(
    alpha_name="α'",
  )

  steps = (
    ProofStep(
      conclusion=first[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=second[
        "restriction"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    steps,
  ) is None


def test_phase48_5_same_groups_but_different_decomposition_map_is_rejected():
  data = build_phase48_5_data()

  other_alpha = HomotopyElement(
    name="α'",
    dimension=data[
      "two_n_minus_one"
    ],
  )

  other_formula = Sum(
    left=Suspension(
      expression=data[
        "beta"
      ],
    ),
    right=Composition(
      left=other_alpha,
      right=data[
        "gamma"
      ],
    ),
  )

  other_map = (
    TodaProp44DecompositionMap(
      source_group=data[
        "source_group"
      ],
      target_group=data[
        "target_group"
      ],
      alpha=other_alpha,
      beta=data[
        "beta"
      ],
      gamma=data[
        "gamma"
      ],
      formula=other_formula,
    )
  )

  other_restriction = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=other_map,
      suspension_map=data[
        "suspension_map"
      ],
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=other_restriction,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    steps,
  ) is None


def test_phase48_5_wrong_suspension_source_is_rejected():
  data = build_phase48_5_data()

  wrong_suspension = TodaSuspensionMap(
    source_group=data[
      "second_summand"
    ],
    target_group=data[
      "target_group"
    ],
  )

  wrong_restriction = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=data[
        "decomposition_map"
      ],
      suspension_map=wrong_suspension,
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_restriction,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    steps,
  ) is None


def test_phase48_5_wrong_suspension_target_is_rejected():
  data = build_phase48_5_data()

  wrong_target = TodaPrimaryGroup(
    group_dimension=ScalarSymbol(
      name="j",
    ),
    sphere_dimension=data[
      "n"
    ],
  )

  wrong_suspension = TodaSuspensionMap(
    source_group=data[
      "first_summand"
    ],
    target_group=wrong_target,
  )

  wrong_restriction = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=data[
        "decomposition_map"
      ],
      suspension_map=wrong_suspension,
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_restriction,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    steps,
  ) is None


def test_phase48_5_second_summand_as_suspension_source_is_rejected():
  data = build_phase48_5_data()

  wrong_suspension = TodaSuspensionMap(
    source_group=data[
      "decomposition_map"
    ].source_group.summands[
      1
    ],
    target_group=data[
      "decomposition_map"
    ].target_group,
  )

  wrong_restriction = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=data[
        "decomposition_map"
      ],
      suspension_map=wrong_suspension,
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_restriction,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_suspension_injective_inference_rule(),
    steps,
  ) is None


def test_phase48_5_different_i_injectivity_statements_remain_distinct():
  first = build_phase48_5_data(
    i_name="i",
  )

  second = build_phase48_5_data(
    i_name="j",
  )

  assert (
    first[
      "injectivity"
    ]
    != second[
      "injectivity"
    ]
  )


def test_phase48_5_different_n_injectivity_statements_remain_distinct():
  first = build_phase48_5_data(
    n_name="n",
  )

  second = build_phase48_5_data(
    n_name="m",
  )

  assert (
    first[
      "injectivity"
    ]
    != second[
      "injectivity"
    ]
  )


def test_phase48_5_specific_injectivity_is_not_generic_injectivity():
  data = build_phase48_5_data()

  generic = InjectiveMapStatement(
    map=EHP_E_MAP,
  )

  assert (
    data[
      "injectivity"
    ]
    != generic
  )


def test_phase48_5_valid_run_does_not_derive_generic_e_injectivity():
  data = build_phase48_5_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_suspension_injective_inference_rule(),
      build_phase48_5_steps(
        data
      ),
    )
  )

  generic = InjectiveMapStatement(
    map=EHP_E_MAP,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert generic not in conclusions


def test_phase48_5_generic_isomorphism_to_injective_rule_rejects_prop44_theorem():
  data = build_phase48_5_data()

  theorem_step = ProofStep(
    conclusion=data[
      "isomorphism"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    isomorphism_implies_injective_inference_rule(),
    (
      theorem_step,
    ),
  ) is None


def test_phase48_5_specific_injectivity_has_no_generic_projection():
  data = build_phase48_5_data()

  statement = data[
    "injectivity"
  ]

  assert not hasattr(
    statement,
    "generic_injectivity",
  )

  assert not hasattr(
    statement,
    "generic_map",
  )

  assert not hasattr(
    statement,
    "injective_map_statement",
  )



