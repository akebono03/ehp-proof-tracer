from dataclasses import replace
from functools import lru_cache

from expression import (
  ScalarSum,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
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
from test_phase63_toda56_semantics import (
  build_phase63_4_data,
)
from test_phase68_prop58_integration import (
  build_phase68_11_data,
)
from test_phase75_pi10_3_zero import (
  build_phase75_3_data,
)
from toda_rules import (
  Toda56Nu4DecompositionIsomorphismStatement,
  TodaProp58FiniteDimensionalStatement,
  toda_prop515_pi11_4_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_4_data():
  phase75_3 = (
    build_phase75_3_data()
  )

  phase68_11 = (
    build_phase68_11_data()
  )

  phase63_4 = (
    build_phase63_4_data()
  )

  pi10_3_zero_step = (
    phase75_3[
      "final_step"
    ]
  )

  prop58_step = (
    phase68_11[
      "integration_step"
    ]
  )

  toda56_step = (
    phase63_4[
      "toda56_step"
    ]
  )

  rule = (
    toda_prop515_pi11_4_zero_inference_rule()
  )

  premise_steps = (
    pi10_3_zero_step,
    prop58_step,
    toda56_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      premise_steps,
    )
  )

  expected_statement = (
    TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=4,
      ),
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase75_3": phase75_3,
    "phase68_11": phase68_11,
    "phase63_4": phase63_4,
    "pi10_3_zero_step": (
      pi10_3_zero_step
    ),
    "prop58_step": prop58_step,
    "toda56_step": toda56_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "expected_statement": (
      expected_statement
    ),
    "final_step": final_step,
  }


def test_phase75_4_reuses_pi10_3_zero():
  data = build_phase75_4_data()

  assert (
    data[
      "pi10_3_zero_step"
    ].conclusion
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=3,
      ),
    )
  )

  assert (
    data[
      "pi10_3_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_4_reuses_derived_prop58():
  data = build_phase75_4_data()

  assert isinstance(
    data[
      "prop58_step"
    ].conclusion,
    TodaProp58FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop58_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_4_prop58_contains_higher_four_stem_zero():
  data = build_phase75_4_data()

  statement = (
    data[
      "prop58_step"
    ].conclusion
  )

  assert isinstance(
    statement.higher_four_stem_zero,
    TodaPrimaryGroupZeroStatement,
  )

  n = (
    statement
    .higher_four_stem_zero
    .group
    .sphere_dimension
  )

  assert (
    statement
    .higher_four_stem_zero
    .group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=4,
      ),
      sphere_dimension=n,
    )
  )

  assert (
    statement.higher_range
    == ScalarGreaterEqualStatement(
      left=n,
      right=6,
    )
  )


def test_phase75_4_prop58_covers_pi11_7():
  data = build_phase75_4_data()

  statement = (
    data[
      "prop58_step"
    ].conclusion
  )

  assert (
    statement
    .higher_range
    .right
    <= 7
  )

  assert (
    7 + 4
    == 11
  )


def test_phase75_4_reuses_derived_toda56():
  data = build_phase75_4_data()

  assert isinstance(
    data[
      "toda56_step"
    ].conclusion,
    Toda56Nu4DecompositionIsomorphismStatement,
  )

  assert (
    data[
      "toda56_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_4_toda56_has_expected_source():
  data = build_phase75_4_data()

  decomposition_map = (
    data[
      "toda56_step"
    ].conclusion
    .prop44_isomorphism
    .map
  )

  i = (
    decomposition_map
    .target_group
    .group_dimension
  )

  assert (
    decomposition_map.source_group
    == DirectSumGroup(
      summands=(
        TodaPrimaryGroup(
          group_dimension=ScalarSum(
            left=i,
            right=-1,
          ),
          sphere_dimension=3,
        ),
        TodaPrimaryGroup(
          group_dimension=i,
          sphere_dimension=7,
        ),
      ),
    )
  )


def test_phase75_4_toda56_has_expected_target():
  data = build_phase75_4_data()

  decomposition_map = (
    data[
      "toda56_step"
    ].conclusion
    .prop44_isomorphism
    .map
  )

  i = (
    decomposition_map
    .target_group
    .group_dimension
  )

  assert (
    decomposition_map.target_group
    == TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=4,
    )
  )


def test_phase75_4_derives_pi11_4_zero():
  data = build_phase75_4_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_4_final_group_is_pi11_4():
  data = build_phase75_4_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .group
    == TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=4,
    )
  )


def test_phase75_4_final_uses_exact_three_premises():
  data = build_phase75_4_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi10_3_zero_step"
      ],
      data[
        "prop58_step"
      ],
      data[
        "toda56_step"
      ],
    )
  )


def test_phase75_4_final_statement_not_present_initially():
  data = build_phase75_4_data()

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


def test_phase75_4_rejects_given_pi10_3_zero():
  data = build_phase75_4_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi10_3_zero_step"
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
        "prop58_step"
      ],
      data[
        "toda56_step"
      ],
    ),
  ) is None


def test_phase75_4_rejects_given_prop58():
  data = build_phase75_4_data()

  given = ProofStep(
    conclusion=(
      data[
        "prop58_step"
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
        "pi10_3_zero_step"
      ],
      given,
      data[
        "toda56_step"
      ],
    ),
  ) is None


def test_phase75_4_rejects_given_toda56():
  data = build_phase75_4_data()

  given = ProofStep(
    conclusion=(
      data[
        "toda56_step"
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
        "pi10_3_zero_step"
      ],
      data[
        "prop58_step"
      ],
      given,
    ),
  ) is None


def test_phase75_4_rejects_wrong_pi10_3_zero():
  data = build_phase75_4_data()

  wrong_step = ProofStep(
    conclusion=TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=3,
      ),
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "prop58_step"
      ],
      data[
        "toda56_step"
      ],
    ),
  ) is None


def test_phase75_4_rejects_wrong_prop58_range():
  data = build_phase75_4_data()

  prop58 = (
    data[
      "prop58_step"
    ].conclusion
  )

  wrong_prop58 = replace(
    prop58,
    higher_range=replace(
      prop58.higher_range,
      right=8,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_prop58,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "pi10_3_zero_step"
      ],
      wrong_step,
      data[
        "toda56_step"
      ],
    ),
  ) is None


def test_phase75_4_rejects_wrong_prop58_higher_group():
  data = build_phase75_4_data()

  prop58 = (
    data[
      "prop58_step"
    ].conclusion
  )

  higher_zero = (
    prop58.higher_four_stem_zero
  )

  higher_group = (
    higher_zero.group
  )

  n = (
    higher_group
    .sphere_dimension
  )

  wrong_prop58 = replace(
    prop58,
    higher_four_stem_zero=(
      TodaPrimaryGroupZeroStatement(
        group=TodaPrimaryGroup(
          group_dimension=ScalarSum(
            left=n,
            right=5,
          ),
          sphere_dimension=n,
        ),
      )
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_prop58,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "pi10_3_zero_step"
      ],
      wrong_step,
      data[
        "toda56_step"
      ],
    ),
  ) is None


def test_phase75_4_rejects_wrong_toda56_target():
  data = build_phase75_4_data()

  toda56 = (
    data[
      "toda56_step"
    ].conclusion
  )

  prop44 = (
    toda56.prop44_isomorphism
  )

  decomposition_map = (
    prop44.map
  )

  wrong_map = replace(
    decomposition_map,
    target_group=TodaPrimaryGroup(
      group_dimension=(
        decomposition_map
        .target_group
        .group_dimension
      ),
      sphere_dimension=5,
    ),
  )

  wrong_toda56 = replace(
    toda56,
    prop44_isomorphism=replace(
      prop44,
      map=wrong_map,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_toda56,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "pi10_3_zero_step"
      ],
      data[
        "prop58_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase75_4_reaches_fixed_point():
  data = build_phase75_4_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


