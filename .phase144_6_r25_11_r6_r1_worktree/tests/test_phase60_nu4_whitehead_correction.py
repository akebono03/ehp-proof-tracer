from functools import lru_cache

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
  Multiple,
  ScalarSymbol,
  Suspension,
  WhiteheadProduct,
  Zero,
)
from map_facts import (
  EHP_H_MAP,
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
from test_phase60_toda48_hopf_parity import (
  build_phase60_7_data,
)
from toda_rules import (
  TodaLemma54Nu4BranchFormula,
  TodaLemma54Nu4ConstructionStatement,
  TodaLemma54WhiteheadCorrectionDataStatement,
  toda_lemma54_nu4_double_suspension_inference_rule,
  toda_lemma54_nu4_hopf_inference_rule,
  toda_lemma54_nu4_membership_inference_rule,
  toda_lemma54_nu4_piecewise_construction_inference_rule,
  toda_lemma54_whitehead_correction_data_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase60_8_data():
  phase60_7 = (
    build_phase60_7_data()
  )

  hopf_odd_step = (
    phase60_7[
      "final_step"
    ]
  )

  phase60_6 = (
    phase60_7[
      "phase60_6"
    ]
  )

  double_step = (
    phase60_6[
      "final_step"
    ]
  )

  alpha_star = (
    phase60_7[
      "alpha_star"
    ]
  )

  s = (
    phase60_7[
      "s"
    ]
  )

  nu_prime = (
    phase60_7[
      "nu_prime"
    ]
  )

  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  iota_7 = HomotopyElement(
    name="ι_7",
    dimension=7,
    generator=GeneratorSymbol(
      family="ι",
      index=7,
    ),
  )

  whitehead_square = WhiteheadProduct(
    left=iota_4,
    right=iota_4,
  )

  whitehead_step = ProofStep(
    conclusion=whitehead_square,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  u = ScalarSymbol(
    name="u",
  )

  expected_whitehead_data = (
    TodaLemma54WhiteheadCorrectionDataStatement(
      whitehead_square=whitehead_square,
      sign_parameter=u,
      hopf_positive_value=Multiple(
        coefficient=2,
        expression=iota_7,
      ),
      suspension_zero_relation=Relation(
        lhs=Suspension(
          expression=whitehead_square,
        ),
        rhs=Zero(),
        relation_type=RelationType.ZERO,
      ),
    )
  )

  nu4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  positive_branch = (
    TodaLemma54Nu4BranchFormula(
      double_suspension_sign=1,
      alpha_star_sign=1,
      whitehead_coefficient_sign=-1,
      parameter_offset=0,
    )
  )

  negative_branch = (
    TodaLemma54Nu4BranchFormula(
      double_suspension_sign=-1,
      alpha_star_sign=-1,
      whitehead_coefficient_sign=1,
      parameter_offset=1,
    )
  )

  expected_construction = (
    TodaLemma54Nu4ConstructionStatement(
      alpha_star=alpha_star,
      nu4=nu4,
      parameter=s,
      whitehead_data=expected_whitehead_data,
      double_suspension_value=(
        IteratedSuspension(
          expression=nu_prime,
          exponent=2,
        )
      ),
      positive_branch=positive_branch,
      negative_branch=negative_branch,
    )
  )

  expected_membership = (
    HomotopyGroupMembershipStatement(
      element=nu4,
      group_dimension=7,
      sphere_dimension=4,
    )
  )

  expected_hopf = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=nu4,
    ),
    rhs=iota_7,
    relation_type=RelationType.EQUALITY,
  )

  expected_double = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=Suspension(
        expression=nu4,
      ),
    ),
    rhs=IteratedSuspension(
      expression=nu_prime,
      exponent=2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  whitehead_rule = (
    toda_lemma54_whitehead_correction_data_inference_rule()
  )

  construction_rule = (
    toda_lemma54_nu4_piecewise_construction_inference_rule()
  )

  membership_rule = (
    toda_lemma54_nu4_membership_inference_rule()
  )

  hopf_rule = (
    toda_lemma54_nu4_hopf_inference_rule()
  )

  double_rule = (
    toda_lemma54_nu4_double_suspension_inference_rule()
  )

  rules = (
    whitehead_rule,
    construction_rule,
    membership_rule,
    hopf_rule,
    double_rule,
  )

  premise_steps = (
    hopf_odd_step,
    double_step,
    whitehead_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  whitehead_data_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_whitehead_data
    )
  )

  construction_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_construction
    )
  )

  membership_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_membership
    )
  )

  hopf_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_hopf
    )
  )

  double_result_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_double
    )
  )

  return {
    "phase60_7": phase60_7,
    "phase60_6": phase60_6,
    "hopf_odd_step": hopf_odd_step,
    "double_step": double_step,
    "alpha_star": alpha_star,
    "s": s,
    "u": u,
    "nu_prime": nu_prime,
    "iota_4": iota_4,
    "iota_7": iota_7,
    "whitehead_square": whitehead_square,
    "whitehead_step": whitehead_step,
    "nu4": nu4,
    "positive_branch": positive_branch,
    "negative_branch": negative_branch,
    "expected_whitehead_data": (
      expected_whitehead_data
    ),
    "expected_construction": (
      expected_construction
    ),
    "expected_membership": (
      expected_membership
    ),
    "expected_hopf": expected_hopf,
    "expected_double": expected_double,
    "whitehead_rule": whitehead_rule,
    "construction_rule": construction_rule,
    "membership_rule": membership_rule,
    "hopf_rule": hopf_rule,
    "double_rule": double_rule,
    "premise_steps": premise_steps,
    "result": result,
    "whitehead_data_step": (
      whitehead_data_step
    ),
    "construction_step": construction_step,
    "membership_step": membership_step,
    "hopf_step": hopf_step,
    "double_result_step": (
      double_result_step
    ),
  }


def test_phase60_8_reuses_derived_hopf_odd_multiple():
  data = build_phase60_8_data()

  assert (
    data[
      "hopf_odd_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_8_reuses_derived_double_suspension_up_to_sign():
  data = build_phase60_8_data()

  assert (
    data[
      "double_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_8_whitehead_rule_matches_iota4_square():
  data = build_phase60_8_data()

  assert find_inference_match(
    data[
      "whitehead_rule"
    ],
    (
      data[
        "whitehead_step"
      ],
    ),
  ) is not None


def test_phase60_8_derives_whitehead_correction_data():
  data = build_phase60_8_data()

  assert (
    data[
      "whitehead_data_step"
    ].conclusion
    == data[
      "expected_whitehead_data"
    ]
  )

  assert (
    data[
      "whitehead_data_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_8_whitehead_hopf_value_is_twice_iota7():
  data = build_phase60_8_data()

  assert (
    data[
      "whitehead_data_step"
    ].conclusion.hopf_positive_value
    == Multiple(
      coefficient=2,
      expression=data[
        "iota_7"
      ],
    )
  )


def test_phase60_8_whitehead_suspension_is_zero():
  data = build_phase60_8_data()

  assert (
    data[
      "whitehead_data_step"
    ].conclusion.suspension_zero_relation
    == Relation(
      lhs=Suspension(
        expression=data[
          "whitehead_square"
        ],
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )


def test_phase60_8_whitehead_sign_parameter_is_u():
  data = build_phase60_8_data()

  assert (
    data[
      "whitehead_data_step"
    ].conclusion.sign_parameter
    == ScalarSymbol(
      name="u",
    )
  )


def test_phase60_8_construction_rule_matches_dependencies():
  data = build_phase60_8_data()

  assert find_inference_match(
    data[
      "construction_rule"
    ],
    (
      data[
        "hopf_odd_step"
      ],
      data[
        "double_step"
      ],
      data[
        "whitehead_data_step"
      ],
    ),
  ) is not None


def test_phase60_8_derives_piecewise_nu4_construction():
  data = build_phase60_8_data()

  assert (
    data[
      "construction_step"
    ].conclusion
    == data[
      "expected_construction"
    ]
  )

  assert (
    data[
      "construction_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_8_positive_branch_matches_toda_formula():
  data = build_phase60_8_data()

  assert (
    data[
      "construction_step"
    ].conclusion.positive_branch
    == TodaLemma54Nu4BranchFormula(
      double_suspension_sign=1,
      alpha_star_sign=1,
      whitehead_coefficient_sign=-1,
      parameter_offset=0,
    )
  )


def test_phase60_8_negative_branch_matches_toda_formula():
  data = build_phase60_8_data()

  assert (
    data[
      "construction_step"
    ].conclusion.negative_branch
    == TodaLemma54Nu4BranchFormula(
      double_suspension_sign=-1,
      alpha_star_sign=-1,
      whitehead_coefficient_sign=1,
      parameter_offset=1,
    )
  )


def test_phase60_8_construction_preserves_s():
  data = build_phase60_8_data()

  assert (
    data[
      "construction_step"
    ].conclusion.parameter
    == data[
      "s"
    ]
  )


def test_phase60_8_constructs_nu4():
  data = build_phase60_8_data()

  assert (
    data[
      "construction_step"
    ].conclusion.nu4
    == data[
      "nu4"
    ]
  )


def test_phase60_8_derives_nu4_membership():
  data = build_phase60_8_data()

  assert (
    data[
      "membership_step"
    ].conclusion
    == data[
      "expected_membership"
    ]
  )

  assert (
    data[
      "membership_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_8_derives_h_nu4_iota7():
  data = build_phase60_8_data()

  assert (
    data[
      "hopf_step"
    ].conclusion
    == data[
      "expected_hopf"
    ]
  )

  assert (
    data[
      "hopf_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_8_derives_two_e_nu4_e2_nu_prime():
  data = build_phase60_8_data()

  assert (
    data[
      "double_result_step"
    ].conclusion
    == data[
      "expected_double"
    ]
  )

  assert (
    data[
      "double_result_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase60_8_final_three_results_use_construction():
  data = build_phase60_8_data()

  for key in (
    "membership_step",
    "hopf_step",
    "double_result_step",
  ):
    assert (
      data[
        key
      ].premises
      == (
        data[
          "construction_step"
        ],
      )
    )


def test_phase60_8_final_results_are_not_given():
  data = build_phase60_8_data()

  assert (
    data[
      "membership_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "hopf_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "double_result_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase60_8_reaches_fixed_point_in_three_rounds():
  data = build_phase60_8_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3

  assert (
    data[
      "whitehead_data_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "construction_step"
    ]
    in result.round_results[
      1
    ].new_steps
  )

  assert (
    data[
      "membership_step"
    ]
    in result.round_results[
      2
    ].new_steps
  )

  assert (
    data[
      "hopf_step"
    ]
    in result.round_results[
      2
    ].new_steps
  )

  assert (
    data[
      "double_result_step"
    ]
    in result.round_results[
      2
    ].new_steps
  )


