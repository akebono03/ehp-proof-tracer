from functools import lru_cache

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarSum,
  ScalarSymbol,
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
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase60_toda36_specialization import (
  build_phase60_6_data,
)
from toda_rules import (
  TodaLemma55BracketContainsUpToSignStatement,
  toda_lemma55_alpha_star_bracket_inclusion_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase61_3_data():
  phase60_6 = (
    build_phase60_6_data()
  )

  theorem36_step = (
    phase60_6[
      "theorem36_step"
    ]
  )

  alpha_star = (
    theorem36_step
    .conclusion
    .alpha_star
  )

  m = ScalarSymbol(
    name="m",
  )

  t = ScalarSymbol(
    name="t",
  )

  t_plus_two = ScalarSum(
    left=t,
    right=2,
  )

  t_plus_three = ScalarSum(
    left=t,
    right=3,
  )

  t_plus_five = ScalarSum(
    left=t,
    right=5,
  )

  t_plus_six = ScalarSum(
    left=t,
    right=6,
  )

  m_plus_two = ScalarSum(
    left=m,
    right=2,
  )

  m_plus_three = ScalarSum(
    left=m,
    right=3,
  )

  beta = HomotopyElement(
    name="β",
    dimension=t_plus_two,
    source=t_plus_two,
    target=m,
  )

  beta_membership = (
    HomotopyGroupMembershipStatement(
      element=beta,
      group_dimension=t_plus_two,
      sphere_dimension=m,
    )
  )

  eta_t_plus_two = HomotopyElement(
    name="η_(t+2)",
    dimension=t_plus_two,
    source=t_plus_three,
    target=t_plus_two,
    generator=GeneratorSymbol(
      family="η",
      index=t_plus_two,
    ),
  )

  beta_eta_zero = Relation(
    lhs=Composition(
      left=beta,
      right=eta_t_plus_two,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  t_range = ScalarGreaterEqualStatement(
    left=t,
    right=1,
  )

  beta_membership_step = ProofStep(
    conclusion=beta_membership,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  beta_eta_zero_step = ProofStep(
    conclusion=beta_eta_zero,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  t_range_step = ProofStep(
    conclusion=t_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta_m_plus_two = HomotopyElement(
    name="η_(m+2)",
    dimension=m_plus_two,
    source=m_plus_three,
    target=m_plus_two,
    generator=GeneratorSymbol(
      family="η",
      index=m_plus_two,
    ),
  )

  eta_t_plus_five = HomotopyElement(
    name="η_(t+5)",
    dimension=t_plus_five,
    source=t_plus_six,
    target=t_plus_five,
    generator=GeneratorSymbol(
      family="η",
      index=t_plus_five,
    ),
  )

  expected_bracket = TodaBracket(
    first=eta_m_plus_two,
    second=IteratedSuspension(
      expression=beta,
      exponent=3,
    ),
    third=eta_t_plus_five,
    index=3,
  )

  expected_positive_value = Composition(
    left=IteratedSuspension(
      expression=beta,
      exponent=2,
    ),
    right=IteratedSuspension(
      expression=alpha_star,
      exponent=t,
    ),
  )

  expected_statement = (
    TodaLemma55BracketContainsUpToSignStatement(
      bracket=expected_bracket,
      positive_value=expected_positive_value,
    )
  )

  rule = (
    toda_lemma55_alpha_star_bracket_inclusion_inference_rule()
  )

  premise_steps = (
    theorem36_step,
    beta_membership_step,
    beta_eta_zero_step,
    t_range_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  inclusion_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase60_6": phase60_6,
    "theorem36_step": theorem36_step,
    "alpha_star": alpha_star,
    "m": m,
    "t": t,
    "t_plus_two": t_plus_two,
    "t_plus_three": t_plus_three,
    "t_plus_five": t_plus_five,
    "t_plus_six": t_plus_six,
    "m_plus_two": m_plus_two,
    "m_plus_three": m_plus_three,
    "beta": beta,
    "beta_membership": beta_membership,
    "beta_membership_step": (
      beta_membership_step
    ),
    "eta_t_plus_two": eta_t_plus_two,
    "beta_eta_zero": beta_eta_zero,
    "beta_eta_zero_step": (
      beta_eta_zero_step
    ),
    "t_range": t_range,
    "t_range_step": t_range_step,
    "eta_m_plus_two": eta_m_plus_two,
    "eta_t_plus_five": eta_t_plus_five,
    "expected_bracket": expected_bracket,
    "expected_positive_value": (
      expected_positive_value
    ),
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "inclusion_step": inclusion_step,
  }


def test_phase61_3_reuses_derived_alpha_star():
  data = build_phase61_3_data()

  assert (
    data[
      "theorem36_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "theorem36_step"
    ].conclusion.alpha_star
    == data[
      "alpha_star"
    ]
  )


def test_phase61_3_rule_matches_dependencies():
  data = build_phase61_3_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase61_3_derives_alpha_star_bracket_inclusion():
  data = build_phase61_3_data()

  step = data[
    "inclusion_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase61_3_bracket_has_index_three():
  data = build_phase61_3_data()

  assert (
    data[
      "inclusion_step"
    ].conclusion.bracket.index
    == 3
  )


def test_phase61_3_bracket_has_expected_entries():
  data = build_phase61_3_data()

  bracket = (
    data[
      "inclusion_step"
    ].conclusion.bracket
  )

  assert (
    bracket.first
    == data[
      "eta_m_plus_two"
    ]
  )

  assert (
    bracket.second
    == IteratedSuspension(
      expression=data[
        "beta"
      ],
      exponent=3,
    )
  )

  assert (
    bracket.third
    == data[
      "eta_t_plus_five"
    ]
  )


def test_phase61_3_positive_value_is_e2_beta_composed_with_et_alpha_star():
  data = build_phase61_3_data()

  assert (
    data[
      "inclusion_step"
    ].conclusion.positive_value
    == Composition(
      left=IteratedSuspension(
        expression=data[
          "beta"
        ],
        exponent=2,
      ),
      right=IteratedSuspension(
        expression=data[
          "alpha_star"
        ],
        exponent=data[
          "t"
        ],
      ),
    )
  )


def test_phase61_3_provenance_uses_exactly_four_premises():
  data = build_phase61_3_data()

  assert (
    data[
      "inclusion_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )


def test_phase61_3_rejects_given_alpha_star_statement():
  data = build_phase61_3_data()

  given_theorem36_step = ProofStep(
    conclusion=(
      data[
        "theorem36_step"
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
      given_theorem36_step,
      data[
        "beta_membership_step"
      ],
      data[
        "beta_eta_zero_step"
      ],
      data[
        "t_range_step"
      ],
    ),
  ) is None


def test_phase61_3_rejects_wrong_beta_group_dimension():
  data = build_phase61_3_data()

  wrong_membership = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=data[
          "beta"
        ],
        group_dimension=ScalarSum(
          left=data[
            "t"
          ],
          right=3,
        ),
        sphere_dimension=data[
          "m"
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
      data[
        "theorem36_step"
      ],
      wrong_membership,
      data[
        "beta_eta_zero_step"
      ],
      data[
        "t_range_step"
      ],
    ),
  ) is None


def test_phase61_3_rejects_wrong_beta_eta_zero_relation():
  data = build_phase61_3_data()

  wrong_eta = HomotopyElement(
    name="η_(t+3)",
    dimension=ScalarSum(
      left=data[
        "t"
      ],
      right=3,
    ),
    source=ScalarSum(
      left=data[
        "t"
      ],
      right=4,
    ),
    target=ScalarSum(
      left=data[
        "t"
      ],
      right=3,
    ),
    generator=GeneratorSymbol(
      family="η",
      index=ScalarSum(
        left=data[
          "t"
        ],
        right=3,
      ),
    ),
  )

  wrong_zero = ProofStep(
    conclusion=Relation(
      lhs=Composition(
        left=data[
          "beta"
        ],
        right=wrong_eta,
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
        "theorem36_step"
      ],
      data[
        "beta_membership_step"
      ],
      wrong_zero,
      data[
        "t_range_step"
      ],
    ),
  ) is None


def test_phase61_3_rejects_t_at_least_zero():
  data = build_phase61_3_data()

  wrong_range = ProofStep(
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
      "rule"
    ],
    (
      data[
        "theorem36_step"
      ],
      data[
        "beta_membership_step"
      ],
      data[
        "beta_eta_zero_step"
      ],
      wrong_range,
    ),
  ) is None


def test_phase61_3_final_result_is_not_given():
  data = build_phase61_3_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_statement"
    ]
    not in initial_conclusions
  )

  assert (
    data[
      "inclusion_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase61_3_reaches_fixed_point_in_one_round():
  data = build_phase61_3_data()

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
      "inclusion_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )


