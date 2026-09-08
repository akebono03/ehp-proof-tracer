from dataclasses import replace

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase63_nu4_prop44_specialization import (
  build_phase63_2_data,
)
from toda_rules import (
  TodaProp44IsomorphismStatement,
  toda_56_nu4_prop44_isomorphism_inference_rule,
)


def build_phase63_3_data():
  phase63_2 = (
    build_phase63_2_data()
  )

  specialization_step = (
    phase63_2[
      "specialization_step"
    ]
  )

  nu_4 = (
    specialization_step
    .conclusion
    .alpha
  )

  i = ScalarSymbol(
    name="i",
  )

  first_variable = HomotopyElement(
    name="α",
    dimension=3,
    source=ScalarSum(
      left=i,
      right=-1,
    ),
    target=3,
  )

  second_variable = HomotopyElement(
    name="β",
    dimension=7,
    source=i,
    target=7,
  )

  first_summand = TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=i,
      right=-1,
    ),
    sphere_dimension=3,
  )

  second_summand = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=7,
  )

  source_group = DirectSumGroup(
    summands=(
      first_summand,
      second_summand,
    ),
  )

  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=4,
  )

  formula = Sum(
    left=Suspension(
      expression=first_variable,
    ),
    right=Composition(
      left=nu_4,
      right=second_variable,
    ),
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=source_group,
      target_group=target_group,
      alpha=nu_4,
      beta=first_variable,
      gamma=second_variable,
      formula=formula,
    )
  )

  decomposition_map_step = ProofStep(
    conclusion=decomposition_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  expected_statement = (
    TodaProp44IsomorphismStatement(
      map=decomposition_map,
    )
  )

  rule = (
    toda_56_nu4_prop44_isomorphism_inference_rule()
  )

  premise_steps = (
    specialization_step,
    decomposition_map_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  isomorphism_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase63_2": phase63_2,
    "specialization_step": (
      specialization_step
    ),
    "nu_4": nu_4,
    "i": i,
    "first_variable": first_variable,
    "second_variable": second_variable,
    "first_summand": first_summand,
    "second_summand": second_summand,
    "source_group": source_group,
    "target_group": target_group,
    "formula": formula,
    "decomposition_map": (
      decomposition_map
    ),
    "decomposition_map_step": (
      decomposition_map_step
    ),
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "isomorphism_step": (
      isomorphism_step
    ),
  }


def test_phase63_3_reuses_derived_phase63_2_specialization():
  data = build_phase63_3_data()

  assert (
    data[
      "specialization_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase63_3_decomposition_map_is_explicit_given():
  data = build_phase63_3_data()

  assert (
    data[
      "decomposition_map_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase63_3_source_is_pi_i_minus_one_3_plus_pi_i_7():
  data = build_phase63_3_data()

  source = (
    data[
      "decomposition_map"
    ].source_group
  )

  assert isinstance(
    source,
    DirectSumGroup,
  )

  assert (
    source.summands
    == (
      TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=data[
            "i"
          ],
          right=-1,
        ),
        sphere_dimension=3,
      ),
      TodaPrimaryGroup(
        group_dimension=data[
          "i"
        ],
        sphere_dimension=7,
      ),
    )
  )


def test_phase63_3_target_is_pi_i_4():
  data = build_phase63_3_data()

  assert (
    data[
      "decomposition_map"
    ].target_group
    == TodaPrimaryGroup(
      group_dimension=data[
        "i"
      ],
      sphere_dimension=4,
    )
  )


def test_phase63_3_map_alpha_is_nu4():
  data = build_phase63_3_data()

  assert (
    data[
      "decomposition_map"
    ].alpha
    == data[
      "nu_4"
    ]
  )


def test_phase63_3_formula_is_suspension_plus_nu4_composition():
  data = build_phase63_3_data()

  assert (
    data[
      "decomposition_map"
    ].formula
    == Sum(
      left=Suspension(
        expression=data[
          "first_variable"
        ],
      ),
      right=Composition(
        left=data[
          "nu_4"
        ],
        right=data[
          "second_variable"
        ],
      ),
    )
  )


def test_phase63_3_rule_matches_dependencies():
  data = build_phase63_3_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase63_3_derives_prop44_isomorphism():
  data = build_phase63_3_data()

  assert (
    data[
      "isomorphism_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase63_3_isomorphism_preserves_exact_map():
  data = build_phase63_3_data()

  assert (
    data[
      "isomorphism_step"
    ].conclusion.map
    is data[
      "decomposition_map"
    ]
  )


def test_phase63_3_provenance_uses_exactly_two_premises():
  data = build_phase63_3_data()

  assert (
    data[
      "isomorphism_step"
    ].premises
    == (
      data[
        "specialization_step"
      ],
      data[
        "decomposition_map_step"
      ],
    )
  )


def test_phase63_3_rejects_given_specialization():
  data = build_phase63_3_data()

  given_specialization_step = ProofStep(
    conclusion=(
      data[
        "specialization_step"
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
      given_specialization_step,
      data[
        "decomposition_map_step"
      ],
    ),
  ) is None


def test_phase63_3_rejects_wrong_first_summand():
  data = build_phase63_3_data()

  wrong_map = replace(
    data[
      "decomposition_map"
    ],
    source_group=DirectSumGroup(
      summands=(
        TodaPrimaryGroup(
          group_dimension=data[
            "i"
          ],
          sphere_dimension=3,
        ),
        data[
          "second_summand"
        ],
      ),
    ),
  )

  wrong_map_step = ProofStep(
    conclusion=wrong_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "specialization_step"
      ],
      wrong_map_step,
    ),
  ) is None


def test_phase63_3_rejects_wrong_second_summand():
  data = build_phase63_3_data()

  wrong_map = replace(
    data[
      "decomposition_map"
    ],
    source_group=DirectSumGroup(
      summands=(
        data[
          "first_summand"
        ],
        TodaPrimaryGroup(
          group_dimension=data[
            "i"
          ],
          sphere_dimension=8,
        ),
      ),
    ),
  )

  wrong_map_step = ProofStep(
    conclusion=wrong_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "specialization_step"
      ],
      wrong_map_step,
    ),
  ) is None


def test_phase63_3_rejects_wrong_target():
  data = build_phase63_3_data()

  wrong_map = replace(
    data[
      "decomposition_map"
    ],
    target_group=TodaPrimaryGroup(
      group_dimension=data[
        "i"
      ],
      sphere_dimension=5,
    ),
  )

  wrong_map_step = ProofStep(
    conclusion=wrong_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "specialization_step"
      ],
      wrong_map_step,
    ),
  ) is None


def test_phase63_3_rejects_wrong_alpha():
  data = build_phase63_3_data()

  wrong_alpha = HomotopyElement(
    name="ν₅",
    dimension=5,
    source=8,
    target=5,
    generator=GeneratorSymbol(
      family="ν",
      index=5,
    ),
  )

  wrong_map = replace(
    data[
      "decomposition_map"
    ],
    alpha=wrong_alpha,
  )

  wrong_map_step = ProofStep(
    conclusion=wrong_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "specialization_step"
      ],
      wrong_map_step,
    ),
  ) is None


def test_phase63_3_rejects_wrong_formula():
  data = build_phase63_3_data()

  wrong_map = replace(
    data[
      "decomposition_map"
    ],
    formula=Sum(
      left=Suspension(
        expression=data[
          "first_variable"
        ],
      ),
      right=Composition(
        left=data[
          "second_variable"
        ],
        right=data[
          "nu_4"
        ],
      ),
    ),
  )

  wrong_map_step = ProofStep(
    conclusion=wrong_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "specialization_step"
      ],
      wrong_map_step,
    ),
  ) is None


def test_phase63_3_rejects_concrete_i():
  data = build_phase63_3_data()

  concrete_first_variable = HomotopyElement(
    name="α",
    dimension=3,
    source=5,
    target=3,
  )

  concrete_second_variable = HomotopyElement(
    name="β",
    dimension=7,
    source=6,
    target=7,
  )

  concrete_map = TodaProp44DecompositionMap(
    source_group=DirectSumGroup(
      summands=(
        TodaPrimaryGroup(
          group_dimension=5,
          sphere_dimension=3,
        ),
        TodaPrimaryGroup(
          group_dimension=6,
          sphere_dimension=7,
        ),
      ),
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=4,
    ),
    alpha=data[
      "nu_4"
    ],
    beta=concrete_first_variable,
    gamma=concrete_second_variable,
    formula=Sum(
      left=Suspension(
        expression=concrete_first_variable,
      ),
      right=Composition(
        left=data[
          "nu_4"
        ],
        right=concrete_second_variable,
      ),
    ),
  )

  concrete_map_step = ProofStep(
    conclusion=concrete_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "specialization_step"
      ],
      concrete_map_step,
    ),
  ) is None


def test_phase63_3_final_result_is_not_given():
  data = build_phase63_3_data()

  assert (
    data[
      "isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "isomorphism_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase63_3_reaches_fixed_point_in_one_round():
  data = build_phase63_3_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    result.round_count
    == 1
  )

  assert (
    data[
      "isomorphism_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )


