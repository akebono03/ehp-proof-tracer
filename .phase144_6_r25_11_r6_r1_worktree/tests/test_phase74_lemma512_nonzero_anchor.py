from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  TodaBracket,
  Zero,
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
from test_phase62_toda55_integration import (
  build_phase62_6_data,
)
from test_phase68_nu_n_eta_n_plus_three_zero import (
  build_phase68_9_data,
)
from test_phase74_lemma512_bracket_singleton_mod2 import (
  build_phase74_5_data,
)
from toda_rules import (
  Toda55NuFamilyFiniteDimensionalStatement,
  TodaLemma55BracketContainsUpToSignStatement,
  TodaLemma512BracketSingletonMod2Statement,
  TodaLemma512NonzeroAnchorStatement,
  toda_eta_family_definition_statement,
  toda_lemma512_lemma55_n8_inclusion_inference_rule,
  toda_lemma512_nonzero_anchor_inference_rule,
  toda_nu_family_definition_statement,
)


@lru_cache(maxsize=1)
def build_phase74_7_data():
  phase62_6 = (
    build_phase62_6_data()
  )

  phase68_9 = (
    build_phase68_9_data()
  )

  phase74_5 = (
    build_phase74_5_data()
  )

  nu_family_step = (
    phase62_6[
      "integration_step"
    ]
  )

  nu6_eta9_zero_step = (
    phase68_9[
      "nu6_eta9_zero_step"
    ]
  )

  singleton_step = (
    phase74_5[
      "final_step"
    ]
  )

  inclusion_rule = (
    toda_lemma512_lemma55_n8_inclusion_inference_rule()
  )

  anchor_rule = (
    toda_lemma512_nonzero_anchor_inference_rule()
  )

  rules = (
    inclusion_rule,
    anchor_rule,
  )

  premise_steps = (
    nu_family_step,
    nu6_eta9_zero_step,
    singleton_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
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

  eta_12 = (
    toda_eta_family_definition_statement(
      12
    ).element
  )

  nu_8 = (
    toda_nu_family_definition_statement(
      8
    ).element
  )

  nu_11 = (
    toda_nu_family_definition_statement(
      11
    ).element
  )

  nu8_squared = Composition(
    left=nu_8,
    right=nu_11,
  )

  expected_indexed_bracket = TodaBracket(
    first=eta_8,
    second=nu_9,
    third=eta_12,
    index=3,
  )

  expected_inclusion = (
    TodaLemma55BracketContainsUpToSignStatement(
      bracket=expected_indexed_bracket,
      positive_value=nu8_squared,
    )
  )

  inclusion_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_inclusion
    )
  )

  expected_ordinary_bracket = TodaBracket(
    first=eta_8,
    second=nu_9,
    third=eta_12,
  )

  expected_anchor = (
    TodaLemma512NonzeroAnchorStatement(
      bracket=expected_ordinary_bracket,
      generator=nu8_squared,
      anchor_dimension=8,
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_anchor
    )
  )

  return {
    "phase62_6": phase62_6,
    "phase68_9": phase68_9,
    "phase74_5": phase74_5,
    "nu_family_step": nu_family_step,
    "nu6_eta9_zero_step": (
      nu6_eta9_zero_step
    ),
    "singleton_step": singleton_step,
    "inclusion_rule": inclusion_rule,
    "anchor_rule": anchor_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "eta_8": eta_8,
    "nu_9": nu_9,
    "eta_12": eta_12,
    "nu_8": nu_8,
    "nu_11": nu_11,
    "nu8_squared": nu8_squared,
    "expected_indexed_bracket": (
      expected_indexed_bracket
    ),
    "expected_inclusion": (
      expected_inclusion
    ),
    "inclusion_step": inclusion_step,
    "expected_ordinary_bracket": (
      expected_ordinary_bracket
    ),
    "expected_anchor": expected_anchor,
    "final_step": final_step,
  }


def test_phase74_7_reuses_derived_nu_family():
  data = build_phase74_7_data()

  assert isinstance(
    data[
      "nu_family_step"
    ].conclusion,
    Toda55NuFamilyFiniteDimensionalStatement,
  )

  assert (
    data[
      "nu_family_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_7_reuses_derived_nu6_eta9_zero():
  data = build_phase74_7_data()

  assert (
    data[
      "nu6_eta9_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "nu6_eta9_zero_step"
    ].conclusion
    == Relation(
      lhs=Composition(
        left=(
          toda_nu_family_definition_statement(
            6
          ).element
        ),
        right=(
          toda_eta_family_definition_statement(
            9
          ).element
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )


def test_phase74_7_reuses_phase74_5_singleton():
  data = build_phase74_7_data()

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


def test_phase74_7_derives_lemma55_n8_inclusion():
  data = build_phase74_7_data()

  assert (
    data[
      "inclusion_step"
    ].conclusion
    == data[
      "expected_inclusion"
    ]
  )

  assert (
    data[
      "inclusion_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_7_lemma55_bracket_has_index_three():
  data = build_phase74_7_data()

  assert (
    data[
      "inclusion_step"
    ].conclusion
    .bracket
    .index
    == 3
  )


def test_phase74_7_lemma55_bracket_is_eta8_nu9_eta12():
  data = build_phase74_7_data()

  bracket = (
    data[
      "inclusion_step"
    ].conclusion
    .bracket
  )

  assert (
    bracket.first
    == data[
      "eta_8"
    ]
  )

  assert (
    bracket.second
    == data[
      "nu_9"
    ]
  )

  assert (
    bracket.third
    == data[
      "eta_12"
    ]
  )


def test_phase74_7_lemma55_positive_value_is_nu8_squared():
  data = build_phase74_7_data()

  assert (
    data[
      "inclusion_step"
    ].conclusion
    .positive_value
    == data[
      "nu8_squared"
    ]
  )


def test_phase74_7_nu8_squared_is_composition():
  data = build_phase74_7_data()

  generator = (
    data[
      "nu8_squared"
    ]
  )

  assert type(
    generator
  ) is Composition

  assert (
    generator.left
    == data[
      "nu_8"
    ]
  )

  assert (
    generator.right
    == data[
      "nu_11"
    ]
  )


def test_phase74_7_inclusion_uses_exact_two_premises():
  data = build_phase74_7_data()

  assert (
    data[
      "inclusion_step"
    ].premises
    == (
      data[
        "nu_family_step"
      ],
      data[
        "nu6_eta9_zero_step"
      ],
    )
  )


def test_phase74_7_derives_nonzero_anchor():
  data = build_phase74_7_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_anchor"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_7_anchor_dimension_is_eight():
  data = build_phase74_7_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .anchor_dimension
    == 8
  )


def test_phase74_7_anchor_bracket_is_ordinary():
  data = build_phase74_7_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .bracket
    .index
    is None
  )


def test_phase74_7_anchor_bracket_is_eta8_nu9_eta12():
  data = build_phase74_7_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .bracket
    == data[
      "expected_ordinary_bracket"
    ]
  )


def test_phase74_7_anchor_generator_is_nu8_squared():
  data = build_phase74_7_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .generator
    == data[
      "nu8_squared"
    ]
  )


def test_phase74_7_anchor_uses_exact_two_premises():
  data = build_phase74_7_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "inclusion_step"
      ],
      data[
        "singleton_step"
      ],
    )
  )


def test_phase74_7_final_statement_not_present_initially():
  data = build_phase74_7_data()

  assert (
    data[
      "expected_anchor"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase74_7_rejects_given_nu_family():
  data = build_phase74_7_data()

  given_nu_family = ProofStep(
    conclusion=(
      data[
        "nu_family_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "inclusion_rule"
    ],
    (
      given_nu_family,
      data[
        "nu6_eta9_zero_step"
      ],
    ),
  ) is None


def test_phase74_7_rejects_given_nu6_eta9_zero():
  data = build_phase74_7_data()

  given_zero = ProofStep(
    conclusion=(
      data[
        "nu6_eta9_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "inclusion_rule"
    ],
    (
      data[
        "nu_family_step"
      ],
      given_zero,
    ),
  ) is None


def test_phase74_7_rejects_wrong_zero_relation():
  data = build_phase74_7_data()

  wrong_zero = ProofStep(
    conclusion=Relation(
      lhs=Composition(
        left=(
          toda_nu_family_definition_statement(
            6
          ).element
        ),
        right=(
          toda_eta_family_definition_statement(
            10
          ).element
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "inclusion_rule"
    ],
    (
      data[
        "nu_family_step"
      ],
      wrong_zero,
    ),
  ) is None


def test_phase74_7_rejects_given_lemma55_inclusion():
  data = build_phase74_7_data()

  given_inclusion = ProofStep(
    conclusion=(
      data[
        "inclusion_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "anchor_rule"
    ],
    (
      given_inclusion,
      data[
        "singleton_step"
      ],
    ),
  ) is None


def test_phase74_7_rejects_wrong_indexed_bracket():
  data = build_phase74_7_data()

  inclusion = (
    data[
      "inclusion_step"
    ].conclusion
  )

  wrong_bracket = TodaBracket(
    first=inclusion.bracket.first,
    second=inclusion.bracket.second,
    third=inclusion.bracket.third,
    index=2,
  )

  wrong_inclusion = replace(
    inclusion,
    bracket=wrong_bracket,
  )

  wrong_step = ProofStep(
    conclusion=wrong_inclusion,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "anchor_rule"
    ],
    (
      wrong_step,
      data[
        "singleton_step"
      ],
    ),
  ) is None


def test_phase74_7_rejects_wrong_positive_value():
  data = build_phase74_7_data()

  inclusion = (
    data[
      "inclusion_step"
    ].conclusion
  )

  wrong_value = Composition(
    left=data[
      "nu_8"
    ],
    right=(
      toda_nu_family_definition_statement(
        12
      ).element
    ),
  )

  wrong_inclusion = replace(
    inclusion,
    positive_value=wrong_value,
  )

  wrong_step = ProofStep(
    conclusion=wrong_inclusion,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "anchor_rule"
    ],
    (
      wrong_step,
      data[
        "singleton_step"
      ],
    ),
  ) is None


def test_phase74_7_rejects_given_singleton():
  data = build_phase74_7_data()

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
      "anchor_rule"
    ],
    (
      data[
        "inclusion_step"
      ],
      given_singleton,
    ),
  ) is None


def test_phase74_7_does_not_use_coefficient_stability_as_direct_premise():
  data = build_phase74_7_data()

  assert len(
    data[
      "final_step"
    ].premises
  ) == 2

  assert (
    data[
      "final_step"
    ].premises[
      0
    ]
    is data[
      "inclusion_step"
    ]
  )

  assert (
    data[
      "final_step"
    ].premises[
      1
    ]
    is data[
      "singleton_step"
    ]
  )


def test_phase74_7_reaches_fixed_point():
  data = build_phase74_7_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )



