from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  ScalarSum,
  Suspension,
  TodaBracket,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase57_prop26_hopf_bracket import (
  build_phase57_3_data,
)
from toda_rules import (
  TodaLemma52BracketCompositionMembershipStatement,
  TodaLemma52BracketRepresentativeStatement,
  toda_cor37_lemma52_representative_inference_rule,
  toda_prop13_lemma52_bracket_transformation_inference_rule,
  toda_prop14_lemma52_bracket_transformation_inference_rule,
)


def build_phase57_5_data():
  phase57_3 = (
    build_phase57_3_data()
  )

  alpha = (
    phase57_3[
      "alpha"
    ]
  )

  beta = (
    phase57_3[
      "beta"
    ]
  )

  i = alpha.dimension

  membership_step = (
    phase57_3[
      "membership_step"
    ]
  )

  prop14_rule = (
    toda_prop14_lemma52_bracket_transformation_inference_rule()
  )

  prop14_result = (
    run_inference_until_stable_with_history(
      prop14_rule,
      (
        membership_step,
      ),
    )
  )

  prop14_steps = tuple(
    step
    for step in prop14_result.steps
    if isinstance(
      step.conclusion,
      TodaLemma52BracketCompositionMembershipStatement,
    )
  )

  prop14_step = prop14_steps[
    0
  ]

  prop13_rule = (
    toda_prop13_lemma52_bracket_transformation_inference_rule()
  )

  prop13_result = (
    run_inference_until_stable_with_history(
      prop13_rule,
      (
        prop14_step,
      ),
    )
  )

  prop13_steps = tuple(
    step
    for step in prop13_result.steps
    if isinstance(
      step.conclusion,
      TodaLemma52BracketCompositionMembershipStatement,
    )
    and (
      step.conclusion.bracket_sign
      == -1
    )
  )

  prop13_step = prop13_steps[
    0
  ]

  cor37_rule = (
    toda_cor37_lemma52_representative_inference_rule()
  )

  cor37_result = (
    run_inference_until_stable_with_history(
      cor37_rule,
      (
        prop13_step,
      ),
    )
  )

  representative_steps = tuple(
    step
    for step in cor37_result.steps
    if isinstance(
      step.conclusion,
      TodaLemma52BracketRepresentativeStatement,
    )
  )

  representative_step = (
    representative_steps[
      0
    ]
  )

  i_plus_one = ScalarSum(
    left=i,
    right=1,
  )

  i_plus_two = ScalarSum(
    left=i,
    right=2,
  )

  eta_i_plus_one = HomotopyElement(
    name="η_(i+1)",
    dimension=i_plus_one,
    source=i_plus_two,
    target=i_plus_one,
    generator=GeneratorSymbol(
      family="η",
      index=i_plus_one,
    ),
  )

  expected_representative = Composition(
    left=phase57_3[
      "eta_3"
    ],
    right=Multiple(
      coefficient=-1,
      expression=Composition(
        left=Suspension(
          expression=alpha,
        ),
        right=eta_i_plus_one,
      ),
    ),
  )

  return {
    "phase57_3": phase57_3,
    "alpha": alpha,
    "beta": beta,
    "i": i,
    "membership_step": membership_step,
    "prop14_rule": prop14_rule,
    "prop14_result": prop14_result,
    "prop14_step": prop14_step,
    "prop13_rule": prop13_rule,
    "prop13_result": prop13_result,
    "prop13_step": prop13_step,
    "cor37_rule": cor37_rule,
    "cor37_result": cor37_result,
    "representative_step": (
      representative_step
    ),
    "expected_representative": (
      expected_representative
    ),
  }


def test_phase57_5_prop14_rule_matches_lemma52_bracket():
  data = build_phase57_5_data()

  assert find_inference_match(
    data[
      "prop14_rule"
    ],
    (
      data[
        "membership_step"
      ],
    ),
  ) is not None


def test_phase57_5_prop14_derives_twice_beta_membership():
  data = build_phase57_5_data()

  statement = (
    data[
      "prop14_step"
    ].conclusion
  )

  assert statement.element == Multiple(
    coefficient=2,
    expression=data[
      "beta"
    ],
  )

  assert (
    statement.bracket_sign
    == 1
  )

  assert (
    statement.bracket_suspension_exponent
    == 1
  )


def test_phase57_5_prop14_inner_bracket_is_expected():
  data = build_phase57_5_data()

  statement = (
    data[
      "prop14_step"
    ].conclusion
  )

  iota_3 = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  iota_i = HomotopyElement(
    name="ι_i",
    dimension=data[
      "i"
    ],
    generator=GeneratorSymbol(
      family="ι",
      index=data[
        "i"
      ],
    ),
  )

  assert statement.bracket == TodaBracket(
    first=Multiple(
      coefficient=2,
      expression=iota_3,
    ),
    second=data[
      "alpha"
    ],
    third=Multiple(
      coefficient=2,
      expression=iota_i,
    ),
  )


def test_phase57_5_prop14_result_is_inference():
  data = build_phase57_5_data()

  assert (
    data[
      "prop14_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "prop14_step"
    ].premises
    == (
      data[
        "membership_step"
      ],
    )
  )


def test_phase57_5_prop13_rule_matches_prop14_result():
  data = build_phase57_5_data()

  assert find_inference_match(
    data[
      "prop13_rule"
    ],
    (
      data[
        "prop14_step"
      ],
    ),
  ) is not None


def test_phase57_5_prop13_derives_negative_index_one_bracket():
  data = build_phase57_5_data()

  statement = (
    data[
      "prop13_step"
    ].conclusion
  )

  assert (
    statement.bracket_sign
    == -1
  )

  assert (
    statement.bracket_suspension_exponent
    == 0
  )

  assert (
    statement.bracket.index
    == 1
  )


def test_phase57_5_prop13_target_has_expected_entries():
  data = build_phase57_5_data()

  statement = (
    data[
      "prop13_step"
    ].conclusion
  )

  i_plus_one = ScalarSum(
    left=data[
      "i"
    ],
    right=1,
  )

  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  iota_i_plus_one = HomotopyElement(
    name="ι_(i+1)",
    dimension=i_plus_one,
    generator=GeneratorSymbol(
      family="ι",
      index=i_plus_one,
    ),
  )

  assert (
    statement.bracket.first
    == Multiple(
      coefficient=2,
      expression=iota_4,
    )
  )

  assert (
    statement.bracket.second
    == Suspension(
      expression=data[
        "alpha"
      ],
    )
  )

  assert (
    statement.bracket.third
    == Multiple(
      coefficient=2,
      expression=iota_i_plus_one,
    )
  )


def test_phase57_5_prop13_preserves_prop14_provenance():
  data = build_phase57_5_data()

  assert (
    data[
      "prop13_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "prop13_step"
    ].premises
    == (
      data[
        "prop14_step"
      ],
    )
  )


def test_phase57_5_cor37_rule_matches_prop13_result():
  data = build_phase57_5_data()

  assert find_inference_match(
    data[
      "cor37_rule"
    ],
    (
      data[
        "prop13_step"
      ],
    ),
  ) is not None


def test_phase57_5_cor37_derives_expected_signed_representative():
  data = build_phase57_5_data()

  statement = (
    data[
      "representative_step"
    ].conclusion
  )

  assert (
    statement.representative
    == data[
      "expected_representative"
    ]
  )


def test_phase57_5_cor37_preserves_prop13_membership():
  data = build_phase57_5_data()

  statement = (
    data[
      "representative_step"
    ].conclusion
  )

  assert (
    statement.membership
    == data[
      "prop13_step"
    ].conclusion
  )


def test_phase57_5_cor37_result_is_inference():
  data = build_phase57_5_data()

  step = (
    data[
      "representative_step"
    ]
  )

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.premises == (
    data[
      "prop13_step"
    ],
  )


def test_phase57_5_prop13_rejects_given_prop14_statement():
  data = build_phase57_5_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "prop14_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "prop13_rule"
    ],
    (
      given_step,
    ),
  ) is None


def test_phase57_5_cor37_rejects_given_prop13_statement():
  data = build_phase57_5_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "prop13_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "cor37_rule"
    ],
    (
      given_step,
    ),
  ) is None


def test_phase57_5_prop14_rejects_wrong_index():
  data = build_phase57_5_data()

  source = (
    data[
      "phase57_3"
    ]
  )

  wrong_step = ProofStep(
    conclusion=(
      source[
        "membership"
      ].__class__(
        element=data[
          "beta"
        ],
        bracket=TodaBracket(
          first=source[
            "eta_3"
          ],
          second=Multiple(
            coefficient=2,
            expression=source[
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
      "prop14_rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase57_5_full_chain_reaches_expected_representative():
  data = build_phase57_5_data()

  rules = (
    data[
      "prop14_rule"
    ],
    data[
      "prop13_rule"
    ],
    data[
      "cor37_rule"
    ],
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        data[
          "membership_step"
        ],
      ),
    )
  )

  representative_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaLemma52BracketRepresentativeStatement,
    )
  )

  assert len(
    representative_steps
  ) == 1

  assert (
    representative_steps[
      0
    ].conclusion.representative
    == data[
      "expected_representative"
    ]
  )


def test_phase57_5_full_chain_reaches_fixed_point():
  data = build_phase57_5_data()

  result = (
    run_inference_until_stable_with_history(
      (
        data[
          "prop14_rule"
        ],
        data[
          "prop13_rule"
        ],
        data[
          "cor37_rule"
        ],
      ),
      (
        data[
          "membership_step"
        ],
      ),
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3


