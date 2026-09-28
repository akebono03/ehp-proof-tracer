from expression import (
  Multiple,
  Suspension,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  Relation,
)
from probes.probe_phase50_capabilities import (
  build_phase50_representative_result,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)


def test_phase50_probe_has_eleven_initial_given_premises():
  representative = (
    build_phase50_representative_result()
  )

  assert len(
    representative[
      "premise_steps"
    ]
  ) == 11

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in representative[
      "premise_steps"
    ]
  )


def test_phase50_probe_reuses_pi3_2_free_cyclic_result():
  representative = (
    build_phase50_representative_result()
  )

  relation = representative[
    "pi_3_2_relation"
  ]

  assert relation.lhs == (
    TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )
  )

  assert isinstance(
    relation.rhs,
    FreeCyclicGroup,
  )

  assert relation.rhs.generator.name == (
    "η₂"
  )


def test_phase50_probe_derives_prop27_consequence():
  representative = (
    build_phase50_representative_result()
  )

  steps = representative[
    "prop27_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaProp27HopfInvariantUpToSignStatement,
  )


def test_phase50_probe_prop27_value_is_two_iota3():
  representative = (
    build_phase50_representative_result()
  )

  statement = representative[
    "prop27_steps"
  ][
    0
  ].conclusion

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
    .name
    == "ι_3"
  )


def test_phase50_probe_derives_whitehead_square_relation():
  representative = (
    build_phase50_representative_result()
  )

  steps = representative[
    "whitehead_square_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaPi32WhiteheadSquareUpToSignStatement,
  )


def test_phase50_probe_whitehead_square_value_is_two_eta2():
  representative = (
    build_phase50_representative_result()
  )

  statement = representative[
    "whitehead_square_steps"
  ][
    0
  ].conclusion

  assert statement.positive_value == (
    Multiple(
      coefficient=2,
      expression=representative[
        "eta_2"
      ],
    )
  )


def test_phase50_probe_derives_delta_up_to_sign():
  representative = (
    build_phase50_representative_result()
  )

  steps = representative[
    "delta_up_to_sign_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )


def test_phase50_probe_derives_delta_image():
  representative = (
    build_phase50_representative_result()
  )

  steps = representative[
    "delta_image_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaDeltaImageFreeCyclicStatement,
  )


def test_phase50_probe_delta_image_is_generated_by_two_eta2():
  representative = (
    build_phase50_representative_result()
  )

  statement = representative[
    "delta_image_steps"
  ][
    0
  ].conclusion

  assert statement.image_group == (
    FreeCyclicGroup(
      generator=Multiple(
        coefficient=2,
        expression=representative[
          "eta_2"
        ],
      ),
    )
  )


def test_phase50_probe_derives_suspension_kernel():
  representative = (
    build_phase50_representative_result()
  )

  steps = representative[
    "suspension_kernel_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaSuspensionKernelFreeCyclicStatement,
  )


def test_phase50_probe_kernel_is_generated_by_two_eta2():
  representative = (
    build_phase50_representative_result()
  )

  statement = representative[
    "suspension_kernel_steps"
  ][
    0
  ].conclusion

  assert statement.kernel_group == (
    FreeCyclicGroup(
      generator=Multiple(
        coefficient=2,
        expression=representative[
          "eta_2"
        ],
      ),
    )
  )


def test_phase50_probe_derives_e_surjectivity():
  representative = (
    build_phase50_representative_result()
  )

  steps = representative[
    "suspension_surjective_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaSuspensionSurjectiveStatement,
  )


def test_phase50_probe_e_surjectivity_has_expected_instance():
  representative = (
    build_phase50_representative_result()
  )

  statement = representative[
    "suspension_surjective_steps"
  ][
    0
  ].conclusion

  assert statement.map.source_group == (
    TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )
  )

  assert statement.map.target_group == (
    TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )
  )


def test_phase50_probe_derives_intermediate_pi4_3_group():
  representative = (
    build_phase50_representative_result()
  )

  steps = representative[
    "intermediate_group_steps"
  ]

  assert len(
    steps
  ) == 1

  relation = steps[
    0
  ].conclusion

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 2

  assert relation.rhs.generator == (
    Suspension(
      expression=representative[
        "eta_2"
      ],
    )
  )


def test_phase50_probe_derives_eta3_equals_e_eta2():
  representative = (
    build_phase50_representative_result()
  )

  steps = representative[
    "eta_3_relation_steps"
  ]

  assert len(
    steps
  ) == 1

  relation = steps[
    0
  ].conclusion

  assert relation.lhs == (
    representative[
      "eta_3"
    ]
  )

  assert relation.rhs == (
    Suspension(
      expression=representative[
        "eta_2"
      ],
    )
  )


def test_phase50_probe_derives_final_pi4_3_group():
  representative = (
    build_phase50_representative_result()
  )

  steps = representative[
    "final_group_steps"
  ]

  assert len(
    steps
  ) == 1

  relation = steps[
    0
  ].conclusion

  assert relation.lhs == (
    TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 2

  assert relation.rhs.generator == (
    representative[
      "eta_3"
    ]
  )


def test_phase50_probe_final_group_is_inference_derived():
  representative = (
    build_phase50_representative_result()
  )

  step = representative[
    "final_group_steps"
  ][
    0
  ]

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.inference_rule is not None


def test_phase50_probe_all_nine_expected_steps_are_derived():
  representative = (
    build_phase50_representative_result()
  )

  derived = tuple(
    step
    for step in representative[
      "result"
    ].steps
    if step.rule
    == ProofRule.INFERENCE
  )

  assert len(
    derived
  ) == 9


def test_phase50_probe_all_derived_steps_preserve_inference_rule():
  representative = (
    build_phase50_representative_result()
  )

  derived = tuple(
    step
    for step in representative[
      "result"
    ].steps
    if step.rule
    == ProofRule.INFERENCE
  )

  assert all(
    step.inference_rule
    is not None
    for step in derived
  )


def test_phase50_probe_reaches_fixed_point():
  representative = (
    build_phase50_representative_result()
  )

  assert (
    representative[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase50_probe_reaches_fixed_point_in_six_rounds():
  representative = (
    build_phase50_representative_result()
  )

  assert representative[
    "result"
  ].round_count == 6


def test_phase50_probe_round_one_derives_four_steps():
  representative = (
    build_phase50_representative_result()
  )

  assert len(
    representative[
      "result"
    ].round_results[
      0
    ].new_steps
  ) == 4


def test_phase50_probe_round_two_derives_whitehead_relation():
  representative = (
    build_phase50_representative_result()
  )

  new_steps = representative[
    "result"
  ].round_results[
    1
  ].new_steps

  assert len(
    new_steps
  ) == 1

  assert isinstance(
    new_steps[
      0
    ].conclusion,
    TodaPi32WhiteheadSquareUpToSignStatement,
  )


def test_phase50_probe_round_three_derives_delta_image():
  representative = (
    build_phase50_representative_result()
  )

  new_steps = representative[
    "result"
  ].round_results[
    2
  ].new_steps

  assert len(
    new_steps
  ) == 1

  assert isinstance(
    new_steps[
      0
    ].conclusion,
    TodaDeltaImageFreeCyclicStatement,
  )


def test_phase50_probe_round_four_derives_kernel():
  representative = (
    build_phase50_representative_result()
  )

  new_steps = representative[
    "result"
  ].round_results[
    3
  ].new_steps

  assert len(
    new_steps
  ) == 1

  assert isinstance(
    new_steps[
      0
    ].conclusion,
    TodaSuspensionKernelFreeCyclicStatement,
  )


def test_phase50_probe_round_five_derives_intermediate_group():
  representative = (
    build_phase50_representative_result()
  )

  new_steps = representative[
    "result"
  ].round_results[
    4
  ].new_steps

  assert len(
    new_steps
  ) == 1

  conclusion = new_steps[
    0
  ].conclusion

  assert isinstance(
    conclusion,
    Relation,
  )

  assert conclusion == (
    representative[
      "intermediate_group_steps"
    ][
      0
    ].conclusion
  )


def test_phase50_probe_round_six_derives_final_eta3_group():
  representative = (
    build_phase50_representative_result()
  )

  new_steps = representative[
    "result"
  ].round_results[
    5
  ].new_steps

  assert len(
    new_steps
  ) == 1

  assert new_steps[
    0
  ] == (
    representative[
      "final_group_steps"
    ][
      0
    ]
  )



