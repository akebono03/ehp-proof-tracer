from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  TodaBracket,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_rules import (
  Toda53NuPrimeBracketSpecializationStatement,
  TodaBracketMembershipStatement,
  toda_53_nu_prime_bracket_specialization_inference_rule,
  toda_54_nu_prime_bracket_inclusion_inference_rule,
)


def build_phase60_4_data():
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

  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
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

  source_bracket = TodaBracket(
    first=eta_3,
    second=Multiple(
      coefficient=2,
      expression=iota_4,
    ),
    third=eta_4,
    index=1,
  )

  source_membership = (
    TodaBracketMembershipStatement(
      element=nu_prime,
      bracket=source_bracket,
    )
  )

  source_membership_step = ProofStep(
    conclusion=source_membership,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  n = ScalarSymbol(
    name="n",
  )

  t = ScalarSymbol(
    name="t",
  )

  n_range = ScalarGreaterEqualStatement(
    left=n,
    right=3,
  )

  t_lower_range = ScalarGreaterEqualStatement(
    left=t,
    right=1,
  )

  t_upper_range = ScalarGreaterEqualStatement(
    left=ScalarSum(
      left=n,
      right=-2,
    ),
    right=t,
  )

  n_range_step = ProofStep(
    conclusion=n_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  t_lower_range_step = ProofStep(
    conclusion=t_lower_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  t_upper_range_step = ProofStep(
    conclusion=t_upper_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )

  n_plus_two = ScalarSum(
    left=n,
    right=2,
  )

  eta_n = HomotopyElement(
    name="η_n",
    dimension=n,
    source=n_plus_one,
    target=n,
    generator=GeneratorSymbol(
      family="η",
      index=n,
    ),
  )

  eta_n_plus_one = HomotopyElement(
    name="η_(n+1)",
    dimension=n_plus_one,
    source=n_plus_two,
    target=n_plus_one,
    generator=GeneratorSymbol(
      family="η",
      index=n_plus_one,
    ),
  )

  iota_n_plus_one = HomotopyElement(
    name="ι_(n+1)",
    dimension=n_plus_one,
    generator=GeneratorSymbol(
      family="ι",
      index=n_plus_one,
    ),
  )

  target_bracket = TodaBracket(
    first=eta_n,
    second=Multiple(
      coefficient=2,
      expression=iota_n_plus_one,
    ),
    third=eta_n_plus_one,
    index=t,
  )

  suspended_nu_prime = IteratedSuspension(
    expression=nu_prime,
    exponent=ScalarSum(
      left=n,
      right=ScalarProduct(
        left=-1,
        right=3,
      ),
    ),
  )

  expected_membership = (
    TodaBracketMembershipStatement(
      element=suspended_nu_prime,
      bracket=target_bracket,
    )
  )

  specialization_rule = (
    toda_53_nu_prime_bracket_specialization_inference_rule()
  )

  inclusion_rule = (
    toda_54_nu_prime_bracket_inclusion_inference_rule()
  )

  rules = (
    specialization_rule,
    inclusion_rule,
  )

  premise_steps = (
    source_membership_step,
    n_range_step,
    t_lower_range_step,
    t_upper_range_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  specialization_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      Toda53NuPrimeBracketSpecializationStatement,
    )
  )

  inclusion_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_membership
    )
  )

  return {
    "eta_3": eta_3,
    "iota_4": iota_4,
    "eta_4": eta_4,
    "nu_prime": nu_prime,
    "source_bracket": source_bracket,
    "source_membership": source_membership,
    "source_membership_step": (
      source_membership_step
    ),
    "n": n,
    "t": t,
    "n_range": n_range,
    "t_lower_range": t_lower_range,
    "t_upper_range": t_upper_range,
    "n_range_step": n_range_step,
    "t_lower_range_step": (
      t_lower_range_step
    ),
    "t_upper_range_step": (
      t_upper_range_step
    ),
    "eta_n": eta_n,
    "eta_n_plus_one": eta_n_plus_one,
    "iota_n_plus_one": iota_n_plus_one,
    "target_bracket": target_bracket,
    "suspended_nu_prime": (
      suspended_nu_prime
    ),
    "expected_membership": (
      expected_membership
    ),
    "specialization_rule": (
      specialization_rule
    ),
    "inclusion_rule": inclusion_rule,
    "premise_steps": premise_steps,
    "result": result,
    "specialization_step": (
      specialization_step
    ),
    "inclusion_step": inclusion_step,
  }


def test_phase60_4_source_is_toda53_nu_prime_bracket():
  data = build_phase60_4_data()

  membership = data[
    "source_membership"
  ]

  assert (
    membership.element
    == data[
      "nu_prime"
    ]
  )

  assert (
    membership.bracket
    == data[
      "source_bracket"
    ]
  )

  assert membership.bracket.index == 1


def test_phase60_4_source_specialization_is_derived():
  data = build_phase60_4_data()

  step = data[
    "specialization_step"
  ]

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    step.conclusion,
    Toda53NuPrimeBracketSpecializationStatement,
  )


def test_phase60_4_scope_is_n_at_least_3():
  data = build_phase60_4_data()

  assert (
    data[
      "n_range"
    ]
    == ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=3,
    )
  )


def test_phase60_4_scope_is_t_at_least_1():
  data = build_phase60_4_data()

  assert (
    data[
      "t_lower_range"
    ]
    == ScalarGreaterEqualStatement(
      left=data[
        "t"
      ],
      right=1,
    )
  )


def test_phase60_4_scope_is_t_at_most_n_minus_2():
  data = build_phase60_4_data()

  assert (
    data[
      "t_upper_range"
    ]
    == ScalarGreaterEqualStatement(
      left=ScalarSum(
        left=data[
          "n"
        ],
        right=-2,
      ),
      right=data[
        "t"
      ],
    )
  )


def test_phase60_4_rule_matches_derived_specialization_and_scope():
  data = build_phase60_4_data()

  assert find_inference_match(
    data[
      "inclusion_rule"
    ],
    (
      data[
        "specialization_step"
      ],
      data[
        "n_range_step"
      ],
      data[
        "t_lower_range_step"
      ],
      data[
        "t_upper_range_step"
      ],
    ),
  ) is not None


def test_phase60_4_derives_suspended_nu_prime_membership():
  data = build_phase60_4_data()

  step = data[
    "inclusion_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_membership"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase60_4_element_is_e_n_minus_3_nu_prime():
  data = build_phase60_4_data()

  element = (
    data[
      "inclusion_step"
    ].conclusion.element
  )

  assert isinstance(
    element,
    IteratedSuspension,
  )

  assert (
    element.expression
    == data[
      "nu_prime"
    ]
  )

  assert (
    element.exponent
    == ScalarSum(
      left=data[
        "n"
      ],
      right=ScalarProduct(
        left=-1,
        right=3,
      ),
    )
  )


def test_phase60_4_target_bracket_has_expected_entries():
  data = build_phase60_4_data()

  bracket = (
    data[
      "inclusion_step"
    ].conclusion.bracket
  )

  assert (
    bracket.first
    == data[
      "eta_n"
    ]
  )

  assert (
    bracket.second
    == Multiple(
      coefficient=2,
      expression=data[
        "iota_n_plus_one"
      ],
    )
  )

  assert (
    bracket.third
    == data[
      "eta_n_plus_one"
    ]
  )


def test_phase60_4_target_bracket_preserves_t():
  data = build_phase60_4_data()

  assert (
    data[
      "inclusion_step"
    ].conclusion.bracket.index
    == data[
      "t"
    ]
  )


def test_phase60_4_provenance_uses_specialization_and_scope():
  data = build_phase60_4_data()

  assert (
    data[
      "inclusion_step"
    ].premises
    == (
      data[
        "specialization_step"
      ],
      data[
        "n_range_step"
      ],
      data[
        "t_lower_range_step"
      ],
      data[
        "t_upper_range_step"
      ],
    )
  )


def test_phase60_4_rejects_given_specialization():
  data = build_phase60_4_data()

  given_step = ProofStep(
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
      "inclusion_rule"
    ],
    (
      given_step,
      data[
        "n_range_step"
      ],
      data[
        "t_lower_range_step"
      ],
      data[
        "t_upper_range_step"
      ],
    ),
  ) is None


def test_phase60_4_rejects_n_at_least_2():
  data = build_phase60_4_data()

  wrong_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=2,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "inclusion_rule"
    ],
    (
      data[
        "specialization_step"
      ],
      wrong_step,
      data[
        "t_lower_range_step"
      ],
      data[
        "t_upper_range_step"
      ],
    ),
  ) is None


def test_phase60_4_rejects_t_at_least_0():
  data = build_phase60_4_data()

  wrong_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=data[
        "t"
      ],
      right=0,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "inclusion_rule"
    ],
    (
      data[
        "specialization_step"
      ],
      data[
        "n_range_step"
      ],
      wrong_step,
      data[
        "t_upper_range_step"
      ],
    ),
  ) is None


def test_phase60_4_rejects_wrong_upper_t_scope():
  data = build_phase60_4_data()

  wrong_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=ScalarSum(
        left=data[
          "n"
        ],
        right=-1,
      ),
      right=data[
        "t"
      ],
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "inclusion_rule"
    ],
    (
      data[
        "specialization_step"
      ],
      data[
        "n_range_step"
      ],
      data[
        "t_lower_range_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase60_4_final_result_is_not_given():
  data = build_phase60_4_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_membership"
    ]
    not in initial_conclusions
  )

  assert (
    data[
      "inclusion_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase60_4_reaches_fixed_point_in_two_rounds():
  data = build_phase60_4_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    result.round_count
    == 2
  )

  assert (
    data[
      "specialization_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "inclusion_step"
    ]
    in result.round_results[
      1
    ].new_steps
  )


