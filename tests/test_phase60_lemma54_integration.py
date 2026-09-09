from functools import lru_cache

from proof import (
  InferenceTerminationReason,
  LiteratureStatement,
  ProofRule,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase60_nu4_whitehead_correction import (
  build_phase60_8_data,
)
from toda_rules import (
  TodaLemma54Statement,
  toda_lemma54_integration_inference_rule,
  toda_lemma54_literature_statements,
)


@lru_cache(maxsize=1)
def build_phase60_9_data():
  phase60_8 = (
    build_phase60_8_data()
  )

  membership_step = (
    phase60_8[
      "membership_step"
    ]
  )

  hopf_step = (
    phase60_8[
      "hopf_step"
    ]
  )

  double_step = (
    phase60_8[
      "double_result_step"
    ]
  )

  literature_statements = (
    toda_lemma54_literature_statements()
  )

  expected_statement = (
    TodaLemma54Statement(
      nu4=phase60_8[
        "nu4"
      ],
      membership=(
        membership_step
        .conclusion
      ),
      hopf_relation=(
        hopf_step
        .conclusion
      ),
      double_suspension_relation=(
        double_step
        .conclusion
      ),
      literature_statements=(
        literature_statements
      ),
    )
  )

  rule = (
    toda_lemma54_integration_inference_rule()
  )

  premise_steps = (
    membership_step,
    hopf_step,
    double_step,
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
    "phase60_8": phase60_8,
    "membership_step": membership_step,
    "hopf_step": hopf_step,
    "double_step": double_step,
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


def test_phase60_9_reuses_derived_membership():
  data = build_phase60_9_data()

  assert (
    data[
      "membership_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_9_reuses_derived_hopf_relation():
  data = build_phase60_9_data()

  assert (
    data[
      "hopf_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_9_reuses_derived_double_suspension():
  data = build_phase60_9_data()

  assert (
    data[
      "double_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_9_integration_rule_matches_three_results():
  data = build_phase60_9_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase60_9_derives_lemma54_aggregate():
  data = build_phase60_9_data()

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


def test_phase60_9_aggregate_preserves_nu4():
  data = build_phase60_9_data()

  assert (
    data[
      "integration_step"
    ].conclusion.nu4
    == data[
      "phase60_8"
    ][
      "nu4"
    ]
  )


def test_phase60_9_aggregate_preserves_three_conclusions():
  data = build_phase60_9_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    statement.membership
    == data[
      "membership_step"
    ].conclusion
  )

  assert (
    statement.hopf_relation
    == data[
      "hopf_step"
    ].conclusion
  )

  assert (
    statement.double_suspension_relation
    == data[
      "double_step"
    ].conclusion
  )


def test_phase60_9_literature_statements_are_first_class():
  data = build_phase60_9_data()

  assert all(
    isinstance(
      statement,
      LiteratureStatement,
    )
    for statement in data[
      "literature_statements"
    ]
  )


def test_phase60_9_literature_statements_are_not_empty():
  data = build_phase60_9_data()

  assert (
    len(
      data[
        "literature_statements"
      ]
    )
    > 0
  )

  assert all(
    statement.statement
    for statement in data[
      "literature_statements"
    ]
  )


def test_phase60_9_records_theorem36_statement():
  data = build_phase60_9_data()

  theorem36 = next(
    statement
    for statement in data[
      "literature_statements"
    ]
    if (
      statement.reference.locator
      == "Theorem 3.6"
    )
  )

  assert (
    "α=η₂"
    in theorem36.statement
  )

  assert (
    "α*∈π_7^4"
    in theorem36.statement
  )


def test_phase60_9_records_prop13_statement():
  data = build_phase60_9_data()

  prop13 = next(
    statement
    for statement in data[
      "literature_statements"
    ]
    if (
      statement.reference.locator
      == "Proposition 1.3"
    )
  )

  assert (
    "-E{α,E^nβ,E^nγ}_n"
    in prop13.statement
  )


def test_phase60_9_records_toda115_statement():
  data = build_phase60_9_data()

  statement = next(
    item
    for item in data[
      "literature_statements"
    ]
    if (
      item.reference.locator
      == "Equation (1.15)"
    )
  )

  assert (
    "{α,E^nβ,E^nγ}_n"
    in statement.statement
  )


def test_phase60_9_records_toda32_statement():
  data = build_phase60_9_data()

  statement = next(
    item
    for item in data[
      "literature_statements"
    ]
    if (
      item.reference.locator
      == "Equation (3.2)"
    )
  )

  assert (
    "isomorphism"
    in statement.statement
  )

  assert (
    "surjective"
    in statement.statement
  )


def test_phase60_9_records_prop53_statement():
  data = build_phase60_9_data()

  statement = next(
    item
    for item in data[
      "literature_statements"
    ]
    if (
      item.reference.locator
      == "Proposition 5.3"
    )
  )

  assert (
    "π_(n+2)^n"
    in statement.statement
  )


def test_phase60_9_records_toda53_statement():
  data = build_phase60_9_data()

  statement = next(
    item
    for item in data[
      "literature_statements"
    ]
    if (
      item.reference.locator
      == "Equation (5.3)"
    )
  )

  assert (
    "2ν′"
    in statement.statement
  )


def test_phase60_9_records_toda54_statement():
  data = build_phase60_9_data()

  statement = next(
    item
    for item in data[
      "literature_statements"
    ]
    if (
      item.reference.locator
      == "Equation (5.4)"
    )
  )

  assert (
    "±E^(n-3)ν′"
    in statement.statement
  )


def test_phase60_9_aggregate_contains_literature_statements():
  data = build_phase60_9_data()

  assert (
    data[
      "integration_step"
    ].conclusion.literature_statements
    == data[
      "literature_statements"
    ]
  )


def test_phase60_9_provenance_uses_exactly_phase60_8_results():
  data = build_phase60_9_data()

  assert (
    data[
      "integration_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )


def test_phase60_9_final_result_is_not_given():
  data = build_phase60_9_data()

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase60_9_reaches_fixed_point_in_one_round():
  data = build_phase60_9_data()

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


