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
from homotopy_groups import (
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase60_nu4_whitehead_correction import (
  build_phase60_8_data,
)
from test_phase66_delta_iota9_nu_expression import (
  build_phase66_3_data,
)
from toda_rules import (
  Toda58WhiteheadSquareUpToSignStatement,
  TodaDeltaImageUpToSignStatement,
  TodaLemma54WhiteheadCorrectionDataStatement,
  toda_58_whitehead_square_nu_expression_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase66_4_data():
  phase66_3 = (
    build_phase66_3_data()
  )

  phase60_8 = (
    build_phase60_8_data()
  )

  delta_step = (
    phase66_3[
      "final_step"
    ]
  )

  whitehead_data_step = (
    phase60_8[
      "whitehead_data_step"
    ]
  )

  rule = (
    toda_58_whitehead_square_nu_expression_inference_rule()
  )

  premise_steps = (
    delta_step,
    whitehead_data_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  expected_statement = (
    Toda58WhiteheadSquareUpToSignStatement(
      whitehead_square=(
        whitehead_data_step
        .conclusion
        .whitehead_square
      ),
      positive_value=(
        delta_step
        .conclusion
        .positive_value
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
    "phase66_3": phase66_3,
    "phase60_8": phase60_8,
    "delta_step": delta_step,
    "whitehead_data_step": (
      whitehead_data_step
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "expected_statement": (
      expected_statement
    ),
    "final_step": final_step,
  }


def test_phase66_4_reuses_phase66_3_delta_result():
  data = build_phase66_4_data()

  assert isinstance(
    data[
      "delta_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )

  assert (
    data[
      "delta_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase66_4_reuses_phase60_whitehead_data():
  data = build_phase66_4_data()

  assert isinstance(
    data[
      "whitehead_data_step"
    ].conclusion,
    TodaLemma54WhiteheadCorrectionDataStatement,
  )

  assert (
    data[
      "whitehead_data_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase66_4_rule_matches_dependencies():
  data = build_phase66_4_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase66_4_derives_whitehead_square_connection():
  data = build_phase66_4_data()

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


def test_phase66_4_whitehead_square_is_iota4_square():
  data = build_phase66_4_data()

  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  assert (
    data[
      "final_step"
    ].conclusion.whitehead_square
    == WhiteheadProduct(
      left=iota_4,
      right=iota_4,
    )
  )


def test_phase66_4_positive_value_is_two_nu4_minus_e_nu_prime():
  data = build_phase66_4_data()

  phase66_3 = data[
    "phase66_3"
  ]

  phase66_2 = phase66_3[
    "phase66_2"
  ]

  assert (
    data[
      "final_step"
    ].conclusion.positive_value
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


def test_phase66_4_preserves_whitehead_object():
  data = build_phase66_4_data()

  assert (
    data[
      "final_step"
    ].conclusion.whitehead_square
    is data[
      "whitehead_data_step"
    ].conclusion.whitehead_square
  )


def test_phase66_4_preserves_nu_expression_object():
  data = build_phase66_4_data()

  assert (
    data[
      "final_step"
    ].conclusion.positive_value
    is data[
      "delta_step"
    ].conclusion.positive_value
  )


def test_phase66_4_provenance_uses_exactly_two_premises():
  data = build_phase66_4_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "delta_step"
      ],
      data[
        "whitehead_data_step"
      ],
    )
  )


def test_phase66_4_rejects_given_delta_result():
  data = build_phase66_4_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "delta_step"
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
        "whitehead_data_step"
      ],
    ),
  ) is None


def test_phase66_4_rejects_given_whitehead_data():
  data = build_phase66_4_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "whitehead_data_step"
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
        "delta_step"
      ],
      given_step,
    ),
  ) is None


def test_phase66_4_rejects_wrong_delta_source():
  data = build_phase66_4_data()

  delta_statement = (
    data[
      "delta_step"
    ].conclusion
  )

  wrong_delta = replace(
    delta_statement,
    map=TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=8,
      ),
      target_group=(
        delta_statement
        .map
        .target_group
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_delta,
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
        "whitehead_data_step"
      ],
    ),
  ) is None


def test_phase66_4_rejects_wrong_delta_target():
  data = build_phase66_4_data()

  delta_statement = (
    data[
      "delta_step"
    ].conclusion
  )

  wrong_delta = replace(
    delta_statement,
    map=TodaDeltaMap(
      source_group=(
        delta_statement
        .map
        .source_group
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=5,
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_delta,
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
        "whitehead_data_step"
      ],
    ),
  ) is None


def test_phase66_4_rejects_wrong_iota9():
  data = build_phase66_4_data()

  delta_statement = (
    data[
      "delta_step"
    ].conclusion
  )

  wrong_delta = replace(
    delta_statement,
    element=HomotopyElement(
      name="ι_8",
      dimension=8,
      generator=GeneratorSymbol(
        family="ι",
        index=8,
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_delta,
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
        "whitehead_data_step"
      ],
    ),
  ) is None


def test_phase66_4_rejects_wrong_nu_expression():
  data = build_phase66_4_data()

  delta_statement = (
    data[
      "delta_step"
    ].conclusion
  )

  wrong_delta = replace(
    delta_statement,
    positive_value=Multiple(
      coefficient=2,
      expression=(
        delta_statement
        .positive_value
        .left
        .expression
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_delta,
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
        "whitehead_data_step"
      ],
    ),
  ) is None


def test_phase66_4_rejects_wrong_whitehead_square():
  data = build_phase66_4_data()

  whitehead_data = (
    data[
      "whitehead_data_step"
    ].conclusion
  )

  iota_3 = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  wrong_data = replace(
    whitehead_data,
    whitehead_square=WhiteheadProduct(
      left=iota_3,
      right=iota_3,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_data,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "delta_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase66_4_final_result_is_not_given():
  data = build_phase66_4_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "expected_statement"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase66_4_reaches_fixed_point_in_one_round():
  data = build_phase66_4_data()

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
      "final_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )


