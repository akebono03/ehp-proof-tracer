from dataclasses import replace
from functools import lru_cache

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
from test_phase56_toda52_composition_isomorphism import (
  build_phase56_5_data,
)
from test_phase73_prop511_finite_dimensional_integration import (
  build_phase73_8e_data,
)
from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  TodaProp511FiniteDimensionalStatement,
  toda_prop515_pi9_2_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_2_data():
  phase56_5 = (
    build_phase56_5_data()
  )

  phase73_8e = (
    build_phase73_8e_data()
  )

  toda52_step = (
    phase56_5[
      "composition_isomorphism_steps"
    ][
      0
    ]
  )

  prop511_step = (
    phase73_8e[
      "final_step"
    ]
  )

  rule = (
    toda_prop515_pi9_2_zero_inference_rule()
  )

  premise_steps = (
    prop511_step,
    toda52_step,
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
        group_dimension=9,
        sphere_dimension=2,
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
    "phase56_5": phase56_5,
    "phase73_8e": phase73_8e,
    "toda52_step": toda52_step,
    "prop511_step": prop511_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "expected_statement": (
      expected_statement
    ),
    "final_step": final_step,
  }


def test_phase75_2_reuses_derived_prop511():
  data = build_phase75_2_data()

  assert isinstance(
    data[
      "prop511_step"
    ].conclusion,
    TodaProp511FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop511_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_2_prop511_contains_pi9_3_zero():
  data = build_phase75_2_data()

  assert (
    data[
      "prop511_step"
    ].conclusion
    .pi9_3_zero
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=3,
      ),
    )
  )


def test_phase75_2_reuses_derived_toda52_isomorphism():
  data = build_phase75_2_data()

  assert isinstance(
    data[
      "toda52_step"
    ].conclusion,
    Toda52CompositionIsomorphismStatement,
  )

  assert (
    data[
      "toda52_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_2_toda52_is_pi_i3_to_pi_i2():
  data = build_phase75_2_data()

  statement = (
    data[
      "toda52_step"
    ].conclusion
  )

  assert (
    statement
    .source_group
    .sphere_dimension
    == 3
  )

  assert (
    statement
    .target_group
    .sphere_dimension
    == 2
  )

  assert (
    statement
    .source_group
    .group_dimension
    == statement
    .target_group
    .group_dimension
  )


def test_phase75_2_derives_pi9_2_zero():
  data = build_phase75_2_data()

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


def test_phase75_2_final_group_is_pi9_2():
  data = build_phase75_2_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .group
    == TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=2,
    )
  )


def test_phase75_2_final_uses_exact_two_premises():
  data = build_phase75_2_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "prop511_step"
      ],
      data[
        "toda52_step"
      ],
    )
  )


def test_phase75_2_final_statement_not_present_initially():
  data = build_phase75_2_data()

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


def test_phase75_2_rejects_given_prop511():
  data = build_phase75_2_data()

  given = ProofStep(
    conclusion=(
      data[
        "prop511_step"
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
        "toda52_step"
      ],
    ),
  ) is None


def test_phase75_2_rejects_given_toda52():
  data = build_phase75_2_data()

  given = ProofStep(
    conclusion=(
      data[
        "toda52_step"
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
        "prop511_step"
      ],
      given,
    ),
  ) is None


def test_phase75_2_rejects_wrong_prop511_pi9_3_group():
  data = build_phase75_2_data()

  prop511 = (
    data[
      "prop511_step"
    ].conclusion
  )

  wrong_prop511 = replace(
    prop511,
    pi9_3_zero=(
      TodaPrimaryGroupZeroStatement(
        group=TodaPrimaryGroup(
          group_dimension=8,
          sphere_dimension=3,
        ),
      )
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_prop511,
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
        "toda52_step"
      ],
    ),
  ) is None


def test_phase75_2_rejects_wrong_toda52_target():
  data = build_phase75_2_data()

  isomorphism = (
    data[
      "toda52_step"
    ].conclusion
  )

  wrong_isomorphism = replace(
    isomorphism,
    target_group=TodaPrimaryGroup(
      group_dimension=(
        isomorphism
        .target_group
        .group_dimension
      ),
      sphere_dimension=4,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_isomorphism,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "prop511_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase75_2_reaches_fixed_point():
  data = build_phase75_2_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


