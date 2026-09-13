from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  Multiple,
)
from homotopy_groups import (
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
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from test_phase71_toda512_n4_delta_injective import (
  build_phase71_2_data,
)
from test_phase73_pi10_4_nu4_squared import (
  build_phase73_5_data,
)
from test_phase73_513_delta_nu9 import (
  build_phase73_6a_data,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaDeltaInjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaProp42ExactnessStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaSuspensionSurjectiveStatement,
  toda_nu_family_definition_statement,
  toda_prop511_pi11_5_concrete_exactness_inference_rule,
  toda_prop511_pi11_5_hopf_zero_inference_rule,
  toda_prop511_pi11_5_nu5_squared_inference_rule,
  toda_prop511_pi11_5_suspension_surjective_inference_rule,
  toda_prop511_pi12_9_nu9_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase73_7a_data():
  phase65 = (
    build_phase65_9_data()
  )

  phase71 = (
    build_phase71_2_data()
  )

  phase73_5 = (
    build_phase73_5_data()
  )

  phase73_6a = (
    build_phase73_6a_data()
  )

  prop56_step = (
    phase65[
      "integration_step"
    ]
  )

  delta_injective_step = (
    phase71[
      "final_step"
    ]
  )

  pi10_4_step = (
    phase73_5[
      "final_step"
    ]
  )

  delta_nu9_step = (
    phase73_6a[
      "final_step"
    ]
  )

  pi12_9_rule = (
    toda_prop511_pi12_9_nu9_inference_rule()
  )

  pi12_9_match = find_inference_match(
    pi12_9_rule,
    (
      prop56_step,
    ),
  )

  assert (
    pi12_9_match
    is not None
  )

  pi12_9_step = apply_inference_match(
    pi12_9_match
  )

  pi12_9 = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=9,
  )

  pi10_4 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=4,
  )

  pi11_5 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=5,
  )

  pi11_9 = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=9,
  )

  pi9_4 = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=4,
  )

  delta_e_window = (
    TodaEHPExactnessWindow(
      source_term=pi12_9,
      middle_term=pi10_4,
      target_term=pi11_5,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    )
  )

  e_h_window = (
    TodaEHPExactnessWindow(
      source_term=pi10_4,
      middle_term=pi11_5,
      target_term=pi11_9,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    )
  )

  h_delta_window = (
    TodaEHPExactnessWindow(
      source_term=pi11_5,
      middle_term=pi11_9,
      target_term=pi9_4,
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
    toda_prop511_pi11_5_concrete_exactness_inference_rule()
  )

  delta_e_exactness_match = (
    find_inference_match(
      exactness_rule,
      (
        delta_e_window_step,
      ),
    )
  )

  assert (
    delta_e_exactness_match
    is not None
  )

  delta_e_exactness_step = (
    apply_inference_match(
      delta_e_exactness_match
    )
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

  hopf_zero_rule = (
    toda_prop511_pi11_5_hopf_zero_inference_rule()
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

  suspension_surjective_rule = (
    toda_prop511_pi11_5_suspension_surjective_inference_rule()
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

  final_rule = (
    toda_prop511_pi11_5_nu5_squared_inference_rule()
  )

  final_premise_steps = (
    pi12_9_step,
    pi10_4_step,
    delta_nu9_step,
    delta_e_exactness_step,
    suspension_surjective_step,
  )

  final_match = find_inference_match(
    final_rule,
    final_premise_steps,
  )

  assert (
    final_match
    is not None
  )

  final_step = apply_inference_match(
    final_match
  )

  nu_5 = (
    toda_nu_family_definition_statement(
      5
    ).element
  )

  nu_8 = (
    toda_nu_family_definition_statement(
      8
    ).element
  )

  nu5_squared = Composition(
    left=nu_5,
    right=nu_8,
  )

  expected_statement = Relation(
    lhs=pi11_5,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=nu5_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  return {
    "phase65": phase65,
    "phase71": phase71,
    "phase73_5": phase73_5,
    "phase73_6a": phase73_6a,
    "prop56_step": prop56_step,
    "delta_injective_step": (
      delta_injective_step
    ),
    "pi10_4_step": pi10_4_step,
    "delta_nu9_step": delta_nu9_step,
    "pi12_9_rule": pi12_9_rule,
    "pi12_9_step": pi12_9_step,
    "pi12_9": pi12_9,
    "pi10_4": pi10_4,
    "pi11_5": pi11_5,
    "pi11_9": pi11_9,
    "pi9_4": pi9_4,
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
    "hopf_zero_step": hopf_zero_step,
    "suspension_surjective_step": (
      suspension_surjective_step
    ),
    "exactness_rule": exactness_rule,
    "hopf_zero_rule": hopf_zero_rule,
    "suspension_surjective_rule": (
      suspension_surjective_rule
    ),
    "final_rule": final_rule,
    "final_premise_steps": (
      final_premise_steps
    ),
    "nu_5": nu_5,
    "nu_8": nu_8,
    "nu5_squared": nu5_squared,
    "expected_statement": (
      expected_statement
    ),
    "final_step": final_step,
  }


def test_phase73_7a_reuses_derived_prop56():
  data = build_phase73_7a_data()

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


def test_phase73_7a_derives_pi12_9():
  data = build_phase73_7a_data()

  relation = (
    data[
      "pi12_9_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == data[
      "pi12_9"
    ]
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 8
  )

  assert (
    relation.rhs.generator
    == toda_nu_family_definition_statement(
      9
    ).element
  )

  assert (
    data[
      "pi12_9_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_7a_reuses_pi10_4():
  data = build_phase73_7a_data()

  assert (
    data[
      "pi10_4_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi10_4_step"
    ].conclusion.rhs.order
    == 8
  )


def test_phase73_7a_reuses_delta_nu9():
  data = build_phase73_7a_data()

  assert isinstance(
    data[
      "delta_nu9_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )

  assert (
    data[
      "delta_nu9_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_7a_delta_nu9_value_is_twice_nu4_squared():
  data = build_phase73_7a_data()

  statement = (
    data[
      "delta_nu9_step"
    ].conclusion
  )

  assert (
    statement.positive_value
    == Multiple(
      coefficient=2,
      expression=(
        data[
          "pi10_4_step"
        ].conclusion
        .rhs
        .generator
      ),
    )
  )


def test_phase73_7a_reuses_phase71_n4_injectivity():
  data = build_phase73_7a_data()

  assert isinstance(
    data[
      "delta_injective_step"
    ].conclusion,
    TodaDeltaInjectiveStatement,
  )

  assert (
    data[
      "delta_injective_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "delta_injective_step"
    ].conclusion.map
    == TodaDeltaMap(
      source_group=data[
        "pi11_9"
      ],
      target_group=data[
        "pi9_4"
      ],
    )
  )


def test_phase73_7a_three_exactness_windows_are_derived():
  data = build_phase73_7a_data()

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


def test_phase73_7a_structural_windows_remain_given():
  data = build_phase73_7a_data()

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


def test_phase73_7a_hopf_zero_is_derived():
  data = build_phase73_7a_data()

  assert (
    data[
      "hopf_zero_step"
    ].conclusion
    == TodaHopfInvariantZeroStatement(
      map=TodaHopfInvariantMap(
        source_group=data[
          "pi11_5"
        ],
        target_group=data[
          "pi11_9"
        ],
      )
    )
  )

  assert (
    data[
      "hopf_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_7a_hopf_zero_uses_phase71_injectivity():
  data = build_phase73_7a_data()

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


def test_phase73_7a_suspension_is_surjective():
  data = build_phase73_7a_data()

  assert isinstance(
    data[
      "suspension_surjective_step"
    ].conclusion,
    TodaSuspensionSurjectiveStatement,
  )

  assert (
    data[
      "suspension_surjective_step"
    ].conclusion.map
    == TodaSuspensionMap(
      source_group=data[
        "pi10_4"
      ],
      target_group=data[
        "pi11_5"
      ],
    )
  )


def test_phase73_7a_nu5_squared_is_composition():
  data = build_phase73_7a_data()

  assert (
    data[
      "nu5_squared"
    ]
    == Composition(
      left=data[
        "nu_5"
      ],
      right=data[
        "nu_8"
      ],
    )
  )

  assert (
    data[
      "nu5_squared"
    ].is_type_compatible()
  )


def test_phase73_7a_derives_pi11_5():
  data = build_phase73_7a_data()

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


def test_phase73_7a_pi11_5_is_order_two():
  data = build_phase73_7a_data()

  group = (
    data[
      "final_step"
    ].conclusion
    .rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert (
    group.order
    == 2
  )

  assert (
    group.generator
    == data[
      "nu5_squared"
    ]
  )


def test_phase73_7a_final_uses_exact_five_dependencies():
  data = build_phase73_7a_data()

  assert (
    data[
      "final_step"
    ].premises
    == data[
      "final_premise_steps"
    ]
  )

  assert (
    len(
      data[
        "final_step"
      ].premises
    )
    == 5
  )


def test_phase73_7a_rejects_given_pi12_9():
  data = build_phase73_7a_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi12_9_step"
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
        "pi10_4_step"
      ],
      data[
        "delta_nu9_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
      data[
        "suspension_surjective_step"
      ],
    ),
  ) is None


def test_phase73_7a_rejects_wrong_pi10_4_order():
  data = build_phase73_7a_data()

  relation = (
    data[
      "pi10_4_step"
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
      data[
        "pi12_9_step"
      ],
      wrong,
      data[
        "delta_nu9_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
      data[
        "suspension_surjective_step"
      ],
    ),
  ) is None


def test_phase73_7a_rejects_wrong_delta_coefficient():
  data = build_phase73_7a_data()

  statement = (
    data[
      "delta_nu9_step"
    ].conclusion
  )

  wrong_statement = replace(
    statement,
    positive_value=Multiple(
      coefficient=4,
      expression=(
        statement
        .positive_value
        .expression
      ),
    ),
  )

  wrong = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "pi12_9_step"
      ],
      data[
        "pi10_4_step"
      ],
      wrong,
      data[
        "delta_e_exactness_step"
      ],
      data[
        "suspension_surjective_step"
      ],
    ),
  ) is None


def test_phase73_7a_rejects_given_surjectivity():
  data = build_phase73_7a_data()

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
        "pi12_9_step"
      ],
      data[
        "pi10_4_step"
      ],
      data[
        "delta_nu9_step"
      ],
      data[
        "delta_e_exactness_step"
      ],
      given,
    ),
  ) is None


def test_phase73_7a_final_is_not_given():
  data = build_phase73_7a_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


