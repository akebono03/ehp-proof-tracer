from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
)
from homotopy_groups import (
  FreeCyclicGroup,
  HomotopyGroup,
  StableHomotopyGroup,
  StablePrimaryComponent,
  TodaPrimaryGroup,
)
from low_dimensional_facts import (
  pi_3_3_free_cyclic_fact,
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
  Toda33StableOrdinaryIdentificationStatement,
  TodaStableIotaDefinitionStatement,
  toda_33_g0_free_cyclic_inference_rule,
  toda_33_g0_stable_identification_inference_rule,
  toda_33_stable_iota_definition_inference_rule,
  toda_43_pi3_3_ordinary_free_cyclic_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase78_10_data():
  toda_pi3_3_relation = (
    pi_3_3_free_cyclic_fact()
  )

  toda_pi3_3_step = ProofStep(
    conclusion=toda_pi3_3_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  diagonal_rule = (
    toda_43_pi3_3_ordinary_free_cyclic_inference_rule()
  )

  stable_identification_rule = (
    toda_33_g0_stable_identification_inference_rule()
  )

  stable_iota_rule = (
    toda_33_stable_iota_definition_inference_rule()
  )

  final_rule = (
    toda_33_g0_free_cyclic_inference_rule()
  )

  rules = (
    diagonal_rule,
    stable_identification_rule,
    stable_iota_rule,
    final_rule,
  )

  premise_steps = (
    toda_pi3_3_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  iota_3 = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  expected_ordinary_relation = Relation(
    lhs=HomotopyGroup(
      group_dimension=3,
      sphere_dimension=3,
    ),
    rhs=FreeCyclicGroup(
      generator=iota_3,
    ),
    relation_type=RelationType.EQUALITY,
  )

  ordinary_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_ordinary_relation
    )
  )

  expected_identification = (
    Toda33StableOrdinaryIdentificationStatement(
      source_group=HomotopyGroup(
        group_dimension=3,
        sphere_dimension=3,
      ),
      target_group=StableHomotopyGroup(
        stem=0,
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

  stable_iota_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaStableIotaDefinitionStatement,
    )
  )

  expected_final = Relation(
    lhs=StableHomotopyGroup(
      stem=0,
    ),
    rhs=FreeCyclicGroup(
      generator=(
        stable_iota_step
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
    "toda_pi3_3_relation": (
      toda_pi3_3_relation
    ),
    "toda_pi3_3_step": (
      toda_pi3_3_step
    ),
    "diagonal_rule": diagonal_rule,
    "stable_identification_rule": (
      stable_identification_rule
    ),
    "stable_iota_rule": (
      stable_iota_rule
    ),
    "final_rule": final_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "expected_ordinary_relation": (
      expected_ordinary_relation
    ),
    "ordinary_step": ordinary_step,
    "identification_step": (
      identification_step
    ),
    "stable_iota_step": (
      stable_iota_step
    ),
    "expected_final": expected_final,
    "final_step": final_step,
  }


def test_phase78_10_reuses_existing_diagonal_fact():
  data = build_phase78_10_data()

  assert (
    data[
      "toda_pi3_3_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "toda_pi3_3_step"
    ].conclusion
    .lhs
    == TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    )
  )


def test_phase78_10_diagonal_fact_is_free_cyclic():
  data = build_phase78_10_data()

  assert isinstance(
    data[
      "toda_pi3_3_relation"
    ].rhs,
    FreeCyclicGroup,
  )


def test_phase78_10_diagonal_fact_generator_is_iota3():
  data = build_phase78_10_data()

  assert (
    data[
      "toda_pi3_3_relation"
    ].rhs
    .generator
    == HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )
  )


def test_phase78_10_derives_ordinary_diagonal_relation():
  data = build_phase78_10_data()

  assert (
    data[
      "ordinary_step"
    ].conclusion
    == data[
      "expected_ordinary_relation"
    ]
  )

  assert (
    data[
      "ordinary_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase78_10_ordinary_group_is_not_toda_group():
  data = build_phase78_10_data()

  assert isinstance(
    data[
      "ordinary_step"
    ].conclusion
    .lhs,
    HomotopyGroup,
  )

  assert not isinstance(
    data[
      "ordinary_step"
    ].conclusion
    .lhs,
    TodaPrimaryGroup,
  )


def test_phase78_10_derives_g0_stable_identification():
  data = build_phase78_10_data()

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
    == Toda33StableOrdinaryIdentificationStatement(
      source_group=HomotopyGroup(
        group_dimension=3,
        sphere_dimension=3,
      ),
      target_group=StableHomotopyGroup(
        stem=0,
      ),
    )
  )


def test_phase78_10_g0_is_not_primary_component():
  data = build_phase78_10_data()

  target_group = (
    data[
      "identification_step"
    ].conclusion
    .target_group
  )

  assert isinstance(
    target_group,
    StableHomotopyGroup,
  )

  assert not isinstance(
    target_group,
    StablePrimaryComponent,
  )


def test_phase78_10_derives_stable_iota_definition():
  data = build_phase78_10_data()

  assert (
    data[
      "stable_iota_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "stable_iota_step"
    ].conclusion,
    TodaStableIotaDefinitionStatement,
  )


def test_phase78_10_stable_iota_has_expected_structure():
  data = build_phase78_10_data()

  stable_iota = (
    data[
      "stable_iota_step"
    ].conclusion
    .stable_element
  )

  assert stable_iota.name == "ι"
  assert stable_iota.dimension == 0
  assert stable_iota.source is None
  assert stable_iota.target is None

  assert (
    stable_iota.generator
    == GeneratorSymbol(
      family="ι",
    )
  )


def test_phase78_10_stable_iota_preserves_iota3_source():
  data = build_phase78_10_data()

  assert (
    data[
      "stable_iota_step"
    ].conclusion
    .source_element
    == data[
      "ordinary_step"
    ].conclusion
    .rhs
    .generator
  )


def test_phase78_10_stable_iota_uses_exact_dependencies():
  data = build_phase78_10_data()

  assert (
    data[
      "stable_iota_step"
    ].premises
    == (
      data[
        "ordinary_step"
      ],
      data[
        "identification_step"
      ],
    )
  )


def test_phase78_10_derives_g0_free_cyclic_iota():
  data = build_phase78_10_data()

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


def test_phase78_10_final_group_is_g0():
  data = build_phase78_10_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    == StableHomotopyGroup(
      stem=0,
    )
  )


def test_phase78_10_final_group_is_free_cyclic():
  data = build_phase78_10_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion
    .rhs,
    FreeCyclicGroup,
  )


def test_phase78_10_final_generator_is_stable_iota():
  data = build_phase78_10_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == data[
      "stable_iota_step"
    ].conclusion
    .stable_element
  )


def test_phase78_10_final_uses_exact_dependencies():
  data = build_phase78_10_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "ordinary_step"
      ],
      data[
        "identification_step"
      ],
      data[
        "stable_iota_step"
      ],
    )
  )


def test_phase78_10_final_not_present_initially():
  data = build_phase78_10_data()

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


def test_phase78_10_identification_rejects_given_ordinary_relation():
  data = build_phase78_10_data()

  given_ordinary_relation = ProofStep(
    conclusion=(
      data[
        "ordinary_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "stable_identification_rule"
    ],
    (
      given_ordinary_relation,
    ),
  ) is None


def test_phase78_10_stable_iota_rejects_given_identification():
  data = build_phase78_10_data()

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
      "stable_iota_rule"
    ],
    (
      data[
        "ordinary_step"
      ],
      given_identification,
    ),
  ) is None


def test_phase78_10_final_rejects_given_stable_iota():
  data = build_phase78_10_data()

  given_stable_iota = ProofStep(
    conclusion=(
      data[
        "stable_iota_step"
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
        "ordinary_step"
      ],
      data[
        "identification_step"
      ],
      given_stable_iota,
    ),
  ) is None


def test_phase78_10_reaches_fixed_point():
  data = build_phase78_10_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


