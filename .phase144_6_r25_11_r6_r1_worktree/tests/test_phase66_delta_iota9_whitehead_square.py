from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
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
from test_phase66_delta_iota9_nu_expression import (
  build_phase66_3_data,
)
from test_phase66_whitehead_square_nu_expression import (
  build_phase66_4_data,
)
from toda_rules import (
  Toda58WhiteheadSquareUpToSignStatement,
  TodaDeltaImageUpToSignStatement,
  toda_58_delta_iota9_whitehead_square_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase66_5_data():
  phase66_3 = (
    build_phase66_3_data()
  )

  phase66_4 = (
    build_phase66_4_data()
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

  rule = (
    toda_58_delta_iota9_whitehead_square_inference_rule()
  )

  premise_steps = (
    delta_nu_step,
    whitehead_nu_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  expected_statement = (
    TodaDeltaImageUpToSignStatement(
      map=(
        delta_nu_step
        .conclusion
        .map
      ),
      element=(
        delta_nu_step
        .conclusion
        .element
      ),
      positive_value=(
        whitehead_nu_step
        .conclusion
        .whitehead_square
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
    "phase66_4": phase66_4,
    "delta_nu_step": delta_nu_step,
    "whitehead_nu_step": (
      whitehead_nu_step
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "expected_statement": (
      expected_statement
    ),
    "final_step": final_step,
  }


def test_phase66_5_reuses_phase66_3_delta_result():
  data = build_phase66_5_data()

  assert isinstance(
    data[
      "delta_nu_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )

  assert (
    data[
      "delta_nu_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase66_5_reuses_phase66_4_whitehead_result():
  data = build_phase66_5_data()

  assert isinstance(
    data[
      "whitehead_nu_step"
    ].conclusion,
    Toda58WhiteheadSquareUpToSignStatement,
  )

  assert (
    data[
      "whitehead_nu_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase66_5_common_positive_value_matches():
  data = build_phase66_5_data()

  assert (
    data[
      "delta_nu_step"
    ].conclusion.positive_value
    == data[
      "whitehead_nu_step"
    ].conclusion.positive_value
  )


def test_phase66_5_rule_matches_dependencies():
  data = build_phase66_5_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase66_5_derives_delta_whitehead_relation():
  data = build_phase66_5_data()

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


def test_phase66_5_delta_source_is_pi9_9():
  data = build_phase66_5_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement.map.source_group
    == TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=9,
    )
  )


def test_phase66_5_delta_target_is_pi7_4():
  data = build_phase66_5_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement.map.target_group
    == TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
    )
  )


def test_phase66_5_argument_is_iota9():
  data = build_phase66_5_data()

  assert (
    data[
      "final_step"
    ].conclusion.element
    == HomotopyElement(
      name="ι_9",
      dimension=9,
      generator=GeneratorSymbol(
        family="ι",
        index=9,
      ),
    )
  )


def test_phase66_5_positive_value_is_iota4_whitehead_square():
  data = build_phase66_5_data()

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
    ].conclusion.positive_value
    == WhiteheadProduct(
      left=iota_4,
      right=iota_4,
    )
  )


def test_phase66_5_preserves_delta_map_object():
  data = build_phase66_5_data()

  assert (
    data[
      "final_step"
    ].conclusion.map
    is data[
      "delta_nu_step"
    ].conclusion.map
  )


def test_phase66_5_preserves_iota9_object():
  data = build_phase66_5_data()

  assert (
    data[
      "final_step"
    ].conclusion.element
    is data[
      "delta_nu_step"
    ].conclusion.element
  )


def test_phase66_5_preserves_whitehead_object():
  data = build_phase66_5_data()

  assert (
    data[
      "final_step"
    ].conclusion.positive_value
    is data[
      "whitehead_nu_step"
    ].conclusion.whitehead_square
  )


def test_phase66_5_provenance_uses_exactly_two_premises():
  data = build_phase66_5_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "delta_nu_step"
      ],
      data[
        "whitehead_nu_step"
      ],
    )
  )


def test_phase66_5_rejects_given_delta_result():
  data = build_phase66_5_data()

  given_delta_step = ProofStep(
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
      given_delta_step,
      data[
        "whitehead_nu_step"
      ],
    ),
  ) is None


def test_phase66_5_rejects_given_whitehead_result():
  data = build_phase66_5_data()

  given_whitehead_step = ProofStep(
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
      given_whitehead_step,
    ),
  ) is None


def test_phase66_5_rejects_wrong_delta_source():
  data = build_phase66_5_data()

  delta_statement = (
    data[
      "delta_nu_step"
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
        "whitehead_nu_step"
      ],
    ),
  ) is None


def test_phase66_5_rejects_wrong_delta_target():
  data = build_phase66_5_data()

  delta_statement = (
    data[
      "delta_nu_step"
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
        "whitehead_nu_step"
      ],
    ),
  ) is None


def test_phase66_5_rejects_wrong_iota9():
  data = build_phase66_5_data()

  delta_statement = (
    data[
      "delta_nu_step"
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
        "whitehead_nu_step"
      ],
    ),
  ) is None


def test_phase66_5_rejects_wrong_whitehead_square():
  data = build_phase66_5_data()

  whitehead_statement = (
    data[
      "whitehead_nu_step"
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

  wrong_whitehead = replace(
    whitehead_statement,
    whitehead_square=WhiteheadProduct(
      left=iota_3,
      right=iota_3,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_whitehead,
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
    ),
  ) is None


def test_phase66_5_rejects_different_positive_representatives():
  data = build_phase66_5_data()

  whitehead_statement = (
    data[
      "whitehead_nu_step"
    ].conclusion
  )

  wrong_whitehead = replace(
    whitehead_statement,
    positive_value=Multiple(
      coefficient=2,
      expression=(
        whitehead_statement
        .positive_value
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_whitehead,
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
    ),
  ) is None


def test_phase66_5_final_result_is_not_given():
  data = build_phase66_5_data()

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


def test_phase66_5_reaches_fixed_point_in_one_round():
  data = build_phase66_5_data()

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


