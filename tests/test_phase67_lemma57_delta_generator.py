from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
  Zero,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from test_phase67_lemma57_nu_prime_specialization import (
  build_phase67_5_data,
)
from test_phase67_pi6_2_eta2_nu_prime import (
  build_phase67_6_data,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaDeltaSurjectiveStatement,
  TodaProp42ExactnessStatement,
  toda_lemma57_concrete_delta_e_exactness_inference_rule,
  toda_lemma57_delta_nu5_generator_inference_rule,
  toda_lemma57_delta_surjective_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase67_7_data():
  phase65_9 = (
    build_phase65_9_data()
  )

  phase67_5 = (
    build_phase67_5_data()
  )

  phase67_6 = (
    build_phase67_6_data()
  )

  prop56_step = (
    phase65_9[
      "integration_step"
    ]
  )

  eta2_nu_prime_zero_step = (
    phase67_5[
      "final_step"
    ]
  )

  pi6_2_step = (
    phase67_6[
      "final_step"
    ]
  )

  window = TodaEHPExactnessWindow(
    source_term=TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    ),
    middle_term=TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=2,
    ),
    target_term=TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=3,
    ),
    first_map=EHP_DELTA_MAP,
    second_map=EHP_E_MAP,
  )

  window_step = ProofStep(
    conclusion=window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  exactness_rule = (
    toda_lemma57_concrete_delta_e_exactness_inference_rule()
  )

  delta_surjective_rule = (
    toda_lemma57_delta_surjective_inference_rule()
  )

  delta_generator_rule = (
    toda_lemma57_delta_nu5_generator_inference_rule()
  )

  rules = (
    exactness_rule,
    delta_surjective_rule,
    delta_generator_rule,
  )

  premise_steps = (
    prop56_step,
    eta2_nu_prime_zero_step,
    pi6_2_step,
    window_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  expected_exactness = (
    TodaProp42ExactnessStatement(
      window=window,
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

  delta_map = TodaDeltaMap(
    source_group=TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=2,
    ),
  )

  expected_surjective = (
    TodaDeltaSurjectiveStatement(
      map=delta_map,
    )
  )

  delta_surjective_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_surjective
    )
  )

  nu_5 = (
    prop56_step
    .conclusion
    .pi8_5_group_relation
    .rhs
    .generator
  )

  eta2_nu_prime = (
    pi6_2_step
    .conclusion
    .rhs
    .generator
  )

  expected_final = (
    TodaDeltaImageUpToSignStatement(
      map=delta_map,
      element=nu_5,
      positive_value=eta2_nu_prime,
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
    "phase65_9": phase65_9,
    "phase67_5": phase67_5,
    "phase67_6": phase67_6,
    "prop56_step": prop56_step,
    "eta2_nu_prime_zero_step": (
      eta2_nu_prime_zero_step
    ),
    "pi6_2_step": pi6_2_step,
    "window": window,
    "window_step": window_step,
    "exactness_rule": exactness_rule,
    "delta_surjective_rule": (
      delta_surjective_rule
    ),
    "delta_generator_rule": (
      delta_generator_rule
    ),
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "expected_exactness": (
      expected_exactness
    ),
    "exactness_step": exactness_step,
    "delta_map": delta_map,
    "expected_surjective": (
      expected_surjective
    ),
    "delta_surjective_step": (
      delta_surjective_step
    ),
    "nu_5": nu_5,
    "eta2_nu_prime": eta2_nu_prime,
    "expected_final": expected_final,
    "final_step": final_step,
  }


def test_phase67_7_reuses_derived_eta2_nu_prime_zero():
  data = build_phase67_7_data()

  assert (
    data[
      "eta2_nu_prime_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_7_reuses_derived_pi6_2():
  data = build_phase67_7_data()

  assert (
    data[
      "pi6_2_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_7_reuses_derived_prop56():
  data = build_phase67_7_data()

  assert (
    data[
      "prop56_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_7_window_is_concrete_delta_e_segment():
  data = build_phase67_7_data()

  assert (
    data[
      "window"
    ].source_term
    == TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    )
  )

  assert (
    data[
      "window"
    ].middle_term
    == TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=2,
    )
  )

  assert (
    data[
      "window"
    ].target_term
    == TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=3,
    )
  )


def test_phase67_7_derives_concrete_exactness():
  data = build_phase67_7_data()

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


def test_phase67_7_exactness_provenance_uses_window():
  data = build_phase67_7_data()

  assert (
    data[
      "exactness_step"
    ].premises
    == (
      data[
        "window_step"
      ],
    )
  )


def test_phase67_7_derives_delta_surjective():
  data = build_phase67_7_data()

  assert (
    data[
      "delta_surjective_step"
    ].conclusion
    == data[
      "expected_surjective"
    ]
  )

  assert (
    data[
      "delta_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_7_delta_surjective_uses_three_dependencies():
  data = build_phase67_7_data()

  assert (
    data[
      "delta_surjective_step"
    ].premises
    == (
      data[
        "eta2_nu_prime_zero_step"
      ],
      data[
        "pi6_2_step"
      ],
      data[
        "exactness_step"
      ],
    )
  )


def test_phase67_7_prop56_contains_pi8_5_z8_nu5():
  data = build_phase67_7_data()

  relation = (
    data[
      "prop56_step"
    ].conclusion
    .pi8_5_group_relation
  )

  assert relation.lhs == TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=5,
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 8

  assert (
    relation.rhs.generator
    == data[
      "nu_5"
    ]
  )


def test_phase67_7_derives_delta_nu5():
  data = build_phase67_7_data()

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


def test_phase67_7_final_is_delta_nu5_plus_minus_eta2_nu_prime():
  data = build_phase67_7_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert statement.element is data[
    "nu_5"
  ]

  assert (
    statement.positive_value
    is data[
      "eta2_nu_prime"
    ]
  )


def test_phase67_7_final_uses_exact_three_dependencies():
  data = build_phase67_7_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "delta_surjective_step"
      ],
      data[
        "pi6_2_step"
      ],
      data[
        "prop56_step"
      ],
    )
  )


def test_phase67_7_rejects_given_eta2_nu_prime_zero():
  data = build_phase67_7_data()

  given_zero = ProofStep(
    conclusion=(
      data[
        "eta2_nu_prime_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "delta_surjective_rule"
    ],
    (
      given_zero,
      data[
        "pi6_2_step"
      ],
      data[
        "exactness_step"
      ],
    ),
  ) is None


def test_phase67_7_rejects_given_pi6_2():
  data = build_phase67_7_data()

  given_pi6_2 = ProofStep(
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
      "delta_surjective_rule"
    ],
    (
      data[
        "eta2_nu_prime_zero_step"
      ],
      given_pi6_2,
      data[
        "exactness_step"
      ],
    ),
  ) is None


def test_phase67_7_rejects_wrong_exactness_target():
  data = build_phase67_7_data()

  wrong_window = replace(
    data[
      "window"
    ],
    target_term=TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
    ),
  )

  wrong_step = ProofStep(
    conclusion=TodaProp42ExactnessStatement(
      window=wrong_window,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "delta_surjective_rule"
    ],
    (
      data[
        "eta2_nu_prime_zero_step"
      ],
      data[
        "pi6_2_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase67_7_rejects_given_delta_surjective():
  data = build_phase67_7_data()

  given_surjective = ProofStep(
    conclusion=(
      data[
        "delta_surjective_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "delta_generator_rule"
    ],
    (
      given_surjective,
      data[
        "pi6_2_step"
      ],
      data[
        "prop56_step"
      ],
    ),
  ) is None


def test_phase67_7_rejects_wrong_pi8_5_order():
  data = build_phase67_7_data()

  prop56 = (
    data[
      "prop56_step"
    ].conclusion
  )

  wrong_pi8_5 = replace(
    prop56.pi8_5_group_relation,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=data[
        "nu_5"
      ],
    ),
  )

  wrong_prop56 = replace(
    prop56,
    pi8_5_group_relation=wrong_pi8_5,
  )

  wrong_step = ProofStep(
    conclusion=wrong_prop56,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "delta_generator_rule"
    ],
    (
      data[
        "delta_surjective_step"
      ],
      data[
        "pi6_2_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase67_7_final_is_not_given():
  data = build_phase67_7_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase67_7_reaches_fixed_point():
  data = build_phase67_7_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    data[
      "result"
    ].round_count
    == 3
  )



