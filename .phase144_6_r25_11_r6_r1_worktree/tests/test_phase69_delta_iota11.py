from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
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
from test_phase68_pi9_5_nu5_eta8 import (
  build_phase68_6_data,
)
from test_phase69_delta_surjectivity import (
  build_phase69_2_data,
)
from toda_rules import (
  TodaDeltaSurjectiveStatement,
  toda_eq510_delta_iota11_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase69_3_data():
  phase68_6 = (
    build_phase68_6_data()
  )

  phase69_2 = (
    build_phase69_2_data()
  )

  pi9_5_step = (
    phase68_6[
      "final_step"
    ]
  )

  delta_surjective_step = (
    phase69_2[
      "surjective_step"
    ]
  )

  iota_11 = HomotopyElement(
    name="ι_11",
    dimension=11,
    generator=GeneratorSymbol(
      family="ι",
      index=11,
    ),
  )

  pi11_11_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=11,
    ),
    rhs=FreeCyclicGroup(
      generator=iota_11,
    ),
    relation_type=RelationType.EQUALITY,
  )

  pi11_11_step = ProofStep(
    conclusion=pi11_11_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_eq510_delta_iota11_inference_rule()
  )

  premise_steps = (
    delta_surjective_step,
    pi11_11_step,
    pi9_5_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  nu5_eta8 = (
    pi9_5_step
    .conclusion
    .rhs
    .generator
  )

  expected_final = Relation(
    lhs=MapApplication(
      map=EHP_DELTA_MAP,
      expression=iota_11,
    ),
    rhs=nu5_eta8,
    relation_type=RelationType.EQUALITY,
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
    "phase68_6": phase68_6,
    "phase69_2": phase69_2,
    "pi9_5_step": pi9_5_step,
    "delta_surjective_step": (
      delta_surjective_step
    ),
    "iota_11": iota_11,
    "pi11_11_relation": (
      pi11_11_relation
    ),
    "pi11_11_step": (
      pi11_11_step
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "nu5_eta8": nu5_eta8,
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase69_3_reuses_derived_delta_surjective():
  data = build_phase69_3_data()

  assert isinstance(
    data[
      "delta_surjective_step"
    ].conclusion,
    TodaDeltaSurjectiveStatement,
  )

  assert (
    data[
      "delta_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase69_3_delta_map_is_pi11_11_to_pi9_5():
  data = build_phase69_3_data()

  assert (
    data[
      "delta_surjective_step"
    ].conclusion.map
    == TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=11,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=5,
      ),
    )
  )


def test_phase69_3_pi11_11_is_foundational_given():
  data = build_phase69_3_data()

  assert (
    data[
      "pi11_11_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "pi11_11_step"
    ].conclusion
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=11,
      ),
      rhs=FreeCyclicGroup(
        generator=data[
          "iota_11"
        ],
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase69_3_iota11_is_canonical_identity_generator():
  data = build_phase69_3_data()

  iota_11 = data[
    "iota_11"
  ]

  assert (
    iota_11.dimension
    == 11
  )

  assert (
    iota_11.generator
    == GeneratorSymbol(
      family="ι",
      index=11,
    )
  )


def test_phase69_3_reuses_derived_pi9_5():
  data = build_phase69_3_data()

  assert (
    data[
      "pi9_5_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi9_5_step"
    ].conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=5,
    )
  )


def test_phase69_3_pi9_5_is_order_two():
  data = build_phase69_3_data()

  group = (
    data[
      "pi9_5_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert (
    group.order
    == 2
  )


def test_phase69_3_pi9_5_generator_is_nu5_eta8():
  data = build_phase69_3_data()

  generator = data[
    "nu5_eta8"
  ]

  assert isinstance(
    generator,
    Composition,
  )

  assert (
    generator.right.generator
    == GeneratorSymbol(
      family="η",
      index=8,
    )
  )


def test_phase69_3_rule_matches_exact_dependencies():
  data = build_phase69_3_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase69_3_derives_toda_510():
  data = build_phase69_3_data()

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


def test_phase69_3_final_is_delta_iota11():
  data = build_phase69_3_data()

  assert (
    data[
      "final_step"
    ].conclusion.lhs
    == MapApplication(
      map=EHP_DELTA_MAP,
      expression=data[
        "iota_11"
      ],
    )
  )


def test_phase69_3_final_value_is_phase68_generator():
  data = build_phase69_3_data()

  assert (
    data[
      "final_step"
    ].conclusion.rhs
    is data[
      "pi9_5_step"
    ].conclusion.rhs.generator
  )

  assert (
    data[
      "final_step"
    ].conclusion.rhs
    == data[
      "nu5_eta8"
    ]
  )


def test_phase69_3_final_uses_exact_three_dependencies():
  data = build_phase69_3_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "delta_surjective_step"
      ],
      data[
        "pi11_11_step"
      ],
      data[
        "pi9_5_step"
      ],
    )
  )


def test_phase69_3_rejects_given_delta_surjective():
  data = build_phase69_3_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_surjective_step"
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
      given,
      data[
        "pi11_11_step"
      ],
      data[
        "pi9_5_step"
      ],
    ),
  ) is None


def test_phase69_3_rejects_given_pi9_5():
  data = build_phase69_3_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi9_5_step"
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
        "delta_surjective_step"
      ],
      data[
        "pi11_11_step"
      ],
      given,
    ),
  ) is None


def test_phase69_3_rejects_inference_pi11_11():
  data = build_phase69_3_data()

  derived = ProofStep(
    conclusion=(
      data[
        "pi11_11_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "delta_surjective_step"
      ],
      derived,
      data[
        "pi9_5_step"
      ],
    ),
  ) is None


def test_phase69_3_rejects_wrong_source_generator():
  data = build_phase69_3_data()

  wrong_iota = HomotopyElement(
    name="ι_10",
    dimension=10,
    generator=GeneratorSymbol(
      family="ι",
      index=10,
    ),
  )

  wrong_source_relation = replace(
    data[
      "pi11_11_relation"
    ],
    rhs=FreeCyclicGroup(
      generator=wrong_iota,
    ),
  )

  wrong_source_step = ProofStep(
    conclusion=wrong_source_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "delta_surjective_step"
      ],
      wrong_source_step,
      data[
        "pi9_5_step"
      ],
    ),
  ) is None


def test_phase69_3_rejects_wrong_target_order():
  data = build_phase69_3_data()

  wrong_target_relation = replace(
    data[
      "pi9_5_step"
    ].conclusion,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=data[
        "nu5_eta8"
      ],
    ),
  )

  wrong_target_step = ProofStep(
    conclusion=wrong_target_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "delta_surjective_step"
      ],
      data[
        "pi11_11_step"
      ],
      wrong_target_step,
    ),
  ) is None


def test_phase69_3_final_not_present_initially():
  data = build_phase69_3_data()

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase69_3_reaches_fixed_point():
  data = build_phase69_3_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


