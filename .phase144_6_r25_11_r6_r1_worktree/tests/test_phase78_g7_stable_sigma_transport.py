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
from test_phase75_pi16_9_sigma9 import (
  build_phase75_8c_data,
)
from toda_rules import (
  Toda45StableTwoPrimaryIdentificationStatement,
  TodaStableSigmaDefinitionStatement,
  toda_45_stable_two_primary_identification_inference_rule,
  toda_prop515_g7_two_primary_finite_cyclic_inference_rule,
  toda_prop515_stable_sigma_definition_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase78_6_data():
  phase75_8c = (
    build_phase75_8c_data()
  )

  pi16_9_step = (
    phase75_8c[
      "final_step"
    ]
  )

  sigma9_definition_step = (
    phase75_8c[
      "sigma9_definition_step"
    ]
  )

  source_group = TodaPrimaryGroup(
    group_dimension=16,
    sphere_dimension=9,
  )

  source_group_step = ProofStep(
    conclusion=source_group,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  identification_rule = (
    toda_45_stable_two_primary_identification_inference_rule()
  )

  stable_sigma_rule = (
    toda_prop515_stable_sigma_definition_inference_rule()
  )

  transport_rule = (
    toda_prop515_g7_two_primary_finite_cyclic_inference_rule()
  )

  rules = (
    identification_rule,
    stable_sigma_rule,
    transport_rule,
  )

  premise_steps = (
    pi16_9_step,
    sigma9_definition_step,
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
          stem=7,
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

  stable_sigma_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaStableSigmaDefinitionStatement,
    )
  )

  expected_final = Relation(
    lhs=StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=7,
      ),
      prime=2,
    ),
    rhs=FiniteCyclicGroup(
      order=16,
      generator=(
        stable_sigma_step
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
    "phase75_8c": phase75_8c,
    "pi16_9_step": pi16_9_step,
    "sigma9_definition_step": (
      sigma9_definition_step
    ),
    "source_group": source_group,
    "source_group_step": (
      source_group_step
    ),
    "identification_rule": (
      identification_rule
    ),
    "stable_sigma_rule": (
      stable_sigma_rule
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
    "stable_sigma_step": (
      stable_sigma_step
    ),
    "expected_final": (
      expected_final
    ),
    "final_step": final_step,
  }


def test_phase78_6_reuses_derived_pi16_9_relation():
  data = build_phase78_6_data()

  assert (
    data[
      "pi16_9_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi16_9_step"
    ].conclusion
    .lhs
    == TodaPrimaryGroup(
      group_dimension=16,
      sphere_dimension=9,
    )
  )

  assert (
    data[
      "pi16_9_step"
    ].conclusion
    .rhs
    .order
    == 16
  )


def test_phase78_6_reuses_derived_sigma9_definition():
  data = build_phase78_6_data()

  sigma9_definition = (
    data[
      "sigma9_definition_step"
    ].conclusion
  )

  assert (
    data[
      "sigma9_definition_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    sigma9_definition.index
    == 9
  )

  assert (
    sigma9_definition.element
    == data[
      "pi16_9_step"
    ].conclusion
    .rhs
    .generator
  )


def test_phase78_6_derives_stable_identification():
  data = build_phase78_6_data()

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
        stem=7,
      ),
      prime=2,
    )
  )


def test_phase78_6_derives_stable_sigma_definition():
  data = build_phase78_6_data()

  assert (
    data[
      "stable_sigma_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "stable_sigma_step"
    ].conclusion,
    TodaStableSigmaDefinitionStatement,
  )


def test_phase78_6_stable_sigma_has_expected_stem():
  data = build_phase78_6_data()

  stable_sigma = (
    data[
      "stable_sigma_step"
    ].conclusion
    .stable_element
  )

  assert stable_sigma.name == "σ"
  assert stable_sigma.dimension == 7

  assert stable_sigma.source is None
  assert stable_sigma.target is None

  assert (
    stable_sigma.generator
    == GeneratorSymbol(
      family="σ",
    )
  )


def test_phase78_6_stable_sigma_preserves_sigma9_source_definition():
  data = build_phase78_6_data()

  assert (
    data[
      "stable_sigma_step"
    ].conclusion
    .source_definition
    == data[
      "sigma9_definition_step"
    ].conclusion
  )


def test_phase78_6_stable_sigma_uses_exact_dependencies():
  data = build_phase78_6_data()

  assert (
    data[
      "stable_sigma_step"
    ].premises
    == (
      data[
        "sigma9_definition_step"
      ],
      data[
        "identification_step"
      ],
    )
  )


def test_phase78_6_derives_g7_two_primary_z16_sigma():
  data = build_phase78_6_data()

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


def test_phase78_6_final_group_is_g7_two_primary():
  data = build_phase78_6_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    == StablePrimaryComponent(
      group=StableHomotopyGroup(
        stem=7,
      ),
      prime=2,
    )
  )


def test_phase78_6_final_group_has_order_16():
  data = build_phase78_6_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .order
    == 16
  )


def test_phase78_6_final_generator_is_stable_sigma():
  data = build_phase78_6_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == data[
      "stable_sigma_step"
    ].conclusion
    .stable_element
  )


def test_phase78_6_final_uses_exact_dependencies():
  data = build_phase78_6_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi16_9_step"
      ],
      data[
        "identification_step"
      ],
      data[
        "stable_sigma_step"
      ],
    )
  )


def test_phase78_6_final_not_present_initially():
  data = build_phase78_6_data()

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


def test_phase78_6_stable_sigma_rejects_given_identification():
  data = build_phase78_6_data()

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
      "stable_sigma_rule"
    ],
    (
      data[
        "sigma9_definition_step"
      ],
      given_identification,
    ),
  ) is None


def test_phase78_6_transport_rejects_given_source_relation():
  data = build_phase78_6_data()

  given_relation = ProofStep(
    conclusion=(
      data[
        "pi16_9_step"
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
      given_relation,
      data[
        "identification_step"
      ],
      data[
        "stable_sigma_step"
      ],
    ),
  ) is None


def test_phase78_6_transport_rejects_given_stable_sigma():
  data = build_phase78_6_data()

  given_stable_sigma = ProofStep(
    conclusion=(
      data[
        "stable_sigma_step"
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
        "pi16_9_step"
      ],
      data[
        "identification_step"
      ],
      given_stable_sigma,
    ),
  ) is None


def test_phase78_6_reaches_fixed_point():
  data = build_phase78_6_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


