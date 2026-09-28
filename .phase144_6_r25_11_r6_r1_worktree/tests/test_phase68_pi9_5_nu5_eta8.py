from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
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
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from test_phase68_delta_eta9 import (
  build_phase68_5_data,
)
from test_phase68_pi8_4_decomposition import (
  build_phase68_4_data,
)
from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionSurjectiveStatement,
  toda_nu_family_definition_statement,
  toda_prop58_e_nu4_eta7_bridge_inference_rule,
  toda_prop58_pi9_5_concrete_exactness_inference_rule,
  toda_prop58_pi9_5_finite_cyclic_inference_rule,
  toda_prop58_pi9_5_hopf_zero_inference_rule,
  toda_prop58_pi9_5_suspension_surjective_inference_rule,
  toda_prop58_pi9_9_delta_injective_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase68_6_data():
  phase65_9 = (
    build_phase65_9_data()
  )

  phase68_4 = (
    build_phase68_4_data()
  )

  phase68_5 = (
    build_phase68_5_data()
  )

  prop56_step = (
    phase65_9[
      "integration_step"
    ]
  )

  toda58_step = (
    phase68_5[
      "toda58_step"
    ]
  )

  pi8_4_step = (
    phase68_4[
      "final_step"
    ]
  )

  prop51_step = (
    phase68_4[
      "prop51_step"
    ]
  )

  delta_eta9_step = (
    phase68_5[
      "final_step"
    ]
  )

  nu5_definition_step = ProofStep(
    conclusion=(
      toda_nu_family_definition_statement(
        5
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi10_9 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=9,
  )

  pi8_4 = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=4,
  )

  pi9_5 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  pi9_9 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=9,
  )

  pi7_4 = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=4,
  )

  delta_e_window = TodaEHPExactnessWindow(
    source_term=pi10_9,
    middle_term=pi8_4,
    target_term=pi9_5,
    first_map=EHP_DELTA_MAP,
    second_map=EHP_E_MAP,
  )

  e_h_window = TodaEHPExactnessWindow(
    source_term=pi8_4,
    middle_term=pi9_5,
    target_term=pi9_9,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )

  h_delta_window = TodaEHPExactnessWindow(
    source_term=pi9_5,
    middle_term=pi9_9,
    target_term=pi7_4,
    first_map=EHP_H_MAP,
    second_map=EHP_DELTA_MAP,
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
    toda_prop58_pi9_5_concrete_exactness_inference_rule()
  )

  delta_injective_rule = (
    toda_prop58_pi9_9_delta_injective_inference_rule()
  )

  hopf_zero_rule = (
    toda_prop58_pi9_5_hopf_zero_inference_rule()
  )

  suspension_surjective_rule = (
    toda_prop58_pi9_5_suspension_surjective_inference_rule()
  )

  generator_bridge_rule = (
    toda_prop58_e_nu4_eta7_bridge_inference_rule()
  )

  final_rule = (
    toda_prop58_pi9_5_finite_cyclic_inference_rule()
  )

  rules = (
    exactness_rule,
    delta_injective_rule,
    hopf_zero_rule,
    suspension_surjective_rule,
    generator_bridge_rule,
    final_rule,
  )

  premise_steps = (
    prop56_step,
    toda58_step,
    pi8_4_step,
    prop51_step,
    delta_eta9_step,
    nu5_definition_step,
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

  delta_e_exactness = (
    TodaProp42ExactnessStatement(
      window=delta_e_window,
    )
  )

  e_h_exactness = (
    TodaProp42ExactnessStatement(
      window=e_h_window,
    )
  )

  h_delta_exactness = (
    TodaProp42ExactnessStatement(
      window=h_delta_window,
    )
  )

  delta_e_exactness_step = next(
    step
    for step in result.steps
    if step.conclusion
    == delta_e_exactness
  )

  e_h_exactness_step = next(
    step
    for step in result.steps
    if step.conclusion
    == e_h_exactness
  )

  h_delta_exactness_step = next(
    step
    for step in result.steps
    if step.conclusion
    == h_delta_exactness
  )

  delta_injective_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaDeltaInjectiveStatement,
    )
    and step.conclusion.map.source_group
    == pi9_9
  )

  hopf_zero_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaHopfInvariantZeroStatement,
    )
    and step.conclusion.map.source_group
    == pi9_5
  )

  suspension_surjective_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaSuspensionSurjectiveStatement,
    )
    and step.conclusion.map.source_group
    == pi8_4
  )

  nu_4 = (
    pi8_4_step
    .conclusion
    .rhs
    .summands[
      0
    ]
    .generator
    .left
  )

  eta_7 = (
    pi8_4_step
    .conclusion
    .rhs
    .summands[
      0
    ]
    .generator
    .right
  )

  nu4_eta7 = Composition(
    left=nu_4,
    right=eta_7,
  )

  nu_5 = (
    nu5_definition_step
    .conclusion
    .element
  )

  eta_8 = HomotopyElement(
    name="η₈",
    dimension=8,
    source=9,
    target=8,
    generator=GeneratorSymbol(
      family="η",
      index=8,
    ),
  )

  nu5_eta8 = Composition(
    left=nu_5,
    right=eta_8,
  )

  expected_bridge = Relation(
    lhs=Suspension(
      expression=nu4_eta7,
    ),
    rhs=nu5_eta8,
    relation_type=RelationType.EQUALITY,
  )

  generator_bridge_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_bridge
    )
  )

  expected_final = Relation(
    lhs=pi9_5,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=nu5_eta8,
    ),
    relation_type=RelationType.EQUALITY,
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
    "phase65_9": phase65_9,
    "phase68_4": phase68_4,
    "phase68_5": phase68_5,
    "prop56_step": prop56_step,
    "toda58_step": toda58_step,
    "pi8_4_step": pi8_4_step,
    "prop51_step": prop51_step,
    "delta_eta9_step": (
      delta_eta9_step
    ),
    "nu5_definition_step": (
      nu5_definition_step
    ),
    "delta_e_window_step": (
      delta_e_window_step
    ),
    "e_h_window_step": (
      e_h_window_step
    ),
    "h_delta_window_step": (
      h_delta_window_step
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
    "delta_injective_step": (
      delta_injective_step
    ),
    "hopf_zero_step": (
      hopf_zero_step
    ),
    "suspension_surjective_step": (
      suspension_surjective_step
    ),
    "generator_bridge_step": (
      generator_bridge_step
    ),
    "final_step": final_step,
    "exactness_rule": exactness_rule,
    "delta_injective_rule": (
      delta_injective_rule
    ),
    "hopf_zero_rule": hopf_zero_rule,
    "suspension_surjective_rule": (
      suspension_surjective_rule
    ),
    "generator_bridge_rule": (
      generator_bridge_rule
    ),
    "final_rule": final_rule,
    "premise_steps": premise_steps,
    "result": result,
    "pi9_5": pi9_5,
    "nu4_eta7": nu4_eta7,
    "nu5_eta8": nu5_eta8,
    "expected_bridge": (
      expected_bridge
    ),
    "expected_final": (
      expected_final
    ),
  }


def test_phase68_6_delta_injective_is_derived():
  data = build_phase68_6_data()

  assert (
    data[
      "delta_injective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_6_delta_injective_uses_toda58_and_prop56():
  data = build_phase68_6_data()

  assert (
    data[
      "delta_injective_step"
    ].premises
    == (
      data[
        "toda58_step"
      ],
      data[
        "prop56_step"
      ],
    )
  )


def test_phase68_6_three_exactness_windows_are_derived():
  data = build_phase68_6_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in (
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


def test_phase68_6_structural_windows_remain_given():
  data = build_phase68_6_data()

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in (
      data[
        "delta_e_window_step"
      ],
      data[
        "e_h_window_step"
      ],
      data[
        "h_delta_window_step"
      ],
    )
  )


def test_phase68_6_hopf_zero_is_derived():
  data = build_phase68_6_data()

  assert (
    data[
      "hopf_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_6_hopf_zero_uses_delta_injectivity():
  data = build_phase68_6_data()

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


def test_phase68_6_suspension_surjective_is_derived():
  data = build_phase68_6_data()

  assert (
    data[
      "suspension_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_6_generator_bridge_is_derived():
  data = build_phase68_6_data()

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


def test_phase68_6_final_is_pi9_5():
  data = build_phase68_6_data()

  assert (
    data[
      "final_step"
    ].conclusion.lhs
    == data[
      "pi9_5"
    ]
  )


def test_phase68_6_final_is_order_two():
  data = build_phase68_6_data()

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


def test_phase68_6_final_generator_is_nu5_eta8():
  data = build_phase68_6_data()

  assert (
    data[
      "final_step"
    ].conclusion.rhs.generator
    == data[
      "nu5_eta8"
    ]
  )


def test_phase68_6_final_is_derived():
  data = build_phase68_6_data()

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


def test_phase68_6_final_reuses_phase68_5_delta_eta9():
  data = build_phase68_6_data()

  assert (
    data[
      "delta_eta9_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "delta_eta9_step"
    ]
    in data[
      "final_step"
    ].premises
  )


def test_phase68_6_rejects_given_delta_injective():
  data = build_phase68_6_data()

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


def test_phase68_6_rejects_given_pi8_4():
  data = build_phase68_6_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi8_4_step"
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
        "delta_eta9_step"
      ],
      data[
        "prop51_step"
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


def test_phase68_6_rejects_given_delta_eta9():
  data = build_phase68_6_data()

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
      "final_rule"
    ],
    (
      data[
        "pi8_4_step"
      ],
      given,
      data[
        "prop51_step"
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


def test_phase68_6_final_result_is_not_given():
  data = build_phase68_6_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase68_6_final_not_present_in_initial_premises():
  data = build_phase68_6_data()

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


def test_phase68_6_reaches_fixed_point():
  data = build_phase68_6_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


