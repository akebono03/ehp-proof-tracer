from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  MapApplication,
  Multiple,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_DELTA_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from test_phase59_prop53_integration import (
  build_phase59_8_data,
)
from test_phase68_nu_n_eta_n_plus_three_zero import (
  build_phase68_9_data,
)
from test_phase70_prop59_integration import (
  build_phase70_10_data,
)
from test_phase72_lemma510_core_inference import (
  build_phase72_3_data,
)
from toda_rules import (
  Toda54IndeterminacyGeneratorStatement,
  TodaLemma510BracketModuloStatement,
  TodaLemma510BracketPlusSuspensionImageStatement,
  TodaLemma510SuspensionImageInDoubleStatement,
  TodaProp53FiniteDimensionalStatement,
  toda_lemma510_indeterminacy_inference_rule,
  toda_lemma510_modulo_integration_inference_rule,
  toda_lemma510_suspension_image_in_double_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase72_4_data():
  phase72_3 = (
    build_phase72_3_data()
  )

  phase68_9 = (
    build_phase68_9_data()
  )

  phase70_10 = (
    build_phase70_10_data()
  )

  phase59_8 = (
    build_phase59_8_data()
  )

  core_step = (
    phase72_3[
      "final_step"
    ]
  )

  nu6_eta9_zero_step = (
    phase68_9[
      "nu6_eta9_zero_step"
    ]
  )

  pi10_5_step = (
    phase70_10[
      "pi10_5_step"
    ]
  )

  pi11_6_step = (
    phase70_10[
      "pi11_6_step"
    ]
  )

  prop53_step = (
    phase59_8[
      "integration_step"
    ]
  )

  indeterminacy_rule = (
    toda_lemma510_indeterminacy_inference_rule()
  )

  indeterminacy_premises = (
    prop53_step,
    nu6_eta9_zero_step,
    pi11_6_step,
  )

  indeterminacy_match = (
    find_inference_match(
      indeterminacy_rule,
      indeterminacy_premises,
    )
  )

  assert (
    indeterminacy_match
    is not None
  )

  indeterminacy_step = (
    apply_inference_match(
      indeterminacy_match
    )
  )

  image_rule = (
    toda_lemma510_suspension_image_in_double_inference_rule()
  )

  image_premises = (
    pi10_5_step,
    pi11_6_step,
  )

  image_match = find_inference_match(
    image_rule,
    image_premises,
  )

  assert (
    image_match
    is not None
  )

  image_step = (
    apply_inference_match(
      image_match
    )
  )

  integration_rule = (
    toda_lemma510_modulo_integration_inference_rule()
  )

  integration_premises = (
    core_step,
    indeterminacy_step,
    image_step,
  )

  integration_match = (
    find_inference_match(
      integration_rule,
      integration_premises,
    )
  )

  assert (
    integration_match
    is not None
  )

  final_step = (
    apply_inference_match(
      integration_match
    )
  )

  return {
    "phase72_3": phase72_3,
    "phase68_9": phase68_9,
    "phase70_10": phase70_10,
    "phase59_8": phase59_8,
    "core_step": core_step,
    "nu6_eta9_zero_step": (
      nu6_eta9_zero_step
    ),
    "pi10_5_step": pi10_5_step,
    "pi11_6_step": pi11_6_step,
    "prop53_step": prop53_step,
    "indeterminacy_rule": (
      indeterminacy_rule
    ),
    "indeterminacy_premises": (
      indeterminacy_premises
    ),
    "indeterminacy_step": (
      indeterminacy_step
    ),
    "image_rule": image_rule,
    "image_premises": (
      image_premises
    ),
    "image_step": image_step,
    "integration_rule": (
      integration_rule
    ),
    "integration_premises": (
      integration_premises
    ),
    "final_step": final_step,
  }


def test_phase72_4_reuses_phase72_3_core():
  data = build_phase72_4_data()

  assert isinstance(
    data[
      "core_step"
    ].conclusion,
    TodaLemma510BracketPlusSuspensionImageStatement,
  )

  assert (
    data[
      "core_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_4_reuses_prop53():
  data = build_phase72_4_data()

  assert isinstance(
    data[
      "prop53_step"
    ].conclusion,
    TodaProp53FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop53_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_4_reuses_nu6_eta9_zero():
  data = build_phase72_4_data()

  step = (
    data[
      "nu6_eta9_zero_step"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert (
    step.conclusion.relation_type
    == RelationType.ZERO
  )


def test_phase72_4_indeterminacy_is_inference():
  data = build_phase72_4_data()

  assert isinstance(
    data[
      "indeterminacy_step"
    ].conclusion,
    Toda54IndeterminacyGeneratorStatement,
  )

  assert (
    data[
      "indeterminacy_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_4_indeterminacy_generator_is_double_delta_iota13():
  data = build_phase72_4_data()

  generator = (
    data[
      "indeterminacy_step"
    ].conclusion
    .generator
  )

  assert isinstance(
    generator,
    Multiple,
  )

  assert (
    generator.coefficient
    == 2
  )

  assert isinstance(
    generator.expression,
    MapApplication,
  )

  assert (
    generator.expression.map
    == EHP_DELTA_MAP
  )

  assert (
    generator.expression
    .expression
    .generator
    == GeneratorSymbol(
      family="ι",
      index=13,
    )
  )


def test_phase72_4_indeterminacy_uses_exact_dependencies():
  data = build_phase72_4_data()

  assert (
    data[
      "indeterminacy_step"
    ].premises
    == data[
      "indeterminacy_premises"
    ]
  )


def test_phase72_4_pi10_5_is_finite_order_two():
  data = build_phase72_4_data()

  group = (
    data[
      "pi10_5_step"
    ].conclusion
    .rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert (
    group.order
    == 2
  )


def test_phase72_4_pi11_6_is_free_cyclic():
  data = build_phase72_4_data()

  assert isinstance(
    data[
      "pi11_6_step"
    ].conclusion
    .rhs,
    FreeCyclicGroup,
  )


def test_phase72_4_image_containment_is_inference():
  data = build_phase72_4_data()

  assert isinstance(
    data[
      "image_step"
    ].conclusion,
    TodaLemma510SuspensionImageInDoubleStatement,
  )

  assert (
    data[
      "image_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_4_image_containment_map_is_expected():
  data = build_phase72_4_data()

  assert (
    data[
      "image_step"
    ].conclusion
    .suspension_map
    == TodaSuspensionMap(
      source_group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=6,
      ),
    )
  )


def test_phase72_4_image_containment_modulus_is_two():
  data = build_phase72_4_data()

  assert (
    data[
      "image_step"
    ].conclusion.modulus
    == 2
  )


def test_phase72_4_image_uses_exact_dependencies():
  data = build_phase72_4_data()

  assert (
    data[
      "image_step"
    ].premises
    == data[
      "image_premises"
    ]
  )


def test_phase72_4_derives_final_modulo_statement():
  data = build_phase72_4_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaLemma510BracketModuloStatement,
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_4_final_is_not_given():
  data = build_phase72_4_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase72_4_final_reuses_core_element():
  data = build_phase72_4_data()

  assert (
    data[
      "final_step"
    ].conclusion.element
    is data[
      "core_step"
    ].conclusion.element
  )


def test_phase72_4_final_reuses_core_bracket():
  data = build_phase72_4_data()

  assert (
    data[
      "final_step"
    ].conclusion.bracket
    is data[
      "core_step"
    ].conclusion.bracket
  )


def test_phase72_4_final_ambient_group_is_pi11_6():
  data = build_phase72_4_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .ambient_group
    == TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )


def test_phase72_4_final_modulus_is_two():
  data = build_phase72_4_data()

  assert (
    data[
      "final_step"
    ].conclusion.modulus
    == 2
  )


def test_phase72_4_final_uses_exact_three_dependencies():
  data = build_phase72_4_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "core_step"
      ],
      data[
        "indeterminacy_step"
      ],
      data[
        "image_step"
      ],
    )
  )


def test_phase72_4_rejects_given_indeterminacy():
  data = build_phase72_4_data()

  given = ProofStep(
    conclusion=(
      data[
        "indeterminacy_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      data[
        "core_step"
      ],
      given,
      data[
        "image_step"
      ],
    ),
  ) is None


def test_phase72_4_rejects_given_image_containment():
  data = build_phase72_4_data()

  given = ProofStep(
    conclusion=(
      data[
        "image_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      data[
        "core_step"
      ],
      data[
        "indeterminacy_step"
      ],
      given,
    ),
  ) is None


def test_phase72_4_rejects_wrong_modulus():
  data = build_phase72_4_data()

  wrong = ProofStep(
    conclusion=replace(
      data[
        "image_step"
      ].conclusion,
      modulus=4,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      data[
        "core_step"
      ],
      data[
        "indeterminacy_step"
      ],
      wrong,
    ),
  ) is None


