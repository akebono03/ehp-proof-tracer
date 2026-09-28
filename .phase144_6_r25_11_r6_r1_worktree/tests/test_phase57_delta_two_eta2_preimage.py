from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
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
from test_phase52_delta_direct_bridge import (
  build_phase52_2_data,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaDeltaPreimageUpToSignStatement,
  toda_lemma52_delta_two_eta2_preimage_inference_rule,
)


def build_phase57_4_data():
  phase52 = (
    build_phase52_2_data()
  )

  delta_whitehead_step = ProofStep(
    conclusion=(
      phase52[
        "delta_whitehead_up_to_sign"
      ]
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  whitehead_two_eta2_step = ProofStep(
    conclusion=(
      phase52[
        "whitehead_two_eta_2_up_to_sign"
      ]
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  from toda_rules import (
    toda_delta_iota5_two_eta2_up_to_sign_inference_rule,
  )

  phase52_rule = (
    toda_delta_iota5_two_eta2_up_to_sign_inference_rule()
  )

  phase52_result = (
    run_inference_until_stable_with_history(
      phase52_rule,
      (
        delta_whitehead_step,
        whitehead_two_eta2_step,
      ),
    )
  )

  delta_statement_step = next(
    step
    for step in phase52_result.steps
    if (
      step.conclusion
      == phase52[
        "delta_two_eta_2_up_to_sign"
      ]
    )
  )

  expected_statement = (
    TodaDeltaPreimageUpToSignStatement(
      map=phase52[
        "delta_map"
      ],
      value=phase52[
        "two_eta_2"
      ],
      positive_preimage=phase52[
        "iota_5"
      ],
    )
  )

  rule = (
    toda_lemma52_delta_two_eta2_preimage_inference_rule()
  )

  return {
    "phase52": phase52,
    "phase52_result": phase52_result,
    "delta_whitehead_step": (
      delta_whitehead_step
    ),
    "whitehead_two_eta2_step": (
      whitehead_two_eta2_step
    ),
    "delta_statement": (
      phase52[
        "delta_two_eta_2_up_to_sign"
      ]
    ),
    "delta_statement_step": (
      delta_statement_step
    ),
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
  }


def phase52_rule():
  from toda_rules import (
    toda_delta_iota5_two_eta2_up_to_sign_inference_rule,
  )

  return (
    toda_delta_iota5_two_eta2_up_to_sign_inference_rule()
  )


def test_phase57_4_preimage_statement_is_representable():
  data = build_phase57_4_data()

  assert isinstance(
    data[
      "expected_statement"
    ],
    TodaDeltaPreimageUpToSignStatement,
  )


def test_phase57_4_preimage_statement_preserves_specific_delta_map():
  data = build_phase57_4_data()

  statement = (
    data[
      "expected_statement"
    ]
  )

  assert (
    statement.map
    == data[
      "phase52"
    ][
      "delta_map"
    ]
  )

  assert (
    statement.map.source_group
    == TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )
  )

  assert (
    statement.map.target_group
    == TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )
  )


def test_phase57_4_preimage_value_is_two_eta2():
  data = build_phase57_4_data()

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  assert (
    data[
      "expected_statement"
    ].value
    == Multiple(
      coefficient=2,
      expression=eta_2,
    )
  )


def test_phase57_4_positive_preimage_is_iota5():
  data = build_phase57_4_data()

  iota_5 = HomotopyElement(
    name="ι_5",
    dimension=5,
    generator=GeneratorSymbol(
      family="ι",
      index=5,
    ),
  )

  assert (
    data[
      "expected_statement"
    ].positive_preimage
    == iota_5
  )


def test_phase57_4_rule_matches_derived_delta_relation():
  data = build_phase57_4_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "delta_statement_step"
      ],
    ),
  ) is not None


def test_phase57_4_rule_derives_delta_preimage_statement():
  data = build_phase57_4_data()

  result = (
    run_inference_until_stable_with_history(
      data[
        "rule"
      ],
      (
        data[
          "delta_statement_step"
        ],
      ),
    )
  )

  steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == data[
        "expected_statement"
      ]
    )
  )

  assert len(
    steps
  ) == 1


def test_phase57_4_result_is_inference():
  data = build_phase57_4_data()

  result = (
    run_inference_until_stable_with_history(
      data[
        "rule"
      ],
      (
        data[
          "delta_statement_step"
        ],
      ),
    )
  )

  step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == data[
        "expected_statement"
      ]
    )
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert (
    step.inference_rule
    == data[
      "rule"
    ]
  )


def test_phase57_4_preserves_phase52_provenance():
  data = build_phase57_4_data()

  result = (
    run_inference_until_stable_with_history(
      data[
        "rule"
      ],
      (
        data[
          "delta_statement_step"
        ],
      ),
    )
  )

  step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == data[
        "expected_statement"
      ]
    )
  )

  assert step.premises == (
    data[
      "delta_statement_step"
    ],
  )

  assert (
    data[
      "delta_statement_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase57_4_rejects_given_delta_relation():
  data = build_phase57_4_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "delta_statement"
      ]
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
    ),
  ) is None


def test_phase57_4_rejects_wrong_delta_source():
  data = build_phase57_4_data()

  wrong_map = TodaDeltaMap(
    source_group=TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=5,
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    ),
  )

  wrong_statement = (
    TodaDeltaImageUpToSignStatement(
      map=wrong_map,
      element=(
        data[
          "phase52"
        ][
          "iota_5"
        ]
      ),
      positive_value=(
        data[
          "phase52"
        ][
          "two_eta_2"
        ]
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
      wrong_step,
    ),
  ) is None


def test_phase57_4_rejects_wrong_delta_target():
  data = build_phase57_4_data()

  wrong_map = TodaDeltaMap(
    source_group=TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    ),
  )

  wrong_statement = (
    TodaDeltaImageUpToSignStatement(
      map=wrong_map,
      element=(
        data[
          "phase52"
        ][
          "iota_5"
        ]
      ),
      positive_value=(
        data[
          "phase52"
        ][
          "two_eta_2"
        ]
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
      wrong_step,
    ),
  ) is None


def test_phase57_4_rejects_wrong_delta_element():
  data = build_phase57_4_data()

  wrong_iota = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  wrong_statement = (
    TodaDeltaImageUpToSignStatement(
      map=(
        data[
          "phase52"
        ][
          "delta_map"
        ]
      ),
      element=wrong_iota,
      positive_value=(
        data[
          "phase52"
        ][
          "two_eta_2"
        ]
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
      wrong_step,
    ),
  ) is None


def test_phase57_4_rejects_wrong_delta_value():
  data = build_phase57_4_data()

  wrong_statement = (
    TodaDeltaImageUpToSignStatement(
      map=(
        data[
          "phase52"
        ][
          "delta_map"
        ]
      ),
      element=(
        data[
          "phase52"
        ][
          "iota_5"
        ]
      ),
      positive_value=(
        data[
          "phase52"
        ][
          "eta_2"
        ]
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
      wrong_step,
    ),
  ) is None


def test_phase57_4_reaches_fixed_point_in_one_round():
  data = build_phase57_4_data()

  result = (
    run_inference_until_stable_with_history(
      data[
        "rule"
      ],
      (
        data[
          "delta_statement_step"
        ],
      ),
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert len(
    result.round_results[
      0
    ].new_steps
  ) == 1


