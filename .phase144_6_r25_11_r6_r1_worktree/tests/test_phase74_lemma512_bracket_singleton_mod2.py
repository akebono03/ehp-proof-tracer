from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  ScalarSum,
  TodaBracket,
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
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase73_prop511_finite_dimensional_integration import (
  build_phase73_8e_data,
)
from test_phase74_lemma512_first_indeterminacy_zero import (
  build_phase74_3_data,
)
from test_phase74_lemma512_second_indeterminacy_zero import (
  build_phase74_4_data,
)
from toda_rules import (
  TodaLemma512BracketSingletonMod2Statement,
  TodaLemma512FirstIndeterminacyZeroStatement,
  TodaLemma512SecondIndeterminacyZeroStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp511NuSquaredFiniteDimensionalStatement,
  toda_lemma512_bracket_singleton_mod2_inference_rule,
  toda_nu_family_definition_statement,
)


@lru_cache(maxsize=1)
def build_phase74_5_data():
  phase74_3 = (
    build_phase74_3_data()
  )

  phase74_4 = (
    build_phase74_4_data()
  )

  phase73_8e = (
    build_phase73_8e_data()
  )

  first_zero_step = (
    phase74_3[
      "final_step"
    ]
  )

  second_zero_step = (
    phase74_4[
      "final_step"
    ]
  )

  prop511_step = (
    phase73_8e[
      "final_step"
    ]
  )

  n = (
    first_zero_step
    .conclusion
    .bracket
    .first
    .dimension
  )

  n_ge_6_step = (
    phase74_4[
      "n_ge_6_step"
    ]
  )

  rule = (
    toda_lemma512_bracket_singleton_mod2_inference_rule()
  )

  premise_steps = (
    first_zero_step,
    second_zero_step,
    prop511_step,
    n_ge_6_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      premise_steps,
    )
  )

  n_plus_three = ScalarSum(
    left=n,
    right=3,
  )

  n_plus_six = ScalarSum(
    left=n,
    right=6,
  )

  bracket = (
    first_zero_step
    .conclusion
    .bracket
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

  nu_n_squared = Composition(
    left=nu_n,
    right=nu_n_plus_three,
  )

  expected_statement = (
    TodaLemma512BracketSingletonMod2Statement(
      bracket=bracket,
      ambient_group=TodaPrimaryGroup(
        group_dimension=n_plus_six,
        sphere_dimension=n,
      ),
      generator=nu_n_squared,
      n_range=n_ge_6_step.conclusion,
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase74_3": phase74_3,
    "phase74_4": phase74_4,
    "phase73_8e": phase73_8e,
    "first_zero_step": (
      first_zero_step
    ),
    "second_zero_step": (
      second_zero_step
    ),
    "prop511_step": prop511_step,
    "n": n,
    "n_ge_6_step": n_ge_6_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "bracket": bracket,
    "nu_n": nu_n,
    "nu_n_plus_three": (
      nu_n_plus_three
    ),
    "nu_n_squared": nu_n_squared,
    "expected_statement": (
      expected_statement
    ),
    "final_step": final_step,
  }


def test_phase74_5_reuses_first_indeterminacy_zero():
  data = build_phase74_5_data()

  assert isinstance(
    data[
      "first_zero_step"
    ].conclusion,
    TodaLemma512FirstIndeterminacyZeroStatement,
  )

  assert (
    data[
      "first_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_5_reuses_second_indeterminacy_zero():
  data = build_phase74_5_data()

  assert isinstance(
    data[
      "second_zero_step"
    ].conclusion,
    TodaLemma512SecondIndeterminacyZeroStatement,
  )

  assert (
    data[
      "second_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_5_two_indeterminacy_statements_use_same_bracket():
  data = build_phase74_5_data()

  assert (
    data[
      "first_zero_step"
    ].conclusion
    .bracket
    == data[
      "second_zero_step"
    ].conclusion
    .bracket
  )


def test_phase74_5_reuses_derived_prop511():
  data = build_phase74_5_data()

  assert isinstance(
    data[
      "prop511_step"
    ].conclusion,
    TodaProp511FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop511_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_5_prop511_contains_nu_squared_aggregate():
  data = build_phase74_5_data()

  assert isinstance(
    data[
      "prop511_step"
    ].conclusion
    .nu_squared_finite_dimensional,
    TodaProp511NuSquaredFiniteDimensionalStatement,
  )


def test_phase74_5_scope_is_n_at_least_6():
  data = build_phase74_5_data()

  assert (
    data[
      "n_ge_6_step"
    ].conclusion
    == ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=6,
    )
  )

  assert (
    data[
      "n_ge_6_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase74_5_derives_singleton_mod2_statement():
  data = build_phase74_5_data()

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


def test_phase74_5_preserves_exact_bracket():
  data = build_phase74_5_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .bracket
    == data[
      "bracket"
    ]
  )


def test_phase74_5_ambient_group_is_pi_n_plus_6_n():
  data = build_phase74_5_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement.ambient_group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=6,
      ),
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase74_5_generator_is_nu_n_squared():
  data = build_phase74_5_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .generator
    == data[
      "nu_n_squared"
    ]
  )

  assert isinstance(
    data[
      "final_step"
    ].conclusion
    .generator,
    Composition,
  )


def test_phase74_5_nu_n_squared_has_expected_factors():
  data = build_phase74_5_data()

  generator = (
    data[
      "final_step"
    ].conclusion
    .generator
  )

  assert (
    generator.left
    == data[
      "nu_n"
    ]
  )

  assert (
    generator.right
    == data[
      "nu_n_plus_three"
    ]
  )


def test_phase74_5_generator_is_not_new_nu_square_class():
  data = build_phase74_5_data()

  assert type(
    data[
      "final_step"
    ].conclusion
    .generator
  ) is Composition


def test_phase74_5_prop511_n6_branch_is_order_two():
  data = build_phase74_5_data()

  relation = (
    data[
      "prop511_step"
    ].conclusion
    .nu_squared_finite_dimensional
    .pi12_6_group_relation
  )

  assert (
    relation
    .lhs
    == TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=6,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 2
  )


def test_phase74_5_prop511_n7_branch_is_order_two():
  data = build_phase74_5_data()

  relation = (
    data[
      "prop511_step"
    ].conclusion
    .nu_squared_finite_dimensional
    .pi13_7_group_relation
  )

  assert (
    relation
    .lhs
    == TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=7,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 2
  )


def test_phase74_5_prop511_n8_branch_is_order_two():
  data = build_phase74_5_data()

  relation = (
    data[
      "prop511_step"
    ].conclusion
    .nu_squared_finite_dimensional
    .pi14_8_group_relation
  )

  assert (
    relation
    .lhs
    == TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=8,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 2
  )


def test_phase74_5_prop511_higher_branch_is_order_two():
  data = build_phase74_5_data()

  relation = (
    data[
      "prop511_step"
    ].conclusion
    .nu_squared_finite_dimensional
    .higher_six_stem_group_relation
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 2
  )


def test_phase74_5_prop511_higher_range_is_n_at_least_9():
  data = build_phase74_5_data()

  statement = (
    data[
      "prop511_step"
    ].conclusion
    .nu_squared_finite_dimensional
  )

  assert (
    statement
    .higher_range
    .right
    == 9
  )


def test_phase74_5_final_step_uses_exact_four_premises():
  data = build_phase74_5_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "first_zero_step"
      ],
      data[
        "second_zero_step"
      ],
      data[
        "prop511_step"
      ],
      data[
        "n_ge_6_step"
      ],
    )
  )


def test_phase74_5_final_statement_not_present_initially():
  data = build_phase74_5_data()

  assert (
    data[
      "expected_statement"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase74_5_rejects_given_first_indeterminacy_zero():
  data = build_phase74_5_data()

  given_first = ProofStep(
    conclusion=(
      data[
        "first_zero_step"
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
      given_first,
      data[
        "second_zero_step"
      ],
      data[
        "prop511_step"
      ],
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_5_rejects_given_second_indeterminacy_zero():
  data = build_phase74_5_data()

  given_second = ProofStep(
    conclusion=(
      data[
        "second_zero_step"
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
        "first_zero_step"
      ],
      given_second,
      data[
        "prop511_step"
      ],
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_5_rejects_given_prop511():
  data = build_phase74_5_data()

  given_prop511 = ProofStep(
    conclusion=(
      data[
        "prop511_step"
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
        "first_zero_step"
      ],
      data[
        "second_zero_step"
      ],
      given_prop511,
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_5_rejects_wrong_range():
  data = build_phase74_5_data()

  wrong_range = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=5,
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
        "first_zero_step"
      ],
      data[
        "second_zero_step"
      ],
      data[
        "prop511_step"
      ],
      wrong_range,
    ),
  ) is None


def test_phase74_5_rejects_different_brackets():
  data = build_phase74_5_data()

  second_statement = (
    data[
      "second_zero_step"
    ].conclusion
  )

  bracket = (
    second_statement.bracket
  )

  wrong_third = HomotopyElement(
    name="wrong eta",
    dimension=bracket.third.dimension,
    source=bracket.third.source,
    target=bracket.third.target,
    generator=GeneratorSymbol(
      family="η",
      index=ScalarSum(
        left=data[
          "n"
        ],
        right=5,
      ),
    ),
  )

  wrong_bracket = TodaBracket(
    first=bracket.first,
    second=bracket.second,
    third=wrong_third,
  )

  wrong_second_statement = replace(
    second_statement,
    bracket=wrong_bracket,
  )

  wrong_second_step = ProofStep(
    conclusion=wrong_second_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "first_zero_step"
      ],
      wrong_second_step,
      data[
        "prop511_step"
      ],
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_5_rejects_wrong_prop511_order():
  data = build_phase74_5_data()

  prop511 = (
    data[
      "prop511_step"
    ].conclusion
  )

  nu_squared = (
    prop511
    .nu_squared_finite_dimensional
  )

  pi12_6 = (
    nu_squared
    .pi12_6_group_relation
  )

  wrong_pi12_6 = Relation(
    lhs=pi12_6.lhs,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=(
        pi12_6
        .rhs
        .generator
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  wrong_nu_squared = replace(
    nu_squared,
    pi12_6_group_relation=(
      wrong_pi12_6
    ),
  )

  wrong_prop511 = replace(
    prop511,
    nu_squared_finite_dimensional=(
      wrong_nu_squared
    ),
  )

  wrong_prop511_step = ProofStep(
    conclusion=wrong_prop511,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "first_zero_step"
      ],
      data[
        "second_zero_step"
      ],
      wrong_prop511_step,
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_5_rejects_wrong_prop511_generator():
  data = build_phase74_5_data()

  prop511 = (
    data[
      "prop511_step"
    ].conclusion
  )

  nu_squared = (
    prop511
    .nu_squared_finite_dimensional
  )

  pi13_7 = (
    nu_squared
    .pi13_7_group_relation
  )

  wrong_generator = HomotopyElement(
    name="wrong generator",
    dimension=7,
    source=13,
    target=7,
    generator=GeneratorSymbol(
      family="wrong",
      index=7,
    ),
  )

  wrong_pi13_7 = Relation(
    lhs=pi13_7.lhs,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=wrong_generator,
    ),
    relation_type=RelationType.EQUALITY,
  )

  wrong_nu_squared = replace(
    nu_squared,
    pi13_7_group_relation=(
      wrong_pi13_7
    ),
  )

  wrong_prop511 = replace(
    prop511,
    nu_squared_finite_dimensional=(
      wrong_nu_squared
    ),
  )

  wrong_prop511_step = ProofStep(
    conclusion=wrong_prop511,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "first_zero_step"
      ],
      data[
        "second_zero_step"
      ],
      wrong_prop511_step,
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_5_reaches_fixed_point():
  data = build_phase74_5_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


