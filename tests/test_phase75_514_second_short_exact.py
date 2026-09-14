from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  MapApplication,
  Zero,
)
from homotopy_groups import (
  FiniteCyclicGroup,
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
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase55_prop51_integration import (
  build_phase55_5_integration,
)
from test_phase59_prop53_integration import (
  build_phase59_8_data,
)
from test_phase73_513_delta_eta13 import (
  build_phase73_6c_data,
)
from toda_rules import (
  Toda514SecondShortExactStatement,
  TodaProp42ExactnessStatement,
  TodaProp53FiniteDimensionalStatement,
  toda_514_delta_eta13_squared_zero_inference_rule,
  toda_514_second_short_exact_concrete_exactness_inference_rule,
  toda_514_second_short_exact_inference_rule,
  toda_eta_family_definition_statement,
  toda_prop511_pi14_13_eta13_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_7a_data():
  phase55 = (
    build_phase55_5_integration()
  )

  phase59 = (
    build_phase59_8_data()
  )

  phase73_6c = (
    build_phase73_6c_data()
  )

  prop51_step = (
    phase55[
      "integration_steps"
    ][
      0
    ]
  )

  prop53_step = (
    phase59[
      "integration_step"
    ]
  )

  delta_eta13_step = (
    phase73_6c[
      "final_step"
    ]
  )

  pi14_13_rule = (
    toda_prop511_pi14_13_eta13_inference_rule()
  )

  pi14_13_result = (
    run_inference_until_stable_with_history(
      (
        pi14_13_rule,
      ),
      (
        prop51_step,
      ),
    )
  )

  pi14_13 = TodaPrimaryGroup(
    group_dimension=14,
    sphere_dimension=13,
  )

  pi14_13_step = next(
    step
    for step in pi14_13_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi14_13
    )
  )

  delta_eta13_squared_rule = (
    toda_514_delta_eta13_squared_zero_inference_rule()
  )

  delta_eta13_squared_result = (
    run_inference_until_stable_with_history(
      (
        delta_eta13_squared_rule,
      ),
      (
        delta_eta13_step,
        prop53_step,
      ),
    )
  )

  eta_13 = (
    toda_eta_family_definition_statement(
      13
    ).element
  )

  eta_14 = (
    toda_eta_family_definition_statement(
      14
    ).element
  )

  eta13_squared = Composition(
    left=eta_13,
    right=eta_14,
  )

  expected_delta_eta13_squared_zero = (
    Relation(
      lhs=MapApplication(
        map=EHP_DELTA_MAP,
        expression=eta13_squared,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  delta_eta13_squared_step = next(
    step
    for step
    in delta_eta13_squared_result.steps
    if (
      step.conclusion
      == expected_delta_eta13_squared_zero
    )
  )

  pi15_13 = TodaPrimaryGroup(
    group_dimension=15,
    sphere_dimension=13,
  )

  pi13_6 = TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=6,
  )

  pi14_7 = TodaPrimaryGroup(
    group_dimension=14,
    sphere_dimension=7,
  )

  pi12_6 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=6,
  )

  delta_e_window = (
    TodaEHPExactnessWindow(
      source_term=pi15_13,
      middle_term=pi13_6,
      target_term=pi14_7,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    )
  )

  e_h_window = (
    TodaEHPExactnessWindow(
      source_term=pi13_6,
      middle_term=pi14_7,
      target_term=pi14_13,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    )
  )

  h_delta_window = (
    TodaEHPExactnessWindow(
      source_term=pi14_7,
      middle_term=pi14_13,
      target_term=pi12_6,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    )
  )

  delta_e_window_step = ProofStep(
    conclusion=delta_e_window,
    premises=(),
    rule=ProofRule.GIVEN,
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

  exactness_rule = (
    toda_514_second_short_exact_concrete_exactness_inference_rule()
  )

  final_rule = (
    toda_514_second_short_exact_inference_rule()
  )

  rules = (
    exactness_rule,
    final_rule,
  )

  premise_steps = (
    delta_eta13_squared_step,
    delta_eta13_step,
    prop53_step,
    pi14_13_step,
    delta_e_window_step,
    e_h_window_step,
    h_delta_window_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  delta_e_exactness_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == TodaProp42ExactnessStatement(
        window=delta_e_window,
      )
    )
  )

  e_h_exactness_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == TodaProp42ExactnessStatement(
        window=e_h_window,
      )
    )
  )

  h_delta_exactness_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == TodaProp42ExactnessStatement(
        window=h_delta_window,
      )
    )
  )

  expected_final = (
    Toda514SecondShortExactStatement(
      source_group=pi13_6,
      middle_group=pi14_7,
      target_group=pi14_13,
      suspension_map=TodaSuspensionMap(
        source_group=pi13_6,
        target_group=pi14_7,
      ),
      hopf_map=TodaHopfInvariantMap(
        source_group=pi14_7,
        target_group=pi14_13,
      ),
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
    "phase55": phase55,
    "phase59": phase59,
    "phase73_6c": phase73_6c,
    "prop51_step": prop51_step,
    "prop53_step": prop53_step,
    "delta_eta13_step": delta_eta13_step,
    "pi14_13_rule": pi14_13_rule,
    "pi14_13_step": pi14_13_step,
    "delta_eta13_squared_rule": (
      delta_eta13_squared_rule
    ),
    "delta_eta13_squared_step": (
      delta_eta13_squared_step
    ),
    "expected_delta_eta13_squared_zero": (
      expected_delta_eta13_squared_zero
    ),
    "pi15_13": pi15_13,
    "pi13_6": pi13_6,
    "pi14_7": pi14_7,
    "pi14_13": pi14_13,
    "pi12_6": pi12_6,
    "delta_e_window": delta_e_window,
    "e_h_window": e_h_window,
    "h_delta_window": h_delta_window,
    "delta_e_window_step": delta_e_window_step,
    "e_h_window_step": e_h_window_step,
    "h_delta_window_step": h_delta_window_step,
    "exactness_rule": exactness_rule,
    "final_rule": final_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "delta_e_exactness_step": (
      delta_e_exactness_step
    ),
    "e_h_exactness_step": (
      e_h_exactness_step
    ),
    "h_delta_exactness_step": (
      h_delta_exactness_step
    ),
    "expected_final": expected_final,
    "final_step": final_step,
  }


def test_phase75_7a_reuses_delta_eta13():
  data = build_phase75_7a_data()

  assert (
    data[
      "delta_eta13_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_7a_reuses_prop53():
  data = build_phase75_7a_data()

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


def test_phase75_7a_derives_pi14_13_z2_eta13():
  data = build_phase75_7a_data()

  relation = (
    data[
      "pi14_13_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=13,
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
    relation.rhs.generator
    == toda_eta_family_definition_statement(
      13
    ).element
  )

  assert (
    data[
      "pi14_13_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_7a_derives_delta_eta13_squared_zero():
  data = build_phase75_7a_data()

  assert (
    data[
      "delta_eta13_squared_step"
    ].conclusion
    == data[
      "expected_delta_eta13_squared_zero"
    ]
  )

  assert (
    data[
      "delta_eta13_squared_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_7a_delta_eta13_squared_uses_exact_dependencies():
  data = build_phase75_7a_data()

  assert (
    data[
      "delta_eta13_squared_step"
    ].premises
    == (
      data[
        "delta_eta13_step"
      ],
      data[
        "prop53_step"
      ],
    )
  )


def test_phase75_7a_derives_three_exactness_statements():
  data = build_phase75_7a_data()

  assert (
    data[
      "delta_e_exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )

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


def test_phase75_7a_derives_second_short_exact_sequence():
  data = build_phase75_7a_data()

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


def test_phase75_7a_second_short_exact_groups_are_correct():
  data = build_phase75_7a_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement.source_group
    == TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=6,
    )
  )

  assert (
    statement.middle_group
    == TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=7,
    )
  )

  assert (
    statement.target_group
    == TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=13,
    )
  )


def test_phase75_7a_second_short_exact_maps_are_correct():
  data = build_phase75_7a_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement.suspension_map
    == TodaSuspensionMap(
      source_group=(
        data[
          "pi13_6"
        ]
      ),
      target_group=(
        data[
          "pi14_7"
        ]
      ),
    )
  )

  assert (
    statement.hopf_map
    == TodaHopfInvariantMap(
      source_group=(
        data[
          "pi14_7"
        ]
      ),
      target_group=(
        data[
          "pi14_13"
        ]
      ),
    )
  )


def test_phase75_7a_final_uses_exact_dependencies():
  data = build_phase75_7a_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "delta_eta13_squared_step"
      ],
      data[
        "delta_eta13_step"
      ],
      data[
        "prop53_step"
      ],
      data[
        "pi14_13_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
      data[
        "e_h_exactness_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
    )
  )


def test_phase75_7a_final_not_present_initially():
  data = build_phase75_7a_data()

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase75_7a_rejects_given_delta_eta13_squared_zero():
  data = build_phase75_7a_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_eta13_squared_step"
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
        "delta_eta13_step"
      ],
      data[
        "prop53_step"
      ],
      data[
        "pi14_13_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
      data[
        "e_h_exactness_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
    ),
  ) is None


def test_phase75_7a_rejects_given_delta_eta13_zero():
  data = build_phase75_7a_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_eta13_step"
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
        "delta_eta13_squared_step"
      ],
      given,
      data[
        "prop53_step"
      ],
      data[
        "pi14_13_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
      data[
        "e_h_exactness_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
    ),
  ) is None


def test_phase75_7a_rejects_given_pi14_13_relation():
  data = build_phase75_7a_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi14_13_step"
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
        "delta_eta13_squared_step"
      ],
      data[
        "delta_eta13_step"
      ],
      data[
        "prop53_step"
      ],
      given,
      data[
        "delta_e_exactness_step"
      ],
      data[
        "e_h_exactness_step"
      ],
      data[
        "h_delta_exactness_step"
      ],
    ),
  ) is None


def test_phase75_7a_reaches_fixed_point():
  data = build_phase75_7a_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


