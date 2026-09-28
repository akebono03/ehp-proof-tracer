from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from test_phase59_prop53_integration import (
  build_phase59_8_data,
)
from test_phase68_pi9_5_nu5_eta8 import (
  build_phase68_6_data,
)
from test_phase70_delta_eta9_squared_surjectivity import (
  build_phase70_5_data,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
  TodaProp53FiniteDimensionalStatement,
  TodaSuspensionSurjectiveStatement,
  toda_prop59_e_nu4_eta7_squared_bridge_inference_rule,
  toda_prop59_pi10_5_delta_e_exactness_inference_rule,
  toda_prop59_pi10_5_finite_cyclic_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase70_6_data():
  phase70_5 = (
    build_phase70_5_data()
  )

  phase68_6 = (
    build_phase68_6_data()
  )

  phase59_8 = (
    build_phase59_8_data()
  )

  phase70_4 = (
    phase70_5[
      "phase70_4"
    ]
  )

  pi9_4_step = (
    phase70_4[
      "final_step"
    ]
  )

  delta_eta9_squared_step = (
    phase70_5[
      "delta_eta9_squared_step"
    ]
  )

  suspension_surjective_step = (
    phase70_5[
      "suspension_surjective_step"
    ]
  )

  phase68_bridge_step = (
    phase68_6[
      "generator_bridge_step"
    ]
  )

  prop53_step = (
    phase59_8[
      "integration_step"
    ]
  )

  pi11_9 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=9,
  )

  pi9_4 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=4,
  )

  pi10_5 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  delta_e_window = (
    TodaEHPExactnessWindow(
      source_term=pi11_9,
      middle_term=pi9_4,
      target_term=pi10_5,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    )
  )

  delta_e_window_step = ProofStep(
    conclusion=delta_e_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  exactness_rule = (
    toda_prop59_pi10_5_delta_e_exactness_inference_rule()
  )

  generator_bridge_rule = (
    toda_prop59_e_nu4_eta7_squared_bridge_inference_rule()
  )

  final_rule = (
    toda_prop59_pi10_5_finite_cyclic_inference_rule()
  )

  exactness_match = find_inference_match(
    exactness_rule,
    (
      delta_e_window_step,
    ),
  )

  assert exactness_match is not None

  delta_e_exactness_step = (
    apply_inference_match(
      exactness_match
    )
  )

  generator_bridge_match = (
    find_inference_match(
      generator_bridge_rule,
      (
        pi9_4_step,
        phase68_bridge_step,
      ),
    )
  )

  assert (
    generator_bridge_match
    is not None
  )

  generator_bridge_step = (
    apply_inference_match(
      generator_bridge_match
    )
  )

  final_match = find_inference_match(
    final_rule,
    (
      pi9_4_step,
      delta_eta9_squared_step,
      prop53_step,
      delta_e_exactness_step,
      suspension_surjective_step,
      generator_bridge_step,
    ),
  )

  assert final_match is not None

  final_step = (
    apply_inference_match(
      final_match
    )
  )

  pi9_4_group = (
    pi9_4_step
    .conclusion
    .rhs
  )

  first_summand = (
    pi9_4_group
    .summands[
      0
    ]
  )

  second_summand = (
    pi9_4_group
    .summands[
      1
    ]
  )

  nu4_eta7_squared = (
    first_summand.generator
  )

  nu_4 = (
    nu4_eta7_squared.left
  )

  eta7_squared = (
    nu4_eta7_squared.right
  )

  eta_7 = (
    eta7_squared.left
  )

  eta_8 = (
    eta7_squared.right
  )

  nu5_eta8 = (
    phase68_bridge_step
    .conclusion
    .rhs
  )

  nu_5 = (
    nu5_eta8.left
  )

  bridge_eta_8 = (
    nu5_eta8.right
  )

  eta_9 = HomotopyElement(
    name="η₉",
    dimension=9,
    source=10,
    target=9,
    generator=GeneratorSymbol(
      family="η",
      index=9,
    ),
  )

  eta8_squared = Composition(
    left=bridge_eta_8,
    right=eta_9,
  )

  nu5_eta8_squared = Composition(
    left=nu_5,
    right=eta8_squared,
  )

  expected_bridge = Relation(
    lhs=Suspension(
      expression=nu4_eta7_squared,
    ),
    rhs=nu5_eta8_squared,
    relation_type=RelationType.EQUALITY,
  )

  expected_exactness = (
    TodaProp42ExactnessStatement(
      window=delta_e_window,
    )
  )

  expected_final = Relation(
    lhs=pi10_5,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=nu5_eta8_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    delta_e_exactness_step.conclusion
    == expected_exactness
  )

  assert (
    generator_bridge_step.conclusion
    == expected_bridge
  )

  assert (
    final_step.conclusion
    == expected_final
  )

  return {
    "phase70_5": phase70_5,
    "phase70_4": phase70_4,
    "phase68_6": phase68_6,
    "phase59_8": phase59_8,
    "pi9_4_step": pi9_4_step,
    "delta_eta9_squared_step": (
      delta_eta9_squared_step
    ),
    "suspension_surjective_step": (
      suspension_surjective_step
    ),
    "phase68_bridge_step": (
      phase68_bridge_step
    ),
    "prop53_step": prop53_step,
    "pi11_9": pi11_9,
    "pi9_4": pi9_4,
    "pi10_5": pi10_5,
    "delta_e_window": (
      delta_e_window
    ),
    "delta_e_window_step": (
      delta_e_window_step
    ),
    "exactness_rule": exactness_rule,
    "generator_bridge_rule": (
      generator_bridge_rule
    ),
    "final_rule": final_rule,
    "exactness_match": (
      exactness_match
    ),
    "delta_e_exactness_step": (
      delta_e_exactness_step
    ),
    "generator_bridge_match": (
      generator_bridge_match
    ),
    "generator_bridge_step": (
      generator_bridge_step
    ),
    "final_match": final_match,
    "final_step": final_step,
    "pi9_4_group": pi9_4_group,
    "first_summand": first_summand,
    "second_summand": second_summand,
    "nu4_eta7_squared": (
      nu4_eta7_squared
    ),
    "nu_4": nu_4,
    "eta7_squared": eta7_squared,
    "eta_7": eta_7,
    "eta_8": eta_8,
    "nu5_eta8": nu5_eta8,
    "nu_5": nu_5,
    "bridge_eta_8": bridge_eta_8,
    "eta_9": eta_9,
    "eta8_squared": eta8_squared,
    "nu5_eta8_squared": (
      nu5_eta8_squared
    ),
    "expected_bridge": expected_bridge,
    "expected_exactness": (
      expected_exactness
    ),
    "expected_final": expected_final,
  }


def test_phase70_6_reuses_phase70_4_pi9_4():
  data = build_phase70_6_data()

  assert (
    data[
      "pi9_4_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi9_4_step"
    ].conclusion.lhs
    == data[
      "pi9_4"
    ]
  )


def test_phase70_6_pi9_4_is_two_order_two_summands():
  data = build_phase70_6_data()

  group = (
    data[
      "pi9_4_group"
    ]
  )

  assert isinstance(
    group,
    DirectSumGroup,
  )

  assert (
    len(
      group.summands
    )
    == 2
  )

  assert all(
    isinstance(
      summand,
      FiniteCyclicGroup,
    )
    and summand.order
    == 2
    for summand
    in group.summands
  )


def test_phase70_6_reuses_delta_eta9_squared():
  data = build_phase70_6_data()

  assert (
    data[
      "delta_eta9_squared_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "delta_eta9_squared_step"
    ].conclusion.rhs
    is data[
      "second_summand"
    ].generator
  )


def test_phase70_6_reuses_suspension_surjectivity():
  data = build_phase70_6_data()

  assert isinstance(
    data[
      "suspension_surjective_step"
    ].conclusion,
    TodaSuspensionSurjectiveStatement,
  )

  assert (
    data[
      "suspension_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "suspension_surjective_step"
    ].conclusion.map
    == TodaSuspensionMap(
      source_group=data[
        "pi9_4"
      ],
      target_group=data[
        "pi10_5"
      ],
    )
  )


def test_phase70_6_reuses_derived_prop53():
  data = build_phase70_6_data()

  assert isinstance(
    data[
      "prop53_step"
    ].conclusion,
    TodaProp53FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop53_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_6_structural_delta_e_window_remains_given():
  data = build_phase70_6_data()

  assert (
    data[
      "delta_e_window_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase70_6_derives_delta_e_exactness():
  data = build_phase70_6_data()

  assert (
    data[
      "delta_e_exactness_step"
    ].conclusion
    == data[
      "expected_exactness"
    ]
  )

  assert (
    data[
      "delta_e_exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_6_exactness_has_expected_window():
  data = build_phase70_6_data()

  assert (
    data[
      "delta_e_exactness_step"
    ].conclusion.window
    == TodaEHPExactnessWindow(
      source_term=data[
        "pi11_9"
      ],
      middle_term=data[
        "pi9_4"
      ],
      target_term=data[
        "pi10_5"
      ],
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    )
  )


def test_phase70_6_reuses_phase68_generator_bridge():
  data = build_phase70_6_data()

  assert (
    data[
      "phase68_bridge_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "phase68_bridge_step"
    ].conclusion.rhs
    == data[
      "nu5_eta8"
    ]
  )


def test_phase70_6_generator_bridge_matches():
  data = build_phase70_6_data()

  assert (
    data[
      "generator_bridge_match"
    ]
    is not None
  )


def test_phase70_6_derives_generator_bridge():
  data = build_phase70_6_data()

  assert (
    data[
      "generator_bridge_step"
    ].conclusion
    == data[
      "expected_bridge"
    ]
  )

  assert (
    data[
      "generator_bridge_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_6_generator_bridge_uses_exact_dependencies():
  data = build_phase70_6_data()

  assert (
    data[
      "generator_bridge_step"
    ].premises
    == (
      data[
        "pi9_4_step"
      ],
      data[
        "phase68_bridge_step"
      ],
    )
  )


def test_phase70_6_eta8_squared_is_right_associated():
  data = build_phase70_6_data()

  assert (
    data[
      "eta8_squared"
    ]
    == Composition(
      left=data[
        "eta_8"
      ],
      right=data[
        "eta_9"
      ],
    )
  )


def test_phase70_6_generator_is_nu5_eta8_squared():
  data = build_phase70_6_data()

  assert (
    data[
      "nu5_eta8_squared"
    ]
    == Composition(
      left=data[
        "nu_5"
      ],
      right=data[
        "eta8_squared"
      ],
    )
  )


def test_phase70_6_final_matches():
  data = build_phase70_6_data()

  assert (
    data[
      "final_match"
    ]
    is not None
  )


def test_phase70_6_derives_pi10_5():
  data = build_phase70_6_data()

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


def test_phase70_6_final_is_pi10_5():
  data = build_phase70_6_data()

  assert (
    data[
      "final_step"
    ].conclusion.lhs
    == data[
      "pi10_5"
    ]
  )


def test_phase70_6_final_is_order_two():
  data = build_phase70_6_data()

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


def test_phase70_6_final_generator_is_nu5_eta8_squared():
  data = build_phase70_6_data()

  assert (
    data[
      "final_step"
    ].conclusion.rhs.generator
    is data[
      "generator_bridge_step"
    ].conclusion.rhs
  )

  assert (
    data[
      "final_step"
    ].conclusion.rhs.generator
    == data[
      "nu5_eta8_squared"
    ]
  )


def test_phase70_6_final_uses_exact_six_dependencies():
  data = build_phase70_6_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi9_4_step"
      ],
      data[
        "delta_eta9_squared_step"
      ],
      data[
        "prop53_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
      data[
        "suspension_surjective_step"
      ],
      data[
        "generator_bridge_step"
      ],
    )
  )


def test_phase70_6_generator_bridge_rejects_given_pi9_4():
  data = build_phase70_6_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi9_4_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "generator_bridge_rule"
    ],
    (
      given,
      data[
        "phase68_bridge_step"
      ],
    ),
  ) is None


def test_phase70_6_generator_bridge_rejects_given_phase68_bridge():
  data = build_phase70_6_data()

  given = ProofStep(
    conclusion=(
      data[
        "phase68_bridge_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "generator_bridge_rule"
    ],
    (
      data[
        "pi9_4_step"
      ],
      given,
    ),
  ) is None


def test_phase70_6_final_rejects_given_delta_eta9_squared():
  data = build_phase70_6_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_eta9_squared_step"
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
        "pi9_4_step"
      ],
      given,
      data[
        "prop53_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
      data[
        "suspension_surjective_step"
      ],
      data[
        "generator_bridge_step"
      ],
    ),
  ) is None


def test_phase70_6_final_rejects_given_surjectivity():
  data = build_phase70_6_data()

  given = ProofStep(
    conclusion=(
      data[
        "suspension_surjective_step"
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
        "pi9_4_step"
      ],
      data[
        "delta_eta9_squared_step"
      ],
      data[
        "prop53_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
      given,
      data[
        "generator_bridge_step"
      ],
    ),
  ) is None


def test_phase70_6_final_rejects_given_prop53():
  data = build_phase70_6_data()

  given = ProofStep(
    conclusion=(
      data[
        "prop53_step"
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
        "pi9_4_step"
      ],
      data[
        "delta_eta9_squared_step"
      ],
      given,
      data[
        "delta_e_exactness_step"
      ],
      data[
        "suspension_surjective_step"
      ],
      data[
        "generator_bridge_step"
      ],
    ),
  ) is None


def test_phase70_6_exactness_rejects_wrong_window():
  data = build_phase70_6_data()

  wrong_window = replace(
    data[
      "delta_e_window"
    ],
    source_term=TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=9,
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


def test_phase70_6_final_is_not_given():
  data = build_phase70_6_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase70_6_uses_staged_one_shot_inference():
  data = build_phase70_6_data()

  assert (
    data[
      "exactness_match"
    ]
    is not None
  )

  assert (
    data[
      "generator_bridge_match"
    ]
    is not None
  )

  assert (
    data[
      "final_match"
    ]
    is not None
  )


