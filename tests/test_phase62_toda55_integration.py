from dataclasses import replace

from proof import (
  InferenceTerminationReason,
  LiteratureStatement,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase62_nu_family_eta_cube_bridge import (
  build_phase62_4_data,
)
from toda_rules import (
  Toda55NuFamilyFiniteDimensionalStatement,
  toda_55_nu_family_finite_dimensional_integration_inference_rule,
  toda_55_nu_family_literature_statements,
)


def build_phase62_6_data():
  phase62_4 = (
    build_phase62_4_data()
  )

  phase62_3 = (
    phase62_4[
      "phase62_3"
    ]
  )

  lemma54_step = (
    phase62_3[
      "lemma54_step"
    ]
  )

  definition_step = (
    phase62_3[
      "definition_step"
    ]
  )

  n_range_step = (
    phase62_3[
      "n_range_step"
    ]
  )

  double_nu_step = (
    phase62_3[
      "transport_step"
    ]
  )

  quadruple_nu_step = (
    phase62_4[
      "final_step"
    ]
  )

  literature_statements = (
    toda_55_nu_family_literature_statements()
  )

  expected_statement = (
    Toda55NuFamilyFiniteDimensionalStatement(
      nu_family_definition=(
        definition_step
        .conclusion
      ),
      lemma54_statement=(
        lemma54_step
        .conclusion
      ),
      n_range=(
        n_range_step
        .conclusion
      ),
      double_nu_relation=(
        double_nu_step
        .conclusion
      ),
      quadruple_nu_relation=(
        quadruple_nu_step
        .conclusion
      ),
      literature_statements=(
        literature_statements
      ),
    )
  )

  rule = (
    toda_55_nu_family_finite_dimensional_integration_inference_rule()
  )

  premise_steps = (
    lemma54_step,
    definition_step,
    n_range_step,
    double_nu_step,
    quadruple_nu_step,
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
    "phase62_4": phase62_4,
    "phase62_3": phase62_3,
    "lemma54_step": lemma54_step,
    "definition_step": definition_step,
    "n_range_step": n_range_step,
    "double_nu_step": double_nu_step,
    "quadruple_nu_step": (
      quadruple_nu_step
    ),
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


def test_phase62_6_reuses_derived_lemma54():
  data = build_phase62_6_data()

  assert (
    data[
      "lemma54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase62_6_definition_remains_explicit_given():
  data = build_phase62_6_data()

  assert (
    data[
      "definition_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase62_6_range_remains_explicit_given():
  data = build_phase62_6_data()

  assert (
    data[
      "n_range_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase62_6_double_nu_relation_is_derived():
  data = build_phase62_6_data()

  assert (
    data[
      "double_nu_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase62_6_quadruple_nu_relation_is_derived():
  data = build_phase62_6_data()

  assert (
    data[
      "quadruple_nu_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase62_6_rule_matches_dependencies():
  data = build_phase62_6_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase62_6_derives_finite_dimensional_aggregate():
  data = build_phase62_6_data()

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


def test_phase62_6_aggregate_preserves_definition():
  data = build_phase62_6_data()

  assert (
    data[
      "integration_step"
    ].conclusion.nu_family_definition
    == data[
      "definition_step"
    ].conclusion
  )


def test_phase62_6_aggregate_preserves_lemma54():
  data = build_phase62_6_data()

  assert (
    data[
      "integration_step"
    ].conclusion.lemma54_statement
    == data[
      "lemma54_step"
    ].conclusion
  )


def test_phase62_6_aggregate_preserves_range():
  data = build_phase62_6_data()

  assert (
    data[
      "integration_step"
    ].conclusion.n_range
    == data[
      "n_range_step"
    ].conclusion
  )


def test_phase62_6_aggregate_preserves_double_relation():
  data = build_phase62_6_data()

  assert (
    data[
      "integration_step"
    ].conclusion.double_nu_relation
    == data[
      "double_nu_step"
    ].conclusion
  )


def test_phase62_6_aggregate_preserves_quadruple_relation():
  data = build_phase62_6_data()

  assert (
    data[
      "integration_step"
    ].conclusion.quadruple_nu_relation
    == data[
      "quadruple_nu_step"
    ].conclusion
  )


def test_phase62_6_literature_is_first_class():
  data = build_phase62_6_data()

  assert (
    len(
      data[
        "literature_statements"
      ]
    )
    == 1
  )

  assert all(
    isinstance(
      statement,
      LiteratureStatement,
    )
    for statement in data[
      "literature_statements"
    ]
  )


def test_phase62_6_records_toda_55():
  data = build_phase62_6_data()

  statement = (
    data[
      "literature_statements"
    ][
      0
    ]
  )

  assert (
    statement.reference.locator
    == "Equation (5.5)"
  )

  assert (
    "ν_n:=E^(n-4)ν₄"
    in statement.statement
  )

  assert (
    "2ν_n=E^(n-3)ν′"
    in statement.statement
  )

  assert (
    "4ν_n=η_n∘η_(n+1)∘η_(n+2)"
    in statement.statement
  )


def test_phase62_6_direct_literature_excludes_stable_clause():
  data = build_phase62_6_data()

  statement = (
    data[
      "literature_statements"
    ][
      0
    ].statement
  )

  assert (
    "4ν=η³"
    not in statement
  )


def test_phase62_6_aggregate_contains_literature():
  data = build_phase62_6_data()

  assert (
    data[
      "integration_step"
    ].conclusion.literature_statements
    == data[
      "literature_statements"
    ]
  )


def test_phase62_6_preserves_phase60_literature():
  data = build_phase62_6_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    statement
    .lemma54_statement
    .literature_statements
    == data[
      "lemma54_step"
    ].conclusion.literature_statements
  )

  assert (
    len(
      statement
      .lemma54_statement
      .literature_statements
    )
    > 0
  )


def test_phase62_6_provenance_uses_exactly_five_premises():
  data = build_phase62_6_data()

  assert (
    data[
      "integration_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )


def test_phase62_6_rejects_given_lemma54():
  data = build_phase62_6_data()

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
      given_step,
      data[
        "definition_step"
      ],
      data[
        "n_range_step"
      ],
      data[
        "double_nu_step"
      ],
      data[
        "quadruple_nu_step"
      ],
    ),
  ) is None


def test_phase62_6_rejects_given_double_relation():
  data = build_phase62_6_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "double_nu_step"
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
        "lemma54_step"
      ],
      data[
        "definition_step"
      ],
      data[
        "n_range_step"
      ],
      given_step,
      data[
        "quadruple_nu_step"
      ],
    ),
  ) is None


def test_phase62_6_rejects_given_quadruple_relation():
  data = build_phase62_6_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "quadruple_nu_step"
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
        "lemma54_step"
      ],
      data[
        "definition_step"
      ],
      data[
        "n_range_step"
      ],
      data[
        "double_nu_step"
      ],
      given_step,
    ),
  ) is None


def test_phase62_6_rejects_different_nu4():
  data = build_phase62_6_data()

  wrong_lemma54 = replace(
    data[
      "lemma54_step"
    ].conclusion,
    nu4=(
      data[
        "phase62_3"
      ][
        "nu_prime"
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
      wrong_step,
      data[
        "definition_step"
      ],
      data[
        "n_range_step"
      ],
      data[
        "double_nu_step"
      ],
      data[
        "quadruple_nu_step"
      ],
    ),
  ) is None


def test_phase62_6_final_result_is_not_given():
  data = build_phase62_6_data()

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
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase62_6_reaches_fixed_point_in_one_round():
  data = build_phase62_6_data()

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
  


