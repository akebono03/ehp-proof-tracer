from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
  Suspension,
  Zero,
)
from homotopy_groups import (
  FiniteCyclicGroup,
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
from test_phase67_lemma57_delta_generator import (
  build_phase67_7_data,
)
from test_phase70_pi7_2_eta2_nu_prime_eta6 import (
  build_phase70_2_data,
)
from toda_rules import (
  Toda55NuFamilyFiniteDimensionalStatement,
  TodaDeltaImageUpToSignStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaProp59DeltaKernelStatement,
  toda_eta_family_definition_statement,
  toda_prop59_concrete_e_h_exactness_inference_rule,
  toda_prop59_concrete_h_delta_exactness_inference_rule,
  toda_prop59_delta_nu5_kernel_inference_rule,
  toda_prop59_nu_prime_eta6_squared_hopf_inference_rule,
  toda_prop59_pi7_2_suspension_zero_inference_rule,
  toda_prop59_pi8_3_finite_cyclic_inference_rule,
  toda_prop59_pi8_3_hopf_injective_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase70_3_data():
  phase70_2 = (
    build_phase70_2_data()
  )

  phase67_7 = (
    build_phase67_7_data()
  )

  pi7_2_step = (
    phase70_2[
      "final_step"
    ]
  )

  phase68_3 = (
    phase70_2[
      "phase68_3"
    ]
  )

  equation57_step = (
    phase68_3[
      "equation57_step"
    ]
  )

  eta2_nu_prime_zero_step = (
    phase67_7[
      "eta2_nu_prime_zero_step"
    ]
  )

  pi6_2_step = (
    phase67_7[
      "pi6_2_step"
    ]
  )

  delta_nu5_step = (
    phase67_7[
      "final_step"
    ]
  )

  phase65_9 = (
    phase67_7[
      "phase65_9"
    ]
  )

  pi8_5_step = (
    phase65_9[
      "pi8_5_step"
    ]
  )

  phase65_7 = (
    phase65_9[
      "phase65_7"
    ]
  )

  toda55_step = (
    phase65_7[
      "toda55_step"
    ]
  )

  eta7_definition = (
    toda_eta_family_definition_statement(
      7
    )
  )

  eta7_definition_step = ProofStep(
    conclusion=eta7_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi7_2 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=2,
  )

  pi8_3 = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=3,
  )

  pi8_5 = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=5,
  )

  pi6_2 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=2,
  )

  e_h_window = TodaEHPExactnessWindow(
    source_term=pi7_2,
    middle_term=pi8_3,
    target_term=pi8_5,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )

  e_h_window_step = ProofStep(
    conclusion=e_h_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  h_delta_window = TodaEHPExactnessWindow(
    source_term=pi8_3,
    middle_term=pi8_5,
    target_term=pi6_2,
    first_map=EHP_H_MAP,
    second_map=EHP_DELTA_MAP,
  )

  h_delta_window_step = ProofStep(
    conclusion=h_delta_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspension_zero_rule = (
    toda_prop59_pi7_2_suspension_zero_inference_rule()
  )

  e_h_exactness_rule = (
    toda_prop59_concrete_e_h_exactness_inference_rule()
  )

  hopf_injective_rule = (
    toda_prop59_pi8_3_hopf_injective_inference_rule()
  )

  h_delta_exactness_rule = (
    toda_prop59_concrete_h_delta_exactness_inference_rule()
  )

  delta_kernel_rule = (
    toda_prop59_delta_nu5_kernel_inference_rule()
  )

  hopf_value_rule = (
    toda_prop59_nu_prime_eta6_squared_hopf_inference_rule()
  )

  group_rule = (
    toda_prop59_pi8_3_finite_cyclic_inference_rule()
  )

  suspension_zero_match = find_inference_match(
    suspension_zero_rule,
    (
      pi7_2_step,
      eta2_nu_prime_zero_step,
    ),
  )

  assert suspension_zero_match is not None

  suspension_zero_step = (
    apply_inference_match(
      suspension_zero_match
    )
  )

  e_h_exactness_match = find_inference_match(
    e_h_exactness_rule,
    (
      e_h_window_step,
    ),
  )

  assert e_h_exactness_match is not None

  e_h_exactness_step = (
    apply_inference_match(
      e_h_exactness_match
    )
  )

  hopf_injective_match = find_inference_match(
    hopf_injective_rule,
    (
      suspension_zero_step,
      pi7_2_step,
      e_h_exactness_step,
    ),
  )

  assert hopf_injective_match is not None

  hopf_injective_step = (
    apply_inference_match(
      hopf_injective_match
    )
  )

  h_delta_exactness_match = find_inference_match(
    h_delta_exactness_rule,
    (
      h_delta_window_step,
    ),
  )

  assert h_delta_exactness_match is not None

  h_delta_exactness_step = (
    apply_inference_match(
      h_delta_exactness_match
    )
  )

  delta_kernel_match = find_inference_match(
    delta_kernel_rule,
    (
      delta_nu5_step,
      pi8_5_step,
      pi6_2_step,
    ),
  )

  assert delta_kernel_match is not None

  delta_kernel_step = (
    apply_inference_match(
      delta_kernel_match
    )
  )

  hopf_value_match = find_inference_match(
    hopf_value_rule,
    (
      equation57_step,
      toda55_step,
      pi8_5_step,
      eta7_definition_step,
    ),
  )

  assert hopf_value_match is not None

  hopf_value_step = (
    apply_inference_match(
      hopf_value_match
    )
  )

  group_match = find_inference_match(
    group_rule,
    (
      hopf_injective_step,
      h_delta_exactness_step,
      delta_kernel_step,
      hopf_value_step,
    ),
  )

  assert group_match is not None

  final_step = (
    apply_inference_match(
      group_match
    )
  )

  pi7_2_generator = (
    pi7_2_step
    .conclusion
    .rhs
    .generator
  )

  expected_suspension_zero = Relation(
    lhs=Suspension(
      expression=pi7_2_generator,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  expected_e_h_exactness = (
    TodaProp42ExactnessStatement(
      window=e_h_window,
    )
  )

  hopf_map = TodaHopfInvariantMap(
    source_group=pi8_3,
    target_group=pi8_5,
  )

  expected_hopf_injective = (
    TodaHopfInvariantInjectiveStatement(
      map=hopf_map,
    )
  )

  expected_h_delta_exactness = (
    TodaProp42ExactnessStatement(
      window=h_delta_window,
    )
  )

  nu_5 = (
    pi8_5_step
    .conclusion
    .rhs
    .generator
  )

  delta_map = TodaDeltaMap(
    source_group=pi8_5,
    target_group=pi6_2,
  )

  expected_delta_kernel = (
    TodaProp59DeltaKernelStatement(
      map=delta_map,
      kernel_group=FiniteCyclicGroup(
        order=2,
        generator=Multiple(
          coefficient=4,
          expression=nu_5,
        ),
      ),
    )
  )

  nu_prime_eta6 = (
    equation57_step
    .conclusion
    .lhs
    .expression
  )

  nu_prime = (
    nu_prime_eta6.left
  )

  eta_6 = (
    nu_prime_eta6.right
  )

  eta_7 = HomotopyElement(
    name="η₇",
    dimension=7,
    source=8,
    target=7,
    generator=GeneratorSymbol(
      family="η",
      index=7,
    ),
  )

  eta6_squared = Composition(
    left=eta_6,
    right=eta_7,
  )

  nu_prime_eta6_squared = (
    Composition(
      left=nu_prime,
      right=eta6_squared,
    )
  )

  expected_hopf_value = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=nu_prime_eta6_squared,
    ),
    rhs=Multiple(
      coefficient=4,
      expression=nu_5,
    ),
    relation_type=RelationType.EQUALITY,
  )

  expected_final = Relation(
    lhs=pi8_3,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=nu_prime_eta6_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    suspension_zero_step.conclusion
    == expected_suspension_zero
  )

  assert (
    e_h_exactness_step.conclusion
    == expected_e_h_exactness
  )

  assert (
    hopf_injective_step.conclusion
    == expected_hopf_injective
  )

  assert (
    h_delta_exactness_step.conclusion
    == expected_h_delta_exactness
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
    "phase70_2": phase70_2,
    "phase67_7": phase67_7,
    "phase68_3": phase68_3,
    "phase65_9": phase65_9,
    "phase65_7": phase65_7,
    "pi7_2_step": pi7_2_step,
    "eta2_nu_prime_zero_step": (
      eta2_nu_prime_zero_step
    ),
    "pi6_2_step": pi6_2_step,
    "delta_nu5_step": delta_nu5_step,
    "pi8_5_step": pi8_5_step,
    "equation57_step": equation57_step,
    "toda55_step": toda55_step,
    "eta7_definition": (
      eta7_definition
    ),
    "eta7_definition_step": (
      eta7_definition_step
    ),
    "pi7_2": pi7_2,
    "pi8_3": pi8_3,
    "pi8_5": pi8_5,
    "pi6_2": pi6_2,
    "e_h_window": e_h_window,
    "e_h_window_step": (
      e_h_window_step
    ),
    "h_delta_window": (
      h_delta_window
    ),
    "h_delta_window_step": (
      h_delta_window_step
    ),
    "suspension_zero_rule": (
      suspension_zero_rule
    ),
    "e_h_exactness_rule": (
      e_h_exactness_rule
    ),
    "hopf_injective_rule": (
      hopf_injective_rule
    ),
    "h_delta_exactness_rule": (
      h_delta_exactness_rule
    ),
    "delta_kernel_rule": (
      delta_kernel_rule
    ),
    "hopf_value_rule": (
      hopf_value_rule
    ),
    "group_rule": group_rule,
    "suspension_zero_match": (
      suspension_zero_match
    ),
    "suspension_zero_step": (
      suspension_zero_step
    ),
    "e_h_exactness_match": (
      e_h_exactness_match
    ),
    "e_h_exactness_step": (
      e_h_exactness_step
    ),
    "hopf_injective_match": (
      hopf_injective_match
    ),
    "hopf_injective_step": (
      hopf_injective_step
    ),
    "h_delta_exactness_match": (
      h_delta_exactness_match
    ),
    "h_delta_exactness_step": (
      h_delta_exactness_step
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
    "group_match": group_match,
    "pi7_2_generator": (
      pi7_2_generator
    ),
    "expected_suspension_zero": (
      expected_suspension_zero
    ),
    "expected_e_h_exactness": (
      expected_e_h_exactness
    ),
    "hopf_map": hopf_map,
    "expected_hopf_injective": (
      expected_hopf_injective
    ),
    "expected_h_delta_exactness": (
      expected_h_delta_exactness
    ),
    "nu_5": nu_5,
    "delta_map": delta_map,
    "expected_delta_kernel": (
      expected_delta_kernel
    ),
    "nu_prime_eta6": (
      nu_prime_eta6
    ),
    "nu_prime": nu_prime,
    "eta_6": eta_6,
    "eta_7": eta_7,
    "eta6_squared": (
      eta6_squared
    ),
    "nu_prime_eta6_squared": (
      nu_prime_eta6_squared
    ),
    "expected_hopf_value": (
      expected_hopf_value
    ),
    "expected_final": expected_final,
    "final_step": final_step,
  }


def test_phase70_3_reuses_phase70_2_pi7_2():
  data = build_phase70_3_data()

  assert (
    data[
      "pi7_2_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi7_2_step"
    ].conclusion.lhs
    == data[
      "pi7_2"
    ]
  )


def test_phase70_3_reuses_phase67_zero():
  data = build_phase70_3_data()

  assert (
    data[
      "eta2_nu_prime_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_3_derives_pi7_2_generator_suspension_zero():
  data = build_phase70_3_data()

  assert (
    data[
      "suspension_zero_step"
    ].conclusion
    == data[
      "expected_suspension_zero"
    ]
  )

  assert (
    data[
      "suspension_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_3_suspension_zero_uses_exact_dependencies():
  data = build_phase70_3_data()

  assert (
    data[
      "suspension_zero_step"
    ].premises
    == (
      data[
        "pi7_2_step"
      ],
      data[
        "eta2_nu_prime_zero_step"
      ],
    )
  )


def test_phase70_3_exactness_windows_remain_given():
  data = build_phase70_3_data()

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


def test_phase70_3_derives_both_exactness_statements():
  data = build_phase70_3_data()

  assert (
    data[
      "e_h_exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "h_delta_exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_3_derives_hopf_injective():
  data = build_phase70_3_data()

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


def test_phase70_3_hopf_injective_uses_exact_dependencies():
  data = build_phase70_3_data()

  assert (
    data[
      "hopf_injective_step"
    ].premises
    == (
      data[
        "suspension_zero_step"
      ],
      data[
        "pi7_2_step"
      ],
      data[
        "e_h_exactness_step"
      ],
    )
  )


def test_phase70_3_reuses_delta_nu5():
  data = build_phase70_3_data()

  assert isinstance(
    data[
      "delta_nu5_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )

  assert (
    data[
      "delta_nu5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_3_reuses_pi8_5_order_eight():
  data = build_phase70_3_data()

  relation = (
    data[
      "pi8_5_step"
    ].conclusion
  )

  assert (
    data[
      "pi8_5_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    relation.lhs
    == data[
      "pi8_5"
    ]
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 8


def test_phase70_3_reuses_pi6_2_order_four():
  data = build_phase70_3_data()

  relation = (
    data[
      "pi6_2_step"
    ].conclusion
  )

  assert (
    data[
      "pi6_2_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    relation.lhs
    == data[
      "pi6_2"
    ]
  )

  assert relation.rhs.order == 4


def test_phase70_3_derives_delta_kernel():
  data = build_phase70_3_data()

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


def test_phase70_3_delta_kernel_is_order_two_four_nu5():
  data = build_phase70_3_data()

  kernel = (
    data[
      "delta_kernel_step"
    ].conclusion
    .kernel_group
  )

  assert kernel.order == 2

  assert (
    kernel.generator
    == Multiple(
      coefficient=4,
      expression=data[
        "nu_5"
      ],
    )
  )


def test_phase70_3_delta_kernel_uses_exact_dependencies():
  data = build_phase70_3_data()

  assert (
    data[
      "delta_kernel_step"
    ].premises
    == (
      data[
        "delta_nu5_step"
      ],
      data[
        "pi8_5_step"
      ],
      data[
        "pi6_2_step"
      ],
    )
  )


def test_phase70_3_reuses_equation57():
  data = build_phase70_3_data()

  assert (
    data[
      "equation57_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_3_reuses_toda55_aggregate():
  data = build_phase70_3_data()

  assert isinstance(
    data[
      "toda55_step"
    ].conclusion,
    Toda55NuFamilyFiniteDimensionalStatement,
  )

  assert (
    data[
      "toda55_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_3_eta7_definition_remains_given():
  data = build_phase70_3_data()

  assert (
    data[
      "eta7_definition_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "eta7_definition"
    ].index
    == 7
  )


def test_phase70_3_derives_hopf_nu_prime_eta6_squared():
  data = build_phase70_3_data()

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


def test_phase70_3_hopf_value_is_four_nu5():
  data = build_phase70_3_data()

  assert (
    data[
      "hopf_value_step"
    ].conclusion.rhs
    == Multiple(
      coefficient=4,
      expression=data[
        "nu_5"
      ],
    )
  )


def test_phase70_3_generator_is_right_associated_nu_prime_eta6_squared():
  data = build_phase70_3_data()

  assert (
    data[
      "nu_prime_eta6_squared"
    ]
    == Composition(
      left=data[
        "nu_prime"
      ],
      right=Composition(
        left=data[
          "eta_6"
        ],
        right=data[
          "eta_7"
        ],
      ),
    )
  )


def test_phase70_3_hopf_value_uses_exact_dependencies():
  data = build_phase70_3_data()

  assert (
    data[
      "hopf_value_step"
    ].premises
    == (
      data[
        "equation57_step"
      ],
      data[
        "toda55_step"
      ],
      data[
        "pi8_5_step"
      ],
      data[
        "eta7_definition_step"
      ],
    )
  )


def test_phase70_3_derives_pi8_3():
  data = build_phase70_3_data()

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


def test_phase70_3_pi8_3_is_order_two():
  data = build_phase70_3_data()

  group = (
    data[
      "final_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert group.order == 2


def test_phase70_3_final_generator_is_nu_prime_eta6_squared():
  data = build_phase70_3_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    is data[
      "hopf_value_step"
    ].conclusion
    .lhs
    .expression
  )

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == data[
      "nu_prime_eta6_squared"
    ]
  )


def test_phase70_3_final_uses_exact_four_dependencies():
  data = build_phase70_3_data()

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


def test_phase70_3_rejects_given_pi7_2():
  data = build_phase70_3_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi7_2_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "suspension_zero_rule"
    ],
    (
      given,
      data[
        "eta2_nu_prime_zero_step"
      ],
    ),
  ) is None


def test_phase70_3_rejects_given_delta_nu5():
  data = build_phase70_3_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_nu5_step"
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
      given,
      data[
        "pi8_5_step"
      ],
      data[
        "pi6_2_step"
      ],
    ),
  ) is None


def test_phase70_3_rejects_wrong_pi8_5_order():
  data = build_phase70_3_data()

  wrong_relation = replace(
    data[
      "pi8_5_step"
    ].conclusion,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=data[
        "nu_5"
      ],
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "delta_kernel_rule"
    ],
    (
      data[
        "delta_nu5_step"
      ],
      wrong_step,
      data[
        "pi6_2_step"
      ],
    ),
  ) is None


def test_phase70_3_rejects_wrong_h_delta_window():
  data = build_phase70_3_data()

  wrong_window = replace(
    data[
      "h_delta_window"
    ],
    target_term=TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=2,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "h_delta_exactness_rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase70_3_rejects_given_hopf_injective():
  data = build_phase70_3_data()

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
      "group_rule"
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


def test_phase70_3_rejects_given_delta_kernel():
  data = build_phase70_3_data()

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
      "group_rule"
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


def test_phase70_3_final_is_not_given():
  data = build_phase70_3_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )

  initial_steps = (
    data[
      "pi7_2_step"
    ],
    data[
      "eta2_nu_prime_zero_step"
    ],
    data[
      "pi6_2_step"
    ],
    data[
      "delta_nu5_step"
    ],
    data[
      "pi8_5_step"
    ],
    data[
      "equation57_step"
    ],
    data[
      "toda55_step"
    ],
    data[
      "eta7_definition_step"
    ],
    data[
      "e_h_window_step"
    ],
    data[
      "h_delta_window_step"
    ],
  )

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step in initial_steps
    )
  )


def test_phase70_3_uses_staged_one_shot_inference():
  data = build_phase70_3_data()

  assert (
    data[
      "suspension_zero_match"
    ]
    is not None
  )

  assert (
    data[
      "e_h_exactness_match"
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
      "h_delta_exactness_match"
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
      "group_match"
    ]
    is not None
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


