from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  ScalarSum,
  ScalarSymbol,
  Suspension,
  TodaBracket,
  Zero,
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
from test_phase57_lemma45_two_iota3 import (
  build_phase57_2_data,
)
from toda_rules import (
  TodaBracketMembershipStatement,
  TodaProp26HopfBracketConsequenceStatement,
  toda_prop26_lemma52_hopf_bracket_inference_rule,
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
from test_phase57_lemma45_two_iota3 import (
  build_phase57_2_data,
)
from toda_rules import (
  TodaBracketMembershipStatement,
  TodaProp26HopfBracketConsequenceStatement,
  toda_prop26_lemma52_hopf_bracket_inference_rule,
)


def build_phase57_3_data():
  phase57_2 = (
    build_phase57_2_data()
  )

  i = (
    phase57_2[
      "i"
    ]
  )

  i_plus_two = ScalarSum(
    left=i,
    right=2,
  )

  alpha = (
    phase57_2[
      "alpha"
    ]
  )

  beta = HomotopyElement(
    name="β",
    dimension=i_plus_two,
    source=i_plus_two,
    target=3,
  )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  iota_3 = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  bracket = TodaBracket(
    first=eta_3,
    second=Multiple(
      coefficient=2,
      expression=iota_4,
    ),
    third=Suspension(
      expression=alpha,
    ),
    index=1,
  )

  membership = (
    TodaBracketMembershipStatement(
      element=beta,
      bracket=bracket,
    )
  )

  first_zero = Relation(
    lhs=Suspension(
      expression=Composition(
        left=eta_2,
        right=Multiple(
          coefficient=2,
          expression=iota_3,
        ),
      ),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  membership_step = ProofStep(
    conclusion=membership,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_zero_step = ProofStep(
    conclusion=first_zero,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  phase57_2_result = (
    run_inference_until_stable_with_history(
      (
        phase57_2[
          "lemma45_rule"
        ],
        phase57_2[
          "zero_rule"
        ],
      ),
      (
        phase57_2[
          "membership_step"
        ],
        phase57_2[
          "two_alpha_zero_step"
        ],
      ),
    )
  )

  second_zero_step = next(
    step
    for step in phase57_2_result.steps
    if (
      step.conclusion
      == phase57_2[
        "final_zero"
      ]
    )
  )

  expected_statement = (
    TodaProp26HopfBracketConsequenceStatement(
      bracket_element=beta,
      bracket=bracket,
      delta_preimage_value=Composition(
        left=eta_2,
        right=Multiple(
          coefficient=2,
          expression=iota_3,
        ),
      ),
      right_factor=IteratedSuspension(
        expression=alpha,
        exponent=2,
      ),
      sign=-1,
    )
  )

  rule = (
    toda_prop26_lemma52_hopf_bracket_inference_rule()
  )

  premise_steps = (
    membership_step,
    first_zero_step,
    second_zero_step,
  )

  return {
    "phase57_2": phase57_2,
    "i": i,
    "i_plus_two": i_plus_two,
    "alpha": alpha,
    "beta": beta,
    "eta_2": eta_2,
    "eta_3": eta_3,
    "iota_3": iota_3,
    "iota_4": iota_4,
    "bracket": bracket,
    "membership": membership,
    "first_zero": first_zero,
    "membership_step": membership_step,
    "first_zero_step": first_zero_step,
    "second_zero_step": second_zero_step,
    "expected_statement": (
      expected_statement
    ),
    "premise_steps": premise_steps,
    "rule": rule,
  }


def test_phase57_3_prop26_consequence_is_representable():
  data = build_phase57_3_data()

  assert isinstance(
    data[
      "expected_statement"
    ],
    TodaProp26HopfBracketConsequenceStatement,
  )

  assert (
    data[
      "expected_statement"
    ].sign
    == -1
  )


def test_phase57_3_bracket_preserves_index_one():
  data = build_phase57_3_data()

  assert (
    data[
      "bracket"
    ].index
    == 1
  )


def test_phase57_3_bracket_has_expected_entries():
  data = build_phase57_3_data()

  assert (
    data[
      "bracket"
    ].first
    == data[
      "eta_3"
    ]
  )

  assert (
    data[
      "bracket"
    ].second
    == Multiple(
      coefficient=2,
      expression=data[
        "iota_4"
      ],
    )
  )

  assert (
    data[
      "bracket"
    ].third
    == Suspension(
      expression=data[
        "alpha"
      ],
    )
  )


def test_phase57_3_rule_matches_prop26_specialization():
  data = build_phase57_3_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase57_3_rule_derives_hopf_bracket_consequence():
  data = build_phase57_3_data()

  result = (
    run_inference_until_stable_with_history(
      data[
        "rule"
      ],
      data[
        "premise_steps"
      ],
    )
  )

  steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == data[
        "expected_statement"
      ]
    )
  )

  assert len(
    steps
  ) == 1


def test_phase57_3_conclusion_has_expected_delta_preimage_value():
  data = build_phase57_3_data()

  statement = (
    data[
      "expected_statement"
    ]
  )

  assert (
    statement.delta_preimage_value
    == Composition(
      left=data[
        "eta_2"
      ],
      right=Multiple(
        coefficient=2,
        expression=data[
          "iota_3"
        ],
      ),
    )
  )


def test_phase57_3_conclusion_has_e_squared_alpha():
  data = build_phase57_3_data()

  statement = (
    data[
      "expected_statement"
    ]
  )

  assert (
    statement.right_factor
    == IteratedSuspension(
      expression=data[
        "alpha"
      ],
      exponent=2,
    )
  )


def test_phase57_3_second_zero_is_derived_from_phase57_2():
  data = build_phase57_3_data()

  assert (
    data[
      "second_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "second_zero_step"
    ].conclusion
    == data[
      "phase57_2"
    ][
      "final_zero"
    ]
  )


def test_phase57_3_result_preserves_three_premises():
  data = build_phase57_3_data()

  result = (
    run_inference_until_stable_with_history(
      data[
        "rule"
      ],
      data[
        "premise_steps"
      ],
    )
  )

  step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == data[
        "expected_statement"
      ]
    )
  )

  assert (
    step.premises
    == data[
      "premise_steps"
    ]
  )


def test_phase57_3_rejects_wrong_index():
  data = build_phase57_3_data()

  wrong_membership_step = ProofStep(
    conclusion=(
      TodaBracketMembershipStatement(
        element=data[
          "beta"
        ],
        bracket=TodaBracket(
          first=data[
            "eta_3"
          ],
          second=Multiple(
            coefficient=2,
            expression=data[
              "iota_4"
            ],
          ),
          third=Suspension(
            expression=data[
              "alpha"
            ],
          ),
          index=2,
        ),
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_membership_step,
      data[
        "first_zero_step"
      ],
      data[
        "second_zero_step"
      ],
    ),
  ) is None


def test_phase57_3_rejects_wrong_second_entry():
  data = build_phase57_3_data()

  wrong_membership_step = ProofStep(
    conclusion=(
      TodaBracketMembershipStatement(
        element=data[
          "beta"
        ],
        bracket=TodaBracket(
          first=data[
            "eta_3"
          ],
          second=data[
            "iota_4"
          ],
          third=Suspension(
            expression=data[
              "alpha"
            ],
          ),
          index=1,
        ),
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_membership_step,
      data[
        "first_zero_step"
      ],
      data[
        "second_zero_step"
      ],
    ),
  ) is None


def test_phase57_3_rejects_given_second_zero():
  data = build_phase57_3_data()

  given_second_zero_step = ProofStep(
    conclusion=(
      data[
        "second_zero_step"
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
      data[
        "membership_step"
      ],
      data[
        "first_zero_step"
      ],
      given_second_zero_step,
    ),
  ) is None


def test_phase57_3_rejects_wrong_first_zero():
  data = build_phase57_3_data()

  wrong_first_zero_step = ProofStep(
    conclusion=Relation(
      lhs=Suspension(
        expression=data[
          "alpha"
        ],
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "membership_step"
      ],
      wrong_first_zero_step,
      data[
        "second_zero_step"
      ],
    ),
  ) is None


def test_phase57_3_reaches_fixed_point_in_one_round():
  data = build_phase57_3_data()

  result = (
    run_inference_until_stable_with_history(
      data[
        "rule"
      ],
      data[
        "premise_steps"
      ],
    )
  )

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



