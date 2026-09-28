from dataclasses import replace
from functools import lru_cache

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase68_pi7_3_nu_prime_eta6 import (
  build_phase68_3_data,
)
from test_phase68_pi8_4_decomposition import (
  build_phase68_4_data,
)
from test_phase68_pi9_5_nu5_eta8 import (
  build_phase68_6_data,
)
from test_phase68_pi_n_plus_4_n_zero import (
  build_phase68_10_data,
)
from toda_rules import (
  TodaProp58FiniteDimensionalStatement,
  toda_prop58_finite_dimensional_integration_inference_rule,
  toda_prop58_finite_dimensional_literature_statements,
)


@lru_cache(maxsize=1)
def build_phase68_11_data():
  phase68_3 = (
    build_phase68_3_data()
  )

  phase68_4 = (
    build_phase68_4_data()
  )

  phase68_6 = (
    build_phase68_6_data()
  )

  phase68_10 = (
    build_phase68_10_data()
  )

  pi6_2_step = (
    phase68_3[
      "pi6_2_step"
    ]
  )

  pi7_3_step = (
    phase68_3[
      "final_step"
    ]
  )

  pi8_4_step = (
    phase68_4[
      "final_step"
    ]
  )

  pi9_5_step = (
    phase68_6[
      "final_step"
    ]
  )

  higher_zero_step = (
    phase68_10[
      "final_step"
    ]
  )

  higher_range_step = (
    phase68_10[
      "n_ge_6_step"
    ]
  )

  expected_statement = (
    TodaProp58FiniteDimensionalStatement(
      pi6_2_group_relation=(
        pi6_2_step.conclusion
      ),
      pi7_3_group_relation=(
        pi7_3_step.conclusion
      ),
      pi8_4_group_relation=(
        pi8_4_step.conclusion
      ),
      pi9_5_group_relation=(
        pi9_5_step.conclusion
      ),
      higher_four_stem_zero=(
        higher_zero_step.conclusion
      ),
      higher_range=(
        higher_range_step.conclusion
      ),
      literature_statements=(
        toda_prop58_finite_dimensional_literature_statements()
      ),
    )
  )

  rule = (
    toda_prop58_finite_dimensional_integration_inference_rule()
  )

  premise_steps = (
    pi6_2_step,
    pi7_3_step,
    pi8_4_step,
    pi9_5_step,
    higher_zero_step,
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
    "phase68_3": phase68_3,
    "phase68_4": phase68_4,
    "phase68_6": phase68_6,
    "phase68_10": phase68_10,
    "pi6_2_step": pi6_2_step,
    "pi7_3_step": pi7_3_step,
    "pi8_4_step": pi8_4_step,
    "pi9_5_step": pi9_5_step,
    "higher_zero_step": (
      higher_zero_step
    ),
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


def test_phase68_11_reuses_five_derived_results():
  data = build_phase68_11_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in (
      data[
        "pi6_2_step"
      ],
      data[
        "pi7_3_step"
      ],
      data[
        "pi8_4_step"
      ],
      data[
        "pi9_5_step"
      ],
      data[
        "higher_zero_step"
      ],
    )
  )


def test_phase68_11_higher_range_remains_given():
  data = build_phase68_11_data()

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


def test_phase68_11_rule_matches_dependencies():
  data = build_phase68_11_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase68_11_derives_prop58_aggregate():
  data = build_phase68_11_data()

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


def test_phase68_11_aggregate_contains_pi6_2():
  data = build_phase68_11_data()

  assert (
    data[
      "integration_step"
    ].conclusion
    .pi6_2_group_relation
    is data[
      "pi6_2_step"
    ].conclusion
  )


def test_phase68_11_aggregate_contains_pi7_3():
  data = build_phase68_11_data()

  assert (
    data[
      "integration_step"
    ].conclusion
    .pi7_3_group_relation
    is data[
      "pi7_3_step"
    ].conclusion
  )


def test_phase68_11_aggregate_contains_pi8_4():
  data = build_phase68_11_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    statement.pi8_4_group_relation
    is data[
      "pi8_4_step"
    ].conclusion
  )

  group = (
    statement
    .pi8_4_group_relation
    .rhs
  )

  assert isinstance(
    group,
    DirectSumGroup,
  )

  assert len(
    group.summands
  ) == 2

  assert all(
    isinstance(
      summand,
      FiniteCyclicGroup,
    )
    and summand.order == 2
    for summand in group.summands
  )


def test_phase68_11_aggregate_contains_pi9_5():
  data = build_phase68_11_data()

  assert (
    data[
      "integration_step"
    ].conclusion
    .pi9_5_group_relation
    is data[
      "pi9_5_step"
    ].conclusion
  )


def test_phase68_11_aggregate_contains_higher_zero():
  data = build_phase68_11_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert isinstance(
    statement.higher_four_stem_zero,
    TodaPrimaryGroupZeroStatement,
  )

  assert (
    statement.higher_four_stem_zero
    is data[
      "higher_zero_step"
    ].conclusion
  )

  assert (
    statement.higher_range
    is data[
      "higher_range_step"
    ].conclusion
  )


def test_phase68_11_aggregate_has_prop58_literature():
  data = build_phase68_11_data()

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
    == "Toda Proposition 5.8"
  )

  assert (
    literature[
      0
    ].reference.locator
    == "Proposition 5.8"
  )


def test_phase68_11_literature_contains_five_branches():
  data = build_phase68_11_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
    .literature_statements[
      0
    ]
    .statement
  )

  assert "pi_6^2" in statement
  assert "pi_7^3" in statement
  assert "pi_8^4" in statement
  assert "pi_9^5" in statement
  assert "pi_(n+4)^n" in statement


def test_phase68_11_literature_does_not_add_stable_g4():
  data = build_phase68_11_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
    .literature_statements[
      0
    ]
    .statement
  )

  assert "(G_4;2)" not in statement


def test_phase68_11_provenance_uses_exactly_six_premises():
  data = build_phase68_11_data()

  assert (
    data[
      "integration_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )

  assert len(
    data[
      "integration_step"
    ].premises
  ) == 6


def test_phase68_11_rejects_given_pi6_2():
  data = build_phase68_11_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi6_2_step"
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
      given,
      data[
        "pi7_3_step"
      ],
      data[
        "pi8_4_step"
      ],
      data[
        "pi9_5_step"
      ],
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase68_11_rejects_given_pi7_3():
  data = build_phase68_11_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi7_3_step"
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
        "pi6_2_step"
      ],
      given,
      data[
        "pi8_4_step"
      ],
      data[
        "pi9_5_step"
      ],
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase68_11_rejects_given_pi8_4():
  data = build_phase68_11_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi8_4_step"
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
        "pi6_2_step"
      ],
      data[
        "pi7_3_step"
      ],
      given,
      data[
        "pi9_5_step"
      ],
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase68_11_rejects_given_pi9_5():
  data = build_phase68_11_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi9_5_step"
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
        "pi6_2_step"
      ],
      data[
        "pi7_3_step"
      ],
      data[
        "pi8_4_step"
      ],
      given,
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase68_11_rejects_given_higher_zero():
  data = build_phase68_11_data()

  given = ProofStep(
    conclusion=(
      data[
        "higher_zero_step"
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
        "pi6_2_step"
      ],
      data[
        "pi7_3_step"
      ],
      data[
        "pi8_4_step"
      ],
      data[
        "pi9_5_step"
      ],
      given,
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase68_11_rejects_wrong_range():
  data = build_phase68_11_data()

  wrong_range = replace(
    data[
      "higher_range_step"
    ].conclusion,
    right=5,
  )

  wrong_step = ProofStep(
    conclusion=wrong_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "pi6_2_step"
      ],
      data[
        "pi7_3_step"
      ],
      data[
        "pi8_4_step"
      ],
      data[
        "pi9_5_step"
      ],
      data[
        "higher_zero_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase68_11_aggregate_not_present_initially():
  data = build_phase68_11_data()

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


def test_phase68_11_reaches_fixed_point():
  data = build_phase68_11_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    data[
      "integration_step"
    ]
    in data[
      "result"
    ].round_results[
      0
    ].new_steps
  )



