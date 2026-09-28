from expression import (
  ScalarSum,
)
from homotopy_groups import (
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
)
from low_dimensional_facts import (
  pi_6_7_zero_fact,
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
from probes.probe_phase48_capabilities import (
  build_phase48_representative_result,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaSuspensionSurjectiveStatement,
  toda_prop53_n4_phase48_injectivity_bridge_inference_rule,
  toda_prop53_n4_suspension_isomorphism_inference_rule,
  toda_prop53_n4_zero_right_suspension_surjective_inference_rule,
)


def build_phase59_5_data():
  phase48 = (
    build_phase48_representative_result(
      i=6,
      n=4,
    )
  )

  phase48_injectivity_step = (
    phase48[
      "injectivity_steps"
    ][
      0
    ]
  )

  zero_statement = (
    pi_6_7_zero_fact()
  )

  zero_step = ProofStep(
    conclusion=zero_statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi_5_3 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=3,
  )

  pi_6_4 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=4,
  )

  pi_6_7 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=7,
  )

  exactness = (
    TodaProp42ExactnessStatement(
      window=TodaEHPExactnessWindow(
        source_term=pi_5_3,
        middle_term=pi_6_4,
        target_term=pi_6_7,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      ),
    )
  )

  exactness_step = ProofStep(
    conclusion=exactness,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  expected_suspension_map = (
    TodaSuspensionMap(
      source_group=pi_5_3,
      target_group=pi_6_4,
    )
  )

  expected_injectivity = (
    TodaProp44SuspensionInjectiveStatement(
      map=expected_suspension_map,
    )
  )

  expected_surjectivity = (
    TodaSuspensionSurjectiveStatement(
      map=expected_suspension_map,
    )
  )

  expected_isomorphism = (
    TodaSuspensionIsomorphismStatement(
      map=expected_suspension_map,
    )
  )

  injectivity_bridge_rule = (
    toda_prop53_n4_phase48_injectivity_bridge_inference_rule()
  )

  surjectivity_rule = (
    toda_prop53_n4_zero_right_suspension_surjective_inference_rule()
  )

  isomorphism_rule = (
    toda_prop53_n4_suspension_isomorphism_inference_rule()
  )

  rules = (
    injectivity_bridge_rule,
    surjectivity_rule,
    isomorphism_rule,
  )

  premise_steps = (
    phase48_injectivity_step,
    zero_step,
    exactness_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  injectivity_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_injectivity
    )
  )

  surjectivity_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_surjectivity
    )
  )

  isomorphism_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_isomorphism
    )
  )

  return {
    "phase48": phase48,
    "phase48_injectivity_step": (
      phase48_injectivity_step
    ),
    "zero_statement": (
      zero_statement
    ),
    "zero_step": zero_step,
    "exactness": exactness,
    "exactness_step": exactness_step,
    "pi_5_3": pi_5_3,
    "pi_6_4": pi_6_4,
    "pi_6_7": pi_6_7,
    "expected_suspension_map": (
      expected_suspension_map
    ),
    "expected_injectivity": (
      expected_injectivity
    ),
    "expected_surjectivity": (
      expected_surjectivity
    ),
    "expected_isomorphism": (
      expected_isomorphism
    ),
    "injectivity_bridge_rule": (
      injectivity_bridge_rule
    ),
    "surjectivity_rule": (
      surjectivity_rule
    ),
    "isomorphism_rule": (
      isomorphism_rule
    ),
    "premise_steps": premise_steps,
    "result": result,
    "injectivity_step": (
      injectivity_step
    ),
    "surjectivity_step": (
      surjectivity_step
    ),
    "isomorphism_step": (
      isomorphism_step
    ),
  }


def test_phase59_5_pi6_7_zero_fact_is_concrete():
  data = build_phase59_5_data()

  assert (
    data[
      "zero_statement"
    ].group
    == TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=7,
    )
  )


def test_phase59_5_reuses_phase48_derived_injectivity():
  data = build_phase59_5_data()

  step = data[
    "phase48_injectivity_step"
  ]

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    step.conclusion,
    TodaProp44SuspensionInjectiveStatement,
  )


def test_phase59_5_phase48_source_remains_structural():
  data = build_phase59_5_data()

  source = (
    data[
      "phase48_injectivity_step"
    ].conclusion.map.source_group
  )

  assert (
    source
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=6,
        right=-1,
      ),
      sphere_dimension=ScalarSum(
        left=4,
        right=-1,
      ),
    )
  )


def test_phase59_5_injectivity_bridge_matches_phase48_result():
  data = build_phase59_5_data()

  assert find_inference_match(
    data[
      "injectivity_bridge_rule"
    ],
    (
      data[
        "phase48_injectivity_step"
      ],
    ),
  ) is not None


def test_phase59_5_derives_concrete_e_injective():
  data = build_phase59_5_data()

  assert (
    data[
      "injectivity_step"
    ].conclusion
    == data[
      "expected_injectivity"
    ]
  )

  assert (
    data[
      "injectivity_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase59_5_injectivity_preserves_phase48_provenance():
  data = build_phase59_5_data()

  assert (
    data[
      "injectivity_step"
    ].premises
    == (
      data[
        "phase48_injectivity_step"
      ],
    )
  )


def test_phase59_5_exactness_is_correct_e_h_window():
  data = build_phase59_5_data()

  window = (
    data[
      "exactness"
    ].window
  )

  assert (
    window.source_term
    == data[
      "pi_5_3"
    ]
  )

  assert (
    window.middle_term
    == data[
      "pi_6_4"
    ]
  )

  assert (
    window.target_term
    == data[
      "pi_6_7"
    ]
  )

  assert window.first_map == EHP_E_MAP
  assert window.second_map == EHP_H_MAP


def test_phase59_5_surjectivity_rule_matches_zero_and_exactness():
  data = build_phase59_5_data()

  assert find_inference_match(
    data[
      "surjectivity_rule"
    ],
    (
      data[
        "zero_step"
      ],
      data[
        "exactness_step"
      ],
    ),
  ) is not None


def test_phase59_5_derives_e_surjective():
  data = build_phase59_5_data()

  assert (
    data[
      "surjectivity_step"
    ].conclusion
    == data[
      "expected_surjectivity"
    ]
  )

  assert (
    data[
      "surjectivity_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase59_5_isomorphism_rule_matches_two_derived_properties():
  data = build_phase59_5_data()

  assert find_inference_match(
    data[
      "isomorphism_rule"
    ],
    (
      data[
        "injectivity_step"
      ],
      data[
        "surjectivity_step"
      ],
    ),
  ) is not None


def test_phase59_5_derives_e_pi5_3_to_pi6_4_isomorphism():
  data = build_phase59_5_data()

  assert (
    data[
      "isomorphism_step"
    ].conclusion
    == data[
      "expected_isomorphism"
    ]
  )

  assert (
    data[
      "isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase59_5_final_map_is_pi5_3_to_pi6_4():
  data = build_phase59_5_data()

  map_instance = (
    data[
      "isomorphism_step"
    ].conclusion.map
  )

  assert (
    map_instance.source_group
    == TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    )
  )

  assert (
    map_instance.target_group
    == TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=4,
    )
  )


def test_phase59_5_final_provenance_uses_injective_and_surjective():
  data = build_phase59_5_data()

  assert (
    data[
      "isomorphism_step"
    ].premises
    == (
      data[
        "injectivity_step"
      ],
      data[
        "surjectivity_step"
      ],
    )
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in (
      data[
        "injectivity_step"
      ],
      data[
        "surjectivity_step"
      ],
    )
  )


def test_phase59_5_rejects_given_phase48_injectivity():
  data = build_phase59_5_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "phase48_injectivity_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "injectivity_bridge_rule"
    ],
    (
      given_step,
    ),
  ) is None


def test_phase59_5_rejects_wrong_zero_group():
  data = build_phase59_5_data()

  wrong_zero = ProofStep(
    conclusion=type(
      data[
        "zero_statement"
      ]
    )(
      group=TodaPrimaryGroup(
        group_dimension=5,
        sphere_dimension=7,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "surjectivity_rule"
    ],
    (
      wrong_zero,
      data[
        "exactness_step"
      ],
    ),
  ) is None


def test_phase59_5_final_result_is_not_given():
  data = build_phase59_5_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_isomorphism"
    ]
    not in initial_conclusions
  )


def test_phase59_5_reaches_fixed_point_in_two_rounds():
  data = build_phase59_5_data()

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
    == 2
  )

  assert (
    data[
      "injectivity_step"
    ]
    in data[
      "result"
    ].round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "surjectivity_step"
    ]
    in data[
      "result"
    ].round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "isomorphism_step"
    ]
    in data[
      "result"
    ].round_results[
      1
    ].new_steps
  )



