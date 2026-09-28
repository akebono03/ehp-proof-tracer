from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from low_dimensional_facts import (
  pi_7_7_free_cyclic_fact,
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
from probes.probe_phase63_capabilities import (
  build_phase63_representative_result,
)
from test_phase65_nu_prime_order_pi6_3 import (
  build_phase65_4_data,
)
from toda_rules import (
  Toda56Nu4DecompositionStatement,
  toda_prop56_pi7_4_decomposition_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase65_5_data():
  phase63 = (
    build_phase63_representative_result()
  )

  phase65_4 = (
    build_phase65_4_data()
  )

  toda56_step = (
    phase63[
      "integration_step"
    ]
  )

  pi6_3_step = (
    phase65_4[
      "pi6_3_step"
    ]
  )

  pi7_7_relation = (
    pi_7_7_free_cyclic_fact()
  )

  pi7_7_step = ProofStep(
    conclusion=pi7_7_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nu_4 = (
    toda56_step
    .conclusion
    .lemma54_statement
    .nu4
  )

  nu_prime = (
    pi6_3_step
    .conclusion
    .rhs
    .generator
  )

  e_nu_prime = Suspension(
    expression=nu_prime,
  )

  expected_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
    ),
    rhs=DirectSumGroup(
      summands=(
        FreeCyclicGroup(
          generator=nu_4,
        ),
        FiniteCyclicGroup(
          order=4,
          generator=e_nu_prime,
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  rule = (
    toda_prop56_pi7_4_decomposition_inference_rule()
  )

  premise_steps = (
    toda56_step,
    pi6_3_step,
    pi7_7_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_relation
    )
  )

  return {
    "phase63": phase63,
    "phase65_4": phase65_4,
    "toda56_step": toda56_step,
    "pi6_3_step": pi6_3_step,
    "pi7_7_relation": (
      pi7_7_relation
    ),
    "pi7_7_step": pi7_7_step,
    "nu_4": nu_4,
    "nu_prime": nu_prime,
    "e_nu_prime": e_nu_prime,
    "expected_relation": (
      expected_relation
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "final_step": final_step,
  }


def test_phase65_5_reuses_derived_toda56():
  data = build_phase65_5_data()

  assert isinstance(
    data[
      "toda56_step"
    ].conclusion,
    Toda56Nu4DecompositionStatement,
  )

  assert (
    data[
      "toda56_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_5_reuses_phase65_4_pi6_3():
  data = build_phase65_5_data()

  assert (
    data[
      "pi6_3_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi6_3_step"
    ].conclusion
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=4,
        generator=data[
          "nu_prime"
        ],
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase65_5_pi7_7_fact_is_free_cyclic():
  data = build_phase65_5_data()

  assert (
    data[
      "pi7_7_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "pi7_7_relation"
    ]
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=7,
      ),
      rhs=FreeCyclicGroup(
        generator=HomotopyElement(
          name="ι_7",
          dimension=7,
          generator=GeneratorSymbol(
            family="ι",
            index=7,
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase65_5_rule_matches_dependencies():
  data = build_phase65_5_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase65_5_derives_pi7_4_decomposition():
  data = build_phase65_5_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_relation"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_5_final_group_is_direct_sum():
  data = build_phase65_5_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion.rhs,
    DirectSumGroup,
  )

  assert (
    len(
      data[
        "final_step"
      ].conclusion.rhs.summands
    )
    == 2
  )


def test_phase65_5_first_summand_is_free_nu4():
  data = build_phase65_5_data()

  first = (
    data[
      "final_step"
    ].conclusion.rhs.summands[
      0
    ]
  )

  assert isinstance(
    first,
    FreeCyclicGroup,
  )

  assert (
    first.generator
    == data[
      "nu_4"
    ]
  )


def test_phase65_5_second_summand_is_order_four():
  data = build_phase65_5_data()

  second = (
    data[
      "final_step"
    ].conclusion.rhs.summands[
      1
    ]
  )

  assert isinstance(
    second,
    FiniteCyclicGroup,
  )

  assert second.order == 4


def test_phase65_5_second_generator_is_e_nu_prime():
  data = build_phase65_5_data()

  second = (
    data[
      "final_step"
    ].conclusion.rhs.summands[
      1
    ]
  )

  assert (
    second.generator
    == Suspension(
      expression=data[
        "nu_prime"
      ],
    )
  )


def test_phase65_5_preserves_phase63_nu4():
  data = build_phase65_5_data()

  assert (
    data[
      "final_step"
    ].conclusion.rhs.summands[
      0
    ].generator
    is data[
      "nu_4"
    ]
  )


def test_phase65_5_provenance_uses_exactly_three_premises():
  data = build_phase65_5_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "toda56_step"
      ],
      data[
        "pi6_3_step"
      ],
      data[
        "pi7_7_step"
      ],
    )
  )


def test_phase65_5_derived_dependencies_remain_inference():
  data = build_phase65_5_data()

  assert (
    data[
      "toda56_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi6_3_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_5_rejects_given_toda56():
  data = build_phase65_5_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "toda56_step"
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
      given_step,
      data[
        "pi6_3_step"
      ],
      data[
        "pi7_7_step"
      ],
    ),
  ) is None


def test_phase65_5_rejects_given_pi6_3():
  data = build_phase65_5_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "pi6_3_step"
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
        "toda56_step"
      ],
      given_step,
      data[
        "pi7_7_step"
      ],
    ),
  ) is None


def test_phase65_5_rejects_wrong_pi7_7_generator():
  data = build_phase65_5_data()

  wrong_iota = HomotopyElement(
    name="ι_6",
    dimension=6,
    generator=GeneratorSymbol(
      family="ι",
      index=6,
    ),
  )

  wrong_step = ProofStep(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=7,
      ),
      rhs=FreeCyclicGroup(
        generator=wrong_iota,
      ),
      relation_type=RelationType.EQUALITY,
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
        "toda56_step"
      ],
      data[
        "pi6_3_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase65_5_final_result_is_not_given():
  data = build_phase65_5_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "expected_relation"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase65_5_reaches_fixed_point_in_one_round():
  data = build_phase65_5_data()

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


