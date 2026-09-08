from dataclasses import replace

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  ScalarSum,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase63_prop44_decomposition_specialization import (
  build_phase63_3_data,
)
from toda_rules import (
  Toda56Nu4DecompositionIsomorphismStatement,
  toda_56_nu4_decomposition_isomorphism_inference_rule,
)


def build_phase63_4_data():
  phase63_3 = (
    build_phase63_3_data()
  )

  prop44_isomorphism_step = (
    phase63_3[
      "isomorphism_step"
    ]
  )

  expected_statement = (
    Toda56Nu4DecompositionIsomorphismStatement(
      prop44_isomorphism=(
        prop44_isomorphism_step
        .conclusion
      ),
    )
  )

  rule = (
    toda_56_nu4_decomposition_isomorphism_inference_rule()
  )

  premise_steps = (
    prop44_isomorphism_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  toda56_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase63_3": phase63_3,
    "prop44_isomorphism_step": (
      prop44_isomorphism_step
    ),
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "toda56_step": toda56_step,
  }


def test_phase63_4_reuses_derived_prop44_isomorphism():
  data = build_phase63_4_data()

  assert (
    data[
      "prop44_isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase63_4_rule_matches_derived_prop44_isomorphism():
  data = build_phase63_4_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase63_4_derives_toda56_statement():
  data = build_phase63_4_data()

  assert (
    data[
      "toda56_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "toda56_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase63_4_preserves_exact_prop44_isomorphism():
  data = build_phase63_4_data()

  assert (
    data[
      "toda56_step"
    ].conclusion.prop44_isomorphism
    is data[
      "prop44_isomorphism_step"
    ].conclusion
  )


def test_phase63_4_source_is_pi_i_minus_one_3_plus_pi_i_7():
  data = build_phase63_4_data()

  decomposition_map = (
    data[
      "toda56_step"
    ]
    .conclusion
    .prop44_isomorphism
    .map
  )

  i = (
    data[
      "phase63_3"
    ][
      "i"
    ]
  )

  assert (
    decomposition_map.source_group
    == DirectSumGroup(
      summands=(
        TodaPrimaryGroup(
          group_dimension=ScalarSum(
            left=i,
            right=-1,
          ),
          sphere_dimension=3,
        ),
        TodaPrimaryGroup(
          group_dimension=i,
          sphere_dimension=7,
        ),
      ),
    )
  )


def test_phase63_4_target_is_pi_i_4():
  data = build_phase63_4_data()

  decomposition_map = (
    data[
      "toda56_step"
    ]
    .conclusion
    .prop44_isomorphism
    .map
  )

  i = (
    data[
      "phase63_3"
    ][
      "i"
    ]
  )

  assert (
    decomposition_map.target_group
    == TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=4,
    )
  )


def test_phase63_4_alpha_is_nu4():
  data = build_phase63_4_data()

  decomposition_map = (
    data[
      "toda56_step"
    ]
    .conclusion
    .prop44_isomorphism
    .map
  )

  nu_4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  assert (
    decomposition_map.alpha
    == nu_4
  )


def test_phase63_4_formula_is_e_alpha_plus_nu4_beta():
  data = build_phase63_4_data()

  decomposition_map = (
    data[
      "toda56_step"
    ]
    .conclusion
    .prop44_isomorphism
    .map
  )

  assert (
    decomposition_map.formula
    == Sum(
      left=Suspension(
        expression=(
          decomposition_map.beta
        ),
      ),
      right=Composition(
        left=(
          decomposition_map.alpha
        ),
        right=(
          decomposition_map.gamma
        ),
      ),
    )
  )


def test_phase63_4_provenance_uses_exactly_prop44_isomorphism():
  data = build_phase63_4_data()

  assert (
    data[
      "toda56_step"
    ].premises
    == (
      data[
        "prop44_isomorphism_step"
      ],
    )
  )


def test_phase63_4_rejects_given_prop44_isomorphism():
  data = build_phase63_4_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "prop44_isomorphism_step"
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
      given_step,
    ),
  ) is None


def test_phase63_4_rejects_wrong_first_summand():
  data = build_phase63_4_data()

  phase63_3 = (
    data[
      "phase63_3"
    ]
  )

  original_isomorphism = (
    data[
      "prop44_isomorphism_step"
    ].conclusion
  )

  original_map = (
    original_isomorphism.map
  )

  wrong_map = replace(
    original_map,
    source_group=DirectSumGroup(
      summands=(
        TodaPrimaryGroup(
          group_dimension=(
            phase63_3[
              "i"
            ]
          ),
          sphere_dimension=3,
        ),
        phase63_3[
          "second_summand"
        ],
      ),
    ),
  )

  wrong_isomorphism = replace(
    original_isomorphism,
    map=wrong_map,
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
      wrong_step,
    ),
  ) is None


def test_phase63_4_rejects_wrong_second_summand():
  data = build_phase63_4_data()

  phase63_3 = (
    data[
      "phase63_3"
    ]
  )

  original_isomorphism = (
    data[
      "prop44_isomorphism_step"
    ].conclusion
  )

  original_map = (
    original_isomorphism.map
  )

  wrong_map = replace(
    original_map,
    source_group=DirectSumGroup(
      summands=(
        phase63_3[
          "first_summand"
        ],
        TodaPrimaryGroup(
          group_dimension=(
            phase63_3[
              "i"
            ]
          ),
          sphere_dimension=8,
        ),
      ),
    ),
  )

  wrong_isomorphism = replace(
    original_isomorphism,
    map=wrong_map,
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
      wrong_step,
    ),
  ) is None


def test_phase63_4_rejects_wrong_target():
  data = build_phase63_4_data()

  phase63_3 = (
    data[
      "phase63_3"
    ]
  )

  original_isomorphism = (
    data[
      "prop44_isomorphism_step"
    ].conclusion
  )

  wrong_map = replace(
    original_isomorphism.map,
    target_group=TodaPrimaryGroup(
      group_dimension=(
        phase63_3[
          "i"
        ]
      ),
      sphere_dimension=5,
    ),
  )

  wrong_isomorphism = replace(
    original_isomorphism,
    map=wrong_map,
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
      wrong_step,
    ),
  ) is None


def test_phase63_4_rejects_wrong_nu4():
  data = build_phase63_4_data()

  original_isomorphism = (
    data[
      "prop44_isomorphism_step"
    ].conclusion
  )

  wrong_nu = HomotopyElement(
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
    original_isomorphism.map,
    alpha=wrong_nu,
  )

  wrong_isomorphism = replace(
    original_isomorphism,
    map=wrong_map,
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
      wrong_step,
    ),
  ) is None


def test_phase63_4_rejects_wrong_formula():
  data = build_phase63_4_data()

  original_isomorphism = (
    data[
      "prop44_isomorphism_step"
    ].conclusion
  )

  original_map = (
    original_isomorphism.map
  )

  wrong_map = replace(
    original_map,
    formula=Sum(
      left=Suspension(
        expression=(
          original_map.beta
        ),
      ),
      right=Composition(
        left=(
          original_map.gamma
        ),
        right=(
          original_map.alpha
        ),
      ),
    ),
  )

  wrong_isomorphism = replace(
    original_isomorphism,
    map=wrong_map,
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
      wrong_step,
    ),
  ) is None


def test_phase63_4_final_result_is_not_given():
  data = build_phase63_4_data()

  assert (
    data[
      "toda56_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "toda56_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase63_4_reaches_fixed_point_in_one_round():
  data = build_phase63_4_data()

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
      "toda56_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )


