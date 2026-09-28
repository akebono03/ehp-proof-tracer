from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  ScalarSum,
  ScalarSymbol,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase75_515_pi15_8_final_group import (
  build_phase75_8e4_data,
)
from test_phase75_pi12_5_order_two import (
  build_phase75_5_data,
)
from test_phase75_pi13_6_order_four import (
  build_phase75_6c_data,
)
from test_phase75_pi14_7_order_eight import (
  build_phase75_7c_data,
)
from test_phase75_sigma_stable_transport import (
  build_phase75_8d_data,
)
from toda_rules import (
  TodaProp515FiniteDimensionalStatement,
  toda_prop515_finite_dimensional_integration_inference_rule,
  toda_prop515_finite_dimensional_literature_statements,
)


@lru_cache(maxsize=1)
def build_phase75_9_data():
  phase75_5 = (
    build_phase75_5_data()
  )

  phase75_6c = (
    build_phase75_6c_data()
  )

  phase75_7c = (
    build_phase75_7c_data()
  )

  phase75_8d = (
    build_phase75_8d_data()
  )

  phase75_8e4 = (
    build_phase75_8e4_data()
  )

  phase75_4 = (
    phase75_5[
      "phase75_4"
    ]
  )

  phase75_3 = (
    phase75_4[
      "phase75_3"
    ]
  )

  pi9_2_step = (
    phase75_3[
      "pi9_2_zero_step"
    ]
  )

  pi10_3_step = (
    phase75_4[
      "pi10_3_zero_step"
    ]
  )

  pi11_4_step = (
    phase75_5[
      "pi11_4_zero_step"
    ]
  )

  pi12_5_step = (
    phase75_5[
      "final_step"
    ]
  )

  pi13_6_step = (
    phase75_6c[
      "final_step"
    ]
  )

  pi14_7_step = (
    phase75_7c[
      "final_step"
    ]
  )

  pi15_8_step = (
    phase75_8e4[
      "final_step"
    ]
  )

  higher_step = (
    phase75_8d[
      "final_step"
    ]
  )

  higher_range_step = (
    phase75_8d[
      "suspension_range_step"
    ]
  )

  rule = (
    toda_prop515_finite_dimensional_integration_inference_rule()
  )

  premise_steps = (
    pi9_2_step,
    pi10_3_step,
    pi11_4_step,
    pi12_5_step,
    pi13_6_step,
    pi14_7_step,
    pi15_8_step,
    higher_step,
    higher_range_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      premise_steps,
    )
  )

  expected_statement = (
    TodaProp515FiniteDimensionalStatement(
      pi9_2_zero=(
        pi9_2_step
        .conclusion
      ),
      pi10_3_zero=(
        pi10_3_step
        .conclusion
      ),
      pi11_4_zero=(
        pi11_4_step
        .conclusion
      ),
      pi12_5_group_relation=(
        pi12_5_step
        .conclusion
      ),
      pi13_6_group_relation=(
        pi13_6_step
        .conclusion
      ),
      pi14_7_group_relation=(
        pi14_7_step
        .conclusion
      ),
      pi15_8_group_relation=(
        pi15_8_step
        .conclusion
      ),
      higher_seven_stem_group_relation=(
        higher_step
        .conclusion
      ),
      higher_range=(
        higher_range_step
        .conclusion
      ),
      literature_statements=(
        toda_prop515_finite_dimensional_literature_statements()
      ),
    )
  )

  aggregate_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase75_5": phase75_5,
    "phase75_4": phase75_4,
    "phase75_3": phase75_3,
    "phase75_6c": phase75_6c,
    "phase75_7c": phase75_7c,
    "phase75_8d": phase75_8d,
    "phase75_8e4": phase75_8e4,
    "pi9_2_step": pi9_2_step,
    "pi10_3_step": pi10_3_step,
    "pi11_4_step": pi11_4_step,
    "pi12_5_step": pi12_5_step,
    "pi13_6_step": pi13_6_step,
    "pi14_7_step": pi14_7_step,
    "pi15_8_step": pi15_8_step,
    "higher_step": higher_step,
    "higher_range_step": (
      higher_range_step
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "expected_statement": (
      expected_statement
    ),
    "aggregate_step": (
      aggregate_step
    ),
  }


def test_phase75_9_all_direct_mathematical_branches_are_inference():
  data = build_phase75_9_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in (
      data[
        "pi9_2_step"
      ],
      data[
        "pi10_3_step"
      ],
      data[
        "pi11_4_step"
      ],
      data[
        "pi12_5_step"
      ],
      data[
        "pi13_6_step"
      ],
      data[
        "pi14_7_step"
      ],
      data[
        "pi15_8_step"
      ],
      data[
        "higher_step"
      ],
    )
  )


def test_phase75_9_higher_range_remains_given():
  data = build_phase75_9_data()

  assert (
    data[
      "higher_range_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "higher_range_step"
    ].conclusion
    == ScalarGreaterEqualStatement(
      left=data[
        "higher_step"
      ].conclusion
      .lhs
      .sphere_dimension,
      right=9,
    )
  )


def test_phase75_9_three_low_groups_are_zero():
  data = build_phase75_9_data()

  assert (
    data[
      "pi9_2_step"
    ].conclusion
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=2,
      ),
    )
  )

  assert (
    data[
      "pi10_3_step"
    ].conclusion
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=3,
      ),
    )
  )

  assert (
    data[
      "pi11_4_step"
    ].conclusion
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=4,
      ),
    )
  )


def test_phase75_9_pi12_5_is_z2_sigma_triple_prime():
  data = build_phase75_9_data()

  relation = (
    data[
      "pi12_5_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=5,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 2
  )

  assert (
    relation.rhs.generator.generator
    == GeneratorSymbol(
      family="σ",
      decoration="'''",
    )
  )


def test_phase75_9_pi13_6_is_z4_sigma_double_prime():
  data = build_phase75_9_data()

  relation = (
    data[
      "pi13_6_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=6,
    )
  )

  assert (
    relation.rhs.order
    == 4
  )

  assert (
    relation.rhs.generator.generator
    == GeneratorSymbol(
      family="σ",
      decoration="''",
    )
  )


def test_phase75_9_pi14_7_is_z8_sigma_prime():
  data = build_phase75_9_data()

  relation = (
    data[
      "pi14_7_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=7,
    )
  )

  assert (
    relation.rhs.order
    == 8
  )

  assert (
    relation.rhs.generator.generator
    == GeneratorSymbol(
      family="σ",
      decoration="'",
    )
  )


def test_phase75_9_pi15_8_has_expected_mixed_decomposition():
  data = build_phase75_9_data()

  relation = (
    data[
      "pi15_8_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=15,
      sphere_dimension=8,
    )
  )

  assert isinstance(
    relation.rhs,
    DirectSumGroup,
  )

  assert isinstance(
    relation.rhs.summands[
      0
    ],
    FreeCyclicGroup,
  )

  assert isinstance(
    relation.rhs.summands[
      1
    ],
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs
    .summands[
      1
    ].order
    == 8
  )


def test_phase75_9_pi15_8_generators_are_sigma8_and_e_sigma_prime():
  data = build_phase75_9_data()

  relation = (
    data[
      "pi15_8_step"
    ].conclusion
  )

  sigma8 = (
    relation.rhs
    .summands[
      0
    ].generator
  )

  e_sigma_prime = (
    relation.rhs
    .summands[
      1
    ].generator
  )

  assert (
    sigma8.generator
    == GeneratorSymbol(
      family="σ",
      index=8,
    )
  )

  assert isinstance(
    e_sigma_prime,
    Suspension,
  )

  assert (
    e_sigma_prime
    .expression
    .generator
    == GeneratorSymbol(
      family="σ",
      decoration="'",
    )
  )


def test_phase75_9_higher_relation_is_z16_sigma_n():
  data = build_phase75_9_data()

  relation = (
    data[
      "higher_step"
    ].conclusion
  )

  n = (
    relation.lhs
    .sphere_dimension
  )

  assert isinstance(
    n,
    ScalarSymbol,
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=7,
      ),
      sphere_dimension=n,
    )
  )

  assert (
    relation.rhs.order
    == 16
  )

  assert (
    relation.rhs.generator.generator
    == GeneratorSymbol(
      family="σ",
      index=n,
    )
  )


def test_phase75_9_derives_expected_aggregate():
  data = build_phase75_9_data()

  assert (
    data[
      "aggregate_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "aggregate_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_9_aggregate_uses_exact_direct_premises():
  data = build_phase75_9_data()

  assert (
    data[
      "aggregate_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )


def test_phase75_9_aggregate_preserves_branch_objects():
  data = build_phase75_9_data()

  statement = (
    data[
      "aggregate_step"
    ].conclusion
  )

  assert (
    statement.pi9_2_zero
    is data[
      "pi9_2_step"
    ].conclusion
  )

  assert (
    statement.pi10_3_zero
    is data[
      "pi10_3_step"
    ].conclusion
  )

  assert (
    statement.pi11_4_zero
    is data[
      "pi11_4_step"
    ].conclusion
  )

  assert (
    statement.pi12_5_group_relation
    is data[
      "pi12_5_step"
    ].conclusion
  )

  assert (
    statement.pi13_6_group_relation
    is data[
      "pi13_6_step"
    ].conclusion
  )

  assert (
    statement.pi14_7_group_relation
    is data[
      "pi14_7_step"
    ].conclusion
  )

  assert (
    statement.pi15_8_group_relation
    is data[
      "pi15_8_step"
    ].conclusion
  )

  assert (
    statement.higher_seven_stem_group_relation
    is data[
      "higher_step"
    ].conclusion
  )


def test_phase75_9_has_proposition_515_literature():
  data = build_phase75_9_data()

  literature = (
    data[
      "aggregate_step"
    ].conclusion
    .literature_statements
  )

  assert (
    literature
    == toda_prop515_finite_dimensional_literature_statements()
  )

  assert any(
    statement.reference.label
    == "Toda Proposition 5.15"
    for statement
    in literature
  )


def test_phase75_9_stable_g7_is_excluded():
  data = build_phase75_9_data()

  statement = (
    data[
      "aggregate_step"
    ].conclusion
  )

  assert not hasattr(
    statement,
    "stable_group_relation",
  )

  assert all(
    "(G_7;2)"
    not in literature.statement
    or "not included"
    in literature.statement
    for literature
    in statement.literature_statements
  )


def test_phase75_9_final_not_present_initially():
  data = build_phase75_9_data()

  assert (
    data[
      "expected_statement"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase75_9_rejects_given_pi15_8():
  data = build_phase75_9_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi15_8_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  premises = list(
    data[
      "premise_steps"
    ]
  )

  premises[
    6
  ] = given

  assert find_inference_match(
    data[
      "rule"
    ],
    tuple(
      premises
    ),
  ) is None


def test_phase75_9_rejects_given_higher_relation():
  data = build_phase75_9_data()

  given = ProofStep(
    conclusion=(
      data[
        "higher_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  premises = list(
    data[
      "premise_steps"
    ]
  )

  premises[
    7
  ] = given

  assert find_inference_match(
    data[
      "rule"
    ],
    tuple(
      premises
    ),
  ) is None


def test_phase75_9_rejects_wrong_higher_range():
  data = build_phase75_9_data()

  n = (
    data[
      "higher_step"
    ].conclusion
    .lhs
    .sphere_dimension
  )

  wrong_range = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=n,
      right=8,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  premises = list(
    data[
      "premise_steps"
    ]
  )

  premises[
    8
  ] = wrong_range

  assert find_inference_match(
    data[
      "rule"
    ],
    tuple(
      premises
    ),
  ) is None


def test_phase75_9_rejects_wrong_pi12_5_order():
  data = build_phase75_9_data()

  relation = (
    data[
      "pi12_5_step"
    ].conclusion
  )

  wrong_relation = replace(
    relation,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=(
        relation
        .rhs
        .generator
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  premises = list(
    data[
      "premise_steps"
    ]
  )

  premises[
    3
  ] = wrong_step

  assert find_inference_match(
    data[
      "rule"
    ],
    tuple(
      premises
    ),
  ) is None


def test_phase75_9_rejects_wrong_pi15_8_torsion_order():
  data = build_phase75_9_data()

  relation = (
    data[
      "pi15_8_step"
    ].conclusion
  )

  free_summand = (
    relation.rhs
    .summands[
      0
    ]
  )

  torsion_summand = (
    relation.rhs
    .summands[
      1
    ]
  )

  wrong_relation = replace(
    relation,
    rhs=DirectSumGroup(
      summands=(
        free_summand,
        FiniteCyclicGroup(
          order=4,
          generator=(
            torsion_summand
            .generator
          ),
        ),
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  premises = list(
    data[
      "premise_steps"
    ]
  )

  premises[
    6
  ] = wrong_step

  assert find_inference_match(
    data[
      "rule"
    ],
    tuple(
      premises
    ),
  ) is None


def test_phase75_9_rejects_wrong_higher_order():
  data = build_phase75_9_data()

  relation = (
    data[
      "higher_step"
    ].conclusion
  )

  wrong_relation = replace(
    relation,
    rhs=FiniteCyclicGroup(
      order=8,
      generator=(
        relation
        .rhs
        .generator
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  premises = list(
    data[
      "premise_steps"
    ]
  )

  premises[
    7
  ] = wrong_step

  assert find_inference_match(
    data[
      "rule"
    ],
    tuple(
      premises
    ),
  ) is None


def test_phase75_9_reaches_fixed_point():
  data = build_phase75_9_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


