from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Suspension,
  WhiteheadProduct,
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
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase60_nu4_whitehead_correction import (
  build_phase60_8_data,
)
from test_phase61_lemma55_alpha_star_inclusion import (
  build_phase61_3_data,
)
from toda_rules import (
  TodaLemma54Nu4BranchFormula,
  TodaLemma55SuspensionUpToSignStatement,
  toda_lemma55_nu4_suspension_correction_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase61_4_data():
  phase60_8 = (
    build_phase60_8_data()
  )

  phase61_3 = (
    build_phase61_3_data()
  )

  construction_step = (
    phase60_8[
      "construction_step"
    ]
  )

  construction = (
    construction_step
    .conclusion
  )

  alpha_star = (
    construction
    .alpha_star
  )

  nu4 = (
    construction
    .nu4
  )

  t = phase61_3[
    "t"
  ]

  t_range = ScalarGreaterEqualStatement(
    left=t,
    right=1,
  )

  t_range_step = ProofStep(
    conclusion=t_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  expected_statement = (
    TodaLemma55SuspensionUpToSignStatement(
      left=IteratedSuspension(
        expression=nu4,
        exponent=t,
      ),
      positive_value=IteratedSuspension(
        expression=alpha_star,
        exponent=t,
      ),
    )
  )

  rule = (
    toda_lemma55_nu4_suspension_correction_inference_rule()
  )

  premise_steps = (
    construction_step,
    t_range_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  suspension_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase60_8": phase60_8,
    "construction_step": (
      construction_step
    ),
    "construction": construction,
    "alpha_star": alpha_star,
    "nu4": nu4,
    "t": t,
    "t_range": t_range,
    "t_range_step": t_range_step,
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "suspension_step": (
      suspension_step
    ),
  }


def test_phase61_4_reuses_derived_nu4_construction():
  data = build_phase61_4_data()

  assert (
    data[
      "construction_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase61_4_construction_contains_alpha_star_and_nu4():
  data = build_phase61_4_data()

  construction = data[
    "construction"
  ]

  assert (
    construction.alpha_star
    == data[
      "alpha_star"
    ]
  )

  assert (
    construction.nu4
    == data[
      "nu4"
    ]
  )


def test_phase61_4_construction_preserves_whitehead_suspension_zero():
  data = build_phase61_4_data()

  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  whitehead_square = WhiteheadProduct(
    left=iota_4,
    right=iota_4,
  )

  assert (
    data[
      "construction"
    ]
    .whitehead_data
    .suspension_zero_relation
    == Relation(
      lhs=Suspension(
        expression=whitehead_square,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )


def test_phase61_4_construction_preserves_positive_branch():
  data = build_phase61_4_data()

  assert (
    data[
      "construction"
    ].positive_branch
    == TodaLemma54Nu4BranchFormula(
      double_suspension_sign=1,
      alpha_star_sign=1,
      whitehead_coefficient_sign=-1,
      parameter_offset=0,
    )
  )


def test_phase61_4_construction_preserves_negative_branch():
  data = build_phase61_4_data()

  assert (
    data[
      "construction"
    ].negative_branch
    == TodaLemma54Nu4BranchFormula(
      double_suspension_sign=-1,
      alpha_star_sign=-1,
      whitehead_coefficient_sign=1,
      parameter_offset=1,
    )
  )


def test_phase61_4_rule_matches_construction_and_positive_t():
  data = build_phase61_4_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase61_4_derives_suspension_up_to_sign():
  data = build_phase61_4_data()

  step = data[
    "suspension_step"
  ]

  assert (
    step.conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase61_4_left_is_et_nu4():
  data = build_phase61_4_data()

  assert (
    data[
      "suspension_step"
    ].conclusion.left
    == IteratedSuspension(
      expression=data[
        "nu4"
      ],
      exponent=data[
        "t"
      ],
    )
  )


def test_phase61_4_positive_value_is_et_alpha_star():
  data = build_phase61_4_data()

  assert (
    data[
      "suspension_step"
    ].conclusion.positive_value
    == IteratedSuspension(
      expression=data[
        "alpha_star"
      ],
      exponent=data[
        "t"
      ],
    )
  )


def test_phase61_4_provenance_uses_construction_and_t_range():
  data = build_phase61_4_data()

  assert (
    data[
      "suspension_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )


def test_phase61_4_rejects_given_construction():
  data = build_phase61_4_data()

  given_construction_step = ProofStep(
    conclusion=data[
      "construction"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      given_construction_step,
      data[
        "t_range_step"
      ],
    ),
  ) is None


def test_phase61_4_rejects_t_at_least_zero():
  data = build_phase61_4_data()

  wrong_range_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=data[
        "t"
      ],
      right=0,
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
        "construction_step"
      ],
      wrong_range_step,
    ),
  ) is None


def test_phase61_4_rejects_wrong_positive_branch():
  data = build_phase61_4_data()

  wrong_construction = replace(
    data[
      "construction"
    ],
    positive_branch=(
      TodaLemma54Nu4BranchFormula(
        double_suspension_sign=1,
        alpha_star_sign=-1,
        whitehead_coefficient_sign=-1,
        parameter_offset=0,
      )
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_construction,
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
        "t_range_step"
      ],
    ),
  ) is None


def test_phase61_4_rejects_wrong_whitehead_suspension_relation():
  data = build_phase61_4_data()

  wrong_whitehead_data = replace(
    data[
      "construction"
    ].whitehead_data,
    suspension_zero_relation=Relation(
      lhs=Suspension(
        expression=(
          data[
            "construction"
          ]
          .whitehead_data
          .whitehead_square
        ),
      ),
      rhs=(
        data[
          "construction"
        ]
        .whitehead_data
        .whitehead_square
      ),
      relation_type=RelationType.EQUALITY,
    ),
  )

  wrong_construction = replace(
    data[
      "construction"
    ],
    whitehead_data=wrong_whitehead_data,
  )

  wrong_step = ProofStep(
    conclusion=wrong_construction,
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
        "t_range_step"
      ],
    ),
  ) is None


def test_phase61_4_final_result_is_not_given():
  data = build_phase61_4_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_statement"
    ]
    not in initial_conclusions
  )

  assert (
    data[
      "suspension_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase61_4_reaches_fixed_point_in_one_round():
  data = build_phase61_4_data()

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
      "suspension_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )



