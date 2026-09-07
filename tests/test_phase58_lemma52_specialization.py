from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
  Multiple,
  Suspension,
  Zero,
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
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from probes.probe_phase50_capabilities import (
  build_phase50_representative_result,
)
from test_phase58_nu_prime_specialization import (
  build_phase58_2_data,
)
from toda_rules import (
  Toda53NuPrimeBracketSpecializationStatement,
  toda_53_eta3_twice_zero_inference_rule,
  toda_53_nu_prime_bracket_specialization_inference_rule,
  toda_53_nu_prime_lemma52_double_inference_rule,
  toda_53_nu_prime_lemma52_hopf_inference_rule,
  toda_53_nu_prime_lemma52_membership_inference_rule,
)


def build_phase58_3_data():
  phase50 = (
    build_phase50_representative_result()
  )

  phase58_2 = (
    build_phase58_2_data()
  )

  pi4_3_relation_step = (
    phase50[
      "final_group_steps"
    ][
      0
    ]
  )

  eta3_zero_rule = (
    toda_53_eta3_twice_zero_inference_rule()
  )

  eta3_zero_result = (
    run_inference_until_stable_with_history(
      eta3_zero_rule,
      (
        pi4_3_relation_step,
      ),
    )
  )

  eta_3 = (
    phase58_2[
      "eta_3"
    ]
  )

  two_eta3_zero = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=eta_3,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  two_eta3_zero_step = next(
    step
    for step in eta3_zero_result.steps
    if (
      step.conclusion
      == two_eta3_zero
    )
  )

  specialization_rule = (
    toda_53_nu_prime_bracket_specialization_inference_rule()
  )

  specialization_result = (
    run_inference_until_stable_with_history(
      specialization_rule,
      (
        phase58_2[
          "membership_step"
        ],
      ),
    )
  )

  specialization_step = next(
    step
    for step in specialization_result.steps
    if isinstance(
      step.conclusion,
      Toda53NuPrimeBracketSpecializationStatement,
    )
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

  expected_hopf_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=(
        phase58_2[
          "nu_prime"
        ]
      ),
    ),
    rhs=IteratedSuspension(
      expression=eta_3,
      exponent=2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  expected_double_relation = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=(
        phase58_2[
          "nu_prime"
        ]
      ),
    ),
    rhs=Composition(
      left=eta_3,
      right=Composition(
        left=Suspension(
          expression=eta_3,
        ),
        right=eta_5,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  expected_membership = (
    HomotopyGroupMembershipStatement(
      element=(
        phase58_2[
          "nu_prime"
        ]
      ),
      group_dimension=6,
      sphere_dimension=3,
    )
  )

  hopf_rule = (
    toda_53_nu_prime_lemma52_hopf_inference_rule()
  )

  double_rule = (
    toda_53_nu_prime_lemma52_double_inference_rule()
  )

  membership_rule = (
    toda_53_nu_prime_lemma52_membership_inference_rule()
  )

  premise_steps = (
    specialization_step,
    two_eta3_zero_step,
  )

  rules = (
    hopf_rule,
    double_rule,
    membership_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  return {
    "phase50": phase50,
    "phase58_2": phase58_2,
    "pi4_3_relation_step": (
      pi4_3_relation_step
    ),
    "eta_3": eta_3,
    "eta_5": eta_5,
    "two_eta3_zero": (
      two_eta3_zero
    ),
    "two_eta3_zero_step": (
      two_eta3_zero_step
    ),
    "specialization_step": (
      specialization_step
    ),
    "expected_hopf_relation": (
      expected_hopf_relation
    ),
    "expected_double_relation": (
      expected_double_relation
    ),
    "expected_membership": (
      expected_membership
    ),
    "eta3_zero_rule": (
      eta3_zero_rule
    ),
    "hopf_rule": hopf_rule,
    "double_rule": double_rule,
    "membership_rule": (
      membership_rule
    ),
    "premise_steps": premise_steps,
    "rules": rules,
    "result": result,
  }


def test_phase58_3_reuses_derived_pi4_3_order_two_relation():
  data = build_phase58_3_data()

  step = data[
    "pi4_3_relation_step"
  ]

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  relation = step.conclusion

  assert relation.lhs == (
    TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )
  )

  assert relation.rhs == (
    FiniteCyclicGroup(
      order=2,
      generator=data[
        "eta_3"
      ],
    )
  )


def test_phase58_3_derives_two_eta3_zero():
  data = build_phase58_3_data()

  assert (
    data[
      "two_eta3_zero_step"
    ].conclusion
    == data[
      "two_eta3_zero"
    ]
  )

  assert (
    data[
      "two_eta3_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase58_3_two_eta3_zero_preserves_phase50_provenance():
  data = build_phase58_3_data()

  assert (
    data[
      "two_eta3_zero_step"
    ].premises
    == (
      data[
        "pi4_3_relation_step"
      ],
    )
  )


def test_phase58_3_eta3_zero_rule_rejects_given_pi4_3_relation():
  data = build_phase58_3_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "pi4_3_relation_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "eta3_zero_rule"
    ],
    (
      given_step,
    ),
  ) is None


def test_phase58_3_specialization_step_is_inference():
  data = build_phase58_3_data()

  assert (
    data[
      "specialization_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "specialization_step"
    ].conclusion.alpha
    == data[
      "eta_3"
    ]
  )

  assert (
    data[
      "specialization_step"
    ].conclusion.lemma52_index
    == 4
  )


def test_phase58_3_hopf_rule_matches_specialization():
  data = build_phase58_3_data()

  assert find_inference_match(
    data[
      "hopf_rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase58_3_derives_h_nu_prime_equals_e2_eta3():
  data = build_phase58_3_data()

  steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_hopf_relation"
      ]
    )
  )

  assert len(
    steps
  ) == 1

  assert (
    steps[
      0
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase58_3_derives_twice_nu_prime_canonical_lemma52_value():
  data = build_phase58_3_data()

  steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_double_relation"
      ]
    )
  )

  assert len(
    steps
  ) == 1

  assert (
    steps[
      0
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase58_3_double_value_still_contains_suspension_eta3():
  data = build_phase58_3_data()

  relation = data[
    "expected_double_relation"
  ]

  assert relation.rhs == (
    Composition(
      left=data[
        "eta_3"
      ],
      right=Composition(
        left=Suspension(
          expression=data[
            "eta_3"
          ],
        ),
        right=data[
          "eta_5"
        ],
      ),
    )
  )


def test_phase58_3_derives_nu_prime_membership_pi6_3():
  data = build_phase58_3_data()

  steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_membership"
      ]
    )
  )

  assert len(
    steps
  ) == 1

  assert (
    steps[
      0
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase58_3_all_three_results_preserve_two_premises():
  data = build_phase58_3_data()

  expected = (
    data[
      "expected_hopf_relation"
    ],
    data[
      "expected_double_relation"
    ],
    data[
      "expected_membership"
    ],
  )

  for conclusion in expected:
    step = next(
      step
      for step in data[
        "result"
      ].steps
      if (
        step.conclusion
        == conclusion
      )
    )

    assert (
      step.premises
      == data[
        "premise_steps"
      ]
    )


def test_phase58_3_rejects_given_two_eta3_zero():
  data = build_phase58_3_data()

  given_zero_step = ProofStep(
    conclusion=(
      data[
        "two_eta3_zero"
      ]
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "hopf_rule"
    ],
    (
      data[
        "specialization_step"
      ],
      given_zero_step,
    ),
  ) is None

  assert find_inference_match(
    data[
      "double_rule"
    ],
    (
      data[
        "specialization_step"
      ],
      given_zero_step,
    ),
  ) is None

  assert find_inference_match(
    data[
      "membership_rule"
    ],
    (
      data[
        "specialization_step"
      ],
      given_zero_step,
    ),
  ) is None


def test_phase58_3_does_not_normalize_hopf_value_to_eta5():
  data = build_phase58_3_data()

  eta5_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=(
        data[
          "phase58_2"
        ][
          "nu_prime"
        ]
      ),
    ),
    rhs=data[
      "eta_5"
    ],
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in data[
      "result"
    ].steps
  )

  assert (
    eta5_relation
    not in conclusions
  )


def test_phase58_3_reaches_fixed_point_in_one_round():
  data = build_phase58_3_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    data[
      "result"
    ].round_count
    == 1
  )

  assert len(
    data[
      "result"
    ].round_results[
      0
    ].new_steps
  ) == 3


