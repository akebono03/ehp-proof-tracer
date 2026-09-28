from functools import lru_cache

from expression import (
  GeneratorSymbol,
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaIteratedSuspensionMap,
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
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase75_pi16_9_sigma9 import (
  build_phase75_8c_data,
)
from test_phase75_sigma_family_definition import (
  build_phase75_8b_data,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  TodaSigmaFamilyDefinitionStatement,
  toda_45_isomorphism_inference_rule,
  toda_45_sigma9_finite_cyclic_transport_inference_rule,
  toda_sigma_family_definition_statement,
)


@lru_cache(maxsize=1)
def build_phase75_8d_data():
  phase75_8b = (
    build_phase75_8b_data()
  )

  phase75_8c = (
    build_phase75_8c_data()
  )

  sigma_family_step = (
    phase75_8b[
      "definition_step"
    ]
  )

  pi16_9_step = (
    phase75_8c[
      "final_step"
    ]
  )

  n = (
    sigma_family_step
    .conclusion
    .index
  )

  stable_range = (
    ScalarGreaterEqualStatement(
      left=9,
      right=ScalarSum(
        left=7,
        right=2,
      ),
    )
  )

  suspension_range = (
    ScalarGreaterEqualStatement(
      left=n,
      right=9,
    )
  )

  target_group = TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=n,
      right=7,
    ),
    sphere_dimension=n,
  )

  suspension_map = (
    TodaIteratedSuspensionMap(
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=9,
        ),
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=9,
          right=7,
        ),
        sphere_dimension=9,
      ),
      target_group=target_group,
    )
  )

  stable_range_step = ProofStep(
    conclusion=stable_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspension_range_step = ProofStep(
    conclusion=suspension_range,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspension_map_step = ProofStep(
    conclusion=suspension_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  toda45_rule = (
    toda_45_isomorphism_inference_rule()
  )

  transport_rule = (
    toda_45_sigma9_finite_cyclic_transport_inference_rule()
  )

  rules = (
    toda45_rule,
    transport_rule,
  )

  premise_steps = (
    pi16_9_step,
    sigma_family_step,
    stable_range_step,
    suspension_range_step,
    suspension_map_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  isomorphism_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == Toda45IsomorphismStatement(
        map=suspension_map,
      )
    )
  )

  expected_final = Relation(
    lhs=target_group,
    rhs=FiniteCyclicGroup(
      order=16,
      generator=(
        sigma_family_step
        .conclusion
        .element
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
    "phase75_8b": phase75_8b,
    "phase75_8c": phase75_8c,
    "sigma_family_step": (
      sigma_family_step
    ),
    "pi16_9_step": pi16_9_step,
    "n": n,
    "stable_range": stable_range,
    "suspension_range": (
      suspension_range
    ),
    "target_group": target_group,
    "suspension_map": suspension_map,
    "stable_range_step": (
      stable_range_step
    ),
    "suspension_range_step": (
      suspension_range_step
    ),
    "suspension_map_step": (
      suspension_map_step
    ),
    "toda45_rule": toda45_rule,
    "transport_rule": transport_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "isomorphism_step": (
      isomorphism_step
    ),
    "expected_final": expected_final,
    "final_step": final_step,
  }


def test_phase75_8d_reuses_pi16_9_z16_sigma9():
  data = build_phase75_8d_data()

  relation = (
    data[
      "pi16_9_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=16,
      sphere_dimension=9,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 16
  )

  assert (
    relation.rhs.generator
    == toda_sigma_family_definition_statement(
      9,
      data[
        "sigma_family_step"
      ].conclusion
      .sigma8_statement,
    ).element
  )

  assert (
    data[
      "pi16_9_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8d_reuses_symbolic_sigma_family():
  data = build_phase75_8d_data()

  assert isinstance(
    data[
      "sigma_family_step"
    ].conclusion,
    TodaSigmaFamilyDefinitionStatement,
  )

  assert (
    data[
      "sigma_family_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8d_stable_range_is_9_ge_7_plus_2():
  data = build_phase75_8d_data()

  assert (
    data[
      "stable_range"
    ]
    == ScalarGreaterEqualStatement(
      left=9,
      right=ScalarSum(
        left=7,
        right=2,
      ),
    )
  )


def test_phase75_8d_suspension_range_is_n_ge_9():
  data = build_phase75_8d_data()

  assert (
    data[
      "suspension_range"
    ]
    == ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=9,
    )
  )


def test_phase75_8d_map_is_e_n_minus_9():
  data = build_phase75_8d_data()

  assert (
    data[
      "suspension_map"
    ].exponent
    == ScalarSum(
      left=data[
        "n"
      ],
      right=ScalarProduct(
        left=-1,
        right=9,
      ),
    )
  )


def test_phase75_8d_map_source_is_pi16_9_structure():
  data = build_phase75_8d_data()

  assert (
    data[
      "suspension_map"
    ].source_group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=9,
        right=7,
      ),
      sphere_dimension=9,
    )
  )


def test_phase75_8d_map_target_is_pi_n_plus_7_n():
  data = build_phase75_8d_data()

  assert (
    data[
      "suspension_map"
    ].target_group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=7,
      ),
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase75_8d_derives_toda45_isomorphism():
  data = build_phase75_8d_data()

  assert (
    data[
      "isomorphism_step"
    ].conclusion
    == Toda45IsomorphismStatement(
      map=(
        data[
          "suspension_map"
        ]
      ),
    )
  )

  assert (
    data[
      "isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8d_toda45_uses_exact_three_premises():
  data = build_phase75_8d_data()

  assert (
    data[
      "isomorphism_step"
    ].premises
    == (
      data[
        "stable_range_step"
      ],
      data[
        "suspension_range_step"
      ],
      data[
        "suspension_map_step"
      ],
    )
  )


def test_phase75_8d_sigma_n_has_expected_generator():
  data = build_phase75_8d_data()

  sigma_n = (
    data[
      "sigma_family_step"
    ].conclusion
    .element
  )

  assert (
    sigma_n.generator
    == GeneratorSymbol(
      family="σ",
      index=(
        data[
          "n"
        ]
      ),
    )
  )


def test_phase75_8d_sigma_n_retains_family_definition():
  data = build_phase75_8d_data()

  statement = (
    data[
      "sigma_family_step"
    ].conclusion
  )

  assert (
    statement.iterated_suspension
    == IteratedSuspension(
      expression=(
        statement
        .sigma8_statement
        .sigma8
      ),
      exponent=ScalarSum(
        left=data[
          "n"
        ],
        right=-8,
      ),
    )
  )


def test_phase75_8d_derives_stable_sigma_group():
  data = build_phase75_8d_data()

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


def test_phase75_8d_final_group_is_pi_n_plus_7_n():
  data = build_phase75_8d_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=7,
      ),
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase75_8d_final_group_order_is_16():
  data = build_phase75_8d_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .order
    == 16
  )


def test_phase75_8d_final_generator_is_sigma_n():
  data = build_phase75_8d_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == data[
      "sigma_family_step"
    ].conclusion
    .element
  )


def test_phase75_8d_final_uses_exact_dependencies():
  data = build_phase75_8d_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi16_9_step"
      ],
      data[
        "isomorphism_step"
      ],
      data[
        "sigma_family_step"
      ],
    )
  )


def test_phase75_8d_final_not_present_initially():
  data = build_phase75_8d_data()

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


def test_phase75_8d_rejects_given_pi16_9():
  data = build_phase75_8d_data()

  given = ProofStep(
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
      given,
      data[
        "isomorphism_step"
      ],
      data[
        "sigma_family_step"
      ],
    ),
  ) is None


def test_phase75_8d_rejects_given_toda45_isomorphism():
  data = build_phase75_8d_data()

  given = ProofStep(
    conclusion=(
      data[
        "isomorphism_step"
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
      given,
      data[
        "sigma_family_step"
      ],
    ),
  ) is None


def test_phase75_8d_rejects_given_sigma_family():
  data = build_phase75_8d_data()

  given = ProofStep(
    conclusion=(
      data[
        "sigma_family_step"
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
        "isomorphism_step"
      ],
      given,
    ),
  ) is None


def test_phase75_8d_rejects_wrong_transport_exponent():
  data = build_phase75_8d_data()

  wrong_map = TodaIteratedSuspensionMap(
    exponent=ScalarSum(
      left=data[
        "n"
      ],
      right=ScalarProduct(
        left=-1,
        right=8,
      ),
    ),
    source_group=(
      data[
        "suspension_map"
      ].source_group
    ),
    target_group=(
      data[
        "suspension_map"
      ].target_group
    ),
  )

  wrong_iso = ProofStep(
    conclusion=Toda45IsomorphismStatement(
      map=wrong_map,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "transport_rule"
    ],
    (
      data[
        "pi16_9_step"
      ],
      wrong_iso,
      data[
        "sigma_family_step"
      ],
    ),
  ) is None


def test_phase75_8d_rejects_wrong_target_stem():
  data = build_phase75_8d_data()

  wrong_map = TodaIteratedSuspensionMap(
    exponent=(
      data[
        "suspension_map"
      ].exponent
    ),
    source_group=(
      data[
        "suspension_map"
      ].source_group
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=8,
      ),
      sphere_dimension=data[
        "n"
      ],
    ),
  )

  wrong_iso = ProofStep(
    conclusion=Toda45IsomorphismStatement(
      map=wrong_map,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "transport_rule"
    ],
    (
      data[
        "pi16_9_step"
      ],
      wrong_iso,
      data[
        "sigma_family_step"
      ],
    ),
  ) is None


def test_phase75_8d_reaches_fixed_point():
  data = build_phase75_8d_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


