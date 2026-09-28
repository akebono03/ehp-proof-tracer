from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from test_phase63_toda56_integration import (
  build_phase63_6_data,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from test_phase73_pi9_3_zero import (
  build_phase73_4_data,
)
from toda_rules import (
  Toda56Nu4DecompositionStatement,
  TodaProp56FiniteDimensionalStatement,
  toda_nu_family_definition_statement,
  toda_prop511_pi10_4_nu4_squared_inference_rule,
  toda_prop511_pi10_7_nu7_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase73_5_data():
  phase63 = (
    build_phase63_6_data()
  )

  phase65 = (
    build_phase65_9_data()
  )

  phase73_4 = (
    build_phase73_4_data()
  )

  toda56_step = (
    phase63[
      "integration_step"
    ]
  )

  prop56_step = (
    phase65[
      "integration_step"
    ]
  )

  pi9_3_zero_step = (
    phase73_4[
      "final_step"
    ]
  )

  pi10_7_rule = (
    toda_prop511_pi10_7_nu7_inference_rule()
  )

  pi10_7_match = (
    find_inference_match(
      pi10_7_rule,
      (
        prop56_step,
      ),
    )
  )

  assert (
    pi10_7_match
    is not None
  )

  pi10_7_step = (
    apply_inference_match(
      pi10_7_match
    )
  )

  nu_4 = (
    toda56_step
    .conclusion
    .lemma54_statement
    .nu4
  )

  nu_7 = (
    pi10_7_step
    .conclusion
    .rhs
    .generator
  )

  nu4_squared = Composition(
    left=nu_4,
    right=nu_7,
  )

  expected_final = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=4,
    ),
    rhs=FiniteCyclicGroup(
      order=8,
      generator=nu4_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  final_rule = (
    toda_prop511_pi10_4_nu4_squared_inference_rule()
  )

  final_match = (
    find_inference_match(
      final_rule,
      (
        pi9_3_zero_step,
        pi10_7_step,
        toda56_step,
      ),
    )
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
    "phase63": phase63,
    "phase65": phase65,
    "phase73_4": phase73_4,
    "toda56_step": toda56_step,
    "prop56_step": prop56_step,
    "pi9_3_zero_step": (
      pi9_3_zero_step
    ),
    "pi10_7_rule": pi10_7_rule,
    "pi10_7_step": pi10_7_step,
    "nu_4": nu_4,
    "nu_7": nu_7,
    "nu4_squared": nu4_squared,
    "expected_final": expected_final,
    "final_rule": final_rule,
    "final_step": final_step,
  }


def test_phase73_5_reuses_derived_prop56():
  data = build_phase73_5_data()

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


def test_phase73_5_reuses_derived_toda56():
  data = build_phase73_5_data()

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


def test_phase73_5_reuses_pi9_3_zero():
  data = build_phase73_5_data()

  assert (
    data[
      "pi9_3_zero_step"
    ].conclusion
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=3,
      )
    )
  )

  assert (
    data[
      "pi9_3_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_5_derives_pi10_7_from_prop56():
  data = build_phase73_5_data()

  nu_7 = (
    toda_nu_family_definition_statement(
      7
    ).element
  )

  assert (
    data[
      "pi10_7_step"
    ].conclusion
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=7,
      ),
      rhs=FiniteCyclicGroup(
        order=8,
        generator=nu_7,
      ),
      relation_type=(
        RelationType.EQUALITY
      ),
    )
  )

  assert (
    data[
      "pi10_7_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_5_pi10_7_uses_only_prop56():
  data = build_phase73_5_data()

  assert (
    data[
      "pi10_7_step"
    ].premises
    == (
      data[
        "prop56_step"
      ],
    )
  )


def test_phase73_5_nu7_has_correct_typing():
  data = build_phase73_5_data()

  nu_7 = data[
    "nu_7"
  ]

  assert (
    nu_7.source
    == 10
  )

  assert (
    nu_7.target
    == 7
  )

  assert (
    nu_7.generator
    == GeneratorSymbol(
      family="ν",
      index=7,
    )
  )


def test_phase73_5_nu4_has_correct_typing():
  data = build_phase73_5_data()

  assert (
    data[
      "nu_4"
    ]
    == HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
      ),
    )
  )


def test_phase73_5_nu4_squared_is_composition():
  data = build_phase73_5_data()

  assert (
    data[
      "nu4_squared"
    ]
    == Composition(
      left=data[
        "nu_4"
      ],
      right=data[
        "nu_7"
      ],
    )
  )

  assert (
    data[
      "nu4_squared"
    ].is_type_compatible()
  )


def test_phase73_5_derives_pi10_4():
  data = build_phase73_5_data()

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


def test_phase73_5_target_is_pi10_4_order_eight():
  data = build_phase73_5_data()

  relation = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=4,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 8
  )


def test_phase73_5_generator_is_nu4_squared():
  data = build_phase73_5_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == Composition(
      left=data[
        "nu_4"
      ],
      right=data[
        "nu_7"
      ],
    )
  )


def test_phase73_5_final_uses_exact_three_dependencies():
  data = build_phase73_5_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi9_3_zero_step"
      ],
      data[
        "pi10_7_step"
      ],
      data[
        "toda56_step"
      ],
    )
  )


def test_phase73_5_rejects_given_prop56():
  data = build_phase73_5_data()

  given_prop56 = ProofStep(
    conclusion=(
      data[
        "prop56_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "pi10_7_rule"
    ],
    (
      given_prop56,
    ),
  ) is None


def test_phase73_5_rejects_wrong_zero_group():
  data = build_phase73_5_data()

  wrong_zero = ProofStep(
    conclusion=(
      TodaPrimaryGroupZeroStatement(
        group=TodaPrimaryGroup(
          group_dimension=8,
          sphere_dimension=3,
        )
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
      wrong_zero,
      data[
        "pi10_7_step"
      ],
      data[
        "toda56_step"
      ],
    ),
  ) is None


def test_phase73_5_rejects_wrong_pi10_7_order():
  data = build_phase73_5_data()

  wrong_relation = replace(
    data[
      "pi10_7_step"
    ].conclusion,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=data[
        "nu_7"
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
      "final_rule"
    ],
    (
      data[
        "pi9_3_zero_step"
      ],
      wrong_step,
      data[
        "toda56_step"
      ],
    ),
  ) is None


def test_phase73_5_rejects_wrong_pi10_7_generator():
  data = build_phase73_5_data()

  wrong_nu_6 = HomotopyElement(
    name="ν₆",
    dimension=6,
    source=9,
    target=6,
    generator=GeneratorSymbol(
      family="ν",
      index=6,
    ),
  )

  wrong_relation = replace(
    data[
      "pi10_7_step"
    ].conclusion,
    rhs=FiniteCyclicGroup(
      order=8,
      generator=wrong_nu_6,
    ),
  )

  wrong_step = ProofStep(
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
        "pi9_3_zero_step"
      ],
      wrong_step,
      data[
        "toda56_step"
      ],
    ),
  ) is None


def test_phase73_5_rejects_given_toda56():
  data = build_phase73_5_data()

  given_toda56 = ProofStep(
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
      "final_rule"
    ],
    (
      data[
        "pi9_3_zero_step"
      ],
      data[
        "pi10_7_step"
      ],
      given_toda56,
    ),
  ) is None


def test_phase73_5_final_is_not_given():
  data = build_phase73_5_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


