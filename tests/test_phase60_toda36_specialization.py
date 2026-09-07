from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  Suspension,
  TodaBracket,
  Zero,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from probes.probe_phase55_capabilities import (
  build_phase55_representative_result,
)
from probes.probe_phase58_capabilities import (
  build_phase58_representative_result,
)
from test_phase60_toda54_t0_bridge import (
  build_phase60_5_data,
)
from toda_rules import (
  Toda36Lemma54SpecializationStatement,
  Toda54BracketUpToSignStatement,
  TodaBracketMembershipStatement,
  TodaLemma54DoubleSuspensionUpToSignStatement,
  toda_36_lemma54_specialization_inference_rule,
  toda_54_n5_t3_specialization_inference_rule,
  toda_lemma54_double_suspension_up_to_sign_inference_rule,
  toda_lemma54_eta6_twice_zero_inference_rule,
)


def build_phase60_6_data():
  phase55 = (
    build_phase55_representative_result()
  )

  phase58 = (
    build_phase58_representative_result()
  )

  phase60_5 = (
    build_phase60_5_data()
  )

  prop51_step = (
    phase55[
      "prop51_steps"
    ][
      0
    ]
  )

  two_eta3_zero_step = (
    phase58[
      "two_eta3_zero_step"
    ]
  )

  symbolic_toda54_step = (
    phase60_5[
      "indexed_step"
    ]
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

  eta_6 = HomotopyElement(
    name="η₆",
    dimension=6,
    source=7,
    target=6,
    generator=GeneratorSymbol(
      family="η",
      index=6,
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

  iota_6 = HomotopyElement(
    name="ι_6",
    dimension=6,
    generator=GeneratorSymbol(
      family="ι",
      index=6,
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

  alpha_star = HomotopyElement(
    name="α*",
    dimension=7,
    source=7,
    target=4,
  )

  expected_two_eta6_zero = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=eta_6,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  concrete_bracket = TodaBracket(
    first=eta_5,
    second=Multiple(
      coefficient=2,
      expression=iota_6,
    ),
    third=eta_6,
    index=3,
  )

  expected_alpha_star_membership = (
    HomotopyGroupMembershipStatement(
      element=alpha_star,
      group_dimension=7,
      sphere_dimension=4,
    )
  )

  expected_negative_membership = (
    TodaBracketMembershipStatement(
      element=Multiple(
        coefficient=-2,
        expression=Suspension(
          expression=alpha_star,
        ),
      ),
      bracket=concrete_bracket,
    )
  )

  expected_theorem36 = (
    Toda36Lemma54SpecializationStatement(
      alpha=eta_2,
      beta=Multiple(
        coefficient=2,
        expression=iota_3,
      ),
      alpha_star=alpha_star,
      alpha_star_membership=(
        expected_alpha_star_membership
      ),
      negative_bracket_membership=(
        expected_negative_membership
      ),
    )
  )

  expected_toda54 = (
    Toda54BracketUpToSignStatement(
      bracket=concrete_bracket,
      positive_value=IteratedSuspension(
        expression=nu_prime,
        exponent=2,
      ),
    )
  )

  expected_final = (
    TodaLemma54DoubleSuspensionUpToSignStatement(
      left=Multiple(
        coefficient=2,
        expression=Suspension(
          expression=alpha_star,
        ),
      ),
      positive_value=IteratedSuspension(
        expression=nu_prime,
        exponent=2,
      ),
    )
  )

  eta6_zero_rule = (
    toda_lemma54_eta6_twice_zero_inference_rule()
  )

  theorem36_rule = (
    toda_36_lemma54_specialization_inference_rule()
  )

  toda54_specialization_rule = (
    toda_54_n5_t3_specialization_inference_rule()
  )

  final_rule = (
    toda_lemma54_double_suspension_up_to_sign_inference_rule()
  )

  rules = (
    eta6_zero_rule,
    theorem36_rule,
    toda54_specialization_rule,
    final_rule,
  )

  premise_steps = (
    prop51_step,
    two_eta3_zero_step,
    symbolic_toda54_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  eta6_zero_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_two_eta6_zero
    )
  )

  theorem36_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_theorem36
    )
  )

  toda54_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_toda54
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_final
    )
  )

  return {
    "phase55": phase55,
    "phase58": phase58,
    "phase60_5": phase60_5,
    "prop51_step": prop51_step,
    "two_eta3_zero_step": (
      two_eta3_zero_step
    ),
    "symbolic_toda54_step": (
      symbolic_toda54_step
    ),
    "eta_2": eta_2,
    "eta_3": eta_3,
    "eta_5": eta_5,
    "eta_6": eta_6,
    "iota_3": iota_3,
    "iota_6": iota_6,
    "nu_prime": nu_prime,
    "alpha_star": alpha_star,
    "concrete_bracket": concrete_bracket,
    "expected_two_eta6_zero": (
      expected_two_eta6_zero
    ),
    "expected_alpha_star_membership": (
      expected_alpha_star_membership
    ),
    "expected_negative_membership": (
      expected_negative_membership
    ),
    "expected_theorem36": (
      expected_theorem36
    ),
    "expected_toda54": expected_toda54,
    "expected_final": expected_final,
    "eta6_zero_rule": eta6_zero_rule,
    "theorem36_rule": theorem36_rule,
    "toda54_specialization_rule": (
      toda54_specialization_rule
    ),
    "final_rule": final_rule,
    "premise_steps": premise_steps,
    "result": result,
    "eta6_zero_step": eta6_zero_step,
    "theorem36_step": theorem36_step,
    "toda54_step": toda54_step,
    "final_step": final_step,
  }


def test_phase60_6_reuses_derived_prop51():
  data = build_phase60_6_data()

  assert (
    data[
      "prop51_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_6_reuses_derived_two_eta3_zero():
  data = build_phase60_6_data()

  assert (
    data[
      "two_eta3_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_6_reuses_derived_symbolic_toda54():
  data = build_phase60_6_data()

  assert (
    data[
      "symbolic_toda54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_6_eta6_zero_rule_matches_prop51():
  data = build_phase60_6_data()

  assert find_inference_match(
    data[
      "eta6_zero_rule"
    ],
    (
      data[
        "prop51_step"
      ],
    ),
  ) is not None


def test_phase60_6_derives_two_eta6_zero():
  data = build_phase60_6_data()

  assert (
    data[
      "eta6_zero_step"
    ].conclusion
    == data[
      "expected_two_eta6_zero"
    ]
  )

  assert (
    data[
      "eta6_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_6_theorem36_rule_matches_required_zero_relations():
  data = build_phase60_6_data()

  assert find_inference_match(
    data[
      "theorem36_rule"
    ],
    (
      data[
        "prop51_step"
      ],
      data[
        "two_eta3_zero_step"
      ],
      data[
        "eta6_zero_step"
      ],
    ),
  ) is not None


def test_phase60_6_derives_theorem36_specialization():
  data = build_phase60_6_data()

  assert (
    data[
      "theorem36_step"
    ].conclusion
    == data[
      "expected_theorem36"
    ]
  )

  assert (
    data[
      "theorem36_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_6_alpha_star_is_in_pi7_4():
  data = build_phase60_6_data()

  assert (
    data[
      "theorem36_step"
    ].conclusion.alpha_star_membership
    == data[
      "expected_alpha_star_membership"
    ]
  )


def test_phase60_6_theorem36_uses_alpha_eta2_beta_two_iota3():
  data = build_phase60_6_data()

  statement = (
    data[
      "theorem36_step"
    ].conclusion
  )

  assert statement.alpha == data[
    "eta_2"
  ]

  assert (
    statement.beta
    == Multiple(
      coefficient=2,
      expression=data[
        "iota_3"
      ],
    )
  )


def test_phase60_6_theorem36_negative_bracket_membership():
  data = build_phase60_6_data()

  assert (
    data[
      "theorem36_step"
    ].conclusion
    .negative_bracket_membership
    == data[
      "expected_negative_membership"
    ]
  )


def test_phase60_6_toda54_specialization_rule_matches_symbolic_result():
  data = build_phase60_6_data()

  assert find_inference_match(
    data[
      "toda54_specialization_rule"
    ],
    (
      data[
        "symbolic_toda54_step"
      ],
    ),
  ) is not None


def test_phase60_6_derives_n5_t3_toda54_value_set():
  data = build_phase60_6_data()

  assert (
    data[
      "toda54_step"
    ].conclusion
    == data[
      "expected_toda54"
    ]
  )

  assert (
    data[
      "toda54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_6_concrete_toda54_value_is_e2_nu_prime():
  data = build_phase60_6_data()

  assert (
    data[
      "toda54_step"
    ].conclusion
    .positive_value
    == IteratedSuspension(
      expression=data[
        "nu_prime"
      ],
      exponent=2,
    )
  )


def test_phase60_6_final_rule_matches_two_derived_results():
  data = build_phase60_6_data()

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "theorem36_step"
      ],
      data[
        "toda54_step"
      ],
    ),
  ) is not None


def test_phase60_6_derives_double_suspension_up_to_sign():
  data = build_phase60_6_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_final"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_6_final_left_is_two_e_alpha_star():
  data = build_phase60_6_data()

  assert (
    data[
      "final_step"
    ].conclusion.left
    == Multiple(
      coefficient=2,
      expression=Suspension(
        expression=data[
          "alpha_star"
        ],
      ),
    )
  )


def test_phase60_6_final_value_is_e2_nu_prime():
  data = build_phase60_6_data()

  assert (
    data[
      "final_step"
    ].conclusion.positive_value
    == IteratedSuspension(
      expression=data[
        "nu_prime"
      ],
      exponent=2,
    )
  )


def test_phase60_6_final_provenance_uses_two_derived_results():
  data = build_phase60_6_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "theorem36_step"
      ],
      data[
        "toda54_step"
      ],
    )
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in data[
      "final_step"
    ].premises
  )


def test_phase60_6_final_result_is_not_given():
  data = build_phase60_6_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_final"
    ]
    not in initial_conclusions
  )


def test_phase60_6_reaches_fixed_point_in_three_rounds():
  data = build_phase60_6_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3

  assert (
    data[
      "eta6_zero_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "toda54_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "theorem36_step"
    ]
    in result.round_results[
      1
    ].new_steps
  )

  assert (
    data[
      "final_step"
    ]
    in result.round_results[
      2
    ].new_steps
  )



