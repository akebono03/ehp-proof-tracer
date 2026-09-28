from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  IteratedSuspension,
  Multiple,
  ScalarSymbol,
  Suspension,
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
  ScalarGreaterEqualStatement,
)
from test_phase75_lemma514_sigma8 import (
  build_phase75_8a_data,
)
from test_phase77_lemma516_typed_setup import (
  build_phase77_2_data,
)
from toda_rules import (
  TodaLemma514Sigma8Statement,
  TodaLemma516Sigma8IteratedSuspensionBridgeStatement,
  TodaLemma516TypedSetupStatement,
  toda_lemma516_sigma8_iterated_suspension_bridge_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase77_5b_data():
  phase75_8a = (
    build_phase75_8a_data()
  )

  phase77_2 = (
    build_phase77_2_data()
  )

  sigma8_step = (
    phase75_8a[
      "sigma8_step"
    ]
  )

  setup = (
    phase77_2[
      "setup"
    ]
  )

  setup_step = ProofStep(
    conclusion=setup,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_lemma516_sigma8_iterated_suspension_bridge_inference_rule()
  )

  premise_steps = (
    sigma8_step,
    setup_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  bridge_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaLemma516Sigma8IteratedSuspensionBridgeStatement,
    )
  )

  return {
    "phase75_8a": phase75_8a,
    "phase77_2": phase77_2,
    "sigma8_step": sigma8_step,
    "setup_step": setup_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "bridge_step": bridge_step,
  }


def test_phase77_5b_reuses_derived_sigma8_statement():
  data = build_phase77_5b_data()

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


def test_phase77_5b_setup_remains_given():
  data = build_phase77_5b_data()

  assert isinstance(
    data[
      "setup_step"
    ].conclusion,
    TodaLemma516TypedSetupStatement,
  )

  assert (
    data[
      "setup_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase77_5b_derives_iterated_suspension_bridge():
  data = build_phase77_5b_data()

  step = (
    data[
      "bridge_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma516Sigma8IteratedSuspensionBridgeStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_5b_reuses_same_sigma8_object():
  data = build_phase77_5b_data()

  sigma8_statement = (
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
    bridge.sigma8
    is sigma8_statement.sigma8
  )


def test_phase77_5b_reuses_same_alpha_star_object():
  data = build_phase77_5b_data()

  sigma8_statement = (
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
    bridge.alpha_star
    is sigma8_statement.alpha_star
  )

  assert (
    bridge.alpha_star
    is (
      sigma8_statement
      .theorem36_bridge
      .alpha_star
    )
  )


def test_phase77_5b_reuses_same_odd_parameter():
  data = build_phase77_5b_data()

  sigma8_statement = (
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
    bridge.odd_parameter
    is sigma8_statement.odd_parameter
  )

  assert (
    bridge.odd_parameter
    is (
      sigma8_statement
      .theorem36_bridge
      .odd_parameter
    )
  )


def test_phase77_5b_preserves_odd_parameter_statement():
  data = build_phase77_5b_data()

  bridge = (
    data[
      "bridge_step"
    ].conclusion
  )

  assert (
    bridge.odd_parameter_statement
    == OddScalarStatement(
      scalar=(
        bridge
        .odd_parameter
      ),
    )
  )


def test_phase77_5b_preserves_base_suspension_relation():
  data = build_phase77_5b_data()

  sigma8_statement = (
    data[
      "sigma8_step"
    ].conclusion
  )

  bridge = (
    data[
      "bridge_step"
    ].conclusion
  )

  expected = Relation(
    lhs=Suspension(
      expression=(
        sigma8_statement
        .sigma8
      ),
    ),
    rhs=Multiple(
      coefficient=(
        sigma8_statement
        .odd_parameter
      ),
      expression=Suspension(
        expression=(
          sigma8_statement
          .alpha_star
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    sigma8_statement
    .suspension_relation
    == expected
  )

  assert (
    bridge
    .base_suspension_relation
    is (
      sigma8_statement
      .suspension_relation
    )
  )


def test_phase77_5b_iterated_relation_is_expected():
  data = build_phase77_5b_data()

  setup = (
    data[
      "setup_step"
    ].conclusion
  )

  bridge = (
    data[
      "bridge_step"
    ].conclusion
  )

  expected = Relation(
    lhs=IteratedSuspension(
      expression=bridge.sigma8,
      exponent=setup.t,
    ),
    rhs=Multiple(
      coefficient=(
        bridge
        .odd_parameter
      ),
      expression=IteratedSuspension(
        expression=(
          bridge
          .alpha_star
        ),
        exponent=setup.t,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    bridge
    .iterated_suspension_relation
    == expected
  )


def test_phase77_5b_uses_same_t_as_typed_setup():
  data = build_phase77_5b_data()

  setup = (
    data[
      "setup_step"
    ].conclusion
  )

  bridge = (
    data[
      "bridge_step"
    ].conclusion
  )

  assert (
    bridge.t
    is setup.t
  )


def test_phase77_5b_preserves_sigma8_statement_provenance():
  data = build_phase77_5b_data()

  assert (
    data[
      "bridge_step"
    ].conclusion
    .sigma8_statement
    is (
      data[
        "sigma8_step"
      ].conclusion
    )
  )


def test_phase77_5b_preserves_exact_direct_provenance():
  data = build_phase77_5b_data()

  step = (
    data[
      "bridge_step"
    ]
  )

  assert (
    step.premises
    == (
      data[
        "sigma8_step"
      ],
      data[
        "setup_step"
      ],
    )
  )

  assert (
    step.inference_rule
    == data[
      "rule"
    ]
  )


def test_phase77_5b_reaches_fixed_point():
  data = build_phase77_5b_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase77_5b_rejects_given_sigma8_statement():
  data = build_phase77_5b_data()

  sigma8_statement = (
    data[
      "sigma8_step"
    ].conclusion
  )

  wrong_step = ProofStep(
    conclusion=sigma8_statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "setup_step"
      ],
    ),
  )

  assert match is None


def test_phase77_5b_rejects_t_zero_scope():
  data = build_phase77_5b_data()

  setup = (
    data[
      "setup_step"
    ].conclusion
  )

  wrong_setup = replace(
    setup,
    t_range=ScalarGreaterEqualStatement(
      left=setup.t,
      right=0,
    ),
  )

  wrong_setup_step = ProofStep(
    conclusion=wrong_setup,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "sigma8_step"
      ],
      wrong_setup_step,
    ),
  )

  assert match is None


def test_phase77_5b_rejects_wrong_odd_parameter_provenance():
  data = build_phase77_5b_data()

  sigma8_statement = (
    data[
      "sigma8_step"
    ].conclusion
  )

  wrong_x = ScalarSymbol(
    name="z",
  )

  wrong_sigma8_statement = replace(
    sigma8_statement,
    odd_parameter=wrong_x,
  )

  wrong_step = ProofStep(
    conclusion=wrong_sigma8_statement,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  match = find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "setup_step"
      ],
    ),
  )

  assert match is None


def test_phase77_5b_sigma8_generator_is_preserved():
  data = build_phase77_5b_data()

  sigma8 = (
    data[
      "bridge_step"
    ].conclusion
    .sigma8
  )

  assert (
    sigma8.generator
    == GeneratorSymbol(
      family="σ",
      index=8,
    )
  )


