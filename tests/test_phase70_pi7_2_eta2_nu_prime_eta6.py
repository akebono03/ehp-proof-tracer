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
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from probes.probe_phase56_capabilities import (
  build_phase56_representative_result,
)
from test_phase68_pi7_3_nu_prime_eta6 import (
  build_phase68_3_data,
)
from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  toda_prop59_pi7_2_eta2_nu_prime_eta6_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase70_2_data():
  phase56 = (
    build_phase56_representative_result()
  )

  phase68_3 = (
    build_phase68_3_data()
  )

  composition_isomorphism_step = (
    phase56[
      "composition_isomorphism_steps"
    ][
      0
    ]
  )

  pi7_3_step = (
    phase68_3[
      "final_step"
    ]
  )

  nu_prime_eta6 = (
    pi7_3_step
    .conclusion
    .rhs
    .generator
  )

  nu_prime = (
    nu_prime_eta6.left
  )

  eta_6 = (
    nu_prime_eta6.right
  )

  eta_2 = (
    composition_isomorphism_step
    .conclusion
    .composition
    .left
  )

  eta2_nu_prime_eta6 = (
    Composition(
      left=eta_2,
      right=nu_prime_eta6,
    )
  )

  expected_statement = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=2,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta2_nu_prime_eta6,
    ),
    relation_type=RelationType.EQUALITY,
  )

  rule = (
    toda_prop59_pi7_2_eta2_nu_prime_eta6_inference_rule()
  )

  premise_steps = (
    pi7_3_step,
    composition_isomorphism_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase56": phase56,
    "phase68_3": phase68_3,
    "composition_isomorphism_step": (
      composition_isomorphism_step
    ),
    "pi7_3_step": pi7_3_step,
    "nu_prime_eta6": (
      nu_prime_eta6
    ),
    "nu_prime": nu_prime,
    "eta_6": eta_6,
    "eta_2": eta_2,
    "eta2_nu_prime_eta6": (
      eta2_nu_prime_eta6
    ),
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "final_step": final_step,
  }


def test_phase70_2_reuses_derived_pi7_3():
  data = build_phase70_2_data()

  assert (
    data[
      "pi7_3_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi7_3_step"
    ].conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=3,
    )
  )


def test_phase70_2_reuses_derived_toda52():
  data = build_phase70_2_data()

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


def test_phase70_2_source_is_pi7_3_order_two():
  data = build_phase70_2_data()

  group = (
    data[
      "pi7_3_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert group.order == 2


def test_phase70_2_source_generator_is_nu_prime_eta6():
  data = build_phase70_2_data()

  generator = (
    data[
      "nu_prime_eta6"
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
      "eta_6"
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


def test_phase70_2_toda52_is_eta2_composition_isomorphism():
  data = build_phase70_2_data()

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


def test_phase70_2_rule_matches_dependencies():
  data = build_phase70_2_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase70_2_derives_pi7_2():
  data = build_phase70_2_data()

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


def test_phase70_2_target_group_is_pi7_2():
  data = build_phase70_2_data()

  assert (
    data[
      "final_step"
    ].conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=2,
    )
  )


def test_phase70_2_target_is_order_two():
  data = build_phase70_2_data()

  group = (
    data[
      "final_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert group.order == 2


def test_phase70_2_generator_is_eta2_nu_prime_eta6():
  data = build_phase70_2_data()

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
        "nu_prime_eta6"
      ],
    )
  )


def test_phase70_2_preserves_upstream_generator_object():
  data = build_phase70_2_data()

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
      "nu_prime_eta6"
    ]
  )


def test_phase70_2_provenance_uses_exactly_two_dependencies():
  data = build_phase70_2_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi7_3_step"
      ],
      data[
        "composition_isomorphism_step"
      ],
    )
  )


def test_phase70_2_rejects_given_pi7_3():
  data = build_phase70_2_data()

  given_pi7_3 = ProofStep(
    conclusion=(
      data[
        "pi7_3_step"
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
      given_pi7_3,
      data[
        "composition_isomorphism_step"
      ],
    ),
  ) is None


def test_phase70_2_rejects_given_toda52():
  data = build_phase70_2_data()

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
        "pi7_3_step"
      ],
      given_toda52,
    ),
  ) is None


def test_phase70_2_rejects_wrong_source_group():
  data = build_phase70_2_data()

  wrong_relation = replace(
    data[
      "pi7_3_step"
    ].conclusion,
    lhs=TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=3,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
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


def test_phase70_2_rejects_wrong_source_order():
  data = build_phase70_2_data()

  wrong_relation = replace(
    data[
      "pi7_3_step"
    ].conclusion,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=data[
        "nu_prime_eta6"
      ],
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
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


def test_phase70_2_rejects_wrong_source_generator():
  data = build_phase70_2_data()

  wrong_eta_6 = HomotopyElement(
    name="η₅",
    dimension=5,
    source=6,
    target=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )

  wrong_generator = Composition(
    left=data[
      "nu_prime"
    ],
    right=wrong_eta_6,
  )

  wrong_relation = replace(
    data[
      "pi7_3_step"
    ].conclusion,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=wrong_generator,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
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


def test_phase70_2_rejects_wrong_toda52_target():
  data = build_phase70_2_data()

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
        "pi7_3_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase70_2_rejects_wrong_toda52_left_composition():
  data = build_phase70_2_data()

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
        "pi7_3_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase70_2_final_result_is_not_given():
  data = build_phase70_2_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "expected_statement"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase70_2_reaches_fixed_point_in_one_round():
  data = build_phase70_2_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    data[
      "result"
    ].round_count
    == 1
  )

  assert (
    data[
      "final_step"
    ]
    in data[
      "result"
    ].round_results[
      0
    ].new_steps
  )


