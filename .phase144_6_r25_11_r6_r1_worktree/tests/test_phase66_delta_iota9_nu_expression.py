from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaPrimaryGroup,
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
from test_phase66_expression_sign_compatibility import (
  build_phase66_2_data,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  toda_58_delta_iota9_nu4_nu_prime_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase66_3_data():
  phase66_2 = (
    build_phase66_2_data()
  )

  pi7_4_step = (
    phase66_2[
      "phase65_5"
    ][
      "final_step"
    ]
  )

  rule = (
    toda_58_delta_iota9_nu4_nu_prime_inference_rule()
  )

  premise_steps = (
    pi7_4_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  expected_statement = (
    TodaDeltaImageUpToSignStatement(
      map=phase66_2[
        "delta_map"
      ],
      element=phase66_2[
        "iota_9"
      ],
      positive_value=phase66_2[
        "expression"
      ],
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase66_2": phase66_2,
    "pi7_4_step": pi7_4_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "expected_statement": (
      expected_statement
    ),
    "final_step": final_step,
  }


def test_phase66_3_reuses_derived_pi7_4():
  data = build_phase66_3_data()

  assert (
    data[
      "pi7_4_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase66_3_pi7_4_has_expected_decomposition():
  data = build_phase66_3_data()

  phase66_2 = data[
    "phase66_2"
  ]

  assert (
    data[
      "pi7_4_step"
    ].conclusion
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=4,
      ),
      rhs=DirectSumGroup(
        summands=(
          FreeCyclicGroup(
            generator=phase66_2[
              "nu_4"
            ],
          ),
          FiniteCyclicGroup(
            order=4,
            generator=phase66_2[
              "e_nu_prime"
            ],
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase66_3_rule_matches_derived_pi7_4():
  data = build_phase66_3_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase66_3_derives_delta_iota9_statement():
  data = build_phase66_3_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase66_3_delta_source_is_pi9_9():
  data = build_phase66_3_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement.map.source_group
    == TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=9,
    )
  )


def test_phase66_3_delta_target_is_pi7_4():
  data = build_phase66_3_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement.map.target_group
    == TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
    )
  )


def test_phase66_3_delta_map_is_expected_instance():
  data = build_phase66_3_data()

  assert (
    data[
      "final_step"
    ].conclusion.map
    == TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=9,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=4,
      ),
    )
  )


def test_phase66_3_argument_is_iota9():
  data = build_phase66_3_data()

  assert (
    data[
      "final_step"
    ].conclusion.element
    == HomotopyElement(
      name="ι_9",
      dimension=9,
      generator=GeneratorSymbol(
        family="ι",
        index=9,
      ),
    )
  )


def test_phase66_3_positive_value_is_two_nu4_minus_e_nu_prime():
  data = build_phase66_3_data()

  phase66_2 = data[
    "phase66_2"
  ]

  assert (
    data[
      "final_step"
    ].conclusion.positive_value
    == Sum(
      left=Multiple(
        coefficient=2,
        expression=phase66_2[
          "nu_4"
        ],
      ),
      right=Multiple(
        coefficient=-1,
        expression=Suspension(
          expression=phase66_2[
            "nu_prime"
          ],
        ),
      ),
    )
  )


def test_phase66_3_positive_value_reuses_phase66_2_expression():
  data = build_phase66_3_data()

  assert (
    data[
      "final_step"
    ].conclusion.positive_value
    == data[
      "phase66_2"
    ][
      "expression"
    ]
  )


def test_phase66_3_preserves_nu4_object():
  data = build_phase66_3_data()

  positive_value = (
    data[
      "final_step"
    ].conclusion
    .positive_value
  )

  assert (
    positive_value.left.expression
    is data[
      "phase66_2"
    ][
      "nu_4"
    ]
  )


def test_phase66_3_preserves_e_nu_prime_object():
  data = build_phase66_3_data()

  positive_value = (
    data[
      "final_step"
    ].conclusion
    .positive_value
  )

  pi7_4_e_nu_prime = (
    data[
      "pi7_4_step"
    ].conclusion
    .rhs
    .summands[
      1
    ]
    .generator
  )

  assert (
    positive_value.right.expression
    is pi7_4_e_nu_prime
  )

  assert (
    positive_value.right.expression
    == data[
      "phase66_2"
    ][
      "e_nu_prime"
    ]
  )


def test_phase66_3_provenance_uses_only_pi7_4():
  data = build_phase66_3_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi7_4_step"
      ],
    )
  )


def test_phase66_3_rejects_given_pi7_4():
  data = build_phase66_3_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "pi7_4_step"
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


def test_phase66_3_rejects_wrong_target_group():
  data = build_phase66_3_data()

  wrong_relation = replace(
    data[
      "pi7_4_step"
    ].conclusion,
    lhs=TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=5,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
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


def test_phase66_3_rejects_wrong_nu4_generator():
  data = build_phase66_3_data()

  phase66_2 = data[
    "phase66_2"
  ]

  wrong_nu_4 = HomotopyElement(
    name="ν₅",
    dimension=5,
    source=8,
    target=5,
    generator=GeneratorSymbol(
      family="ν",
      index=5,
    ),
  )

  wrong_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
    ),
    rhs=DirectSumGroup(
      summands=(
        FreeCyclicGroup(
          generator=wrong_nu_4,
        ),
        FiniteCyclicGroup(
          order=4,
          generator=phase66_2[
            "e_nu_prime"
          ],
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
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


def test_phase66_3_rejects_wrong_nu_prime_order():
  data = build_phase66_3_data()

  phase66_2 = data[
    "phase66_2"
  ]

  wrong_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
    ),
    rhs=DirectSumGroup(
      summands=(
        FreeCyclicGroup(
          generator=phase66_2[
            "nu_4"
          ],
        ),
        FiniteCyclicGroup(
          order=8,
          generator=phase66_2[
            "e_nu_prime"
          ],
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
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


def test_phase66_3_final_result_is_not_given():
  data = build_phase66_3_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "expected_statement"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase66_3_reaches_fixed_point_in_one_round():
  data = build_phase66_3_data()

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
      "final_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )


