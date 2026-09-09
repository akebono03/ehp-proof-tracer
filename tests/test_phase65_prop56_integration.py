from functools import lru_cache

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase65_nu5_order_pi8_5 import (
  build_phase65_7_data,
)
from test_phase65_nu5_stable_transport import (
  build_phase65_8_data,
)
from test_phase65_nu_prime_order_pi6_3 import (
  build_phase65_4_data,
)
from test_phase65_pi5_2_eta2_cube import (
  build_phase65_2_data,
)
from test_phase65_pi7_4_decomposition import (
  build_phase65_5_data,
)
from toda_rules import (
  TodaProp56FiniteDimensionalStatement,
  toda_prop56_finite_dimensional_integration_inference_rule,
  toda_prop56_finite_dimensional_literature_statements,
)


@lru_cache(maxsize=1)
def build_phase65_9_data():
  phase65_2 = (
    build_phase65_2_data()
  )

  phase65_4 = (
    build_phase65_4_data()
  )

  phase65_5 = (
    build_phase65_5_data()
  )

  phase65_7 = (
    build_phase65_7_data()
  )

  phase65_8 = (
    build_phase65_8_data()
  )

  pi5_2_step = (
    phase65_2[
      "final_step"
    ]
  )

  pi6_3_step = (
    phase65_4[
      "pi6_3_step"
    ]
  )

  pi7_4_step = (
    phase65_5[
      "final_step"
    ]
  )

  pi8_5_step = (
    phase65_7[
      "pi8_5_step"
    ]
  )

  higher_step = (
    phase65_8[
      "final_step"
    ]
  )

  higher_range_step = (
    phase65_8[
      "higher_range_step"
    ]
  )

  expected_statement = (
    TodaProp56FiniteDimensionalStatement(
      pi5_2_group_relation=(
        pi5_2_step.conclusion
      ),
      pi6_3_group_relation=(
        pi6_3_step.conclusion
      ),
      pi7_4_group_relation=(
        pi7_4_step.conclusion
      ),
      pi8_5_group_relation=(
        pi8_5_step.conclusion
      ),
      higher_nu_group_relation=(
        higher_step.conclusion
      ),
      higher_range=(
        higher_range_step.conclusion
      ),
      literature_statements=(
        toda_prop56_finite_dimensional_literature_statements()
      ),
    )
  )

  rule = (
    toda_prop56_finite_dimensional_integration_inference_rule()
  )

  premise_steps = (
    pi5_2_step,
    pi6_3_step,
    pi7_4_step,
    pi8_5_step,
    higher_step,
    higher_range_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  integration_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase65_2": phase65_2,
    "phase65_4": phase65_4,
    "phase65_5": phase65_5,
    "phase65_7": phase65_7,
    "phase65_8": phase65_8,
    "pi5_2_step": pi5_2_step,
    "pi6_3_step": pi6_3_step,
    "pi7_4_step": pi7_4_step,
    "pi8_5_step": pi8_5_step,
    "higher_step": higher_step,
    "higher_range_step": (
      higher_range_step
    ),
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "integration_step": (
      integration_step
    ),
  }


def test_phase65_9_reuses_pi5_2_result():
  data = build_phase65_9_data()

  assert (
    data[
      "pi5_2_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi5_2_step"
    ].conclusion.rhs.order
    == 2
  )


def test_phase65_9_reuses_pi6_3_result():
  data = build_phase65_9_data()

  assert (
    data[
      "pi6_3_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi6_3_step"
    ].conclusion.rhs.order
    == 4
  )


def test_phase65_9_reuses_pi7_4_result():
  data = build_phase65_9_data()

  assert (
    data[
      "pi7_4_step"
    ].rule
    == ProofRule.INFERENCE
  )

  group = (
    data[
      "pi7_4_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    DirectSumGroup,
  )

  assert isinstance(
    group.summands[
      0
    ],
    FreeCyclicGroup,
  )

  assert isinstance(
    group.summands[
      1
    ],
    FiniteCyclicGroup,
  )


def test_phase65_9_reuses_pi8_5_result():
  data = build_phase65_9_data()

  assert (
    data[
      "pi8_5_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi8_5_step"
    ].conclusion.rhs.order
    == 8
  )


def test_phase65_9_reuses_higher_nu_result():
  data = build_phase65_9_data()

  assert (
    data[
      "higher_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "higher_step"
    ].conclusion.rhs.order
    == 8
  )


def test_phase65_9_higher_scope_is_n_at_least_six():
  data = build_phase65_9_data()

  assert (
    data[
      "higher_range_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "higher_range_step"
    ].conclusion.right
    == 6
  )


def test_phase65_9_rule_matches_all_dependencies():
  data = build_phase65_9_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase65_9_derives_prop56_aggregate():
  data = build_phase65_9_data()

  assert (
    data[
      "integration_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "integration_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_9_aggregate_contains_pi5_2():
  data = build_phase65_9_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    statement.pi5_2_group_relation
    == data[
      "pi5_2_step"
    ].conclusion
  )


def test_phase65_9_aggregate_contains_pi6_3():
  data = build_phase65_9_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    statement.pi6_3_group_relation
    == data[
      "pi6_3_step"
    ].conclusion
  )


def test_phase65_9_aggregate_contains_pi7_4():
  data = build_phase65_9_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    statement.pi7_4_group_relation
    == data[
      "pi7_4_step"
    ].conclusion
  )


def test_phase65_9_aggregate_contains_pi8_5():
  data = build_phase65_9_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    statement.pi8_5_group_relation
    == data[
      "pi8_5_step"
    ].conclusion
  )


def test_phase65_9_aggregate_contains_higher_branch():
  data = build_phase65_9_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    statement.higher_nu_group_relation
    == data[
      "higher_step"
    ].conclusion
  )

  assert (
    statement.higher_range
    == data[
      "higher_range_step"
    ].conclusion
  )


def test_phase65_9_aggregate_has_prop56_literature():
  data = build_phase65_9_data()

  literature = (
    data[
      "integration_step"
    ].conclusion
    .literature_statements
  )

  assert len(
    literature
  ) == 1

  assert (
    literature[
      0
    ].reference.label
    == "Toda Proposition 5.6"
  )

  assert (
    literature[
      0
    ].reference.locator
    == "Proposition 5.6"
  )


def test_phase65_9_provenance_uses_exactly_six_premises():
  data = build_phase65_9_data()

  assert (
    data[
      "integration_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )

  assert (
    len(
      data[
        "integration_step"
      ].premises
    )
    == 6
  )


def test_phase65_9_theorem_dependencies_are_derived():
  data = build_phase65_9_data()

  theorem_steps = (
    data[
      "pi5_2_step"
    ],
    data[
      "pi6_3_step"
    ],
    data[
      "pi7_4_step"
    ],
    data[
      "pi8_5_step"
    ],
    data[
      "higher_step"
    ],
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in theorem_steps
  )


def test_phase65_9_only_scope_remains_given():
  data = build_phase65_9_data()

  assert (
    data[
      "higher_range_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in (
      data[
        "pi5_2_step"
      ],
      data[
        "pi6_3_step"
      ],
      data[
        "pi7_4_step"
      ],
      data[
        "pi8_5_step"
      ],
      data[
        "higher_step"
      ],
    )
  )


def test_phase65_9_rejects_given_pi8_5_result():
  data = build_phase65_9_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "pi8_5_step"
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
      data[
        "pi5_2_step"
      ],
      data[
        "pi6_3_step"
      ],
      data[
        "pi7_4_step"
      ],
      given_step,
      data[
        "higher_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase65_9_rejects_given_higher_result():
  data = build_phase65_9_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "higher_step"
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
      data[
        "pi5_2_step"
      ],
      data[
        "pi6_3_step"
      ],
      data[
        "pi7_4_step"
      ],
      data[
        "pi8_5_step"
      ],
      given_step,
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase65_9_final_result_is_not_given():
  data = build_phase65_9_data()

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "expected_statement"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase65_9_reaches_fixed_point_in_one_round():
  data = build_phase65_9_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert (
    data[
      "integration_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )


