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
  TodaPrimaryGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase74_lemma512_bracket_singleton_mod2 import (
  build_phase74_5_data,
)
from toda_rules import (
  TodaLemma512BracketSingletonMod2Statement,
  TodaLemma512CoefficientStabilityStatement,
  toda_lemma512_coefficient_stability_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase74_6_data():
  phase74_5 = (
    build_phase74_5_data()
  )

  singleton_step = (
    phase74_5[
      "final_step"
    ]
  )

  n = (
    singleton_step
    .conclusion
    .bracket
    .first
    .dimension
  )

  n_ge_6_step = (
    phase74_5[
      "n_ge_6_step"
    ]
  )

  rule = (
    toda_lemma512_coefficient_stability_inference_rule()
  )

  premise_steps = (
    singleton_step,
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

  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )

  n_plus_two = ScalarSum(
    left=n,
    right=2,
  )

  n_plus_four = ScalarSum(
    left=n,
    right=4,
  )

  n_plus_five = ScalarSum(
    left=n,
    right=5,
  )

  n_plus_six = ScalarSum(
    left=n,
    right=6,
  )

  n_plus_seven = ScalarSum(
    left=n,
    right=7,
  )

  eta_n_plus_one = HomotopyElement(
    name="η_(n+1)",
    dimension=n_plus_one,
    source=n_plus_two,
    target=n_plus_one,
    generator=GeneratorSymbol(
      family="η",
      index=n_plus_one,
    ),
  )

  nu_n_plus_two = HomotopyElement(
    name="ν_(n+2)",
    dimension=n_plus_two,
    source=n_plus_five,
    target=n_plus_two,
    generator=GeneratorSymbol(
      family="ν",
      index=n_plus_two,
    ),
  )

  eta_n_plus_five = HomotopyElement(
    name="η_(n+5)",
    dimension=n_plus_five,
    source=n_plus_six,
    target=n_plus_five,
    generator=GeneratorSymbol(
      family="η",
      index=n_plus_five,
    ),
  )

  expected_target_bracket = TodaBracket(
    first=eta_n_plus_one,
    second=nu_n_plus_two,
    third=eta_n_plus_five,
  )

  nu_n_plus_one = HomotopyElement(
    name="ν_(n+1)",
    dimension=n_plus_one,
    source=n_plus_four,
    target=n_plus_one,
    generator=GeneratorSymbol(
      family="ν",
      index=n_plus_one,
    ),
  )

  nu_n_plus_four = HomotopyElement(
    name="ν_(n+4)",
    dimension=n_plus_four,
    source=n_plus_seven,
    target=n_plus_four,
    generator=GeneratorSymbol(
      family="ν",
      index=n_plus_four,
    ),
  )

  expected_target_generator = Composition(
    left=nu_n_plus_one,
    right=nu_n_plus_four,
  )

  expected_statement = (
    TodaLemma512CoefficientStabilityStatement(
      source_bracket=(
        singleton_step
        .conclusion
        .bracket
      ),
      target_bracket=(
        expected_target_bracket
      ),
      source_generator=(
        singleton_step
        .conclusion
        .generator
      ),
      target_generator=(
        expected_target_generator
      ),
      source_group=(
        singleton_step
        .conclusion
        .ambient_group
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=n_plus_seven,
        sphere_dimension=n_plus_one,
      ),
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
    "phase74_5": phase74_5,
    "singleton_step": singleton_step,
    "n": n,
    "n_ge_6_step": n_ge_6_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "expected_target_bracket": (
      expected_target_bracket
    ),
    "expected_target_generator": (
      expected_target_generator
    ),
    "expected_statement": (
      expected_statement
    ),
    "final_step": final_step,
  }


def test_phase74_6_reuses_phase74_5_singleton():
  data = build_phase74_6_data()

  assert isinstance(
    data[
      "singleton_step"
    ].conclusion,
    TodaLemma512BracketSingletonMod2Statement,
  )

  assert (
    data[
      "singleton_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_6_scope_is_n_at_least_6():
  data = build_phase74_6_data()

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


def test_phase74_6_derives_coefficient_stability():
  data = build_phase74_6_data()

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


def test_phase74_6_preserves_source_bracket():
  data = build_phase74_6_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .source_bracket
    == data[
      "singleton_step"
    ].conclusion
    .bracket
  )


def test_phase74_6_target_bracket_is_shifted_lemma512_bracket():
  data = build_phase74_6_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .target_bracket
    == data[
      "expected_target_bracket"
    ]
  )


def test_phase74_6_target_bracket_is_unindexed():
  data = build_phase74_6_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .target_bracket
    .index
    is None
  )


def test_phase74_6_target_first_is_eta_n_plus_one():
  data = build_phase74_6_data()

  target = (
    data[
      "final_step"
    ].conclusion
    .target_bracket
  )

  assert (
    target.first.generator
    == GeneratorSymbol(
      family="η",
      index=ScalarSum(
        left=data[
          "n"
        ],
        right=1,
      ),
    )
  )


def test_phase74_6_target_second_is_nu_n_plus_two():
  data = build_phase74_6_data()

  target = (
    data[
      "final_step"
    ].conclusion
    .target_bracket
  )

  assert (
    target.second.generator
    == GeneratorSymbol(
      family="ν",
      index=ScalarSum(
        left=data[
          "n"
        ],
        right=2,
      ),
    )
  )


def test_phase74_6_target_third_is_eta_n_plus_five():
  data = build_phase74_6_data()

  target = (
    data[
      "final_step"
    ].conclusion
    .target_bracket
  )

  assert (
    target.third.generator
    == GeneratorSymbol(
      family="η",
      index=ScalarSum(
        left=data[
          "n"
        ],
        right=5,
      ),
    )
  )


def test_phase74_6_preserves_source_generator():
  data = build_phase74_6_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .source_generator
    == data[
      "singleton_step"
    ].conclusion
    .generator
  )


def test_phase74_6_target_generator_is_nu_n_plus_one_squared():
  data = build_phase74_6_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .target_generator
    == data[
      "expected_target_generator"
    ]
  )

  assert isinstance(
    data[
      "final_step"
    ].conclusion
    .target_generator,
    Composition,
  )


def test_phase74_6_target_generator_factors_are_shifted_nu_family():
  data = build_phase74_6_data()

  generator = (
    data[
      "final_step"
    ].conclusion
    .target_generator
  )

  assert (
    generator.left.generator
    == GeneratorSymbol(
      family="ν",
      index=ScalarSum(
        left=data[
          "n"
        ],
        right=1,
      ),
    )
  )

  assert (
    generator.right.generator
    == GeneratorSymbol(
      family="ν",
      index=ScalarSum(
        left=data[
          "n"
        ],
        right=4,
      ),
    )
  )


def test_phase74_6_source_group_is_pi_n_plus_6_n():
  data = build_phase74_6_data()

  n = data[
    "n"
  ]

  assert (
    data[
      "final_step"
    ].conclusion
    .source_group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=6,
      ),
      sphere_dimension=n,
    )
  )


def test_phase74_6_target_group_is_pi_n_plus_7_n_plus_1():
  data = build_phase74_6_data()

  n = data[
    "n"
  ]

  assert (
    data[
      "final_step"
    ].conclusion
    .target_group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=7,
      ),
      sphere_dimension=ScalarSum(
        left=n,
        right=1,
      ),
    )
  )


def test_phase74_6_target_group_is_suspension_shift_of_source_group():
  data = build_phase74_6_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement.target_group.sphere_dimension
    == ScalarSum(
      left=(
        statement
        .source_group
        .sphere_dimension
      ),
      right=1,
    )
  )


def test_phase74_6_final_scope_remains_n_at_least_6():
  data = build_phase74_6_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .n_range
    == data[
      "n_ge_6_step"
    ].conclusion
  )


def test_phase74_6_final_step_uses_exact_two_premises():
  data = build_phase74_6_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "singleton_step"
      ],
      data[
        "n_ge_6_step"
      ],
    )
  )


def test_phase74_6_final_statement_not_present_initially():
  data = build_phase74_6_data()

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


def test_phase74_6_rejects_given_singleton():
  data = build_phase74_6_data()

  given_singleton = ProofStep(
    conclusion=(
      data[
        "singleton_step"
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
      given_singleton,
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_6_rejects_wrong_range():
  data = build_phase74_6_data()

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
        "singleton_step"
      ],
      wrong_range,
    ),
  ) is None


def test_phase74_6_rejects_wrong_source_generator():
  data = build_phase74_6_data()

  singleton = (
    data[
      "singleton_step"
    ].conclusion
  )

  source_generator = (
    singleton.generator
  )

  wrong_right = HomotopyElement(
    name="wrong ν",
    dimension=source_generator.right.dimension,
    source=source_generator.right.source,
    target=source_generator.right.target,
    generator=GeneratorSymbol(
      family="ν",
      index=ScalarSum(
        left=data[
          "n"
        ],
        right=4,
      ),
    ),
  )

  wrong_singleton = replace(
    singleton,
    generator=Composition(
      left=source_generator.left,
      right=wrong_right,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_singleton,
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
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_6_rejects_wrong_source_group():
  data = build_phase74_6_data()

  singleton = (
    data[
      "singleton_step"
    ].conclusion
  )

  wrong_singleton = replace(
    singleton,
    ambient_group=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=7,
      ),
      sphere_dimension=data[
        "n"
      ],
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_singleton,
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
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_6_rejects_wrong_bracket_second_entry():
  data = build_phase74_6_data()

  singleton = (
    data[
      "singleton_step"
    ].conclusion
  )

  bracket = singleton.bracket

  wrong_nu = HomotopyElement(
    name="wrong ν_(n+1)",
    dimension=bracket.second.dimension,
    source=bracket.second.source,
    target=bracket.second.target,
    generator=GeneratorSymbol(
      family="ν",
      index=ScalarSum(
        left=data[
          "n"
        ],
        right=2,
      ),
    ),
  )

  wrong_bracket = TodaBracket(
    first=bracket.first,
    second=wrong_nu,
    third=bracket.third,
  )

  wrong_singleton = replace(
    singleton,
    bracket=wrong_bracket,
  )

  wrong_step = ProofStep(
    conclusion=wrong_singleton,
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
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_6_rejects_indexed_source_bracket():
  data = build_phase74_6_data()

  singleton = (
    data[
      "singleton_step"
    ].conclusion
  )

  bracket = singleton.bracket

  indexed_bracket = TodaBracket(
    first=bracket.first,
    second=bracket.second,
    third=bracket.third,
    index=1,
  )

  wrong_singleton = replace(
    singleton,
    bracket=indexed_bracket,
  )

  wrong_step = ProofStep(
    conclusion=wrong_singleton,
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
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_6_coefficient_is_not_explicit_scalar_field():
  data = build_phase74_6_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert not hasattr(
    statement,
    "coefficient",
  )

  assert not hasattr(
    statement,
    "source_coefficient",
  )

  assert not hasattr(
    statement,
    "target_coefficient",
  )


def test_phase74_6_does_not_create_new_square_expression_type():
  data = build_phase74_6_data()

  assert type(
    data[
      "final_step"
    ].conclusion
    .source_generator
  ) is Composition

  assert type(
    data[
      "final_step"
    ].conclusion
    .target_generator
  ) is Composition


def test_phase74_6_reaches_fixed_point():
  data = build_phase74_6_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


