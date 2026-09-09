from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarSum,
  Zero,
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
from test_phase62_toda55_integration import (
  build_phase62_6_data,
)
from test_phase65_nu5_order_pi8_5 import (
  build_phase65_7_data,
)
from test_phase68_pi9_5_nu5_eta8 import (
  build_phase68_6_data,
)
from test_phase68_toda59_eta3_nu4 import (
  build_phase68_7_data,
)
from toda_rules import (
  Toda55NuFamilyFiniteDimensionalStatement,
  TodaEtaFamilyDefinitionStatement,
  TodaNuFamilyDefinitionStatement,
  toda_eta_family_definition_statement,
  toda_nu_family_definition_statement,
  toda_510_eta5_nu6_bridge_inference_rule,
  toda_510_eta5_nu6_zero_inference_rule,
  toda_510_higher_eta_nu_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase68_8_data():
  phase62_6 = (
    build_phase62_6_data()
  )

  phase65_7 = (
    build_phase65_7_data()
  )

  phase68_6 = (
    build_phase68_6_data()
  )

  phase68_7 = (
    build_phase68_7_data()
  )

  toda55_step = (
    phase62_6[
      "integration_step"
    ]
  )

  double_nu5_step = (
    phase65_7[
      "double_step"
    ]
  )

  pi9_5_step = (
    phase68_6[
      "final_step"
    ]
  )

  toda59_step = (
    phase68_7[
      "final_step"
    ]
  )

  nu6_definition_step = ProofStep(
    conclusion=(
      toda_nu_family_definition_statement(
        6
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  n = (
    toda55_step
    .conclusion
    .nu_family_definition
    .index
  )

  eta_n_definition_step = ProofStep(
    conclusion=(
      toda_eta_family_definition_statement(
        n
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  bridge_rule = (
    toda_510_eta5_nu6_bridge_inference_rule()
  )

  base_zero_rule = (
    toda_510_eta5_nu6_zero_inference_rule()
  )

  higher_zero_rule = (
    toda_510_higher_eta_nu_zero_inference_rule()
  )

  rules = (
    bridge_rule,
    base_zero_rule,
    higher_zero_rule,
  )

  premise_steps = (
    toda59_step,
    nu6_definition_step,
    double_nu5_step,
    pi9_5_step,
    toda55_step,
    eta_n_definition_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  eta_5 = HomotopyElement(
    name="η₅",
    dimension=5,
    source=6,
    target=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
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

  nu_6 = (
    nu6_definition_step
    .conclusion
    .element
  )

  nu_prime = (
    phase65_7[
      "nu_prime"
    ]
  )

  expected_bridge = Relation(
    lhs=Composition(
      left=eta_5,
      right=nu_6,
    ),
    rhs=Composition(
      left=IteratedSuspension(
        expression=nu_prime,
        exponent=2,
      ),
      right=eta_8,
    ),
    relation_type=RelationType.EQUALITY,
  )

  bridge_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_bridge
    )
  )

  expected_base_zero = Relation(
    lhs=Composition(
      left=eta_5,
      right=nu_6,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  base_zero_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_base_zero
    )
  )

  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )

  nu_n_plus_one = HomotopyElement(
    name="ν_(n+1)",
    dimension=n_plus_one,
    source=ScalarSum(
      left=n,
      right=4,
    ),
    target=n_plus_one,
    generator=GeneratorSymbol(
      family="ν",
      index=n_plus_one,
    ),
  )

  eta_n = (
    eta_n_definition_step
    .conclusion
    .element
  )

  expected_final = Relation(
    lhs=Composition(
      left=eta_n,
      right=nu_n_plus_one,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
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
    "phase62_6": phase62_6,
    "phase65_7": phase65_7,
    "phase68_6": phase68_6,
    "phase68_7": phase68_7,
    "toda55_step": toda55_step,
    "double_nu5_step": (
      double_nu5_step
    ),
    "pi9_5_step": pi9_5_step,
    "toda59_step": toda59_step,
    "nu6_definition_step": (
      nu6_definition_step
    ),
    "eta_n_definition_step": (
      eta_n_definition_step
    ),
    "bridge_rule": bridge_rule,
    "base_zero_rule": (
      base_zero_rule
    ),
    "higher_zero_rule": (
      higher_zero_rule
    ),
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "n": n,
    "eta_5": eta_5,
    "eta_8": eta_8,
    "nu_6": nu_6,
    "nu_prime": nu_prime,
    "eta_n": eta_n,
    "nu_n_plus_one": (
      nu_n_plus_one
    ),
    "expected_bridge": (
      expected_bridge
    ),
    "bridge_step": bridge_step,
    "expected_base_zero": (
      expected_base_zero
    ),
    "base_zero_step": (
      base_zero_step
    ),
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase68_8_reuses_derived_toda59():
  data = build_phase68_8_data()

  assert (
    data[
      "toda59_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_8_reuses_derived_two_nu5():
  data = build_phase68_8_data()

  assert (
    data[
      "double_nu5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_8_reuses_derived_pi9_5():
  data = build_phase68_8_data()

  assert (
    data[
      "pi9_5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_8_reuses_toda55_aggregate():
  data = build_phase68_8_data()

  assert isinstance(
    data[
      "toda55_step"
    ].conclusion,
    Toda55NuFamilyFiniteDimensionalStatement,
  )

  assert (
    data[
      "toda55_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_8_nu6_definition_remains_given():
  data = build_phase68_8_data()

  assert isinstance(
    data[
      "nu6_definition_step"
    ].conclusion,
    TodaNuFamilyDefinitionStatement,
  )

  assert (
    data[
      "nu6_definition_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase68_8_symbolic_eta_definition_remains_given():
  data = build_phase68_8_data()

  assert isinstance(
    data[
      "eta_n_definition_step"
    ].conclusion,
    TodaEtaFamilyDefinitionStatement,
  )

  assert (
    data[
      "eta_n_definition_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase68_8_derives_eta5_nu6_bridge():
  data = build_phase68_8_data()

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


def test_phase68_8_bridge_uses_toda59_and_nu6_definition():
  data = build_phase68_8_data()

  assert (
    data[
      "bridge_step"
    ].premises
    == (
      data[
        "toda59_step"
      ],
      data[
        "nu6_definition_step"
      ],
    )
  )


def test_phase68_8_derives_eta5_nu6_zero():
  data = build_phase68_8_data()

  assert (
    data[
      "base_zero_step"
    ].conclusion
    == data[
      "expected_base_zero"
    ]
  )

  assert (
    data[
      "base_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_8_base_zero_uses_exact_dependencies():
  data = build_phase68_8_data()

  assert (
    data[
      "base_zero_step"
    ].premises
    == (
      data[
        "bridge_step"
      ],
      data[
        "double_nu5_step"
      ],
      data[
        "pi9_5_step"
      ],
    )
  )


def test_phase68_8_final_is_eta_n_nu_n_plus_one_zero():
  data = build_phase68_8_data()

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


def test_phase68_8_final_left_has_eta_n():
  data = build_phase68_8_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    .left
    == data[
      "eta_n"
    ]
  )


def test_phase68_8_final_left_has_nu_n_plus_one():
  data = build_phase68_8_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    .right
    == data[
      "nu_n_plus_one"
    ]
  )


def test_phase68_8_final_is_zero_relation():
  data = build_phase68_8_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .relation_type
    == RelationType.ZERO
  )

  assert (
    data[
      "final_step"
    ].conclusion.rhs
    == Zero()
  )


def test_phase68_8_final_range_is_n_at_least_five():
  data = build_phase68_8_data()

  statement = (
    data[
      "toda55_step"
    ].conclusion
  )

  assert (
    statement.n_range.left
    == data[
      "n"
    ]
  )

  assert (
    statement.n_range.right
    == 5
  )


def test_phase68_8_final_uses_exact_three_dependencies():
  data = build_phase68_8_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "base_zero_step"
      ],
      data[
        "toda55_step"
      ],
      data[
        "eta_n_definition_step"
      ],
    )
  )


def test_phase68_8_rejects_given_toda59():
  data = build_phase68_8_data()

  given = ProofStep(
    conclusion=(
      data[
        "toda59_step"
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
        "nu6_definition_step"
      ],
    ),
  ) is None


def test_phase68_8_rejects_given_base_zero():
  data = build_phase68_8_data()

  given = ProofStep(
    conclusion=(
      data[
        "base_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "higher_zero_rule"
    ],
    (
      given,
      data[
        "toda55_step"
      ],
      data[
        "eta_n_definition_step"
      ],
    ),
  ) is None


def test_phase68_8_rejects_given_toda55():
  data = build_phase68_8_data()

  given = ProofStep(
    conclusion=(
      data[
        "toda55_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "higher_zero_rule"
    ],
    (
      data[
        "base_zero_step"
      ],
      given,
      data[
        "eta_n_definition_step"
      ],
    ),
  ) is None


def test_phase68_8_final_result_not_present_initially():
  data = build_phase68_8_data()

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


def test_phase68_8_reaches_fixed_point():
  data = build_phase68_8_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


