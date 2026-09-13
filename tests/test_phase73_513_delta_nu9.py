from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  Sum,
  Suspension,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaDeltaMap,
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
from test_phase66_literature_aggregate import (
  build_phase66_7_data,
)
from test_phase73_pi9_3_zero import (
  build_phase73_4_data,
)
from test_phase73_pi10_4_nu4_squared import (
  build_phase73_5_data,
)
from toda_rules import (
  Toda58EquationStatement,
  TodaDeltaImageUpToSignStatement,
  toda_nu_family_definition_statement,
  toda_prop511_513_delta_nu9_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase73_6a_data():
  phase66 = (
    build_phase66_7_data()
  )

  phase73_4 = (
    build_phase73_4_data()
  )

  phase73_5 = (
    build_phase73_5_data()
  )

  toda58_step = (
    phase66[
      "integration_step"
    ]
  )

  pi9_3_zero_step = (
    phase73_4[
      "final_step"
    ]
  )

  pi10_4_step = (
    phase73_5[
      "final_step"
    ]
  )

  nu4_squared = (
    pi10_4_step
    .conclusion
    .rhs
    .generator
  )

  nu_4 = (
    nu4_squared.left
  )

  nu_7 = (
    nu4_squared.right
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

  delta_iota9 = (
    toda58_step
    .conclusion
    .delta_nu_relation
  )

  nu_prime = (
    delta_iota9
    .positive_value
    .right
    .expression
    .expression
  )

  nu_prime_nu6 = Composition(
    left=nu_prime,
    right=nu_6,
  )

  expected_statement = (
    TodaDeltaImageUpToSignStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=12,
          sphere_dimension=9,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=4,
        ),
      ),
      element=nu_9,
      positive_value=Multiple(
        coefficient=2,
        expression=nu4_squared,
      ),
    )
  )

  rule = (
    toda_prop511_513_delta_nu9_inference_rule()
  )

  premise_steps = (
    toda58_step,
    pi9_3_zero_step,
    pi10_4_step,
  )

  match = find_inference_match(
    rule,
    premise_steps,
  )

  assert (
    match
    is not None
  )

  final_step = (
    apply_inference_match(
      match
    )
  )

  return {
    "phase66": phase66,
    "phase73_4": phase73_4,
    "phase73_5": phase73_5,
    "toda58_step": toda58_step,
    "pi9_3_zero_step": (
      pi9_3_zero_step
    ),
    "pi10_4_step": pi10_4_step,
    "delta_iota9": delta_iota9,
    "nu_prime": nu_prime,
    "nu_4": nu_4,
    "nu_6": nu_6,
    "nu_7": nu_7,
    "nu_9": nu_9,
    "nu_prime_nu6": (
      nu_prime_nu6
    ),
    "nu4_squared": nu4_squared,
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "match": match,
    "final_step": final_step,
  }


def test_phase73_6a_reuses_derived_toda58():
  data = build_phase73_6a_data()

  assert isinstance(
    data[
      "toda58_step"
    ].conclusion,
    Toda58EquationStatement,
  )

  assert (
    data[
      "toda58_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_6a_reuses_derived_pi9_3_zero():
  data = build_phase73_6a_data()

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


def test_phase73_6a_reuses_derived_pi10_4():
  data = build_phase73_6a_data()

  relation = (
    data[
      "pi10_4_step"
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

  assert (
    data[
      "pi10_4_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_6a_toda58_has_expected_delta_iota9():
  data = build_phase73_6a_data()

  nu_prime = data[
    "nu_prime"
  ]

  expected_value = Sum(
    left=Multiple(
      coefficient=2,
      expression=data[
        "nu_4"
      ],
    ),
    right=Multiple(
      coefficient=-1,
      expression=Suspension(
        expression=nu_prime,
      ),
    ),
  )

  assert (
    data[
      "delta_iota9"
    ].positive_value
    == expected_value
  )


def test_phase73_6a_nu4_squared_is_nu4_nu7():
  data = build_phase73_6a_data()

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


def test_phase73_6a_nu_prime_nu6_lies_in_pi9_3():
  data = build_phase73_6a_data()

  expression = (
    data[
      "nu_prime_nu6"
    ]
  )

  assert (
    expression
    .is_type_compatible()
  )

  assert (
    data[
      "nu_6"
    ].source
    == 9
  )

  assert (
    data[
      "nu_6"
    ].target
    == 6
  )

  assert (
    data[
      "nu_prime"
    ].source
    == 6
  )

  assert (
    data[
      "nu_prime"
    ].target
    == 3
  )


def test_phase73_6a_nu9_has_correct_typing():
  data = build_phase73_6a_data()

  nu_9 = data[
    "nu_9"
  ]

  assert (
    nu_9.source
    == 12
  )

  assert (
    nu_9.target
    == 9
  )

  assert (
    nu_9.generator
    == GeneratorSymbol(
      family="ν",
      index=9,
    )
  )


def test_phase73_6a_rule_matches_dependencies():
  data = build_phase73_6a_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase73_6a_derives_delta_nu9():
  data = build_phase73_6a_data()

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


def test_phase73_6a_delta_map_has_correct_groups():
  data = build_phase73_6a_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement.map
    == TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=12,
        sphere_dimension=9,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=4,
      ),
    )
  )


def test_phase73_6a_positive_value_is_twice_nu4_squared():
  data = build_phase73_6a_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    statement.positive_value
    == Multiple(
      coefficient=2,
      expression=data[
        "nu4_squared"
      ],
    )
  )


def test_phase73_6a_final_uses_exact_three_dependencies():
  data = build_phase73_6a_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "toda58_step"
      ],
      data[
        "pi9_3_zero_step"
      ],
      data[
        "pi10_4_step"
      ],
    )
  )


def test_phase73_6a_rejects_given_toda58():
  data = build_phase73_6a_data()

  given = ProofStep(
    conclusion=(
      data[
        "toda58_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      given,
      data[
        "pi9_3_zero_step"
      ],
      data[
        "pi10_4_step"
      ],
    ),
  ) is None


def test_phase73_6a_rejects_wrong_zero_group():
  data = build_phase73_6a_data()

  wrong = ProofStep(
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
      "rule"
    ],
    (
      data[
        "toda58_step"
      ],
      wrong,
      data[
        "pi10_4_step"
      ],
    ),
  ) is None


def test_phase73_6a_rejects_wrong_pi10_4_order():
  data = build_phase73_6a_data()

  relation = (
    data[
      "pi10_4_step"
    ].conclusion
  )

  wrong_relation = replace(
    relation,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=data[
        "nu4_squared"
      ],
    ),
  )

  wrong = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "toda58_step"
      ],
      data[
        "pi9_3_zero_step"
      ],
      wrong,
    ),
  ) is None


def test_phase73_6a_rejects_wrong_pi10_4_generator():
  data = build_phase73_6a_data()

  wrong_nu_6 = (
    toda_nu_family_definition_statement(
      6
    ).element
  )

  wrong_generator = Composition(
    left=data[
      "nu_4"
    ],
    right=wrong_nu_6,
  )

  relation = (
    data[
      "pi10_4_step"
    ].conclusion
  )

  wrong_relation = replace(
    relation,
    rhs=FiniteCyclicGroup(
      order=8,
      generator=wrong_generator,
    ),
  )

  wrong = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "toda58_step"
      ],
      data[
        "pi9_3_zero_step"
      ],
      wrong,
    ),
  ) is None


def test_phase73_6a_rejects_wrong_delta_iota9_value():
  data = build_phase73_6a_data()

  toda58 = (
    data[
      "toda58_step"
    ].conclusion
  )

  wrong_delta = replace(
    toda58.delta_nu_relation,
    positive_value=Multiple(
      coefficient=2,
      expression=data[
        "nu_4"
      ],
    ),
  )

  wrong_toda58 = replace(
    toda58,
    delta_nu_relation=wrong_delta,
  )

  wrong = ProofStep(
    conclusion=wrong_toda58,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong,
      data[
        "pi9_3_zero_step"
      ],
      data[
        "pi10_4_step"
      ],
    ),
  ) is None


def test_phase73_6a_final_is_not_given():
  data = build_phase73_6a_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


