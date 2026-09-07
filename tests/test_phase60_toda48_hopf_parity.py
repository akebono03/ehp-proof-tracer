from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
  Multiple,
  ScalarSymbol,
  Suspension,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_H_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase60_toda36_specialization import (
  build_phase60_6_data,
)
from toda_rules import (
  TodaLemma54HopfOddMultipleStatement,
  toda_48_lemma54_hopf_odd_multiple_inference_rule,
  toda_lemma54_pi6_5_finite_cyclic_inference_rule,
)


def build_phase60_7_data():
  phase60_6 = (
    build_phase60_6_data()
  )

  prop51_step = (
    phase60_6[
      "prop51_step"
    ]
  )

  final_double_step = (
    phase60_6[
      "final_step"
    ]
  )

  theorem36_step = (
    phase60_6[
      "theorem36_step"
    ]
  )

  phase58 = (
    phase60_6[
      "phase58"
    ]
  )

  nu_prime_hopf_step = (
    phase58[
      "final_hopf_step"
    ]
  )

  alpha_star = (
    phase60_6[
      "alpha_star"
    ]
  )

  nu_prime = (
    phase60_6[
      "nu_prime"
    ]
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

  iota_7 = HomotopyElement(
    name="ι_7",
    dimension=7,
    generator=GeneratorSymbol(
      family="ι",
      index=7,
    ),
  )

  s = ScalarSymbol(
    name="s",
  )

  expected_pi6_5 = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=5,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_5,
    ),
    relation_type=RelationType.EQUALITY,
  )

  expected_hopf = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=nu_prime,
    ),
    rhs=eta_5,
    relation_type=RelationType.EQUALITY,
  )

  expected_double_left = Multiple(
    coefficient=2,
    expression=Suspension(
      expression=alpha_star,
    ),
  )

  expected_double_value = (
    IteratedSuspension(
      expression=nu_prime,
      exponent=2,
    )
  )

  expected_final = (
    TodaLemma54HopfOddMultipleStatement(
      alpha_star=alpha_star,
      parameter=s,
      generator=iota_7,
    )
  )

  pi6_5_rule = (
    toda_lemma54_pi6_5_finite_cyclic_inference_rule()
  )

  hopf_parity_rule = (
    toda_48_lemma54_hopf_odd_multiple_inference_rule()
  )

  rules = (
    pi6_5_rule,
    hopf_parity_rule,
  )

  premise_steps = (
    prop51_step,
    theorem36_step,
    final_double_step,
    nu_prime_hopf_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  pi6_5_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_pi6_5
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
    "phase60_6": phase60_6,
    "phase58": phase58,
    "prop51_step": prop51_step,
    "theorem36_step": theorem36_step,
    "final_double_step": (
      final_double_step
    ),
    "nu_prime_hopf_step": (
      nu_prime_hopf_step
    ),
    "alpha_star": alpha_star,
    "nu_prime": nu_prime,
    "eta_5": eta_5,
    "iota_7": iota_7,
    "s": s,
    "expected_pi6_5": (
      expected_pi6_5
    ),
    "expected_hopf": expected_hopf,
    "expected_double_left": (
      expected_double_left
    ),
    "expected_double_value": (
      expected_double_value
    ),
    "expected_final": expected_final,
    "pi6_5_rule": pi6_5_rule,
    "hopf_parity_rule": (
      hopf_parity_rule
    ),
    "premise_steps": premise_steps,
    "result": result,
    "pi6_5_step": pi6_5_step,
    "final_step": final_step,
  }


def test_phase60_7_reuses_derived_prop51():
  data = build_phase60_7_data()

  assert (
    data[
      "prop51_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_7_reuses_derived_theorem36_specialization():
  data = build_phase60_7_data()

  assert (
    data[
      "theorem36_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_7_reuses_derived_double_suspension_relation():
  data = build_phase60_7_data()

  assert (
    data[
      "final_double_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_7_reuses_derived_nu_prime_hopf_relation():
  data = build_phase60_7_data()

  assert (
    data[
      "nu_prime_hopf_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "nu_prime_hopf_step"
    ].conclusion
    == data[
      "expected_hopf"
    ]
  )


def test_phase60_7_pi6_5_rule_matches_prop51():
  data = build_phase60_7_data()

  assert find_inference_match(
    data[
      "pi6_5_rule"
    ],
    (
      data[
        "prop51_step"
      ],
    ),
  ) is not None


def test_phase60_7_derives_pi6_5_order_two_eta5():
  data = build_phase60_7_data()

  step = data[
    "pi6_5_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_pi6_5"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase60_7_pi6_5_generator_is_eta5():
  data = build_phase60_7_data()

  group = (
    data[
      "pi6_5_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert group.order == 2

  assert (
    group.generator
    == data[
      "eta_5"
    ]
  )


def test_phase60_7_double_statement_has_expected_left():
  data = build_phase60_7_data()

  assert (
    data[
      "final_double_step"
    ].conclusion.left
    == data[
      "expected_double_left"
    ]
  )


def test_phase60_7_double_statement_has_e2_nu_prime_value():
  data = build_phase60_7_data()

  assert (
    data[
      "final_double_step"
    ].conclusion
    .positive_value
    == data[
      "expected_double_value"
    ]
  )


def test_phase60_7_parity_rule_matches_all_derived_dependencies():
  data = build_phase60_7_data()

  assert find_inference_match(
    data[
      "hopf_parity_rule"
    ],
    (
      data[
        "theorem36_step"
      ],
      data[
        "final_double_step"
      ],
      data[
        "nu_prime_hopf_step"
      ],
      data[
        "pi6_5_step"
      ],
    ),
  ) is not None


def test_phase60_7_derives_hopf_odd_multiple_statement():
  data = build_phase60_7_data()

  step = data[
    "final_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_final"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase60_7_hopf_statement_preserves_alpha_star():
  data = build_phase60_7_data()

  assert (
    data[
      "final_step"
    ].conclusion.alpha_star
    == data[
      "alpha_star"
    ]
  )


def test_phase60_7_hopf_statement_uses_symbolic_s():
  data = build_phase60_7_data()

  parameter = (
    data[
      "final_step"
    ].conclusion.parameter
  )

  assert isinstance(
    parameter,
    ScalarSymbol,
  )

  assert parameter.name == "s"


def test_phase60_7_hopf_statement_generator_is_iota7():
  data = build_phase60_7_data()

  assert (
    data[
      "final_step"
    ].conclusion.generator
    == data[
      "iota_7"
    ]
  )


def test_phase60_7_hopf_statement_means_two_s_plus_one_iota7():
  data = build_phase60_7_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement
    == TodaLemma54HopfOddMultipleStatement(
      alpha_star=data[
        "alpha_star"
      ],
      parameter=ScalarSymbol(
        name="s",
      ),
      generator=data[
        "iota_7"
      ],
    )
  )


def test_phase60_7_final_provenance_uses_four_derived_premises():
  data = build_phase60_7_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "theorem36_step"
      ],
      data[
        "final_double_step"
      ],
      data[
        "nu_prime_hopf_step"
      ],
      data[
        "pi6_5_step"
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


def test_phase60_7_final_result_is_not_given():
  data = build_phase60_7_data()

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


def test_phase60_7_reaches_fixed_point_in_two_rounds():
  data = build_phase60_7_data()

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
      "pi6_5_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "final_step"
    ]
    in result.round_results[
      1
    ].new_steps
  )


