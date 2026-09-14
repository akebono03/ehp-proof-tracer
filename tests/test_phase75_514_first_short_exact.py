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
from test_phase59_prop53_integration import (
  build_phase59_8_data,
)
from test_phase62_toda55_integration import (
  build_phase62_6_data,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from test_phase68_eta_n_nu_n_plus_one_zero import (
  build_phase68_8_data,
)
from test_phase69_delta_iota11 import (
  build_phase69_3_data,
)
from test_phase73_513_delta_nu9 import (
  build_phase73_6a_data,
)
from toda_rules import (
  Toda514FirstShortExactStatement,
  TodaProp42ExactnessStatement,
  TodaProp56FiniteDimensionalStatement,
  toda_514_delta_nu11_zero_inference_rule,
  toda_514_first_short_exact_concrete_exactness_inference_rule,
  toda_514_first_short_exact_inference_rule,
  toda_nu_family_definition_statement,
  toda_prop511_513_delta_eta11_squared_zero_inference_rule,
  toda_prop511_pi13_11_eta11_squared_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_6a_data():
  phase59_8 = (
    build_phase59_8_data()
  )

  phase62_6 = (
    build_phase62_6_data()
  )

  phase65_9 = (
    build_phase65_9_data()
  )

  phase68_8 = (
    build_phase68_8_data()
  )

  phase69_3 = (
    build_phase69_3_data()
  )

  phase73_6a = (
    build_phase73_6a_data()
  )

  prop53_step = (
    phase59_8[
      "integration_step"
    ]
  )

  toda55_step = (
    phase62_6[
      "integration_step"
    ]
  )

  prop56_step = (
    phase65_9[
      "integration_step"
    ]
  )

  eta_n_nu_n_plus_one_zero_step = (
    phase68_8[
      "final_step"
    ]
  )

  delta_iota11_step = (
    phase69_3[
      "final_step"
    ]
  )

  delta_nu9_step = (
    phase73_6a[
      "final_step"
    ]
  )

  delta_eta11_squared_rule = (
    toda_prop511_513_delta_eta11_squared_zero_inference_rule()
  )

  delta_eta11_squared_result = (
    run_inference_until_stable_with_history(
      (
        delta_eta11_squared_rule,
      ),
      (
        delta_iota11_step,
        toda55_step,
        delta_nu9_step,
      ),
    )
  )

  delta_eta11_squared_step = next(
    step
    for step
    in delta_eta11_squared_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.relation_type
      == RelationType.ZERO
      and isinstance(
        step.conclusion.lhs,
        MapApplication,
      )
      and step.conclusion.lhs.map
      == EHP_DELTA_MAP
      and isinstance(
        step.conclusion
        .lhs
        .expression,
        Composition,
      )
      and step.conclusion
      .lhs
      .expression
      .left
      .generator
      == GeneratorSymbol(
        family="η",
        index=11,
      )
    )
  )

  pi13_11_rule = (
    toda_prop511_pi13_11_eta11_squared_inference_rule()
  )

  pi13_11_result = (
    run_inference_until_stable_with_history(
      (
        pi13_11_rule,
      ),
      (
        prop53_step,
      ),
    )
  )

  pi13_11 = TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=11,
  )

  pi13_11_step = next(
    step
    for step
    in pi13_11_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi13_11
    )
  )

  pi14_11 = TodaPrimaryGroup(
    group_dimension=14,
    sphere_dimension=11,
  )

  pi12_5 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=5,
  )

  pi13_6 = TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=6,
  )

  pi11_5 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=5,
  )

  delta_e_window = (
    TodaEHPExactnessWindow(
      source_term=pi14_11,
      middle_term=pi12_5,
      target_term=pi13_6,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    )
  )

  e_h_window = (
    TodaEHPExactnessWindow(
      source_term=pi12_5,
      middle_term=pi13_6,
      target_term=pi13_11,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    )
  )

  h_delta_window = (
    TodaEHPExactnessWindow(
      source_term=pi13_6,
      middle_term=pi13_11,
      target_term=pi11_5,
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

  delta_nu11_rule = (
    toda_514_delta_nu11_zero_inference_rule()
  )

  exactness_rule = (
    toda_514_first_short_exact_concrete_exactness_inference_rule()
  )

  final_rule = (
    toda_514_first_short_exact_inference_rule()
  )

  rules = (
    delta_nu11_rule,
    exactness_rule,
    final_rule,
  )

  premise_steps = (
    delta_iota11_step,
    eta_n_nu_n_plus_one_zero_step,
    toda55_step,
    prop56_step,
    delta_eta11_squared_step,
    pi13_11_step,
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

  nu_11 = (
    toda_nu_family_definition_statement(
      11
    ).element
  )

  expected_delta_nu11_zero = Relation(
    lhs=MapApplication(
      map=EHP_DELTA_MAP,
      expression=nu_11,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  delta_nu11_zero_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_delta_nu11_zero
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
    Toda514FirstShortExactStatement(
      source_group=pi12_5,
      middle_group=pi13_6,
      target_group=pi13_11,
      suspension_map=TodaSuspensionMap(
        source_group=pi12_5,
        target_group=pi13_6,
      ),
      hopf_map=TodaHopfInvariantMap(
        source_group=pi13_6,
        target_group=pi13_11,
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
    "phase59_8": phase59_8,
    "phase62_6": phase62_6,
    "phase65_9": phase65_9,
    "phase68_8": phase68_8,
    "phase69_3": phase69_3,
    "phase73_6a": phase73_6a,
    "prop53_step": prop53_step,
    "toda55_step": toda55_step,
    "prop56_step": prop56_step,
    "eta_n_nu_n_plus_one_zero_step": (
      eta_n_nu_n_plus_one_zero_step
    ),
    "delta_iota11_step": (
      delta_iota11_step
    ),
    "delta_nu9_step": (
      delta_nu9_step
    ),
    "delta_eta11_squared_rule": (
      delta_eta11_squared_rule
    ),
    "delta_eta11_squared_step": (
      delta_eta11_squared_step
    ),
    "pi13_11_rule": pi13_11_rule,
    "pi13_11_step": pi13_11_step,
    "pi14_11": pi14_11,
    "pi12_5": pi12_5,
    "pi13_6": pi13_6,
    "pi13_11": pi13_11,
    "pi11_5": pi11_5,
    "delta_e_window": delta_e_window,
    "e_h_window": e_h_window,
    "h_delta_window": h_delta_window,
    "delta_e_window_step": (
      delta_e_window_step
    ),
    "e_h_window_step": (
      e_h_window_step
    ),
    "h_delta_window_step": (
      h_delta_window_step
    ),
    "delta_nu11_rule": delta_nu11_rule,
    "exactness_rule": exactness_rule,
    "final_rule": final_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "nu_11": nu_11,
    "expected_delta_nu11_zero": (
      expected_delta_nu11_zero
    ),
    "delta_nu11_zero_step": (
      delta_nu11_zero_step
    ),
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


def test_phase75_6a_reuses_delta_iota11():
  data = build_phase75_6a_data()

  assert (
    data[
      "delta_iota11_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6a_reuses_eta_n_nu_n_plus_one_zero():
  data = build_phase75_6a_data()

  assert (
    data[
      "eta_n_nu_n_plus_one_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6a_reuses_prop56():
  data = build_phase75_6a_data()

  assert isinstance(
    data[
      "prop56_step"
    ].conclusion,
    TodaProp56FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop56_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6a_derives_delta_eta11_squared_zero():
  data = build_phase75_6a_data()

  assert (
    data[
      "delta_eta11_squared_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "delta_eta11_squared_step"
    ].conclusion
    .relation_type
    == RelationType.ZERO
  )


def test_phase75_6a_derives_pi13_11_z2_eta11_squared():
  data = build_phase75_6a_data()

  relation = (
    data[
      "pi13_11_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == data[
      "pi13_11"
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

  assert (
    data[
      "pi13_11_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6a_derives_delta_nu11_zero():
  data = build_phase75_6a_data()

  assert (
    data[
      "delta_nu11_zero_step"
    ].conclusion
    == data[
      "expected_delta_nu11_zero"
    ]
  )

  assert (
    data[
      "delta_nu11_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6a_delta_nu11_uses_exact_dependencies():
  data = build_phase75_6a_data()

  assert (
    data[
      "delta_nu11_zero_step"
    ].premises
    == (
      data[
        "delta_iota11_step"
      ],
      data[
        "eta_n_nu_n_plus_one_zero_step"
      ],
      data[
        "toda55_step"
      ],
      data[
        "prop56_step"
      ],
    )
  )


def test_phase75_6a_derives_three_exactness_statements():
  data = build_phase75_6a_data()

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


def test_phase75_6a_derives_first_short_exact_sequence():
  data = build_phase75_6a_data()

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


def test_phase75_6a_first_short_exact_groups_are_correct():
  data = build_phase75_6a_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement.source_group
    == TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=5,
    )
  )

  assert (
    statement.middle_group
    == TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=6,
    )
  )

  assert (
    statement.target_group
    == TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=11,
    )
  )


def test_phase75_6a_first_short_exact_maps_are_correct():
  data = build_phase75_6a_data()

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
          "pi12_5"
        ]
      ),
      target_group=(
        data[
          "pi13_6"
        ]
      ),
    )
  )

  assert (
    statement.hopf_map
    == TodaHopfInvariantMap(
      source_group=(
        data[
          "pi13_6"
        ]
      ),
      target_group=(
        data[
          "pi13_11"
        ]
      ),
    )
  )


def test_phase75_6a_final_uses_exact_dependencies():
  data = build_phase75_6a_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "delta_nu11_zero_step"
      ],
      data[
        "delta_eta11_squared_step"
      ],
      data[
        "prop56_step"
      ],
      data[
        "pi13_11_step"
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


def test_phase75_6a_final_not_present_initially():
  data = build_phase75_6a_data()

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


def test_phase75_6a_rejects_given_delta_nu11_zero():
  data = build_phase75_6a_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_nu11_zero_step"
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
        "delta_eta11_squared_step"
      ],
      data[
        "prop56_step"
      ],
      data[
        "pi13_11_step"
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


def test_phase75_6a_rejects_given_delta_eta11_squared_zero():
  data = build_phase75_6a_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_eta11_squared_step"
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
        "delta_nu11_zero_step"
      ],
      given,
      data[
        "prop56_step"
      ],
      data[
        "pi13_11_step"
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


def test_phase75_6a_rejects_given_pi13_11():
  data = build_phase75_6a_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi13_11_step"
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
        "delta_nu11_zero_step"
      ],
      data[
        "delta_eta11_squared_step"
      ],
      data[
        "prop56_step"
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


def test_phase75_6a_reaches_fixed_point():
  data = build_phase75_6a_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


