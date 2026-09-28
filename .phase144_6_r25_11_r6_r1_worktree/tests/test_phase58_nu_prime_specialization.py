from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  TodaBracket,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  Toda53NuPrimeBracketSpecializationStatement,
  TodaBracketMembershipStatement,
  toda_53_nu_prime_bracket_specialization_inference_rule,
)


def build_phase58_2_data():
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

  eta_4 = HomotopyElement(
    name="η₄",
    dimension=4,
    source=5,
    target=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
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

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  bracket = TodaBracket(
    first=eta_3,
    second=Multiple(
      coefficient=2,
      expression=iota_4,
    ),
    third=eta_4,
    index=1,
  )

  membership = (
    TodaBracketMembershipStatement(
      element=nu_prime,
      bracket=bracket,
    )
  )

  membership_step = ProofStep(
    conclusion=membership,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  expected_statement = (
    Toda53NuPrimeBracketSpecializationStatement(
      nu_prime=nu_prime,
      alpha=eta_3,
      lemma52_index=4,
      bracket_membership=membership,
    )
  )

  rule = (
    toda_53_nu_prime_bracket_specialization_inference_rule()
  )

  return {
    "eta_3": eta_3,
    "eta_4": eta_4,
    "iota_4": iota_4,
    "nu_prime": nu_prime,
    "bracket": bracket,
    "membership": membership,
    "membership_step": membership_step,
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
  }


def test_phase58_2_nu_prime_preserves_existing_generator_identity():
  data = build_phase58_2_data()

  assert (
    data[
      "nu_prime"
    ].generator
    == GeneratorSymbol(
      family="ν",
      decoration="′",
    )
  )


def test_phase58_2_nu_prime_has_pi6_s3_typing():
  data = build_phase58_2_data()

  nu_prime = data[
    "nu_prime"
  ]

  assert nu_prime.dimension == 3
  assert nu_prime.source == 6
  assert nu_prime.target == 3


def test_phase58_2_bracket_membership_is_representable():
  data = build_phase58_2_data()

  assert (
    data[
      "membership"
    ]
    == TodaBracketMembershipStatement(
      element=data[
        "nu_prime"
      ],
      bracket=data[
        "bracket"
      ],
    )
  )


def test_phase58_2_bracket_has_expected_entries():
  data = build_phase58_2_data()

  bracket = data[
    "bracket"
  ]

  assert (
    bracket.first
    == data[
      "eta_3"
    ]
  )

  assert bracket.second == Multiple(
    coefficient=2,
    expression=data[
      "iota_4"
    ],
  )

  assert (
    bracket.third
    == data[
      "eta_4"
    ]
  )

  assert bracket.index == 1


def test_phase58_2_specialization_rule_matches_expected_membership():
  data = build_phase58_2_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "membership_step"
      ],
    ),
  ) is not None


def test_phase58_2_specialization_rule_derives_alpha_eta3_i4_instance():
  data = build_phase58_2_data()

  result = (
    run_inference_until_stable_with_history(
      data[
        "rule"
      ],
      (
        data[
          "membership_step"
        ],
      ),
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

  statement = (
    steps[
      0
    ].conclusion
  )

  assert (
    statement.alpha
    == data[
      "eta_3"
    ]
  )

  assert statement.lemma52_index == 4


def test_phase58_2_specialization_preserves_membership_provenance():
  data = build_phase58_2_data()

  result = (
    run_inference_until_stable_with_history(
      data[
        "rule"
      ],
      (
        data[
          "membership_step"
        ],
      ),
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

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.premises == (
    data[
      "membership_step"
    ],
  )

  assert (
    step.inference_rule
    == data[
      "rule"
    ]
  )


def test_phase58_2_rejects_plain_nu_generator():
  data = build_phase58_2_data()

  wrong_nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
    ),
  )

  wrong_step = ProofStep(
    conclusion=(
      TodaBracketMembershipStatement(
        element=wrong_nu_prime,
        bracket=data[
          "bracket"
        ],
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
      wrong_step,
    ),
  ) is None


def test_phase58_2_rejects_wrong_bracket_index():
  data = build_phase58_2_data()

  wrong_bracket = TodaBracket(
    first=data[
      "eta_3"
    ],
    second=Multiple(
      coefficient=2,
      expression=data[
        "iota_4"
      ],
    ),
    third=data[
      "eta_4"
    ],
    index=2,
  )

  wrong_step = ProofStep(
    conclusion=(
      TodaBracketMembershipStatement(
        element=data[
          "nu_prime"
        ],
        bracket=wrong_bracket,
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
      wrong_step,
    ),
  ) is None


def test_phase58_2_rejects_wrong_third_entry():
  data = build_phase58_2_data()

  eta_5 = HomotopyElement(
    name="η₅",
    dimension=5,
    source=6,
    target=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )

  wrong_bracket = TodaBracket(
    first=data[
      "eta_3"
    ],
    second=Multiple(
      coefficient=2,
      expression=data[
        "iota_4"
      ],
    ),
    third=eta_5,
    index=1,
  )

  wrong_step = ProofStep(
    conclusion=(
      TodaBracketMembershipStatement(
        element=data[
          "nu_prime"
        ],
        bracket=wrong_bracket,
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
      wrong_step,
    ),
  ) is None


def test_phase58_2_reaches_fixed_point_in_one_round():
  data = build_phase58_2_data()

  result = (
    run_inference_until_stable_with_history(
      data[
        "rule"
      ],
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

  assert result.round_count == 1

  assert len(
    result.round_results[
      0
    ].new_steps
  ) == 1


