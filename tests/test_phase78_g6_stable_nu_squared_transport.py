from functools import lru_cache

from expression import (
  Composition,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  StableHomotopyGroup,
  StablePrimaryComponent,
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
from test_phase78_g3_stable_nu_transport import (
  build_phase78_8c_data,
)
from toda_rules import (
  Toda45StableTwoPrimaryIdentificationStatement,
  TodaStableNuSquaredDefinitionStatement,
  toda_45_stable_two_primary_identification_inference_rule,
  toda_nu_family_definition_statement,
  toda_prop511_g6_two_primary_finite_cyclic_inference_rule,
  toda_prop511_stable_nu_squared_definition_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase78_8d_data():
  phase78_8c = (
    build_phase78_8c_data()
  )

  stable_nu_step = (
    phase78_8c[
      "stable_nu_step"
    ]
  )

  nu8_definition = (
    toda_nu_family_definition_statement(
      8
    )
  )

  nu11_definition = (
    toda_nu_family_definition_statement(
      11
    )
  )

  nu8_definition_step = ProofStep(
    conclusion=nu8_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nu11_definition_step = ProofStep(
    conclusion=nu11_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nu8_squared = Composition(
    left=nu8_definition.element,
    right=nu11_definition.element,
  )

  pi14_8_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=8,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=nu8_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  pi14_8_step = ProofStep(
    conclusion=pi14_8_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
    note=(
      "Existing Phase 73 derived result "
      "pi_14^8=Z/2{nu_8 squared}."
    ),
  )

  source_group = (
    pi14_8_relation.lhs
  )

  source_group_step = ProofStep(
    conclusion=source_group,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  identification_rule = (
    toda_45_stable_two_primary_identification_inference_rule()
  )

  stable_nu_squared_rule = (
    toda_prop511_stable_nu_squared_definition_inference_rule()
  )

  transport_rule = (
    toda_prop511_g6_two_primary_finite_cyclic_inference_rule()
  )

  rules = (
    identification_rule,
    stable_nu_squared_rule,
    transport_rule,
  )

  premise_steps = (
    nu8_definition_step,
    nu11_definition_step,
    pi14_8_step,
    source_group_step,
    stable_nu_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  expected_identification = (
    Toda45StableTwoPrimaryIdentificationStatement(
      source_group=source_group,
      target_component=StablePrimaryComponent(
        group=StableHomotopyGroup(
          stem=6,
        ),
        prime=2,
      ),
    )
  )

  identification_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_identification
    )
  )

  stable_nu_squared_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaStableNuSquaredDefinitionStatement,
    )
  )

  expected_final = Relation(
    lhs=StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=6,
      ),
      prime=2,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=(
        stable_nu_squared_step
        .conclusion
        .stable_element
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
    "phase78_8c": phase78_8c,
    "stable_nu_step": stable_nu_step,
    "nu8_definition": nu8_definition,
    "nu11_definition": nu11_definition,
    "nu8_definition_step": (
      nu8_definition_step
    ),
    "nu11_definition_step": (
      nu11_definition_step
    ),
    "nu8_squared": nu8_squared,
    "pi14_8_relation": (
      pi14_8_relation
    ),
    "pi14_8_step": pi14_8_step,
    "source_group": source_group,
    "source_group_step": (
      source_group_step
    ),
    "identification_rule": (
      identification_rule
    ),
    "stable_nu_squared_rule": (
      stable_nu_squared_rule
    ),
    "transport_rule": transport_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "identification_step": (
      identification_step
    ),
    "stable_nu_squared_step": (
      stable_nu_squared_step
    ),
    "expected_final": expected_final,
    "final_step": final_step,
  }


def test_phase78_8d_reuses_derived_stable_nu():
  data = build_phase78_8d_data()

  assert (
    data[
      "stable_nu_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase78_8d_nu8_squared_has_expected_structure():
  data = build_phase78_8d_data()

  assert (
    data[
      "nu8_squared"
    ]
    == Composition(
      left=(
        data[
          "nu8_definition"
        ].element
      ),
      right=(
        data[
          "nu11_definition"
        ].element
      ),
    )
  )


def test_phase78_8d_nu8_squared_is_finite_type_compatible():
  data = build_phase78_8d_data()

  assert (
    data[
      "nu8_squared"
    ].is_type_compatible()
  )


def test_phase78_8d_source_group_relation_is_inference():
  data = build_phase78_8d_data()

  assert (
    data[
      "pi14_8_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi14_8_step"
    ].conclusion
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=14,
        sphere_dimension=8,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=(
          data[
            "nu8_squared"
          ]
        ),
      ),
      relation_type=(
        RelationType.EQUALITY
      ),
    )
  )


def test_phase78_8d_derives_stable_identification():
  data = build_phase78_8d_data()

  assert (
    data[
      "identification_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "identification_step"
    ].conclusion
    .target_component
    == StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=6,
      ),
      prime=2,
    )
  )


def test_phase78_8d_derives_stable_nu_squared_definition():
  data = build_phase78_8d_data()

  assert (
    data[
      "stable_nu_squared_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "stable_nu_squared_step"
    ].conclusion,
    TodaStableNuSquaredDefinitionStatement,
  )


def test_phase78_8d_stable_nu_squared_is_composition():
  data = build_phase78_8d_data()

  stable_nu = (
    data[
      "stable_nu_step"
    ].conclusion
    .stable_element
  )

  stable_nu_squared = (
    data[
      "stable_nu_squared_step"
    ].conclusion
    .stable_element
  )

  assert (
    stable_nu_squared
    == Composition(
      left=stable_nu,
      right=stable_nu,
    )
  )


def test_phase78_8d_does_not_require_stable_composition_typing():
  data = build_phase78_8d_data()

  stable_nu_squared = (
    data[
      "stable_nu_squared_step"
    ].conclusion
    .stable_element
  )

  assert not (
    stable_nu_squared
    .is_type_compatible()
  )


def test_phase78_8d_stable_square_preserves_finite_generator():
  data = build_phase78_8d_data()

  assert (
    data[
      "stable_nu_squared_step"
    ].conclusion
    .source_generator
    == data[
      "nu8_squared"
    ]
  )


def test_phase78_8d_stable_square_preserves_stable_nu_provenance():
  data = build_phase78_8d_data()

  assert (
    data[
      "stable_nu_squared_step"
    ].conclusion
    .stable_nu_definition
    == data[
      "stable_nu_step"
    ].conclusion
  )


def test_phase78_8d_stable_square_uses_exact_dependencies():
  data = build_phase78_8d_data()

  assert (
    data[
      "stable_nu_squared_step"
    ].premises
    == (
      data[
        "nu8_definition_step"
      ],
      data[
        "nu11_definition_step"
      ],
      data[
        "stable_nu_step"
      ],
      data[
        "identification_step"
      ],
    )
  )


def test_phase78_8d_derives_g6_two_primary_z2_nu_squared():
  data = build_phase78_8d_data()

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


def test_phase78_8d_final_group_is_g6_two_primary():
  data = build_phase78_8d_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    == StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=6,
      ),
      prime=2,
    )
  )


def test_phase78_8d_final_group_has_order_two():
  data = build_phase78_8d_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .order
    == 2
  )


def test_phase78_8d_final_generator_is_stable_nu_squared():
  data = build_phase78_8d_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == data[
      "stable_nu_squared_step"
    ].conclusion
    .stable_element
  )


def test_phase78_8d_final_uses_exact_dependencies():
  data = build_phase78_8d_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi14_8_step"
      ],
      data[
        "identification_step"
      ],
      data[
        "stable_nu_squared_step"
      ],
    )
  )


def test_phase78_8d_final_not_present_initially():
  data = build_phase78_8d_data()

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


def test_phase78_8d_square_rejects_given_stable_nu():
  data = build_phase78_8d_data()

  given_stable_nu = ProofStep(
    conclusion=(
      data[
        "stable_nu_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "stable_nu_squared_rule"
    ],
    (
      data[
        "nu8_definition_step"
      ],
      data[
        "nu11_definition_step"
      ],
      given_stable_nu,
      data[
        "identification_step"
      ],
    ),
  ) is None


def test_phase78_8d_transport_rejects_given_source_relation():
  data = build_phase78_8d_data()

  given_source_relation = ProofStep(
    conclusion=(
      data[
        "pi14_8_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "transport_rule"
    ],
    (
      given_source_relation,
      data[
        "identification_step"
      ],
      data[
        "stable_nu_squared_step"
      ],
    ),
  ) is None


def test_phase78_8d_transport_rejects_given_square_definition():
  data = build_phase78_8d_data()

  given_square = ProofStep(
    conclusion=(
      data[
        "stable_nu_squared_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "transport_rule"
    ],
    (
      data[
        "pi14_8_step"
      ],
      data[
        "identification_step"
      ],
      given_square,
    ),
  ) is None


def test_phase78_8d_reaches_fixed_point():
  data = build_phase78_8d_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


