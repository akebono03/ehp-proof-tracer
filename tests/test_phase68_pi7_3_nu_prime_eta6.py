from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_E_MAP,
  EHP_H_MAP,
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
from test_phase65_equation57_injectivity import (
  build_phase65_3_data,
)
from test_phase67_lemma57_nu_prime_specialization import (
  build_phase67_5_data,
)
from test_phase67_pi6_2_eta2_nu_prime import (
  build_phase67_6_data,
)
from toda_rules import (
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaProp42ExactnessStatement,
  toda_hopf_injective_surjective_implies_isomorphism_inference_rule,
  toda_prop58_concrete_e_h_exactness_inference_rule,
  toda_prop58_pi7_3_finite_cyclic_inference_rule,
  toda_prop58_pi7_3_hopf_injective_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase68_3_data():
  phase65_3 = (
    build_phase65_3_data()
  )

  phase67_5 = (
    build_phase67_5_data()
  )

  phase67_6 = (
    build_phase67_6_data()
  )

  equation57_step = (
    phase65_3[
      "equation57_step"
    ]
  )

  hopf_surjective_step = (
    phase65_3[
      "hopf_surjective_step"
    ]
  )

  prop53_step = (
    phase65_3[
      "prop53_step"
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

  pi6_2 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=2,
  )

  pi7_3 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=3,
  )

  pi7_5 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=5,
  )

  window = TodaEHPExactnessWindow(
    source_term=pi6_2,
    middle_term=pi7_3,
    target_term=pi7_5,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )

  window_step = ProofStep(
    conclusion=window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  exactness_rule = (
    toda_prop58_concrete_e_h_exactness_inference_rule()
  )

  hopf_injective_rule = (
    toda_prop58_pi7_3_hopf_injective_inference_rule()
  )

  hopf_isomorphism_rule = (
    toda_hopf_injective_surjective_implies_isomorphism_inference_rule()
  )

  group_rule = (
    toda_prop58_pi7_3_finite_cyclic_inference_rule()
  )

  rules = (
    exactness_rule,
    hopf_injective_rule,
    hopf_isomorphism_rule,
    group_rule,
  )

  premise_steps = (
    equation57_step,
    hopf_surjective_step,
    prop53_step,
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

  hopf_map = TodaHopfInvariantMap(
    source_group=pi7_3,
    target_group=pi7_5,
  )

  expected_hopf_injective = (
    TodaHopfInvariantInjectiveStatement(
      map=hopf_map,
    )
  )

  hopf_injective_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_hopf_injective
    )
  )

  expected_hopf_isomorphism = (
    TodaHopfInvariantIsomorphismStatement(
      map=hopf_map,
    )
  )

  hopf_isomorphism_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_hopf_isomorphism
    )
  )

  nu_prime_eta6 = (
    equation57_step
    .conclusion
    .lhs
    .expression
  )

  expected_final = Relation(
    lhs=pi7_3,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=nu_prime_eta6,
    ),
    relation_type=RelationType.EQUALITY,
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
    "phase65_3": phase65_3,
    "phase67_5": phase67_5,
    "phase67_6": phase67_6,
    "equation57_step": equation57_step,
    "hopf_surjective_step": (
      hopf_surjective_step
    ),
    "prop53_step": prop53_step,
    "eta2_nu_prime_zero_step": (
      eta2_nu_prime_zero_step
    ),
    "pi6_2_step": pi6_2_step,
    "pi6_2": pi6_2,
    "pi7_3": pi7_3,
    "pi7_5": pi7_5,
    "window": window,
    "window_step": window_step,
    "exactness_rule": exactness_rule,
    "hopf_injective_rule": (
      hopf_injective_rule
    ),
    "hopf_isomorphism_rule": (
      hopf_isomorphism_rule
    ),
    "group_rule": group_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "expected_exactness": (
      expected_exactness
    ),
    "exactness_step": exactness_step,
    "hopf_map": hopf_map,
    "expected_hopf_injective": (
      expected_hopf_injective
    ),
    "hopf_injective_step": (
      hopf_injective_step
    ),
    "expected_hopf_isomorphism": (
      expected_hopf_isomorphism
    ),
    "hopf_isomorphism_step": (
      hopf_isomorphism_step
    ),
    "nu_prime_eta6": nu_prime_eta6,
    "expected_final": expected_final,
    "final_step": final_step,
  }


def test_phase68_3_reuses_toda57():
  data = build_phase68_3_data()

  assert (
    data[
      "equation57_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_3_reuses_hopf_surjectivity():
  data = build_phase68_3_data()

  assert isinstance(
    data[
      "hopf_surjective_step"
    ].conclusion,
    TodaHopfInvariantSurjectiveStatement,
  )

  assert (
    data[
      "hopf_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_3_reuses_phase67_zero():
  data = build_phase68_3_data()

  assert (
    data[
      "eta2_nu_prime_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_3_reuses_phase67_pi6_2():
  data = build_phase68_3_data()

  assert (
    data[
      "pi6_2_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_3_window_is_pi6_2_e_pi7_3_h_pi7_5():
  data = build_phase68_3_data()

  assert (
    data[
      "window"
    ].source_term
    == data[
      "pi6_2"
    ]
  )

  assert (
    data[
      "window"
    ].middle_term
    == data[
      "pi7_3"
    ]
  )

  assert (
    data[
      "window"
    ].target_term
    == data[
      "pi7_5"
    ]
  )

  assert (
    data[
      "window"
    ].first_map
    == EHP_E_MAP
  )

  assert (
    data[
      "window"
    ].second_map
    == EHP_H_MAP
  )


def test_phase68_3_derives_concrete_exactness():
  data = build_phase68_3_data()

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


def test_phase68_3_derives_hopf_injective():
  data = build_phase68_3_data()

  assert (
    data[
      "hopf_injective_step"
    ].conclusion
    == data[
      "expected_hopf_injective"
    ]
  )

  assert (
    data[
      "hopf_injective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_3_hopf_injective_uses_exact_dependencies():
  data = build_phase68_3_data()

  assert (
    data[
      "hopf_injective_step"
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


def test_phase68_3_derives_hopf_isomorphism():
  data = build_phase68_3_data()

  assert (
    data[
      "hopf_isomorphism_step"
    ].conclusion
    == data[
      "expected_hopf_isomorphism"
    ]
  )

  assert (
    data[
      "hopf_isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_3_hopf_isomorphism_uses_injective_and_surjective():
  data = build_phase68_3_data()

  assert (
    data[
      "hopf_isomorphism_step"
    ].premises
    == (
      data[
        "hopf_injective_step"
      ],
      data[
        "hopf_surjective_step"
      ],
    )
  )


def test_phase68_3_derives_pi7_3():
  data = build_phase68_3_data()

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


def test_phase68_3_pi7_3_is_order_two():
  data = build_phase68_3_data()

  group = (
    data[
      "final_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert group.order == 2


def test_phase68_3_generator_is_nu_prime_eta6():
  data = build_phase68_3_data()

  assert (
    data[
      "final_step"
    ].conclusion.rhs.generator
    == data[
      "nu_prime_eta6"
    ]
  )

  assert isinstance(
    data[
      "nu_prime_eta6"
    ],
    Composition,
  )


def test_phase68_3_final_uses_exact_three_dependencies():
  data = build_phase68_3_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "hopf_isomorphism_step"
      ],
      data[
        "equation57_step"
      ],
      data[
        "prop53_step"
      ],
    )
  )


def test_phase68_3_rejects_given_pi6_2():
  data = build_phase68_3_data()

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
      "hopf_injective_rule"
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


def test_phase68_3_rejects_given_eta2_nu_prime_zero():
  data = build_phase68_3_data()

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
      "hopf_injective_rule"
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


def test_phase68_3_rejects_wrong_exactness_target():
  data = build_phase68_3_data()

  wrong_window = replace(
    data[
      "window"
    ],
    target_term=TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=6,
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
      "hopf_injective_rule"
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


def test_phase68_3_rejects_given_hopf_isomorphism():
  data = build_phase68_3_data()

  given_isomorphism = ProofStep(
    conclusion=(
      data[
        "hopf_isomorphism_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "group_rule"
    ],
    (
      given_isomorphism,
      data[
        "equation57_step"
      ],
      data[
        "prop53_step"
      ],
    ),
  ) is None


def test_phase68_3_final_result_is_not_given():
  data = build_phase68_3_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )

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


def test_phase68_3_reaches_fixed_point():
  data = build_phase68_3_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


