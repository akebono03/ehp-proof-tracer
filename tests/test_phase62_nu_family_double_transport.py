from dataclasses import replace

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Suspension,
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
from test_phase60_lemma54_integration import (
  build_phase60_9_data,
)
from toda_rules import (
  TodaNuFamilyDefinitionStatement,
  toda_55_nu_family_double_suspension_transport_inference_rule,
  toda_nu_family_definition_statement,
)


def build_phase62_3_data():
  phase60_9 = (
    build_phase60_9_data()
  )

  lemma54_step = (
    phase60_9[
      "integration_step"
    ]
  )

  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_nu_family_definition_statement(
      n
    )
  )

  definition_step = ProofStep(
    conclusion=definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  n_range = ScalarGreaterEqualStatement(
    left=n,
    right=5,
  )

  n_range_step = ProofStep(
    conclusion=n_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  expected_relation = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=definition.element,
    ),
    rhs=IteratedSuspension(
      expression=nu_prime,
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=3,
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  rule = (
    toda_55_nu_family_double_suspension_transport_inference_rule()
  )

  premise_steps = (
    lemma54_step,
    definition_step,
    n_range_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  transport_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_relation
    )
  )

  return {
    "phase60_9": phase60_9,
    "lemma54_step": lemma54_step,
    "n": n,
    "definition": definition,
    "definition_step": definition_step,
    "n_range": n_range,
    "n_range_step": n_range_step,
    "nu_prime": nu_prime,
    "expected_relation": expected_relation,
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "transport_step": transport_step,
  }


def test_phase62_3_reuses_derived_lemma54():
  data = build_phase62_3_data()

  assert (
    data[
      "lemma54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase62_3_uses_nu_family_definition():
  data = build_phase62_3_data()

  assert isinstance(
    data[
      "definition"
    ],
    TodaNuFamilyDefinitionStatement,
  )

  assert (
    data[
      "definition_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase62_3_rule_matches_dependencies():
  data = build_phase62_3_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase62_3_derives_double_nu_relation():
  data = build_phase62_3_data()

  step = data[
    "transport_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_relation"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase62_3_left_is_twice_nu_n():
  data = build_phase62_3_data()

  assert (
    data[
      "transport_step"
    ].conclusion.lhs
    == Multiple(
      coefficient=2,
      expression=(
        data[
          "definition"
        ].element
      ),
    )
  )


def test_phase62_3_right_is_e_n_minus_three_nu_prime():
  data = build_phase62_3_data()

  assert (
    data[
      "transport_step"
    ].conclusion.rhs
    == IteratedSuspension(
      expression=data[
        "nu_prime"
      ],
      exponent=ScalarSum(
        left=data[
          "n"
        ],
        right=ScalarProduct(
          left=-1,
          right=3,
        ),
      ),
    )
  )


def test_phase62_3_provenance_uses_exactly_three_premises():
  data = build_phase62_3_data()

  assert (
    data[
      "transport_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )


def test_phase62_3_rejects_given_lemma54():
  data = build_phase62_3_data()

  given_lemma54_step = ProofStep(
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
      given_lemma54_step,
      data[
        "definition_step"
      ],
      data[
        "n_range_step"
      ],
    ),
  ) is None


def test_phase62_3_rejects_n_at_least_four():
  data = build_phase62_3_data()

  wrong_range_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=4,
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
      wrong_range_step,
    ),
  ) is None


def test_phase62_3_rejects_mismatched_symbolic_index():
  data = build_phase62_3_data()

  q = ScalarSymbol(
    name="q",
  )

  wrong_range_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=q,
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
        "lemma54_step"
      ],
      data[
        "definition_step"
      ],
      wrong_range_step,
    ),
  ) is None


def test_phase62_3_rejects_wrong_nu_family_definition():
  data = build_phase62_3_data()

  definition = data[
    "definition"
  ]

  wrong_definition = replace(
    definition,
    iterated_suspension=IteratedSuspension(
      expression=(
        definition
        .iterated_suspension
        .expression
      ),
      exponent=ScalarSum(
        left=data[
          "n"
        ],
        right=-3,
      ),
    ),
  )

  wrong_definition_step = ProofStep(
    conclusion=wrong_definition,
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
      wrong_definition_step,
      data[
        "n_range_step"
      ],
    ),
  ) is None


def test_phase62_3_rejects_wrong_lemma54_double_relation():
  data = build_phase62_3_data()

  lemma54 = (
    data[
      "lemma54_step"
    ].conclusion
  )

  wrong_double_relation = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=Suspension(
        expression=lemma54.nu4,
      ),
    ),
    rhs=IteratedSuspension(
      expression=data[
        "nu_prime"
      ],
      exponent=3,
    ),
    relation_type=RelationType.EQUALITY,
  )

  wrong_lemma54 = replace(
    lemma54,
    double_suspension_relation=(
      wrong_double_relation
    ),
  )

  wrong_lemma54_step = ProofStep(
    conclusion=wrong_lemma54,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_lemma54_step,
      data[
        "definition_step"
      ],
      data[
        "n_range_step"
      ],
    ),
  ) is None


def test_phase62_3_final_result_is_not_given():
  data = build_phase62_3_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_relation"
    ]
    not in initial_conclusions
  )

  assert (
    data[
      "transport_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase62_3_reaches_fixed_point_in_one_round():
  data = build_phase62_3_data()

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
      "transport_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )


