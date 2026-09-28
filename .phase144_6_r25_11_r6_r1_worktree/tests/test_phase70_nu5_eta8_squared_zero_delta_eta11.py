from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Suspension,
  Zero,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from test_phase68_nu_n_eta_n_plus_three_zero import (
  build_phase68_9_data,
)
from test_phase69_delta_iota11 import (
  build_phase69_3_data,
)
from test_phase70_pi10_5_nu5_eta8_squared import (
  build_phase70_6_data,
)
from toda_rules import (
  toda_prop59_delta_eta11_inference_rule,
  toda_prop59_e_nu5_eta8_squared_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase70_7_data():
  phase70_6 = (
    build_phase70_6_data()
  )

  phase68_9 = (
    build_phase68_9_data()
  )

  phase69_3 = (
    build_phase69_3_data()
  )

  pi10_5_step = (
    phase70_6[
      "final_step"
    ]
  )

  nu6_eta9_zero_step = (
    phase68_9[
      "nu6_eta9_zero_step"
    ]
  )

  delta_iota11_step = (
    phase69_3[
      "final_step"
    ]
  )

  suspension_zero_rule = (
    toda_prop59_e_nu5_eta8_squared_zero_inference_rule()
  )

  delta_eta11_rule = (
    toda_prop59_delta_eta11_inference_rule()
  )

  suspension_zero_match = (
    find_inference_match(
      suspension_zero_rule,
      (
        pi10_5_step,
        nu6_eta9_zero_step,
      ),
    )
  )

  assert (
    suspension_zero_match
    is not None
  )

  suspension_zero_step = (
    apply_inference_match(
      suspension_zero_match
    )
  )

  delta_eta11_match = (
    find_inference_match(
      delta_eta11_rule,
      (
        delta_iota11_step,
        pi10_5_step,
      ),
    )
  )

  assert (
    delta_eta11_match
    is not None
  )

  delta_eta11_step = (
    apply_inference_match(
      delta_eta11_match
    )
  )

  pi10_5 = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=5,
  )

  nu5_eta8_squared = (
    pi10_5_step
    .conclusion
    .rhs
    .generator
  )

  nu_5 = (
    nu5_eta8_squared.left
  )

  eta8_squared = (
    nu5_eta8_squared.right
  )

  eta_8 = (
    eta8_squared.left
  )

  eta_9 = (
    eta8_squared.right
  )

  expected_suspension_zero = Relation(
    lhs=Suspension(
      expression=nu5_eta8_squared,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  eta_11 = HomotopyElement(
    name="η₁₁",
    dimension=11,
    source=12,
    target=11,
    generator=GeneratorSymbol(
      family="η",
      index=11,
    ),
  )

  expected_delta_eta11 = Relation(
    lhs=MapApplication(
      map=EHP_DELTA_MAP,
      expression=eta_11,
    ),
    rhs=nu5_eta8_squared,
    relation_type=RelationType.EQUALITY,
  )

  assert (
    suspension_zero_step.conclusion
    == expected_suspension_zero
  )

  assert (
    delta_eta11_step.conclusion
    == expected_delta_eta11
  )

  return {
    "phase70_6": phase70_6,
    "phase68_9": phase68_9,
    "phase69_3": phase69_3,
    "pi10_5_step": pi10_5_step,
    "nu6_eta9_zero_step": (
      nu6_eta9_zero_step
    ),
    "delta_iota11_step": (
      delta_iota11_step
    ),
    "suspension_zero_rule": (
      suspension_zero_rule
    ),
    "delta_eta11_rule": (
      delta_eta11_rule
    ),
    "suspension_zero_match": (
      suspension_zero_match
    ),
    "suspension_zero_step": (
      suspension_zero_step
    ),
    "delta_eta11_match": (
      delta_eta11_match
    ),
    "delta_eta11_step": (
      delta_eta11_step
    ),
    "pi10_5": pi10_5,
    "nu5_eta8_squared": (
      nu5_eta8_squared
    ),
    "nu_5": nu_5,
    "eta8_squared": eta8_squared,
    "eta_8": eta_8,
    "eta_9": eta_9,
    "eta_11": eta_11,
    "expected_suspension_zero": (
      expected_suspension_zero
    ),
    "expected_delta_eta11": (
      expected_delta_eta11
    ),
  }


def test_phase70_7_reuses_phase70_6_pi10_5():
  data = build_phase70_7_data()

  assert (
    data[
      "pi10_5_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi10_5_step"
    ].conclusion.lhs
    == data[
      "pi10_5"
    ]
  )


def test_phase70_7_pi10_5_is_order_two():
  data = build_phase70_7_data()

  group = (
    data[
      "pi10_5_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert (
    group.order
    == 2
  )


def test_phase70_7_generator_is_nu5_eta8_squared():
  data = build_phase70_7_data()

  generator = (
    data[
      "nu5_eta8_squared"
    ]
  )

  assert isinstance(
    generator,
    Composition,
  )

  assert (
    generator.left
    is data[
      "nu_5"
    ]
  )

  assert (
    generator.right
    is data[
      "eta8_squared"
    ]
  )


def test_phase70_7_eta8_squared_is_right_associated():
  data = build_phase70_7_data()

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


def test_phase70_7_reuses_phase68_nu6_eta9_zero():
  data = build_phase70_7_data()

  assert (
    data[
      "nu6_eta9_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "nu6_eta9_zero_step"
    ].conclusion.relation_type
    == RelationType.ZERO
  )

  assert (
    data[
      "nu6_eta9_zero_step"
    ].conclusion.rhs
    == Zero()
  )


def test_phase70_7_nu6_eta9_zero_uses_same_eta9():
  data = build_phase70_7_data()

  zero_expression = (
    data[
      "nu6_eta9_zero_step"
    ].conclusion.lhs
  )

  assert isinstance(
    zero_expression,
    Composition,
  )

  zero_eta_9 = (
    zero_expression.right
  )

  eta_9 = (
    data[
      "eta_9"
    ]
  )

  assert isinstance(
    zero_eta_9,
    HomotopyElement,
  )

  assert (
    zero_eta_9.dimension
    == eta_9.dimension
  )

  assert (
    zero_eta_9.source
    == eta_9.source
  )

  assert (
    zero_eta_9.target
    == eta_9.target
  )

  assert (
    zero_eta_9.generator
    == eta_9.generator
  )

  assert (
    zero_eta_9.generator
    == GeneratorSymbol(
      family="η",
      index=9,
    )
  )


def test_phase70_7_suspension_zero_matches():
  data = build_phase70_7_data()

  assert (
    data[
      "suspension_zero_match"
    ]
    is not None
  )


def test_phase70_7_derives_suspension_zero():
  data = build_phase70_7_data()

  assert (
    data[
      "suspension_zero_step"
    ].conclusion
    == data[
      "expected_suspension_zero"
    ]
  )

  assert (
    data[
      "suspension_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_7_suspension_zero_argument_is_phase70_6_generator():
  data = build_phase70_7_data()

  assert (
    data[
      "suspension_zero_step"
    ].conclusion.lhs
    == Suspension(
      expression=data[
        "nu5_eta8_squared"
      ],
    )
  )


def test_phase70_7_suspension_zero_uses_exact_two_dependencies():
  data = build_phase70_7_data()

  assert (
    data[
      "suspension_zero_step"
    ].premises
    == (
      data[
        "pi10_5_step"
      ],
      data[
        "nu6_eta9_zero_step"
      ],
    )
  )


def test_phase70_7_reuses_phase69_delta_iota11():
  data = build_phase70_7_data()

  assert (
    data[
      "delta_iota11_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "delta_iota11_step"
    ].conclusion.lhs.map
    == EHP_DELTA_MAP
  )


def test_phase70_7_phase69_value_is_nu5_eta8():
  data = build_phase70_7_data()

  value = (
    data[
      "delta_iota11_step"
    ].conclusion.rhs
  )

  assert isinstance(
    value,
    Composition,
  )

  assert (
    value.left
    == data[
      "nu_5"
    ]
  )

  assert (
    value.right
    == data[
      "eta_8"
    ]
  )


def test_phase70_7_delta_eta11_matches():
  data = build_phase70_7_data()

  assert (
    data[
      "delta_eta11_match"
    ]
    is not None
  )


def test_phase70_7_derives_delta_eta11():
  data = build_phase70_7_data()

  assert (
    data[
      "delta_eta11_step"
    ].conclusion
    == data[
      "expected_delta_eta11"
    ]
  )

  assert (
    data[
      "delta_eta11_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_7_delta_eta11_argument_is_eta11():
  data = build_phase70_7_data()

  assert (
    data[
      "delta_eta11_step"
    ].conclusion.lhs
    == MapApplication(
      map=EHP_DELTA_MAP,
      expression=data[
        "eta_11"
      ],
    )
  )


def test_phase70_7_delta_eta11_value_reuses_phase70_6_generator():
  data = build_phase70_7_data()

  assert (
    data[
      "delta_eta11_step"
    ].conclusion.rhs
    is data[
      "pi10_5_step"
    ].conclusion.rhs.generator
  )

  assert (
    data[
      "delta_eta11_step"
    ].conclusion.rhs
    == data[
      "nu5_eta8_squared"
    ]
  )


def test_phase70_7_delta_eta11_uses_exact_two_dependencies():
  data = build_phase70_7_data()

  assert (
    data[
      "delta_eta11_step"
    ].premises
    == (
      data[
        "delta_iota11_step"
      ],
      data[
        "pi10_5_step"
      ],
    )
  )


def test_phase70_7_suspension_zero_rejects_given_pi10_5():
  data = build_phase70_7_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi10_5_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "suspension_zero_rule"
    ],
    (
      given,
      data[
        "nu6_eta9_zero_step"
      ],
    ),
  ) is None


def test_phase70_7_suspension_zero_rejects_given_nu6_eta9_zero():
  data = build_phase70_7_data()

  given = ProofStep(
    conclusion=(
      data[
        "nu6_eta9_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "suspension_zero_rule"
    ],
    (
      data[
        "pi10_5_step"
      ],
      given,
    ),
  ) is None


def test_phase70_7_delta_eta11_rejects_given_delta_iota11():
  data = build_phase70_7_data()

  given = ProofStep(
    conclusion=(
      data[
        "delta_iota11_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "delta_eta11_rule"
    ],
    (
      given,
      data[
        "pi10_5_step"
      ],
    ),
  ) is None


def test_phase70_7_delta_eta11_rejects_given_pi10_5():
  data = build_phase70_7_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi10_5_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "delta_eta11_rule"
    ],
    (
      data[
        "delta_iota11_step"
      ],
      given,
    ),
  ) is None


def test_phase70_7_delta_eta11_rejects_wrong_target_order():
  data = build_phase70_7_data()

  wrong_relation = replace(
    data[
      "pi10_5_step"
    ].conclusion,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=data[
        "nu5_eta8_squared"
      ],
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "delta_eta11_rule"
    ],
    (
      data[
        "delta_iota11_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase70_7_delta_eta11_rejects_wrong_eta9():
  data = build_phase70_7_data()

  wrong_eta_10 = HomotopyElement(
    name="η₁₀",
    dimension=10,
    source=11,
    target=10,
    generator=GeneratorSymbol(
      family="η",
      index=10,
    ),
  )

  wrong_generator = Composition(
    left=data[
      "nu_5"
    ],
    right=Composition(
      left=data[
        "eta_8"
      ],
      right=wrong_eta_10,
    ),
  )

  wrong_relation = replace(
    data[
      "pi10_5_step"
    ].conclusion,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=wrong_generator,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "delta_eta11_rule"
    ],
    (
      data[
        "delta_iota11_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase70_7_results_are_not_given():
  data = build_phase70_7_data()

  assert (
    data[
      "suspension_zero_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "delta_eta11_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase70_7_uses_staged_one_shot_inference():
  data = build_phase70_7_data()

  assert (
    data[
      "suspension_zero_match"
    ]
    is not None
  )

  assert (
    data[
      "delta_eta11_match"
    ]
    is not None
  )

  assert (
    data[
      "suspension_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "delta_eta11_step"
    ].rule
    == ProofRule.INFERENCE
  )




