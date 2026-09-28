from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  ScalarSum,
  TodaBracket,
  Zero,
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
  ScalarGreaterEqualStatement,
)
from test_phase68_eta_n_nu_n_plus_one_zero import (
  build_phase68_8_data,
)
from test_phase68_nu_n_eta_n_plus_three_zero import (
  build_phase68_9_data,
)
from toda_rules import (
  TodaBracketDefinedStatement,
  toda_bracket_defined_by_zero_compositions_inference_rule,
  toda_lemma512_shifted_nu_eta_zero_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase74_2_data():
  phase68_8 = (
    build_phase68_8_data()
  )

  phase68_9 = (
    build_phase68_9_data()
  )

  eta_n_nu_n_plus_one_zero_step = (
    phase68_8[
      "final_step"
    ]
  )

  nu_n_eta_n_plus_three_zero_step = (
    phase68_9[
      "final_step"
    ]
  )

  nu_n = (
    nu_n_eta_n_plus_three_zero_step
    .conclusion
    .lhs
    .left
  )

  n = (
    nu_n.dimension
  )

  n_ge_6_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=n,
      right=6,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  shifted_zero_rule = (
    toda_lemma512_shifted_nu_eta_zero_inference_rule()
  )

  bracket_defined_rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  rules = (
    shifted_zero_rule,
    bracket_defined_rule,
  )

  premise_steps = (
    eta_n_nu_n_plus_one_zero_step,
    nu_n_eta_n_plus_three_zero_step,
    n_ge_6_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  eta_n = (
    eta_n_nu_n_plus_one_zero_step
    .conclusion
    .lhs
    .left
  )

  nu_n_plus_one = (
    eta_n_nu_n_plus_one_zero_step
    .conclusion
    .lhs
    .right
  )

  n_plus_four = ScalarSum(
    left=n,
    right=4,
  )

  n_plus_five = ScalarSum(
    left=n,
    right=5,
  )

  eta_n_plus_four = HomotopyElement(
    name="η_(n+4)",
    dimension=n_plus_four,
    source=n_plus_five,
    target=n_plus_four,
    generator=GeneratorSymbol(
      family="η",
      index=n_plus_four,
    ),
  )

  expected_shifted_zero = Relation(
    lhs=Composition(
      left=nu_n_plus_one,
      right=eta_n_plus_four,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  shifted_zero_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_shifted_zero
    )
  )

  expected_bracket = TodaBracket(
    first=eta_n,
    second=nu_n_plus_one,
    third=eta_n_plus_four,
  )

  expected_defined = (
    TodaBracketDefinedStatement(
      bracket=expected_bracket,
    )
  )

  final_step = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_defined
    )
  )

  return {
    "phase68_8": phase68_8,
    "phase68_9": phase68_9,
    "eta_n_nu_n_plus_one_zero_step": (
      eta_n_nu_n_plus_one_zero_step
    ),
    "nu_n_eta_n_plus_three_zero_step": (
      nu_n_eta_n_plus_three_zero_step
    ),
    "n": n,
    "n_ge_6_step": n_ge_6_step,
    "shifted_zero_rule": shifted_zero_rule,
    "bracket_defined_rule": (
      bracket_defined_rule
    ),
    "premise_steps": premise_steps,
    "result": result,
    "eta_n": eta_n,
    "nu_n_plus_one": nu_n_plus_one,
    "eta_n_plus_four": eta_n_plus_four,
    "expected_shifted_zero": (
      expected_shifted_zero
    ),
    "shifted_zero_step": shifted_zero_step,
    "expected_bracket": expected_bracket,
    "expected_defined": expected_defined,
    "final_step": final_step,
  }


def test_phase74_2_reuses_eta_n_nu_n_plus_one_zero():
  data = build_phase74_2_data()

  assert (
    data[
      "eta_n_nu_n_plus_one_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "eta_n_nu_n_plus_one_zero_step"
    ].conclusion
    == Relation(
      lhs=Composition(
        left=data[
          "eta_n"
        ],
        right=data[
          "nu_n_plus_one"
        ],
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )


def test_phase74_2_reuses_nu_n_eta_n_plus_three_zero():
  data = build_phase74_2_data()

  assert (
    data[
      "nu_n_eta_n_plus_three_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_2_derives_shifted_nu_eta_zero():
  data = build_phase74_2_data()

  assert (
    data[
      "shifted_zero_step"
    ].conclusion
    == data[
      "expected_shifted_zero"
    ]
  )

  assert (
    data[
      "shifted_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_2_shifted_zero_uses_exact_dependencies():
  data = build_phase74_2_data()

  assert (
    data[
      "shifted_zero_step"
    ].premises
    == (
      data[
        "nu_n_eta_n_plus_three_zero_step"
      ],
      data[
        "n_ge_6_step"
      ],
    )
  )


def test_phase74_2_shifted_zero_matches_first_zero_middle_element():
  data = build_phase74_2_data()

  first_middle = (
    data[
      "eta_n_nu_n_plus_one_zero_step"
    ].conclusion
    .lhs
    .right
  )

  second_middle = (
    data[
      "shifted_zero_step"
    ].conclusion
    .lhs
    .left
  )

  assert first_middle == second_middle


def test_phase74_2_derives_lemma512_bracket_defined():
  data = build_phase74_2_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_defined"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_2_defined_bracket_has_expected_entries():
  data = build_phase74_2_data()

  bracket = (
    data[
      "final_step"
    ].conclusion
    .bracket
  )

  assert (
    bracket.first
    == data[
      "eta_n"
    ]
  )

  assert (
    bracket.second
    == data[
      "nu_n_plus_one"
    ]
  )

  assert (
    bracket.third
    == data[
      "eta_n_plus_four"
    ]
  )


def test_phase74_2_defined_bracket_is_unindexed():
  data = build_phase74_2_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .bracket
    .index
    is None
  )


def test_phase74_2_definedness_uses_exact_two_zero_relations():
  data = build_phase74_2_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "eta_n_nu_n_plus_one_zero_step"
      ],
      data[
        "shifted_zero_step"
      ],
    )
  )


def test_phase74_2_rejects_given_higher_nu_eta_zero():
  data = build_phase74_2_data()

  given = ProofStep(
    conclusion=(
      data[
        "nu_n_eta_n_plus_three_zero_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "shifted_zero_rule"
    ],
    (
      given,
      data[
        "n_ge_6_step"
      ],
    ),
  ) is None


def test_phase74_2_rejects_wrong_range():
  data = build_phase74_2_data()

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
      "shifted_zero_rule"
    ],
    (
      data[
        "nu_n_eta_n_plus_three_zero_step"
      ],
      wrong_range,
    ),
  ) is None


def test_phase74_2_rejects_mismatched_middle_element():
  data = build_phase74_2_data()

  wrong_nu = HomotopyElement(
    name="wrong ν",
    dimension=(
      data[
        "nu_n_plus_one"
      ].dimension
    ),
    source=(
      data[
        "nu_n_plus_one"
      ].source
    ),
    target=(
      data[
        "nu_n_plus_one"
      ].target
    ),
    generator=GeneratorSymbol(
      family="ν",
      index=ScalarSum(
        left=data[
          "n"
        ],
        right=2,
      ),
    ),
  )

  wrong_zero = ProofStep(
    conclusion=Relation(
      lhs=Composition(
        left=data[
          "eta_n"
        ],
        right=wrong_nu,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "bracket_defined_rule"
    ],
    (
      wrong_zero,
      data[
        "shifted_zero_step"
      ],
    ),
  ) is None


def test_phase74_2_final_result_not_present_initially():
  data = build_phase74_2_data()

  assert (
    data[
      "expected_defined"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase74_2_reaches_fixed_point():
  data = build_phase74_2_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )



