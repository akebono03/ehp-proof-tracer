from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from low_dimensional_facts import (
  pi_15_15_free_cyclic_fact,
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
from test_phase75_515_sigma8_prop44_decomposition import (
  build_phase75_8e2_data,
)
from test_phase75_pi14_7_order_eight import (
  build_phase75_7c_data,
)
from toda_rules import (
  Toda515Sigma8TransportedDecompositionStatement,
  TodaProp44IsomorphismStatement,
  toda_prop515_sigma8_transported_decomposition_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_8e3_data():
  phase75_8e2 = (
    build_phase75_8e2_data()
  )

  phase75_7c = (
    build_phase75_7c_data()
  )

  isomorphism_step = (
    phase75_8e2[
      "isomorphism_step"
    ]
  )

  pi14_7_step = (
    phase75_7c[
      "final_step"
    ]
  )

  pi15_15_relation = (
    pi_15_15_free_cyclic_fact()
  )

  pi15_15_step = ProofStep(
    conclusion=pi15_15_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  sigma8 = (
    isomorphism_step
    .conclusion
    .map
    .alpha
  )

  sigma_prime = (
    pi14_7_step
    .conclusion
    .rhs
    .generator
  )

  e_sigma_prime = Suspension(
    expression=sigma_prime,
  )

  transported_group = DirectSumGroup(
    summands=(
      FiniteCyclicGroup(
        order=8,
        generator=e_sigma_prime,
      ),
      FreeCyclicGroup(
        generator=sigma8,
      ),
    ),
  )

  expected_statement = (
    Toda515Sigma8TransportedDecompositionStatement(
      prop44_isomorphism=(
        isomorphism_step
        .conclusion
      ),
      pi14_7_group_relation=(
        pi14_7_step
        .conclusion
      ),
      pi15_15_group_relation=(
        pi15_15_relation
      ),
      first_generator_image=(
        e_sigma_prime
      ),
      second_generator_image=(
        sigma8
      ),
      transported_group=(
        transported_group
      ),
    )
  )

  rule = (
    toda_prop515_sigma8_transported_decomposition_inference_rule()
  )

  premise_steps = (
    isomorphism_step,
    pi14_7_step,
    pi15_15_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      premise_steps,
    )
  )

  transported_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase75_8e2": phase75_8e2,
    "phase75_7c": phase75_7c,
    "isomorphism_step": (
      isomorphism_step
    ),
    "pi14_7_step": pi14_7_step,
    "pi15_15_relation": (
      pi15_15_relation
    ),
    "pi15_15_step": pi15_15_step,
    "sigma8": sigma8,
    "sigma_prime": sigma_prime,
    "e_sigma_prime": (
      e_sigma_prime
    ),
    "transported_group": (
      transported_group
    ),
    "expected_statement": (
      expected_statement
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "transported_step": (
      transported_step
    ),
  }


def test_phase75_8e3_pi15_15_foundational_fact():
  relation = (
    pi_15_15_free_cyclic_fact()
  )

  assert (
    relation
    == Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=15,
        sphere_dimension=15,
      ),
      rhs=FreeCyclicGroup(
        generator=HomotopyElement(
          name="ι_15",
          dimension=15,
          generator=GeneratorSymbol(
            family="ι",
            index=15,
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase75_8e3_pi15_15_fact_remains_given():
  data = build_phase75_8e3_data()

  assert (
    data[
      "pi15_15_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase75_8e3_reuses_derived_prop44_isomorphism():
  data = build_phase75_8e3_data()

  assert isinstance(
    data[
      "isomorphism_step"
    ].conclusion,
    TodaProp44IsomorphismStatement,
  )

  assert (
    data[
      "isomorphism_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8e3_reuses_derived_pi14_7():
  data = build_phase75_8e3_data()

  assert (
    data[
      "pi14_7_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "pi14_7_step"
    ].conclusion
    .lhs
    == TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=7,
    )
  )


def test_phase75_8e3_pi14_7_is_order_eight():
  data = build_phase75_8e3_data()

  group = (
    data[
      "pi14_7_step"
    ].conclusion
    .rhs
  )

  assert isinstance(
    group,
    FiniteCyclicGroup,
  )

  assert (
    group.order
    == 8
  )


def test_phase75_8e3_pi14_7_generator_is_sigma_prime():
  data = build_phase75_8e3_data()

  sigma_prime = (
    data[
      "sigma_prime"
    ]
  )

  assert (
    sigma_prime.source
    == 14
  )

  assert (
    sigma_prime.target
    == 7
  )

  assert (
    sigma_prime.generator
    == GeneratorSymbol(
      family="σ",
      decoration="'",
    )
  )


def test_phase75_8e3_pi15_15_is_free_cyclic():
  data = build_phase75_8e3_data()

  relation = (
    data[
      "pi15_15_relation"
    ]
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=15,
      sphere_dimension=15,
    )
  )

  assert isinstance(
    relation.rhs,
    FreeCyclicGroup,
  )


def test_phase75_8e3_pi15_15_generator_is_iota15():
  data = build_phase75_8e3_data()

  iota_15 = (
    data[
      "pi15_15_relation"
    ].rhs
    .generator
  )

  assert (
    iota_15.dimension
    == 15
  )

  assert (
    iota_15.generator
    == GeneratorSymbol(
      family="ι",
      index=15,
    )
  )


def test_phase75_8e3_first_generator_image_is_e_sigma_prime():
  data = build_phase75_8e3_data()

  statement = (
    data[
      "transported_step"
    ].conclusion
  )

  assert (
    statement.first_generator_image
    == Suspension(
      expression=(
        data[
          "sigma_prime"
        ]
      ),
    )
  )


def test_phase75_8e3_second_generator_image_is_sigma8():
  data = build_phase75_8e3_data()

  statement = (
    data[
      "transported_step"
    ].conclusion
  )

  assert (
    statement.second_generator_image
    == data[
      "sigma8"
    ]
  )


def test_phase75_8e3_sigma8_has_expected_generator():
  data = build_phase75_8e3_data()

  sigma8 = (
    data[
      "sigma8"
    ]
  )

  assert (
    sigma8.source
    == 15
  )

  assert (
    sigma8.target
    == 8
  )

  assert (
    sigma8.generator
    == GeneratorSymbol(
      family="σ",
      index=8,
    )
  )


def test_phase75_8e3_transport_preserves_source_summand_order():
  data = build_phase75_8e3_data()

  group = (
    data[
      "transported_step"
    ].conclusion
    .transported_group
  )

  assert isinstance(
    group.summands[
      0
    ],
    FiniteCyclicGroup,
  )

  assert isinstance(
    group.summands[
      1
    ],
    FreeCyclicGroup,
  )


def test_phase75_8e3_first_transported_summand_is_z8_e_sigma_prime():
  data = build_phase75_8e3_data()

  first = (
    data[
      "transported_step"
    ].conclusion
    .transported_group
    .summands[
      0
    ]
  )

  assert (
    first
    == FiniteCyclicGroup(
      order=8,
      generator=(
        data[
          "e_sigma_prime"
        ]
      ),
    )
  )


def test_phase75_8e3_second_transported_summand_is_z_sigma8():
  data = build_phase75_8e3_data()

  second = (
    data[
      "transported_step"
    ].conclusion
    .transported_group
    .summands[
      1
    ]
  )

  assert (
    second
    == FreeCyclicGroup(
      generator=(
        data[
          "sigma8"
        ]
      ),
    )
  )


def test_phase75_8e3_derives_expected_statement():
  data = build_phase75_8e3_data()

  assert (
    data[
      "transported_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "transported_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8e3_preserves_prop44_isomorphism():
  data = build_phase75_8e3_data()

  assert (
    data[
      "transported_step"
    ].conclusion
    .prop44_isomorphism
    is data[
      "isomorphism_step"
    ].conclusion
  )


def test_phase75_8e3_preserves_pi14_7_relation():
  data = build_phase75_8e3_data()

  assert (
    data[
      "transported_step"
    ].conclusion
    .pi14_7_group_relation
    is data[
      "pi14_7_step"
    ].conclusion
  )


def test_phase75_8e3_preserves_pi15_15_relation():
  data = build_phase75_8e3_data()

  assert (
    data[
      "transported_step"
    ].conclusion
    .pi15_15_group_relation
    is data[
      "pi15_15_step"
    ].conclusion
  )


def test_phase75_8e3_uses_exact_dependencies():
  data = build_phase75_8e3_data()

  assert (
    data[
      "transported_step"
    ].premises
    == (
      data[
        "isomorphism_step"
      ],
      data[
        "pi14_7_step"
      ],
      data[
        "pi15_15_step"
      ],
    )
  )


def test_phase75_8e3_statement_not_present_initially():
  data = build_phase75_8e3_data()

  assert (
    data[
      "expected_statement"
    ]
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase75_8e3_rejects_given_prop44_isomorphism():
  data = build_phase75_8e3_data()

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
      "rule"
    ],
    (
      given,
      data[
        "pi14_7_step"
      ],
      data[
        "pi15_15_step"
      ],
    ),
  ) is None


def test_phase75_8e3_rejects_given_pi14_7():
  data = build_phase75_8e3_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi14_7_step"
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
        "isomorphism_step"
      ],
      given,
      data[
        "pi15_15_step"
      ],
    ),
  ) is None


def test_phase75_8e3_rejects_inferred_pi15_15():
  data = build_phase75_8e3_data()

  inferred = ProofStep(
    conclusion=(
      data[
        "pi15_15_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "isomorphism_step"
      ],
      data[
        "pi14_7_step"
      ],
      inferred,
    ),
  ) is None


def test_phase75_8e3_rejects_wrong_pi14_7_order():
  data = build_phase75_8e3_data()

  wrong_relation = replace(
    data[
      "pi14_7_step"
    ].conclusion,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=(
        data[
          "sigma_prime"
        ]
      ),
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
      data[
        "isomorphism_step"
      ],
      wrong_step,
      data[
        "pi15_15_step"
      ],
    ),
  ) is None


def test_phase75_8e3_rejects_wrong_sigma_prime():
  data = build_phase75_8e3_data()

  wrong_sigma_prime = HomotopyElement(
    name="τ′",
    dimension=7,
    source=14,
    target=7,
    generator=GeneratorSymbol(
      family="τ",
      decoration="'",
    ),
  )

  wrong_relation = replace(
    data[
      "pi14_7_step"
    ].conclusion,
    rhs=FiniteCyclicGroup(
      order=8,
      generator=wrong_sigma_prime,
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
      data[
        "isomorphism_step"
      ],
      wrong_step,
      data[
        "pi15_15_step"
      ],
    ),
  ) is None


def test_phase75_8e3_rejects_wrong_pi15_15_generator():
  data = build_phase75_8e3_data()

  wrong_relation = replace(
    data[
      "pi15_15_relation"
    ],
    rhs=FreeCyclicGroup(
      generator=HomotopyElement(
        name="x",
        dimension=15,
        generator=GeneratorSymbol(
          family="x",
          index=15,
        ),
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "isomorphism_step"
      ],
      data[
        "pi14_7_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase75_8e3_rejects_wrong_pi15_15_group():
  data = build_phase75_8e3_data()

  wrong_relation = replace(
    data[
      "pi15_15_relation"
    ],
    lhs=TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=14,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "isomorphism_step"
      ],
      data[
        "pi14_7_step"
      ],
      wrong_step,
    ),
  ) is None


def test_phase75_8e3_reaches_fixed_point():
  data = build_phase75_8e3_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


