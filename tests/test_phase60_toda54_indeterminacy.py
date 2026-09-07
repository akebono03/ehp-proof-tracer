from expression import (
  Composition,
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
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from probes.probe_phase58_capabilities import (
  build_phase58_representative_result,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase59_prop53_integration import (
  build_phase59_8_data,
)
from toda_rules import (
  Toda54IndeterminacyGeneratorStatement,
  TodaProp53FiniteDimensionalStatement,
  toda_54_indeterminacy_double_nu_prime_generator_inference_rule,
  toda_54_nu_prime_triple_eta_transport_inference_rule,
  toda_54_t_ge_1_indeterminacy_eta_cube_inference_rule,
)


def build_phase60_3_data():
  phase58 = (
    build_phase58_representative_result()
  )

  phase59 = (
    build_phase59_8_data()
  )

  prop53_step = (
    phase59[
      "integration_step"
    ]
  )

  nu_prime_double_step = (
    phase58[
      "final_double_step"
    ]
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

  t_range = ScalarGreaterEqualStatement(
    left=t,
    right=1,
  )

  n_range_step = ProofStep(
    conclusion=n_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  t_range_step = ProofStep(
    conclusion=t_range,
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

  eta_n_plus_two = HomotopyElement(
    name="η_(n+2)",
    dimension=n_plus_two,
    source=ScalarSum(
      left=n,
      right=3,
    ),
    target=n_plus_two,
    generator=GeneratorSymbol(
      family="η",
      index=n_plus_two,
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

  bracket = TodaBracket(
    first=eta_n,
    second=Multiple(
      coefficient=2,
      expression=iota_n_plus_one,
    ),
    third=eta_n_plus_one,
    index=t,
  )

  eta_cube = Composition(
    left=eta_n,
    right=Composition(
      left=eta_n_plus_one,
      right=eta_n_plus_two,
    ),
  )

  nu_prime = (
    phase58[
      "nu_prime"
    ]
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

  double_suspended_nu_prime = Multiple(
    coefficient=2,
    expression=suspended_nu_prime,
  )

  expected_eta_indeterminacy = (
    Toda54IndeterminacyGeneratorStatement(
      bracket=bracket,
      generator=eta_cube,
    )
  )

  expected_transport = Relation(
    lhs=double_suspended_nu_prime,
    rhs=eta_cube,
    relation_type=RelationType.EQUALITY,
  )

  expected_final_indeterminacy = (
    Toda54IndeterminacyGeneratorStatement(
      bracket=bracket,
      generator=double_suspended_nu_prime,
    )
  )

  indeterminacy_rule = (
    toda_54_t_ge_1_indeterminacy_eta_cube_inference_rule()
  )

  transport_rule = (
    toda_54_nu_prime_triple_eta_transport_inference_rule()
  )

  generator_bridge_rule = (
    toda_54_indeterminacy_double_nu_prime_generator_inference_rule()
  )

  rules = (
    indeterminacy_rule,
    transport_rule,
    generator_bridge_rule,
  )

  premise_steps = (
    prop53_step,
    nu_prime_double_step,
    n_range_step,
    t_range_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  eta_indeterminacy_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_eta_indeterminacy
    )
  )

  transport_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_transport
    )
  )

  final_indeterminacy_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_final_indeterminacy
    )
  )

  return {
    "phase58": phase58,
    "phase59": phase59,
    "prop53_step": prop53_step,
    "nu_prime_double_step": (
      nu_prime_double_step
    ),
    "n": n,
    "t": t,
    "n_range": n_range,
    "t_range": t_range,
    "n_range_step": n_range_step,
    "t_range_step": t_range_step,
    "eta_n": eta_n,
    "eta_n_plus_one": (
      eta_n_plus_one
    ),
    "eta_n_plus_two": (
      eta_n_plus_two
    ),
    "iota_n_plus_one": (
      iota_n_plus_one
    ),
    "bracket": bracket,
    "eta_cube": eta_cube,
    "nu_prime": nu_prime,
    "suspended_nu_prime": (
      suspended_nu_prime
    ),
    "double_suspended_nu_prime": (
      double_suspended_nu_prime
    ),
    "expected_eta_indeterminacy": (
      expected_eta_indeterminacy
    ),
    "expected_transport": (
      expected_transport
    ),
    "expected_final_indeterminacy": (
      expected_final_indeterminacy
    ),
    "indeterminacy_rule": (
      indeterminacy_rule
    ),
    "transport_rule": transport_rule,
    "generator_bridge_rule": (
      generator_bridge_rule
    ),
    "premise_steps": premise_steps,
    "result": result,
    "eta_indeterminacy_step": (
      eta_indeterminacy_step
    ),
    "transport_step": transport_step,
    "final_indeterminacy_step": (
      final_indeterminacy_step
    ),
  }


def test_phase60_3_reuses_derived_prop53():
  data = build_phase60_3_data()

  assert isinstance(
    data[
      "prop53_step"
    ].conclusion,
    TodaProp53FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop53_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_3_reuses_derived_nu_prime_double_relation():
  data = build_phase60_3_data()

  assert (
    data[
      "nu_prime_double_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "nu_prime_double_step"
    ].conclusion
    == data[
      "phase58"
    ][
      "expected_final_double"
    ]
  )


def test_phase60_3_scope_is_n_at_least_3_and_t_at_least_1():
  data = build_phase60_3_data()

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

  assert (
    data[
      "t_range"
    ]
    == ScalarGreaterEqualStatement(
      left=data[
        "t"
      ],
      right=1,
    )
  )


def test_phase60_3_indeterminacy_rule_matches_prop53_and_scope():
  data = build_phase60_3_data()

  assert find_inference_match(
    data[
      "indeterminacy_rule"
    ],
    (
      data[
        "prop53_step"
      ],
      data[
        "n_range_step"
      ],
      data[
        "t_range_step"
      ],
    ),
  ) is not None


def test_phase60_3_derives_eta_cube_indeterminacy():
  data = build_phase60_3_data()

  step = data[
    "eta_indeterminacy_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_eta_indeterminacy"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase60_3_eta_cube_is_right_associated_composition():
  data = build_phase60_3_data()

  assert (
    data[
      "eta_cube"
    ]
    == Composition(
      left=data[
        "eta_n"
      ],
      right=Composition(
        left=data[
          "eta_n_plus_one"
        ],
        right=data[
          "eta_n_plus_two"
        ],
      ),
    )
  )


def test_phase60_3_indeterminacy_preserves_target_bracket():
  data = build_phase60_3_data()

  bracket = (
    data[
      "eta_indeterminacy_step"
    ].conclusion.bracket
  )

  assert (
    bracket
    == data[
      "bracket"
    ]
  )

  assert (
    bracket.index
    == data[
      "t"
    ]
  )


def test_phase60_3_transport_rule_matches_phase58_double_relation():
  data = build_phase60_3_data()

  assert find_inference_match(
    data[
      "transport_rule"
    ],
    (
      data[
        "nu_prime_double_step"
      ],
      data[
        "n_range_step"
      ],
    ),
  ) is not None


def test_phase60_3_derives_higher_double_nu_prime_relation():
  data = build_phase60_3_data()

  step = data[
    "transport_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_transport"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase60_3_transport_exponent_is_n_minus_3():
  data = build_phase60_3_data()

  suspended = (
    data[
      "transport_step"
    ].conclusion
    .lhs
    .expression
  )

  assert isinstance(
    suspended,
    IteratedSuspension,
  )

  assert (
    suspended.exponent
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


def test_phase60_3_generator_bridge_matches_two_derived_results():
  data = build_phase60_3_data()

  assert find_inference_match(
    data[
      "generator_bridge_rule"
    ],
    (
      data[
        "eta_indeterminacy_step"
      ],
      data[
        "transport_step"
      ],
    ),
  ) is not None


def test_phase60_3_derives_double_nu_prime_indeterminacy_generator():
  data = build_phase60_3_data()

  step = data[
    "final_indeterminacy_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_final_indeterminacy"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase60_3_final_indeterminacy_uses_two_derived_premises():
  data = build_phase60_3_data()

  assert (
    data[
      "final_indeterminacy_step"
    ].premises
    == (
      data[
        "eta_indeterminacy_step"
      ],
      data[
        "transport_step"
      ],
    )
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in data[
      "final_indeterminacy_step"
    ].premises
  )


def test_phase60_3_rejects_given_prop53():
  data = build_phase60_3_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "prop53_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "indeterminacy_rule"
    ],
    (
      given_step,
      data[
        "n_range_step"
      ],
      data[
        "t_range_step"
      ],
    ),
  ) is None


def test_phase60_3_rejects_given_nu_prime_double_relation():
  data = build_phase60_3_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "nu_prime_double_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "transport_rule"
    ],
    (
      given_step,
      data[
        "n_range_step"
      ],
    ),
  ) is None


def test_phase60_3_rejects_n_at_least_2_scope():
  data = build_phase60_3_data()

  wrong_range = ProofStep(
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
      "indeterminacy_rule"
    ],
    (
      data[
        "prop53_step"
      ],
      wrong_range,
      data[
        "t_range_step"
      ],
    ),
  ) is None


def test_phase60_3_rejects_t_at_least_0_scope():
  data = build_phase60_3_data()

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
      "indeterminacy_rule"
    ],
    (
      data[
        "prop53_step"
      ],
      data[
        "n_range_step"
      ],
      wrong_range,
    ),
  ) is None


def test_phase60_3_final_result_is_not_given():
  data = build_phase60_3_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_final_indeterminacy"
    ]
    not in initial_conclusions
  )


def test_phase60_3_reaches_fixed_point_in_two_rounds():
  data = build_phase60_3_data()

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
      "eta_indeterminacy_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "transport_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "final_indeterminacy_step"
    ]
    in result.round_results[
      1
    ].new_steps
  )





