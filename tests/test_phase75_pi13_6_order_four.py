from functools import lru_cache

from expression import (
  GeneratorSymbol,
  MapApplication,
  Multiple,
  Suspension,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_H_MAP,
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
from test_phase75_lemma514_sigma_double_prime import (
  build_phase75_6b_data,
)
from toda_rules import (
  Toda514FirstShortExactStatement,
  TodaLemma514SigmaDoublePrimeStatement,
  toda_prop515_pi13_6_finite_cyclic_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_6c_data():
  phase75_6b = (
    build_phase75_6b_data()
  )

  sigma_step = (
    phase75_6b[
      "sigma_step"
    ]
  )

  short_exact_step = (
    phase75_6b[
      "short_exact_step"
    ]
  )

  pi12_5_step = (
    phase75_6b[
      "pi12_5_step"
    ]
  )

  pi13_11_step = (
    phase75_6b[
      "pi13_11_step"
    ]
  )

  final_rule = (
    toda_prop515_pi13_6_finite_cyclic_inference_rule()
  )

  rules = (
    final_rule,
  )

  premise_steps = (
    sigma_step,
    short_exact_step,
    pi12_5_step,
    pi13_11_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  sigma_double_prime = (
    sigma_step
    .conclusion
    .sigma_double_prime
  )

  expected_final = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=6,
    ),
    rhs=FiniteCyclicGroup(
      order=4,
      generator=sigma_double_prime,
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
    "phase75_6b": phase75_6b,
    "sigma_step": sigma_step,
    "short_exact_step": (
      short_exact_step
    ),
    "pi12_5_step": pi12_5_step,
    "pi13_11_step": pi13_11_step,
    "sigma_double_prime": (
      sigma_double_prime
    ),
    "final_rule": final_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "expected_final": expected_final,
    "final_step": final_step,
  }


def test_phase75_6c_reuses_sigma_double_prime_statement():
  data = build_phase75_6c_data()

  assert isinstance(
    data[
      "sigma_step"
    ].conclusion,
    TodaLemma514SigmaDoublePrimeStatement,
  )

  assert (
    data[
      "sigma_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6c_reuses_first_short_exact_sequence():
  data = build_phase75_6c_data()

  assert isinstance(
    data[
      "short_exact_step"
    ].conclusion,
    Toda514FirstShortExactStatement,
  )

  assert (
    data[
      "short_exact_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6c_reuses_pi12_5_z2():
  data = build_phase75_6c_data()

  relation = (
    data[
      "pi12_5_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=5,
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

  assert (
    relation.rhs.generator
    == data[
      "sigma_step"
    ].conclusion
    .sigma_triple_prime
  )

  assert (
    data[
      "pi12_5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6c_reuses_pi13_11_z2():
  data = build_phase75_6c_data()

  relation = (
    data[
      "pi13_11_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=11,
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

  assert (
    data[
      "pi13_11_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6c_double_relation_connects_kernel_generator():
  data = build_phase75_6c_data()

  statement = (
    data[
      "sigma_step"
    ].conclusion
  )

  expected = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=(
        statement
        .sigma_double_prime
      ),
    ),
    rhs=Suspension(
      expression=(
        data[
          "pi12_5_step"
        ].conclusion
        .rhs
        .generator
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    statement.double_relation
    == expected
  )


def test_phase75_6c_hopf_relation_hits_quotient_generator():
  data = build_phase75_6c_data()

  statement = (
    data[
      "sigma_step"
    ].conclusion
  )

  target_generator = (
    data[
      "pi13_11_step"
    ].conclusion
    .rhs
    .generator
  )

  assert (
    statement.hopf_relation
    == Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=(
          statement
          .sigma_double_prime
        ),
      ),
      rhs=target_generator,
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase75_6c_sigma_double_prime_has_expected_type():
  data = build_phase75_6c_data()

  sigma = (
    data[
      "sigma_double_prime"
    ]
  )

  assert (
    sigma.source
    == 13
  )

  assert (
    sigma.target
    == 6
  )

  assert (
    sigma.generator
    == GeneratorSymbol(
      family="σ",
      decoration="''",
    )
  )


def test_phase75_6c_derives_pi13_6_z4():
  data = build_phase75_6c_data()

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


def test_phase75_6c_final_group_is_pi13_6():
  data = build_phase75_6c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    == TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=6,
    )
  )


def test_phase75_6c_final_group_order_is_four():
  data = build_phase75_6c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .order
    == 4
  )


def test_phase75_6c_final_generator_is_sigma_double_prime():
  data = build_phase75_6c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == data[
      "sigma_double_prime"
    ]
  )


def test_phase75_6c_final_uses_exact_dependencies():
  data = build_phase75_6c_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "sigma_step"
      ],
      data[
        "short_exact_step"
      ],
      data[
        "pi12_5_step"
      ],
      data[
        "pi13_11_step"
      ],
    )
  )


def test_phase75_6c_final_not_present_initially():
  data = build_phase75_6c_data()

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


def test_phase75_6c_rejects_given_sigma_statement():
  data = build_phase75_6c_data()

  given = ProofStep(
    conclusion=(
      data[
        "sigma_step"
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
      given,
      data[
        "short_exact_step"
      ],
      data[
        "pi12_5_step"
      ],
      data[
        "pi13_11_step"
      ],
    ),
  ) is None


def test_phase75_6c_rejects_given_short_exact_sequence():
  data = build_phase75_6c_data()

  given = ProofStep(
    conclusion=(
      data[
        "short_exact_step"
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
        "sigma_step"
      ],
      given,
      data[
        "pi12_5_step"
      ],
      data[
        "pi13_11_step"
      ],
    ),
  ) is None


def test_phase75_6c_rejects_given_pi12_5_relation():
  data = build_phase75_6c_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi12_5_step"
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
        "sigma_step"
      ],
      data[
        "short_exact_step"
      ],
      given,
      data[
        "pi13_11_step"
      ],
    ),
  ) is None


def test_phase75_6c_rejects_given_pi13_11_relation():
  data = build_phase75_6c_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi13_11_step"
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
        "sigma_step"
      ],
      data[
        "short_exact_step"
      ],
      data[
        "pi12_5_step"
      ],
      given,
    ),
  ) is None


def test_phase75_6c_reaches_fixed_point():
  data = build_phase75_6c_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


