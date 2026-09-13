from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_rules import (
  TodaProp511NuSquaredFiniteDimensionalStatement,
  toda_nu_family_definition_statement,
  toda_prop511_nu_squared_finite_dimensional_integration_inference_rule,
  toda_prop511_nu_squared_finite_dimensional_literature_statements,
)


def build_concrete_nu_squared_relation(
  n,
):
  nu_n = (
    toda_nu_family_definition_statement(
      n
    ).element
  )

  nu_n_plus_three = (
    toda_nu_family_definition_statement(
      n + 3
    ).element
  )

  return Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=n + 6,
      sphere_dimension=n,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=Composition(
        left=nu_n,
        right=nu_n_plus_three,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )


@lru_cache(maxsize=1)
def build_phase73_8c_data():
  pi11_5_relation = (
    build_concrete_nu_squared_relation(
      5
    )
  )

  pi12_6_relation = (
    build_concrete_nu_squared_relation(
      6
    )
  )

  pi13_7_relation = (
    build_concrete_nu_squared_relation(
      7
    )
  )

  pi14_8_relation = (
    build_concrete_nu_squared_relation(
      8
    )
  )

  pi11_5_step = ProofStep(
    conclusion=pi11_5_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  pi12_6_step = ProofStep(
    conclusion=pi12_6_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  pi13_7_step = ProofStep(
    conclusion=pi13_7_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  pi14_8_step = ProofStep(
    conclusion=pi14_8_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  n = ScalarSymbol(
    name="n",
  )

  n_plus_three = ScalarSum(
    left=n,
    right=3,
  )

  n_plus_six = ScalarSum(
    left=n,
    right=6,
  )

  nu_n = (
    toda_nu_family_definition_statement(
      n
    ).element
  )

  nu_n_plus_three = HomotopyElement(
    name="ν_(n+3)",
    dimension=n_plus_three,
    source=n_plus_six,
    target=n_plus_three,
    generator=GeneratorSymbol(
      family="ν",
      index=n_plus_three,
    ),
  )

  higher_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=n_plus_six,
      sphere_dimension=n,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=Composition(
        left=nu_n,
        right=nu_n_plus_three,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  higher_step = ProofStep(
    conclusion=higher_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  higher_range = (
    ScalarGreaterEqualStatement(
      left=n,
      right=9,
    )
  )

  higher_range_step = ProofStep(
    conclusion=higher_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_prop511_nu_squared_finite_dimensional_integration_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      pi11_5_step,
      pi12_6_step,
      pi13_7_step,
      pi14_8_step,
      higher_step,
      higher_range_step,
    ),
  )

  assert (
    match
    is not None
  )

  final_step = (
    apply_inference_match(
      match
    )
  )

  return {
    "pi11_5_relation": (
      pi11_5_relation
    ),
    "pi12_6_relation": (
      pi12_6_relation
    ),
    "pi13_7_relation": (
      pi13_7_relation
    ),
    "pi14_8_relation": (
      pi14_8_relation
    ),
    "pi11_5_step": pi11_5_step,
    "pi12_6_step": pi12_6_step,
    "pi13_7_step": pi13_7_step,
    "pi14_8_step": pi14_8_step,
    "n": n,
    "nu_n": nu_n,
    "nu_n_plus_three": (
      nu_n_plus_three
    ),
    "higher_relation": (
      higher_relation
    ),
    "higher_step": higher_step,
    "higher_range": higher_range,
    "higher_range_step": (
      higher_range_step
    ),
    "rule": rule,
    "final_step": final_step,
  }


def test_phase73_8c_derives_nu_squared_finite_dimensional_aggregate():
  data = build_phase73_8c_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaProp511NuSquaredFiniteDimensionalStatement,
  )


def test_phase73_8c_preserves_pi11_5_branch():
  data = build_phase73_8c_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .pi11_5_group_relation
    == data[
      "pi11_5_relation"
    ]
  )


def test_phase73_8c_preserves_pi12_6_branch():
  data = build_phase73_8c_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .pi12_6_group_relation
    == data[
      "pi12_6_relation"
    ]
  )


def test_phase73_8c_preserves_pi13_7_branch():
  data = build_phase73_8c_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .pi13_7_group_relation
    == data[
      "pi13_7_relation"
    ]
  )


def test_phase73_8c_preserves_pi14_8_branch():
  data = build_phase73_8c_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .pi14_8_group_relation
    == data[
      "pi14_8_relation"
    ]
  )


def test_phase73_8c_preserves_higher_branch():
  data = build_phase73_8c_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .higher_six_stem_group_relation
    == data[
      "higher_relation"
    ]
  )


def test_phase73_8c_preserves_higher_range():
  data = build_phase73_8c_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .higher_range
    == ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=9,
    )
  )


def test_phase73_8c_attaches_prop511_literature():
  data = build_phase73_8c_data()

  assert (
    data[
      "final_step"
    ]
    .conclusion
    .literature_statements
    == (
      toda_prop511_nu_squared_finite_dimensional_literature_statements()
    )
  )


def test_phase73_8c_preserves_exact_provenance():
  data = build_phase73_8c_data()

  final_step = (
    data[
      "final_step"
    ]
  )

  assert (
    final_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    final_step.premises
    == (
      data[
        "pi11_5_step"
      ],
      data[
        "pi12_6_step"
      ],
      data[
        "pi13_7_step"
      ],
      data[
        "pi14_8_step"
      ],
      data[
        "higher_step"
      ],
      data[
        "higher_range_step"
      ],
    )
  )


def test_phase73_8c_rejects_wrong_pi11_5_order():
  data = build_phase73_8c_data()

  relation = (
    data[
      "pi11_5_relation"
    ]
  )

  wrong_step = ProofStep(
    conclusion=Relation(
      lhs=relation.lhs,
      rhs=FiniteCyclicGroup(
        order=4,
        generator=(
          relation
          .rhs
          .generator
        ),
      ),
      relation_type=RelationType.EQUALITY,
    ),
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
        "pi12_6_step"
      ],
      data[
        "pi13_7_step"
      ],
      data[
        "pi14_8_step"
      ],
      data[
        "higher_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase73_8c_rejects_wrong_higher_range():
  data = build_phase73_8c_data()

  wrong_range_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=8,
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
        "pi11_5_step"
      ],
      data[
        "pi12_6_step"
      ],
      data[
        "pi13_7_step"
      ],
      data[
        "pi14_8_step"
      ],
      data[
        "higher_step"
      ],
      wrong_range_step,
    ),
  ) is None


def test_phase73_8c_rejects_given_mathematical_branch():
  data = build_phase73_8c_data()

  given_step = ProofStep(
    conclusion=data[
      "pi14_8_relation"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "pi11_5_step"
      ],
      data[
        "pi12_6_step"
      ],
      data[
        "pi13_7_step"
      ],
      given_step,
      data[
        "higher_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None



