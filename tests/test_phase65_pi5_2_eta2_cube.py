from functools import lru_cache

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
from probes.probe_phase56_capabilities import (
  build_phase56_representative_result,
)
from test_phase59_pi5_3_eta3_squared import (
  build_phase59_4_data,
)
from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  toda_prop56_pi5_2_eta2_cube_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase65_2_data():
  phase56 = (
    build_phase56_representative_result()
  )

  phase59 = (
    build_phase59_4_data()
  )

  toda52_step = (
    phase56[
      "composition_isomorphism_steps"
    ][
      0
    ]
  )

  pi5_3_step = (
    phase59[
      "final_step"
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

  eta_3_squared = Composition(
    left=eta_3,
    right=eta_4,
  )

  eta_2_cube = Composition(
    left=eta_2,
    right=eta_3_squared,
  )

  expected_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=2,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_2_cube,
    ),
    relation_type=RelationType.EQUALITY,
  )

  rule = (
    toda_prop56_pi5_2_eta2_cube_inference_rule()
  )

  premise_steps = (
    pi5_3_step,
    toda52_step,
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
    "phase56": phase56,
    "phase59": phase59,
    "toda52_step": toda52_step,
    "pi5_3_step": pi5_3_step,
    "eta_2": eta_2,
    "eta_3": eta_3,
    "eta_4": eta_4,
    "eta_3_squared": eta_3_squared,
    "eta_2_cube": eta_2_cube,
    "expected_relation": (
      expected_relation
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "final_step": final_step,
  }


def test_phase65_2_reuses_derived_pi5_3_relation():
  data = build_phase65_2_data()

  assert (
    data[
      "pi5_3_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi5_3_step"
    ].conclusion
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=5,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=data[
          "eta_3_squared"
        ],
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase65_2_reuses_derived_toda52_isomorphism():
  data = build_phase65_2_data()

  assert (
    data[
      "toda52_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "toda52_step"
    ].conclusion,
    Toda52CompositionIsomorphismStatement,
  )


def test_phase65_2_eta3_squared_is_right_composition():
  data = build_phase65_2_data()

  assert (
    data[
      "eta_3_squared"
    ]
    == Composition(
      left=data[
        "eta_3"
      ],
      right=data[
        "eta_4"
      ],
    )
  )


def test_phase65_2_eta2_cube_is_right_associated():
  data = build_phase65_2_data()

  assert (
    data[
      "eta_2_cube"
    ]
    == Composition(
      left=data[
        "eta_2"
      ],
      right=Composition(
        left=data[
          "eta_3"
        ],
        right=data[
          "eta_4"
        ],
      ),
    )
  )


def test_phase65_2_rule_matches_two_derived_dependencies():
  data = build_phase65_2_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase65_2_derives_pi5_2_order_two_eta2_cube():
  data = build_phase65_2_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_relation"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_2_final_group_is_order_two():
  data = build_phase65_2_data()

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


def test_phase65_2_final_generator_is_eta2_cube():
  data = build_phase65_2_data()

  assert (
    data[
      "final_step"
    ].conclusion.rhs.generator
    == data[
      "eta_2_cube"
    ]
  )


def test_phase65_2_provenance_uses_exactly_two_dependencies():
  data = build_phase65_2_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi5_3_step"
      ],
      data[
        "toda52_step"
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


def test_phase65_2_rejects_given_pi5_3_relation():
  data = build_phase65_2_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "pi5_3_step"
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


def test_phase65_2_rejects_given_toda52_isomorphism():
  data = build_phase65_2_data()

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
        "pi5_3_step"
      ],
      given_step,
    ),
  ) is None


def test_phase65_2_rejects_wrong_source_generator():
  data = build_phase65_2_data()

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
        "toda52_step"
      ],
    ),
  ) is None


def test_phase65_2_rejects_wrong_source_group():
  data = build_phase65_2_data()

  wrong_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=data[
        "eta_3_squared"
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
        "toda52_step"
      ],
    ),
  ) is None


def test_phase65_2_final_result_is_not_given():
  data = build_phase65_2_data()

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

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase65_2_reaches_fixed_point_in_one_round():
  data = build_phase65_2_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert (
    data[
      "final_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )


