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
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaSuspensionMap,
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
from test_phase68_delta_eta9 import (
  build_phase68_5_data,
)
from test_phase70_pi9_4_decomposition import (
  build_phase70_4_data,
)
from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaProp42ExactnessStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaSuspensionSurjectiveStatement,
  toda_prop59_delta_eta9_squared_inference_rule,
  toda_prop59_pi10_5_concrete_exactness_inference_rule,
  toda_prop59_pi10_5_hopf_zero_inference_rule,
  toda_prop59_pi10_5_suspension_surjective_inference_rule,
  toda_prop59_pi10_9_delta_injective_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase70_5_data():
  phase70_4 = (
    build_phase70_4_data()
  )

  phase68_5 = (
    build_phase68_5_data()
  )

  pi9_4_step = (
    phase70_4[
      "final_step"
    ]
  )

  delta_eta9_step = (
    phase68_5[
      "final_step"
    ]
  )

  pi8_4_step = (
    phase68_5[
      "pi8_4_step"
    ]
  )

  prop51_step = (
    phase68_5[
      "phase68_4"
    ][
      "prop51_step"
    ]
  )

  delta_eta9_squared_rule = (
    toda_prop59_delta_eta9_squared_inference_rule()
  )

  delta_injective_rule = (
    toda_prop59_pi10_9_delta_injective_inference_rule()
  )

  exactness_rule = (
    toda_prop59_pi10_5_concrete_exactness_inference_rule()
  )

  hopf_zero_rule = (
    toda_prop59_pi10_5_hopf_zero_inference_rule()
  )

  suspension_surjective_rule = (
    toda_prop59_pi10_5_suspension_surjective_inference_rule()
  )

  delta_eta9_squared_match = (
    find_inference_match(
      delta_eta9_squared_rule,
      (
        delta_eta9_step,
        pi9_4_step,
      ),
    )
  )

  assert (
    delta_eta9_squared_match
    is not None
  )

  delta_eta9_squared_step = (
    apply_inference_match(
      delta_eta9_squared_match
    )
  )

  delta_injective_match = (
    find_inference_match(
      delta_injective_rule,
      (
        delta_eta9_step,
        pi8_4_step,
        prop51_step,
      ),
    )
  )

  assert (
    delta_injective_match
    is not None
  )

  delta_injective_step = (
    apply_inference_match(
      delta_injective_match
    )
  )

  pi9_4 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=4,
  )

  pi10_5 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  pi10_9 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=9,
  )

  pi8_4 = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=4,
  )

  e_h_window = TodaEHPExactnessWindow(
    source_term=pi9_4,
    middle_term=pi10_5,
    target_term=pi10_9,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )

  e_h_window_step = ProofStep(
    conclusion=e_h_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  h_delta_window = TodaEHPExactnessWindow(
    source_term=pi10_5,
    middle_term=pi10_9,
    target_term=pi8_4,
    first_map=EHP_H_MAP,
    second_map=EHP_DELTA_MAP,
  )

  h_delta_window_step = ProofStep(
    conclusion=h_delta_window,
    premises=(),
    rule=ProofRule.GIVEN,
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

  hopf_zero_match = (
    find_inference_match(
      hopf_zero_rule,
      (
        delta_injective_step,
        h_delta_exactness_step,
      ),
    )
  )

  assert (
    hopf_zero_match
    is not None
  )

  hopf_zero_step = (
    apply_inference_match(
      hopf_zero_match
    )
  )

  suspension_surjective_match = (
    find_inference_match(
      suspension_surjective_rule,
      (
        hopf_zero_step,
        e_h_exactness_step,
      ),
    )
  )

  assert (
    suspension_surjective_match
    is not None
  )

  suspension_surjective_step = (
    apply_inference_match(
      suspension_surjective_match
    )
  )

  eta_9 = (
    delta_eta9_step
    .conclusion
    .lhs
    .expression
  )

  eta_10 = HomotopyElement(
    name="η₁₀",
    dimension=10,
    source=11,
    target=10,
    generator=GeneratorSymbol(
      family="η",
      index=10,
    ),
  )

  eta9_squared = Composition(
    left=eta_9,
    right=eta_10,
  )

  pi9_4_group = (
    pi9_4_step
    .conclusion
    .rhs
  )

  second_summand = (
    pi9_4_group
    .summands[
      1
    ]
  )

  e_nu_prime_eta7_squared = (
    second_summand.generator
  )

  expected_delta_eta9_squared = (
    Relation(
      lhs=MapApplication(
        map=EHP_DELTA_MAP,
        expression=eta9_squared,
      ),
      rhs=e_nu_prime_eta7_squared,
      relation_type=RelationType.EQUALITY,
    )
  )

  expected_delta_injective = (
    TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=pi10_9,
        target_group=pi8_4,
      ),
    )
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

  expected_hopf_zero = (
    TodaHopfInvariantZeroStatement(
      map=TodaHopfInvariantMap(
        source_group=pi10_5,
        target_group=pi10_9,
      ),
    )
  )

  expected_suspension_surjective = (
    TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=pi9_4,
        target_group=pi10_5,
      ),
    )
  )

  assert (
    delta_eta9_squared_step.conclusion
    == expected_delta_eta9_squared
  )

  assert (
    delta_injective_step.conclusion
    == expected_delta_injective
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
    hopf_zero_step.conclusion
    == expected_hopf_zero
  )

  assert (
    suspension_surjective_step.conclusion
    == expected_suspension_surjective
  )

  return {
    "phase70_4": phase70_4,
    "phase68_5": phase68_5,
    "pi9_4_step": pi9_4_step,
    "delta_eta9_step": (
      delta_eta9_step
    ),
    "pi8_4_step": pi8_4_step,
    "prop51_step": prop51_step,
    "delta_eta9_squared_rule": (
      delta_eta9_squared_rule
    ),
    "delta_injective_rule": (
      delta_injective_rule
    ),
    "exactness_rule": exactness_rule,
    "hopf_zero_rule": hopf_zero_rule,
    "suspension_surjective_rule": (
      suspension_surjective_rule
    ),
    "delta_eta9_squared_match": (
      delta_eta9_squared_match
    ),
    "delta_eta9_squared_step": (
      delta_eta9_squared_step
    ),
    "delta_injective_match": (
      delta_injective_match
    ),
    "delta_injective_step": (
      delta_injective_step
    ),
    "pi9_4": pi9_4,
    "pi10_5": pi10_5,
    "pi10_9": pi10_9,
    "pi8_4": pi8_4,
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
    "hopf_zero_match": (
      hopf_zero_match
    ),
    "hopf_zero_step": hopf_zero_step,
    "suspension_surjective_match": (
      suspension_surjective_match
    ),
    "suspension_surjective_step": (
      suspension_surjective_step
    ),
    "eta_9": eta_9,
    "eta_10": eta_10,
    "eta9_squared": eta9_squared,
    "pi9_4_group": pi9_4_group,
    "second_summand": second_summand,
    "e_nu_prime_eta7_squared": (
      e_nu_prime_eta7_squared
    ),
    "expected_delta_eta9_squared": (
      expected_delta_eta9_squared
    ),
    "expected_delta_injective": (
      expected_delta_injective
    ),
    "expected_e_h_exactness": (
      expected_e_h_exactness
    ),
    "expected_h_delta_exactness": (
      expected_h_delta_exactness
    ),
    "expected_hopf_zero": (
      expected_hopf_zero
    ),
    "expected_suspension_surjective": (
      expected_suspension_surjective
    ),
  }


def test_phase70_5_reuses_phase68_delta_eta9():
  data = build_phase70_5_data()

  assert (
    data[
      "delta_eta9_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_5_reuses_phase70_4_pi9_4():
  data = build_phase70_5_data()

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


def test_phase70_5_pi9_4_is_two_order_two_summands():
  data = build_phase70_5_data()

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


def test_phase70_5_delta_eta9_squared_matches():
  data = build_phase70_5_data()

  assert (
    data[
      "delta_eta9_squared_match"
    ]
    is not None
  )


def test_phase70_5_derives_delta_eta9_squared():
  data = build_phase70_5_data()

  assert (
    data[
      "delta_eta9_squared_step"
    ].conclusion
    == data[
      "expected_delta_eta9_squared"
    ]
  )

  assert (
    data[
      "delta_eta9_squared_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_5_delta_eta9_squared_value_is_second_summand():
  data = build_phase70_5_data()

  assert (
    data[
      "delta_eta9_squared_step"
    ].conclusion.rhs
    is data[
      "second_summand"
    ].generator
  )


def test_phase70_5_delta_eta9_squared_has_expected_argument():
  data = build_phase70_5_data()

  assert (
    data[
      "delta_eta9_squared_step"
    ].conclusion.lhs
    == MapApplication(
      map=EHP_DELTA_MAP,
      expression=data[
        "eta9_squared"
      ],
    )
  )


def test_phase70_5_delta_eta9_squared_uses_exact_two_dependencies():
  data = build_phase70_5_data()

  assert (
    data[
      "delta_eta9_squared_step"
    ].premises
    == (
      data[
        "delta_eta9_step"
      ],
      data[
        "pi9_4_step"
      ],
    )
  )


def test_phase70_5_reuses_derived_prop51():
  data = build_phase70_5_data()

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


def test_phase70_5_delta_injective_matches():
  data = build_phase70_5_data()

  assert (
    data[
      "delta_injective_match"
    ]
    is not None
  )


def test_phase70_5_derives_delta_injective():
  data = build_phase70_5_data()

  assert (
    data[
      "delta_injective_step"
    ].conclusion
    == data[
      "expected_delta_injective"
    ]
  )

  assert (
    data[
      "delta_injective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_5_delta_injective_uses_exact_dependencies():
  data = build_phase70_5_data()

  assert (
    data[
      "delta_injective_step"
    ].premises
    == (
      data[
        "delta_eta9_step"
      ],
      data[
        "pi8_4_step"
      ],
      data[
        "prop51_step"
      ],
    )
  )


def test_phase70_5_structural_windows_remain_given():
  data = build_phase70_5_data()

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


def test_phase70_5_derives_e_h_exactness():
  data = build_phase70_5_data()

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


def test_phase70_5_derives_h_delta_exactness():
  data = build_phase70_5_data()

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


def test_phase70_5_hopf_zero_matches():
  data = build_phase70_5_data()

  assert (
    data[
      "hopf_zero_match"
    ]
    is not None
  )


def test_phase70_5_derives_hopf_zero():
  data = build_phase70_5_data()

  assert (
    data[
      "hopf_zero_step"
    ].conclusion
    == data[
      "expected_hopf_zero"
    ]
  )

  assert (
    data[
      "hopf_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_5_hopf_zero_uses_exact_dependencies():
  data = build_phase70_5_data()

  assert (
    data[
      "hopf_zero_step"
    ].premises
    == (
      data[
        "delta_injective_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
    )
  )


def test_phase70_5_suspension_surjective_matches():
  data = build_phase70_5_data()

  assert (
    data[
      "suspension_surjective_match"
    ]
    is not None
  )


def test_phase70_5_derives_suspension_surjective():
  data = build_phase70_5_data()

  assert (
    data[
      "suspension_surjective_step"
    ].conclusion
    == data[
      "expected_suspension_surjective"
    ]
  )

  assert (
    data[
      "suspension_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_5_suspension_surjective_map_is_expected():
  data = build_phase70_5_data()

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


def test_phase70_5_surjectivity_uses_exact_dependencies():
  data = build_phase70_5_data()

  assert (
    data[
      "suspension_surjective_step"
    ].premises
    == (
      data[
        "hopf_zero_step"
      ],
      data[
        "e_h_exactness_step"
      ],
    )
  )


def test_phase70_5_delta_eta9_squared_rejects_given_delta_eta9():
  data = build_phase70_5_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_eta9_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "delta_eta9_squared_rule"
    ],
    (
      given,
      data[
        "pi9_4_step"
      ],
    ),
  ) is None


def test_phase70_5_delta_eta9_squared_rejects_given_pi9_4():
  data = build_phase70_5_data()

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
      "delta_eta9_squared_rule"
    ],
    (
      data[
        "delta_eta9_step"
      ],
      given,
    ),
  ) is None


def test_phase70_5_delta_injective_rejects_given_delta_eta9():
  data = build_phase70_5_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_eta9_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "delta_injective_rule"
    ],
    (
      given,
      data[
        "pi8_4_step"
      ],
      data[
        "prop51_step"
      ],
    ),
  ) is None


def test_phase70_5_hopf_zero_rejects_given_delta_injective():
  data = build_phase70_5_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_injective_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "hopf_zero_rule"
    ],
    (
      given,
      data[
        "h_delta_exactness_step"
      ],
    ),
  ) is None


def test_phase70_5_surjectivity_rejects_given_hopf_zero():
  data = build_phase70_5_data()

  given = ProofStep(
    conclusion=(
      data[
        "hopf_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "suspension_surjective_rule"
    ],
    (
      given,
      data[
        "e_h_exactness_step"
      ],
    ),
  ) is None


def test_phase70_5_exactness_rejects_wrong_window():
  data = build_phase70_5_data()

  wrong_window = replace(
    data[
      "e_h_window"
    ],
    target_term=TodaPrimaryGroup(
      group_dimension=11,
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


def test_phase70_5_final_results_are_not_given():
  data = build_phase70_5_data()

  assert (
    data[
      "delta_eta9_squared_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "suspension_surjective_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase70_5_uses_staged_one_shot_inference():
  data = build_phase70_5_data()

  assert (
    data[
      "delta_eta9_squared_match"
    ]
    is not None
  )

  assert (
    data[
      "delta_injective_match"
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
      "h_delta_exactness_match"
    ]
    is not None
  )

  assert (
    data[
      "hopf_zero_match"
    ]
    is not None
  )

  assert (
    data[
      "suspension_surjective_match"
    ]
    is not None
  )


