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
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  TodaProp56FiniteDimensionalStatement,
  toda_lemma57_pi6_2_eta2_nu_prime_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase67_6_data():
  phase56 = (
    build_phase56_representative_result()
  )

  phase65_9 = (
    build_phase65_9_data()
  )

  composition_isomorphism_step = (
    phase56[
      "composition_isomorphism_steps"
    ][
      0
    ]
  )

  prop56_step = (
    phase65_9[
      "integration_step"
    ]
  )

  nu_prime = (
    prop56_step
    .conclusion
    .pi6_3_group_relation
    .rhs
    .generator
  )

  eta_2 = (
    composition_isomorphism_step
    .conclusion
    .composition
    .left
  )

  eta2_nu_prime = Composition(
    left=eta_2,
    right=nu_prime,
  )

  expected_statement = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=2,
    ),
    rhs=FiniteCyclicGroup(
      order=4,
      generator=eta2_nu_prime,
    ),
    relation_type=RelationType.EQUALITY,
  )

  rule = (
    toda_lemma57_pi6_2_eta2_nu_prime_inference_rule()
  )

  premise_steps = (
    prop56_step,
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
    "phase65_9": phase65_9,
    "composition_isomorphism_step": (
      composition_isomorphism_step
    ),
    "prop56_step": prop56_step,
    "nu_prime": nu_prime,
    "eta_2": eta_2,
    "eta2_nu_prime": eta2_nu_prime,
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "final_step": final_step,
  }


def test_phase67_6_reuses_derived_prop56():
  data = build_phase67_6_data()

  assert isinstance(
    data[
      "prop56_step"
    ].conclusion,
    TodaProp56FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop56_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_6_reuses_derived_toda52():
  data = build_phase67_6_data()

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


def test_phase67_6_prop56_contains_pi6_3_z4_nu_prime():
  data = build_phase67_6_data()

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  assert (
    data[
      "prop56_step"
    ].conclusion.pi6_3_group_relation
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=4,
        generator=nu_prime,
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase67_6_toda52_is_eta2_composition_isomorphism():
  data = build_phase67_6_data()

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
    == data[
      "eta_2"
    ]
  )


def test_phase67_6_rule_matches_dependencies():
  data = build_phase67_6_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase67_6_derives_pi6_2_z4_eta2_nu_prime():
  data = build_phase67_6_data()

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


def test_phase67_6_target_group_is_pi6_2():
  data = build_phase67_6_data()

  assert (
    data[
      "final_step"
    ].conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=2,
    )
  )


def test_phase67_6_target_is_order_four():
  data = build_phase67_6_data()

  group = (
    data[
      "final_step"
    ].conclusion
    .rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert group.order == 4


def test_phase67_6_generator_is_eta2_composed_with_nu_prime():
  data = build_phase67_6_data()

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
        "nu_prime"
      ],
    )
  )


def test_phase67_6_preserves_nu_prime_object():
  data = build_phase67_6_data()

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
      "nu_prime"
    ]
  )


def test_phase67_6_provenance_uses_exactly_two_dependencies():
  data = build_phase67_6_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "prop56_step"
      ],
      data[
        "composition_isomorphism_step"
      ],
    )
  )


def test_phase67_6_rejects_given_prop56():
  data = build_phase67_6_data()

  given_prop56 = ProofStep(
    conclusion=(
      data[
        "prop56_step"
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
      given_prop56,
      data[
        "composition_isomorphism_step"
      ],
    ),
  ) is None


def test_phase67_6_rejects_given_toda52():
  data = build_phase67_6_data()

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
        "prop56_step"
      ],
      given_toda52,
    ),
  ) is None


def test_phase67_6_rejects_wrong_pi6_3_order():
  data = build_phase67_6_data()

  prop56 = (
    data[
      "prop56_step"
    ].conclusion
  )

  wrong_pi6_3 = replace(
    prop56.pi6_3_group_relation,
    rhs=FiniteCyclicGroup(
      order=8,
      generator=data[
        "nu_prime"
      ],
    ),
  )

  wrong_prop56 = replace(
    prop56,
    pi6_3_group_relation=wrong_pi6_3,
  )

  wrong_step = ProofStep(
    conclusion=wrong_prop56,
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


def test_phase67_6_rejects_wrong_pi6_3_generator():
  data = build_phase67_6_data()

  prop56 = (
    data[
      "prop56_step"
    ].conclusion
  )

  wrong_nu_prime = HomotopyElement(
    name="ν",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
    ),
  )

  wrong_pi6_3 = replace(
    prop56.pi6_3_group_relation,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=wrong_nu_prime,
    ),
  )

  wrong_prop56 = replace(
    prop56,
    pi6_3_group_relation=wrong_pi6_3,
  )

  wrong_step = ProofStep(
    conclusion=wrong_prop56,
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


def test_phase67_6_final_result_is_not_given():
  data = build_phase67_6_data()

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


def test_phase67_6_reaches_fixed_point_in_one_round():
  data = build_phase67_6_data()

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


