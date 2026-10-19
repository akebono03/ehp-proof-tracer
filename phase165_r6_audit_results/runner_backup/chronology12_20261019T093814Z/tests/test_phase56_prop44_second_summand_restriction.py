from expression import (
  Composition,
  HomotopyElement,
  ScalarSum,
  Sum,
  Suspension,
)
from homotopy_groups import (
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
from test_phase56_prop44_eta2_specialization import (
  build_phase56_3_data,
)
from toda_rules import (
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  toda_prop44_eta2_second_summand_restriction_inference_rule,
)


def build_phase56_4_data():
  phase56_3 = (
    build_phase56_3_data()
  )

  isomorphism_step = (
    phase56_3[
      "isomorphism_steps"
    ][
      0
    ]
  )

  decomposition_map = (
    isomorphism_step
    .conclusion
    .map
  )

  expected_composition = (
    Composition(
      left=(
        decomposition_map.alpha
      ),
      right=(
        decomposition_map.gamma
      ),
    )
  )

  expected_statement = (
    TodaProp44SecondSummandRestrictionStatement(
      decomposition_map=(
        decomposition_map
      ),
      composition=(
        expected_composition
      ),
    )
  )

  rule = (
    toda_prop44_eta2_second_summand_restriction_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        isomorphism_step,
      ),
    )
  )

  restriction_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase56_3": phase56_3,
    "isomorphism_step": (
      isomorphism_step
    ),
    "decomposition_map": (
      decomposition_map
    ),
    "expected_composition": (
      expected_composition
    ),
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "result": result,
    "restriction_steps": (
      restriction_steps
    ),
  }


def test_phase56_4_second_summand_restriction_is_representable():
  data = build_phase56_4_data()

  assert isinstance(
    data[
      "expected_statement"
    ],
    TodaProp44SecondSummandRestrictionStatement,
  )

  assert (
    data[
      "expected_statement"
    ].decomposition_map
    == data[
      "decomposition_map"
    ]
  )

  assert (
    data[
      "expected_statement"
    ].composition
    == data[
      "expected_composition"
    ]
  )


def test_phase56_4_rule_matches_derived_eta2_specialization():
  data = build_phase56_4_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "isomorphism_step"
      ],
    ),
  ) is not None


def test_phase56_4_derives_second_summand_restriction():
  data = build_phase56_4_data()

  steps = data[
    "restriction_steps"
  ]

  assert len(
    steps
  ) == 1

  assert (
    steps[
      0
    ].conclusion
    == data[
      "expected_statement"
    ]
  )


def test_phase56_4_restriction_is_eta2_composition():
  data = build_phase56_4_data()

  restriction = (
    data[
      "restriction_steps"
    ][
      0
    ].conclusion
  )

  assert isinstance(
    restriction.composition,
    Composition,
  )

  assert (
    restriction.composition.left
    == data[
      "phase56_3"
    ][
      "eta_2"
    ]
  )

  assert (
    restriction.composition.right
    == data[
      "phase56_3"
    ][
      "gamma"
    ]
  )


def test_phase56_4_second_summand_is_pi_i_3():
  data = build_phase56_4_data()

  i = (
    data[
      "phase56_3"
    ][
      "i"
    ]
  )

  second_summand = (
    data[
      "decomposition_map"
    ]
    .source_group
    .summands[
      1
    ]
  )

  assert (
    second_summand
    == TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=3,
    )
  )


def test_phase56_4_target_is_pi_i_2():
  data = build_phase56_4_data()

  i = (
    data[
      "phase56_3"
    ][
      "i"
    ]
  )

  assert (
    data[
      "decomposition_map"
    ].target_group
    == TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=2,
    )
  )


def test_phase56_4_result_is_inference():
  data = build_phase56_4_data()

  step = (
    data[
      "restriction_steps"
    ][
      0
    ]
  )

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.inference_rule is not None

  assert (
    step.inference_rule.name
    == (
      "Toda Proposition 4.4 "
      "eta_2 second-summand restriction"
    )
  )


def test_phase56_4_preserves_phase56_3_provenance():
  data = build_phase56_4_data()

  step = (
    data[
      "restriction_steps"
    ][
      0
    ]
  )

  assert (
    step.premises
    == (
      data[
        "isomorphism_step"
      ],
    )
  )

  assert (
    data[
      "isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase56_4_rejects_given_isomorphism():
  data = build_phase56_4_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "isomorphism_step"
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


def test_phase56_4_rejects_wrong_alpha():
  data = build_phase56_4_data()

  decomposition_map = (
    data[
      "decomposition_map"
    ]
  )

  wrong_alpha = HomotopyElement(
    name="α",
    dimension=3,
    source=3,
    target=2,
  )

  wrong_map = TodaProp44DecompositionMap(
    source_group=(
      decomposition_map.source_group
    ),
    target_group=(
      decomposition_map.target_group
    ),
    alpha=wrong_alpha,
    beta=(
      decomposition_map.beta
    ),
    gamma=(
      decomposition_map.gamma
    ),
    formula=Sum(
      left=Suspension(
        expression=(
          decomposition_map.beta
        ),
      ),
      right=Composition(
        left=wrong_alpha,
        right=(
          decomposition_map.gamma
        ),
      ),
    ),
  )

  wrong_isomorphism_step = ProofStep(
    conclusion=(
      TodaProp44IsomorphismStatement(
        map=wrong_map,
      )
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_isomorphism_step,
    ),
  ) is None


def test_phase56_4_rejects_wrong_second_summand():
  data = build_phase56_4_data()

  phase56_3 = (
    data[
      "phase56_3"
    ]
  )

  decomposition_map = (
    data[
      "decomposition_map"
    ]
  )

  wrong_second_summand = (
    TodaPrimaryGroup(
      group_dimension=(
        phase56_3[
          "i"
        ]
      ),
      sphere_dimension=4,
    )
  )

  wrong_source_group = (
    decomposition_map
    .source_group
    .__class__(
      summands=(
        decomposition_map
        .source_group
        .summands[
          0
        ],
        wrong_second_summand,
      ),
    )
  )

  wrong_map = TodaProp44DecompositionMap(
    source_group=(
      wrong_source_group
    ),
    target_group=(
      decomposition_map.target_group
    ),
    alpha=(
      decomposition_map.alpha
    ),
    beta=(
      decomposition_map.beta
    ),
    gamma=(
      decomposition_map.gamma
    ),
    formula=(
      decomposition_map.formula
    ),
  )

  wrong_step = ProofStep(
    conclusion=(
      TodaProp44IsomorphismStatement(
        map=wrong_map,
      )
    ),
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


def test_phase56_4_rejects_wrong_formula():
  data = build_phase56_4_data()

  decomposition_map = (
    data[
      "decomposition_map"
    ]
  )

  wrong_map = TodaProp44DecompositionMap(
    source_group=(
      decomposition_map.source_group
    ),
    target_group=(
      decomposition_map.target_group
    ),
    alpha=(
      decomposition_map.alpha
    ),
    beta=(
      decomposition_map.beta
    ),
    gamma=(
      decomposition_map.gamma
    ),
    formula=Composition(
      left=(
        decomposition_map.alpha
      ),
      right=(
        decomposition_map.gamma
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=(
      TodaProp44IsomorphismStatement(
        map=wrong_map,
      )
    ),
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


def test_phase56_4_reaches_fixed_point_in_one_round():
  data = build_phase56_4_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert len(
    result.round_results[
      0
    ].new_steps
  ) == 1



