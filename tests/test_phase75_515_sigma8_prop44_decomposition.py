from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  HomotopyElement,
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
from test_phase75_515_sigma8_prop44_specialization import (
  build_phase75_8e1_data,
)
from toda_rules import (
  Toda515Sigma8Prop44SpecializationStatement,
  TodaProp44IsomorphismStatement,
  toda_prop515_sigma8_prop44_isomorphism_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_8e2_data():
  phase75_8e1 = (
    build_phase75_8e1_data()
  )

  specialization_step = (
    phase75_8e1[
      "specialization_step"
    ]
  )

  sigma8 = (
    specialization_step
    .conclusion
    .alpha
  )

  pi14_7 = TodaPrimaryGroup(
    group_dimension=14,
    sphere_dimension=7,
  )

  pi15_15 = TodaPrimaryGroup(
    group_dimension=15,
    sphere_dimension=15,
  )

  pi15_8 = TodaPrimaryGroup(
    group_dimension=15,
    sphere_dimension=8,
  )

  source_group = DirectSumGroup(
    summands=(
      pi14_7,
      pi15_15,
    ),
  )

  first_variable = HomotopyElement(
    name="α",
    dimension=14,
  )

  second_variable = HomotopyElement(
    name="β",
    dimension=15,
  )

  formula = Sum(
    left=Suspension(
      expression=first_variable,
    ),
    right=Composition(
      left=sigma8,
      right=second_variable,
    ),
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=source_group,
      target_group=pi15_8,
      alpha=sigma8,
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

  rule = (
    toda_prop515_sigma8_prop44_isomorphism_inference_rule()
  )

  premise_steps = (
    specialization_step,
    decomposition_map_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      premise_steps,
    )
  )

  expected_isomorphism = (
    TodaProp44IsomorphismStatement(
      map=decomposition_map,
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
    "phase75_8e1": phase75_8e1,
    "specialization_step": (
      specialization_step
    ),
    "sigma8": sigma8,
    "pi14_7": pi14_7,
    "pi15_15": pi15_15,
    "pi15_8": pi15_8,
    "source_group": source_group,
    "first_variable": first_variable,
    "second_variable": second_variable,
    "formula": formula,
    "decomposition_map": (
      decomposition_map
    ),
    "decomposition_map_step": (
      decomposition_map_step
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "expected_isomorphism": (
      expected_isomorphism
    ),
    "isomorphism_step": (
      isomorphism_step
    ),
  }


def test_phase75_8e2_reuses_derived_specialization():
  data = build_phase75_8e2_data()

  assert isinstance(
    data[
      "specialization_step"
    ].conclusion,
    Toda515Sigma8Prop44SpecializationStatement,
  )

  assert (
    data[
      "specialization_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8e2_specialization_is_n8_sigma8():
  data = build_phase75_8e2_data()

  specialization = (
    data[
      "specialization_step"
    ].conclusion
  )

  assert (
    specialization.n
    == 8
  )

  assert (
    specialization.alpha
    == data[
      "sigma8"
    ]
  )


def test_phase75_8e2_decomposition_map_is_structural_given():
  data = build_phase75_8e2_data()

  assert isinstance(
    data[
      "decomposition_map_step"
    ].conclusion,
    TodaProp44DecompositionMap,
  )

  assert (
    data[
      "decomposition_map_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase75_8e2_source_is_pi14_7_direct_sum_pi15_15():
  data = build_phase75_8e2_data()

  assert (
    data[
      "decomposition_map"
    ].source_group
    == DirectSumGroup(
      summands=(
        TodaPrimaryGroup(
          group_dimension=14,
          sphere_dimension=7,
        ),
        TodaPrimaryGroup(
          group_dimension=15,
          sphere_dimension=15,
        ),
      ),
    )
  )


def test_phase75_8e2_first_summand_is_pi14_7():
  data = build_phase75_8e2_data()

  assert (
    data[
      "decomposition_map"
    ].source_group
    .summands[
      0
    ]
    == data[
      "pi14_7"
    ]
  )


def test_phase75_8e2_second_summand_is_pi15_15():
  data = build_phase75_8e2_data()

  assert (
    data[
      "decomposition_map"
    ].source_group
    .summands[
      1
    ]
    == data[
      "pi15_15"
    ]
  )


def test_phase75_8e2_second_summand_is_diagonal_group():
  data = build_phase75_8e2_data()

  group = (
    data[
      "pi15_15"
    ]
  )

  assert (
    group.group_dimension
    == group.sphere_dimension
    == 15
  )


def test_phase75_8e2_target_is_pi15_8():
  data = build_phase75_8e2_data()

  assert (
    data[
      "decomposition_map"
    ].target_group
    == TodaPrimaryGroup(
      group_dimension=15,
      sphere_dimension=8,
    )
  )


def test_phase75_8e2_target_is_critical_degree_group():
  data = build_phase75_8e2_data()

  target = (
    data[
      "decomposition_map"
    ].target_group
  )

  assert (
    target.group_dimension
    == (
      2
      * target.sphere_dimension
      - 1
    )
  )


def test_phase75_8e2_map_uses_same_sigma8():
  data = build_phase75_8e2_data()

  assert (
    data[
      "decomposition_map"
    ].alpha
    == data[
      "specialization_step"
    ].conclusion
    .alpha
  )


def test_phase75_8e2_first_variable_represents_pi14_7_input():
  data = build_phase75_8e2_data()

  assert (
    data[
      "decomposition_map"
    ].beta
    == data[
      "first_variable"
    ]
  )

  assert (
    data[
      "first_variable"
    ].dimension
    == 14
  )


def test_phase75_8e2_second_variable_represents_pi15_15_input():
  data = build_phase75_8e2_data()

  assert (
    data[
      "decomposition_map"
    ].gamma
    == data[
      "second_variable"
    ]
  )

  assert (
    data[
      "second_variable"
    ].dimension
    == 15
  )


def test_phase75_8e2_formula_is_e_alpha_plus_sigma8_beta():
  data = build_phase75_8e2_data()

  assert (
    data[
      "decomposition_map"
    ].formula
    == Sum(
      left=Suspension(
        expression=(
          data[
            "first_variable"
          ]
        ),
      ),
      right=Composition(
        left=(
          data[
            "sigma8"
          ]
        ),
        right=(
          data[
            "second_variable"
          ]
        ),
      ),
    )
  )


def test_phase75_8e2_derives_prop44_isomorphism():
  data = build_phase75_8e2_data()

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


def test_phase75_8e2_isomorphism_preserves_same_map():
  data = build_phase75_8e2_data()

  assert (
    data[
      "isomorphism_step"
    ].conclusion
    .map
    == data[
      "decomposition_map"
    ]
  )


def test_phase75_8e2_isomorphism_uses_exact_dependencies():
  data = build_phase75_8e2_data()

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


def test_phase75_8e2_isomorphism_not_present_initially():
  data = build_phase75_8e2_data()

  assert (
    data[
      "expected_isomorphism"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase75_8e2_rejects_given_specialization():
  data = build_phase75_8e2_data()

  given = ProofStep(
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
      given,
      data[
        "decomposition_map_step"
      ],
    ),
  ) is None


def test_phase75_8e2_rejects_wrong_first_summand():
  data = build_phase75_8e2_data()

  wrong_map = replace(
    data[
      "decomposition_map"
    ],
    source_group=DirectSumGroup(
      summands=(
        TodaPrimaryGroup(
          group_dimension=13,
          sphere_dimension=7,
        ),
        data[
          "pi15_15"
        ],
      ),
    ),
  )

  wrong_step = ProofStep(
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
      wrong_step,
    ),
  ) is None


def test_phase75_8e2_rejects_wrong_second_summand():
  data = build_phase75_8e2_data()

  wrong_map = replace(
    data[
      "decomposition_map"
    ],
    source_group=DirectSumGroup(
      summands=(
        data[
          "pi14_7"
        ],
        TodaPrimaryGroup(
          group_dimension=15,
          sphere_dimension=14,
        ),
      ),
    ),
  )

  wrong_step = ProofStep(
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
      wrong_step,
    ),
  ) is None


def test_phase75_8e2_rejects_reversed_source_summands():
  data = build_phase75_8e2_data()

  wrong_map = replace(
    data[
      "decomposition_map"
    ],
    source_group=DirectSumGroup(
      summands=(
        data[
          "pi15_15"
        ],
        data[
          "pi14_7"
        ],
      ),
    ),
  )

  wrong_step = ProofStep(
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
      wrong_step,
    ),
  ) is None


def test_phase75_8e2_rejects_wrong_target():
  data = build_phase75_8e2_data()

  wrong_map = replace(
    data[
      "decomposition_map"
    ],
    target_group=TodaPrimaryGroup(
      group_dimension=16,
      sphere_dimension=8,
    ),
  )

  wrong_step = ProofStep(
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
      wrong_step,
    ),
  ) is None


def test_phase75_8e2_rejects_wrong_sigma8():
  data = build_phase75_8e2_data()

  wrong_alpha = HomotopyElement(
    name="τ",
    dimension=8,
    source=15,
    target=8,
  )

  wrong_map = replace(
    data[
      "decomposition_map"
    ],
    alpha=wrong_alpha,
  )

  wrong_step = ProofStep(
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
      wrong_step,
    ),
  ) is None


def test_phase75_8e2_rejects_wrong_formula():
  data = build_phase75_8e2_data()

  wrong_formula = HomotopyElement(
    name="δ",
    dimension=15,
  )

  wrong_map = replace(
    data[
      "decomposition_map"
    ],
    formula=wrong_formula,
  )

  wrong_step = ProofStep(
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
      wrong_step,
    ),
  ) is None


def test_phase75_8e2_reaches_fixed_point():
  data = build_phase75_8e2_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


