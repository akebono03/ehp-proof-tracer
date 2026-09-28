from dataclasses import replace

from proof import (
  InferenceTerminationReason,
  LiteratureStatement,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase63_toda56_semantics import (
  build_phase63_4_data,
)
from toda_rules import (
  Toda56Nu4DecompositionStatement,
  toda_56_nu4_decomposition_integration_inference_rule,
  toda_56_nu4_decomposition_literature_statements,
)


def build_phase63_6_data():
  phase63_4 = (
    build_phase63_4_data()
  )

  phase63_3 = (
    phase63_4[
      "phase63_3"
    ]
  )

  phase63_2 = (
    phase63_3[
      "phase63_2"
    ]
  )

  decomposition_step = (
    phase63_4[
      "toda56_step"
    ]
  )

  lemma54_step = (
    phase63_2[
      "lemma54_step"
    ]
  )

  literature_statements = (
    toda_56_nu4_decomposition_literature_statements()
  )

  expected_statement = (
    Toda56Nu4DecompositionStatement(
      decomposition_isomorphism=(
        decomposition_step
        .conclusion
      ),
      lemma54_statement=(
        lemma54_step
        .conclusion
      ),
      literature_statements=(
        literature_statements
      ),
    )
  )

  rule = (
    toda_56_nu4_decomposition_integration_inference_rule()
  )

  premise_steps = (
    decomposition_step,
    lemma54_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  integration_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase63_4": phase63_4,
    "phase63_3": phase63_3,
    "phase63_2": phase63_2,
    "decomposition_step": (
      decomposition_step
    ),
    "lemma54_step": lemma54_step,
    "literature_statements": (
      literature_statements
    ),
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "integration_step": (
      integration_step
    ),
  }


def test_phase63_6_reuses_derived_toda56_semantics():
  data = build_phase63_6_data()

  assert (
    data[
      "decomposition_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase63_6_reuses_derived_lemma54():
  data = build_phase63_6_data()

  assert (
    data[
      "lemma54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase63_6_rule_matches_dependencies():
  data = build_phase63_6_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase63_6_derives_final_aggregate():
  data = build_phase63_6_data()

  assert (
    data[
      "integration_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "integration_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase63_6_preserves_toda56_semantics():
  data = build_phase63_6_data()

  assert (
    data[
      "integration_step"
    ]
    .conclusion
    .decomposition_isomorphism
    is data[
      "decomposition_step"
    ].conclusion
  )


def test_phase63_6_preserves_exact_lemma54():
  data = build_phase63_6_data()

  assert (
    data[
      "integration_step"
    ]
    .conclusion
    .lemma54_statement
    is data[
      "lemma54_step"
    ].conclusion
  )


def test_phase63_6_literature_is_first_class():
  data = build_phase63_6_data()

  statements = data[
    "literature_statements"
  ]

  assert (
    len(
      statements
    )
    == 1
  )

  assert all(
    isinstance(
      statement,
      LiteratureStatement,
    )
    for statement in statements
  )


def test_phase63_6_records_toda56_reference():
  data = build_phase63_6_data()

  statement = (
    data[
      "literature_statements"
    ][
      0
    ]
  )

  assert (
    statement.reference.label
    == "Toda (5.6)"
  )

  assert (
    statement.reference.locator
    == "Equation (5.6)"
  )


def test_phase63_6_literature_records_map_formula():
  data = build_phase63_6_data()

  statement = (
    data[
      "literature_statements"
    ][
      0
    ].statement
  )

  assert (
    "(α,β)↦Eα+ν₄∘β"
    in statement
  )


def test_phase63_6_literature_records_isomorphism():
  data = build_phase63_6_data()

  statement = (
    data[
      "literature_statements"
    ][
      0
    ].statement
  )

  assert (
    "π_(i-1)^3⊕π_i^7≅π_i^4"
    in statement
  )


def test_phase63_6_aggregate_contains_direct_literature():
  data = build_phase63_6_data()

  assert (
    data[
      "integration_step"
    ]
    .conclusion
    .literature_statements
    == data[
      "literature_statements"
    ]
  )


def test_phase63_6_preserves_phase60_literature():
  data = build_phase63_6_data()

  aggregate = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    aggregate
    .lemma54_statement
    .literature_statements
    == data[
      "lemma54_step"
    ]
    .conclusion
    .literature_statements
  )

  assert (
    len(
      aggregate
      .lemma54_statement
      .literature_statements
    )
    > 0
  )


def test_phase63_6_provenance_uses_exactly_two_premises():
  data = build_phase63_6_data()

  assert (
    data[
      "integration_step"
    ].premises
    == (
      data[
        "decomposition_step"
      ],
      data[
        "lemma54_step"
      ],
    )
  )


def test_phase63_6_rejects_given_toda56_semantics():
  data = build_phase63_6_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "decomposition_step"
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
        "lemma54_step"
      ],
    ),
  ) is None


def test_phase63_6_rejects_given_lemma54():
  data = build_phase63_6_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "lemma54_step"
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
        "decomposition_step"
      ],
      given_step,
    ),
  ) is None


def test_phase63_6_rejects_different_nu4():
  data = build_phase63_6_data()

  wrong_lemma54 = replace(
    data[
      "lemma54_step"
    ].conclusion,
    nu4=(
      data[
        "phase63_3"
      ][
        "second_variable"
      ]
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_lemma54,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "decomposition_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase63_6_final_result_is_not_given():
  data = build_phase63_6_data()

  assert (
    data[
      "integration_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase63_6_final_result_is_not_initial_input():
  data = build_phase63_6_data()

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


def test_phase63_6_reaches_fixed_point_in_one_round():
  data = build_phase63_6_data()

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
      "integration_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )


