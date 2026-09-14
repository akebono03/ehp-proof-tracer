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
from test_phase75_514_second_short_exact import (
  build_phase75_7a_data,
)
from test_phase75_lemma514_sigma_prime import (
  build_phase75_7b_data,
)
from test_phase75_pi13_6_order_four import (
  build_phase75_6c_data,
)
from toda_rules import (
  Toda514SecondShortExactStatement,
  TodaLemma514SigmaPrimeStatement,
  toda_prop515_pi14_7_finite_cyclic_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_7c_data():
  phase75_6c = (
    build_phase75_6c_data()
  )

  phase75_7a = (
    build_phase75_7a_data()
  )

  phase75_7b = (
    build_phase75_7b_data()
  )

  pi13_6_step = (
    phase75_6c[
      "final_step"
    ]
  )

  second_short_exact_step = (
    phase75_7a[
      "final_step"
    ]
  )

  pi14_13_step = (
    phase75_7a[
      "pi14_13_step"
    ]
  )

  sigma_prime_step = (
    phase75_7b[
      "sigma_prime_step"
    ]
  )

  final_rule = (
    toda_prop515_pi14_7_finite_cyclic_inference_rule()
  )

  rules = (
    final_rule,
  )

  premise_steps = (
    sigma_prime_step,
    second_short_exact_step,
    pi13_6_step,
    pi14_13_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  sigma_prime = (
    sigma_prime_step
    .conclusion
    .sigma_prime
  )

  expected_final = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=7,
    ),
    rhs=FiniteCyclicGroup(
      order=8,
      generator=sigma_prime,
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
    "phase75_6c": phase75_6c,
    "phase75_7a": phase75_7a,
    "phase75_7b": phase75_7b,
    "pi13_6_step": pi13_6_step,
    "second_short_exact_step": (
      second_short_exact_step
    ),
    "pi14_13_step": pi14_13_step,
    "sigma_prime_step": sigma_prime_step,
    "sigma_prime": sigma_prime,
    "final_rule": final_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "expected_final": expected_final,
    "final_step": final_step,
  }


def test_phase75_7c_reuses_sigma_prime_statement():
  data = build_phase75_7c_data()

  assert isinstance(
    data[
      "sigma_prime_step"
    ].conclusion,
    TodaLemma514SigmaPrimeStatement,
  )

  assert (
    data[
      "sigma_prime_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_7c_reuses_second_short_exact_sequence():
  data = build_phase75_7c_data()

  assert isinstance(
    data[
      "second_short_exact_step"
    ].conclusion,
    Toda514SecondShortExactStatement,
  )

  assert (
    data[
      "second_short_exact_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_7c_reuses_pi13_6_z4():
  data = build_phase75_7c_data()

  relation = (
    data[
      "pi13_6_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=6,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 4
  )

  assert (
    relation.rhs.generator
    == data[
      "sigma_prime_step"
    ].conclusion
    .sigma_double_prime
  )

  assert (
    data[
      "pi13_6_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_7c_reuses_pi14_13_z2():
  data = build_phase75_7c_data()

  relation = (
    data[
      "pi14_13_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=13,
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
    relation.rhs.generator.generator
    == GeneratorSymbol(
      family="η",
      index=13,
    )
  )

  assert (
    data[
      "pi14_13_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_7c_double_relation_connects_kernel_generator():
  data = build_phase75_7c_data()

  statement = (
    data[
      "sigma_prime_step"
    ].conclusion
  )

  expected = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=(
        statement.sigma_prime
      ),
    ),
    rhs=Suspension(
      expression=(
        data[
          "pi13_6_step"
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


def test_phase75_7c_hopf_relation_hits_quotient_generator():
  data = build_phase75_7c_data()

  statement = (
    data[
      "sigma_prime_step"
    ].conclusion
  )

  target_generator = (
    data[
      "pi14_13_step"
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
          statement.sigma_prime
        ),
      ),
      rhs=target_generator,
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase75_7c_sigma_prime_has_expected_type():
  data = build_phase75_7c_data()

  sigma = (
    data[
      "sigma_prime"
    ]
  )

  assert (
    sigma.source
    == 14
  )

  assert (
    sigma.target
    == 7
  )

  assert (
    sigma.generator
    == GeneratorSymbol(
      family="σ",
      decoration="'",
    )
  )


def test_phase75_7c_derives_pi14_7_z8():
  data = build_phase75_7c_data()

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


def test_phase75_7c_final_group_is_pi14_7():
  data = build_phase75_7c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .lhs
    == TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=7,
    )
  )


def test_phase75_7c_final_group_order_is_eight():
  data = build_phase75_7c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .order
    == 8
  )


def test_phase75_7c_final_generator_is_sigma_prime():
  data = build_phase75_7c_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .rhs
    .generator
    == data[
      "sigma_prime"
    ]
  )


def test_phase75_7c_final_uses_exact_dependencies():
  data = build_phase75_7c_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "sigma_prime_step"
      ],
      data[
        "second_short_exact_step"
      ],
      data[
        "pi13_6_step"
      ],
      data[
        "pi14_13_step"
      ],
    )
  )


def test_phase75_7c_final_not_present_initially():
  data = build_phase75_7c_data()

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


def test_phase75_7c_rejects_given_sigma_prime_statement():
  data = build_phase75_7c_data()

  given = ProofStep(
    conclusion=(
      data[
        "sigma_prime_step"
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
        "second_short_exact_step"
      ],
      data[
        "pi13_6_step"
      ],
      data[
        "pi14_13_step"
      ],
    ),
  ) is None


def test_phase75_7c_rejects_given_second_short_exact():
  data = build_phase75_7c_data()

  given = ProofStep(
    conclusion=(
      data[
        "second_short_exact_step"
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
        "sigma_prime_step"
      ],
      given,
      data[
        "pi13_6_step"
      ],
      data[
        "pi14_13_step"
      ],
    ),
  ) is None


def test_phase75_7c_rejects_given_pi13_6_relation():
  data = build_phase75_7c_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi13_6_step"
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
        "sigma_prime_step"
      ],
      data[
        "second_short_exact_step"
      ],
      given,
      data[
        "pi14_13_step"
      ],
    ),
  ) is None


def test_phase75_7c_rejects_given_pi14_13_relation():
  data = build_phase75_7c_data()

  given = ProofStep(
    conclusion=(
      data[
        "pi14_13_step"
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
        "sigma_prime_step"
      ],
      data[
        "second_short_exact_step"
      ],
      data[
        "pi13_6_step"
      ],
      given,
    ),
  ) is None


def test_phase75_7c_reaches_fixed_point():
  data = build_phase75_7c_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


