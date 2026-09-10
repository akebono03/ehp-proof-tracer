from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  TodaPrimaryGroup,
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
from test_phase63_toda56_integration import (
  build_phase63_6_data,
)
from test_phase70_pi8_3_nu_prime_eta6_squared import (
  build_phase70_3_data,
)
from toda_rules import (
  Toda56Nu4DecompositionStatement,
  TodaProp53FiniteDimensionalStatement,
  toda_prop59_e_nu_prime_eta6_squared_bridge_inference_rule,
  toda_prop59_pi9_4_decomposition_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase70_4_data():
  phase70_3 = (
    build_phase70_3_data()
  )

  phase59_8 = (
    build_phase59_8_data()
  )

  phase63_6 = (
    build_phase63_6_data()
  )

  pi8_3_step = (
    phase70_3[
      "final_step"
    ]
  )

  prop53_step = (
    phase59_8[
      "integration_step"
    ]
  )

  toda56_step = (
    phase63_6[
      "integration_step"
    ]
  )

  bridge_rule = (
    toda_prop59_e_nu_prime_eta6_squared_bridge_inference_rule()
  )

  decomposition_rule = (
    toda_prop59_pi9_4_decomposition_inference_rule()
  )

  bridge_match = find_inference_match(
    bridge_rule,
    (
      pi8_3_step,
      prop53_step,
    ),
  )

  assert bridge_match is not None

  bridge_step = (
    apply_inference_match(
      bridge_match
    )
  )

  decomposition_match = find_inference_match(
    decomposition_rule,
    (
      toda56_step,
      pi8_3_step,
      prop53_step,
      bridge_step,
    ),
  )

  assert decomposition_match is not None

  final_step = (
    apply_inference_match(
      decomposition_match
    )
  )

  nu_prime_eta6_squared = (
    pi8_3_step
    .conclusion
    .rhs
    .generator
  )

  nu_prime = (
    nu_prime_eta6_squared.left
  )

  eta6_squared = (
    nu_prime_eta6_squared.right
  )

  eta_6 = (
    eta6_squared.left
  )

  eta_7 = (
    eta6_squared.right
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

  eta7_squared = Composition(
    left=eta_7,
    right=eta_8,
  )

  e_nu_prime_eta7_squared = (
    Composition(
      left=Suspension(
        expression=nu_prime,
      ),
      right=eta7_squared,
    )
  )

  expected_bridge = Relation(
    lhs=Suspension(
      expression=nu_prime_eta6_squared,
    ),
    rhs=e_nu_prime_eta7_squared,
    relation_type=RelationType.EQUALITY,
  )

  nu_4 = (
    toda56_step
    .conclusion
    .lemma54_statement
    .nu4
  )

  nu4_eta7_squared = Composition(
    left=nu_4,
    right=eta7_squared,
  )

  expected_final = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=4,
    ),
    rhs=DirectSumGroup(
      summands=(
        FiniteCyclicGroup(
          order=2,
          generator=nu4_eta7_squared,
        ),
        FiniteCyclicGroup(
          order=2,
          generator=e_nu_prime_eta7_squared,
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    bridge_step.conclusion
    == expected_bridge
  )

  assert (
    final_step.conclusion
    == expected_final
  )

  return {
    "phase70_3": phase70_3,
    "phase59_8": phase59_8,
    "phase63_6": phase63_6,
    "pi8_3_step": pi8_3_step,
    "prop53_step": prop53_step,
    "toda56_step": toda56_step,
    "bridge_rule": bridge_rule,
    "decomposition_rule": (
      decomposition_rule
    ),
    "bridge_match": bridge_match,
    "bridge_step": bridge_step,
    "decomposition_match": (
      decomposition_match
    ),
    "final_step": final_step,
    "nu_prime_eta6_squared": (
      nu_prime_eta6_squared
    ),
    "nu_prime": nu_prime,
    "eta6_squared": eta6_squared,
    "eta_6": eta_6,
    "eta_7": eta_7,
    "eta_8": eta_8,
    "eta7_squared": eta7_squared,
    "e_nu_prime_eta7_squared": (
      e_nu_prime_eta7_squared
    ),
    "expected_bridge": expected_bridge,
    "nu_4": nu_4,
    "nu4_eta7_squared": (
      nu4_eta7_squared
    ),
    "expected_final": expected_final,
  }


def test_phase70_4_reuses_phase70_3_pi8_3():
  data = build_phase70_4_data()

  assert (
    data[
      "pi8_3_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi8_3_step"
    ].conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=3,
    )
  )


def test_phase70_4_reuses_derived_prop53():
  data = build_phase70_4_data()

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


def test_phase70_4_reuses_derived_toda56():
  data = build_phase70_4_data()

  assert isinstance(
    data[
      "toda56_step"
    ].conclusion,
    Toda56Nu4DecompositionStatement,
  )

  assert (
    data[
      "toda56_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_4_source_generator_is_nu_prime_eta6_squared():
  data = build_phase70_4_data()

  generator = (
    data[
      "nu_prime_eta6_squared"
    ]
  )

  assert isinstance(
    generator,
    Composition,
  )

  assert (
    generator.left
    is data[
      "nu_prime"
    ]
  )

  assert (
    generator.right
    is data[
      "eta6_squared"
    ]
  )


def test_phase70_4_eta6_squared_is_right_associated():
  data = build_phase70_4_data()

  assert (
    data[
      "eta6_squared"
    ]
    == Composition(
      left=data[
        "eta_6"
      ],
      right=data[
        "eta_7"
      ],
    )
  )


def test_phase70_4_eta7_squared_is_composition():
  data = build_phase70_4_data()

  assert (
    data[
      "eta7_squared"
    ]
    == Composition(
      left=data[
        "eta_7"
      ],
      right=data[
        "eta_8"
      ],
    )
  )


def test_phase70_4_bridge_matches_dependencies():
  data = build_phase70_4_data()

  assert (
    data[
      "bridge_match"
    ]
    is not None
  )


def test_phase70_4_derives_suspension_bridge():
  data = build_phase70_4_data()

  assert (
    data[
      "bridge_step"
    ].conclusion
    == data[
      "expected_bridge"
    ]
  )

  assert (
    data[
      "bridge_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_4_bridge_is_expected_formula():
  data = build_phase70_4_data()

  assert (
    data[
      "bridge_step"
    ].conclusion.lhs
    == Suspension(
      expression=data[
        "nu_prime_eta6_squared"
      ],
    )
  )

  assert (
    data[
      "bridge_step"
    ].conclusion.rhs
    == Composition(
      left=Suspension(
        expression=data[
          "nu_prime"
        ],
      ),
      right=data[
        "eta7_squared"
      ],
    )
  )


def test_phase70_4_bridge_uses_exact_two_dependencies():
  data = build_phase70_4_data()

  assert (
    data[
      "bridge_step"
    ].premises
    == (
      data[
        "pi8_3_step"
      ],
      data[
        "prop53_step"
      ],
    )
  )


def test_phase70_4_decomposition_matches_dependencies():
  data = build_phase70_4_data()

  assert (
    data[
      "decomposition_match"
    ]
    is not None
  )


def test_phase70_4_final_is_pi9_4():
  data = build_phase70_4_data()

  assert (
    data[
      "final_step"
    ].conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=4,
    )
  )


def test_phase70_4_final_is_direct_sum():
  data = build_phase70_4_data()

  group = (
    data[
      "final_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    DirectSumGroup,
  )

  assert len(
    group.summands
  ) == 2


def test_phase70_4_first_summand_is_nu4_eta7_squared():
  data = build_phase70_4_data()

  first = (
    data[
      "final_step"
    ].conclusion
    .rhs
    .summands[
      0
    ]
  )

  assert isinstance(
    first,
    FiniteCyclicGroup,
  )

  assert first.order == 2

  assert (
    first.generator
    == data[
      "nu4_eta7_squared"
    ]
  )


def test_phase70_4_second_summand_is_e_nu_prime_eta7_squared():
  data = build_phase70_4_data()

  second = (
    data[
      "final_step"
    ].conclusion
    .rhs
    .summands[
      1
    ]
  )

  assert isinstance(
    second,
    FiniteCyclicGroup,
  )

  assert second.order == 2

  assert (
    second.generator
    == data[
      "e_nu_prime_eta7_squared"
    ]
  )


def test_phase70_4_derives_expected_decomposition():
  data = build_phase70_4_data()

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


def test_phase70_4_final_uses_exact_four_dependencies():
  data = build_phase70_4_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "toda56_step"
      ],
      data[
        "pi8_3_step"
      ],
      data[
        "prop53_step"
      ],
      data[
        "bridge_step"
      ],
    )
  )


def test_phase70_4_bridge_rejects_given_pi8_3():
  data = build_phase70_4_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi8_3_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "bridge_rule"
    ],
    (
      given,
      data[
        "prop53_step"
      ],
    ),
  ) is None


def test_phase70_4_bridge_rejects_given_prop53():
  data = build_phase70_4_data()

  given = ProofStep(
    conclusion=(
      data[
        "prop53_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "bridge_rule"
    ],
    (
      data[
        "pi8_3_step"
      ],
      given,
    ),
  ) is None


def test_phase70_4_decomposition_rejects_given_toda56():
  data = build_phase70_4_data()

  given = ProofStep(
    conclusion=(
      data[
        "toda56_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "decomposition_rule"
    ],
    (
      given,
      data[
        "pi8_3_step"
      ],
      data[
        "prop53_step"
      ],
      data[
        "bridge_step"
      ],
    ),
  ) is None


def test_phase70_4_decomposition_rejects_given_pi8_3():
  data = build_phase70_4_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi8_3_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "decomposition_rule"
    ],
    (
      data[
        "toda56_step"
      ],
      given,
      data[
        "prop53_step"
      ],
      data[
        "bridge_step"
      ],
    ),
  ) is None


def test_phase70_4_decomposition_rejects_given_prop53():
  data = build_phase70_4_data()

  given = ProofStep(
    conclusion=(
      data[
        "prop53_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "decomposition_rule"
    ],
    (
      data[
        "toda56_step"
      ],
      data[
        "pi8_3_step"
      ],
      given,
      data[
        "bridge_step"
      ],
    ),
  ) is None


def test_phase70_4_decomposition_rejects_given_bridge():
  data = build_phase70_4_data()

  given = ProofStep(
    conclusion=(
      data[
        "bridge_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "decomposition_rule"
    ],
    (
      data[
        "toda56_step"
      ],
      data[
        "pi8_3_step"
      ],
      data[
        "prop53_step"
      ],
      given,
    ),
  ) is None


def test_phase70_4_rejects_wrong_bridge_eta8():
  data = build_phase70_4_data()

  eta_9 = HomotopyElement(
    name="η₉",
    dimension=9,
    source=10,
    target=9,
    generator=GeneratorSymbol(
      family="η",
      index=9,
    ),
  )

  wrong_bridge = replace(
    data[
      "bridge_step"
    ].conclusion,
    rhs=Composition(
      left=Suspension(
        expression=data[
          "nu_prime"
        ],
      ),
      right=Composition(
        left=data[
          "eta_7"
        ],
        right=eta_9,
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_bridge,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "decomposition_rule"
    ],
    (
      data[
        "toda56_step"
      ],
      data[
        "pi8_3_step"
      ],
      data[
        "prop53_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase70_4_final_is_not_given():
  data = build_phase70_4_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )

  initial_steps = (
    data[
      "toda56_step"
    ],
    data[
      "pi8_3_step"
    ],
    data[
      "prop53_step"
    ],
  )

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step in initial_steps
    )
  )


def test_phase70_4_uses_staged_one_shot_inference():
  data = build_phase70_4_data()

  assert (
    data[
      "bridge_match"
    ]
    is not None
  )

  assert (
    data[
      "decomposition_match"
    ]
    is not None
  )

  assert (
    data[
      "bridge_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


