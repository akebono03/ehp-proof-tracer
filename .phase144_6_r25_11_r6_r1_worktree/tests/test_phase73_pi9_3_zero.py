from dataclasses import replace
from functools import lru_cache

from homotopy_groups import (
  FiniteCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
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
  apply_inference_match,
  find_inference_match,
)
from test_phase67_lemma57_nu_prime_specialization import (
  build_phase67_5_data,
)
from test_phase68_prop58_integration import (
  build_phase68_11_data,
)
from test_phase70_prop59_integration import (
  build_phase70_10_data,
)
from test_phase73_pi8_2_eta2_nu_prime_eta6_squared import (
  build_phase73_3_data,
)
from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaDeltaSurjectiveStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionZeroStatement,
  toda_prop511_pi7_2_suspension_zero_inference_rule,
  toda_prop511_pi8_2_suspension_zero_inference_rule,
  toda_prop511_pi9_3_concrete_exactness_inference_rule,
  toda_prop511_pi9_3_zero_inference_rule,
  toda_prop511_pi9_5_to_pi7_2_delta_injective_inference_rule,
  toda_prop511_zero_suspension_left_implies_hopf_injective_inference_rule,
  toda_prop511_zero_suspension_right_implies_delta_surjective_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase73_4_data():
  phase67_5 = (
    build_phase67_5_data()
  )

  phase68_11 = (
    build_phase68_11_data()
  )

  phase70_10 = (
    build_phase70_10_data()
  )

  phase73_3 = (
    build_phase73_3_data()
  )

  eta2_nu_prime_zero_step = (
    phase67_5[
      "final_step"
    ]
  )

  prop58_step = (
    phase68_11[
      "integration_step"
    ]
  )

  prop59_step = (
    phase70_10[
      "integration_step"
    ]
  )

  pi8_2_step = (
    phase73_3[
      "final_step"
    ]
  )

  pi8_zero_rule = (
    toda_prop511_pi8_2_suspension_zero_inference_rule()
  )

  pi8_zero_match = (
    find_inference_match(
      pi8_zero_rule,
      (
        pi8_2_step,
        eta2_nu_prime_zero_step,
      ),
    )
  )

  assert (
    pi8_zero_match
    is not None
  )

  pi8_zero_step = (
    apply_inference_match(
      pi8_zero_match
    )
  )

  pi7_zero_rule = (
    toda_prop511_pi7_2_suspension_zero_inference_rule()
  )

  pi7_zero_match = (
    find_inference_match(
      pi7_zero_rule,
      (
        prop59_step,
        eta2_nu_prime_zero_step,
      ),
    )
  )

  assert (
    pi7_zero_match
    is not None
  )

  pi7_zero_step = (
    apply_inference_match(
      pi7_zero_match
    )
  )

  pi8_2 = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=2,
  )

  pi9_3 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=3,
  )

  pi9_5 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  pi7_2 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=2,
  )

  pi8_3 = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=3,
  )

  e_h_window = TodaEHPExactnessWindow(
    source_term=pi8_2,
    middle_term=pi9_3,
    target_term=pi9_5,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )

  h_delta_window = (
    TodaEHPExactnessWindow(
      source_term=pi9_3,
      middle_term=pi9_5,
      target_term=pi7_2,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    )
  )

  delta_e_window = (
    TodaEHPExactnessWindow(
      source_term=pi9_5,
      middle_term=pi7_2,
      target_term=pi8_3,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    )
  )

  e_h_window_step = ProofStep(
    conclusion=e_h_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  h_delta_window_step = ProofStep(
    conclusion=h_delta_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  delta_e_window_step = ProofStep(
    conclusion=delta_e_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  exactness_rule = (
    toda_prop511_pi9_3_concrete_exactness_inference_rule()
  )

  e_h_match = find_inference_match(
    exactness_rule,
    (
      e_h_window_step,
    ),
  )

  h_delta_match = find_inference_match(
    exactness_rule,
    (
      h_delta_window_step,
    ),
  )

  delta_e_match = find_inference_match(
    exactness_rule,
    (
      delta_e_window_step,
    ),
  )

  assert e_h_match is not None
  assert h_delta_match is not None
  assert delta_e_match is not None

  e_h_exactness_step = (
    apply_inference_match(
      e_h_match
    )
  )

  h_delta_exactness_step = (
    apply_inference_match(
      h_delta_match
    )
  )

  delta_e_exactness_step = (
    apply_inference_match(
      delta_e_match
    )
  )

  hopf_injective_rule = (
    toda_prop511_zero_suspension_left_implies_hopf_injective_inference_rule()
  )

  hopf_injective_match = (
    find_inference_match(
      hopf_injective_rule,
      (
        pi8_zero_step,
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

  delta_surjective_rule = (
    toda_prop511_zero_suspension_right_implies_delta_surjective_inference_rule()
  )

  delta_surjective_match = (
    find_inference_match(
      delta_surjective_rule,
      (
        pi7_zero_step,
        delta_e_exactness_step,
      ),
    )
  )

  assert (
    delta_surjective_match
    is not None
  )

  delta_surjective_step = (
    apply_inference_match(
      delta_surjective_match
    )
  )

  delta_injective_rule = (
    toda_prop511_pi9_5_to_pi7_2_delta_injective_inference_rule()
  )

  delta_injective_match = (
    find_inference_match(
      delta_injective_rule,
      (
        delta_surjective_step,
        prop58_step,
        prop59_step,
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

  final_rule = (
    toda_prop511_pi9_3_zero_inference_rule()
  )

  final_match = find_inference_match(
    final_rule,
    (
      hopf_injective_step,
      delta_injective_step,
      h_delta_exactness_step,
    ),
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

  return {
    "phase67_5": phase67_5,
    "phase68_11": phase68_11,
    "phase70_10": phase70_10,
    "phase73_3": phase73_3,
    "eta2_nu_prime_zero_step": (
      eta2_nu_prime_zero_step
    ),
    "prop58_step": prop58_step,
    "prop59_step": prop59_step,
    "pi8_2_step": pi8_2_step,
    "pi8_zero_rule": pi8_zero_rule,
    "pi8_zero_step": pi8_zero_step,
    "pi7_zero_rule": pi7_zero_rule,
    "pi7_zero_step": pi7_zero_step,
    "pi8_2": pi8_2,
    "pi9_3": pi9_3,
    "pi9_5": pi9_5,
    "pi7_2": pi7_2,
    "pi8_3": pi8_3,
    "e_h_window": e_h_window,
    "h_delta_window": (
      h_delta_window
    ),
    "delta_e_window": (
      delta_e_window
    ),
    "e_h_window_step": (
      e_h_window_step
    ),
    "h_delta_window_step": (
      h_delta_window_step
    ),
    "delta_e_window_step": (
      delta_e_window_step
    ),
    "exactness_rule": exactness_rule,
    "e_h_exactness_step": (
      e_h_exactness_step
    ),
    "h_delta_exactness_step": (
      h_delta_exactness_step
    ),
    "delta_e_exactness_step": (
      delta_e_exactness_step
    ),
    "hopf_injective_rule": (
      hopf_injective_rule
    ),
    "hopf_injective_step": (
      hopf_injective_step
    ),
    "delta_surjective_rule": (
      delta_surjective_rule
    ),
    "delta_surjective_step": (
      delta_surjective_step
    ),
    "delta_injective_rule": (
      delta_injective_rule
    ),
    "delta_injective_step": (
      delta_injective_step
    ),
    "final_rule": final_rule,
    "final_step": final_step,
  }


def test_phase73_4_reuses_derived_dependencies():
  data = build_phase73_4_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in (
      data[
        "eta2_nu_prime_zero_step"
      ],
      data[
        "prop58_step"
      ],
      data[
        "prop59_step"
      ],
      data[
        "pi8_2_step"
      ],
    )
  )


def test_phase73_4_derives_e_pi8_2_zero():
  data = build_phase73_4_data()

  assert (
    data[
      "pi8_zero_step"
    ].conclusion
    == TodaSuspensionZeroStatement(
      map=TodaSuspensionMap(
        source_group=data[
          "pi8_2"
        ],
        target_group=data[
          "pi9_3"
        ],
      )
    )
  )

  assert (
    data[
      "pi8_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_4_e_pi8_2_zero_uses_exact_dependencies():
  data = build_phase73_4_data()

  assert (
    data[
      "pi8_zero_step"
    ].premises
    == (
      data[
        "pi8_2_step"
      ],
      data[
        "eta2_nu_prime_zero_step"
      ],
    )
  )


def test_phase73_4_derives_e_pi7_2_zero():
  data = build_phase73_4_data()

  assert (
    data[
      "pi7_zero_step"
    ].conclusion
    == TodaSuspensionZeroStatement(
      map=TodaSuspensionMap(
        source_group=data[
          "pi7_2"
        ],
        target_group=data[
          "pi8_3"
        ],
      )
    )
  )

  assert (
    data[
      "pi7_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_4_derives_three_exactness_segments():
  data = build_phase73_4_data()

  assert (
    data[
      "e_h_exactness_step"
    ].conclusion
    == TodaProp42ExactnessStatement(
      window=data[
        "e_h_window"
      ],
    )
  )

  assert (
    data[
      "h_delta_exactness_step"
    ].conclusion
    == TodaProp42ExactnessStatement(
      window=data[
        "h_delta_window"
      ],
    )
  )

  assert (
    data[
      "delta_e_exactness_step"
    ].conclusion
    == TodaProp42ExactnessStatement(
      window=data[
        "delta_e_window"
      ],
    )
  )


def test_phase73_4_exactness_windows_remain_foundational_given():
  data = build_phase73_4_data()

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in (
      data[
        "e_h_window_step"
      ],
      data[
        "h_delta_window_step"
      ],
      data[
        "delta_e_window_step"
      ],
    )
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in (
      data[
        "e_h_exactness_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
    )
  )


def test_phase73_4_derives_hopf_injective():
  data = build_phase73_4_data()

  assert (
    data[
      "hopf_injective_step"
    ].conclusion
    == TodaHopfInvariantInjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=data[
          "pi9_3"
        ],
        target_group=data[
          "pi9_5"
        ],
      )
    )
  )


def test_phase73_4_hopf_injective_uses_zero_e_and_exactness():
  data = build_phase73_4_data()

  assert (
    data[
      "hopf_injective_step"
    ].premises
    == (
      data[
        "pi8_zero_step"
      ],
      data[
        "e_h_exactness_step"
      ],
    )
  )


def test_phase73_4_derives_delta_surjective():
  data = build_phase73_4_data()

  assert (
    data[
      "delta_surjective_step"
    ].conclusion
    == TodaDeltaSurjectiveStatement(
      map=TodaDeltaMap(
        source_group=data[
          "pi9_5"
        ],
        target_group=data[
          "pi7_2"
        ],
      )
    )
  )


def test_phase73_4_source_and_target_are_order_two():
  data = build_phase73_4_data()

  source_relation = (
    data[
      "prop58_step"
    ].conclusion
    .pi9_5_group_relation
  )

  target_relation = (
    data[
      "prop59_step"
    ].conclusion
    .pi7_2_group_relation
  )

  assert isinstance(
    source_relation.rhs,
    FiniteCyclicGroup,
  )

  assert isinstance(
    target_relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    source_relation.rhs.order
    == 2
  )

  assert (
    target_relation.rhs.order
    == 2
  )


def test_phase73_4_derives_delta_injective():
  data = build_phase73_4_data()

  assert (
    data[
      "delta_injective_step"
    ].conclusion
    == TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=data[
          "pi9_5"
        ],
        target_group=data[
          "pi7_2"
        ],
      )
    )
  )

  assert (
    data[
      "delta_injective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_4_delta_injective_uses_exact_three_dependencies():
  data = build_phase73_4_data()

  assert (
    data[
      "delta_injective_step"
    ].premises
    == (
      data[
        "delta_surjective_step"
      ],
      data[
        "prop58_step"
      ],
      data[
        "prop59_step"
      ],
    )
  )


def test_phase73_4_derives_pi9_3_zero():
  data = build_phase73_4_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == TodaPrimaryGroupZeroStatement(
      group=data[
        "pi9_3"
      ],
    )
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_4_final_uses_exact_three_dependencies():
  data = build_phase73_4_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "hopf_injective_step"
      ],
      data[
        "delta_injective_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
    )
  )


def test_phase73_4_rejects_given_pi8_2_result():
  data = build_phase73_4_data()

  given_pi8_2 = ProofStep(
    conclusion=(
      data[
        "pi8_2_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "pi8_zero_rule"
    ],
    (
      given_pi8_2,
      data[
        "eta2_nu_prime_zero_step"
      ],
    ),
  ) is None


def test_phase73_4_rejects_wrong_exactness_window():
  data = build_phase73_4_data()

  wrong_window = replace(
    data[
      "e_h_window"
    ],
    target_term=TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=5,
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


def test_phase73_4_rejects_given_hopf_injective():
  data = build_phase73_4_data()

  given_hopf = ProofStep(
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
      given_hopf,
      data[
        "delta_injective_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
    ),
  ) is None


def test_phase73_4_rejects_wrong_delta_map():
  data = build_phase73_4_data()

  wrong_delta = ProofStep(
    conclusion=TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=data[
          "pi9_5"
        ],
        target_group=TodaPrimaryGroup(
          group_dimension=8,
          sphere_dimension=2,
        ),
      )
    ),
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
      wrong_delta,
      data[
        "h_delta_exactness_step"
      ],
    ),
  ) is None


def test_phase73_4_final_is_not_given():
  data = build_phase73_4_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


