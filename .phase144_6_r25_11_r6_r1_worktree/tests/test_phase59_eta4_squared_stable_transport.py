from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
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
from probes.probe_phase46_capabilities import (
  build_phase46_representative_result,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase59_pi6_4_eta4_squared import (
  build_phase59_6_data,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  toda_prop53_eta4_squared_stable_transport_inference_rule,
)


def build_phase59_7_data():
  phase59_6 = (
    build_phase59_6_data()
  )

  pi6_4_step = (
    phase59_6[
      "final_step"
    ]
  )

  n = ScalarSymbol(
    name="n",
  )

  phase46 = (
    build_phase46_representative_result(
      n=4,
      k=2,
      m=n,
    )
  )

  stable_isomorphism_step = (
    phase46[
      "theorem_steps"
    ][
      0
    ]
  )

  higher_range = (
    ScalarGreaterEqualStatement(
      left=n,
      right=5,
    )
  )

  higher_range_step = ProofStep(
    conclusion=higher_range,
    premises=(),
    rule=ProofRule.GIVEN,
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

  eta_4_squared = Composition(
    left=eta_4,
    right=eta_5,
  )

  exponent = ScalarSum(
    left=n,
    right=ScalarProduct(
      left=-1,
      right=4,
    ),
  )

  expected_generator = (
    IteratedSuspension(
      expression=eta_4_squared,
      exponent=exponent,
    )
  )

  expected_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=2,
      ),
      sphere_dimension=n,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=expected_generator,
    ),
    relation_type=RelationType.EQUALITY,
  )

  rule = (
    toda_prop53_eta4_squared_stable_transport_inference_rule()
  )

  premise_steps = (
    pi6_4_step,
    stable_isomorphism_step,
    higher_range_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_relation
    )
  )

  return {
    "phase59_6": phase59_6,
    "phase46": phase46,
    "n": n,
    "pi6_4_step": pi6_4_step,
    "stable_isomorphism_step": (
      stable_isomorphism_step
    ),
    "higher_range": higher_range,
    "higher_range_step": (
      higher_range_step
    ),
    "eta_4": eta_4,
    "eta_5": eta_5,
    "eta_4_squared": (
      eta_4_squared
    ),
    "exponent": exponent,
    "expected_generator": (
      expected_generator
    ),
    "expected_relation": (
      expected_relation
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "final_step": final_step,
  }


def test_phase59_7_reuses_phase59_6_pi6_4_relation():
  data = build_phase59_7_data()

  step = data[
    "pi6_4_step"
  ]

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert (
    step.conclusion
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=4,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=data[
          "eta_4_squared"
        ],
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase59_7_reuses_phase46_toda45_isomorphism():
  data = build_phase59_7_data()

  step = data[
    "stable_isomorphism_step"
  ]

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    step.conclusion,
    Toda45IsomorphismStatement,
  )


def test_phase59_7_phase46_instance_has_base_n4_k2():
  data = build_phase59_7_data()

  suspension_map = (
    data[
      "stable_isomorphism_step"
    ].conclusion.map
  )

  assert (
    suspension_map.source_group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=4,
        right=2,
      ),
      sphere_dimension=4,
    )
  )


def test_phase59_7_phase46_target_is_pi_n_plus_2_n():
  data = build_phase59_7_data()

  suspension_map = (
    data[
      "stable_isomorphism_step"
    ].conclusion.map
  )

  assert (
    suspension_map.target_group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=2,
      ),
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase59_7_phase46_exponent_is_n_minus_4():
  data = build_phase59_7_data()

  expected_exponent = ScalarSum(
    left=data[
      "n"
    ],
    right=ScalarProduct(
      left=-1,
      right=4,
    ),
  )

  assert (
    data[
      "stable_isomorphism_step"
    ].conclusion.map.exponent
    == expected_exponent
  )

  assert (
    data[
      "exponent"
    ]
    == expected_exponent
  )


def test_phase59_7_scope_is_n_at_least_5():
  data = build_phase59_7_data()

  assert (
    data[
      "higher_range"
    ]
    == ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=5,
    )
  )


def test_phase59_7_eta4_squared_uses_composition():
  data = build_phase59_7_data()

  assert (
    data[
      "eta_4_squared"
    ]
    == Composition(
      left=data[
        "eta_4"
      ],
      right=data[
        "eta_5"
      ],
    )
  )


def test_phase59_7_rule_matches_dependencies():
  data = build_phase59_7_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase59_7_derives_stable_range_finite_cyclic_transport():
  data = build_phase59_7_data()

  step = data[
    "final_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_relation"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase59_7_target_generator_is_iterated_suspension_eta4_squared():
  data = build_phase59_7_data()

  group = (
    data[
      "final_step"
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
      "expected_generator"
    ]
  )


def test_phase59_7_final_provenance_uses_three_dependencies():
  data = build_phase59_7_data()

  assert (
    data[
      "final_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "pi6_4_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "stable_isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase59_7_rejects_given_pi6_4_relation():
  data = build_phase59_7_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "pi6_4_step"
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
      data[
        "stable_isomorphism_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase59_7_rejects_given_toda45_isomorphism():
  data = build_phase59_7_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "stable_isomorphism_step"
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
        "pi6_4_step"
      ],
      given_step,
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase59_7_rejects_n4_scope():
  data = build_phase59_7_data()

  wrong_range = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=4,
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
        "pi6_4_step"
      ],
      data[
        "stable_isomorphism_step"
      ],
      wrong_range,
    ),
  ) is None


def test_phase59_7_rejects_wrong_source_generator():
  data = build_phase59_7_data()

  wrong_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=4,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=data[
        "eta_4"
      ],
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
      data[
        "stable_isomorphism_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase59_7_does_not_normalize_generator_to_eta_n_squared():
  data = build_phase59_7_data()

  generator = (
    data[
      "final_step"
    ].conclusion.rhs.generator
  )

  assert isinstance(
    generator,
    IteratedSuspension,
  )

  assert (
    generator
    == data[
      "expected_generator"
    ]
  )


def test_phase59_7_final_result_is_not_given():
  data = build_phase59_7_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_relation"
    ]
    not in initial_conclusions
  )


def test_phase59_7_reaches_fixed_point_in_one_round():
  data = build_phase59_7_data()

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

  assert (
    data[
      "final_step"
    ]
    in data[
      "result"
    ].round_results[
      0
    ].new_steps
  )



