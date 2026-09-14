from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
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
from test_phase77_theorem36_first_bracket import (
  build_phase77_3_data,
)
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda36Lemma516FirstBracketTermStatement,
  Toda36Lemma516SecondBracketTermStatement,
  TodaLemma516TypedSetupStatement,
  toda_36_lemma516_second_bracket_term_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase77_4_data():
  phase77_3 = (
    build_phase77_3_data()
  )

  bridge_step = (
    phase77_3[
      "bridge_step"
    ]
  )

  setup_step = (
    phase77_3[
      "setup_step"
    ]
  )

  rule = (
    toda_36_lemma516_second_bracket_term_inference_rule()
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

  second_term_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      Toda36Lemma516SecondBracketTermStatement,
    )
  )

  return {
    "phase77_3": phase77_3,
    "bridge_step": bridge_step,
    "setup_step": setup_step,
    "first_term_step": (
      phase77_3[
        "first_term_step"
      ]
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "second_term_step": (
      second_term_step
    ),
  }


def test_phase77_4_reuses_phase75_theorem36_bridge():
  data = build_phase77_4_data()

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


def test_phase77_4_setup_remains_given():
  data = build_phase77_4_data()

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


def test_phase77_4_derives_second_bracket_term():
  data = build_phase77_4_data()

  step = data[
    "second_term_step"
  ]

  assert isinstance(
    step.conclusion,
    Toda36Lemma516SecondBracketTermStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_4_preserves_alpha_star_object():
  data = build_phase77_4_data()

  bridge = (
    data[
      "bridge_step"
    ].conclusion
  )

  statement = (
    data[
      "second_term_step"
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


def test_phase77_4_composed_value_is_e4_beta_composed_with_et_alpha_star():
  data = build_phase77_4_data()

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
      "second_term_step"
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


def test_phase77_4_second_coefficient_is_minus_one_power_t():
  data = build_phase77_4_data()

  setup = (
    data[
      "setup_step"
    ].conclusion
  )

  statement = (
    data[
      "second_term_step"
    ].conclusion
  )

  assert (
    statement.coefficient
    == ScalarPower(
      base=-1,
      exponent=setup.t,
    )
  )


def test_phase77_4_reuses_phase77_2_second_bracket():
  data = build_phase77_4_data()

  setup = (
    data[
      "setup_step"
    ].conclusion
  )

  statement = (
    data[
      "second_term_step"
    ].conclusion
  )

  assert (
    statement.bracket
    is setup.second_bracket
  )


def test_phase77_4_second_bracket_has_expected_exact_structure():
  data = build_phase77_4_data()

  setup = (
    data[
      "setup_step"
    ].conclusion
  )

  t = setup.t

  nu_t_plus_8 = HomotopyElement(
    name="ν_(t+8)",
    dimension=ScalarSum(
      left=t,
      right=8,
    ),
    source=ScalarSum(
      left=t,
      right=11,
    ),
    target=ScalarSum(
      left=t,
      right=8,
    ),
    generator=GeneratorSymbol(
      family="ν",
      index=ScalarSum(
        left=t,
        right=8,
      ),
    ),
  )

  nu_t_plus_11 = HomotopyElement(
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
  )

  expected = TodaBracket(
    first=setup.e4_beta,
    second=nu_t_plus_8,
    third=Multiple(
      coefficient=2,
      expression=nu_t_plus_11,
    ),
    index=ScalarSum(
      left=t,
      right=3,
    ),
  )

  assert (
    data[
      "second_term_step"
    ]
    .conclusion
    .bracket
    == expected
  )


def test_phase77_4_second_bracket_first_term_is_e4_beta():
  data = build_phase77_4_data()

  setup = (
    data[
      "setup_step"
    ].conclusion
  )

  bracket = (
    data[
      "second_term_step"
    ]
    .conclusion
    .bracket
  )

  assert (
    bracket.first
    == IteratedSuspension(
      expression=setup.beta,
      exponent=4,
    )
  )

  assert (
    bracket.first
    == setup.e4_beta
  )


def test_phase77_4_first_and_second_branches_share_composed_value():
  data = build_phase77_4_data()

  first_statement = (
    data[
      "first_term_step"
    ].conclusion
  )

  second_statement = (
    data[
      "second_term_step"
    ].conclusion
  )

  assert isinstance(
    first_statement,
    Toda36Lemma516FirstBracketTermStatement,
  )

  assert (
    second_statement.composed_value
    == first_statement.composed_value
  )

  assert (
    second_statement.alpha_star
    is first_statement.alpha_star
  )

  assert (
    second_statement.beta
    is first_statement.beta
  )


def test_phase77_4_first_branch_is_not_direct_premise():
  data = build_phase77_4_data()

  step = data[
    "second_term_step"
  ]

  assert (
    data[
      "first_term_step"
    ]
    not in step.premises
  )

  assert (
    step.premises
    == data[
      "premise_steps"
    ]
  )


def test_phase77_4_preserves_exact_direct_provenance():
  data = build_phase77_4_data()

  step = data[
    "second_term_step"
  ]

  assert (
    step.premises
    == (
      data[
        "bridge_step"
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


def test_phase77_4_reaches_fixed_point():
  data = build_phase77_4_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase77_4_rejects_given_theorem36_bridge():
  data = build_phase77_4_data()

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


def test_phase77_4_rejects_wrong_second_bracket():
  data = build_phase77_4_data()

  setup = (
    data[
      "setup_step"
    ].conclusion
  )

  wrong_t = ScalarSymbol(
    name="q",
  )

  wrong_second_bracket = TodaBracket(
    first=setup.e4_beta,
    second=HomotopyElement(
      name="ν_(q+8)",
      dimension=ScalarSum(
        left=wrong_t,
        right=8,
      ),
      source=ScalarSum(
        left=wrong_t,
        right=11,
      ),
      target=ScalarSum(
        left=wrong_t,
        right=8,
      ),
      generator=GeneratorSymbol(
        family="ν",
        index=ScalarSum(
          left=wrong_t,
          right=8,
        ),
      ),
    ),
    third=setup.second_bracket.third,
    index=ScalarSum(
      left=wrong_t,
      right=3,
    ),
  )

  wrong_setup = replace(
    setup,
    second_bracket=wrong_second_bracket,
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


