from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  Sum,
  Suspension,
  WhiteheadProduct,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase66_delta_iota9_nu_expression import (
  build_phase66_3_data,
)
from test_phase66_whitehead_square_nu_expression import (
  build_phase66_4_data,
)
from test_phase66_delta_iota9_whitehead_square import (
  build_phase66_5_data,
)
from toda_rules import (
  Toda58EquationStatement,
  Toda58WhiteheadSquareUpToSignStatement,
  TodaDeltaImageUpToSignStatement,
  toda_58_integration_inference_rule,
  toda_58_literature_statements,
)


@lru_cache(maxsize=1)
def build_phase66_7_data():
  phase66_3 = (
    build_phase66_3_data()
  )

  phase66_4 = (
    build_phase66_4_data()
  )

  phase66_5 = (
    build_phase66_5_data()
  )

  delta_nu_step = (
    phase66_3[
      "final_step"
    ]
  )

  whitehead_nu_step = (
    phase66_4[
      "final_step"
    ]
  )

  delta_whitehead_step = (
    phase66_5[
      "final_step"
    ]
  )

  expected_statement = (
    Toda58EquationStatement(
      delta_nu_relation=(
        delta_nu_step.conclusion
      ),
      whitehead_nu_relation=(
        whitehead_nu_step.conclusion
      ),
      delta_whitehead_relation=(
        delta_whitehead_step.conclusion
      ),
      literature_statements=(
        toda_58_literature_statements()
      ),
    )
  )

  rule = (
    toda_58_integration_inference_rule()
  )

  premise_steps = (
    delta_nu_step,
    whitehead_nu_step,
    delta_whitehead_step,
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
    "phase66_3": phase66_3,
    "phase66_4": phase66_4,
    "phase66_5": phase66_5,
    "delta_nu_step": delta_nu_step,
    "whitehead_nu_step": (
      whitehead_nu_step
    ),
    "delta_whitehead_step": (
      delta_whitehead_step
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


def test_phase66_7_reuses_three_derived_results():
  data = build_phase66_7_data()

  assert (
    data[
      "delta_nu_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "whitehead_nu_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "delta_whitehead_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase66_7_statement_types_are_expected():
  data = build_phase66_7_data()

  assert isinstance(
    data[
      "delta_nu_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )

  assert isinstance(
    data[
      "whitehead_nu_step"
    ].conclusion,
    Toda58WhiteheadSquareUpToSignStatement,
  )

  assert isinstance(
    data[
      "delta_whitehead_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )


def test_phase66_7_rule_matches_dependencies():
  data = build_phase66_7_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase66_7_derives_aggregate():
  data = build_phase66_7_data()

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


def test_phase66_7_aggregate_is_not_given():
  data = build_phase66_7_data()

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase66_7_preserves_delta_nu_object():
  data = build_phase66_7_data()

  assert (
    data[
      "integration_step"
    ].conclusion.delta_nu_relation
    is data[
      "delta_nu_step"
    ].conclusion
  )


def test_phase66_7_preserves_whitehead_nu_object():
  data = build_phase66_7_data()

  assert (
    data[
      "integration_step"
    ].conclusion.whitehead_nu_relation
    is data[
      "whitehead_nu_step"
    ].conclusion
  )


def test_phase66_7_preserves_delta_whitehead_object():
  data = build_phase66_7_data()

  assert (
    data[
      "integration_step"
    ].conclusion.delta_whitehead_relation
    is data[
      "delta_whitehead_step"
    ].conclusion
  )


def test_phase66_7_premises_are_exactly_three_results():
  data = build_phase66_7_data()

  assert (
    data[
      "integration_step"
    ].premises
    == (
      data[
        "delta_nu_step"
      ],
      data[
        "whitehead_nu_step"
      ],
      data[
        "delta_whitehead_step"
      ],
    )
  )


def test_phase66_7_literature_statement_is_toda58():
  data = build_phase66_7_data()

  literature = (
    data[
      "integration_step"
    ].conclusion
    .literature_statements
  )

  assert len(
    literature
  ) == 1

  assert (
    literature[
      0
    ].reference.label
    == "Toda (5.8)"
  )

  assert (
    literature[
      0
    ].reference.locator
    == "Equation (5.8)"
  )


def test_phase66_7_literature_reference_metadata():
  data = build_phase66_7_data()

  reference = (
    data[
      "integration_step"
    ].conclusion
    .literature_statements[
      0
    ]
    .reference
  )

  assert reference.author == "H. Toda"

  assert (
    reference.title
    == (
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    )
  )

  assert reference.year == 1962


def test_phase66_7_literature_statement_contains_equation():
  data = build_phase66_7_data()

  statement = (
    data[
      "integration_step"
    ].conclusion
    .literature_statements[
      0
    ]
    .statement
  )

  assert "Δ(ι₉)" in statement

  assert "2ν₄-Eν′" in statement

  assert "[ι₄,ι₄]" in statement


def test_phase66_7_delta_nu_relation_is_expected():
  data = build_phase66_7_data()

  relation = (
    data[
      "integration_step"
    ].conclusion
    .delta_nu_relation
  )

  phase66_2 = (
    data[
      "phase66_3"
    ][
      "phase66_2"
    ]
  )

  assert (
    relation.positive_value
    == Sum(
      left=Multiple(
        coefficient=2,
        expression=phase66_2[
          "nu_4"
        ],
      ),
      right=Multiple(
        coefficient=-1,
        expression=Suspension(
          expression=phase66_2[
            "nu_prime"
          ],
        ),
      ),
    )
  )


def test_phase66_7_whitehead_relation_is_expected():
  data = build_phase66_7_data()

  relation = (
    data[
      "integration_step"
    ].conclusion
    .whitehead_nu_relation
  )

  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  assert (
    relation.whitehead_square
    == WhiteheadProduct(
      left=iota_4,
      right=iota_4,
    )
  )


def test_phase66_7_delta_whitehead_relation_is_expected():
  data = build_phase66_7_data()

  aggregate = (
    data[
      "integration_step"
    ].conclusion
  )

  assert (
    aggregate
    .delta_whitehead_relation
    .positive_value
    == aggregate
    .whitehead_nu_relation
    .whitehead_square
  )


def test_phase66_7_rejects_given_delta_nu():
  data = build_phase66_7_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "delta_nu_step"
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
        "whitehead_nu_step"
      ],
      data[
        "delta_whitehead_step"
      ],
    ),
  ) is None


def test_phase66_7_rejects_given_whitehead_nu():
  data = build_phase66_7_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "whitehead_nu_step"
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
        "delta_nu_step"
      ],
      given_step,
      data[
        "delta_whitehead_step"
      ],
    ),
  ) is None


def test_phase66_7_rejects_given_delta_whitehead():
  data = build_phase66_7_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "delta_whitehead_step"
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
        "delta_nu_step"
      ],
      data[
        "whitehead_nu_step"
      ],
      given_step,
    ),
  ) is None


def test_phase66_7_rejects_wrong_common_nu_expression():
  data = build_phase66_7_data()

  whitehead_relation = (
    data[
      "whitehead_nu_step"
    ].conclusion
  )

  wrong_relation = replace(
    whitehead_relation,
    positive_value=Multiple(
      coefficient=2,
      expression=(
        whitehead_relation
        .positive_value
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "delta_nu_step"
      ],
      wrong_step,
      data[
        "delta_whitehead_step"
      ],
    ),
  ) is None


def test_phase66_7_rejects_wrong_final_whitehead_value():
  data = build_phase66_7_data()

  delta_whitehead_relation = (
    data[
      "delta_whitehead_step"
    ].conclusion
  )

  wrong_relation = replace(
    delta_whitehead_relation,
    positive_value=(
      data[
        "delta_nu_step"
      ].conclusion
      .positive_value
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "delta_nu_step"
      ],
      data[
        "whitehead_nu_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase66_7_reaches_fixed_point_in_one_round():
  data = build_phase66_7_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert (
    data[
      "integration_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )


