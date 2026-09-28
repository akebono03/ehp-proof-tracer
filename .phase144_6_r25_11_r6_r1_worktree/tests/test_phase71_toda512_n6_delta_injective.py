from dataclasses import replace
from functools import lru_cache

from expression import (
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
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from test_phase70_pi11_6_delta_iota13 import (
  build_phase70_8_data,
)
from toda_rules import (
  TodaDeltaInjectiveStatement,
  toda_512_n6_delta_injective_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase71_4_data():
  phase70_8 = (
    build_phase70_8_data()
  )

  pi13_13_step = (
    phase70_8[
      "pi13_13_step"
    ]
  )

  pi11_6_step = (
    phase70_8[
      "final_step"
    ]
  )

  rule = (
    toda_512_n6_delta_injective_inference_rule()
  )

  premise_steps = (
    pi13_13_step,
    pi11_6_step,
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

  pi13_13 = TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=13,
  )

  pi11_6 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=6,
  )

  expected_statement = (
    TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=pi13_13,
        target_group=pi11_6,
      ),
    )
  )

  assert (
    final_step.conclusion
    == expected_statement
  )

  return {
    "phase70_8": phase70_8,
    "pi13_13_step": pi13_13_step,
    "pi11_6_step": pi11_6_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "match": match,
    "final_step": final_step,
    "pi13_13": pi13_13,
    "pi11_6": pi11_6,
    "expected_statement": (
      expected_statement
    ),
  }


def test_phase71_4_reuses_foundational_pi13_13():
  data = build_phase71_4_data()

  assert (
    data[
      "pi13_13_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "pi13_13_step"
    ].conclusion.lhs
    == data[
      "pi13_13"
    ]
  )


def test_phase71_4_pi13_13_is_free_cyclic():
  data = build_phase71_4_data()

  group = (
    data[
      "pi13_13_step"
    ].conclusion
    .rhs
  )

  assert isinstance(
    group,
    FreeCyclicGroup,
  )


def test_phase71_4_source_generator_is_iota13():
  data = build_phase71_4_data()

  generator = (
    data[
      "pi13_13_step"
    ].conclusion
    .rhs
    .generator
  )

  assert isinstance(
    generator,
    HomotopyElement,
  )

  assert (
    generator.dimension
    == 13
  )

  assert (
    generator.generator
    == GeneratorSymbol(
      family="ι",
      index=13,
    )
  )


def test_phase71_4_reuses_derived_pi11_6():
  data = build_phase71_4_data()

  assert (
    data[
      "pi11_6_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi11_6_step"
    ].conclusion.lhs
    == data[
      "pi11_6"
    ]
  )


def test_phase71_4_pi11_6_is_free_cyclic():
  data = build_phase71_4_data()

  group = (
    data[
      "pi11_6_step"
    ].conclusion
    .rhs
  )

  assert isinstance(
    group,
    FreeCyclicGroup,
  )


def test_phase71_4_target_generator_is_delta_iota13():
  data = build_phase71_4_data()

  source_generator = (
    data[
      "pi13_13_step"
    ].conclusion
    .rhs
    .generator
  )

  target_generator = (
    data[
      "pi11_6_step"
    ].conclusion
    .rhs
    .generator
  )

  assert (
    target_generator
    == MapApplication(
      map=EHP_DELTA_MAP,
      expression=source_generator,
    )
  )


def test_phase71_4_rule_matches_dependencies():
  data = build_phase71_4_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase71_4_derives_delta_injective():
  data = build_phase71_4_data()

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


def test_phase71_4_map_is_pi13_13_to_pi11_6():
  data = build_phase71_4_data()

  assert (
    data[
      "final_step"
    ].conclusion.map
    == TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=13,
        sphere_dimension=13,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=6,
      ),
    )
  )


def test_phase71_4_uses_exact_two_dependencies():
  data = build_phase71_4_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi13_13_step"
      ],
      data[
        "pi11_6_step"
      ],
    )
  )


def test_phase71_4_rejects_inference_pi13_13():
  data = build_phase71_4_data()

  wrong_rule_step = ProofStep(
    conclusion=(
      data[
        "pi13_13_step"
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
      wrong_rule_step,
      data[
        "pi11_6_step"
      ],
    ),
  ) is None


def test_phase71_4_rejects_given_pi11_6():
  data = build_phase71_4_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi11_6_step"
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
        "pi13_13_step"
      ],
      given,
    ),
  ) is None


def test_phase71_4_rejects_wrong_source_group():
  data = build_phase71_4_data()

  wrong_relation = replace(
    data[
      "pi13_13_step"
    ].conclusion,
    lhs=TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=13,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "pi11_6_step"
      ],
    ),
  ) is None


def test_phase71_4_rejects_non_free_source():
  data = build_phase71_4_data()

  source_generator = (
    data[
      "pi13_13_step"
    ].conclusion
    .rhs
    .generator
  )

  wrong_relation = replace(
    data[
      "pi13_13_step"
    ].conclusion,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=source_generator,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "pi11_6_step"
      ],
    ),
  ) is None


def test_phase71_4_rejects_wrong_source_generator():
  data = build_phase71_4_data()

  wrong_iota = HomotopyElement(
    name="ι_12",
    dimension=12,
    generator=GeneratorSymbol(
      family="ι",
      index=12,
    ),
  )

  wrong_relation = replace(
    data[
      "pi13_13_step"
    ].conclusion,
    rhs=FreeCyclicGroup(
      generator=wrong_iota,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "pi11_6_step"
      ],
    ),
  ) is None


def test_phase71_4_rejects_wrong_target_group():
  data = build_phase71_4_data()

  wrong_relation = replace(
    data[
      "pi11_6_step"
    ].conclusion,
    lhs=TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=7,
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
        "pi13_13_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase71_4_rejects_non_free_target():
  data = build_phase71_4_data()

  target_generator = (
    data[
      "pi11_6_step"
    ].conclusion
    .rhs
    .generator
  )

  wrong_relation = replace(
    data[
      "pi11_6_step"
    ].conclusion,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=target_generator,
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
        "pi13_13_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase71_4_rejects_wrong_target_generator():
  data = build_phase71_4_data()

  source_generator = (
    data[
      "pi13_13_step"
    ].conclusion
    .rhs
    .generator
  )

  wrong_target_generator = (
    MapApplication(
      map=EHP_DELTA_MAP,
      expression=HomotopyElement(
        name="ι_12",
        dimension=12,
        generator=GeneratorSymbol(
          family="ι",
          index=12,
        ),
      ),
    )
  )

  assert (
    wrong_target_generator
    != MapApplication(
      map=EHP_DELTA_MAP,
      expression=source_generator,
    )
  )

  wrong_relation = replace(
    data[
      "pi11_6_step"
    ].conclusion,
    rhs=FreeCyclicGroup(
      generator=wrong_target_generator,
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
        "pi13_13_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase71_4_final_is_not_given():
  data = build_phase71_4_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


