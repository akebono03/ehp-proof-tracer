from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  ScalarSymbol,
  Zero,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from relation_rules import (
  zero_equality_implies_zero_inference_rule,
)
from toda_rules import (
  toda_lemma45_n4_two_iota3_composition_inference_rule,
)


def build_phase57_2_data():
  i = ScalarSymbol(
    name="i",
  )

  alpha = HomotopyElement(
    name="α",
    dimension=i,
  )

  iota_3 = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  membership = (
    HomotopyGroupMembershipStatement(
      element=alpha,
      group_dimension=i,
      sphere_dimension=3,
    )
  )

  two_alpha_zero = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=alpha,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  lemma45_equality = Relation(
    lhs=Composition(
      left=Multiple(
        coefficient=2,
        expression=iota_3,
      ),
      right=alpha,
    ),
    rhs=Multiple(
      coefficient=2,
      expression=alpha,
    ),
    relation_type=RelationType.EQUALITY,
  )

  final_zero = Relation(
    lhs=Composition(
      left=Multiple(
        coefficient=2,
        expression=iota_3,
      ),
      right=alpha,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  membership_step = ProofStep(
    conclusion=membership,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  two_alpha_zero_step = ProofStep(
    conclusion=two_alpha_zero,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  lemma45_rule = (
    toda_lemma45_n4_two_iota3_composition_inference_rule()
  )

  zero_rule = (
    zero_equality_implies_zero_inference_rule()
  )

  return {
    "i": i,
    "alpha": alpha,
    "iota_3": iota_3,
    "membership": membership,
    "two_alpha_zero": two_alpha_zero,
    "lemma45_equality": lemma45_equality,
    "final_zero": final_zero,
    "membership_step": membership_step,
    "two_alpha_zero_step": (
      two_alpha_zero_step
    ),
    "lemma45_rule": lemma45_rule,
    "zero_rule": zero_rule,
  }


def test_phase57_2_alpha_in_pi_i_s3_is_representable():
  data = build_phase57_2_data()

  assert data[
    "membership"
  ] == HomotopyGroupMembershipStatement(
    element=data[
      "alpha"
    ],
    group_dimension=data[
      "i"
    ],
    sphere_dimension=3,
  )


def test_phase57_2_lemma45_rule_matches_alpha_in_pi_i_s3():
  data = build_phase57_2_data()

  match = find_inference_match(
    data[
      "lemma45_rule"
    ],
    (
      data[
        "membership_step"
      ],
    ),
  )

  assert match is not None


def test_phase57_2_lemma45_rule_derives_two_iota3_alpha_equals_two_alpha():
  data = build_phase57_2_data()

  match = find_inference_match(
    data[
      "lemma45_rule"
    ],
    (
      data[
        "membership_step"
      ],
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    data[
      "lemma45_equality"
    ]
  )


def test_phase57_2_lemma45_equality_preserves_provenance():
  data = build_phase57_2_data()

  result = (
    run_inference_until_stable_with_history(
      data[
        "lemma45_rule"
      ],
      (
        data[
          "membership_step"
        ],
      ),
    )
  )

  lemma_steps = tuple(
    step
    for step in result.steps
    if step.conclusion
    == data[
      "lemma45_equality"
    ]
  )

  assert len(
    lemma_steps
  ) == 1

  lemma_step = lemma_steps[
    0
  ]

  assert lemma_step.rule == (
    ProofRule.INFERENCE
  )

  assert lemma_step.premises == (
    data[
      "membership_step"
    ],
  )

  assert (
    lemma_step.inference_rule
    == data[
      "lemma45_rule"
    ]
  )


def test_phase57_2_lemma45_rule_alone_does_not_derive_zero():
  data = build_phase57_2_data()

  result = (
    run_inference_until_stable_with_history(
      data[
        "lemma45_rule"
      ],
      (
        data[
          "membership_step"
        ],
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert (
    data[
      "lemma45_equality"
    ]
    in conclusions
  )

  assert (
    data[
      "final_zero"
    ]
    not in conclusions
  )


def test_phase57_2_two_alpha_zero_reaches_two_iota3_alpha_zero():
  data = build_phase57_2_data()

  result = (
    run_inference_until_stable_with_history(
      (
        data[
          "lemma45_rule"
        ],
        data[
          "zero_rule"
        ],
      ),
      (
        data[
          "membership_step"
        ],
        data[
          "two_alpha_zero_step"
        ],
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert (
    data[
      "lemma45_equality"
    ]
    in conclusions
  )

  assert (
    data[
      "final_zero"
    ]
    in conclusions
  )


def test_phase57_2_final_zero_uses_generic_zero_propagation():
  data = build_phase57_2_data()

  result = (
    run_inference_until_stable_with_history(
      (
        data[
          "lemma45_rule"
        ],
        data[
          "zero_rule"
        ],
      ),
      (
        data[
          "membership_step"
        ],
        data[
          "two_alpha_zero_step"
        ],
      ),
    )
  )

  lemma_step = next(
    step
    for step in result.steps
    if step.conclusion
    == data[
      "lemma45_equality"
    ]
  )

  final_step = next(
    step
    for step in result.steps
    if step.conclusion
    == data[
      "final_zero"
    ]
  )

  assert final_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    final_step.inference_rule
    == data[
      "zero_rule"
    ]
  )

  assert final_step.premises == (
    data[
      "two_alpha_zero_step"
    ],
    lemma_step,
  )


def test_phase57_2_wrong_sphere_dimension_is_rejected():
  data = build_phase57_2_data()

  wrong_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=data[
          "alpha"
        ],
        group_dimension=data[
          "i"
        ],
        sphere_dimension=4,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    data[
      "lemma45_rule"
    ],
    (
      wrong_membership_step,
    ),
  )

  assert match is None


def test_phase57_2_zero_of_different_element_does_not_prove_target_zero():
  data = build_phase57_2_data()

  gamma = HomotopyElement(
    name="γ",
    dimension=data[
      "i"
    ],
  )

  two_gamma_zero_step = ProofStep(
    conclusion=Relation(
      lhs=Multiple(
        coefficient=2,
        expression=gamma,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        data[
          "lemma45_rule"
        ],
        data[
          "zero_rule"
        ],
      ),
      (
        data[
          "membership_step"
        ],
        two_gamma_zero_step,
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert (
    data[
      "lemma45_equality"
    ]
    in conclusions
  )

  assert (
    data[
      "final_zero"
    ]
    not in conclusions
  )


def test_phase57_2_representative_reaches_fixed_point():
  data = build_phase57_2_data()

  result = (
    run_inference_until_stable_with_history(
      (
        data[
          "lemma45_rule"
        ],
        data[
          "zero_rule"
        ],
      ),
      (
        data[
          "membership_step"
        ],
        data[
          "two_alpha_zero_step"
        ],
      ),
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2


