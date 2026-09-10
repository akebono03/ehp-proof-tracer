from dataclasses import replace
from functools import lru_cache

from homotopy_groups import (
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase68_pi_n_plus_4_n_zero import (
  build_phase68_10_data,
)
from toda_rules import (
  TodaDeltaSurjectiveStatement,
  TodaProp42ExactnessStatement,
  toda_eq510_concrete_delta_e_exactness_inference_rule,
  toda_eq510_delta_surjective_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase69_2_data():
  phase68_10 = (
    build_phase68_10_data()
  )

  pi10_6_zero_step = (
    phase68_10[
      "pi10_6_zero_step"
    ]
  )

  pi11_11 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=11,
  )

  pi9_5 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  pi10_6 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=6,
  )

  exactness_window = (
    TodaEHPExactnessWindow(
      source_term=pi11_11,
      middle_term=pi9_5,
      target_term=pi10_6,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    )
  )

  exactness_window_step = ProofStep(
    conclusion=exactness_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  exactness_rule = (
    toda_eq510_concrete_delta_e_exactness_inference_rule()
  )

  surjective_rule = (
    toda_eq510_delta_surjective_inference_rule()
  )

  rules = (
    exactness_rule,
    surjective_rule,
  )

  premise_steps = (
    pi10_6_zero_step,
    exactness_window_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  expected_exactness = (
    TodaProp42ExactnessStatement(
      window=exactness_window,
    )
  )

  exactness_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_exactness
    )
  )

  expected_surjective = (
    TodaDeltaSurjectiveStatement(
      map=TodaDeltaMap(
        source_group=pi11_11,
        target_group=pi9_5,
      ),
    )
  )

  surjective_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_surjective
    )
  )

  return {
    "phase68_10": phase68_10,
    "pi10_6_zero_step": (
      pi10_6_zero_step
    ),
    "pi11_11": pi11_11,
    "pi9_5": pi9_5,
    "pi10_6": pi10_6,
    "exactness_window": (
      exactness_window
    ),
    "exactness_window_step": (
      exactness_window_step
    ),
    "exactness_rule": (
      exactness_rule
    ),
    "surjective_rule": (
      surjective_rule
    ),
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "expected_exactness": (
      expected_exactness
    ),
    "exactness_step": (
      exactness_step
    ),
    "expected_surjective": (
      expected_surjective
    ),
    "surjective_step": (
      surjective_step
    ),
  }


def test_phase69_2_reuses_derived_pi10_6_zero():
  data = build_phase69_2_data()

  assert (
    data[
      "pi10_6_zero_step"
    ].conclusion
    == TodaPrimaryGroupZeroStatement(
      group=data[
        "pi10_6"
      ],
    )
  )

  assert (
    data[
      "pi10_6_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase69_2_structural_window_remains_given():
  data = build_phase69_2_data()

  assert (
    data[
      "exactness_window_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase69_2_window_is_expected_delta_e_segment():
  data = build_phase69_2_data()

  window = data[
    "exactness_window"
  ]

  assert (
    window.source_term
    == data[
      "pi11_11"
    ]
  )

  assert (
    window.middle_term
    == data[
      "pi9_5"
    ]
  )

  assert (
    window.target_term
    == data[
      "pi10_6"
    ]
  )

  assert (
    window.first_map
    == EHP_DELTA_MAP
  )

  assert (
    window.second_map
    == EHP_E_MAP
  )


def test_phase69_2_derives_concrete_exactness():
  data = build_phase69_2_data()

  assert (
    data[
      "exactness_step"
    ].conclusion
    == data[
      "expected_exactness"
    ]
  )

  assert (
    data[
      "exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase69_2_exactness_uses_only_structural_window():
  data = build_phase69_2_data()

  assert (
    data[
      "exactness_step"
    ].premises
    == (
      data[
        "exactness_window_step"
      ],
    )
  )


def test_phase69_2_derives_delta_surjective():
  data = build_phase69_2_data()

  assert (
    data[
      "surjective_step"
    ].conclusion
    == data[
      "expected_surjective"
    ]
  )

  assert (
    data[
      "surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase69_2_delta_surjective_map_is_expected():
  data = build_phase69_2_data()

  delta_map = (
    data[
      "surjective_step"
    ].conclusion.map
  )

  assert (
    delta_map.source_group
    == data[
      "pi11_11"
    ]
  )

  assert (
    delta_map.target_group
    == data[
      "pi9_5"
    ]
  )


def test_phase69_2_surjectivity_uses_exact_dependencies():
  data = build_phase69_2_data()

  assert (
    data[
      "surjective_step"
    ].premises
    == (
      data[
        "pi10_6_zero_step"
      ],
      data[
        "exactness_step"
      ],
    )
  )


def test_phase69_2_exactness_rejects_wrong_window():
  data = build_phase69_2_data()

  wrong_window = replace(
    data[
      "exactness_window"
    ],
    source_term=TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=11,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "exactness_rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase69_2_surjectivity_rejects_given_pi10_6_zero():
  data = build_phase69_2_data()

  given_zero = ProofStep(
    conclusion=(
      data[
        "pi10_6_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "surjective_rule"
    ],
    (
      given_zero,
      data[
        "exactness_step"
      ],
    ),
  ) is None


def test_phase69_2_surjectivity_rejects_given_exactness():
  data = build_phase69_2_data()

  given_exactness = ProofStep(
    conclusion=(
      data[
        "exactness_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "surjective_rule"
    ],
    (
      data[
        "pi10_6_zero_step"
      ],
      given_exactness,
    ),
  ) is None


def test_phase69_2_surjectivity_rejects_wrong_zero_group():
  data = build_phase69_2_data()

  wrong_zero = ProofStep(
    conclusion=(
      TodaPrimaryGroupZeroStatement(
        group=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=5,
        ),
      )
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "surjective_rule"
    ],
    (
      wrong_zero,
      data[
        "exactness_step"
      ],
    ),
  ) is None


def test_phase69_2_result_reaches_fixed_point():
  data = build_phase69_2_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


