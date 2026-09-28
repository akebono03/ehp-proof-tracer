from typing import (
  get_type_hints,
)

from expression import (
  Expression,
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
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  toda_delta_iota5_two_eta2_up_to_sign_inference_rule,
)


def build_phase52_2_data():
  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )

  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  iota_5 = HomotopyElement(
    name="ι_5",
    dimension=5,
    generator=GeneratorSymbol(
      family="ι",
      index=5,
    ),
  )

  iota_2 = HomotopyElement(
    name="ι_2",
    dimension=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
    ),
  )

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

  two_eta_2 = Multiple(
    coefficient=2,
    expression=eta_2,
  )

  whitehead_square = WhiteheadProduct(
    left=iota_2,
    right=iota_2,
  )

  delta_map = TodaDeltaMap(
    source_group=pi_5_5,
    target_group=pi_3_2,
  )

  delta_two_eta_2_up_to_sign = (
    TodaDeltaImageUpToSignStatement(
      map=delta_map,
      element=iota_5,
      positive_value=two_eta_2,
    )
  )

  delta_whitehead_up_to_sign = (
    TodaDeltaImageUpToSignStatement(
      map=delta_map,
      element=iota_5,
      positive_value=whitehead_square,
    )
  )

  whitehead_two_eta_2_up_to_sign = (
    TodaPi32WhiteheadSquareUpToSignStatement(
      whitehead_square=whitehead_square,
      positive_value=two_eta_2,
    )
  )

  return {
    "pi_5_5": pi_5_5,
    "pi_3_2": pi_3_2,
    "iota_5": iota_5,
    "iota_2": iota_2,
    "eta_2": eta_2,
    "two_eta_2": two_eta_2,
    "whitehead_square": (
      whitehead_square
    ),
    "delta_map": delta_map,
    "delta_two_eta_2_up_to_sign": (
      delta_two_eta_2_up_to_sign
    ),
    "delta_whitehead_up_to_sign": (
      delta_whitehead_up_to_sign
    ),
    "whitehead_two_eta_2_up_to_sign": (
      whitehead_two_eta_2_up_to_sign
    ),
  }


def test_phase52_2_statement_uses_specific_delta_map():
  type_hints = get_type_hints(
    TodaDeltaImageUpToSignStatement
  )

  assert type_hints[
    "map"
  ] is TodaDeltaMap

  data = build_phase52_2_data()

  assert (
    data[
      "delta_two_eta_2_up_to_sign"
    ].map
    == data[
      "delta_map"
    ]
  )

  assert (
    data[
      "delta_map"
    ].source_group
    == data[
      "pi_5_5"
    ]
  )

  assert (
    data[
      "delta_map"
    ].target_group
    == data[
      "pi_3_2"
    ]
  )


def test_phase52_2_statement_preserves_iota5_element():
  type_hints = get_type_hints(
    TodaDeltaImageUpToSignStatement
  )

  assert type_hints[
    "element"
  ] is Expression

  data = build_phase52_2_data()

  assert (
    data[
      "delta_two_eta_2_up_to_sign"
    ].element
    == data[
      "iota_5"
    ]
  )


def test_phase52_2_statement_preserves_two_eta2_positive_value():
  type_hints = get_type_hints(
    TodaDeltaImageUpToSignStatement
  )

  assert type_hints[
    "positive_value"
  ] is Expression

  data = build_phase52_2_data()

  statement = data[
    "delta_two_eta_2_up_to_sign"
  ]

  assert (
    statement.positive_value
    == data[
      "two_eta_2"
    ]
  )

  assert isinstance(
    statement.positive_value,
    Multiple,
  )

  assert (
    statement
    .positive_value
    .coefficient
    == 2
  )

  assert (
    statement
    .positive_value
    .expression
    == data[
      "eta_2"
    ]
  )


def test_phase52_2_statement_is_structurally_distinct_from_whitehead_version():
  data = build_phase52_2_data()

  assert (
    data[
      "delta_two_eta_2_up_to_sign"
    ]
    != data[
      "delta_whitehead_up_to_sign"
    ]
  )

  assert (
    data[
      "delta_two_eta_2_up_to_sign"
    ].positive_value
    != data[
      "whitehead_square"
    ]
  )


def test_phase52_2_statement_does_not_encode_a_sign_choice():
  data = build_phase52_2_data()

  statement = data[
    "delta_two_eta_2_up_to_sign"
  ]

  negative_two_eta_2 = Multiple(
    coefficient=-2,
    expression=data[
      "eta_2"
    ],
  )

  sign_specific_negative_statement = (
    TodaDeltaImageUpToSignStatement(
      map=data[
        "delta_map"
      ],
      element=data[
        "iota_5"
      ],
      positive_value=negative_two_eta_2,
    )
  )

  assert (
    statement
    != sign_specific_negative_statement
  )

  assert (
    statement.positive_value
    == data[
      "two_eta_2"
    ]
  )


def test_phase52_3_bridge_rule_matches_valid_statements():
  data = build_phase52_2_data()

  steps = (
    ProofStep(
      conclusion=data[
        "delta_whitehead_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "whitehead_two_eta_2_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_delta_iota5_two_eta2_up_to_sign_inference_rule(),
    steps,
  ) is not None


def test_phase52_3_bridge_rule_derives_delta_iota5_two_eta2():
  data = build_phase52_2_data()

  steps = (
    ProofStep(
      conclusion=data[
        "delta_whitehead_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "whitehead_two_eta_2_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  result = (
    run_inference_until_stable_with_history(
      toda_delta_iota5_two_eta2_up_to_sign_inference_rule(),
      steps,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "delta_two_eta_2_up_to_sign"
  ] in conclusions


def test_phase52_3_bridge_result_is_inference():
  data = build_phase52_2_data()

  steps = (
    ProofStep(
      conclusion=data[
        "delta_whitehead_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "whitehead_two_eta_2_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  result = (
    run_inference_until_stable_with_history(
      toda_delta_iota5_two_eta2_up_to_sign_inference_rule(),
      steps,
    )
  )

  derived = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == data[
        "delta_two_eta_2_up_to_sign"
      ]
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )


def test_phase52_3_bridge_preserves_both_premises():
  data = build_phase52_2_data()

  delta_step = ProofStep(
    conclusion=data[
      "delta_whitehead_up_to_sign"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  whitehead_step = ProofStep(
    conclusion=data[
      "whitehead_two_eta_2_up_to_sign"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      toda_delta_iota5_two_eta2_up_to_sign_inference_rule(),
      (
        delta_step,
        whitehead_step,
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == data[
        "delta_two_eta_2_up_to_sign"
      ]
    )
  )

  assert derived.premises == (
    delta_step,
    whitehead_step,
  )


def test_phase52_3_bridge_reaches_fixed_point_in_one_round():
  data = build_phase52_2_data()

  steps = (
    ProofStep(
      conclusion=data[
        "delta_whitehead_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "whitehead_two_eta_2_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  result = (
    run_inference_until_stable_with_history(
      toda_delta_iota5_two_eta2_up_to_sign_inference_rule(),
      steps,
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


def test_phase52_4_rejects_wrong_delta_source():
  data = build_phase52_2_data()

  wrong_delta_map = TodaDeltaMap(
    source_group=TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=5,
    ),
    target_group=data[
      "pi_3_2"
    ],
  )

  wrong_delta_statement = (
    TodaDeltaImageUpToSignStatement(
      map=wrong_delta_map,
      element=data[
        "iota_5"
      ],
      positive_value=data[
        "whitehead_square"
      ],
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_delta_statement,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "whitehead_two_eta_2_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_delta_iota5_two_eta2_up_to_sign_inference_rule(),
    steps,
  ) is None


def test_phase52_4_rejects_wrong_delta_target():
  data = build_phase52_2_data()

  wrong_delta_map = TodaDeltaMap(
    source_group=data[
      "pi_5_5"
    ],
    target_group=TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    ),
  )

  wrong_delta_statement = (
    TodaDeltaImageUpToSignStatement(
      map=wrong_delta_map,
      element=data[
        "iota_5"
      ],
      positive_value=data[
        "whitehead_square"
      ],
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_delta_statement,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "whitehead_two_eta_2_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_delta_iota5_two_eta2_up_to_sign_inference_rule(),
    steps,
  ) is None


def test_phase52_4_rejects_wrong_delta_element():
  data = build_phase52_2_data()

  wrong_iota = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  wrong_delta_statement = (
    TodaDeltaImageUpToSignStatement(
      map=data[
        "delta_map"
      ],
      element=wrong_iota,
      positive_value=data[
        "whitehead_square"
      ],
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_delta_statement,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "whitehead_two_eta_2_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_delta_iota5_two_eta2_up_to_sign_inference_rule(),
    steps,
  ) is None


def test_phase52_4_rejects_wrong_whitehead_square():
  data = build_phase52_2_data()

  iota_3 = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  wrong_whitehead_square = WhiteheadProduct(
    left=iota_3,
    right=iota_3,
  )

  wrong_delta_statement = (
    TodaDeltaImageUpToSignStatement(
      map=data[
        "delta_map"
      ],
      element=data[
        "iota_5"
      ],
      positive_value=wrong_whitehead_square,
    )
  )

  wrong_whitehead_statement = (
    TodaPi32WhiteheadSquareUpToSignStatement(
      whitehead_square=wrong_whitehead_square,
      positive_value=data[
        "two_eta_2"
      ],
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_delta_statement,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_whitehead_statement,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_delta_iota5_two_eta2_up_to_sign_inference_rule(),
    steps,
  ) is None


def test_phase52_4_rejects_wrong_coefficient():
  data = build_phase52_2_data()

  three_eta_2 = Multiple(
    coefficient=3,
    expression=data[
      "eta_2"
    ],
  )

  wrong_whitehead_statement = (
    TodaPi32WhiteheadSquareUpToSignStatement(
      whitehead_square=data[
        "whitehead_square"
      ],
      positive_value=three_eta_2,
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "delta_whitehead_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_whitehead_statement,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_delta_iota5_two_eta2_up_to_sign_inference_rule(),
    steps,
  ) is None


def test_phase52_4_rejects_wrong_eta_index():
  data = build_phase52_2_data()

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  two_eta_3 = Multiple(
    coefficient=2,
    expression=eta_3,
  )

  wrong_whitehead_statement = (
    TodaPi32WhiteheadSquareUpToSignStatement(
      whitehead_square=data[
        "whitehead_square"
      ],
      positive_value=two_eta_3,
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "delta_whitehead_up_to_sign"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_whitehead_statement,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_delta_iota5_two_eta2_up_to_sign_inference_rule(),
    steps,
  ) is None




