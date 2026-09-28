from proof import (
  InferenceTerminationReason,
  ProofRule,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase55_prop51_phase49_dependency import (
  build_phase55_3_dependency,
)
from test_phase55_prop51_phase52_phase54_dependency import (
  build_phase55_4_dependency,
)
from toda_rules import (
  TodaProp51FiniteDimensionalStatement,
  toda_prop51_finite_dimensional_integration_inference_rule,
)


def build_phase55_5_integration():
  phase49_dependency = (
    build_phase55_3_dependency()
  )

  phase52_phase54_dependency = (
    build_phase55_4_dependency()
  )

  pi3_2_group_step = (
    phase49_dependency[
      "pi3_2_group_step"
    ]
  )

  eta2_hopf_step = (
    phase49_dependency[
      "hopf_relation_step"
    ]
  )

  delta_iota5_step = (
    phase52_phase54_dependency[
      "delta_iota5_step"
    ]
  )

  higher_eta_group_step = (
    phase52_phase54_dependency[
      "higher_eta_group_step"
    ]
  )

  premise_steps = (
    pi3_2_group_step,
    eta2_hopf_step,
    delta_iota5_step,
    higher_eta_group_step,
  )

  expected_statement = (
    TodaProp51FiniteDimensionalStatement(
      pi3_2_group_relation=(
        pi3_2_group_step
        .conclusion
      ),
      eta2_hopf_relation=(
        eta2_hopf_step
        .conclusion
      ),
      delta_iota5_relation=(
        delta_iota5_step
        .conclusion
      ),
      higher_eta_group_relation=(
        higher_eta_group_step
        .conclusion
      ),
    )
  )

  rule = (
    toda_prop51_finite_dimensional_integration_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  integration_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase49_dependency": (
      phase49_dependency
    ),
    "phase52_phase54_dependency": (
      phase52_phase54_dependency
    ),
    "pi3_2_group_step": (
      pi3_2_group_step
    ),
    "eta2_hopf_step": (
      eta2_hopf_step
    ),
    "delta_iota5_step": (
      delta_iota5_step
    ),
    "higher_eta_group_step": (
      higher_eta_group_step
    ),
    "premise_steps": premise_steps,
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "result": result,
    "integration_steps": (
      integration_steps
    ),
  }


def test_phase55_5_rule_matches_four_derived_finite_dimensional_results():
  integration = (
    build_phase55_5_integration()
  )

  assert find_inference_match(
    integration[
      "rule"
    ],
    integration[
      "premise_steps"
    ],
  ) is not None


def test_phase55_5_derives_prop51_finite_dimensional_statement():
  integration = (
    build_phase55_5_integration()
  )

  steps = integration[
    "integration_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaProp51FiniteDimensionalStatement,
  )

  assert (
    steps[
      0
    ].conclusion
    == integration[
      "expected_statement"
    ]
  )


def test_phase55_5_statement_preserves_all_four_results():
  integration = (
    build_phase55_5_integration()
  )

  statement = (
    integration[
      "integration_steps"
    ][
      0
    ].conclusion
  )

  assert (
    statement.pi3_2_group_relation
    == integration[
      "pi3_2_group_step"
    ].conclusion
  )

  assert (
    statement.eta2_hopf_relation
    == integration[
      "eta2_hopf_step"
    ].conclusion
  )

  assert (
    statement.delta_iota5_relation
    == integration[
      "delta_iota5_step"
    ].conclusion
  )

  assert (
    statement.higher_eta_group_relation
    == integration[
      "higher_eta_group_step"
    ].conclusion
  )


def test_phase55_5_integration_result_is_inference():
  integration = (
    build_phase55_5_integration()
  )

  step = integration[
    "integration_steps"
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
      "Toda Proposition 5.1 "
      "finite-dimensional integration"
    )
  )


def test_phase55_5_integration_preserves_four_derived_premises():
  integration = (
    build_phase55_5_integration()
  )

  step = integration[
    "integration_steps"
  ][
    0
  ]

  assert len(
    step.premises
  ) == 4

  assert (
    step.premises
    == integration[
      "premise_steps"
    ]
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in step.premises
  )


def test_phase55_5_integration_reaches_fixed_point_in_one_round():
  integration = (
    build_phase55_5_integration()
  )

  result = integration[
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

  assert (
    integration[
      "integration_steps"
    ][
      0
    ]
    in result.round_results[
      0
    ].new_steps
  )


