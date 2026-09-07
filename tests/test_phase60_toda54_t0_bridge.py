from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  ScalarProduct,
  ScalarSum,
  TodaBracket,
)
from homotopy_groups import (
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase60_toda54_bracket_inclusion import (
  build_phase60_4_data,
)
from test_phase60_toda54_indeterminacy import (
  build_phase60_3_data,
)
from toda_rules import (
  Toda54BracketUpToSignStatement,
  TodaSuspensionSurjectiveStatement,
  toda_32_phase60_suspension_surjective_inference_rule,
  toda_54_t0_bridge_inference_rule,
  toda_54_t_ge_1_up_to_sign_inference_rule,
)


def build_phase60_5_data():
  phase60_3 = (
    build_phase60_3_data()
  )

  phase60_4 = (
    build_phase60_4_data()
  )

  indeterminacy_step = (
    phase60_3[
      "final_indeterminacy_step"
    ]
  )

  membership_step = (
    phase60_4[
      "inclusion_step"
    ]
  )

  n = phase60_4[
    "n"
  ]

  n_range = ScalarGreaterEqualStatement(
    left=n,
    right=3,
  )

  n_range_step = ProofStep(
    conclusion=n_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  up_to_sign_rule = (
    toda_54_t_ge_1_up_to_sign_inference_rule()
  )

  suspension_rule = (
    toda_32_phase60_suspension_surjective_inference_rule()
  )

  t0_rule = (
    toda_54_t0_bridge_inference_rule()
  )

  rules = (
    up_to_sign_rule,
    suspension_rule,
    t0_rule,
  )

  premise_steps = (
    indeterminacy_step,
    membership_step,
    n_range_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  positive_value = (
    membership_step
    .conclusion
    .element
  )

  indexed_bracket = (
    membership_step
    .conclusion
    .bracket
  )

  expected_indexed_statement = (
    Toda54BracketUpToSignStatement(
      bracket=indexed_bracket,
      positive_value=positive_value,
    )
  )

  unindexed_bracket = TodaBracket(
    first=indexed_bracket.first,
    second=indexed_bracket.second,
    third=indexed_bracket.third,
  )

  expected_t0_statement = (
    Toda54BracketUpToSignStatement(
      bracket=unindexed_bracket,
      positive_value=positive_value,
    )
  )

  expected_suspension = (
    TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=TodaPrimaryGroup(
          group_dimension=ScalarSum(
            left=n,
            right=2,
          ),
          sphere_dimension=n,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=ScalarSum(
            left=n,
            right=3,
          ),
          sphere_dimension=ScalarSum(
            left=n,
            right=1,
          ),
        ),
      ),
    )
  )

  indexed_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_indexed_statement
    )
  )

  suspension_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_suspension
    )
  )

  t0_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_t0_statement
    )
  )

  return {
    "phase60_3": phase60_3,
    "phase60_4": phase60_4,
    "indeterminacy_step": (
      indeterminacy_step
    ),
    "membership_step": membership_step,
    "n": n,
    "n_range": n_range,
    "n_range_step": n_range_step,
    "positive_value": positive_value,
    "indexed_bracket": indexed_bracket,
    "unindexed_bracket": (
      unindexed_bracket
    ),
    "expected_indexed_statement": (
      expected_indexed_statement
    ),
    "expected_suspension": (
      expected_suspension
    ),
    "expected_t0_statement": (
      expected_t0_statement
    ),
    "up_to_sign_rule": (
      up_to_sign_rule
    ),
    "suspension_rule": (
      suspension_rule
    ),
    "t0_rule": t0_rule,
    "premise_steps": premise_steps,
    "result": result,
    "indexed_step": indexed_step,
    "suspension_step": suspension_step,
    "t0_step": t0_step,
  }


def test_phase60_5_reuses_phase60_3_indeterminacy():
  data = build_phase60_5_data()

  assert (
    data[
      "indeterminacy_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_5_reuses_phase60_4_membership():
  data = build_phase60_5_data()

  assert (
    data[
      "membership_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_5_t_ge_1_rule_matches_derived_dependencies():
  data = build_phase60_5_data()

  assert find_inference_match(
    data[
      "up_to_sign_rule"
    ],
    (
      data[
        "indeterminacy_step"
      ],
      data[
        "membership_step"
      ],
    ),
  ) is not None


def test_phase60_5_derives_t_ge_1_up_to_sign_statement():
  data = build_phase60_5_data()

  step = data[
    "indexed_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_indexed_statement"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase60_5_t_ge_1_statement_preserves_symbolic_index():
  data = build_phase60_5_data()

  assert (
    data[
      "indexed_step"
    ].conclusion.bracket.index
    == data[
      "phase60_4"
    ][
      "t"
    ]
  )


def test_phase60_5_toda32_rule_matches_n_at_least_3():
  data = build_phase60_5_data()

  assert find_inference_match(
    data[
      "suspension_rule"
    ],
    (
      data[
        "n_range_step"
      ],
    ),
  ) is not None


def test_phase60_5_derives_toda32_suspension_surjective():
  data = build_phase60_5_data()

  step = data[
    "suspension_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_suspension"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase60_5_toda32_source_is_pi_n_plus_2_n():
  data = build_phase60_5_data()

  suspension_map = (
    data[
      "suspension_step"
    ].conclusion.map
  )

  assert (
    suspension_map.source_group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=2,
      ),
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase60_5_toda32_target_is_pi_n_plus_3_n_plus_1():
  data = build_phase60_5_data()

  suspension_map = (
    data[
      "suspension_step"
    ].conclusion.map
  )

  assert (
    suspension_map.target_group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=3,
      ),
      sphere_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=1,
      ),
    )
  )


def test_phase60_5_t0_rule_matches_indexed_statement_and_toda32():
  data = build_phase60_5_data()

  assert find_inference_match(
    data[
      "t0_rule"
    ],
    (
      data[
        "indexed_step"
      ],
      data[
        "suspension_step"
      ],
      data[
        "n_range_step"
      ],
    ),
  ) is not None


def test_phase60_5_derives_unindexed_t0_statement():
  data = build_phase60_5_data()

  step = data[
    "t0_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_t0_statement"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase60_5_t0_bracket_is_unindexed():
  data = build_phase60_5_data()

  assert (
    data[
      "t0_step"
    ].conclusion.bracket.index
    is None
  )


def test_phase60_5_t0_bracket_preserves_entries():
  data = build_phase60_5_data()

  indexed = data[
    "indexed_bracket"
  ]

  unindexed = (
    data[
      "t0_step"
    ].conclusion.bracket
  )

  assert unindexed.first == indexed.first
  assert unindexed.second == indexed.second
  assert unindexed.third == indexed.third


def test_phase60_5_t0_preserves_positive_value():
  data = build_phase60_5_data()

  value = (
    data[
      "t0_step"
    ].conclusion
    .positive_value
  )

  assert isinstance(
    value,
    IteratedSuspension,
  )

  assert (
    value
    == data[
      "positive_value"
    ]
  )


def test_phase60_5_positive_value_is_e_n_minus_3_nu_prime():
  data = build_phase60_5_data()

  value = data[
    "positive_value"
  ]

  assert (
    value.exponent
    == ScalarSum(
      left=data[
        "n"
      ],
      right=ScalarProduct(
        left=-1,
        right=3,
      ),
    )
  )


def test_phase60_5_t0_provenance_uses_t_ge_1_and_toda32():
  data = build_phase60_5_data()

  assert (
    data[
      "t0_step"
    ].premises
    == (
      data[
        "indexed_step"
      ],
      data[
        "suspension_step"
      ],
      data[
        "n_range_step"
      ],
    )
  )


def test_phase60_5_rejects_given_indexed_statement():
  data = build_phase60_5_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "indexed_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "t0_rule"
    ],
    (
      given_step,
      data[
        "suspension_step"
      ],
      data[
        "n_range_step"
      ],
    ),
  ) is None


def test_phase60_5_rejects_given_toda32_surjectivity():
  data = build_phase60_5_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "suspension_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "t0_rule"
    ],
    (
      data[
        "indexed_step"
      ],
      given_step,
      data[
        "n_range_step"
      ],
    ),
  ) is None


def test_phase60_5_rejects_n_at_least_2():
  data = build_phase60_5_data()

  wrong_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=2,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "suspension_rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase60_5_final_result_is_not_given():
  data = build_phase60_5_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_t0_statement"
    ]
    not in initial_conclusions
  )

  assert (
    data[
      "t0_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase60_5_reaches_fixed_point_in_two_rounds():
  data = build_phase60_5_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    result.round_count
    == 2
  )

  assert (
    data[
      "indexed_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "suspension_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "t0_step"
    ]
    in result.round_results[
      1
    ].new_steps
  )


