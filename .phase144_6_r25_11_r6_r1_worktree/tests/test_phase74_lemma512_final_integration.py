from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  ScalarSum,
  TodaBracket,
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
from test_phase74_lemma512_coefficient_stability import (
  build_phase74_6_data,
)
from test_phase74_lemma512_nonzero_anchor import (
  build_phase74_7_data,
)
from toda_rules import (
  TodaLemma512BracketSingletonMod2Statement,
  TodaLemma512CoefficientStabilityStatement,
  TodaLemma512NonzeroAnchorStatement,
  TodaLemma512Statement,
  toda_eta_family_definition_statement,
  toda_lemma512_final_integration_inference_rule,
  toda_nu_family_definition_statement,
)


@lru_cache(maxsize=1)
def build_phase74_8_data():
  phase74_5 = (
    build_phase74_5_data()
  )

  phase74_6 = (
    build_phase74_6_data()
  )

  phase74_7 = (
    build_phase74_7_data()
  )

  singleton_step = (
    phase74_5[
      "final_step"
    ]
  )

  stability_step = (
    phase74_6[
      "final_step"
    ]
  )

  anchor_step = (
    phase74_7[
      "final_step"
    ]
  )

  rule = (
    toda_lemma512_final_integration_inference_rule()
  )

  premise_steps = (
    singleton_step,
    stability_step,
    anchor_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      premise_steps,
    )
  )

  expected_statement = (
    TodaLemma512Statement(
      bracket=(
        singleton_step
        .conclusion
        .bracket
      ),
      generator=(
        singleton_step
        .conclusion
        .generator
      ),
      n_range=(
        singleton_step
        .conclusion
        .n_range
      ),
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
    "phase74_6": phase74_6,
    "phase74_7": phase74_7,
    "singleton_step": singleton_step,
    "stability_step": stability_step,
    "anchor_step": anchor_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "expected_statement": (
      expected_statement
    ),
    "final_step": final_step,
  }


def test_phase74_8_reuses_singleton_mod2():
  data = build_phase74_8_data()

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


def test_phase74_8_reuses_coefficient_stability():
  data = build_phase74_8_data()

  assert isinstance(
    data[
      "stability_step"
    ].conclusion,
    TodaLemma512CoefficientStabilityStatement,
  )

  assert (
    data[
      "stability_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_8_reuses_nonzero_anchor():
  data = build_phase74_8_data()

  assert isinstance(
    data[
      "anchor_step"
    ].conclusion,
    TodaLemma512NonzeroAnchorStatement,
  )

  assert (
    data[
      "anchor_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_8_anchor_is_n8():
  data = build_phase74_8_data()

  assert (
    data[
      "anchor_step"
    ].conclusion
    .anchor_dimension
    == 8
  )


def test_phase74_8_derives_final_lemma512():
  data = build_phase74_8_data()

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


def test_phase74_8_final_bracket_matches_phase74_5():
  data = build_phase74_8_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .bracket
    == data[
      "singleton_step"
    ].conclusion
    .bracket
  )


def test_phase74_8_final_generator_matches_phase74_5():
  data = build_phase74_8_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .generator
    == data[
      "singleton_step"
    ].conclusion
    .generator
  )


def test_phase74_8_final_generator_is_composition():
  data = build_phase74_8_data()

  assert type(
    data[
      "final_step"
    ].conclusion
    .generator
  ) is Composition


def test_phase74_8_final_generator_is_symbolic_nu_n_squared():
  data = build_phase74_8_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  n = (
    statement
    .bracket
    .first
    .dimension
  )

  n_plus_three = ScalarSum(
    left=n,
    right=3,
  )

  n_plus_six = ScalarSum(
    left=n,
    right=6,
  )

  generator = (
    statement.generator
  )

  assert (
    generator.left
    == toda_nu_family_definition_statement(
      n
    ).element
  )

  assert isinstance(
    generator.right,
    HomotopyElement,
  )

  assert (
    generator.right.dimension
    == n_plus_three
  )

  assert (
    generator.right.source
    == n_plus_six
  )

  assert (
    generator.right.target
    == n_plus_three
  )

  assert (
    generator.right.generator
    == GeneratorSymbol(
      family="ν",
      index=n_plus_three,
    )
  )


def test_phase74_8_final_bracket_is_symbolic_lemma512_bracket():
  data = build_phase74_8_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  bracket = statement.bracket

  n = (
    bracket
    .first
    .dimension
  )

  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )

  n_plus_four = ScalarSum(
    left=n,
    right=4,
  )

  assert (
    bracket.first.generator
    == GeneratorSymbol(
      family="η",
      index=n,
    )
  )

  assert (
    bracket.second.generator
    == GeneratorSymbol(
      family="ν",
      index=n_plus_one,
    )
  )

  assert (
    bracket.third.generator
    == GeneratorSymbol(
      family="η",
      index=n_plus_four,
    )
  )


def test_phase74_8_final_bracket_is_unindexed():
  data = build_phase74_8_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .bracket
    .index
    is None
  )


def test_phase74_8_final_range_is_n_at_least_6():
  data = build_phase74_8_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  n = (
    statement
    .bracket
    .first
    .dimension
  )

  assert (
    statement.n_range
    == ScalarGreaterEqualStatement(
      left=n,
      right=6,
    )
  )


def test_phase74_8_final_step_uses_exact_three_premises():
  data = build_phase74_8_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "singleton_step"
      ],
      data[
        "stability_step"
      ],
      data[
        "anchor_step"
      ],
    )
  )


def test_phase74_8_final_statement_not_present_initially():
  data = build_phase74_8_data()

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


def test_phase74_8_rejects_given_singleton():
  data = build_phase74_8_data()

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
        "stability_step"
      ],
      data[
        "anchor_step"
      ],
    ),
  ) is None


def test_phase74_8_rejects_given_stability():
  data = build_phase74_8_data()

  given_stability = ProofStep(
    conclusion=(
      data[
        "stability_step"
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
        "singleton_step"
      ],
      given_stability,
      data[
        "anchor_step"
      ],
    ),
  ) is None


def test_phase74_8_rejects_given_anchor():
  data = build_phase74_8_data()

  given_anchor = ProofStep(
    conclusion=(
      data[
        "anchor_step"
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
        "singleton_step"
      ],
      data[
        "stability_step"
      ],
      given_anchor,
    ),
  ) is None


def test_phase74_8_rejects_wrong_anchor_dimension():
  data = build_phase74_8_data()

  anchor = (
    data[
      "anchor_step"
    ].conclusion
  )

  wrong_anchor = replace(
    anchor,
    anchor_dimension=7,
  )

  wrong_step = ProofStep(
    conclusion=wrong_anchor,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "singleton_step"
      ],
      data[
        "stability_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase74_8_rejects_wrong_anchor_bracket():
  data = build_phase74_8_data()

  anchor = (
    data[
      "anchor_step"
    ].conclusion
  )

  eta_8 = (
    toda_eta_family_definition_statement(
      8
    ).element
  )

  nu_9 = (
    toda_nu_family_definition_statement(
      9
    ).element
  )

  eta_13 = (
    toda_eta_family_definition_statement(
      13
    ).element
  )

  wrong_anchor = replace(
    anchor,
    bracket=TodaBracket(
      first=eta_8,
      second=nu_9,
      third=eta_13,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_anchor,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "singleton_step"
      ],
      data[
        "stability_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase74_8_rejects_wrong_anchor_generator():
  data = build_phase74_8_data()

  anchor = (
    data[
      "anchor_step"
    ].conclusion
  )

  wrong_anchor = replace(
    anchor,
    generator=Composition(
      left=(
        toda_nu_family_definition_statement(
          8
        ).element
      ),
      right=(
        toda_nu_family_definition_statement(
          12
        ).element
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_anchor,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "singleton_step"
      ],
      data[
        "stability_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase74_8_rejects_stability_for_different_source_bracket():
  data = build_phase74_8_data()

  stability = (
    data[
      "stability_step"
    ].conclusion
  )

  source_bracket = (
    stability.source_bracket
  )

  wrong_source_bracket = TodaBracket(
    first=source_bracket.first,
    second=source_bracket.second,
    third=HomotopyElement(
      name="wrong eta",
      dimension=(
        source_bracket
        .third
        .dimension
      ),
      source=(
        source_bracket
        .third
        .source
      ),
      target=(
        source_bracket
        .third
        .target
      ),
      generator=GeneratorSymbol(
        family="η",
        index=ScalarSum(
          left=(
            source_bracket
            .first
            .dimension
          ),
          right=5,
        ),
      ),
    ),
  )

  wrong_stability = replace(
    stability,
    source_bracket=wrong_source_bracket,
  )

  wrong_step = ProofStep(
    conclusion=wrong_stability,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "singleton_step"
      ],
      wrong_step,
      data[
        "anchor_step"
      ],
    ),
  ) is None


def test_phase74_8_rejects_stability_for_wrong_source_generator():
  data = build_phase74_8_data()

  stability = (
    data[
      "stability_step"
    ].conclusion
  )

  source_generator = (
    stability.source_generator
  )

  wrong_generator = Composition(
    left=source_generator.left,
    right=HomotopyElement(
      name="wrong nu",
      dimension=(
        source_generator
        .right
        .dimension
      ),
      source=(
        source_generator
        .right
        .source
      ),
      target=(
        source_generator
        .right
        .target
      ),
      generator=GeneratorSymbol(
        family="ν",
        index=ScalarSum(
          left=(
            data[
              "singleton_step"
            ].conclusion
            .bracket
            .first
            .dimension
          ),
          right=4,
        ),
      ),
    ),
  )

  wrong_stability = replace(
    stability,
    source_generator=wrong_generator,
  )

  wrong_step = ProofStep(
    conclusion=wrong_stability,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "singleton_step"
      ],
      wrong_step,
      data[
        "anchor_step"
      ],
    ),
  ) is None


def test_phase74_8_does_not_expose_coefficient_field():
  data = build_phase74_8_data()

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
    "x",
  )


def test_phase74_8_does_not_create_nu_square_class():
  data = build_phase74_8_data()

  assert type(
    data[
      "final_step"
    ].conclusion
    .generator
  ) is Composition


def test_phase74_8_reaches_fixed_point():
  data = build_phase74_8_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


