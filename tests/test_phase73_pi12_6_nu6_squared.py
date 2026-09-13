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
from test_phase59_prop53_integration import (
  build_phase59_8_data,
)
from test_phase71_toda512_n5_delta_injective import (
  build_phase71_3_data,
)
from test_phase73_513_delta_eta11_squared import (
  build_phase73_6b_data,
)
from test_phase73_pi11_5_nu5_squared import (
  build_phase73_7a_data,
)
from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaProp42ExactnessStatement,
  TodaProp53FiniteDimensionalStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionSurjectiveStatement,
  toda_eta_family_definition_statement,
  toda_nu_family_definition_statement,
  toda_prop511_pi12_6_concrete_exactness_inference_rule,
  toda_prop511_pi12_6_hopf_zero_inference_rule,
  toda_prop511_pi12_6_nu6_squared_inference_rule,
  toda_prop511_pi12_6_suspension_injective_inference_rule,
  toda_prop511_pi12_6_suspension_isomorphism_inference_rule,
  toda_prop511_pi12_6_suspension_surjective_inference_rule,
  toda_prop511_pi13_11_eta11_squared_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase73_7b_data():
  phase59 = (
    build_phase59_8_data()
  )

  phase71 = (
    build_phase71_3_data()
  )

  phase73_6b = (
    build_phase73_6b_data()
  )

  phase73_7a = (
    build_phase73_7a_data()
  )

  prop53_step = (
    phase59[
      "integration_step"
    ]
  )

  delta_injective_step = (
    phase71[
      "final_step"
    ]
  )

  delta_eta11_squared_zero_step = (
    phase73_6b[
      "final_step"
    ]
  )

  pi11_5_step = (
    phase73_7a[
      "final_step"
    ]
  )

  pi13_11_rule = (
    toda_prop511_pi13_11_eta11_squared_inference_rule()
  )

  pi13_11_match = find_inference_match(
    pi13_11_rule,
    (
      prop53_step,
    ),
  )

  assert (
    pi13_11_match
    is not None
  )

  pi13_11_step = apply_inference_match(
    pi13_11_match
  )

  pi13_11 = TodaPrimaryGroup(
    group_dimension=13,
    sphere_dimension=11,
  )

  pi11_5 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=5,
  )

  pi12_6 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=6,
  )

  pi12_11 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=11,
  )

  pi10_5 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  delta_e_window = TodaEHPExactnessWindow(
    source_term=pi13_11,
    middle_term=pi11_5,
    target_term=pi12_6,
    first_map=EHP_DELTA_MAP,
    second_map=EHP_E_MAP,
  )

  e_h_window = TodaEHPExactnessWindow(
    source_term=pi11_5,
    middle_term=pi12_6,
    target_term=pi12_11,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )

  h_delta_window = TodaEHPExactnessWindow(
    source_term=pi12_6,
    middle_term=pi12_11,
    target_term=pi10_5,
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
    toda_prop511_pi12_6_concrete_exactness_inference_rule()
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

  injectivity_rule = (
    toda_prop511_pi12_6_suspension_injective_inference_rule()
  )

  injectivity_match = find_inference_match(
    injectivity_rule,
    (
      pi13_11_step,
      delta_eta11_squared_zero_step,
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
    toda_prop511_pi12_6_hopf_zero_inference_rule()
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
    toda_prop511_pi12_6_suspension_surjective_inference_rule()
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
    toda_prop511_pi12_6_suspension_isomorphism_inference_rule()
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
    toda_prop511_pi12_6_nu6_squared_inference_rule()
  )

  final_match = find_inference_match(
    final_rule,
    (
      pi11_5_step,
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

  eta11_squared = (
    pi13_11_step
    .conclusion
    .rhs
    .generator
  )

  nu_6 = (
    toda_nu_family_definition_statement(
      6
    ).element
  )

  nu_9 = (
    toda_nu_family_definition_statement(
      9
    ).element
  )

  nu6_squared = Composition(
    left=nu_6,
    right=nu_9,
  )

  expected_statement = Relation(
    lhs=pi12_6,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=nu6_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  return {
    "phase59": phase59,
    "phase71": phase71,
    "phase73_6b": phase73_6b,
    "phase73_7a": phase73_7a,
    "prop53_step": prop53_step,
    "delta_injective_step": (
      delta_injective_step
    ),
    "delta_eta11_squared_zero_step": (
      delta_eta11_squared_zero_step
    ),
    "pi11_5_step": pi11_5_step,
    "pi13_11_step": pi13_11_step,
    "pi13_11": pi13_11,
    "pi11_5": pi11_5,
    "pi12_6": pi12_6,
    "pi12_11": pi12_11,
    "pi10_5": pi10_5,
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
    "eta11_squared": eta11_squared,
    "nu_6": nu_6,
    "nu_9": nu_9,
    "nu6_squared": nu6_squared,
    "expected_statement": (
      expected_statement
    ),
    "final_rule": final_rule,
    "final_step": final_step,
  }


def test_phase73_7b_reuses_prop53():
  data = build_phase73_7b_data()

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


def test_phase73_7b_derives_pi13_11():
  data = build_phase73_7b_data()

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
    relation.rhs.generator
    == data[
      "eta11_squared"
    ]
  )


def test_phase73_7b_reuses_delta_eta11_squared_zero():
  data = build_phase73_7b_data()

  step = (
    data[
      "delta_eta11_squared_zero_step"
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

  eta11_squared = (
    relation
    .lhs
    .expression
  )

  assert isinstance(
    eta11_squared,
    Composition,
  )

  eta_11 = (
    eta11_squared.left
  )

  eta_12 = (
    eta11_squared.right
  )

  assert (
    eta_11.dimension
    == 11
  )

  assert (
    eta_11.source
    == 12
  )

  assert (
    eta_11.target
    == 11
  )

  assert (
    eta_11.generator
    == GeneratorSymbol(
      family="η",
      index=11,
    )
  )

  assert (
    eta_12.dimension
    == 12
  )

  assert (
    eta_12.source
    == 13
  )

  assert (
    eta_12.target
    == 12
  )

  assert (
    eta_12.generator
    == GeneratorSymbol(
      family="η",
      index=12,
    )
  )

  assert (
    relation.rhs
    == Zero()
  )


def test_phase73_7b_reuses_phase71_n5_injectivity():
  data = build_phase73_7b_data()

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
        "pi12_11"
      ],
      target_group=data[
        "pi10_5"
      ],
    )
  )


def test_phase73_7b_three_exactness_windows_are_derived():
  data = build_phase73_7b_data()

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


def test_phase73_7b_structural_windows_remain_given():
  data = build_phase73_7b_data()

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


def test_phase73_7b_suspension_is_injective():
  data = build_phase73_7b_data()

  assert (
    data[
      "injectivity_step"
    ].conclusion
    == TodaSuspensionInjectiveStatement(
      map=TodaSuspensionMap(
        source_group=data[
          "pi11_5"
        ],
        target_group=data[
          "pi12_6"
        ],
      )
    )
  )

  assert (
    data[
      "injectivity_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_7b_hopf_is_zero():
  data = build_phase73_7b_data()

  assert (
    data[
      "hopf_zero_step"
    ].conclusion
    == TodaHopfInvariantZeroStatement(
      map=TodaHopfInvariantMap(
        source_group=data[
          "pi12_6"
        ],
        target_group=data[
          "pi12_11"
        ],
      )
    )
  )


def test_phase73_7b_suspension_is_surjective():
  data = build_phase73_7b_data()

  assert (
    data[
      "surjectivity_step"
    ].conclusion
    == TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=data[
          "pi11_5"
        ],
        target_group=data[
          "pi12_6"
        ],
      )
    )
  )


def test_phase73_7b_suspension_is_isomorphism():
  data = build_phase73_7b_data()

  assert (
    data[
      "isomorphism_step"
    ].conclusion
    == TodaSuspensionIsomorphismStatement(
      map=TodaSuspensionMap(
        source_group=data[
          "pi11_5"
        ],
        target_group=data[
          "pi12_6"
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


def test_phase73_7b_isomorphism_uses_injective_and_surjective():
  data = build_phase73_7b_data()

  assert (
    data[
      "isomorphism_step"
    ].premises
    == (
      data[
        "injectivity_step"
      ],
      data[
        "surjectivity_step"
      ],
    )
  )


def test_phase73_7b_nu6_squared_is_composition():
  data = build_phase73_7b_data()

  assert (
    data[
      "nu6_squared"
    ]
    == Composition(
      left=data[
        "nu_6"
      ],
      right=data[
        "nu_9"
      ],
    )
  )

  assert (
    data[
      "nu6_squared"
    ].is_type_compatible()
  )


def test_phase73_7b_derives_pi12_6():
  data = build_phase73_7b_data()

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


def test_phase73_7b_pi12_6_is_order_two():
  data = build_phase73_7b_data()

  group = (
    data[
      "final_step"
    ].conclusion.rhs
  )

  assert (
    group.order
    == 2
  )

  assert (
    group.generator
    == data[
      "nu6_squared"
    ]
  )


def test_phase73_7b_final_uses_exact_two_dependencies():
  data = build_phase73_7b_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi11_5_step"
      ],
      data[
        "isomorphism_step"
      ],
    )
  )


def test_phase73_7b_rejects_given_pi11_5():
  data = build_phase73_7b_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi11_5_step"
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


def test_phase73_7b_rejects_wrong_pi11_5_order():
  data = build_phase73_7b_data()

  relation = (
    data[
      "pi11_5_step"
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


def test_phase73_7b_rejects_given_isomorphism():
  data = build_phase73_7b_data()

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
        "pi11_5_step"
      ],
      given,
    ),
  ) is None


def test_phase73_7b_final_is_not_given():
  data = build_phase73_7b_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


