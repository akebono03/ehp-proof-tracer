from functools import lru_cache

from expression import (
  GeneratorSymbol,
  IteratedSuspension,
  Multiple,
  ScalarProduct,
  Suspension,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
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
from test_phase75_lemma514_sigma8 import (
  build_phase75_8a_data,
)
from test_phase75_pi12_5_order_two import (
  build_phase75_5_data,
)
from test_phase75_sigma_family_definition import (
  build_phase75_8b_data,
)
from toda_rules import (
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  TodaLemma514Sigma8Statement,
  TodaSigmaFamilyDefinitionStatement,
  toda_48_pi16_9_order_and_e4_injective_inference_rule,
  toda_prop515_pi16_9_sigma9_finite_cyclic_inference_rule,
  toda_sigma_family_definition_statement,
)


@lru_cache(maxsize=1)
def build_phase75_8c_data():
  phase75_5 = (
    build_phase75_5_data()
  )

  phase75_8a = (
    build_phase75_8a_data()
  )

  phase75_8b = (
    build_phase75_8b_data()
  )

  pi12_5_step = (
    phase75_5[
      "final_step"
    ]
  )

  sigma8_step = (
    phase75_8a[
      "sigma8_step"
    ]
  )

  prop48_rule = (
    toda_48_pi16_9_order_and_e4_injective_inference_rule()
  )

  prop48_result = (
    run_inference_until_stable_with_history(
      (
        prop48_rule,
      ),
      (
        pi12_5_step,
      ),
    )
  )

  prop48_step = next(
    step
    for step
    in prop48_result.steps
    if isinstance(
      step.conclusion,
      Toda48Pi16_9OrderAndE4InjectiveStatement,
    )
  )

  sigma9_definition = (
    toda_sigma_family_definition_statement(
      9,
      sigma8_step.conclusion,
    )
  )

  sigma9_definition_step = ProofStep(
    conclusion=sigma9_definition,
    premises=(
      sigma8_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  final_rule = (
    toda_prop515_pi16_9_sigma9_finite_cyclic_inference_rule()
  )

  premise_steps = (
    prop48_step,
    sigma8_step,
    sigma9_definition_step,
    pi12_5_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        final_rule,
      ),
      premise_steps,
    )
  )

  expected_final = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=16,
      sphere_dimension=9,
    ),
    rhs=FiniteCyclicGroup(
      order=16,
      generator=(
        sigma9_definition.element
      ),
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
    "phase75_5": phase75_5,
    "phase75_8a": phase75_8a,
    "phase75_8b": phase75_8b,
    "pi12_5_step": pi12_5_step,
    "sigma8_step": sigma8_step,
    "prop48_rule": prop48_rule,
    "prop48_step": prop48_step,
    "sigma9_definition": (
      sigma9_definition
    ),
    "sigma9_definition_step": (
      sigma9_definition_step
    ),
    "final_rule": final_rule,
    "premise_steps": premise_steps,
    "result": result,
    "expected_final": expected_final,
    "final_step": final_step,
  }


def test_phase75_8c_reuses_pi12_5_z2():
  data = build_phase75_8c_data()

  relation = (
    data[
      "pi12_5_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=5,
    )
  )

  assert (
    relation.rhs.order
    == 2
  )

  assert (
    data[
      "pi12_5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8c_derives_prop48_concrete_statement():
  data = build_phase75_8c_data()

  assert isinstance(
    data[
      "prop48_step"
    ].conclusion,
    Toda48Pi16_9OrderAndE4InjectiveStatement,
  )

  assert (
    data[
      "prop48_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8c_prop48_target_order_is_16():
  data = build_phase75_8c_data()

  assert (
    data[
      "prop48_step"
    ].conclusion
    .target_order
    == 16
  )


def test_phase75_8c_prop48_map_is_e4():
  data = build_phase75_8c_data()

  statement = (
    data[
      "prop48_step"
    ].conclusion
  )

  assert (
    statement.iterated_suspension_map
    == TodaIteratedSuspensionMap(
      exponent=4,
      source_group=TodaPrimaryGroup(
        group_dimension=12,
        sphere_dimension=5,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=16,
        sphere_dimension=9,
      ),
    )
  )


def test_phase75_8c_reuses_sigma8_statement():
  data = build_phase75_8c_data()

  assert isinstance(
    data[
      "sigma8_step"
    ].conclusion,
    TodaLemma514Sigma8Statement,
  )

  assert (
    data[
      "sigma8_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8c_sigma9_definition():
  data = build_phase75_8c_data()

  statement = (
    data[
      "sigma9_definition"
    ]
  )

  assert isinstance(
    statement,
    TodaSigmaFamilyDefinitionStatement,
  )

  assert (
    statement.index
    == 9
  )

  assert (
    statement.element.source
    == 16
  )

  assert (
    statement.element.target
    == 9
  )

  assert (
    statement.element.generator
    == GeneratorSymbol(
      family="σ",
      index=9,
    )
  )


def test_phase75_8c_sigma9_is_e_sigma8():
  data = build_phase75_8c_data()

  assert (
    data[
      "sigma9_definition"
    ].iterated_suspension
    == IteratedSuspension(
      expression=(
        data[
          "sigma8_step"
        ].conclusion
        .sigma8
      ),
      exponent=1,
    )
  )


def test_phase75_8c_sigma8_relation_uses_same_x_alpha_star():
  data = build_phase75_8c_data()

  statement = (
    data[
      "sigma8_step"
    ].conclusion
  )

  assert (
    statement.suspension_relation
    == Relation(
      lhs=Suspension(
        expression=statement.sigma8,
      ),
      rhs=Multiple(
        coefficient=(
          statement.odd_parameter
        ),
        expression=Suspension(
          expression=statement.alpha_star,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase75_8c_bridge_gives_eight_sigma9_nonzero_source():
  data = build_phase75_8c_data()

  sigma8_statement = (
    data[
      "sigma8_step"
    ].conclusion
  )

  bridge = (
    sigma8_statement
    .theorem36_bridge
  )

  sigma_triple_prime = (
    data[
      "pi12_5_step"
    ].conclusion
    .rhs
    .generator
  )

  assert (
    bridge.bridge_relation
    == Relation(
      lhs=Multiple(
        coefficient=ScalarProduct(
          left=8,
          right=(
            bridge.odd_parameter
          ),
        ),
        expression=Suspension(
          expression=bridge.alpha_star,
        ),
      ),
      rhs=IteratedSuspension(
        expression=sigma_triple_prime,
        exponent=4,
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase75_8c_derives_pi16_9_z16_sigma9():
  data = build_phase75_8c_data()

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


def test_phase75_8c_final_group_is_pi16_9():
  data = build_phase75_8c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    == TodaPrimaryGroup(
      group_dimension=16,
      sphere_dimension=9,
    )
  )


def test_phase75_8c_final_group_order_is_16():
  data = build_phase75_8c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .order
    == 16
  )


def test_phase75_8c_final_generator_is_sigma9():
  data = build_phase75_8c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == data[
      "sigma9_definition"
    ].element
  )


def test_phase75_8c_final_uses_exact_dependencies():
  data = build_phase75_8c_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "prop48_step"
      ],
      data[
        "sigma8_step"
      ],
      data[
        "sigma9_definition_step"
      ],
      data[
        "pi12_5_step"
      ],
    )
  )


def test_phase75_8c_final_not_present_initially():
  data = build_phase75_8c_data()

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


def test_phase75_8c_rejects_given_prop48():
  data = build_phase75_8c_data()

  given = ProofStep(
    conclusion=(
      data[
        "prop48_step"
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
        "sigma8_step"
      ],
      data[
        "sigma9_definition_step"
      ],
      data[
        "pi12_5_step"
      ],
    ),
  ) is None


def test_phase75_8c_rejects_given_sigma8():
  data = build_phase75_8c_data()

  given = ProofStep(
    conclusion=(
      data[
        "sigma8_step"
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
        "prop48_step"
      ],
      given,
      data[
        "sigma9_definition_step"
      ],
      data[
        "pi12_5_step"
      ],
    ),
  ) is None


def test_phase75_8c_rejects_given_pi12_5():
  data = build_phase75_8c_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi12_5_step"
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
        "prop48_step"
      ],
      data[
        "sigma8_step"
      ],
      data[
        "sigma9_definition_step"
      ],
      given,
    ),
  ) is None


def test_phase75_8c_reaches_fixed_point():
  data = build_phase75_8c_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


