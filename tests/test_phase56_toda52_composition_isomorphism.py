from expression import (
  Composition,
  ScalarSum,
)
from homotopy_groups import (
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase56_pi_i_minus_1_1_zero import (
  build_phase56_2_data,
)
from test_phase56_prop44_second_summand_restriction import (
  build_phase56_4_data,
)
from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  toda_52_eta2_composition_isomorphism_inference_rule,
)


def build_phase56_5_data():
  phase56_2 = (
    build_phase56_2_data()
  )

  phase56_4 = (
    build_phase56_4_data()
  )

  zero_step = (
    phase56_2[
      "zero_steps"
    ][
      0
    ]
  )

  isomorphism_step = (
    phase56_4[
      "isomorphism_step"
    ]
  )

  restriction_step = (
    phase56_4[
      "restriction_steps"
    ][
      0
    ]
  )

  decomposition_map = (
    isomorphism_step
    .conclusion
    .map
  )

  expected_statement = (
    Toda52CompositionIsomorphismStatement(
      source_group=(
        decomposition_map
        .source_group
        .summands[
          1
        ]
      ),
      target_group=(
        decomposition_map
        .target_group
      ),
      composition=(
        restriction_step
        .conclusion
        .composition
      ),
    )
  )

  premise_steps = (
    zero_step,
    isomorphism_step,
    restriction_step,
  )

  rule = (
    toda_52_eta2_composition_isomorphism_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  composition_isomorphism_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase56_2": phase56_2,
    "phase56_4": phase56_4,
    "zero_step": zero_step,
    "isomorphism_step": (
      isomorphism_step
    ),
    "restriction_step": (
      restriction_step
    ),
    "decomposition_map": (
      decomposition_map
    ),
    "premise_steps": premise_steps,
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "result": result,
    "composition_isomorphism_steps": (
      composition_isomorphism_steps
    ),
  }


def test_phase56_5_composition_isomorphism_is_representable():
  data = build_phase56_5_data()

  assert isinstance(
    data[
      "expected_statement"
    ],
    Toda52CompositionIsomorphismStatement,
  )


def test_phase56_5_rule_matches_three_derived_dependencies():
  data = build_phase56_5_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase56_5_derives_toda52_composition_isomorphism():
  data = build_phase56_5_data()

  steps = data[
    "composition_isomorphism_steps"
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


def test_phase56_5_source_is_pi_i_3():
  data = build_phase56_5_data()

  i = (
    data[
      "phase56_4"
    ][
      "phase56_3"
    ][
      "i"
    ]
  )

  statement = (
    data[
      "composition_isomorphism_steps"
    ][
      0
    ].conclusion
  )

  assert (
    statement.source_group
    == TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=3,
    )
  )


def test_phase56_5_target_is_pi_i_2():
  data = build_phase56_5_data()

  i = (
    data[
      "phase56_4"
    ][
      "phase56_3"
    ][
      "i"
    ]
  )

  statement = (
    data[
      "composition_isomorphism_steps"
    ][
      0
    ].conclusion
  )

  assert (
    statement.target_group
    == TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=2,
    )
  )


def test_phase56_5_map_is_eta2_composition():
  data = build_phase56_5_data()

  statement = (
    data[
      "composition_isomorphism_steps"
    ][
      0
    ].conclusion
  )

  assert isinstance(
    statement.composition,
    Composition,
  )

  assert (
    statement.composition.left
    == data[
      "phase56_4"
    ][
      "phase56_3"
    ][
      "eta_2"
    ]
  )

  assert (
    statement.composition.right
    == data[
      "phase56_4"
    ][
      "phase56_3"
    ][
      "gamma"
    ]
  )


def test_phase56_5_zero_statement_matches_first_summand():
  data = build_phase56_5_data()

  first_summand = (
    data[
      "decomposition_map"
    ]
    .source_group
    .summands[
      0
    ]
  )

  assert (
    data[
      "zero_step"
    ].conclusion
    == TodaPrimaryGroupZeroStatement(
      group=first_summand,
    )
  )


def test_phase56_5_zero_statement_encodes_i_at_least_3_dependency():
  data = build_phase56_5_data()

  i = (
    data[
      "phase56_4"
    ][
      "phase56_3"
    ][
      "i"
    ]
  )

  assert (
    data[
      "zero_step"
    ].conclusion.group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=-1,
      ),
      sphere_dimension=1,
    )
  )

  assert (
    data[
      "zero_step"
    ].premises
    == (
      data[
        "phase56_2"
      ][
        "premise_step"
      ],
    )
  )


def test_phase56_5_result_is_inference():
  data = build_phase56_5_data()

  step = (
    data[
      "composition_isomorphism_steps"
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
      "Toda 5.2 eta_2 "
      "composition isomorphism"
    )
  )


def test_phase56_5_preserves_three_derived_premises():
  data = build_phase56_5_data()

  step = (
    data[
      "composition_isomorphism_steps"
    ][
      0
    ]
  )

  assert (
    step.premises
    == data[
      "premise_steps"
    ]
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in step.premises
  )


def test_phase56_5_rejects_given_zero_statement():
  data = build_phase56_5_data()

  given_zero_step = ProofStep(
    conclusion=(
      data[
        "zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  steps = (
    given_zero_step,
    data[
      "isomorphism_step"
    ],
    data[
      "restriction_step"
    ],
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    steps,
  ) is None


def test_phase56_5_rejects_given_isomorphism():
  data = build_phase56_5_data()

  given_isomorphism_step = ProofStep(
    conclusion=(
      data[
        "isomorphism_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  steps = (
    data[
      "zero_step"
    ],
    given_isomorphism_step,
    data[
      "restriction_step"
    ],
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    steps,
  ) is None


def test_phase56_5_rejects_given_restriction():
  data = build_phase56_5_data()

  given_restriction_step = ProofStep(
    conclusion=(
      data[
        "restriction_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  steps = (
    data[
      "zero_step"
    ],
    data[
      "isomorphism_step"
    ],
    given_restriction_step,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    steps,
  ) is None


def test_phase56_5_rejects_zero_for_wrong_first_summand():
  data = build_phase56_5_data()

  i = (
    data[
      "phase56_4"
    ][
      "phase56_3"
    ][
      "i"
    ]
  )

  wrong_zero_step = ProofStep(
    conclusion=(
      TodaPrimaryGroupZeroStatement(
        group=TodaPrimaryGroup(
          group_dimension=i,
          sphere_dimension=1,
        ),
      )
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  steps = (
    wrong_zero_step,
    data[
      "isomorphism_step"
    ],
    data[
      "restriction_step"
    ],
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    steps,
  ) is None


def test_phase56_5_rejects_restriction_with_wrong_composition():
  data = build_phase56_5_data()

  restriction = (
    data[
      "restriction_step"
    ].conclusion
  )

  wrong_restriction_step = ProofStep(
    conclusion=(
      TodaProp44SecondSummandRestrictionStatement(
        decomposition_map=(
          restriction.decomposition_map
        ),
        composition=Composition(
          left=(
            data[
              "phase56_4"
            ][
              "phase56_3"
            ][
              "eta_2"
            ]
          ),
          right=(
            data[
              "phase56_4"
            ][
              "phase56_3"
            ][
              "beta"
            ]
          ),
        ),
      )
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  steps = (
    data[
      "zero_step"
    ],
    data[
      "isomorphism_step"
    ],
    wrong_restriction_step,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    steps,
  ) is None


def test_phase56_5_reaches_fixed_point_in_one_round():
  data = build_phase56_5_data()

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




