from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
)
from homotopy_groups import (
  DirectSumGroup,
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
from test_phase70_delta_eta9_squared_surjectivity import (
  build_phase70_5_data,
)
from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaProp53FiniteDimensionalStatement,
  toda_512_n4_delta_injective_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase71_2_data():
  phase70_5 = (
    build_phase70_5_data()
  )

  phase70_4 = (
    phase70_5[
      "phase70_4"
    ]
  )

  phase59_8 = (
    phase70_4[
      "phase59_8"
    ]
  )

  delta_eta9_squared_step = (
    phase70_5[
      "delta_eta9_squared_step"
    ]
  )

  pi9_4_step = (
    phase70_5[
      "pi9_4_step"
    ]
  )

  prop53_step = (
    phase59_8[
      "integration_step"
    ]
  )

  rule = (
    toda_512_n4_delta_injective_inference_rule()
  )

  premise_steps = (
    delta_eta9_squared_step,
    pi9_4_step,
    prop53_step,
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

  pi11_9 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=9,
  )

  pi9_4 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=4,
  )

  expected_statement = (
    TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=pi11_9,
        target_group=pi9_4,
      ),
    )
  )

  assert (
    final_step.conclusion
    == expected_statement
  )

  return {
    "phase70_5": phase70_5,
    "phase70_4": phase70_4,
    "phase59_8": phase59_8,
    "delta_eta9_squared_step": (
      delta_eta9_squared_step
    ),
    "pi9_4_step": pi9_4_step,
    "prop53_step": prop53_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "match": match,
    "final_step": final_step,
    "pi11_9": pi11_9,
    "pi9_4": pi9_4,
    "expected_statement": (
      expected_statement
    ),
  }


def test_phase71_2_reuses_derived_delta_eta9_squared():
  data = build_phase71_2_data()

  assert (
    data[
      "delta_eta9_squared_step"
    ].rule
    == ProofRule.INFERENCE
  )

  relation = (
    data[
      "delta_eta9_squared_step"
    ].conclusion
  )

  assert (
    relation.lhs.map
    == EHP_DELTA_MAP
  )

  assert isinstance(
    relation.lhs.expression,
    Composition,
  )


def test_phase71_2_delta_argument_is_eta9_squared():
  data = build_phase71_2_data()

  eta9_squared = (
    data[
      "delta_eta9_squared_step"
    ].conclusion
    .lhs
    .expression
  )

  assert isinstance(
    eta9_squared,
    Composition,
  )

  eta_9 = eta9_squared.left
  eta_10 = eta9_squared.right

  assert (
    eta_9.generator
    == GeneratorSymbol(
      family="η",
      index=9,
    )
  )

  assert (
    eta_10.generator
    == GeneratorSymbol(
      family="η",
      index=10,
    )
  )


def test_phase71_2_reuses_derived_pi9_4():
  data = build_phase71_2_data()

  assert (
    data[
      "pi9_4_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi9_4_step"
    ].conclusion.lhs
    == data[
      "pi9_4"
    ]
  )


def test_phase71_2_pi9_4_has_two_order_two_summands():
  data = build_phase71_2_data()

  group = (
    data[
      "pi9_4_step"
    ].conclusion
    .rhs
  )

  assert isinstance(
    group,
    DirectSumGroup,
  )

  assert (
    len(
      group.summands
    )
    == 2
  )

  assert all(
    isinstance(
      summand,
      FiniteCyclicGroup,
    )
    and summand.order
    == 2
    for summand
    in group.summands
  )


def test_phase71_2_delta_value_is_second_summand_generator():
  data = build_phase71_2_data()

  delta_value = (
    data[
      "delta_eta9_squared_step"
    ].conclusion
    .rhs
  )

  second_generator = (
    data[
      "pi9_4_step"
    ].conclusion
    .rhs
    .summands[
      1
    ]
    .generator
  )

  assert (
    delta_value
    is second_generator
  )


def test_phase71_2_reuses_derived_prop53():
  data = build_phase71_2_data()

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


def test_phase71_2_prop53_higher_source_is_order_two():
  data = build_phase71_2_data()

  higher_relation = (
    data[
      "prop53_step"
    ].conclusion
    .higher_eta_squared_group_relation
  )

  assert isinstance(
    higher_relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    higher_relation.rhs.order
    == 2
  )


def test_phase71_2_rule_matches_dependencies():
  data = build_phase71_2_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase71_2_derives_delta_injective():
  data = build_phase71_2_data()

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


def test_phase71_2_target_map_is_pi11_9_to_pi9_4():
  data = build_phase71_2_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement.map
    == TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=9,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=4,
      ),
    )
  )


def test_phase71_2_uses_exact_three_dependencies():
  data = build_phase71_2_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "delta_eta9_squared_step"
      ],
      data[
        "pi9_4_step"
      ],
      data[
        "prop53_step"
      ],
    )
  )


def test_phase71_2_rejects_given_delta_eta9_squared():
  data = build_phase71_2_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_eta9_squared_step"
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
        "pi9_4_step"
      ],
      data[
        "prop53_step"
      ],
    ),
  ) is None


def test_phase71_2_rejects_given_pi9_4():
  data = build_phase71_2_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi9_4_step"
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
        "delta_eta9_squared_step"
      ],
      given,
      data[
        "prop53_step"
      ],
    ),
  ) is None


def test_phase71_2_rejects_given_prop53():
  data = build_phase71_2_data()

  given = ProofStep(
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
      "rule"
    ],
    (
      data[
        "delta_eta9_squared_step"
      ],
      data[
        "pi9_4_step"
      ],
      given,
    ),
  ) is None


def test_phase71_2_rejects_wrong_delta_argument():
  data = build_phase71_2_data()

  wrong_eta_9 = HomotopyElement(
    name="η₈",
    dimension=8,
    source=9,
    target=8,
    generator=GeneratorSymbol(
      family="η",
      index=8,
    ),
  )

  wrong_eta_10 = HomotopyElement(
    name="η₉",
    dimension=9,
    source=10,
    target=9,
    generator=GeneratorSymbol(
      family="η",
      index=9,
    ),
  )

  wrong_relation = replace(
    data[
      "delta_eta9_squared_step"
    ].conclusion,
    lhs=MapApplication(
      map=EHP_DELTA_MAP,
      expression=Composition(
        left=wrong_eta_9,
        right=wrong_eta_10,
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
      wrong_step,
      data[
        "pi9_4_step"
      ],
      data[
        "prop53_step"
      ],
    ),
  ) is None


def test_phase71_2_rejects_wrong_delta_value():
  data = build_phase71_2_data()

  first_generator = (
    data[
      "pi9_4_step"
    ].conclusion
    .rhs
    .summands[
      0
    ]
    .generator
  )

  wrong_relation = replace(
    data[
      "delta_eta9_squared_step"
    ].conclusion,
    rhs=first_generator,
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
        "pi9_4_step"
      ],
      data[
        "prop53_step"
      ],
    ),
  ) is None


def test_phase71_2_rejects_wrong_target_group():
  data = build_phase71_2_data()

  wrong_relation = replace(
    data[
      "pi9_4_step"
    ].conclusion,
    lhs=TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=4,
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
        "delta_eta9_squared_step"
      ],
      wrong_step,
      data[
        "prop53_step"
      ],
    ),
  ) is None


def test_phase71_2_rejects_wrong_target_order():
  data = build_phase71_2_data()

  group = (
    data[
      "pi9_4_step"
    ].conclusion
    .rhs
  )

  wrong_second = FiniteCyclicGroup(
    order=4,
    generator=(
      group
      .summands[
        1
      ]
      .generator
    ),
  )

  wrong_relation = replace(
    data[
      "pi9_4_step"
    ].conclusion,
    rhs=DirectSumGroup(
      summands=(
        group.summands[
          0
        ],
        wrong_second,
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
        "delta_eta9_squared_step"
      ],
      wrong_step,
      data[
        "prop53_step"
      ],
    ),
  ) is None


def test_phase71_2_final_is_not_given():
  data = build_phase71_2_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


