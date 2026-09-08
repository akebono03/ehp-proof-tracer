from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  IteratedSuspension,
  ScalarSymbol,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase61_lemma55_alpha_star_inclusion import (
  build_phase61_3_data,
)
from test_phase61_lemma55_nu4_suspension import (
  build_phase61_4_data,
)
from toda_rules import (
  TodaLemma55BracketContainsUpToSignStatement,
  TodaLemma55SuspensionUpToSignStatement,
  toda_lemma55_alpha_star_to_nu4_composition_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase61_5_data():
  phase61_3 = (
    build_phase61_3_data()
  )

  phase61_4 = (
    build_phase61_4_data()
  )

  alpha_star_inclusion_step = (
    phase61_3[
      "inclusion_step"
    ]
  )

  suspension_step = (
    phase61_4[
      "suspension_step"
    ]
  )

  beta = (
    phase61_3[
      "beta"
    ]
  )

  t = (
    phase61_3[
      "t"
    ]
  )

  nu4 = (
    phase61_4[
      "nu4"
    ]
  )

  expected_positive_value = Composition(
    left=IteratedSuspension(
      expression=beta,
      exponent=2,
    ),
    right=IteratedSuspension(
      expression=nu4,
      exponent=t,
    ),
  )

  expected_statement = (
    TodaLemma55BracketContainsUpToSignStatement(
      bracket=(
        alpha_star_inclusion_step
        .conclusion
        .bracket
      ),
      positive_value=(
        expected_positive_value
      ),
    )
  )

  rule = (
    toda_lemma55_alpha_star_to_nu4_composition_inference_rule()
  )

  premise_steps = (
    alpha_star_inclusion_step,
    suspension_step,
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
      == expected_statement
    )
  )

  return {
    "phase61_3": phase61_3,
    "phase61_4": phase61_4,
    "alpha_star_inclusion_step": (
      alpha_star_inclusion_step
    ),
    "suspension_step": suspension_step,
    "beta": beta,
    "t": t,
    "nu4": nu4,
    "expected_positive_value": (
      expected_positive_value
    ),
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "final_step": final_step,
  }


def test_phase61_5_reuses_derived_alpha_star_inclusion():
  data = build_phase61_5_data()

  assert (
    data[
      "alpha_star_inclusion_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase61_5_reuses_derived_nu4_suspension_relation():
  data = build_phase61_5_data()

  assert (
    data[
      "suspension_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase61_5_rule_matches_two_derived_dependencies():
  data = build_phase61_5_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase61_5_derives_nu4_bracket_inclusion():
  data = build_phase61_5_data()

  step = data[
    "final_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase61_5_preserves_bracket():
  data = build_phase61_5_data()

  assert (
    data[
      "final_step"
    ].conclusion.bracket
    == data[
      "alpha_star_inclusion_step"
    ].conclusion.bracket
  )


def test_phase61_5_positive_value_is_e2_beta_composed_with_et_nu4():
  data = build_phase61_5_data()

  assert (
    data[
      "final_step"
    ].conclusion.positive_value
    == Composition(
      left=IteratedSuspension(
        expression=data[
          "beta"
        ],
        exponent=2,
      ),
      right=IteratedSuspension(
        expression=data[
          "nu4"
        ],
        exponent=data[
          "t"
        ],
      ),
    )
  )


def test_phase61_5_replaces_only_alpha_star_factor():
  data = build_phase61_5_data()

  source_value = (
    data[
      "alpha_star_inclusion_step"
    ].conclusion.positive_value
  )

  final_value = (
    data[
      "final_step"
    ].conclusion.positive_value
  )

  assert (
    final_value.left
    == source_value.left
  )

  assert (
    final_value.right
    == data[
      "suspension_step"
    ].conclusion.left
  )


def test_phase61_5_provenance_uses_exactly_two_derived_premises():
  data = build_phase61_5_data()

  assert (
    data[
      "final_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in data[
      "final_step"
    ].premises
  )


def test_phase61_5_rejects_given_alpha_star_inclusion():
  data = build_phase61_5_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "alpha_star_inclusion_step"
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
        "suspension_step"
      ],
    ),
  ) is None


def test_phase61_5_rejects_given_suspension_relation():
  data = build_phase61_5_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "suspension_step"
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
        "alpha_star_inclusion_step"
      ],
      given_step,
    ),
  ) is None


def test_phase61_5_rejects_different_alpha_star_factor():
  data = build_phase61_5_data()

  wrong_alpha_star = (
    data[
      "phase61_3"
    ][
      "alpha_star"
    ]
  )

  wrong_t = ScalarSymbol(
    name="u",
  )

  wrong_statement = replace(
    data[
      "suspension_step"
    ].conclusion,
    positive_value=IteratedSuspension(
      expression=wrong_alpha_star,
      exponent=wrong_t,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "alpha_star_inclusion_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase61_5_rejects_different_t_on_nu4_suspension():
  data = build_phase61_5_data()

  wrong_statement = (
    TodaLemma55SuspensionUpToSignStatement(
      left=IteratedSuspension(
        expression=data[
          "nu4"
        ],
        exponent=ScalarSymbol(
          name="u",
        ),
      ),
      positive_value=(
        data[
          "suspension_step"
        ].conclusion.positive_value
      ),
    )
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "alpha_star_inclusion_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase61_5_final_result_is_not_given():
  data = build_phase61_5_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_statement"
    ]
    not in initial_conclusions
  )

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase61_5_reaches_fixed_point_in_one_round():
  data = build_phase61_5_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    result.round_count
    == 1
  )

  assert (
    data[
      "final_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )



