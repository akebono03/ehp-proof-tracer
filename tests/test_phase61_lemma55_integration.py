from dataclasses import replace
from functools import lru_cache

from proof import (
  InferenceTerminationReason,
  LiteratureStatement,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase60_lemma54_integration import (
  build_phase60_9_data,
)
from test_phase61_lemma55_nu4_composition import (
  build_phase61_5_data,
)
from toda_rules import (
  TodaLemma55Statement,
  toda_lemma55_integration_inference_rule,
  toda_lemma55_literature_statements,
)


@lru_cache(maxsize=1)
def build_phase61_6_data():
  phase60_9 = (
    build_phase60_9_data()
  )

  phase61_5 = (
    build_phase61_5_data()
  )

  lemma54_step = (
    phase60_9[
      "integration_step"
    ]
  )

  phase61_3 = (
    phase61_5[
      "phase61_3"
    ]
  )

  beta_membership_step = (
    phase61_3[
      "beta_membership_step"
    ]
  )

  beta_eta_zero_step = (
    phase61_3[
      "beta_eta_zero_step"
    ]
  )

  t_range_step = (
    phase61_3[
      "t_range_step"
    ]
  )

  final_inclusion_step = (
    phase61_5[
      "final_step"
    ]
  )

  literature_statements = (
    toda_lemma55_literature_statements()
  )

  expected_statement = (
    TodaLemma55Statement(
      nu4=(
        lemma54_step
        .conclusion
        .nu4
      ),
      lemma54_statement=(
        lemma54_step
        .conclusion
      ),
      beta_membership=(
        beta_membership_step
        .conclusion
      ),
      beta_eta_zero_relation=(
        beta_eta_zero_step
        .conclusion
      ),
      t_range=(
        t_range_step
        .conclusion
      ),
      bracket_inclusion=(
        final_inclusion_step
        .conclusion
      ),
      literature_statements=(
        literature_statements
      ),
    )
  )

  rule = (
    toda_lemma55_integration_inference_rule()
  )

  premise_steps = (
    lemma54_step,
    beta_membership_step,
    beta_eta_zero_step,
    t_range_step,
    final_inclusion_step,
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
    "phase60_9": phase60_9,
    "phase61_5": phase61_5,
    "phase61_3": phase61_3,
    "lemma54_step": lemma54_step,
    "beta_membership_step": (
      beta_membership_step
    ),
    "beta_eta_zero_step": (
      beta_eta_zero_step
    ),
    "t_range_step": t_range_step,
    "final_inclusion_step": (
      final_inclusion_step
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


def test_phase61_6_reuses_derived_lemma54_aggregate():
  data = build_phase61_6_data()

  assert (
    data[
      "lemma54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase61_6_reuses_derived_final_inclusion():
  data = build_phase61_6_data()

  assert (
    data[
      "final_inclusion_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase61_6_rule_matches_dependencies():
  data = build_phase61_6_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase61_6_derives_lemma55_aggregate():
  data = build_phase61_6_data()

  step = data[
    "integration_step"
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


def test_phase61_6_aggregate_preserves_lemma54_nu4():
  data = build_phase61_6_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    statement.nu4
    == data[
      "lemma54_step"
    ].conclusion.nu4
  )

  assert (
    statement.lemma54_statement
    == data[
      "lemma54_step"
    ].conclusion
  )


def test_phase61_6_aggregate_preserves_hypotheses():
  data = build_phase61_6_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    statement.beta_membership
    == data[
      "beta_membership_step"
    ].conclusion
  )

  assert (
    statement.beta_eta_zero_relation
    == data[
      "beta_eta_zero_step"
    ].conclusion
  )

  assert (
    statement.t_range
    == data[
      "t_range_step"
    ].conclusion
  )


def test_phase61_6_aggregate_preserves_final_inclusion():
  data = build_phase61_6_data()

  assert (
    data[
      "integration_step"
    ].conclusion.bracket_inclusion
    == data[
      "final_inclusion_step"
    ].conclusion
  )


def test_phase61_6_literature_statements_are_first_class():
  data = build_phase61_6_data()

  assert all(
    isinstance(
      statement,
      LiteratureStatement,
    )
    for statement in data[
      "literature_statements"
    ]
  )


def test_phase61_6_literature_statements_are_not_empty():
  data = build_phase61_6_data()

  assert (
    len(
      data[
        "literature_statements"
      ]
    )
    == 2
  )

  assert all(
    statement.statement
    for statement in data[
      "literature_statements"
    ]
  )


def test_phase61_6_records_lemma55_statement():
  data = build_phase61_6_data()

  statement = next(
    item
    for item in data[
      "literature_statements"
    ]
    if (
      item.reference.locator
      == "Lemma 5.5"
    )
  )

  assert (
    "β∈π_(t+2)(S^m)"
    in statement.statement
  )

  assert (
    "E^2β∘E^tν₄"
    in statement.statement
  )


def test_phase61_6_records_lemma55_proof():
  data = build_phase61_6_data()

  statement = next(
    item
    for item in data[
      "literature_statements"
    ]
    if (
      item.reference.locator
      == "Lemma 5.5 proof"
    )
  )

  assert (
    "E^2β∘E^tα*"
    in statement.statement
  )

  assert (
    "E[ι₄,ι₄]=0"
    in statement.statement
  )

  assert (
    "E^tν₄=±E^tα*"
    in statement.statement
  )


def test_phase61_6_aggregate_contains_literature_statements():
  data = build_phase61_6_data()

  assert (
    data[
      "integration_step"
    ].conclusion.literature_statements
    == data[
      "literature_statements"
    ]
  )


def test_phase61_6_preserves_phase60_literature_through_lemma54():
  data = build_phase61_6_data()

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


def test_phase61_6_provenance_uses_exactly_five_premises():
  data = build_phase61_6_data()

  assert (
    data[
      "integration_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )


def test_phase61_6_final_derived_dependencies_are_inference():
  data = build_phase61_6_data()

  assert (
    data[
      "lemma54_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "final_inclusion_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase61_6_rejects_given_lemma54_aggregate():
  data = build_phase61_6_data()

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
        "beta_membership_step"
      ],
      data[
        "beta_eta_zero_step"
      ],
      data[
        "t_range_step"
      ],
      data[
        "final_inclusion_step"
      ],
    ),
  ) is None


def test_phase61_6_rejects_given_final_inclusion():
  data = build_phase61_6_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "final_inclusion_step"
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
        "beta_membership_step"
      ],
      data[
        "beta_eta_zero_step"
      ],
      data[
        "t_range_step"
      ],
      given_step,
    ),
  ) is None


def test_phase61_6_rejects_different_nu4():
  data = build_phase61_6_data()

  wrong_lemma54 = replace(
    data[
      "lemma54_step"
    ].conclusion,
    nu4=(
      data[
        "phase60_9"
      ][
        "phase60_8"
      ][
        "alpha_star"
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
        "beta_membership_step"
      ],
      data[
        "beta_eta_zero_step"
      ],
      data[
        "t_range_step"
      ],
      data[
        "final_inclusion_step"
      ],
    ),
  ) is None


def test_phase61_6_final_result_is_not_given():
  data = build_phase61_6_data()

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


def test_phase61_6_reaches_fixed_point_in_one_round():
  data = build_phase61_6_data()

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


