from functools import lru_cache

from expression import (
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
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
from probes.probe_phase46_capabilities import (
  build_phase46_representative_result,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase65_nu5_order_pi8_5 import (
  build_phase65_7_data,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  TodaNuFamilyDefinitionStatement,
  toda_nu_family_definition_statement,
  toda_prop56_higher_nu_family_bridge_inference_rule,
  toda_prop56_higher_nu_finite_cyclic_generator_inference_rule,
  toda_prop56_nu5_stable_transport_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase65_8_data():
  phase65_7 = (
    build_phase65_7_data()
  )

  pi8_5_step = (
    phase65_7[
      "pi8_5_step"
    ]
  )

  n = ScalarSymbol(
    name="n",
  )

  phase46 = (
    build_phase46_representative_result(
      n=5,
      k=3,
      m=n,
    )
  )

  stable_isomorphism_step = (
    phase46[
      "theorem_steps"
    ][
      0
    ]
  )

  higher_range = (
    ScalarGreaterEqualStatement(
      left=n,
      right=6,
    )
  )

  higher_range_step = ProofStep(
    conclusion=higher_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nu5_definition = (
    toda_nu_family_definition_statement(
      5
    )
  )

  nu5_definition_step = ProofStep(
    conclusion=nu5_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nu_n_definition = (
    toda_nu_family_definition_statement(
      n
    )
  )

  nu_n_definition_step = ProofStep(
    conclusion=nu_n_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  exponent = ScalarSum(
    left=n,
    right=ScalarProduct(
      left=-1,
      right=5,
    ),
  )

  transported_generator = (
    IteratedSuspension(
      expression=(
        nu5_definition.element
      ),
      exponent=exponent,
    )
  )

  expected_transport_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=3,
      ),
      sphere_dimension=n,
    ),
    rhs=FiniteCyclicGroup(
      order=8,
      generator=transported_generator,
    ),
    relation_type=RelationType.EQUALITY,
  )

  expected_bridge = Relation(
    lhs=transported_generator,
    rhs=nu_n_definition.element,
    relation_type=RelationType.EQUALITY,
  )

  expected_final_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=3,
      ),
      sphere_dimension=n,
    ),
    rhs=FiniteCyclicGroup(
      order=8,
      generator=(
        nu_n_definition.element
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  transport_rule = (
    toda_prop56_nu5_stable_transport_inference_rule()
  )

  bridge_rule = (
    toda_prop56_higher_nu_family_bridge_inference_rule()
  )

  generator_rule = (
    toda_prop56_higher_nu_finite_cyclic_generator_inference_rule()
  )

  rules = (
    transport_rule,
    bridge_rule,
    generator_rule,
  )

  premise_steps = (
    pi8_5_step,
    stable_isomorphism_step,
    higher_range_step,
    nu5_definition_step,
    nu_n_definition_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  transport_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_transport_relation
    )
  )

  bridge_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_bridge
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_final_relation
    )
  )

  return {
    "phase65_7": phase65_7,
    "phase46": phase46,
    "n": n,
    "pi8_5_step": pi8_5_step,
    "stable_isomorphism_step": (
      stable_isomorphism_step
    ),
    "higher_range": higher_range,
    "higher_range_step": (
      higher_range_step
    ),
    "nu5_definition": (
      nu5_definition
    ),
    "nu5_definition_step": (
      nu5_definition_step
    ),
    "nu_n_definition": (
      nu_n_definition
    ),
    "nu_n_definition_step": (
      nu_n_definition_step
    ),
    "exponent": exponent,
    "transported_generator": (
      transported_generator
    ),
    "expected_transport_relation": (
      expected_transport_relation
    ),
    "expected_bridge": expected_bridge,
    "expected_final_relation": (
      expected_final_relation
    ),
    "transport_rule": transport_rule,
    "bridge_rule": bridge_rule,
    "generator_rule": generator_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "transport_step": transport_step,
    "bridge_step": bridge_step,
    "final_step": final_step,
  }


def test_phase65_8_reuses_phase65_7_pi8_5():
  data = build_phase65_8_data()

  assert (
    data[
      "pi8_5_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi8_5_step"
    ].conclusion.rhs.order
    == 8
  )


def test_phase65_8_reuses_toda45_isomorphism():
  data = build_phase65_8_data()

  step = data[
    "stable_isomorphism_step"
  ]

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    step.conclusion,
    Toda45IsomorphismStatement,
  )


def test_phase65_8_toda45_source_is_pi8_5():
  data = build_phase65_8_data()

  suspension_map = (
    data[
      "stable_isomorphism_step"
    ].conclusion.map
  )

  assert (
    suspension_map.source_group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=5,
        right=3,
      ),
      sphere_dimension=5,
    )
  )


def test_phase65_8_toda45_target_is_pi_n_plus_3_n():
  data = build_phase65_8_data()

  suspension_map = (
    data[
      "stable_isomorphism_step"
    ].conclusion.map
  )

  assert (
    suspension_map.target_group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=3,
      ),
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase65_8_toda45_exponent_is_n_minus_5():
  data = build_phase65_8_data()

  assert (
    data[
      "stable_isomorphism_step"
    ].conclusion.map.exponent
    == data[
      "exponent"
    ]
  )


def test_phase65_8_scope_is_n_at_least_six():
  data = build_phase65_8_data()

  assert (
    data[
      "higher_range"
    ]
    == ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=6,
    )
  )


def test_phase65_8_nu_definitions_are_given():
  data = build_phase65_8_data()

  assert isinstance(
    data[
      "nu5_definition"
    ],
    TodaNuFamilyDefinitionStatement,
  )

  assert isinstance(
    data[
      "nu_n_definition"
    ],
    TodaNuFamilyDefinitionStatement,
  )

  assert (
    data[
      "nu5_definition_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "nu_n_definition_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase65_8_transport_rule_matches():
  data = build_phase65_8_data()

  assert find_inference_match(
    data[
      "transport_rule"
    ],
    (
      data[
        "pi8_5_step"
      ],
      data[
        "stable_isomorphism_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is not None


def test_phase65_8_derives_order_eight_transport():
  data = build_phase65_8_data()

  assert (
    data[
      "transport_step"
    ].conclusion
    == data[
      "expected_transport_relation"
    ]
  )

  assert (
    data[
      "transport_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_8_transport_generator_is_e_n_minus_5_nu5():
  data = build_phase65_8_data()

  assert (
    data[
      "transport_step"
    ].conclusion.rhs.generator
    == data[
      "transported_generator"
    ]
  )


def test_phase65_8_bridge_rule_matches():
  data = build_phase65_8_data()

  assert find_inference_match(
    data[
      "bridge_rule"
    ],
    (
      data[
        "nu5_definition_step"
      ],
      data[
        "nu_n_definition_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is not None


def test_phase65_8_derives_nu_family_bridge():
  data = build_phase65_8_data()

  assert (
    data[
      "bridge_step"
    ].conclusion
    == data[
      "expected_bridge"
    ]
  )

  assert (
    data[
      "bridge_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_8_bridge_target_is_nu_n():
  data = build_phase65_8_data()

  assert (
    data[
      "bridge_step"
    ].conclusion.rhs
    == data[
      "nu_n_definition"
    ].element
  )


def test_phase65_8_generator_rule_matches():
  data = build_phase65_8_data()

  assert find_inference_match(
    data[
      "generator_rule"
    ],
    (
      data[
        "transport_step"
      ],
      data[
        "bridge_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is not None


def test_phase65_8_derives_pi_n_plus_3_n_z8_nu_n():
  data = build_phase65_8_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_final_relation"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_8_final_generator_is_nu_n():
  data = build_phase65_8_data()

  group = (
    data[
      "final_step"
    ].conclusion.rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert group.order == 8

  assert (
    group.generator
    == data[
      "nu_n_definition"
    ].element
  )


def test_phase65_8_transport_provenance():
  data = build_phase65_8_data()

  assert (
    data[
      "transport_step"
    ].premises
    == (
      data[
        "pi8_5_step"
      ],
      data[
        "stable_isomorphism_step"
      ],
      data[
        "higher_range_step"
      ],
    )
  )


def test_phase65_8_bridge_provenance():
  data = build_phase65_8_data()

  assert (
    data[
      "bridge_step"
    ].premises
    == (
      data[
        "nu5_definition_step"
      ],
      data[
        "nu_n_definition_step"
      ],
      data[
        "higher_range_step"
      ],
    )
  )


def test_phase65_8_final_provenance():
  data = build_phase65_8_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "transport_step"
      ],
      data[
        "bridge_step"
      ],
      data[
        "higher_range_step"
      ],
    )
  )


def test_phase65_8_rejects_given_pi8_5():
  data = build_phase65_8_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "pi8_5_step"
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
      given_step,
      data[
        "stable_isomorphism_step"
      ],
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase65_8_rejects_given_toda45():
  data = build_phase65_8_data()

  given_step = ProofStep(
    conclusion=(
      data[
        "stable_isomorphism_step"
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
        "pi8_5_step"
      ],
      given_step,
      data[
        "higher_range_step"
      ],
    ),
  ) is None


def test_phase65_8_rejects_n_at_least_five_scope():
  data = build_phase65_8_data()

  wrong_range = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=5,
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
        "pi8_5_step"
      ],
      data[
        "stable_isomorphism_step"
      ],
      wrong_range,
    ),
  ) is None

  assert find_inference_match(
    data[
      "bridge_rule"
    ],
    (
      data[
        "nu5_definition_step"
      ],
      data[
        "nu_n_definition_step"
      ],
      wrong_range,
    ),
  ) is None


def test_phase65_8_final_result_is_not_given():
  data = build_phase65_8_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert (
    data[
      "expected_final_relation"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase65_8_reaches_fixed_point_in_two_rounds():
  data = build_phase65_8_data()

  result = data[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2

  assert (
    data[
      "transport_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "bridge_step"
    ]
    in result.round_results[
      0
    ].new_steps
  )

  assert (
    data[
      "final_step"
    ]
    in result.round_results[
      1
    ].new_steps
  )



