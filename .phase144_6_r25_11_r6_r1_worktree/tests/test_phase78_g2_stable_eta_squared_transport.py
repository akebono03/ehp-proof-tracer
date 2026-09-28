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
from test_phase78_g1_stable_eta_transport import (
  build_phase78_8a_data,
)
from toda_rules import (
  Toda45StableTwoPrimaryIdentificationStatement,
  TodaStableEtaSquaredDefinitionStatement,
  toda_45_stable_two_primary_identification_inference_rule,
  toda_eta_family_definition_statement,
  toda_prop53_g2_two_primary_finite_cyclic_inference_rule,
  toda_prop53_stable_eta_squared_definition_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase78_8b_data():
  phase78_8a = (
    build_phase78_8a_data()
  )

  stable_eta_step = (
    phase78_8a[
      "stable_eta_step"
    ]
  )

  eta4_definition = (
    toda_eta_family_definition_statement(
      4
    )
  )

  eta5_definition = (
    toda_eta_family_definition_statement(
      5
    )
  )

  eta4_definition_step = ProofStep(
    conclusion=eta4_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta5_definition_step = ProofStep(
    conclusion=eta5_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta4_squared = Composition(
    left=eta4_definition.element,
    right=eta5_definition.element,
  )

  pi6_4_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=4,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta4_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  pi6_4_step = ProofStep(
    conclusion=pi6_4_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
    note=(
      "Existing Phase 59 derived result "
      "pi_6^4=Z/2{eta_4 squared}."
    ),
  )

  source_group = (
    pi6_4_relation.lhs
  )

  source_group_step = ProofStep(
    conclusion=source_group,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  identification_rule = (
    toda_45_stable_two_primary_identification_inference_rule()
  )

  stable_eta_squared_rule = (
    toda_prop53_stable_eta_squared_definition_inference_rule()
  )

  transport_rule = (
    toda_prop53_g2_two_primary_finite_cyclic_inference_rule()
  )

  rules = (
    identification_rule,
    stable_eta_squared_rule,
    transport_rule,
  )

  premise_steps = (
    eta4_definition_step,
    eta5_definition_step,
    pi6_4_step,
    source_group_step,
    stable_eta_step,
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
          stem=2,
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

  stable_eta_squared_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaStableEtaSquaredDefinitionStatement,
    )
  )

  expected_final = Relation(
    lhs=StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=2,
      ),
      prime=2,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=(
        stable_eta_squared_step
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
    "phase78_8a": phase78_8a,
    "stable_eta_step": (
      stable_eta_step
    ),
    "eta4_definition": (
      eta4_definition
    ),
    "eta5_definition": (
      eta5_definition
    ),
    "eta4_definition_step": (
      eta4_definition_step
    ),
    "eta5_definition_step": (
      eta5_definition_step
    ),
    "eta4_squared": eta4_squared,
    "pi6_4_relation": (
      pi6_4_relation
    ),
    "pi6_4_step": pi6_4_step,
    "source_group": source_group,
    "source_group_step": (
      source_group_step
    ),
    "identification_rule": (
      identification_rule
    ),
    "stable_eta_squared_rule": (
      stable_eta_squared_rule
    ),
    "transport_rule": (
      transport_rule
    ),
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "identification_step": (
      identification_step
    ),
    "stable_eta_squared_step": (
      stable_eta_squared_step
    ),
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase78_8b_reuses_derived_stable_eta():
  data = build_phase78_8b_data()

  assert (
    data[
      "stable_eta_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase78_8b_eta4_squared_has_expected_structure():
  data = build_phase78_8b_data()

  assert (
    data[
      "eta4_squared"
    ]
    == Composition(
      left=(
        data[
          "eta4_definition"
        ].element
      ),
      right=(
        data[
          "eta5_definition"
        ].element
      ),
    )
  )


def test_phase78_8b_source_group_relation_is_inference():
  data = build_phase78_8b_data()

  assert (
    data[
      "pi6_4_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi6_4_step"
    ].conclusion
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=4,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=(
          data[
            "eta4_squared"
          ]
        ),
      ),
      relation_type=(
        RelationType.EQUALITY
      ),
    )
  )


def test_phase78_8b_derives_stable_identification():
  data = build_phase78_8b_data()

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
        stem=2,
      ),
      prime=2,
    )
  )


def test_phase78_8b_derives_stable_eta_squared_definition():
  data = build_phase78_8b_data()

  assert (
    data[
      "stable_eta_squared_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "stable_eta_squared_step"
    ].conclusion,
    TodaStableEtaSquaredDefinitionStatement,
  )


def test_phase78_8b_stable_eta_squared_is_composition():
  data = build_phase78_8b_data()

  stable_eta = (
    data[
      "stable_eta_step"
    ].conclusion
    .stable_element
  )

  stable_eta_squared = (
    data[
      "stable_eta_squared_step"
    ].conclusion
    .stable_element
  )

  assert (
    stable_eta_squared
    == Composition(
      left=stable_eta,
      right=stable_eta,
    )
  )


def test_phase78_8b_does_not_require_stable_composition_typing():
  data = build_phase78_8b_data()

  stable_eta_squared = (
    data[
      "stable_eta_squared_step"
    ].conclusion
    .stable_element
  )

  assert not (
    stable_eta_squared
    .is_type_compatible()
  )


def test_phase78_8b_stable_square_preserves_finite_generator():
  data = build_phase78_8b_data()

  assert (
    data[
      "stable_eta_squared_step"
    ].conclusion
    .source_generator
    == data[
      "eta4_squared"
    ]
  )


def test_phase78_8b_stable_square_preserves_stable_eta_provenance():
  data = build_phase78_8b_data()

  assert (
    data[
      "stable_eta_squared_step"
    ].conclusion
    .stable_eta_definition
    == data[
      "stable_eta_step"
    ].conclusion
  )


def test_phase78_8b_stable_square_uses_exact_dependencies():
  data = build_phase78_8b_data()

  assert (
    data[
      "stable_eta_squared_step"
    ].premises
    == (
      data[
        "eta4_definition_step"
      ],
      data[
        "eta5_definition_step"
      ],
      data[
        "stable_eta_step"
      ],
      data[
        "identification_step"
      ],
    )
  )


def test_phase78_8b_derives_g2_two_primary_z2_eta_squared():
  data = build_phase78_8b_data()

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


def test_phase78_8b_final_group_is_g2_two_primary():
  data = build_phase78_8b_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    == StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=2,
      ),
      prime=2,
    )
  )


def test_phase78_8b_final_group_has_order_two():
  data = build_phase78_8b_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .order
    == 2
  )


def test_phase78_8b_final_generator_is_stable_eta_squared():
  data = build_phase78_8b_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == data[
      "stable_eta_squared_step"
    ].conclusion
    .stable_element
  )


def test_phase78_8b_final_uses_exact_dependencies():
  data = build_phase78_8b_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi6_4_step"
      ],
      data[
        "identification_step"
      ],
      data[
        "stable_eta_squared_step"
      ],
    )
  )


def test_phase78_8b_final_not_present_initially():
  data = build_phase78_8b_data()

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


def test_phase78_8b_square_rejects_given_stable_eta():
  data = build_phase78_8b_data()

  given_stable_eta = ProofStep(
    conclusion=(
      data[
        "stable_eta_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "stable_eta_squared_rule"
    ],
    (
      data[
        "eta4_definition_step"
      ],
      data[
        "eta5_definition_step"
      ],
      given_stable_eta,
      data[
        "identification_step"
      ],
    ),
  ) is None


def test_phase78_8b_transport_rejects_given_source_relation():
  data = build_phase78_8b_data()

  given_source_relation = ProofStep(
    conclusion=(
      data[
        "pi6_4_step"
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
        "stable_eta_squared_step"
      ],
    ),
  ) is None


def test_phase78_8b_transport_rejects_given_square_definition():
  data = build_phase78_8b_data()

  given_square = ProofStep(
    conclusion=(
      data[
        "stable_eta_squared_step"
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
        "pi6_4_step"
      ],
      data[
        "identification_step"
      ],
      given_square,
    ),
  ) is None


def test_phase78_8b_reaches_fixed_point():
  data = build_phase78_8b_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


