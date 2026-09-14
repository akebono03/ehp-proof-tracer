from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
  Multiple,
  ScalarProduct,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
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
from test_phase75_lemma514_sigma_double_prime import (
  build_phase75_6b_data,
)
from test_phase75_lemma514_sigma_prime import (
  build_phase75_7b_data,
)
from test_phase75_pi14_7_order_eight import (
  build_phase75_7c_data,
)
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaPrimeStatement,
  toda_lemma514_sigma8_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase75_8a_data():
  phase75_6b = (
    build_phase75_6b_data()
  )

  phase75_7b = (
    build_phase75_7b_data()
  )

  phase75_7c = (
    build_phase75_7c_data()
  )

  bridge_step = (
    phase75_6b[
      "bridge_step"
    ]
  )

  sigma_prime_step = (
    phase75_7b[
      "sigma_prime_step"
    ]
  )

  pi14_7_step = (
    phase75_7c[
      "final_step"
    ]
  )

  sigma8_rule = (
    toda_lemma514_sigma8_inference_rule()
  )

  rules = (
    sigma8_rule,
  )

  premise_steps = (
    bridge_step,
    sigma_prime_step,
    pi14_7_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  sigma8_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaLemma514Sigma8Statement,
    )
  )

  sigma8 = (
    sigma8_step
    .conclusion
    .sigma8
  )

  return {
    "phase75_6b": phase75_6b,
    "phase75_7b": phase75_7b,
    "phase75_7c": phase75_7c,
    "bridge_step": bridge_step,
    "sigma_prime_step": (
      sigma_prime_step
    ),
    "pi14_7_step": pi14_7_step,
    "sigma8_rule": sigma8_rule,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "sigma8_step": sigma8_step,
    "sigma8": sigma8,
  }


def test_phase75_8a_reuses_theorem36_bridge():
  data = build_phase75_8a_data()

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


def test_phase75_8a_reuses_sigma_prime_statement():
  data = build_phase75_8a_data()

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


def test_phase75_8a_reuses_pi14_7_z8():
  data = build_phase75_8a_data()

  relation = (
    data[
      "pi14_7_step"
    ].conclusion
  )

  assert (
    relation.lhs
    == TodaPrimaryGroup(
      group_dimension=14,
      sphere_dimension=7,
    )
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.order
    == 8
  )

  assert (
    relation.rhs.generator
    == data[
      "sigma_prime_step"
    ].conclusion
    .sigma_prime
  )

  assert (
    data[
      "pi14_7_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8a_derives_sigma8_statement():
  data = build_phase75_8a_data()

  assert isinstance(
    data[
      "sigma8_step"
    ].conclusion,
    TodaLemma514Sigma8Statement,
  )

  assert (
    data[
      "sigma8_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase75_8a_sigma8_has_expected_type():
  data = build_phase75_8a_data()

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


def test_phase75_8a_preserves_odd_parameter():
  data = build_phase75_8a_data()

  statement = (
    data[
      "sigma8_step"
    ].conclusion
  )

  bridge = (
    data[
      "bridge_step"
    ].conclusion
  )

  assert (
    statement.odd_parameter
    == bridge.odd_parameter
  )

  assert (
    bridge.odd_parameter_statement
    == OddScalarStatement(
      scalar=(
        statement
        .odd_parameter
      ),
    )
  )


def test_phase75_8a_has_integral_correction_parameter():
  data = build_phase75_8a_data()

  statement = (
    data[
      "sigma8_step"
    ].conclusion
  )

  assert (
    statement.correction_parameter
    == ScalarSymbol(
      name="y",
    )
  )


def test_phase75_8a_definition_is_corrected_alpha_star():
  data = build_phase75_8a_data()

  statement = (
    data[
      "sigma8_step"
    ].conclusion
  )

  iota_17 = (
    HomotopyElement(
      name="ι_17",
      dimension=17,
      generator=GeneratorSymbol(
        family="ι",
        index=17,
      ),
    )
  )

  expected = Relation(
    lhs=statement.sigma8,
    rhs=Sum(
      left=Multiple(
        coefficient=(
          statement
          .odd_parameter
        ),
        expression=(
          statement
          .alpha_star
        ),
      ),
      right=Multiple(
        coefficient=ScalarProduct(
          left=-1,
          right=(
            statement
            .correction_parameter
          ),
        ),
        expression=MapApplication(
          map=EHP_DELTA_MAP,
          expression=iota_17,
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    statement.definition_relation
    == expected
  )


def test_phase75_8a_hopf_sigma8_is_iota15():
  data = build_phase75_8a_data()

  statement = (
    data[
      "sigma8_step"
    ].conclusion
  )

  expected_iota15 = HomotopyElement(
    name="ι_15",
    dimension=15,
    generator=GeneratorSymbol(
      family="ι",
      index=15,
    ),
  )

  assert (
    statement.hopf_relation
    == Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=statement.sigma8,
      ),
      rhs=expected_iota15,
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase75_8a_e_sigma8_is_x_e_alpha_star():
  data = build_phase75_8a_data()

  statement = (
    data[
      "sigma8_step"
    ].conclusion
  )

  expected = Relation(
    lhs=Suspension(
      expression=statement.sigma8,
    ),
    rhs=Multiple(
      coefficient=(
        statement
        .odd_parameter
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
    statement.suspension_relation
    == expected
  )


def test_phase75_8a_double_e_sigma8_is_e2_sigma_prime():
  data = build_phase75_8a_data()

  statement = (
    data[
      "sigma8_step"
    ].conclusion
  )

  expected = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=Suspension(
        expression=statement.sigma8,
      ),
    ),
    rhs=IteratedSuspension(
      expression=statement.sigma_prime,
      exponent=2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    statement
    .double_suspension_relation
    == expected
  )


def test_phase75_8a_reuses_same_sigma_prime():
  data = build_phase75_8a_data()

  assert (
    data[
      "sigma8_step"
    ].conclusion
    .sigma_prime
    == data[
      "sigma_prime_step"
    ].conclusion
    .sigma_prime
  )


def test_phase75_8a_reuses_same_alpha_star():
  data = build_phase75_8a_data()

  assert (
    data[
      "sigma8_step"
    ].conclusion
    .alpha_star
    == data[
      "bridge_step"
    ].conclusion
    .alpha_star
  )


def test_phase75_8a_preserves_theorem36_provenance():
  data = build_phase75_8a_data()

  assert (
    data[
      "sigma8_step"
    ].conclusion
    .theorem36_bridge
    == data[
      "bridge_step"
    ].conclusion
  )


def test_phase75_8a_preserves_sigma_prime_provenance():
  data = build_phase75_8a_data()

  assert (
    data[
      "sigma8_step"
    ].conclusion
    .sigma_prime_statement
    == data[
      "sigma_prime_step"
    ].conclusion
  )


def test_phase75_8a_uses_exact_dependencies():
  data = build_phase75_8a_data()

  assert (
    data[
      "sigma8_step"
    ].premises
    == (
      data[
        "bridge_step"
      ],
      data[
        "sigma_prime_step"
      ],
      data[
        "pi14_7_step"
      ],
    )
  )


def test_phase75_8a_statement_not_present_initially():
  data = build_phase75_8a_data()

  assert (
    data[
      "sigma8_step"
    ].conclusion
    not in tuple(
      step.conclusion
      for step
      in data[
        "premise_steps"
      ]
    )
  )


def test_phase75_8a_rejects_given_bridge():
  data = build_phase75_8a_data()

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
      "sigma8_rule"
    ],
    (
      given,
      data[
        "sigma_prime_step"
      ],
      data[
        "pi14_7_step"
      ],
    ),
  ) is None


def test_phase75_8a_rejects_given_sigma_prime():
  data = build_phase75_8a_data()

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
      "sigma8_rule"
    ],
    (
      data[
        "bridge_step"
      ],
      given,
      data[
        "pi14_7_step"
      ],
    ),
  ) is None


def test_phase75_8a_rejects_given_pi14_7():
  data = build_phase75_8a_data()

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
      "sigma8_rule"
    ],
    (
      data[
        "bridge_step"
      ],
      data[
        "sigma_prime_step"
      ],
      given,
    ),
  ) is None


def test_phase75_8a_reaches_fixed_point():
  data = build_phase75_8a_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


