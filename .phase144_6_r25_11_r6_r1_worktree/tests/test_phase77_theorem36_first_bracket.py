from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarPower,
  ScalarSum,
  ScalarSymbol,
  TodaBracket,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase75_lemma514_sigma8 import (
  build_phase75_8a_data,
)
from test_phase77_lemma516_typed_setup import (
  build_phase77_2_data,
)
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda36Lemma516FirstBracketTermStatement,
  TodaLemma516TypedSetupStatement,
  toda_36_lemma516_first_bracket_term_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase77_3_data():
  phase75 = (
    build_phase75_8a_data()
  )

  phase77_2 = (
    build_phase77_2_data()
  )

  bridge_step = (
    phase75[
      "bridge_step"
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
    toda_36_lemma516_first_bracket_term_inference_rule()
  )

  premise_steps = (
    bridge_step,
    setup_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  first_term_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      Toda36Lemma516FirstBracketTermStatement,
    )
  )

  return {
    "phase75": phase75,
    "phase77_2": phase77_2,
    "bridge_step": bridge_step,
    "setup_step": setup_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "first_term_step": (
      first_term_step
    ),
  }


def test_phase77_3_reuses_phase75_theorem36_bridge():
  data = build_phase77_3_data()

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


def test_phase77_3_setup_remains_given():
  data = build_phase77_3_data()

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


def test_phase77_3_derives_first_bracket_term():
  data = build_phase77_3_data()

  step = data[
    "first_term_step"
  ]

  assert isinstance(
    step.conclusion,
    Toda36Lemma516FirstBracketTermStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_3_preserves_alpha_star_object():
  data = build_phase77_3_data()

  bridge = (
    data[
      "bridge_step"
    ].conclusion
  )

  statement = (
    data[
      "first_term_step"
    ].conclusion
  )

  assert (
    statement.alpha_star
    is bridge.alpha_star
  )

  assert (
    statement.alpha_star_membership
    is bridge.alpha_star_membership
  )


def test_phase77_3_composed_value_is_e4_beta_composed_with_et_alpha_star():
  data = build_phase77_3_data()

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

  statement = (
    data[
      "first_term_step"
    ].conclusion
  )

  assert (
    statement.composed_value
    == Composition(
      left=setup.e4_beta,
      right=IteratedSuspension(
        expression=bridge.alpha_star,
        exponent=setup.t,
      ),
    )
  )


def test_phase77_3_first_coefficient_is_minus_one_power_m():
  data = build_phase77_3_data()

  setup = (
    data[
      "setup_step"
    ].conclusion
  )

  statement = (
    data[
      "first_term_step"
    ].conclusion
  )

  assert (
    statement.coefficient
    == ScalarPower(
      base=-1,
      exponent=setup.m,
    )
  )


def test_phase77_3_reuses_phase77_2_first_bracket():
  data = build_phase77_3_data()

  setup = (
    data[
      "setup_step"
    ].conclusion
  )

  statement = (
    data[
      "first_term_step"
    ].conclusion
  )

  assert (
    statement.bracket
    is setup.first_bracket
  )


def test_phase77_3_first_bracket_middle_term_is_e7_beta():
  data = build_phase77_3_data()

  setup = (
    data[
      "setup_step"
    ].conclusion
  )

  bracket = (
    data[
      "first_term_step"
    ]
    .conclusion
    .bracket
  )

  assert (
    bracket.second
    == IteratedSuspension(
      expression=setup.beta,
      exponent=7,
    )
  )

  assert (
    bracket.second
    == setup.e7_beta
  )


def test_phase77_3_first_bracket_has_expected_exact_structure():
  data = build_phase77_3_data()

  setup = (
    data[
      "setup_step"
    ].conclusion
  )

  m = setup.m
  t = setup.t

  expected = TodaBracket(
    first=HomotopyElement(
      name="ν_(m+4)",
      dimension=ScalarSum(
        left=m,
        right=4,
      ),
      source=ScalarSum(
        left=m,
        right=7,
      ),
      target=ScalarSum(
        left=m,
        right=4,
      ),
      generator=GeneratorSymbol(
        family="ν",
        index=ScalarSum(
          left=m,
          right=4,
        ),
      ),
    ),
    second=setup.e7_beta,
    third=HomotopyElement(
      name="ν_(t+11)",
      dimension=ScalarSum(
        left=t,
        right=11,
      ),
      source=ScalarSum(
        left=t,
        right=14,
      ),
      target=ScalarSum(
        left=t,
        right=11,
      ),
      generator=GeneratorSymbol(
        family="ν",
        index=ScalarSum(
          left=t,
          right=11,
        ),
      ),
    ),
    index=7,
  )

  assert (
    data[
      "first_term_step"
    ]
    .conclusion
    .bracket
    == expected
  )


def test_phase77_3_preserves_exact_direct_provenance():
  data = build_phase77_3_data()

  step = data[
    "first_term_step"
  ]

  assert (
    step.premises
    == data[
      "premise_steps"
    ]
  )

  assert (
    step.inference_rule
    == data[
      "rule"
    ]
  )


def test_phase77_3_reaches_fixed_point():
  data = build_phase77_3_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase77_3_rejects_given_theorem36_bridge():
  data = build_phase77_3_data()

  bridge = (
    data[
      "bridge_step"
    ].conclusion
  )

  wrong_bridge_step = ProofStep(
    conclusion=bridge,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_bridge_step,
      data[
        "setup_step"
      ],
    ),
  )

  assert match is None


def test_phase77_3_rejects_wrong_t_range_setup():
  data = build_phase77_3_data()

  setup = (
    data[
      "setup_step"
    ].conclusion
  )

  wrong_t = ScalarSymbol(
    name="q",
  )

  wrong_setup = (
    TodaLemma516TypedSetupStatement(
      beta=setup.beta,
      beta_membership=(
        setup.beta_membership
      ),
      beta_nu_zero_relation=(
        setup.beta_nu_zero_relation
      ),
      t_range=setup.t_range,
      m=setup.m,
      t=wrong_t,
      e4_beta=setup.e4_beta,
      e4_beta_membership=(
        setup.e4_beta_membership
      ),
      e7_beta=setup.e7_beta,
      e7_beta_membership=(
        setup.e7_beta_membership
      ),
      first_bracket=(
        setup.first_bracket
      ),
      second_bracket=(
        setup.second_bracket
      ),
    )
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
        "bridge_step"
      ],
      wrong_setup_step,
    ),
  )

  assert match is None


