from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from probes.probe_phase56_capabilities import (
  build_phase56_representative_result,
)
from test_phase70_prop59_integration import (
  build_phase70_10_data,
)
from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  TodaProp59FiniteDimensionalStatement,
  toda_prop511_pi8_2_eta2_nu_prime_eta6_squared_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase73_3_data():
  phase56 = (
    build_phase56_representative_result()
  )

  phase70 = (
    build_phase70_10_data()
  )

  composition_isomorphism_step = (
    phase56[
      "composition_isomorphism_steps"
    ][
      0
    ]
  )

  prop59_step = (
    phase70[
      "integration_step"
    ]
  )

  pi8_3_relation = (
    prop59_step
    .conclusion
    .pi8_3_group_relation
  )

  nu_prime_eta6_squared = (
    pi8_3_relation
    .rhs
    .generator
  )

  nu_prime = (
    nu_prime_eta6_squared
    .left
  )

  eta6_squared = (
    nu_prime_eta6_squared
    .right
  )

  eta_6 = (
    eta6_squared.left
  )

  eta_7 = (
    eta6_squared.right
  )

  eta_2 = (
    composition_isomorphism_step
    .conclusion
    .composition
    .left
  )

  eta2_nu_prime_eta6_squared = (
    Composition(
      left=eta_2,
      right=nu_prime_eta6_squared,
    )
  )

  expected_statement = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=2,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=(
        eta2_nu_prime_eta6_squared
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  rule = (
    toda_prop511_pi8_2_eta2_nu_prime_eta6_squared_inference_rule()
  )

  premise_steps = (
    prop59_step,
    composition_isomorphism_step,
  )

  match = find_inference_match(
    rule,
    premise_steps,
  )

  assert match is not None

  final_step = (
    apply_inference_match(
      match
    )
  )

  return {
    "phase56": phase56,
    "phase70": phase70,
    "composition_isomorphism_step": (
      composition_isomorphism_step
    ),
    "prop59_step": prop59_step,
    "pi8_3_relation": pi8_3_relation,
    "nu_prime_eta6_squared": (
      nu_prime_eta6_squared
    ),
    "nu_prime": nu_prime,
    "eta6_squared": eta6_squared,
    "eta_6": eta_6,
    "eta_7": eta_7,
    "eta_2": eta_2,
    "eta2_nu_prime_eta6_squared": (
      eta2_nu_prime_eta6_squared
    ),
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "match": match,
    "final_step": final_step,
  }


def test_phase73_3_reuses_derived_prop59():
  data = build_phase73_3_data()

  assert isinstance(
    data[
      "prop59_step"
    ].conclusion,
    TodaProp59FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop59_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_3_reuses_derived_toda52():
  data = build_phase73_3_data()

  assert isinstance(
    data[
      "composition_isomorphism_step"
    ].conclusion,
    Toda52CompositionIsomorphismStatement,
  )

  assert (
    data[
      "composition_isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_3_source_is_pi8_3_order_two():
  data = build_phase73_3_data()

  relation = (
    data[
      "pi8_3_relation"
    ]
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=3,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 2
  )


def test_phase73_3_source_generator_is_nu_prime_eta6_squared():
  data = build_phase73_3_data()

  generator = (
    data[
      "nu_prime_eta6_squared"
    ]
  )

  assert isinstance(
    generator,
    Composition,
  )

  assert (
    generator.left
    is data[
      "nu_prime"
    ]
  )

  assert (
    generator.right
    is data[
      "eta6_squared"
    ]
  )

  assert isinstance(
    data[
      "eta6_squared"
    ],
    Composition,
  )

  assert (
    data[
      "eta6_squared"
    ].left
    is data[
      "eta_6"
    ]
  )

  assert (
    data[
      "eta6_squared"
    ].right
    is data[
      "eta_7"
    ]
  )

  assert (
    data[
      "nu_prime"
    ].generator
    == GeneratorSymbol(
      family="ν",
      decoration="′",
    )
  )

  assert (
    data[
      "eta_6"
    ].generator
    == GeneratorSymbol(
      family="η",
      index=6,
    )
  )

  assert (
    data[
      "eta_7"
    ].generator
    == GeneratorSymbol(
      family="η",
      index=7,
    )
  )


def test_phase73_3_toda52_is_eta2_composition_isomorphism():
  data = build_phase73_3_data()

  statement = (
    data[
      "composition_isomorphism_step"
    ].conclusion
  )

  assert isinstance(
    statement.composition,
    Composition,
  )

  assert (
    statement.composition.left
    is data[
      "eta_2"
    ]
  )

  assert (
    data[
      "eta_2"
    ].generator
    == GeneratorSymbol(
      family="η",
      index=2,
    )
  )


def test_phase73_3_rule_matches_dependencies():
  data = build_phase73_3_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase73_3_derives_pi8_2():
  data = build_phase73_3_data()

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


def test_phase73_3_target_is_pi8_2_order_two():
  data = build_phase73_3_data()

  relation = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=2,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 2
  )


def test_phase73_3_generator_is_eta2_nu_prime_eta6_squared():
  data = build_phase73_3_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == Composition(
      left=data[
        "eta_2"
      ],
      right=data[
        "nu_prime_eta6_squared"
      ],
    )
  )


def test_phase73_3_preserves_source_generator_object():
  data = build_phase73_3_data()

  generator = (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
  )

  assert (
    generator.right
    is data[
      "nu_prime_eta6_squared"
    ]
  )


def test_phase73_3_final_direct_premises_are_prop59_and_toda52():
  data = build_phase73_3_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "prop59_step"
      ],
      data[
        "composition_isomorphism_step"
      ],
    )
  )


def test_phase73_3_rejects_given_prop59():
  data = build_phase73_3_data()

  given_prop59 = ProofStep(
    conclusion=(
      data[
        "prop59_step"
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
      given_prop59,
      data[
        "composition_isomorphism_step"
      ],
    ),
  ) is None


def test_phase73_3_rejects_given_toda52():
  data = build_phase73_3_data()

  given_toda52 = ProofStep(
    conclusion=(
      data[
        "composition_isomorphism_step"
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
      data[
        "prop59_step"
      ],
      given_toda52,
    ),
  ) is None


def test_phase73_3_rejects_wrong_pi8_3_group():
  data = build_phase73_3_data()

  prop59 = (
    data[
      "prop59_step"
    ].conclusion
  )

  wrong_pi8_3 = replace(
    prop59.pi8_3_group_relation,
    lhs=TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=3,
    ),
  )

  wrong_prop59 = replace(
    prop59,
    pi8_3_group_relation=wrong_pi8_3,
  )

  wrong_step = ProofStep(
    conclusion=wrong_prop59,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "composition_isomorphism_step"
      ],
    ),
  ) is None


def test_phase73_3_rejects_wrong_pi8_3_order():
  data = build_phase73_3_data()

  prop59 = (
    data[
      "prop59_step"
    ].conclusion
  )

  wrong_pi8_3 = replace(
    prop59.pi8_3_group_relation,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=(
        data[
          "nu_prime_eta6_squared"
        ]
      ),
    ),
  )

  wrong_prop59 = replace(
    prop59,
    pi8_3_group_relation=wrong_pi8_3,
  )

  wrong_step = ProofStep(
    conclusion=wrong_prop59,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "composition_isomorphism_step"
      ],
    ),
  ) is None


def test_phase73_3_rejects_wrong_pi8_3_generator():
  data = build_phase73_3_data()

  prop59 = (
    data[
      "prop59_step"
    ].conclusion
  )

  wrong_eta_7 = HomotopyElement(
    name="η₈",
    dimension=8,
    source=9,
    target=8,
    generator=GeneratorSymbol(
      family="η",
      index=8,
    ),
  )

  wrong_generator = Composition(
    left=data[
      "nu_prime"
    ],
    right=Composition(
      left=data[
        "eta_6"
      ],
      right=wrong_eta_7,
    ),
  )

  wrong_pi8_3 = replace(
    prop59.pi8_3_group_relation,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=wrong_generator,
    ),
  )

  wrong_prop59 = replace(
    prop59,
    pi8_3_group_relation=wrong_pi8_3,
  )

  wrong_step = ProofStep(
    conclusion=wrong_prop59,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "composition_isomorphism_step"
      ],
    ),
  ) is None


def test_phase73_3_rejects_wrong_toda52_source():
  data = build_phase73_3_data()

  isomorphism = (
    data[
      "composition_isomorphism_step"
    ].conclusion
  )

  wrong_isomorphism = replace(
    isomorphism,
    source_group=TodaPrimaryGroup(
      group_dimension=(
        isomorphism
        .source_group
        .group_dimension
      ),
      sphere_dimension=4,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_isomorphism,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "prop59_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase73_3_rejects_wrong_toda52_target():
  data = build_phase73_3_data()

  isomorphism = (
    data[
      "composition_isomorphism_step"
    ].conclusion
  )

  wrong_isomorphism = replace(
    isomorphism,
    target_group=TodaPrimaryGroup(
      group_dimension=(
        isomorphism
        .source_group
        .group_dimension
      ),
      sphere_dimension=3,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_isomorphism,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "prop59_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase73_3_rejects_wrong_toda52_left_composition():
  data = build_phase73_3_data()

  isomorphism = (
    data[
      "composition_isomorphism_step"
    ].conclusion
  )

  wrong_eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  wrong_isomorphism = replace(
    isomorphism,
    composition=Composition(
      left=wrong_eta_3,
      right=(
        isomorphism
        .composition
        .right
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_isomorphism,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "prop59_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase73_3_final_result_is_not_given():
  data = build_phase73_3_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )



