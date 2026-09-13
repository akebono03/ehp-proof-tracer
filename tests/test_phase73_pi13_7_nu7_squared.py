from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  MapApplication,
  Zero,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaSuspensionIsomorphismStatement,
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
from test_phase55_prop51_integration import (
  build_phase55_5_integration,
)
from test_phase71_toda512_n6_delta_injective import (
  build_phase71_4_data,
)
from test_phase73_513_delta_eta13 import (
  build_phase73_6c_data,
)
from test_phase73_pi12_6_nu6_squared import (
  build_phase73_7b_data,
)
from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaProp42ExactnessStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionSurjectiveStatement,
  toda_nu_family_definition_statement,
  toda_prop511_pi13_7_concrete_exactness_inference_rule,
  toda_prop511_pi13_7_hopf_zero_inference_rule,
  toda_prop511_pi13_7_nu7_squared_inference_rule,
  toda_prop511_pi13_7_suspension_injective_inference_rule,
  toda_prop511_pi13_7_suspension_isomorphism_inference_rule,
  toda_prop511_pi13_7_suspension_surjective_inference_rule,
  toda_prop511_pi14_13_eta13_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase73_7c_data():
  phase55 = (
    build_phase55_5_integration()
  )

  phase71 = (
    build_phase71_4_data()
  )

  phase73_6c = (
    build_phase73_6c_data()
  )

  phase73_7b = (
    build_phase73_7b_data()
  )

  prop51_step = (
    phase55[
      "integration_steps"
    ][
      0
    ]
  )

  delta_injective_step = (
    phase71[
      "final_step"
    ]
  )

  delta_eta13_zero_step = (
    phase73_6c[
      "final_step"
    ]
  )

  pi12_6_step = (
    phase73_7b[
      "final_step"
    ]
  )

  pi14_13_rule = (
    toda_prop511_pi14_13_eta13_inference_rule()
  )

  pi14_13_match = find_inference_match(
    pi14_13_rule,
    (
      prop51_step,
    ),
  )

  assert (
    pi14_13_match
    is not None
  )

  pi14_13_step = apply_inference_match(
    pi14_13_match
  )

  pi14_13 = TodaPrimaryGroup(
    group_dimension=14,
    sphere_dimension=13,
  )

  pi12_6 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=6,
  )

  pi13_7 = TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=7,
  )

  pi13_13 = TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=13,
  )

  pi11_6 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=6,
  )

  delta_e_window = TodaEHPExactnessWindow(
    source_term=pi14_13,
    middle_term=pi12_6,
    target_term=pi13_7,
    first_map=EHP_DELTA_MAP,
    second_map=EHP_E_MAP,
  )

  e_h_window = TodaEHPExactnessWindow(
    source_term=pi12_6,
    middle_term=pi13_7,
    target_term=pi13_13,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )

  h_delta_window = TodaEHPExactnessWindow(
    source_term=pi13_7,
    middle_term=pi13_13,
    target_term=pi11_6,
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
    toda_prop511_pi13_7_concrete_exactness_inference_rule()
  )

  delta_e_exactness_match = find_inference_match(
    exactness_rule,
    (
      delta_e_window_step,
    ),
  )

  assert (
    delta_e_exactness_match
    is not None
  )

  delta_e_exactness_step = apply_inference_match(
    delta_e_exactness_match
  )

  e_h_exactness_match = find_inference_match(
    exactness_rule,
    (
      e_h_window_step,
    ),
  )

  assert (
    e_h_exactness_match
    is not None
  )

  e_h_exactness_step = apply_inference_match(
    e_h_exactness_match
  )

  h_delta_exactness_match = find_inference_match(
    exactness_rule,
    (
      h_delta_window_step,
    ),
  )

  assert (
    h_delta_exactness_match
    is not None
  )

  h_delta_exactness_step = apply_inference_match(
    h_delta_exactness_match
  )

  injectivity_rule = (
    toda_prop511_pi13_7_suspension_injective_inference_rule()
  )

  injectivity_match = find_inference_match(
    injectivity_rule,
    (
      pi14_13_step,
      delta_eta13_zero_step,
      delta_e_exactness_step,
    ),
  )

  assert (
    injectivity_match
    is not None
  )

  injectivity_step = apply_inference_match(
    injectivity_match
  )

  hopf_zero_rule = (
    toda_prop511_pi13_7_hopf_zero_inference_rule()
  )

  hopf_zero_match = find_inference_match(
    hopf_zero_rule,
    (
      delta_injective_step,
      h_delta_exactness_step,
    ),
  )

  assert (
    hopf_zero_match
    is not None
  )

  hopf_zero_step = apply_inference_match(
    hopf_zero_match
  )

  surjectivity_rule = (
    toda_prop511_pi13_7_suspension_surjective_inference_rule()
  )

  surjectivity_match = find_inference_match(
    surjectivity_rule,
    (
      hopf_zero_step,
      e_h_exactness_step,
    ),
  )

  assert (
    surjectivity_match
    is not None
  )

  surjectivity_step = apply_inference_match(
    surjectivity_match
  )

  isomorphism_rule = (
    toda_prop511_pi13_7_suspension_isomorphism_inference_rule()
  )

  isomorphism_match = find_inference_match(
    isomorphism_rule,
    (
      injectivity_step,
      surjectivity_step,
    ),
  )

  assert (
    isomorphism_match
    is not None
  )

  isomorphism_step = apply_inference_match(
    isomorphism_match
  )

  final_rule = (
    toda_prop511_pi13_7_nu7_squared_inference_rule()
  )

  final_match = find_inference_match(
    final_rule,
    (
      pi12_6_step,
      isomorphism_step,
    ),
  )

  assert (
    final_match
    is not None
  )

  final_step = apply_inference_match(
    final_match
  )

  eta_13 = (
    pi14_13_step
    .conclusion
    .rhs
    .generator
  )

  nu_7 = (
    toda_nu_family_definition_statement(
      7
    ).element
  )

  nu_10 = (
    toda_nu_family_definition_statement(
      10
    ).element
  )

  nu7_squared = Composition(
    left=nu_7,
    right=nu_10,
  )

  expected_statement = Relation(
    lhs=pi13_7,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=nu7_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  return {
    "phase55": phase55,
    "phase71": phase71,
    "phase73_6c": phase73_6c,
    "phase73_7b": phase73_7b,
    "prop51_step": prop51_step,
    "delta_injective_step": (
      delta_injective_step
    ),
    "delta_eta13_zero_step": (
      delta_eta13_zero_step
    ),
    "pi12_6_step": pi12_6_step,
    "pi14_13_step": pi14_13_step,
    "pi14_13": pi14_13,
    "pi12_6": pi12_6,
    "pi13_7": pi13_7,
    "pi13_13": pi13_13,
    "pi11_6": pi11_6,
    "delta_e_window_step": (
      delta_e_window_step
    ),
    "e_h_window_step": e_h_window_step,
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
    "injectivity_step": injectivity_step,
    "hopf_zero_step": hopf_zero_step,
    "surjectivity_step": (
      surjectivity_step
    ),
    "isomorphism_step": (
      isomorphism_step
    ),
    "eta_13": eta_13,
    "nu_7": nu_7,
    "nu_10": nu_10,
    "nu7_squared": nu7_squared,
    "expected_statement": (
      expected_statement
    ),
    "final_rule": final_rule,
    "final_step": final_step,
  }


def test_phase73_7c_reuses_prop51():
  data = build_phase73_7c_data()

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


def test_phase73_7c_derives_pi14_13():
  data = build_phase73_7c_data()

  relation = (
    data[
      "pi14_13_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == data[
      "pi14_13"
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

  eta_13 = (
    relation.rhs.generator
  )

  assert (
    eta_13.dimension
    == 13
  )

  assert (
    eta_13.source
    == 14
  )

  assert (
    eta_13.target
    == 13
  )

  assert (
    eta_13.generator
    == GeneratorSymbol(
      family="η",
      index=13,
    )
  )


def test_phase73_7c_reuses_delta_eta13_zero():
  data = build_phase73_7c_data()

  step = (
    data[
      "delta_eta13_zero_step"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  relation = (
    step.conclusion
  )

  assert (
    relation.relation_type
    == RelationType.ZERO
  )

  assert isinstance(
    relation.lhs,
    MapApplication,
  )

  assert (
    relation.lhs.map
    == EHP_DELTA_MAP
  )

  eta_13 = (
    relation
    .lhs
    .expression
  )

  assert (
    eta_13.dimension
    == 13
  )

  assert (
    eta_13.source
    == 14
  )

  assert (
    eta_13.target
    == 13
  )

  assert (
    eta_13.generator
    == GeneratorSymbol(
      family="η",
      index=13,
    )
  )

  assert (
    relation.rhs
    == Zero()
  )


def test_phase73_7c_reuses_phase71_n6_injectivity():
  data = build_phase73_7c_data()

  assert isinstance(
    data[
      "delta_injective_step"
    ].conclusion,
    TodaDeltaInjectiveStatement,
  )

  assert (
    data[
      "delta_injective_step"
    ].conclusion.map
    == TodaDeltaMap(
      source_group=data[
        "pi13_13"
      ],
      target_group=data[
        "pi11_6"
      ],
    )
  )

  assert (
    data[
      "delta_injective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_7c_three_exactness_windows_are_derived():
  data = build_phase73_7c_data()

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


def test_phase73_7c_structural_windows_remain_given():
  data = build_phase73_7c_data()

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


def test_phase73_7c_suspension_is_injective():
  data = build_phase73_7c_data()

  assert (
    data[
      "injectivity_step"
    ].conclusion
    == TodaSuspensionInjectiveStatement(
      map=TodaSuspensionMap(
        source_group=data[
          "pi12_6"
        ],
        target_group=data[
          "pi13_7"
        ],
      )
    )
  )


def test_phase73_7c_hopf_is_zero():
  data = build_phase73_7c_data()

  assert (
    data[
      "hopf_zero_step"
    ].conclusion
    == TodaHopfInvariantZeroStatement(
      map=TodaHopfInvariantMap(
        source_group=data[
          "pi13_7"
        ],
        target_group=data[
          "pi13_13"
        ],
      )
    )
  )


def test_phase73_7c_suspension_is_surjective():
  data = build_phase73_7c_data()

  assert (
    data[
      "surjectivity_step"
    ].conclusion
    == TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=data[
          "pi12_6"
        ],
        target_group=data[
          "pi13_7"
        ],
      )
    )
  )


def test_phase73_7c_suspension_is_isomorphism():
  data = build_phase73_7c_data()

  assert (
    data[
      "isomorphism_step"
    ].conclusion
    == TodaSuspensionIsomorphismStatement(
      map=TodaSuspensionMap(
        source_group=data[
          "pi12_6"
        ],
        target_group=data[
          "pi13_7"
        ],
      )
    )
  )

  assert (
    data[
      "isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_7c_nu7_squared_is_composition():
  data = build_phase73_7c_data()

  assert (
    data[
      "nu7_squared"
    ]
    == Composition(
      left=data[
        "nu_7"
      ],
      right=data[
        "nu_10"
      ],
    )
  )

  assert (
    data[
      "nu7_squared"
    ].is_type_compatible()
  )


def test_phase73_7c_derives_pi13_7():
  data = build_phase73_7c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_7c_pi13_7_is_order_two():
  data = build_phase73_7c_data()

  group = (
    data[
      "final_step"
    ].conclusion
    .rhs
  )

  assert (
    group.order
    == 2
  )

  assert (
    group.generator
    == data[
      "nu7_squared"
    ]
  )


def test_phase73_7c_final_uses_exact_two_dependencies():
  data = build_phase73_7c_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi12_6_step"
      ],
      data[
        "isomorphism_step"
      ],
    )
  )


def test_phase73_7c_rejects_given_pi12_6():
  data = build_phase73_7c_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi12_6_step"
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
        "isomorphism_step"
      ],
    ),
  ) is None


def test_phase73_7c_rejects_wrong_pi12_6_order():
  data = build_phase73_7c_data()

  relation = (
    data[
      "pi12_6_step"
    ].conclusion
  )

  wrong_relation = replace(
    relation,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=(
        relation
        .rhs
        .generator
      ),
    ),
  )

  wrong = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      wrong,
      data[
        "isomorphism_step"
      ],
    ),
  ) is None


def test_phase73_7c_rejects_given_isomorphism():
  data = build_phase73_7c_data()

  given = ProofStep(
    conclusion=(
      data[
        "isomorphism_step"
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
        "pi12_6_step"
      ],
      given,
    ),
  ) is None


def test_phase73_7c_final_is_not_given():
  data = build_phase73_7c_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )



