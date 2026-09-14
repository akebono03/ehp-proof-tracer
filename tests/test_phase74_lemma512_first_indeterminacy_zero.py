from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  ScalarSum,
  TodaBracket,
)
from homotopy_groups import (
  HomotopyGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase70_prop59_integration import (
  build_phase70_10_data,
)
from test_phase74_lemma512_bracket_defined import (
  build_phase74_2_data,
)
from toda_rules import (
  TodaBracketDefinedStatement,
  TodaLemma512FirstIndeterminacyZeroStatement,
  toda_lemma512_first_indeterminacy_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase74_3_data():
  phase74_2 = (
    build_phase74_2_data()
  )

  phase70_10 = (
    build_phase70_10_data()
  )

  bracket_defined_step = (
    phase74_2[
      "final_step"
    ]
  )

  prop59_step = (
    phase70_10[
      "integration_step"
    ]
  )

  n = (
    bracket_defined_step
    .conclusion
    .bracket
    .first
    .dimension
  )

  n_ge_6_step = (
    phase74_2[
      "n_ge_6_step"
    ]
  )

  rule = (
    toda_lemma512_first_indeterminacy_zero_inference_rule()
  )

  premise_steps = (
    bracket_defined_step,
    prop59_step,
    n_ge_6_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      premise_steps,
    )
  )

  expected_ordinary_group = (
    HomotopyGroup(
      group_dimension=ScalarSum(
        left=n,
        right=6,
      ),
      sphere_dimension=ScalarSum(
        left=n,
        right=1,
      ),
    )
  )

  expected_statement = (
    TodaLemma512FirstIndeterminacyZeroStatement(
      bracket=(
        bracket_defined_step
        .conclusion
        .bracket
      ),
      ordinary_group=(
        expected_ordinary_group
      ),
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase74_2": phase74_2,
    "phase70_10": phase70_10,
    "bracket_defined_step": (
      bracket_defined_step
    ),
    "prop59_step": prop59_step,
    "n": n,
    "n_ge_6_step": n_ge_6_step,
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "expected_ordinary_group": (
      expected_ordinary_group
    ),
    "expected_statement": (
      expected_statement
    ),
    "final_step": final_step,
  }


def test_phase74_3_reuses_derived_bracket_definedness():
  data = build_phase74_3_data()

  assert (
    data[
      "bracket_defined_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_3_reuses_derived_prop59_aggregate():
  data = build_phase74_3_data()

  assert (
    data[
      "prop59_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_3_scope_is_n_at_least_6():
  data = build_phase74_3_data()

  assert (
    data[
      "n_ge_6_step"
    ].conclusion
    == ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=6,
    )
  )

  assert (
    data[
      "n_ge_6_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase74_3_derives_first_indeterminacy_zero_statement():
  data = build_phase74_3_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_statement"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_3_preserves_exact_lemma512_bracket():
  data = build_phase74_3_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .bracket
    == data[
      "bracket_defined_step"
    ].conclusion
    .bracket
  )


def test_phase74_3_ordinary_group_is_pi_n_plus_6_s_n_plus_1():
  data = build_phase74_3_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .ordinary_group
    == data[
      "expected_ordinary_group"
    ]
  )

  assert isinstance(
    data[
      "final_step"
    ].conclusion
    .ordinary_group,
    HomotopyGroup,
  )


def test_phase74_3_does_not_replace_ordinary_group_with_toda_group():
  data = build_phase74_3_data()

  ordinary_group = (
    data[
      "final_step"
    ].conclusion
    .ordinary_group
  )

  assert type(
    ordinary_group
  ) is HomotopyGroup


def test_phase74_3_final_step_uses_exact_direct_premises():
  data = build_phase74_3_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "bracket_defined_step"
      ],
      data[
        "prop59_step"
      ],
      data[
        "n_ge_6_step"
      ],
    )
  )


def test_phase74_3_final_statement_not_present_initially():
  data = build_phase74_3_data()

  assert (
    data[
      "expected_statement"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase74_3_rejects_given_bracket_definedness():
  data = build_phase74_3_data()

  given_bracket = ProofStep(
    conclusion=(
      data[
        "bracket_defined_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      given_bracket,
      data[
        "prop59_step"
      ],
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_3_rejects_given_prop59_aggregate():
  data = build_phase74_3_data()

  given_prop59 = ProofStep(
    conclusion=(
      data[
        "prop59_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "bracket_defined_step"
      ],
      given_prop59,
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_3_rejects_wrong_range():
  data = build_phase74_3_data()

  wrong_range = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=5,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "bracket_defined_step"
      ],
      data[
        "prop59_step"
      ],
      wrong_range,
    ),
  ) is None


def test_phase74_3_rejects_wrong_first_bracket_element():
  data = build_phase74_3_data()

  bracket = (
    data[
      "bracket_defined_step"
    ].conclusion
    .bracket
  )

  n = data[
    "n"
  ]

  wrong_eta = HomotopyElement(
    name="wrong eta_n",
    dimension=n,
    source=ScalarSum(
      left=n,
      right=1,
    ),
    target=n,
    generator=GeneratorSymbol(
      family="η",
      index=ScalarSum(
        left=n,
        right=1,
      ),
    ),
  )

  wrong_bracket = TodaBracket(
    first=wrong_eta,
    second=bracket.second,
    third=bracket.third,
  )

  wrong_defined_step = ProofStep(
    conclusion=TodaBracketDefinedStatement(
      bracket=wrong_bracket,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_defined_step,
      data[
        "prop59_step"
      ],
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_3_rejects_wrong_prop59_higher_range():
  data = build_phase74_3_data()

  prop59 = (
    data[
      "prop59_step"
    ].conclusion
  )

  higher_n = (
    prop59
    .higher_five_stem_zero
    .group
    .sphere_dimension
  )

  wrong_prop59 = replace(
    prop59,
    higher_range=ScalarGreaterEqualStatement(
      left=higher_n,
      right=6,
    ),
  )

  wrong_prop59_step = ProofStep(
    conclusion=wrong_prop59,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "bracket_defined_step"
      ],
      wrong_prop59_step,
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_3_reaches_fixed_point():
  data = build_phase74_3_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


