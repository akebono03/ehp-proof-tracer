from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  ScalarSum,
  ScalarSymbol,
  Suspension,
  Zero,
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
from probes.probe_phase55_capabilities import (
  build_phase55_representative_result,
)
from toda_rules import (
  TodaProp51FiniteDimensionalStatement,
  toda_21_lemma52_suspended_indeterminacy_zero_inference_rule,
  toda_lemma45_n4_suspension_zero_reflection_inference_rule,
  toda_prop51_eta4_twice_zero_inference_rule,
)


def build_phase57_6_data():
  phase55 = (
    build_phase55_representative_result()
  )

  prop51_step = (
    phase55[
      "prop51_steps"
    ][
      0
    ]
  )

  i = ScalarSymbol(
    name="i",
  )

  i_plus_two = ScalarSum(
    left=i,
    right=2,
  )

  gamma = HomotopyElement(
    name="γ",
    dimension=i_plus_two,
    source=i_plus_two,
    target=4,
  )

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

  eta_4 = HomotopyElement(
    name="η₄",
    dimension=4,
    source=5,
    target=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
  )

  iota_i_plus_two = HomotopyElement(
    name="ι_(i+2)",
    dimension=i_plus_two,
    generator=GeneratorSymbol(
      family="ι",
      index=i_plus_two,
    ),
  )

  gamma_membership = (
    HomotopyGroupMembershipStatement(
      element=gamma,
      group_dimension=i_plus_two,
      sphere_dimension=4,
    )
  )

  gamma_membership_step = ProofStep(
    conclusion=gamma_membership,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta4_zero = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=eta_4,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  indeterminacy_element = Composition(
    left=Composition(
      left=eta_3,
      right=gamma,
    ),
    right=Multiple(
      coefficient=2,
      expression=iota_i_plus_two,
    ),
  )

  suspended_zero = Relation(
    lhs=Suspension(
      expression=indeterminacy_element,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  final_zero = Relation(
    lhs=indeterminacy_element,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  eta4_rule = (
    toda_prop51_eta4_twice_zero_inference_rule()
  )

  suspended_rule = (
    toda_21_lemma52_suspended_indeterminacy_zero_inference_rule()
  )

  reflection_rule = (
    toda_lemma45_n4_suspension_zero_reflection_inference_rule()
  )

  rules = (
    eta4_rule,
    suspended_rule,
    reflection_rule,
  )

  premise_steps = (
    prop51_step,
    gamma_membership_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  return {
    "phase55": phase55,
    "prop51_step": prop51_step,
    "i": i,
    "i_plus_two": i_plus_two,
    "gamma": gamma,
    "eta_3": eta_3,
    "eta_4": eta_4,
    "iota_i_plus_two": (
      iota_i_plus_two
    ),
    "gamma_membership": (
      gamma_membership
    ),
    "gamma_membership_step": (
      gamma_membership_step
    ),
    "eta4_zero": eta4_zero,
    "indeterminacy_element": (
      indeterminacy_element
    ),
    "suspended_zero": (
      suspended_zero
    ),
    "final_zero": final_zero,
    "eta4_rule": eta4_rule,
    "suspended_rule": (
      suspended_rule
    ),
    "reflection_rule": (
      reflection_rule
    ),
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
  }


def test_phase57_6_uses_derived_prop51_result():
  data = build_phase57_6_data()

  assert isinstance(
    data[
      "prop51_step"
    ].conclusion,
    TodaProp51FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop51_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase57_6_prop51_derives_two_eta4_zero():
  data = build_phase57_6_data()

  conclusions = tuple(
    step.conclusion
    for step in data[
      "result"
    ].steps
  )

  assert (
    data[
      "eta4_zero"
    ]
    in conclusions
  )


def test_phase57_6_eta4_zero_preserves_prop51_provenance():
  data = build_phase57_6_data()

  step = next(
    step
    for step in data[
      "result"
    ].steps
    if step.conclusion
    == data[
      "eta4_zero"
    ]
  )

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.premises == (
    data[
      "prop51_step"
    ],
  )


def test_phase57_6_eta4_zero_rule_rejects_given_prop51():
  data = build_phase57_6_data()

  given_prop51 = ProofStep(
    conclusion=(
      data[
        "prop51_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "eta4_rule"
    ],
    (
      given_prop51,
    ),
  ) is None


def test_phase57_6_gamma_membership_is_pi_i_plus_2_s4():
  data = build_phase57_6_data()

  assert (
    data[
      "gamma_membership"
    ]
    == HomotopyGroupMembershipStatement(
      element=data[
        "gamma"
      ],
      group_dimension=data[
        "i_plus_two"
      ],
      sphere_dimension=4,
    )
  )


def test_phase57_6_toda21_derives_suspended_indeterminacy_zero():
  data = build_phase57_6_data()

  conclusions = tuple(
    step.conclusion
    for step in data[
      "result"
    ].steps
  )

  assert (
    data[
      "suspended_zero"
    ]
    in conclusions
  )


def test_phase57_6_toda21_step_preserves_two_premises():
  data = build_phase57_6_data()

  eta4_step = next(
    step
    for step in data[
      "result"
    ].steps
    if step.conclusion
    == data[
      "eta4_zero"
    ]
  )

  suspended_step = next(
    step
    for step in data[
      "result"
    ].steps
    if step.conclusion
    == data[
      "suspended_zero"
    ]
  )

  assert suspended_step.rule == (
    ProofRule.INFERENCE
  )

  assert suspended_step.premises == (
    data[
      "gamma_membership_step"
    ],
    eta4_step,
  )


def test_phase57_6_toda21_rejects_wrong_sphere():
  data = build_phase57_6_data()

  wrong_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=data[
          "gamma"
        ],
        group_dimension=data[
          "i_plus_two"
        ],
        sphere_dimension=5,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta4_step = next(
    step
    for step in data[
      "result"
    ].steps
    if step.conclusion
    == data[
      "eta4_zero"
    ]
  )

  assert find_inference_match(
    data[
      "suspended_rule"
    ],
    (
      wrong_membership_step,
      eta4_step,
    ),
  ) is None


def test_phase57_6_toda21_rejects_given_two_eta4_zero():
  data = build_phase57_6_data()

  given_eta4_zero_step = ProofStep(
    conclusion=data[
      "eta4_zero"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "suspended_rule"
    ],
    (
      data[
        "gamma_membership_step"
      ],
      given_eta4_zero_step,
    ),
  ) is None


def test_phase57_6_lemma45_derives_unsuspended_zero():
  data = build_phase57_6_data()

  conclusions = tuple(
    step.conclusion
    for step in data[
      "result"
    ].steps
  )

  assert (
    data[
      "final_zero"
    ]
    in conclusions
  )


def test_phase57_6_lemma45_reflection_preserves_provenance():
  data = build_phase57_6_data()

  suspended_step = next(
    step
    for step in data[
      "result"
    ].steps
    if step.conclusion
    == data[
      "suspended_zero"
    ]
  )

  final_step = next(
    step
    for step in data[
      "result"
    ].steps
    if step.conclusion
    == data[
      "final_zero"
    ]
  )

  assert final_step.rule == (
    ProofRule.INFERENCE
  )

  assert final_step.premises == (
    data[
      "gamma_membership_step"
    ],
    suspended_step,
  )


def test_phase57_6_lemma45_rejects_given_suspended_zero():
  data = build_phase57_6_data()

  given_suspended_zero_step = ProofStep(
    conclusion=data[
      "suspended_zero"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "reflection_rule"
    ],
    (
      data[
        "gamma_membership_step"
      ],
      given_suspended_zero_step,
    ),
  ) is None


def test_phase57_6_lemma45_rejects_wrong_iota_index():
  data = build_phase57_6_data()

  i_plus_one = ScalarSum(
    left=data[
      "i"
    ],
    right=1,
  )

  wrong_iota = HomotopyElement(
    name="ι_(i+1)",
    dimension=i_plus_one,
    generator=GeneratorSymbol(
      family="ι",
      index=i_plus_one,
    ),
  )

  wrong_element = Composition(
    left=Composition(
      left=data[
        "eta_3"
      ],
      right=data[
        "gamma"
      ],
    ),
    right=Multiple(
      coefficient=2,
      expression=wrong_iota,
    ),
  )

  wrong_suspended_zero_step = ProofStep(
    conclusion=Relation(
      lhs=Suspension(
        expression=wrong_element,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(
      data[
        "gamma_membership_step"
      ],
    ),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "reflection_rule"
    ],
    (
      data[
        "gamma_membership_step"
      ],
      wrong_suspended_zero_step,
    ),
  ) is None


def test_phase57_6_end_to_end_result_is_derived():
  data = build_phase57_6_data()

  final_steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if step.conclusion
    == data[
      "final_zero"
    ]
  )

  assert len(
    final_steps
  ) == 1

  assert (
    final_steps[
      0
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase57_6_end_to_end_reaches_fixed_point():
  data = build_phase57_6_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    data[
      "result"
    ].round_count
    == 3
  )
  


