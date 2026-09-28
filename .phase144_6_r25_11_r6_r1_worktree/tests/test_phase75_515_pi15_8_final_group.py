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
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase75_515_sigma8_transported_decomposition import (
  build_phase75_8e3_data,
)
from toda_rules import (
  Toda515Sigma8TransportedDecompositionStatement,
  toda_prop515_pi15_8_final_group_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_8e4_data():
  phase75_8e3 = (
    build_phase75_8e3_data()
  )

  transported_step = (
    phase75_8e3[
      "transported_step"
    ]
  )

  transported_statement = (
    transported_step.conclusion
  )

  sigma8 = (
    transported_statement
    .second_generator_image
  )

  e_sigma_prime = (
    transported_statement
    .first_generator_image
  )

  free_summand = FreeCyclicGroup(
    generator=sigma8,
  )

  torsion_summand = (
    FiniteCyclicGroup(
      order=8,
      generator=e_sigma_prime,
    )
  )

  expected_final = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=15,
      sphere_dimension=8,
    ),
    rhs=DirectSumGroup(
      summands=(
        free_summand,
        torsion_summand,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  rule = (
    toda_prop515_pi15_8_final_group_inference_rule()
  )

  premise_steps = (
    transported_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      premise_steps,
    )
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
    "phase75_8e3": phase75_8e3,
    "transported_step": (
      transported_step
    ),
    "transported_statement": (
      transported_statement
    ),
    "sigma8": sigma8,
    "e_sigma_prime": (
      e_sigma_prime
    ),
    "free_summand": (
      free_summand
    ),
    "torsion_summand": (
      torsion_summand
    ),
    "expected_final": (
      expected_final
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "final_step": final_step,
  }


def test_phase75_8e4_reuses_transported_decomposition():
  data = build_phase75_8e4_data()

  assert isinstance(
    data[
      "transported_step"
    ].conclusion,
    Toda515Sigma8TransportedDecompositionStatement,
  )

  assert (
    data[
      "transported_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8e4_source_order_is_torsion_then_free():
  data = build_phase75_8e4_data()

  group = (
    data[
      "transported_statement"
    ].transported_group
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


def test_phase75_8e4_source_first_summand_is_z8_e_sigma_prime():
  data = build_phase75_8e4_data()

  first = (
    data[
      "transported_statement"
    ].transported_group
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


def test_phase75_8e4_source_second_summand_is_z_sigma8():
  data = build_phase75_8e4_data()

  second = (
    data[
      "transported_statement"
    ].transported_group
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


def test_phase75_8e4_e_sigma_prime_has_expected_structure():
  data = build_phase75_8e4_data()

  e_sigma_prime = (
    data[
      "e_sigma_prime"
    ]
  )

  assert isinstance(
    e_sigma_prime,
    Suspension,
  )

  sigma_prime = (
    e_sigma_prime.expression
  )

  assert isinstance(
    sigma_prime,
    HomotopyElement,
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


def test_phase75_8e4_sigma8_has_expected_structure():
  data = build_phase75_8e4_data()

  sigma8 = (
    data[
      "sigma8"
    ]
  )

  assert isinstance(
    sigma8,
    HomotopyElement,
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


def test_phase75_8e4_derives_final_pi15_8_relation():
  data = build_phase75_8e4_data()

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


def test_phase75_8e4_final_group_is_pi15_8():
  data = build_phase75_8e4_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    == TodaPrimaryGroup(
      group_dimension=15,
      sphere_dimension=8,
    )
  )


def test_phase75_8e4_final_rhs_is_direct_sum():
  data = build_phase75_8e4_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion
    .rhs,
    DirectSumGroup,
  )


def test_phase75_8e4_final_order_is_free_then_torsion():
  data = build_phase75_8e4_data()

  group = (
    data[
      "final_step"
    ].conclusion
    .rhs
  )

  assert isinstance(
    group.summands[
      0
    ],
    FreeCyclicGroup,
  )

  assert isinstance(
    group.summands[
      1
    ],
    FiniteCyclicGroup,
  )


def test_phase75_8e4_final_free_summand_is_z_sigma8():
  data = build_phase75_8e4_data()

  free_summand = (
    data[
      "final_step"
    ].conclusion
    .rhs
    .summands[
      0
    ]
  )

  assert (
    free_summand
    == FreeCyclicGroup(
      generator=(
        data[
          "sigma8"
        ]
      ),
    )
  )


def test_phase75_8e4_final_torsion_summand_is_z8_e_sigma_prime():
  data = build_phase75_8e4_data()

  torsion_summand = (
    data[
      "final_step"
    ].conclusion
    .rhs
    .summands[
      1
    ]
  )

  assert (
    torsion_summand
    == FiniteCyclicGroup(
      order=8,
      generator=(
        data[
          "e_sigma_prime"
        ]
      ),
    )
  )


def test_phase75_8e4_reuses_same_sigma8_object():
  data = build_phase75_8e4_data()

  final_sigma8 = (
    data[
      "final_step"
    ].conclusion
    .rhs
    .summands[
      0
    ]
    .generator
  )

  assert (
    final_sigma8
    is data[
      "transported_statement"
    ].second_generator_image
  )


def test_phase75_8e4_reuses_same_e_sigma_prime_object():
  data = build_phase75_8e4_data()

  final_e_sigma_prime = (
    data[
      "final_step"
    ].conclusion
    .rhs
    .summands[
      1
    ]
    .generator
  )

  assert (
    final_e_sigma_prime
    is data[
      "transported_statement"
    ].first_generator_image
  )


def test_phase75_8e4_uses_exact_dependency():
  data = build_phase75_8e4_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "transported_step"
      ],
    )
  )


def test_phase75_8e4_final_relation_not_present_initially():
  data = build_phase75_8e4_data()

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase75_8e4_rejects_given_transported_decomposition():
  data = build_phase75_8e4_data()

  given = ProofStep(
    conclusion=(
      data[
        "transported_statement"
      ]
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
    ),
  ) is None


def test_phase75_8e4_rejects_reversed_transported_source_order():
  data = build_phase75_8e4_data()

  statement = (
    data[
      "transported_statement"
    ]
  )

  source_group = (
    statement.transported_group
  )

  wrong_statement = replace(
    statement,
    transported_group=DirectSumGroup(
      summands=(
        source_group.summands[
          1
        ],
        source_group.summands[
          0
        ],
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase75_8e4_rejects_wrong_torsion_order():
  data = build_phase75_8e4_data()

  statement = (
    data[
      "transported_statement"
    ]
  )

  wrong_statement = replace(
    statement,
    transported_group=DirectSumGroup(
      summands=(
        FiniteCyclicGroup(
          order=4,
          generator=(
            statement
            .first_generator_image
          ),
        ),
        FreeCyclicGroup(
          generator=(
            statement
            .second_generator_image
          ),
        ),
      ),
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase75_8e4_rejects_wrong_first_generator_image():
  data = build_phase75_8e4_data()

  statement = (
    data[
      "transported_statement"
    ]
  )

  wrong_image = Suspension(
    expression=HomotopyElement(
      name="τ'",
      dimension=7,
      source=14,
      target=7,
      generator=GeneratorSymbol(
        family="τ",
        decoration="'",
      ),
    ),
  )

  wrong_statement = replace(
    statement,
    first_generator_image=wrong_image,
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase75_8e4_rejects_wrong_second_generator_image():
  data = build_phase75_8e4_data()

  statement = (
    data[
      "transported_statement"
    ]
  )

  wrong_sigma8 = HomotopyElement(
    name="τ₈",
    dimension=8,
    source=15,
    target=8,
    generator=GeneratorSymbol(
      family="τ",
      index=8,
    ),
  )

  wrong_statement = replace(
    statement,
    second_generator_image=wrong_sigma8,
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase75_8e4_rejects_wrong_target_isomorphism():
  data = build_phase75_8e4_data()

  statement = (
    data[
      "transported_statement"
    ]
  )

  prop44 = (
    statement
    .prop44_isomorphism
  )

  wrong_map = replace(
    prop44.map,
    target_group=TodaPrimaryGroup(
      group_dimension=16,
      sphere_dimension=8,
    ),
  )

  wrong_prop44 = replace(
    prop44,
    map=wrong_map,
  )

  wrong_statement = replace(
    statement,
    prop44_isomorphism=wrong_prop44,
  )

  wrong_step = ProofStep(
    conclusion=wrong_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase75_8e4_reaches_fixed_point():
  data = build_phase75_8e4_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


