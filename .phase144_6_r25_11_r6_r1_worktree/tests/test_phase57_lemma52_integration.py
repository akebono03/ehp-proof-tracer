from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  IteratedSuspension,
  MapApplication,
  Multiple,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_H_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase57_capabilities import (
  build_phase57_representative_result,
)


def test_phase57_7_derives_hopf_value():
  data = (
    build_phase57_representative_result()
  )

  assert len(
    data[
      "hopf_steps"
    ]
  ) == 1

  step = data[
    "hopf_steps"
  ][
    0
  ]

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    step.conclusion
    == data[
      "expected_hopf_relation"
    ]
  )


def test_phase57_7_hopf_value_is_h_beta_equals_e2_alpha():
  data = (
    build_phase57_representative_result()
  )

  relation = (
    data[
      "hopf_steps"
    ][
      0
    ].conclusion
  )

  assert relation.lhs == (
    MapApplication(
      map=EHP_H_MAP,
      expression=data[
        "beta"
      ],
    )
  )

  assert relation.rhs == (
    IteratedSuspension(
      expression=data[
        "alpha"
      ],
      exponent=2,
    )
  )


def test_phase57_7_derives_twice_beta_value():
  data = (
    build_phase57_representative_result()
  )

  assert len(
    data[
      "double_steps"
    ]
  ) == 1

  step = data[
    "double_steps"
  ][
    0
  ]

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    step.conclusion
    == data[
      "expected_double_relation"
    ]
  )


def test_phase57_7_twice_beta_has_correct_eta_index():
  data = (
    build_phase57_representative_result()
  )

  relation = (
    data[
      "double_steps"
    ][
      0
    ].conclusion
  )

  assert relation.lhs == Multiple(
    coefficient=2,
    expression=data[
      "beta"
    ],
  )

  assert (
    relation
    .rhs
    .right
    .right
    == data[
      "eta_i_plus_one"
    ]
  )


def test_phase57_7_derives_beta_membership():
  data = (
    build_phase57_representative_result()
  )

  assert len(
    data[
      "beta_membership_steps"
    ]
  ) == 1

  step = (
    data[
      "beta_membership_steps"
    ][
      0
    ]
  )

  assert isinstance(
    step.conclusion,
    HomotopyGroupMembershipStatement,
  )

  assert step.conclusion == (
    data[
      "expected_beta_membership"
    ]
  )

  assert step.rule == (
    ProofRule.INFERENCE
  )


def test_phase57_7_beta_membership_is_pi_i_plus_2_s3():
  data = (
    build_phase57_representative_result()
  )

  membership = (
    data[
      "beta_membership_steps"
    ][
      0
    ].conclusion
  )

  assert (
    membership.group_dimension
    == data[
      "i_plus_two"
    ]
  )

  assert (
    membership.sphere_dimension
    == 3
  )


def test_phase57_7_derives_delta_e2_alpha_zero():
  data = (
    build_phase57_representative_result()
  )

  assert len(
    data[
      "delta_zero_steps"
    ]
  ) == 1

  step = (
    data[
      "delta_zero_steps"
    ][
      0
    ]
  )

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.conclusion == (
    data[
      "expected_delta_zero"
    ]
  )


def test_phase57_7_delta_zero_targets_e2_alpha():
  data = (
    build_phase57_representative_result()
  )

  relation = (
    data[
      "delta_zero_steps"
    ][
      0
    ].conclusion
  )

  assert relation.lhs == (
    MapApplication(
      map=EHP_DELTA_MAP,
      expression=IteratedSuspension(
        expression=data[
          "alpha"
        ],
        exponent=2,
      ),
    )
  )


def test_phase57_7_final_results_are_not_given():
  data = (
    build_phase57_representative_result()
  )

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  for conclusion in (
    data[
      "expected_hopf_relation"
    ],
    data[
      "expected_double_relation"
    ],
    data[
      "expected_beta_membership"
    ],
    data[
      "expected_delta_zero"
    ],
  ):
    assert (
      conclusion
      not in initial_conclusions
    )


def test_phase57_7_uses_only_lemma52_actual_hypotheses_as_new_givens():
  data = (
    build_phase57_representative_result()
  )

  steps = data[
    "phase57_premise_steps"
  ]

  assert len(
    steps
  ) == 4

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in steps
  )

  conclusions = tuple(
    step.conclusion
    for step in steps
  )

  assert (
    data[
      "alpha_membership"
    ]
    in conclusions
  )

  assert (
    data[
      "two_alpha_zero"
    ]
    in conclusions
  )

  assert (
    data[
      "bracket_membership"
    ]
    in conclusions
  )

  assert (
    data[
      "gamma_membership"
    ]
    in conclusions
  )


def test_phase57_7_prop26_first_zero_is_not_given():
  data = (
    build_phase57_representative_result()
  )

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  first_zero_steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.inference_rule
      is not None
      and step.inference_rule.name
      == (
        "Toda Lemma 5.2 "
        "Proposition 2.6 first zero premise"
      )
    )
  )

  assert len(
    first_zero_steps
  ) == 1

  assert (
    first_zero_steps[
      0
    ].conclusion
    not in initial_conclusions
  )

  assert (
    first_zero_steps[
      0
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase57_7_all_four_final_results_are_derived():
  data = (
    build_phase57_representative_result()
  )

  groups = (
    data[
      "hopf_steps"
    ],
    data[
      "double_steps"
    ],
    data[
      "beta_membership_steps"
    ],
    data[
      "delta_zero_steps"
    ],
  )

  assert all(
    len(
      steps
    ) == 1
    and steps[
      0
    ].rule
    == ProofRule.INFERENCE
    for steps in groups
  )


def test_phase57_7_reaches_fixed_point():
  data = (
    build_phase57_representative_result()
  )

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )



