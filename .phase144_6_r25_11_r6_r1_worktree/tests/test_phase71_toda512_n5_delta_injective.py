from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from test_phase70_nu5_eta8_squared_zero_delta_eta11 import (
  build_phase70_7_data,
)
from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaProp51FiniteDimensionalStatement,
  toda_512_n5_delta_injective_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase71_3_data():
  phase70_7 = (
    build_phase70_7_data()
  )

  phase70_6 = (
    phase70_7[
      "phase70_6"
    ]
  )

  phase70_5 = (
    phase70_6[
      "phase70_5"
    ]
  )

  delta_eta11_step = (
    phase70_7[
      "delta_eta11_step"
    ]
  )

  pi10_5_step = (
    phase70_7[
      "pi10_5_step"
    ]
  )

  prop51_step = (
    phase70_5[
      "prop51_step"
    ]
  )

  rule = (
    toda_512_n5_delta_injective_inference_rule()
  )

  premise_steps = (
    delta_eta11_step,
    pi10_5_step,
    prop51_step,
  )

  match = find_inference_match(
    rule,
    premise_steps,
  )

  assert match is not None

  final_step = (
    apply_inference_match(
      match
    )
  )

  pi12_11 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=11,
  )

  pi10_5 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  expected_statement = (
    TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=pi12_11,
        target_group=pi10_5,
      ),
    )
  )

  assert (
    final_step.conclusion
    == expected_statement
  )

  return {
    "phase70_7": phase70_7,
    "phase70_6": phase70_6,
    "phase70_5": phase70_5,
    "delta_eta11_step": (
      delta_eta11_step
    ),
    "pi10_5_step": pi10_5_step,
    "prop51_step": prop51_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "match": match,
    "final_step": final_step,
    "pi12_11": pi12_11,
    "pi10_5": pi10_5,
    "expected_statement": (
      expected_statement
    ),
  }


def test_phase71_3_reuses_derived_delta_eta11():
  data = build_phase71_3_data()

  assert (
    data[
      "delta_eta11_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase71_3_delta_argument_is_eta11():
  data = build_phase71_3_data()

  relation = (
    data[
      "delta_eta11_step"
    ].conclusion
  )

  assert isinstance(
    relation.lhs,
    MapApplication,
  )

  assert (
    relation.lhs.map
    == EHP_DELTA_MAP
  )

  eta_11 = (
    relation
    .lhs
    .expression
  )

  assert isinstance(
    eta_11,
    HomotopyElement,
  )

  assert (
    eta_11.dimension
    == 11
  )

  assert (
    eta_11.source
    == 12
  )

  assert (
    eta_11.target
    == 11
  )

  assert (
    eta_11.generator
    == GeneratorSymbol(
      family="η",
      index=11,
    )
  )


def test_phase71_3_reuses_derived_pi10_5():
  data = build_phase71_3_data()

  assert (
    data[
      "pi10_5_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi10_5_step"
    ].conclusion.lhs
    == data[
      "pi10_5"
    ]
  )


def test_phase71_3_pi10_5_is_order_two():
  data = build_phase71_3_data()

  group = (
    data[
      "pi10_5_step"
    ].conclusion
    .rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert (
    group.order
    == 2
  )


def test_phase71_3_delta_value_is_pi10_5_generator():
  data = build_phase71_3_data()

  assert (
    data[
      "delta_eta11_step"
    ].conclusion
    .rhs
    is data[
      "pi10_5_step"
    ].conclusion
    .rhs
    .generator
  )


def test_phase71_3_reuses_derived_prop51():
  data = build_phase71_3_data()

  assert isinstance(
    data[
      "prop51_step"
    ].conclusion,
    TodaProp51FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop51_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase71_3_prop51_higher_eta_is_order_two():
  data = build_phase71_3_data()

  relation = (
    data[
      "prop51_step"
    ].conclusion
    .higher_eta_group_relation
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 2
  )


def test_phase71_3_rule_matches_dependencies():
  data = build_phase71_3_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase71_3_derives_delta_injective():
  data = build_phase71_3_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase71_3_map_is_pi12_11_to_pi10_5():
  data = build_phase71_3_data()

  assert (
    data[
      "final_step"
    ].conclusion.map
    == TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=12,
        sphere_dimension=11,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      ),
    )
  )


def test_phase71_3_uses_exact_three_dependencies():
  data = build_phase71_3_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "delta_eta11_step"
      ],
      data[
        "pi10_5_step"
      ],
      data[
        "prop51_step"
      ],
    )
  )


def test_phase71_3_rejects_given_delta_eta11():
  data = build_phase71_3_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_eta11_step"
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
        "pi10_5_step"
      ],
      data[
        "prop51_step"
      ],
    ),
  ) is None


def test_phase71_3_rejects_given_pi10_5():
  data = build_phase71_3_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi10_5_step"
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
        "delta_eta11_step"
      ],
      given,
      data[
        "prop51_step"
      ],
    ),
  ) is None


def test_phase71_3_rejects_given_prop51():
  data = build_phase71_3_data()

  given = ProofStep(
    conclusion=(
      data[
        "prop51_step"
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
        "delta_eta11_step"
      ],
      data[
        "pi10_5_step"
      ],
      given,
    ),
  ) is None


def test_phase71_3_rejects_wrong_delta_argument():
  data = build_phase71_3_data()

  wrong_eta = HomotopyElement(
    name="η₁₀",
    dimension=10,
    source=11,
    target=10,
    generator=GeneratorSymbol(
      family="η",
      index=10,
    ),
  )

  wrong_relation = replace(
    data[
      "delta_eta11_step"
    ].conclusion,
    lhs=MapApplication(
      map=EHP_DELTA_MAP,
      expression=wrong_eta,
    ),
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
        "pi10_5_step"
      ],
      data[
        "prop51_step"
      ],
    ),
  ) is None


def test_phase71_3_rejects_wrong_delta_map():
  data = build_phase71_3_data()

  wrong_relation = replace(
    data[
      "delta_eta11_step"
    ].conclusion,
    lhs=data[
      "delta_eta11_step"
    ].conclusion.rhs,
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
        "pi10_5_step"
      ],
      data[
        "prop51_step"
      ],
    ),
  ) is None


def test_phase71_3_rejects_wrong_delta_value():
  data = build_phase71_3_data()

  wrong_value = HomotopyElement(
    name="x",
    dimension=5,
  )

  wrong_relation = replace(
    data[
      "delta_eta11_step"
    ].conclusion,
    rhs=wrong_value,
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
        "pi10_5_step"
      ],
      data[
        "prop51_step"
      ],
    ),
  ) is None


def test_phase71_3_rejects_wrong_target_group():
  data = build_phase71_3_data()

  wrong_relation = replace(
    data[
      "pi10_5_step"
    ].conclusion,
    lhs=TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=6,
    ),
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
      data[
        "delta_eta11_step"
      ],
      wrong_step,
      data[
        "prop51_step"
      ],
    ),
  ) is None


def test_phase71_3_rejects_wrong_target_order():
  data = build_phase71_3_data()

  relation = (
    data[
      "pi10_5_step"
    ].conclusion
  )

  wrong_relation = replace(
    relation,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=(
        relation
        .rhs
        .generator
      ),
    ),
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
      data[
        "delta_eta11_step"
      ],
      wrong_step,
      data[
        "prop51_step"
      ],
    ),
  ) is None


def test_phase71_3_final_is_not_given():
  data = build_phase71_3_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


