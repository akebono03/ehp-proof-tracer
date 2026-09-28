from functools import lru_cache

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
  barratt_hilton_first_inference_rule,
  barratt_hilton_second_inference_rule,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  ScalarPower,
  ScalarProduct,
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
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase62_toda55_integration import (
  build_phase62_6_data,
)
from test_phase68_eta_n_nu_n_plus_one_zero import (
  build_phase68_8_data,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
  TodaNuFamilyDefinitionStatement,
  toda_eta_family_definition_statement,
  toda_nu_family_definition_statement,
  toda_prop31_nu6_eta9_zero_inference_rule,
  toda_prop58_eta6_nu7_zero_specialization_inference_rule,
  toda_prop58_higher_nu_eta_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase68_9_data():
  phase62_6 = (
    build_phase62_6_data()
  )

  phase68_8 = (
    build_phase68_8_data()
  )

  toda55_step = (
    phase62_6[
      "integration_step"
    ]
  )

  higher_eta_nu_zero_step = (
    phase68_8[
      "final_step"
    ]
  )

  eta6_definition_step = ProofStep(
    conclusion=(
      toda_eta_family_definition_statement(
        6
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nu7_definition_step = ProofStep(
    conclusion=(
      toda_nu_family_definition_statement(
        7
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  nu_4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  eta2_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=eta_2,
        group_dimension=3,
        sphere_dimension=2,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nu4_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=nu_4,
        group_dimension=7,
        sphere_dimension=4,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_rule = (
    barratt_hilton_first_inference_rule(
      alpha=eta_2,
      beta=nu_4,
      p=2,
      q=4,
      k=1,
      h=3,
    )
  )

  second_rule = (
    barratt_hilton_second_inference_rule(
      alpha=eta_2,
      beta=nu_4,
      p=2,
      q=4,
      k=1,
      h=3,
    )
  )

  specialization_rule = (
    toda_prop58_eta6_nu7_zero_specialization_inference_rule()
  )

  concrete_zero_rule = (
    toda_prop31_nu6_eta9_zero_inference_rule()
  )

  higher_zero_rule = (
    toda_prop58_higher_nu_eta_zero_inference_rule()
  )

  n = (
    toda55_step
    .conclusion
    .nu_family_definition
    .index
  )

  n_ge_6_step = ProofStep(
    conclusion=(
      ScalarGreaterEqualStatement(
        left=n,
        right=6,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rules = (
    first_rule,
    second_rule,
    specialization_rule,
    concrete_zero_rule,
    higher_zero_rule,
  )

  premise_steps = (
    toda55_step,
    higher_eta_nu_zero_step,
    eta6_definition_step,
    nu7_definition_step,
    eta2_membership_step,
    nu4_membership_step,
    n_ge_6_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  eta_6 = (
    eta6_definition_step
    .conclusion
    .element
  )

  nu_7 = (
    nu7_definition_step
    .conclusion
    .element
  )

  expected_eta6_nu7_zero = Relation(
    lhs=Composition(
      left=eta_6,
      right=nu_7,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  eta6_nu7_zero_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_eta6_nu7_zero
    )
  )

  first_formula_step = next(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.rhs
      == Multiple(
        coefficient=ScalarPower(
          base=-1,
          exponent=ScalarProduct(
            left=3,
            right=3,
          ),
        ),
        expression=Composition(
          left=IteratedSuspension(
            expression=eta_2,
            exponent=4,
          ),
          right=IteratedSuspension(
            expression=nu_4,
            exponent=3,
          ),
        ),
      )
    )
  )

  second_formula_step = next(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.rhs
      == Multiple(
        coefficient=ScalarPower(
          base=-1,
          exponent=ScalarProduct(
            left=2,
            right=3,
          ),
        ),
        expression=Composition(
          left=IteratedSuspension(
            expression=nu_4,
            exponent=2,
          ),
          right=IteratedSuspension(
            expression=eta_2,
            exponent=7,
          ),
        ),
      )
    )
  )

  nu_6 = (
    toda_nu_family_definition_statement(
      6
    ).element
  )

  eta_9 = (
    toda_eta_family_definition_statement(
      9
    ).element
  )

  expected_nu6_eta9_zero = Relation(
    lhs=Composition(
      left=nu_6,
      right=eta_9,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  nu6_eta9_zero_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_nu6_eta9_zero
    )
  )

  nu_n = (
    toda55_step
    .conclusion
    .nu_family_definition
    .element
  )

  n_plus_three = ScalarSum(
    left=n,
    right=3,
  )

  eta_n_plus_three = HomotopyElement(
    name="η_(n+3)",
    dimension=n_plus_three,
    source=ScalarSum(
      left=n,
      right=4,
    ),
    target=n_plus_three,
    generator=GeneratorSymbol(
      family="η",
      index=n_plus_three,
    ),
  )

  expected_final = Relation(
    lhs=Composition(
      left=nu_n,
      right=eta_n_plus_three,
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
    "phase68_8": phase68_8,
    "toda55_step": toda55_step,
    "higher_eta_nu_zero_step": (
      higher_eta_nu_zero_step
    ),
    "eta6_definition_step": (
      eta6_definition_step
    ),
    "nu7_definition_step": (
      nu7_definition_step
    ),
    "eta2_membership_step": (
      eta2_membership_step
    ),
    "nu4_membership_step": (
      nu4_membership_step
    ),
    "n_ge_6_step": n_ge_6_step,
    "first_rule": first_rule,
    "second_rule": second_rule,
    "specialization_rule": (
      specialization_rule
    ),
    "concrete_zero_rule": (
      concrete_zero_rule
    ),
    "higher_zero_rule": (
      higher_zero_rule
    ),
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "n": n,
    "eta_2": eta_2,
    "nu_4": nu_4,
    "eta_6": eta_6,
    "nu_7": nu_7,
    "nu_6": nu_6,
    "eta_9": eta_9,
    "nu_n": nu_n,
    "eta_n_plus_three": (
      eta_n_plus_three
    ),
    "first_formula_step": (
      first_formula_step
    ),
    "second_formula_step": (
      second_formula_step
    ),
    "expected_eta6_nu7_zero": (
      expected_eta6_nu7_zero
    ),
    "eta6_nu7_zero_step": (
      eta6_nu7_zero_step
    ),
    "expected_nu6_eta9_zero": (
      expected_nu6_eta9_zero
    ),
    "nu6_eta9_zero_step": (
      nu6_eta9_zero_step
    ),
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase68_9a_reuses_phase68_8():
  data = build_phase68_9_data()

  assert (
    data[
      "higher_eta_nu_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_9a_derives_eta6_nu7_zero():
  data = build_phase68_9_data()

  assert (
    data[
      "eta6_nu7_zero_step"
    ].conclusion
    == data[
      "expected_eta6_nu7_zero"
    ]
  )

  assert (
    data[
      "eta6_nu7_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_9a_uses_exact_dependencies():
  data = build_phase68_9_data()

  assert (
    data[
      "eta6_nu7_zero_step"
    ].premises
    == (
      data[
        "higher_eta_nu_zero_step"
      ],
      data[
        "toda55_step"
      ],
      data[
        "eta6_definition_step"
      ],
      data[
        "nu7_definition_step"
      ],
    )
  )


def test_phase68_9b_prop31_first_formula_is_derived():
  data = build_phase68_9_data()

  assert (
    data[
      "first_formula_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_9b_prop31_second_formula_is_derived():
  data = build_phase68_9_data()

  assert (
    data[
      "second_formula_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_9b_prop31_formulas_share_lhs():
  data = build_phase68_9_data()

  assert (
    data[
      "first_formula_step"
    ].conclusion.lhs
    == data[
      "second_formula_step"
    ].conclusion.lhs
  )


def test_phase68_9b_derives_nu6_eta9_zero():
  data = build_phase68_9_data()

  assert (
    data[
      "nu6_eta9_zero_step"
    ].conclusion
    == data[
      "expected_nu6_eta9_zero"
    ]
  )

  assert (
    data[
      "nu6_eta9_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_9b_uses_prop31_provenance():
  data = build_phase68_9_data()

  assert (
    data[
      "first_formula_step"
    ]
    in data[
      "nu6_eta9_zero_step"
    ].premises
  )

  assert (
    data[
      "second_formula_step"
    ]
    in data[
      "nu6_eta9_zero_step"
    ].premises
  )


def test_phase68_9b_uses_eta6_nu7_zero():
  data = build_phase68_9_data()

  assert (
    data[
      "eta6_nu7_zero_step"
    ]
    in data[
      "nu6_eta9_zero_step"
    ].premises
  )


def test_phase68_9c_range_is_explicit_n_ge_6():
  data = build_phase68_9_data()

  assert (
    data[
      "n_ge_6_step"
    ].conclusion
    == ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=6,
    )
  )

  assert (
    data[
      "n_ge_6_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase68_9c_derives_higher_zero():
  data = build_phase68_9_data()

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


def test_phase68_9c_final_left_is_nu_n_eta_n_plus_three():
  data = build_phase68_9_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    .left
    == data[
      "nu_n"
    ]
  )

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    .right
    == data[
      "eta_n_plus_three"
    ]
  )


def test_phase68_9c_final_is_zero():
  data = build_phase68_9_data()

  assert (
    data[
      "final_step"
    ].conclusion.rhs
    == Zero()
  )

  assert (
    data[
      "final_step"
    ].conclusion.relation_type
    == RelationType.ZERO
  )


def test_phase68_9c_uses_exact_dependencies():
  data = build_phase68_9_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "nu6_eta9_zero_step"
      ],
      data[
        "toda55_step"
      ],
      data[
        "n_ge_6_step"
      ],
    )
  )


def test_phase68_9a_rejects_given_phase68_8_result():
  data = build_phase68_9_data()

  given = ProofStep(
    conclusion=(
      data[
        "higher_eta_nu_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "specialization_rule"
    ],
    (
      given,
      data[
        "toda55_step"
      ],
      data[
        "eta6_definition_step"
      ],
      data[
        "nu7_definition_step"
      ],
    ),
  ) is None


def test_phase68_9b_rejects_given_first_prop31_formula():
  data = build_phase68_9_data()

  given = ProofStep(
    conclusion=(
      data[
        "first_formula_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "concrete_zero_rule"
    ],
    (
      data[
        "eta6_nu7_zero_step"
      ],
      given,
      data[
        "second_formula_step"
      ],
    ),
  ) is None


def test_phase68_9b_rejects_given_second_prop31_formula():
  data = build_phase68_9_data()

  given = ProofStep(
    conclusion=(
      data[
        "second_formula_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "concrete_zero_rule"
    ],
    (
      data[
        "eta6_nu7_zero_step"
      ],
      data[
        "first_formula_step"
      ],
      given,
    ),
  ) is None


def test_phase68_9c_rejects_given_base_zero():
  data = build_phase68_9_data()

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
      "higher_zero_rule"
    ],
    (
      given,
      data[
        "toda55_step"
      ],
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase68_9_final_result_not_initially_given():
  data = build_phase68_9_data()

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


def test_phase68_9_reaches_fixed_point():
  data = build_phase68_9_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase68_9c_does_not_require_shifted_eta_family_definition():
  data = build_phase68_9_data()

  assert all(
    not (
      isinstance(
        step.conclusion,
        TodaEtaFamilyDefinitionStatement,
      )
      and isinstance(
        step.conclusion.index,
        ScalarSum,
      )
    )
    for step in data[
      "premise_steps"
    ]
  )


