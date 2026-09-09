from functools import lru_cache

from expression import (
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from map_facts import (
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from probes.probe_phase46_capabilities import (
  build_phase46_representative_result,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase68_nu_n_eta_n_plus_three_zero import (
  build_phase68_9_data,
)
from test_phase68_pi9_5_nu5_eta8 import (
  build_phase68_6_data,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionSurjectiveStatement,
  toda_prop58_higher_four_stem_zero_transport_inference_rule,
  toda_prop58_pi10_6_concrete_exactness_inference_rule,
  toda_prop58_pi10_6_suspension_surjective_inference_rule,
  toda_prop58_pi10_6_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase68_10_data():
  phase68_6 = (
    build_phase68_6_data()
  )

  phase68_9 = (
    build_phase68_9_data()
  )

  pi9_5_step = (
    phase68_6[
      "final_step"
    ]
  )

  nu6_eta9_zero_step = (
    phase68_9[
      "nu6_eta9_zero_step"
    ]
  )

  pi9_5 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  pi10_6 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=6,
  )

  pi10_11 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=11,
  )

  exactness_window = (
    TodaEHPExactnessWindow(
      source_term=pi9_5,
      middle_term=pi10_6,
      target_term=pi10_11,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    )
  )

  exactness_window_step = ProofStep(
    conclusion=exactness_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi10_11_zero_step = ProofStep(
    conclusion=(
      TodaPrimaryGroupZeroStatement(
        group=pi10_11,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  n = ScalarSymbol(
    name="n",
  )

  phase46 = (
    build_phase46_representative_result(
      n=6,
      k=4,
      m=n,
    )
  )

  stable_isomorphism_step = (
    phase46[
      "theorem_steps"
    ][
      0
    ]
  )

  n_ge_6_step = ProofStep(
    conclusion=(
      ScalarGreaterEqualStatement(
        left=n,
        right=6,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  exactness_rule = (
    toda_prop58_pi10_6_concrete_exactness_inference_rule()
  )

  surjective_rule = (
    toda_prop58_pi10_6_suspension_surjective_inference_rule()
  )

  pi10_6_zero_rule = (
    toda_prop58_pi10_6_zero_inference_rule()
  )

  higher_zero_rule = (
    toda_prop58_higher_four_stem_zero_transport_inference_rule()
  )

  rules = (
    exactness_rule,
    surjective_rule,
    pi10_6_zero_rule,
    higher_zero_rule,
  )

  premise_steps = (
    pi9_5_step,
    nu6_eta9_zero_step,
    exactness_window_step,
    pi10_11_zero_step,
    stable_isomorphism_step,
    n_ge_6_step,
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

  surjective_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaSuspensionSurjectiveStatement,
    )
    and (
      step.conclusion
      .map
      .source_group
      == pi9_5
    )
    and (
      step.conclusion
      .map
      .target_group
      == pi10_6
    )
  )

  expected_pi10_6_zero = (
    TodaPrimaryGroupZeroStatement(
      group=pi10_6,
    )
  )

  pi10_6_zero_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_pi10_6_zero
    )
  )

  expected_final = (
    TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=4,
        ),
        sphere_dimension=n,
      )
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_final
    )
  )

  return {
    "phase68_6": phase68_6,
    "phase68_9": phase68_9,
    "pi9_5_step": pi9_5_step,
    "nu6_eta9_zero_step": (
      nu6_eta9_zero_step
    ),
    "pi9_5": pi9_5,
    "pi10_6": pi10_6,
    "pi10_11": pi10_11,
    "exactness_window": (
      exactness_window
    ),
    "exactness_window_step": (
      exactness_window_step
    ),
    "pi10_11_zero_step": (
      pi10_11_zero_step
    ),
    "phase46": phase46,
    "n": n,
    "stable_isomorphism_step": (
      stable_isomorphism_step
    ),
    "n_ge_6_step": n_ge_6_step,
    "exactness_rule": exactness_rule,
    "surjective_rule": (
      surjective_rule
    ),
    "pi10_6_zero_rule": (
      pi10_6_zero_rule
    ),
    "higher_zero_rule": (
      higher_zero_rule
    ),
    "premise_steps": premise_steps,
    "result": result,
    "exactness_step": (
      exactness_step
    ),
    "surjective_step": (
      surjective_step
    ),
    "expected_pi10_6_zero": (
      expected_pi10_6_zero
    ),
    "pi10_6_zero_step": (
      pi10_6_zero_step
    ),
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase68_10_reuses_derived_pi9_5():
  data = build_phase68_10_data()

  assert (
    data[
      "pi9_5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_10_reuses_derived_nu6_eta9_zero():
  data = build_phase68_10_data()

  assert (
    data[
      "nu6_eta9_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_10_structural_exactness_window_is_given():
  data = build_phase68_10_data()

  assert (
    data[
      "exactness_window_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase68_10_derives_concrete_exactness():
  data = build_phase68_10_data()

  assert (
    data[
      "exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_10_pi10_11_zero_is_foundational_given():
  data = build_phase68_10_data()

  assert (
    data[
      "pi10_11_zero_step"
    ].conclusion
    == TodaPrimaryGroupZeroStatement(
      group=data[
        "pi10_11"
      ],
    )
  )

  assert (
    data[
      "pi10_11_zero_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase68_10_derives_suspension_surjective():
  data = build_phase68_10_data()

  assert (
    data[
      "surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_10_surjectivity_uses_exactness_and_zero_target():
  data = build_phase68_10_data()

  assert (
    data[
      "surjective_step"
    ].premises
    == (
      data[
        "pi10_11_zero_step"
      ],
      data[
        "exactness_step"
      ],
    )
  )


def test_phase68_10_derives_pi10_6_zero():
  data = build_phase68_10_data()

  assert (
    data[
      "pi10_6_zero_step"
    ].conclusion
    == data[
      "expected_pi10_6_zero"
    ]
  )

  assert (
    data[
      "pi10_6_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_10_pi10_6_zero_uses_exact_dependencies():
  data = build_phase68_10_data()

  assert (
    data[
      "pi10_6_zero_step"
    ].premises
    == (
      data[
        "pi9_5_step"
      ],
      data[
        "surjective_step"
      ],
      data[
        "nu6_eta9_zero_step"
      ],
    )
  )


def test_phase68_10_reuses_phase46_isomorphism():
  data = build_phase68_10_data()

  assert isinstance(
    data[
      "stable_isomorphism_step"
    ].conclusion,
    Toda45IsomorphismStatement,
  )

  assert (
    data[
      "stable_isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_10_toda45_source_is_pi10_6_structurally():
  data = build_phase68_10_data()

  source = (
    data[
      "stable_isomorphism_step"
    ].conclusion
    .map
    .source_group
  )

  assert source == TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=6,
      right=4,
    ),
    sphere_dimension=6,
  )


def test_phase68_10_toda45_target_is_pi_n_plus_4_n():
  data = build_phase68_10_data()

  target = (
    data[
      "stable_isomorphism_step"
    ].conclusion
    .map
    .target_group
  )

  assert target == TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=data[
        "n"
      ],
      right=4,
    ),
    sphere_dimension=data[
      "n"
    ],
  )


def test_phase68_10_toda45_exponent_is_n_minus_6():
  data = build_phase68_10_data()

  assert (
    data[
      "stable_isomorphism_step"
    ].conclusion
    .map
    .exponent
    == ScalarSum(
      left=data[
        "n"
      ],
      right=ScalarProduct(
        left=-1,
        right=6,
      ),
    )
  )


def test_phase68_10_range_is_n_at_least_6():
  data = build_phase68_10_data()

  assert (
    data[
      "n_ge_6_step"
    ].conclusion
    == ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=6,
    )
  )


def test_phase68_10_derives_higher_zero():
  data = build_phase68_10_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_final"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_10_final_is_pi_n_plus_4_n_zero():
  data = build_phase68_10_data()

  assert (
    data[
      "final_step"
    ].conclusion.group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=4,
      ),
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase68_10_final_uses_exact_three_dependencies():
  data = build_phase68_10_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi10_6_zero_step"
      ],
      data[
        "stable_isomorphism_step"
      ],
      data[
        "n_ge_6_step"
      ],
    )
  )


def test_phase68_10_rejects_given_pi10_6_zero():
  data = build_phase68_10_data()

  given = ProofStep(
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
      "higher_zero_rule"
    ],
    (
      given,
      data[
        "stable_isomorphism_step"
      ],
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase68_10_rejects_given_toda45():
  data = build_phase68_10_data()

  given = ProofStep(
    conclusion=(
      data[
        "stable_isomorphism_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "higher_zero_rule"
    ],
    (
      data[
        "pi10_6_zero_step"
      ],
      given,
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase68_10_final_not_present_initially():
  data = build_phase68_10_data()

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase68_10_reaches_fixed_point():
  data = build_phase68_10_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


