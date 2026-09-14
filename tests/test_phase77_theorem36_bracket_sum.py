from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  ScalarPower,
  ScalarSymbol,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from test_phase77_theorem36_second_bracket import (
  build_phase77_4_data,
)
from toda_rules import (
  Toda36Lemma516BracketSumContainmentStatement,
  Toda36Lemma516FirstBracketTermStatement,
  Toda36Lemma516SecondBracketTermStatement,
  toda_36_lemma516_bracket_sum_containment_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase77_5a_data():
  phase77_4 = (
    build_phase77_4_data()
  )

  first_term_step = (
    phase77_4[
      "first_term_step"
    ]
  )

  second_term_step = (
    phase77_4[
      "second_term_step"
    ]
  )

  rule = (
    toda_36_lemma516_bracket_sum_containment_inference_rule()
  )

  premise_steps = (
    first_term_step,
    second_term_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  bracket_sum_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      Toda36Lemma516BracketSumContainmentStatement,
    )
  )

  return {
    "phase77_4": phase77_4,
    "first_term_step": (
      first_term_step
    ),
    "second_term_step": (
      second_term_step
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "bracket_sum_step": (
      bracket_sum_step
    ),
  }


def test_phase77_5a_inputs_are_two_derived_sibling_branches():
  data = build_phase77_5a_data()

  first_step = (
    data[
      "first_term_step"
    ]
  )

  second_step = (
    data[
      "second_term_step"
    ]
  )

  assert isinstance(
    first_step.conclusion,
    Toda36Lemma516FirstBracketTermStatement,
  )

  assert isinstance(
    second_step.conclusion,
    Toda36Lemma516SecondBracketTermStatement,
  )

  assert (
    first_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    second_step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_5a_derives_bracket_sum_containment():
  data = build_phase77_5a_data()

  step = (
    data[
      "bracket_sum_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    Toda36Lemma516BracketSumContainmentStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_5a_preserves_common_composed_value():
  data = build_phase77_5a_data()

  first = (
    data[
      "first_term_step"
    ].conclusion
  )

  second = (
    data[
      "second_term_step"
    ].conclusion
  )

  result = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  assert (
    first.composed_value
    == second.composed_value
  )

  assert (
    result.element
    == first.composed_value
  )

  assert (
    result.element
    == second.composed_value
  )


def test_phase77_5a_composed_value_is_e4_beta_et_alpha_star():
  data = build_phase77_5a_data()

  first = (
    data[
      "first_term_step"
    ].conclusion
  )

  result = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  assert isinstance(
    result.element,
    Composition,
  )

  assert (
    result.element
    == first.composed_value
  )


def test_phase77_5a_reuses_alpha_star_and_beta():
  data = build_phase77_5a_data()

  first = (
    data[
      "first_term_step"
    ].conclusion
  )

  second = (
    data[
      "second_term_step"
    ].conclusion
  )

  result = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  assert (
    result.alpha_star
    is first.alpha_star
  )

  assert (
    result.alpha_star
    is second.alpha_star
  )

  assert (
    result.beta
    is first.beta
  )

  assert (
    result.beta
    is second.beta
  )


def test_phase77_5a_first_coefficient_is_minus_one_power_m():
  data = build_phase77_5a_data()

  result = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  assert (
    result.first_coefficient
    == ScalarPower(
      base=-1,
      exponent=result.m,
    )
  )


def test_phase77_5a_second_coefficient_is_minus_one_power_t():
  data = build_phase77_5a_data()

  result = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  assert (
    result.second_coefficient
    == ScalarPower(
      base=-1,
      exponent=result.t,
    )
  )


def test_phase77_5a_reuses_both_bracket_objects():
  data = build_phase77_5a_data()

  first = (
    data[
      "first_term_step"
    ].conclusion
  )

  second = (
    data[
      "second_term_step"
    ].conclusion
  )

  result = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  assert (
    result.first_bracket
    is first.bracket
  )

  assert (
    result.second_bracket
    is second.bracket
  )


def test_phase77_5a_preserves_exact_direct_provenance():
  data = build_phase77_5a_data()

  step = (
    data[
      "bracket_sum_step"
    ]
  )

  assert (
    step.premises
    == data[
      "premise_steps"
    ]
  )

  assert (
    step.premises
    == (
      data[
        "first_term_step"
      ],
      data[
        "second_term_step"
      ],
    )
  )

  assert (
    step.inference_rule
    == data[
      "rule"
    ]
  )


def test_phase77_5a_reaches_fixed_point():
  data = build_phase77_5a_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase77_5a_rejects_given_first_branch():
  data = build_phase77_5a_data()

  first = (
    data[
      "first_term_step"
    ].conclusion
  )

  wrong_first_step = ProofStep(
    conclusion=first,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_first_step,
      data[
        "second_term_step"
      ],
    ),
  )

  assert match is None


def test_phase77_5a_rejects_given_second_branch():
  data = build_phase77_5a_data()

  second = (
    data[
      "second_term_step"
    ].conclusion
  )

  wrong_second_step = ProofStep(
    conclusion=second,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "first_term_step"
      ],
      wrong_second_step,
    ),
  )

  assert match is None


def test_phase77_5a_rejects_mismatched_composed_value():
  data = build_phase77_5a_data()

  second = (
    data[
      "second_term_step"
    ].conclusion
  )

  wrong_second = replace(
    second,
    composed_value=Composition(
      left=second.composed_value.left,
      right=second.beta,
    ),
  )

  wrong_second_step = ProofStep(
    conclusion=wrong_second,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  match = find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "first_term_step"
      ],
      wrong_second_step,
    ),
  )

  assert match is None


def test_phase77_5a_rejects_mismatched_beta():
  data = build_phase77_5a_data()

  second = (
    data[
      "second_term_step"
    ].conclusion
  )

  wrong_beta = replace(
    second.beta,
    name="γ",
  )

  wrong_second = replace(
    second,
    beta=wrong_beta,
  )

  wrong_second_step = ProofStep(
    conclusion=wrong_second,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  match = find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "first_term_step"
      ],
      wrong_second_step,
    ),
  )

  assert match is None


def test_phase77_5a_rejects_wrong_first_coefficient():
  data = build_phase77_5a_data()

  first = (
    data[
      "first_term_step"
    ].conclusion
  )

  wrong_first = replace(
    first,
    coefficient=ScalarPower(
      base=-1,
      exponent=first.t,
    ),
  )

  wrong_first_step = ProofStep(
    conclusion=wrong_first,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  match = find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_first_step,
      data[
        "second_term_step"
      ],
    ),
  )

  assert match is None


def test_phase77_5a_rejects_wrong_second_coefficient():
  data = build_phase77_5a_data()

  second = (
    data[
      "second_term_step"
    ].conclusion
  )

  wrong_second = replace(
    second,
    coefficient=ScalarPower(
      base=-1,
      exponent=second.m,
    ),
  )

  wrong_second_step = ProofStep(
    conclusion=wrong_second,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  match = find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "first_term_step"
      ],
      wrong_second_step,
    ),
  )

  assert match is None


def test_phase77_5a_has_no_odd_parameter_yet():
  data = build_phase77_5a_data()

  statement = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  assert not hasattr(
    statement,
    "odd_parameter",
  )

  assert not hasattr(
    statement,
    "odd_parameter_statement",
  )


