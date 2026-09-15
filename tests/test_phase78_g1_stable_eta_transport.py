from functools import lru_cache

from expression import (
  GeneratorSymbol,
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
from toda_rules import (
  Toda45StableTwoPrimaryIdentificationStatement,
  TodaStableEtaDefinitionStatement,
  toda_45_stable_two_primary_identification_inference_rule,
  toda_eta_family_definition_statement,
  toda_prop51_g1_two_primary_finite_cyclic_inference_rule,
  toda_prop51_stable_eta_definition_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase78_8a_data():
  eta3_definition = (
    toda_eta_family_definition_statement(
      3
    )
  )

  eta3_definition_step = ProofStep(
    conclusion=eta3_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pi4_3_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=(
        eta3_definition.element
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  pi4_3_step = ProofStep(
    conclusion=pi4_3_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
    note=(
      "Existing Phase 50 derived result "
      "pi_4^3=Z/2{eta_3}."
    ),
  )

  source_group = (
    pi4_3_relation.lhs
  )

  source_group_step = ProofStep(
    conclusion=source_group,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  identification_rule = (
    toda_45_stable_two_primary_identification_inference_rule()
  )

  stable_eta_rule = (
    toda_prop51_stable_eta_definition_inference_rule()
  )

  transport_rule = (
    toda_prop51_g1_two_primary_finite_cyclic_inference_rule()
  )

  rules = (
    identification_rule,
    stable_eta_rule,
    transport_rule,
  )

  premise_steps = (
    eta3_definition_step,
    pi4_3_step,
    source_group_step,
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
          stem=1,
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

  stable_eta_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaStableEtaDefinitionStatement,
    )
  )

  expected_final = Relation(
    lhs=StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=1,
      ),
      prime=2,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=(
        stable_eta_step
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
    "eta3_definition": (
      eta3_definition
    ),
    "eta3_definition_step": (
      eta3_definition_step
    ),
    "pi4_3_relation": (
      pi4_3_relation
    ),
    "pi4_3_step": (
      pi4_3_step
    ),
    "source_group": source_group,
    "source_group_step": (
      source_group_step
    ),
    "identification_rule": (
      identification_rule
    ),
    "stable_eta_rule": (
      stable_eta_rule
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
    "stable_eta_step": (
      stable_eta_step
    ),
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase78_8a_eta3_definition_is_given():
  data = build_phase78_8a_data()

  assert (
    data[
      "eta3_definition_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase78_8a_eta3_has_expected_structure():
  data = build_phase78_8a_data()

  eta_3 = (
    data[
      "eta3_definition"
    ].element
  )

  assert eta_3.name == "η₃"
  assert eta_3.dimension == 3
  assert eta_3.source == 4
  assert eta_3.target == 3

  assert (
    eta_3.generator
    == GeneratorSymbol(
      family="η",
      index=3,
    )
  )


def test_phase78_8a_source_group_relation_is_inference():
  data = build_phase78_8a_data()

  assert (
    data[
      "pi4_3_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi4_3_step"
    ].conclusion
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=4,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=(
          data[
            "eta3_definition"
          ].element
        ),
      ),
      relation_type=(
        RelationType.EQUALITY
      ),
    )
  )


def test_phase78_8a_derives_stable_identification():
  data = build_phase78_8a_data()

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
        stem=1,
      ),
      prime=2,
    )
  )


def test_phase78_8a_derives_stable_eta_definition():
  data = build_phase78_8a_data()

  assert (
    data[
      "stable_eta_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "stable_eta_step"
    ].conclusion,
    TodaStableEtaDefinitionStatement,
  )


def test_phase78_8a_stable_eta_has_expected_structure():
  data = build_phase78_8a_data()

  stable_eta = (
    data[
      "stable_eta_step"
    ].conclusion
    .stable_element
  )

  assert stable_eta.name == "η"
  assert stable_eta.dimension == 1
  assert stable_eta.source is None
  assert stable_eta.target is None

  assert (
    stable_eta.generator
    == GeneratorSymbol(
      family="η",
    )
  )


def test_phase78_8a_stable_eta_preserves_eta3_definition():
  data = build_phase78_8a_data()

  assert (
    data[
      "stable_eta_step"
    ].conclusion
    .source_definition
    == data[
      "eta3_definition"
    ]
  )


def test_phase78_8a_stable_eta_uses_exact_dependencies():
  data = build_phase78_8a_data()

  assert (
    data[
      "stable_eta_step"
    ].premises
    == (
      data[
        "eta3_definition_step"
      ],
      data[
        "identification_step"
      ],
    )
  )


def test_phase78_8a_derives_g1_two_primary_z2_eta():
  data = build_phase78_8a_data()

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


def test_phase78_8a_final_group_is_g1_two_primary():
  data = build_phase78_8a_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    == StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=1,
      ),
      prime=2,
    )
  )


def test_phase78_8a_final_group_has_order_two():
  data = build_phase78_8a_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .order
    == 2
  )


def test_phase78_8a_final_generator_is_stable_eta():
  data = build_phase78_8a_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == data[
      "stable_eta_step"
    ].conclusion
    .stable_element
  )


def test_phase78_8a_final_uses_exact_dependencies():
  data = build_phase78_8a_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi4_3_step"
      ],
      data[
        "identification_step"
      ],
      data[
        "stable_eta_step"
      ],
    )
  )


def test_phase78_8a_final_not_present_initially():
  data = build_phase78_8a_data()

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


def test_phase78_8a_stable_eta_rejects_given_identification():
  data = build_phase78_8a_data()

  given_identification = ProofStep(
    conclusion=(
      data[
        "identification_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "stable_eta_rule"
    ],
    (
      data[
        "eta3_definition_step"
      ],
      given_identification,
    ),
  ) is None


def test_phase78_8a_transport_rejects_given_source_relation():
  data = build_phase78_8a_data()

  given_source_relation = ProofStep(
    conclusion=(
      data[
        "pi4_3_step"
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
        "stable_eta_step"
      ],
    ),
  ) is None


def test_phase78_8a_transport_rejects_given_stable_eta():
  data = build_phase78_8a_data()

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
      "transport_rule"
    ],
    (
      data[
        "pi4_3_step"
      ],
      data[
        "identification_step"
      ],
      given_stable_eta,
    ),
  ) is None


def test_phase78_8a_reaches_fixed_point():
  data = build_phase78_8a_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


