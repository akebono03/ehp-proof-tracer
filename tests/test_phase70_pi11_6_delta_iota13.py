from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
  Suspension,
  Zero,
)
from homotopy_groups import (
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from test_phase70_nu5_eta8_squared_zero_delta_eta11 import (
  build_phase70_7_data,
)
from toda_rules import (
  TodaDeltaKernelFreeCyclicStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  TodaProp42ExactnessStatement,
  toda_prop59_delta_iota13_hopf_inference_rule,
  toda_prop59_pi11_11_delta_kernel_inference_rule,
  toda_prop59_pi11_6_concrete_exactness_inference_rule,
  toda_prop59_pi11_6_free_cyclic_inference_rule,
  toda_prop59_pi11_6_hopf_injective_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase70_8_data():
  phase70_7 = (
    build_phase70_7_data()
  )

  phase70_6 = (
    phase70_7[
      "phase70_6"
    ]
  )

  phase69_3 = (
    phase70_7[
      "phase69_3"
    ]
  )

  pi10_5_step = (
    phase70_7[
      "pi10_5_step"
    ]
  )

  suspension_zero_step = (
    phase70_7[
      "suspension_zero_step"
    ]
  )

  pi11_11_step = (
    phase69_3[
      "pi11_11_step"
    ]
  )

  pi9_5_step = (
    phase69_3[
      "pi9_5_step"
    ]
  )

  delta_iota11_step = (
    phase69_3[
      "final_step"
    ]
  )

  pi10_5 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  pi11_6 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=6,
  )

  pi11_11 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=11,
  )

  pi9_5 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  pi13_13 = TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=13,
  )

  e_h_window = TodaEHPExactnessWindow(
    source_term=pi10_5,
    middle_term=pi11_6,
    target_term=pi11_11,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )

  e_h_window_step = ProofStep(
    conclusion=e_h_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  h_delta_window = TodaEHPExactnessWindow(
    source_term=pi11_6,
    middle_term=pi11_11,
    target_term=pi9_5,
    first_map=EHP_H_MAP,
    second_map=EHP_DELTA_MAP,
  )

  h_delta_window_step = ProofStep(
    conclusion=h_delta_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  iota_13 = HomotopyElement(
    name="ι_13",
    dimension=13,
    generator=GeneratorSymbol(
      family="ι",
      index=13,
    ),
  )

  pi13_13_relation = Relation(
    lhs=pi13_13,
    rhs=FreeCyclicGroup(
      generator=iota_13,
    ),
    relation_type=RelationType.EQUALITY,
  )

  pi13_13_step = ProofStep(
    conclusion=pi13_13_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  exactness_rule = (
    toda_prop59_pi11_6_concrete_exactness_inference_rule()
  )

  hopf_injective_rule = (
    toda_prop59_pi11_6_hopf_injective_inference_rule()
  )

  delta_kernel_rule = (
    toda_prop59_pi11_11_delta_kernel_inference_rule()
  )

  hopf_value_rule = (
    toda_prop59_delta_iota13_hopf_inference_rule()
  )

  final_rule = (
    toda_prop59_pi11_6_free_cyclic_inference_rule()
  )

  e_h_exactness_match = (
    find_inference_match(
      exactness_rule,
      (
        e_h_window_step,
      ),
    )
  )

  assert (
    e_h_exactness_match
    is not None
  )

  e_h_exactness_step = (
    apply_inference_match(
      e_h_exactness_match
    )
  )

  h_delta_exactness_match = (
    find_inference_match(
      exactness_rule,
      (
        h_delta_window_step,
      ),
    )
  )

  assert (
    h_delta_exactness_match
    is not None
  )

  h_delta_exactness_step = (
    apply_inference_match(
      h_delta_exactness_match
    )
  )

  hopf_injective_match = (
    find_inference_match(
      hopf_injective_rule,
      (
        suspension_zero_step,
        pi10_5_step,
        e_h_exactness_step,
      ),
    )
  )

  assert (
    hopf_injective_match
    is not None
  )

  hopf_injective_step = (
    apply_inference_match(
      hopf_injective_match
    )
  )

  delta_kernel_match = (
    find_inference_match(
      delta_kernel_rule,
      (
        pi11_11_step,
        pi9_5_step,
        delta_iota11_step,
      ),
    )
  )

  assert (
    delta_kernel_match
    is not None
  )

  delta_kernel_step = (
    apply_inference_match(
      delta_kernel_match
    )
  )

  hopf_value_match = (
    find_inference_match(
      hopf_value_rule,
      (
        pi13_13_step,
      ),
    )
  )

  assert (
    hopf_value_match
    is not None
  )

  hopf_value_step = (
    apply_inference_match(
      hopf_value_match
    )
  )

  final_match = (
    find_inference_match(
      final_rule,
      (
        hopf_injective_step,
        h_delta_exactness_step,
        delta_kernel_step,
        hopf_value_step,
      ),
    )
  )

  assert (
    final_match
    is not None
  )

  final_step = (
    apply_inference_match(
      final_match
    )
  )

  iota_11 = (
    pi11_11_step
    .conclusion
    .rhs
    .generator
  )

  two_iota_11 = Multiple(
    coefficient=2,
    expression=iota_11,
  )

  delta_iota13 = MapApplication(
    map=EHP_DELTA_MAP,
    expression=iota_13,
  )

  expected_e_h_exactness = (
    TodaProp42ExactnessStatement(
      window=e_h_window,
    )
  )

  expected_h_delta_exactness = (
    TodaProp42ExactnessStatement(
      window=h_delta_window,
    )
  )

  expected_hopf_injective = (
    TodaHopfInvariantInjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=pi11_6,
        target_group=pi11_11,
      ),
    )
  )

  expected_delta_kernel = (
    TodaDeltaKernelFreeCyclicStatement(
      map=TodaDeltaMap(
        source_group=pi11_11,
        target_group=pi9_5,
      ),
      kernel_group=FreeCyclicGroup(
        generator=two_iota_11,
      ),
    )
  )

  expected_hopf_value = (
    TodaProp27HopfInvariantUpToSignStatement(
      argument=delta_iota13,
      positive_value=two_iota_11,
    )
  )

  expected_final = Relation(
    lhs=pi11_6,
    rhs=FreeCyclicGroup(
      generator=delta_iota13,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    e_h_exactness_step.conclusion
    == expected_e_h_exactness
  )

  assert (
    h_delta_exactness_step.conclusion
    == expected_h_delta_exactness
  )

  assert (
    hopf_injective_step.conclusion
    == expected_hopf_injective
  )

  assert (
    delta_kernel_step.conclusion
    == expected_delta_kernel
  )

  assert (
    hopf_value_step.conclusion
    == expected_hopf_value
  )

  assert (
    final_step.conclusion
    == expected_final
  )

  return {
    "phase70_7": phase70_7,
    "phase70_6": phase70_6,
    "phase69_3": phase69_3,
    "pi10_5_step": pi10_5_step,
    "suspension_zero_step": (
      suspension_zero_step
    ),
    "pi11_11_step": pi11_11_step,
    "pi9_5_step": pi9_5_step,
    "delta_iota11_step": (
      delta_iota11_step
    ),
    "pi10_5": pi10_5,
    "pi11_6": pi11_6,
    "pi11_11": pi11_11,
    "pi9_5": pi9_5,
    "pi13_13": pi13_13,
    "e_h_window": e_h_window,
    "e_h_window_step": (
      e_h_window_step
    ),
    "h_delta_window": h_delta_window,
    "h_delta_window_step": (
      h_delta_window_step
    ),
    "iota_13": iota_13,
    "pi13_13_relation": (
      pi13_13_relation
    ),
    "pi13_13_step": pi13_13_step,
    "exactness_rule": exactness_rule,
    "hopf_injective_rule": (
      hopf_injective_rule
    ),
    "delta_kernel_rule": (
      delta_kernel_rule
    ),
    "hopf_value_rule": hopf_value_rule,
    "final_rule": final_rule,
    "e_h_exactness_match": (
      e_h_exactness_match
    ),
    "e_h_exactness_step": (
      e_h_exactness_step
    ),
    "h_delta_exactness_match": (
      h_delta_exactness_match
    ),
    "h_delta_exactness_step": (
      h_delta_exactness_step
    ),
    "hopf_injective_match": (
      hopf_injective_match
    ),
    "hopf_injective_step": (
      hopf_injective_step
    ),
    "delta_kernel_match": (
      delta_kernel_match
    ),
    "delta_kernel_step": (
      delta_kernel_step
    ),
    "hopf_value_match": (
      hopf_value_match
    ),
    "hopf_value_step": (
      hopf_value_step
    ),
    "final_match": final_match,
    "final_step": final_step,
    "iota_11": iota_11,
    "two_iota_11": two_iota_11,
    "delta_iota13": delta_iota13,
    "expected_e_h_exactness": (
      expected_e_h_exactness
    ),
    "expected_h_delta_exactness": (
      expected_h_delta_exactness
    ),
    "expected_hopf_injective": (
      expected_hopf_injective
    ),
    "expected_delta_kernel": (
      expected_delta_kernel
    ),
    "expected_hopf_value": (
      expected_hopf_value
    ),
    "expected_final": expected_final,
  }


def test_phase70_8_reuses_phase70_7_suspension_zero():
  data = build_phase70_8_data()

  assert (
    data[
      "suspension_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "suspension_zero_step"
    ].conclusion
    == Relation(
      lhs=Suspension(
        expression=(
          data[
            "pi10_5_step"
          ]
          .conclusion
          .rhs
          .generator
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )


def test_phase70_8_reuses_phase70_6_pi10_5():
  data = build_phase70_8_data()

  assert (
    data[
      "pi10_5_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi10_5_step"
    ].conclusion.lhs
    == data[
      "pi10_5"
    ]
  )


def test_phase70_8_reuses_phase69_pi11_11():
  data = build_phase70_8_data()

  assert (
    data[
      "pi11_11_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert isinstance(
    data[
      "pi11_11_step"
    ].conclusion.rhs,
    FreeCyclicGroup,
  )


def test_phase70_8_reuses_phase69_pi9_5():
  data = build_phase70_8_data()

  assert (
    data[
      "pi9_5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_8_reuses_phase69_delta_iota11():
  data = build_phase70_8_data()

  assert (
    data[
      "delta_iota11_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "delta_iota11_step"
    ].conclusion.lhs
    == MapApplication(
      map=EHP_DELTA_MAP,
      expression=data[
        "iota_11"
      ],
    )
  )


def test_phase70_8_exactness_windows_remain_given():
  data = build_phase70_8_data()

  assert (
    data[
      "e_h_window_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "h_delta_window_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase70_8_derives_e_h_exactness():
  data = build_phase70_8_data()

  assert (
    data[
      "e_h_exactness_step"
    ].conclusion
    == data[
      "expected_e_h_exactness"
    ]
  )

  assert (
    data[
      "e_h_exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_8_derives_h_delta_exactness():
  data = build_phase70_8_data()

  assert (
    data[
      "h_delta_exactness_step"
    ].conclusion
    == data[
      "expected_h_delta_exactness"
    ]
  )

  assert (
    data[
      "h_delta_exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_8_hopf_injective_matches():
  data = build_phase70_8_data()

  assert (
    data[
      "hopf_injective_match"
    ]
    is not None
  )


def test_phase70_8_derives_hopf_injective():
  data = build_phase70_8_data()

  assert (
    data[
      "hopf_injective_step"
    ].conclusion
    == data[
      "expected_hopf_injective"
    ]
  )

  assert (
    data[
      "hopf_injective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_8_hopf_injective_uses_exact_dependencies():
  data = build_phase70_8_data()

  assert (
    data[
      "hopf_injective_step"
    ].premises
    == (
      data[
        "suspension_zero_step"
      ],
      data[
        "pi10_5_step"
      ],
      data[
        "e_h_exactness_step"
      ],
    )
  )


def test_phase70_8_delta_kernel_matches():
  data = build_phase70_8_data()

  assert (
    data[
      "delta_kernel_match"
    ]
    is not None
  )


def test_phase70_8_derives_delta_kernel():
  data = build_phase70_8_data()

  assert (
    data[
      "delta_kernel_step"
    ].conclusion
    == data[
      "expected_delta_kernel"
    ]
  )

  assert (
    data[
      "delta_kernel_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_8_delta_kernel_is_two_iota11():
  data = build_phase70_8_data()

  kernel = (
    data[
      "delta_kernel_step"
    ].conclusion.kernel_group
  )

  assert isinstance(
    kernel,
    FreeCyclicGroup,
  )

  assert (
    kernel.generator
    == Multiple(
      coefficient=2,
      expression=data[
        "iota_11"
      ],
    )
  )


def test_phase70_8_delta_kernel_uses_exact_dependencies():
  data = build_phase70_8_data()

  assert (
    data[
      "delta_kernel_step"
    ].premises
    == (
      data[
        "pi11_11_step"
      ],
      data[
        "pi9_5_step"
      ],
      data[
        "delta_iota11_step"
      ],
    )
  )


def test_phase70_8_pi13_13_remains_foundational_given():
  data = build_phase70_8_data()

  assert (
    data[
      "pi13_13_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "pi13_13_step"
    ].conclusion
    == Relation(
      lhs=data[
        "pi13_13"
      ],
      rhs=FreeCyclicGroup(
        generator=data[
          "iota_13"
        ],
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase70_8_hopf_value_matches():
  data = build_phase70_8_data()

  assert (
    data[
      "hopf_value_match"
    ]
    is not None
  )


def test_phase70_8_derives_prop27_hopf_value():
  data = build_phase70_8_data()

  assert (
    data[
      "hopf_value_step"
    ].conclusion
    == data[
      "expected_hopf_value"
    ]
  )

  assert (
    data[
      "hopf_value_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_8_hopf_value_is_two_iota11_up_to_sign():
  data = build_phase70_8_data()

  assert (
    data[
      "hopf_value_step"
    ].conclusion.positive_value
    == data[
      "two_iota_11"
    ]
  )


def test_phase70_8_hopf_value_argument_is_delta_iota13():
  data = build_phase70_8_data()

  assert (
    data[
      "hopf_value_step"
    ].conclusion.argument
    == data[
      "delta_iota13"
    ]
  )


def test_phase70_8_hopf_value_uses_exact_dependency():
  data = build_phase70_8_data()

  assert (
    data[
      "hopf_value_step"
    ].premises
    == (
      data[
        "pi13_13_step"
      ],
    )
  )


def test_phase70_8_final_matches():
  data = build_phase70_8_data()

  assert (
    data[
      "final_match"
    ]
    is not None
  )


def test_phase70_8_derives_pi11_6():
  data = build_phase70_8_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_final"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_8_pi11_6_is_free_cyclic():
  data = build_phase70_8_data()

  group = (
    data[
      "final_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    FreeCyclicGroup,
  )


def test_phase70_8_final_generator_is_delta_iota13():
  data = build_phase70_8_data()

  generator = (
    data[
      "final_step"
    ].conclusion.rhs.generator
  )

  assert (
    generator
    is data[
      "hopf_value_step"
    ].conclusion.argument
  )

  assert (
    generator
    == MapApplication(
      map=EHP_DELTA_MAP,
      expression=data[
        "iota_13"
      ],
    )
  )


def test_phase70_8_final_uses_exact_four_dependencies():
  data = build_phase70_8_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "hopf_injective_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
      data[
        "delta_kernel_step"
      ],
      data[
        "hopf_value_step"
      ],
    )
  )


def test_phase70_8_hopf_injective_rejects_given_suspension_zero():
  data = build_phase70_8_data()

  given = ProofStep(
    conclusion=(
      data[
        "suspension_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "hopf_injective_rule"
    ],
    (
      given,
      data[
        "pi10_5_step"
      ],
      data[
        "e_h_exactness_step"
      ],
    ),
  ) is None


def test_phase70_8_delta_kernel_rejects_inference_pi11_11():
  data = build_phase70_8_data()

  derived = ProofStep(
    conclusion=(
      data[
        "pi11_11_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "delta_kernel_rule"
    ],
    (
      derived,
      data[
        "pi9_5_step"
      ],
      data[
        "delta_iota11_step"
      ],
    ),
  ) is None


def test_phase70_8_delta_kernel_rejects_given_pi9_5():
  data = build_phase70_8_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi9_5_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "delta_kernel_rule"
    ],
    (
      data[
        "pi11_11_step"
      ],
      given,
      data[
        "delta_iota11_step"
      ],
    ),
  ) is None


def test_phase70_8_hopf_value_rejects_inference_pi13_13():
  data = build_phase70_8_data()

  derived = ProofStep(
    conclusion=(
      data[
        "pi13_13_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "hopf_value_rule"
    ],
    (
      derived,
    ),
  ) is None


def test_phase70_8_final_rejects_given_hopf_injective():
  data = build_phase70_8_data()

  given = ProofStep(
    conclusion=(
      data[
        "hopf_injective_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      given,
      data[
        "h_delta_exactness_step"
      ],
      data[
        "delta_kernel_step"
      ],
      data[
        "hopf_value_step"
      ],
    ),
  ) is None


def test_phase70_8_final_rejects_given_delta_kernel():
  data = build_phase70_8_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_kernel_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "hopf_injective_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
      given,
      data[
        "hopf_value_step"
      ],
    ),
  ) is None


def test_phase70_8_final_rejects_wrong_delta_kernel_generator():
  data = build_phase70_8_data()

  wrong_kernel = replace(
    data[
      "delta_kernel_step"
    ].conclusion,
    kernel_group=FreeCyclicGroup(
      generator=Multiple(
        coefficient=4,
        expression=data[
          "iota_11"
        ],
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_kernel,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "hopf_injective_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
      wrong_step,
      data[
        "hopf_value_step"
      ],
    ),
  ) is None


def test_phase70_8_exactness_rejects_wrong_window():
  data = build_phase70_8_data()

  wrong_window = replace(
    data[
      "e_h_window"
    ],
    target_term=TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=11,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "exactness_rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase70_8_final_is_not_given():
  data = build_phase70_8_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase70_8_uses_staged_one_shot_inference():
  data = build_phase70_8_data()

  assert (
    data[
      "e_h_exactness_match"
    ]
    is not None
  )

  assert (
    data[
      "h_delta_exactness_match"
    ]
    is not None
  )

  assert (
    data[
      "hopf_injective_match"
    ]
    is not None
  )

  assert (
    data[
      "delta_kernel_match"
    ]
    is not None
  )

  assert (
    data[
      "hopf_value_match"
    ]
    is not None
  )

  assert (
    data[
      "final_match"
    ]
    is not None
  )


