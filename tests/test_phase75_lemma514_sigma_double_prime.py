from functools import lru_cache

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Composition,
  GeneratorSymbol,
  IteratedSuspension,
  MapApplication,
  Multiple,
  ScalarProduct,
  ScalarSymbol,
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
from scalar_rules import (
  OddScalarStatement,
)
from test_phase60_lemma54_integration import (
  build_phase60_9_data,
)
from test_phase68_prop58_integration import (
  build_phase68_11_data,
)
from test_phase73_prop511_finite_dimensional_integration import (
  build_phase73_8e_data,
)
from test_phase75_514_first_short_exact import (
  build_phase75_6a_data,
)
from test_phase75_pi12_5_order_two import (
  build_phase75_5_data,
)
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda514FirstShortExactStatement,
  TodaLemma513Statement,
  TodaLemma514SigmaDoublePrimeStatement,
  TodaLemma54Statement,
  TodaProp58FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  toda_36_lemma514_sigma_double_prime_bridge_inference_rule,
  toda_lemma514_sigma_double_prime_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_6b_data():
  phase60_9 = (
    build_phase60_9_data()
  )

  phase68_11 = (
    build_phase68_11_data()
  )

  phase73_8e = (
    build_phase73_8e_data()
  )

  phase75_5 = (
    build_phase75_5_data()
  )

  phase75_6a = (
    build_phase75_6a_data()
  )

  lemma54_step = (
    phase60_9[
      "integration_step"
    ]
  )

  prop58_step = (
    phase68_11[
      "integration_step"
    ]
  )

  prop511_step = (
    phase73_8e[
      "final_step"
    ]
  )

  lemma513_step = (
    phase75_5[
      "lemma513_step"
    ]
  )

  pi12_5_step = (
    phase75_5[
      "final_step"
    ]
  )

  short_exact_step = (
    phase75_6a[
      "final_step"
    ]
  )

  pi13_11_step = (
    phase75_6a[
      "pi13_11_step"
    ]
  )

  bridge_rule = (
    toda_36_lemma514_sigma_double_prime_bridge_inference_rule()
  )

  sigma_rule = (
    toda_lemma514_sigma_double_prime_inference_rule()
  )

  rules = (
    bridge_rule,
    sigma_rule,
  )

  premise_steps = (
    lemma54_step,
    prop511_step,
    prop58_step,
    lemma513_step,
    pi12_5_step,
    short_exact_step,
    pi13_11_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  bridge_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      Toda36Lemma514SigmaDoublePrimeBridgeStatement,
    )
  )

  sigma_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaLemma514SigmaDoublePrimeStatement,
    )
  )

  sigma_double_prime = (
    sigma_step
    .conclusion
    .sigma_double_prime
  )

  return {
    "phase60_9": phase60_9,
    "phase68_11": phase68_11,
    "phase73_8e": phase73_8e,
    "phase75_5": phase75_5,
    "phase75_6a": phase75_6a,
    "lemma54_step": lemma54_step,
    "prop58_step": prop58_step,
    "prop511_step": prop511_step,
    "lemma513_step": lemma513_step,
    "pi12_5_step": pi12_5_step,
    "short_exact_step": short_exact_step,
    "pi13_11_step": pi13_11_step,
    "bridge_rule": bridge_rule,
    "sigma_rule": sigma_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "bridge_step": bridge_step,
    "sigma_step": sigma_step,
    "sigma_double_prime": (
      sigma_double_prime
    ),
  }


def test_phase75_6b_reuses_lemma54():
  data = build_phase75_6b_data()

  assert isinstance(
    data[
      "lemma54_step"
    ].conclusion,
    TodaLemma54Statement,
  )

  assert (
    data[
      "lemma54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6b_reuses_prop511():
  data = build_phase75_6b_data()

  assert isinstance(
    data[
      "prop511_step"
    ].conclusion,
    TodaProp511FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop511_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6b_reuses_prop58():
  data = build_phase75_6b_data()

  assert isinstance(
    data[
      "prop58_step"
    ].conclusion,
    TodaProp58FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop58_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6b_reuses_lemma513():
  data = build_phase75_6b_data()

  assert isinstance(
    data[
      "lemma513_step"
    ].conclusion,
    TodaLemma513Statement,
  )

  assert (
    data[
      "lemma513_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6b_reuses_pi12_5_z2():
  data = build_phase75_6b_data()

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
    data[
      "pi12_5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6b_reuses_first_short_exact_sequence():
  data = build_phase75_6b_data()

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


def test_phase75_6b_derives_theorem36_bridge():
  data = build_phase75_6b_data()

  assert isinstance(
    data[
      "bridge_step"
    ].conclusion,
    Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  )

  assert (
    data[
      "bridge_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_6b_alpha_star_is_in_pi15_s8():
  data = build_phase75_6b_data()

  statement = (
    data[
      "bridge_step"
    ].conclusion
  )

  assert (
    statement.alpha_star.source
    == 15
  )

  assert (
    statement.alpha_star.target
    == 8
  )

  assert isinstance(
    statement.alpha_star_membership,
    HomotopyGroupMembershipStatement,
  )

  assert (
    statement
    .alpha_star_membership
    .group_dimension
    == 15
  )

  assert (
    statement
    .alpha_star_membership
    .sphere_dimension
    == 8
  )


def test_phase75_6b_bridge_parameter_is_odd():
  data = build_phase75_6b_data()

  statement = (
    data[
      "bridge_step"
    ].conclusion
  )

  assert (
    statement.odd_parameter
    == ScalarSymbol(
      name="x",
    )
  )

  assert (
    statement.odd_parameter_statement
    == OddScalarStatement(
      scalar=statement.odd_parameter,
    )
  )


def test_phase75_6b_bridge_is_8x_e_alpha_star_equals_e4_sigma_triple_prime():
  data = build_phase75_6b_data()

  statement = (
    data[
      "bridge_step"
    ].conclusion
  )

  expected = Relation(
    lhs=Multiple(
      coefficient=ScalarProduct(
        left=8,
        right=(
          statement
          .odd_parameter
        ),
      ),
      expression=Suspension(
        expression=(
          statement.alpha_star
        ),
      ),
    ),
    rhs=IteratedSuspension(
      expression=(
        statement
        .lemma513_statement
        .sigma_triple_prime
      ),
      exponent=4,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    statement.bridge_relation
    == expected
  )


def test_phase75_6b_bridge_uses_exact_dependencies():
  data = build_phase75_6b_data()

  assert (
    data[
      "bridge_step"
    ].premises
    == (
      data[
        "lemma54_step"
      ],
      data[
        "prop511_step"
      ],
      data[
        "prop58_step"
      ],
      data[
        "lemma513_step"
      ],
      data[
        "pi12_5_step"
      ],
    )
  )


def test_phase75_6b_derives_sigma_double_prime():
  data = build_phase75_6b_data()

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


def test_phase75_6b_sigma_double_prime_has_expected_type():
  data = build_phase75_6b_data()

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


def test_phase75_6b_e3_sigma_double_prime_relation():
  data = build_phase75_6b_data()

  statement = (
    data[
      "sigma_step"
    ].conclusion
  )

  expected = Relation(
    lhs=IteratedSuspension(
      expression=(
        statement
        .sigma_double_prime
      ),
      exponent=3,
    ),
    rhs=Multiple(
      coefficient=ScalarProduct(
        left=4,
        right=(
          statement
          .odd_parameter
        ),
      ),
      expression=Suspension(
        expression=(
          statement.alpha_star
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    statement
    .iterated_suspension_relation
    == expected
  )


def test_phase75_6b_double_sigma_double_prime_is_e_sigma_triple_prime():
  data = build_phase75_6b_data()

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
        statement
        .sigma_triple_prime
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    statement.double_relation
    == expected
  )


def test_phase75_6b_hopf_sigma_double_prime_is_eta11_squared():
  data = build_phase75_6b_data()

  statement = (
    data[
      "sigma_step"
    ].conclusion
  )

  assert (
    statement
    .hopf_relation
    .lhs
    == MapApplication(
      map=EHP_H_MAP,
      expression=(
        statement
        .sigma_double_prime
      ),
    )
  )

  eta11_squared = (
    statement
    .hopf_relation
    .rhs
  )

  assert isinstance(
    eta11_squared,
    Composition,
  )

  assert (
    eta11_squared
    .left
    .generator
    == GeneratorSymbol(
      family="η",
      index=11,
    )
  )

  assert (
    eta11_squared
    .right
    .generator
    == GeneratorSymbol(
      family="η",
      index=12,
    )
  )


def test_phase75_6b_sigma_branch_uses_exact_dependencies():
  data = build_phase75_6b_data()

  assert (
    data[
      "sigma_step"
    ].premises
    == (
      data[
        "bridge_step"
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


def test_phase75_6b_rejects_given_bridge():
  data = build_phase75_6b_data()

  given = ProofStep(
    conclusion=(
      data[
        "bridge_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "sigma_rule"
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


def test_phase75_6b_rejects_given_short_exact_sequence():
  data = build_phase75_6b_data()

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
      "sigma_rule"
    ],
    (
      data[
        "bridge_step"
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


def test_phase75_6b_rejects_given_pi12_5_relation():
  data = build_phase75_6b_data()

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
      "sigma_rule"
    ],
    (
      data[
        "bridge_step"
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


def test_phase75_6b_rejects_given_pi13_11_relation():
  data = build_phase75_6b_data()

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
      "sigma_rule"
    ],
    (
      data[
        "bridge_step"
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


def test_phase75_6b_reaches_fixed_point():
  data = build_phase75_6b_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


