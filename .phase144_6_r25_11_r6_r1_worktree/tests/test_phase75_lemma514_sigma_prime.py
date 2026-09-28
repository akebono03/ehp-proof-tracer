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
from test_phase75_lemma514_sigma_double_prime import (
  build_phase75_6b_data,
)
from test_phase75_pi13_6_order_four import (
  build_phase75_6c_data,
)
from toda_rules import (
  Toda514SecondShortExactStatement,
  TodaLemma514SigmaDoublePrimeStatement,
  TodaLemma514SigmaPrimeStatement,
  toda_lemma514_sigma_prime_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_7b_data():
  phase75_6b = (
    build_phase75_6b_data()
  )

  phase75_6c = (
    build_phase75_6c_data()
  )

  phase75_7a = (
    build_phase75_7a_data()
  )

  sigma_double_prime_step = (
    phase75_6b[
      "sigma_step"
    ]
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

  sigma_prime_rule = (
    toda_lemma514_sigma_prime_inference_rule()
  )

  rules = (
    sigma_prime_rule,
  )

  premise_steps = (
    sigma_double_prime_step,
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

  sigma_prime_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaLemma514SigmaPrimeStatement,
    )
  )

  sigma_prime = (
    sigma_prime_step
    .conclusion
    .sigma_prime
  )

  return {
    "phase75_6b": phase75_6b,
    "phase75_6c": phase75_6c,
    "phase75_7a": phase75_7a,
    "sigma_double_prime_step": (
      sigma_double_prime_step
    ),
    "pi13_6_step": pi13_6_step,
    "second_short_exact_step": (
      second_short_exact_step
    ),
    "pi14_13_step": pi14_13_step,
    "sigma_prime_rule": (
      sigma_prime_rule
    ),
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "sigma_prime_step": (
      sigma_prime_step
    ),
    "sigma_prime": sigma_prime,
  }


def test_phase75_7b_reuses_sigma_double_prime_statement():
  data = build_phase75_7b_data()

  assert isinstance(
    data[
      "sigma_double_prime_step"
    ].conclusion,
    TodaLemma514SigmaDoublePrimeStatement,
  )

  assert (
    data[
      "sigma_double_prime_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_7b_reuses_pi13_6_z4():
  data = build_phase75_7b_data()

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
      "sigma_double_prime_step"
    ].conclusion
    .sigma_double_prime
  )

  assert (
    data[
      "pi13_6_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_7b_reuses_second_short_exact_sequence():
  data = build_phase75_7b_data()

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


def test_phase75_7b_reuses_pi14_13_z2_eta13():
  data = build_phase75_7b_data()

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


def test_phase75_7b_derives_sigma_prime_statement():
  data = build_phase75_7b_data()

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


def test_phase75_7b_sigma_prime_has_expected_type():
  data = build_phase75_7b_data()

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


def test_phase75_7b_hopf_sigma_prime_is_eta13():
  data = build_phase75_7b_data()

  statement = (
    data[
      "sigma_prime_step"
    ].conclusion
  )

  eta_13 = (
    data[
      "pi14_13_step"
    ].conclusion
    .rhs
    .generator
  )

  expected = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=(
        statement.sigma_prime
      ),
    ),
    rhs=eta_13,
    relation_type=RelationType.EQUALITY,
  )

  assert (
    statement.hopf_relation
    == expected
  )


def test_phase75_7b_double_sigma_prime_is_e_sigma_double_prime():
  data = build_phase75_7b_data()

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
        statement.sigma_double_prime
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    statement.double_relation
    == expected
  )


def test_phase75_7b_sigma_prime_reuses_sigma_double_prime():
  data = build_phase75_7b_data()

  assert (
    data[
      "sigma_prime_step"
    ].conclusion
    .sigma_double_prime
    == data[
      "sigma_double_prime_step"
    ].conclusion
    .sigma_double_prime
  )


def test_phase75_7b_preserves_sigma_double_prime_provenance():
  data = build_phase75_7b_data()

  statement = (
    data[
      "sigma_prime_step"
    ].conclusion
  )

  assert (
    statement
    .sigma_double_prime_statement
    == data[
      "sigma_double_prime_step"
    ].conclusion
  )

  assert (
    statement
    .sigma_double_prime_statement
    .theorem36_bridge
    == data[
      "sigma_double_prime_step"
    ].conclusion
    .theorem36_bridge
  )


def test_phase75_7b_preserves_second_short_exact_provenance():
  data = build_phase75_7b_data()

  assert (
    data[
      "sigma_prime_step"
    ].conclusion
    .short_exact_statement
    == data[
      "second_short_exact_step"
    ].conclusion
  )


def test_phase75_7b_uses_exact_dependencies():
  data = build_phase75_7b_data()

  assert (
    data[
      "sigma_prime_step"
    ].premises
    == (
      data[
        "sigma_double_prime_step"
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


def test_phase75_7b_statement_not_present_initially():
  data = build_phase75_7b_data()

  assert (
    data[
      "sigma_prime_step"
    ].conclusion
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase75_7b_rejects_given_sigma_double_prime_statement():
  data = build_phase75_7b_data()

  given = ProofStep(
    conclusion=(
      data[
        "sigma_double_prime_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "sigma_prime_rule"
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


def test_phase75_7b_rejects_given_second_short_exact():
  data = build_phase75_7b_data()

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
      "sigma_prime_rule"
    ],
    (
      data[
        "sigma_double_prime_step"
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


def test_phase75_7b_rejects_given_pi13_6_relation():
  data = build_phase75_7b_data()

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
      "sigma_prime_rule"
    ],
    (
      data[
        "sigma_double_prime_step"
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


def test_phase75_7b_rejects_given_pi14_13_relation():
  data = build_phase75_7b_data()

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
      "sigma_prime_rule"
    ],
    (
      data[
        "sigma_double_prime_step"
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


def test_phase75_7b_reaches_fixed_point():
  data = build_phase75_7b_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


