from dataclasses import replace
from functools import lru_cache

from homotopy_groups import (
  FiniteCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase70_prop59_integration import (
  build_phase70_10_data,
)
from test_phase73_prop511_finite_dimensional_integration import (
  build_phase73_8e_data,
)
from test_phase75_pi9_2_zero import (
  build_phase75_2_data,
)
from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaDeltaSurjectiveStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaProp59FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  toda_exactness_zero_left_implies_hopf_injective_inference_rule,
  toda_prop515_pi10_3_concrete_exactness_inference_rule,
  toda_prop515_pi10_3_delta_injective_inference_rule,
  toda_prop515_pi10_3_delta_surjective_inference_rule,
  toda_prop515_pi10_3_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_3_data():
  phase75_2 = (
    build_phase75_2_data()
  )

  phase70_10 = (
    build_phase70_10_data()
  )

  phase73_8e = (
    build_phase73_8e_data()
  )

  pi9_2_zero_step = (
    phase75_2[
      "final_step"
    ]
  )

  prop59_step = (
    phase70_10[
      "integration_step"
    ]
  )

  prop511_step = (
    phase73_8e[
      "final_step"
    ]
  )

  pi9_2 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=2,
  )

  pi10_3 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=3,
  )

  pi10_5 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  pi8_2 = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=2,
  )

  pi9_3 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=3,
  )

  e_h_window_step = ProofStep(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi9_2,
      middle_term=pi10_3,
      target_term=pi10_5,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  h_delta_window_step = ProofStep(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi10_3,
      middle_term=pi10_5,
      target_term=pi8_2,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  delta_e_window_step = ProofStep(
    conclusion=TodaEHPExactnessWindow(
      source_term=pi10_5,
      middle_term=pi8_2,
      target_term=pi9_3,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  exactness_rule = (
    toda_prop515_pi10_3_concrete_exactness_inference_rule()
  )

  hopf_injective_rule = (
    toda_exactness_zero_left_implies_hopf_injective_inference_rule()
  )

  delta_surjective_rule = (
    toda_prop515_pi10_3_delta_surjective_inference_rule()
  )

  delta_injective_rule = (
    toda_prop515_pi10_3_delta_injective_inference_rule()
  )

  zero_rule = (
    toda_prop515_pi10_3_zero_inference_rule()
  )

  rules = (
    exactness_rule,
    hopf_injective_rule,
    delta_surjective_rule,
    delta_injective_rule,
    zero_rule,
  )

  premise_steps = (
    pi9_2_zero_step,
    prop59_step,
    prop511_step,
    e_h_window_step,
    h_delta_window_step,
    delta_e_window_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  e_h_exactness_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == TodaProp42ExactnessStatement(
        window=(
          e_h_window_step
          .conclusion
        ),
      )
    )
  )

  h_delta_exactness_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == TodaProp42ExactnessStatement(
        window=(
          h_delta_window_step
          .conclusion
        ),
      )
    )
  )

  delta_e_exactness_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == TodaProp42ExactnessStatement(
        window=(
          delta_e_window_step
          .conclusion
        ),
      )
    )
  )

  expected_hopf_injective = (
    TodaHopfInvariantInjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=pi10_3,
        target_group=pi10_5,
      ),
    )
  )

  hopf_injective_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_hopf_injective
    )
  )

  expected_delta_surjective = (
    TodaDeltaSurjectiveStatement(
      map=TodaDeltaMap(
        source_group=pi10_5,
        target_group=pi8_2,
      ),
    )
  )

  delta_surjective_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_delta_surjective
    )
  )

  expected_delta_injective = (
    TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=pi10_5,
        target_group=pi8_2,
      ),
    )
  )

  delta_injective_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_delta_injective
    )
  )

  expected_final = (
    TodaPrimaryGroupZeroStatement(
      group=pi10_3,
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_final
    )
  )

  return {
    "phase75_2": phase75_2,
    "phase70_10": phase70_10,
    "phase73_8e": phase73_8e,
    "pi9_2_zero_step": (
      pi9_2_zero_step
    ),
    "prop59_step": prop59_step,
    "prop511_step": prop511_step,
    "pi9_2": pi9_2,
    "pi10_3": pi10_3,
    "pi10_5": pi10_5,
    "pi8_2": pi8_2,
    "pi9_3": pi9_3,
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
    "hopf_injective_rule": (
      hopf_injective_rule
    ),
    "delta_surjective_rule": (
      delta_surjective_rule
    ),
    "delta_injective_rule": (
      delta_injective_rule
    ),
    "zero_rule": zero_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "e_h_exactness_step": (
      e_h_exactness_step
    ),
    "h_delta_exactness_step": (
      h_delta_exactness_step
    ),
    "delta_e_exactness_step": (
      delta_e_exactness_step
    ),
    "expected_hopf_injective": (
      expected_hopf_injective
    ),
    "hopf_injective_step": (
      hopf_injective_step
    ),
    "expected_delta_surjective": (
      expected_delta_surjective
    ),
    "delta_surjective_step": (
      delta_surjective_step
    ),
    "expected_delta_injective": (
      expected_delta_injective
    ),
    "delta_injective_step": (
      delta_injective_step
    ),
    "expected_final": expected_final,
    "final_step": final_step,
  }


def test_phase75_3_reuses_phase75_2_pi9_2_zero():
  data = build_phase75_3_data()

  assert (
    data[
      "pi9_2_zero_step"
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
      "pi9_2_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_3_reuses_prop59():
  data = build_phase75_3_data()

  assert isinstance(
    data[
      "prop59_step"
    ].conclusion,
    TodaProp59FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop59_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_3_reuses_prop511():
  data = build_phase75_3_data()

  assert isinstance(
    data[
      "prop511_step"
    ].conclusion,
    TodaProp511FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop511_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_3_prop59_pi10_5_is_order_two():
  data = build_phase75_3_data()

  relation = (
    data[
      "prop59_step"
    ].conclusion
    .pi10_5_group_relation
  )

  assert (
    relation.lhs
    == data[
      "pi10_5"
    ]
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 2
  )


def test_phase75_3_prop511_pi8_2_is_order_two():
  data = build_phase75_3_data()

  relation = (
    data[
      "prop511_step"
    ].conclusion
    .pi8_2_group_relation
  )

  assert (
    relation.lhs
    == data[
      "pi8_2"
    ]
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 2
  )


def test_phase75_3_prop511_pi9_3_is_zero():
  data = build_phase75_3_data()

  assert (
    data[
      "prop511_step"
    ].conclusion
    .pi9_3_zero
    == TodaPrimaryGroupZeroStatement(
      group=data[
        "pi9_3"
      ],
    )
  )


def test_phase75_3_derives_all_three_exactness_statements():
  data = build_phase75_3_data()

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

  assert (
    data[
      "delta_e_exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_3_derives_hopf_injective():
  data = build_phase75_3_data()

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


def test_phase75_3_hopf_injective_uses_phase75_2_zero():
  data = build_phase75_3_data()

  assert (
    data[
      "hopf_injective_step"
    ].premises
    == (
      data[
        "pi9_2_zero_step"
      ],
      data[
        "e_h_exactness_step"
      ],
    )
  )


def test_phase75_3_derives_delta_surjective():
  data = build_phase75_3_data()

  assert (
    data[
      "delta_surjective_step"
    ].conclusion
    == data[
      "expected_delta_surjective"
    ]
  )

  assert (
    data[
      "delta_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_3_delta_surjective_uses_prop511_and_exactness():
  data = build_phase75_3_data()

  assert (
    data[
      "delta_surjective_step"
    ].premises
    == (
      data[
        "prop511_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
    )
  )


def test_phase75_3_derives_delta_injective():
  data = build_phase75_3_data()

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


def test_phase75_3_delta_injective_uses_exact_three_premises():
  data = build_phase75_3_data()

  assert (
    data[
      "delta_injective_step"
    ].premises
    == (
      data[
        "delta_surjective_step"
      ],
      data[
        "prop59_step"
      ],
      data[
        "prop511_step"
      ],
    )
  )


def test_phase75_3_derives_pi10_3_zero():
  data = build_phase75_3_data()

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


def test_phase75_3_final_uses_exact_three_premises():
  data = build_phase75_3_data()

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


def test_phase75_3_final_statement_not_present_initially():
  data = build_phase75_3_data()

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase75_3_rejects_wrong_exactness_window():
  data = build_phase75_3_data()

  wrong_window = ProofStep(
    conclusion=TodaEHPExactnessWindow(
      source_term=data[
        "pi10_3"
      ],
      middle_term=data[
        "pi8_2"
      ],
      target_term=data[
        "pi10_5"
      ],
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "exactness_rule"
    ],
    (
      wrong_window,
    ),
  ) is None


def test_phase75_3_rejects_given_prop511_for_delta_surjectivity():
  data = build_phase75_3_data()

  given = ProofStep(
    conclusion=(
      data[
        "prop511_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "delta_surjective_rule"
    ],
    (
      given,
      data[
        "delta_e_exactness_step"
      ],
    ),
  ) is None


def test_phase75_3_rejects_wrong_source_order_for_delta_injectivity():
  data = build_phase75_3_data()

  prop59 = (
    data[
      "prop59_step"
    ].conclusion
  )

  relation = (
    prop59.pi10_5_group_relation
  )

  wrong_prop59 = replace(
    prop59,
    pi10_5_group_relation=replace(
      relation,
      rhs=FiniteCyclicGroup(
        order=4,
        generator=(
          relation
          .rhs
          .generator
        ),
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_prop59,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "delta_injective_rule"
    ],
    (
      data[
        "delta_surjective_step"
      ],
      wrong_step,
      data[
        "prop511_step"
      ],
    ),
  ) is None


def test_phase75_3_rejects_wrong_target_order_for_delta_injectivity():
  data = build_phase75_3_data()

  prop511 = (
    data[
      "prop511_step"
    ].conclusion
  )

  relation = (
    prop511.pi8_2_group_relation
  )

  wrong_prop511 = replace(
    prop511,
    pi8_2_group_relation=replace(
      relation,
      rhs=FiniteCyclicGroup(
        order=4,
        generator=(
          relation
          .rhs
          .generator
        ),
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_prop511,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "delta_injective_rule"
    ],
    (
      data[
        "delta_surjective_step"
      ],
      data[
        "prop59_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase75_3_rejects_given_hopf_injective_for_final():
  data = build_phase75_3_data()

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
      "zero_rule"
    ],
    (
      given,
      data[
        "delta_injective_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
    ),
  ) is None


def test_phase75_3_rejects_given_delta_injective_for_final():
  data = build_phase75_3_data()

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
      "zero_rule"
    ],
    (
      data[
        "hopf_injective_step"
      ],
      given,
      data[
        "h_delta_exactness_step"
      ],
    ),
  ) is None


def test_phase75_3_reaches_fixed_point():
  data = build_phase75_3_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


