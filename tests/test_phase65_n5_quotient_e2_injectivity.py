from dataclasses import replace
from functools import lru_cache

from homotopy_groups import (
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from probes.probe_phase63_capabilities import (
  build_phase63_representative_result,
)
from toda_rules import (
  TodaIteratedSuspensionInjectiveStatement,
  TodaProp56Pi8_5QuotientStatement,
  toda_prop56_pi6_3_e2_injective_inference_rule,
  toda_prop56_pi8_5_quotient_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase65_6_data():
  phase63 = (
    build_phase63_representative_result()
  )

  toda56_step = (
    phase63[
      "integration_step"
    ]
  )

  pi_6_3 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  )

  pi_8_5 = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=5,
  )

  e2_map = TodaIteratedSuspensionMap(
    exponent=2,
    source_group=pi_6_3,
    target_group=pi_8_5,
  )

  expected_quotient = (
    TodaProp56Pi8_5QuotientStatement(
      ambient_group=pi_8_5,
      subobject_map=e2_map,
      quotient_order=2,
    )
  )

  expected_injective = (
    TodaIteratedSuspensionInjectiveStatement(
      map=e2_map,
    )
  )

  quotient_rule = (
    toda_prop56_pi8_5_quotient_inference_rule()
  )

  injective_rule = (
    toda_prop56_pi6_3_e2_injective_inference_rule()
  )

  rules = (
    quotient_rule,
    injective_rule,
  )

  premise_steps = (
    toda56_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  quotient_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_quotient
    )
  )

  injective_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_injective
    )
  )

  return {
    "phase63": phase63,
    "toda56_step": toda56_step,
    "pi_6_3": pi_6_3,
    "pi_8_5": pi_8_5,
    "e2_map": e2_map,
    "expected_quotient": (
      expected_quotient
    ),
    "expected_injective": (
      expected_injective
    ),
    "quotient_rule": quotient_rule,
    "injective_rule": injective_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "quotient_step": quotient_step,
    "injective_step": injective_step,
  }


def test_phase65_6_reuses_derived_toda56():
  data = build_phase65_6_data()

  assert (
    data[
      "toda56_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_6_e2_map_has_exponent_two():
  data = build_phase65_6_data()

  assert (
    data[
      "e2_map"
    ].exponent
    == 2
  )


def test_phase65_6_e2_map_source_is_pi6_3():
  data = build_phase65_6_data()

  assert (
    data[
      "e2_map"
    ].source_group
    == TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=3,
    )
  )


def test_phase65_6_e2_map_target_is_pi8_5():
  data = build_phase65_6_data()

  assert (
    data[
      "e2_map"
    ].target_group
    == TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    )
  )


def test_phase65_6_quotient_rule_matches_toda56():
  data = build_phase65_6_data()

  assert find_inference_match(
    data[
      "quotient_rule"
    ],
    (
      data[
        "toda56_step"
      ],
    ),
  ) is not None


def test_phase65_6_injective_rule_matches_toda56():
  data = build_phase65_6_data()

  assert find_inference_match(
    data[
      "injective_rule"
    ],
    (
      data[
        "toda56_step"
      ],
    ),
  ) is not None


def test_phase65_6_derives_pi8_5_quotient():
  data = build_phase65_6_data()

  step = data[
    "quotient_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_quotient"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase65_6_quotient_ambient_is_pi8_5():
  data = build_phase65_6_data()

  assert (
    data[
      "quotient_step"
    ].conclusion.ambient_group
    == data[
      "pi_8_5"
    ]
  )


def test_phase65_6_quotient_subobject_is_e2_pi6_3():
  data = build_phase65_6_data()

  assert (
    data[
      "quotient_step"
    ].conclusion.subobject_map
    == data[
      "e2_map"
    ]
  )


def test_phase65_6_quotient_has_order_two():
  data = build_phase65_6_data()

  assert (
    data[
      "quotient_step"
    ].conclusion.quotient_order
    == 2
  )


def test_phase65_6_derives_e2_injective():
  data = build_phase65_6_data()

  step = data[
    "injective_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_injective"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase65_6_injective_statement_preserves_map_instance():
  data = build_phase65_6_data()

  assert (
    data[
      "injective_step"
    ].conclusion.map
    == data[
      "e2_map"
    ]
  )


def test_phase65_6_two_results_share_same_map_value():
  data = build_phase65_6_data()

  assert (
    data[
      "quotient_step"
    ].conclusion.subobject_map
    == data[
      "injective_step"
    ].conclusion.map
  )


def test_phase65_6_provenance_uses_toda56():
  data = build_phase65_6_data()

  assert (
    data[
      "quotient_step"
    ].premises
    == (
      data[
        "toda56_step"
      ],
    )
  )

  assert (
    data[
      "injective_step"
    ].premises
    == (
      data[
        "toda56_step"
      ],
    )
  )


def test_phase65_6_rejects_given_toda56():
  data = build_phase65_6_data()

  given_step = ProofStep(
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
      "quotient_rule"
    ],
    (
      given_step,
    ),
  ) is None

  assert find_inference_match(
    data[
      "injective_rule"
    ],
    (
      given_step,
    ),
  ) is None


def test_phase65_6_results_are_not_given():
  data = build_phase65_6_data()

  assert (
    data[
      "quotient_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "injective_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase65_6_reaches_fixed_point_in_one_round():
  data = build_phase65_6_data()

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
      "quotient_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "injective_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )


