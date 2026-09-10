from dataclasses import replace
from functools import lru_cache

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofRule,
  ProofStep,
  apply_inference_match,
  find_inference_match,
)
from test_phase70_pi_n_plus_5_n_zero import (
  build_phase70_9_data,
)
from toda_rules import (
  TodaProp59FiniteDimensionalStatement,
  toda_prop59_finite_dimensional_integration_inference_rule,
  toda_prop59_finite_dimensional_literature_statements,
)


@lru_cache(maxsize=1)
def build_phase70_10_data():
  phase70_9 = (
    build_phase70_9_data()
  )

  phase70_8 = (
    phase70_9[
      "phase70_8"
    ]
  )

  phase70_7 = (
    phase70_8[
      "phase70_7"
    ]
  )

  phase70_6 = (
    phase70_7[
      "phase70_6"
    ]
  )

  phase70_5 = (
    phase70_6[
      "phase70_5"
    ]
  )

  phase70_4 = (
    phase70_5[
      "phase70_4"
    ]
  )

  phase70_3 = (
    phase70_4[
      "phase70_3"
    ]
  )

  phase70_2 = (
    phase70_3[
      "phase70_2"
    ]
  )

  pi7_2_step = (
    phase70_2[
      "final_step"
    ]
  )

  pi8_3_step = (
    phase70_3[
      "final_step"
    ]
  )

  pi9_4_step = (
    phase70_4[
      "final_step"
    ]
  )

  pi10_5_step = (
    phase70_6[
      "final_step"
    ]
  )

  pi11_6_step = (
    phase70_8[
      "final_step"
    ]
  )

  higher_zero_step = (
    phase70_9[
      "higher_zero_step"
    ]
  )

  higher_range_step = (
    phase70_9[
      "n_ge_7_step"
    ]
  )

  expected_statement = (
    TodaProp59FiniteDimensionalStatement(
      pi7_2_group_relation=(
        pi7_2_step.conclusion
      ),
      pi8_3_group_relation=(
        pi8_3_step.conclusion
      ),
      pi9_4_group_relation=(
        pi9_4_step.conclusion
      ),
      pi10_5_group_relation=(
        pi10_5_step.conclusion
      ),
      pi11_6_group_relation=(
        pi11_6_step.conclusion
      ),
      higher_five_stem_zero=(
        higher_zero_step.conclusion
      ),
      higher_range=(
        higher_range_step.conclusion
      ),
      literature_statements=(
        toda_prop59_finite_dimensional_literature_statements()
      ),
    )
  )

  rule = (
    toda_prop59_finite_dimensional_integration_inference_rule()
  )

  premise_steps = (
    pi7_2_step,
    pi8_3_step,
    pi9_4_step,
    pi10_5_step,
    pi11_6_step,
    higher_zero_step,
    higher_range_step,
  )

  match = find_inference_match(
    rule,
    premise_steps,
  )

  assert match is not None

  integration_step = (
    apply_inference_match(
      match
    )
  )

  assert (
    integration_step.conclusion
    == expected_statement
  )

  return {
    "phase70_9": phase70_9,
    "phase70_8": phase70_8,
    "phase70_7": phase70_7,
    "phase70_6": phase70_6,
    "phase70_5": phase70_5,
    "phase70_4": phase70_4,
    "phase70_3": phase70_3,
    "phase70_2": phase70_2,
    "pi7_2_step": pi7_2_step,
    "pi8_3_step": pi8_3_step,
    "pi9_4_step": pi9_4_step,
    "pi10_5_step": pi10_5_step,
    "pi11_6_step": pi11_6_step,
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
    "match": match,
    "integration_step": (
      integration_step
    ),
  }


def test_phase70_10_reuses_six_derived_results():
  data = build_phase70_10_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in (
      data[
        "pi7_2_step"
      ],
      data[
        "pi8_3_step"
      ],
      data[
        "pi9_4_step"
      ],
      data[
        "pi10_5_step"
      ],
      data[
        "pi11_6_step"
      ],
      data[
        "higher_zero_step"
      ],
    )
  )


def test_phase70_10_higher_range_remains_given():
  data = build_phase70_10_data()

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
    == 7
  )


def test_phase70_10_rule_matches_dependencies():
  data = build_phase70_10_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase70_10_derives_prop59_aggregate():
  data = build_phase70_10_data()

  assert isinstance(
    data[
      "integration_step"
    ].conclusion,
    TodaProp59FiniteDimensionalStatement,
  )

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


def test_phase70_10_contains_pi7_2():
  data = build_phase70_10_data()

  assert (
    data[
      "integration_step"
    ].conclusion
    .pi7_2_group_relation
    is data[
      "pi7_2_step"
    ].conclusion
  )


def test_phase70_10_contains_pi8_3():
  data = build_phase70_10_data()

  assert (
    data[
      "integration_step"
    ].conclusion
    .pi8_3_group_relation
    is data[
      "pi8_3_step"
    ].conclusion
  )


def test_phase70_10_contains_pi9_4():
  data = build_phase70_10_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    statement.pi9_4_group_relation
    is data[
      "pi9_4_step"
    ].conclusion
  )

  group = (
    statement
    .pi9_4_group_relation
    .rhs
  )

  assert isinstance(
    group,
    DirectSumGroup,
  )

  assert (
    len(
      group.summands
    )
    == 2
  )

  assert all(
    isinstance(
      summand,
      FiniteCyclicGroup,
    )
    and summand.order == 2
    for summand
    in group.summands
  )


def test_phase70_10_contains_pi10_5():
  data = build_phase70_10_data()

  relation = (
    data[
      "integration_step"
    ].conclusion
    .pi10_5_group_relation
  )

  assert (
    relation
    is data[
      "pi10_5_step"
    ].conclusion
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 2
  )


def test_phase70_10_contains_pi11_6():
  data = build_phase70_10_data()

  relation = (
    data[
      "integration_step"
    ].conclusion
    .pi11_6_group_relation
  )

  assert (
    relation
    is data[
      "pi11_6_step"
    ].conclusion
  )

  assert isinstance(
    relation.rhs,
    FreeCyclicGroup,
  )


def test_phase70_10_contains_higher_zero():
  data = build_phase70_10_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert isinstance(
    statement.higher_five_stem_zero,
    TodaPrimaryGroupZeroStatement,
  )

  assert (
    statement.higher_five_stem_zero
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


def test_phase70_10_has_prop59_literature():
  data = build_phase70_10_data()

  literature = (
    data[
      "integration_step"
    ].conclusion
    .literature_statements
  )

  assert (
    len(
      literature
    )
    == 1
  )

  assert (
    literature[
      0
    ].reference.label
    == "Toda Proposition 5.9"
  )

  assert (
    literature[
      0
    ].reference.locator
    == "Proposition 5.9"
  )


def test_phase70_10_literature_contains_six_branches():
  data = build_phase70_10_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
    .literature_statements[
      0
    ]
    .statement
  )

  assert "pi_7^2" in statement
  assert "pi_8^3" in statement
  assert "pi_9^4" in statement
  assert "pi_10^5" in statement
  assert "pi_11^6" in statement
  assert "pi_(n+5)^n" in statement


def test_phase70_10_literature_does_not_add_stable_g5():
  data = build_phase70_10_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
    .literature_statements[
      0
    ]
    .statement
  )

  assert "(G_5;2)" not in statement


def test_phase70_10_provenance_uses_exactly_seven_premises():
  data = build_phase70_10_data()

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
    == 7
  )


def test_phase70_10_rejects_given_pi7_2():
  data = build_phase70_10_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi7_2_step"
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
        "pi8_3_step"
      ],
      data[
        "pi9_4_step"
      ],
      data[
        "pi10_5_step"
      ],
      data[
        "pi11_6_step"
      ],
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase70_10_rejects_given_pi8_3():
  data = build_phase70_10_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi8_3_step"
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
        "pi7_2_step"
      ],
      given,
      data[
        "pi9_4_step"
      ],
      data[
        "pi10_5_step"
      ],
      data[
        "pi11_6_step"
      ],
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase70_10_rejects_given_pi9_4():
  data = build_phase70_10_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi9_4_step"
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
        "pi7_2_step"
      ],
      data[
        "pi8_3_step"
      ],
      given,
      data[
        "pi10_5_step"
      ],
      data[
        "pi11_6_step"
      ],
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase70_10_rejects_given_pi10_5():
  data = build_phase70_10_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi10_5_step"
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
        "pi7_2_step"
      ],
      data[
        "pi8_3_step"
      ],
      data[
        "pi9_4_step"
      ],
      given,
      data[
        "pi11_6_step"
      ],
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase70_10_rejects_given_pi11_6():
  data = build_phase70_10_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi11_6_step"
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
        "pi7_2_step"
      ],
      data[
        "pi8_3_step"
      ],
      data[
        "pi9_4_step"
      ],
      data[
        "pi10_5_step"
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


def test_phase70_10_rejects_given_higher_zero():
  data = build_phase70_10_data()

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
        "pi7_2_step"
      ],
      data[
        "pi8_3_step"
      ],
      data[
        "pi9_4_step"
      ],
      data[
        "pi10_5_step"
      ],
      data[
        "pi11_6_step"
      ],
      given,
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase70_10_rejects_inference_higher_range():
  data = build_phase70_10_data()

  derived = ProofStep(
    conclusion=(
      data[
        "higher_range_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "pi7_2_step"
      ],
      data[
        "pi8_3_step"
      ],
      data[
        "pi9_4_step"
      ],
      data[
        "pi10_5_step"
      ],
      data[
        "pi11_6_step"
      ],
      data[
        "higher_zero_step"
      ],
      derived,
    ),
  ) is None


def test_phase70_10_rejects_wrong_range():
  data = build_phase70_10_data()

  wrong_range = replace(
    data[
      "higher_range_step"
    ].conclusion,
    right=8,
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
        "pi7_2_step"
      ],
      data[
        "pi8_3_step"
      ],
      data[
        "pi9_4_step"
      ],
      data[
        "pi10_5_step"
      ],
      data[
        "pi11_6_step"
      ],
      data[
        "higher_zero_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase70_10_aggregate_not_present_initially():
  data = build_phase70_10_data()

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


def test_phase70_10_uses_one_shot_inference():
  data = build_phase70_10_data()

  assert (
    data[
      "match"
    ]
    is not None
  )

  assert (
    data[
      "integration_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "integration_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )


