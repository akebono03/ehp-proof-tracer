from expression import (
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
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
from toda_rules import (
  toda_pi_i_minus_1_1_zero_inference_rule,
)


def build_phase56_2_data():
  i = ScalarSymbol(
    name="i",
  )

  lower_bound = (
    ScalarGreaterEqualStatement(
      left=i,
      right=3,
    )
  )

  expected_zero = (
    TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=-1,
        ),
        sphere_dimension=1,
      ),
    )
  )

  premise_step = ProofStep(
    conclusion=lower_bound,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_pi_i_minus_1_1_zero_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        premise_step,
      ),
    )
  )

  zero_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_zero
    )
  )

  return {
    "i": i,
    "lower_bound": lower_bound,
    "expected_zero": expected_zero,
    "premise_step": premise_step,
    "rule": rule,
    "result": result,
    "zero_steps": zero_steps,
  }


def test_phase56_2_pi_i_minus_1_1_zero_is_representable():
  data = build_phase56_2_data()

  assert (
    data[
      "expected_zero"
    ]
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=data[
            "i"
          ],
          right=-1,
        ),
        sphere_dimension=1,
      ),
    )
  )


def test_phase56_2_rule_matches_i_at_least_3():
  data = build_phase56_2_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "premise_step"
      ],
    ),
  ) is not None


def test_phase56_2_derives_pi_i_minus_1_1_zero():
  data = build_phase56_2_data()

  steps = data[
    "zero_steps"
  ]

  assert len(
    steps
  ) == 1

  assert (
    steps[
      0
    ].conclusion
    == data[
      "expected_zero"
    ]
  )


def test_phase56_2_zero_result_is_inference():
  data = build_phase56_2_data()

  step = data[
    "zero_steps"
  ][
    0
  ]

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.inference_rule is not None

  assert (
    step.inference_rule.name
    == (
      "Toda pi_(i-1)^1 "
      "zero for i at least 3"
    )
  )


def test_phase56_2_zero_result_preserves_lower_bound_premise():
  data = build_phase56_2_data()

  step = data[
    "zero_steps"
  ][
    0
  ]

  assert (
    step.premises
    == (
      data[
        "premise_step"
      ],
    )
  )


def test_phase56_2_reaches_fixed_point_in_one_round():
  data = build_phase56_2_data()

  result = data[
    "result"
  ]

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


def test_phase56_2_rejects_i_at_least_2():
  i = ScalarSymbol(
    name="i",
  )

  step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=i,
      right=2,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_pi_i_minus_1_1_zero_inference_rule(),
    (
      step,
    ),
  ) is None


def test_phase56_2_rejects_i_at_least_4():
  i = ScalarSymbol(
    name="i",
  )

  step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=i,
      right=4,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_pi_i_minus_1_1_zero_inference_rule(),
    (
      step,
    ),
  ) is None


def test_phase56_2_rejects_reversed_inequality():
  i = ScalarSymbol(
    name="i",
  )

  step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=3,
      right=i,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_pi_i_minus_1_1_zero_inference_rule(),
    (
      step,
    ),
  ) is None


def test_phase56_2_rejects_concrete_left_side():
  step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=5,
      right=3,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_pi_i_minus_1_1_zero_inference_rule(),
    (
      step,
    ),
  ) is None


