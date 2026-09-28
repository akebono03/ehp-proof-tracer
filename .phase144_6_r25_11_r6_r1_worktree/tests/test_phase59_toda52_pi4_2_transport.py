from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
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
from probes.probe_phase50_capabilities import (
  build_phase50_representative_result,
)
from probes.probe_phase56_capabilities import (
  build_phase56_representative_result,
)
from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  toda_52_pi4_2_finite_cyclic_transport_inference_rule,
)


def build_phase59_2_data():
  phase50 = (
    build_phase50_representative_result()
  )

  phase56 = (
    build_phase56_representative_result()
  )

  pi4_3_step = (
    phase50[
      "final_group_steps"
    ][
      0
    ]
  )

  toda52_step = (
    phase56[
      "composition_isomorphism_steps"
    ][
      0
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

  eta_2_squared = Composition(
    left=eta_2,
    right=eta_3,
  )

  expected_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_2_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  premise_steps = (
    pi4_3_step,
    toda52_step,
  )

  rule = (
    toda_52_pi4_2_finite_cyclic_transport_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  result_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_relation
    )
  )

  return {
    "phase50": phase50,
    "phase56": phase56,
    "pi4_3_step": pi4_3_step,
    "toda52_step": toda52_step,
    "eta_2": eta_2,
    "eta_3": eta_3,
    "eta_2_squared": (
      eta_2_squared
    ),
    "expected_relation": (
      expected_relation
    ),
    "premise_steps": premise_steps,
    "rule": rule,
    "result": result,
    "result_steps": result_steps,
  }


def test_phase59_2_reuses_derived_pi4_3_relation():
  data = build_phase59_2_data()

  step = data[
    "pi4_3_step"
  ]

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert (
    step.conclusion
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=4,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=data[
          "eta_3"
        ],
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase59_2_reuses_derived_toda52_isomorphism():
  data = build_phase59_2_data()

  step = data[
    "toda52_step"
  ]

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    step.conclusion,
    Toda52CompositionIsomorphismStatement,
  )


def test_phase59_2_toda52_map_is_eta2_composition():
  data = build_phase59_2_data()

  statement = (
    data[
      "toda52_step"
    ].conclusion
  )

  assert isinstance(
    statement.composition,
    Composition,
  )

  assert (
    statement.composition.left
    == data[
      "eta_2"
    ]
  )


def test_phase59_2_eta2_squared_uses_existing_composition():
  data = build_phase59_2_data()

  eta_2_squared = data[
    "eta_2_squared"
  ]

  assert isinstance(
    eta_2_squared,
    Composition,
  )

  assert (
    eta_2_squared.left
    == data[
      "eta_2"
    ]
  )

  assert (
    eta_2_squared.right
    == data[
      "eta_3"
    ]
  )


def test_phase59_2_rule_matches_derived_dependencies():
  data = build_phase59_2_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase59_2_derives_pi4_2_order_two_eta2_squared():
  data = build_phase59_2_data()

  steps = data[
    "result_steps"
  ]

  assert len(
    steps
  ) == 1

  assert (
    steps[
      0
    ].conclusion
    == data[
      "expected_relation"
    ]
  )

  assert (
    steps[
      0
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase59_2_target_is_pi4_2():
  data = build_phase59_2_data()

  relation = (
    data[
      "result_steps"
    ][
      0
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    )
  )


def test_phase59_2_target_is_order_two_finite_cyclic():
  data = build_phase59_2_data()

  group = (
    data[
      "result_steps"
    ][
      0
    ].conclusion
    .rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert group.order == 2

  assert (
    group.generator
    == data[
      "eta_2_squared"
    ]
  )


def test_phase59_2_preserves_two_derived_premises():
  data = build_phase59_2_data()

  step = (
    data[
      "result_steps"
    ][
      0
    ]
  )

  assert (
    step.premises
    == data[
      "premise_steps"
    ]
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in step.premises
  )


def test_phase59_2_rejects_given_pi4_3_relation():
  data = build_phase59_2_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "pi4_3_step"
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
        "toda52_step"
      ],
    ),
  ) is None


def test_phase59_2_rejects_given_toda52_isomorphism():
  data = build_phase59_2_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "toda52_step"
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
        "pi4_3_step"
      ],
      given_step,
    ),
  ) is None


def test_phase59_2_rejects_wrong_source_group():
  data = build_phase59_2_data()

  wrong_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=data[
        "eta_3"
      ],
    ),
    relation_type=RelationType.EQUALITY,
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(
      data[
        "pi4_3_step"
      ],
    ),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "toda52_step"
      ],
    ),
  ) is None


def test_phase59_2_rejects_wrong_cyclic_order():
  data = build_phase59_2_data()

  wrong_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    ),
    rhs=FiniteCyclicGroup(
      order=3,
      generator=data[
        "eta_3"
      ],
    ),
    relation_type=RelationType.EQUALITY,
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(
      data[
        "pi4_3_step"
      ],
    ),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "toda52_step"
      ],
    ),
  ) is None


def test_phase59_2_rejects_wrong_generator():
  data = build_phase59_2_data()

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

  wrong_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_4,
    ),
    relation_type=RelationType.EQUALITY,
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(
      data[
        "pi4_3_step"
      ],
    ),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "toda52_step"
      ],
    ),
  ) is None


def test_phase59_2_reaches_fixed_point_in_one_round():
  data = build_phase59_2_data()

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
  ) == 1



