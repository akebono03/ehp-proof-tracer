from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  ScalarSum,
  Zero,
)
from homotopy_groups import (
  FreeCyclicGroup,
  HomotopyGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from map_facts import (
  EHP_DELTA_MAP,
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
from test_phase70_prop59_integration import (
  build_phase70_10_data,
)
from test_phase73_513_delta_eta13 import (
  build_phase73_6c_data,
)
from test_phase74_lemma512_bracket_defined import (
  build_phase74_2_data,
)
from toda_rules import (
  TodaLemma512SecondIndeterminacyHigherZeroStatement,
  TodaLemma512SecondIndeterminacyN6ZeroStatement,
  TodaLemma512SecondIndeterminacyZeroStatement,
  toda_lemma512_second_indeterminacy_higher_zero_inference_rule,
  toda_lemma512_second_indeterminacy_n6_zero_inference_rule,
  toda_lemma512_second_indeterminacy_zero_integration_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase74_4_data():
  phase74_2 = (
    build_phase74_2_data()
  )

  phase70_10 = (
    build_phase70_10_data()
  )

  phase73_6c = (
    build_phase73_6c_data()
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

  delta_eta13_step = (
    phase73_6c[
      "final_step"
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

  higher_rule = (
    toda_lemma512_second_indeterminacy_higher_zero_inference_rule()
  )

  n6_rule = (
    toda_lemma512_second_indeterminacy_n6_zero_inference_rule()
  )

  integration_rule = (
    toda_lemma512_second_indeterminacy_zero_integration_inference_rule()
  )

  rules = (
    higher_rule,
    n6_rule,
    integration_rule,
  )

  premise_steps = (
    bracket_defined_step,
    prop59_step,
    delta_eta13_step,
    n_ge_6_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  higher_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaLemma512SecondIndeterminacyHigherZeroStatement,
    )
  )

  n6_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaLemma512SecondIndeterminacyN6ZeroStatement,
    )
  )

  expected_final = (
    TodaLemma512SecondIndeterminacyZeroStatement(
      bracket=(
        bracket_defined_step
        .conclusion
        .bracket
      ),
      ordinary_group=HomotopyGroup(
        group_dimension=ScalarSum(
          left=n,
          right=5,
        ),
        sphere_dimension=n,
      ),
      n_range=n_ge_6_step.conclusion,
    )
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
    "phase74_2": phase74_2,
    "phase70_10": phase70_10,
    "phase73_6c": phase73_6c,
    "bracket_defined_step": (
      bracket_defined_step
    ),
    "prop59_step": prop59_step,
    "delta_eta13_step": (
      delta_eta13_step
    ),
    "n": n,
    "n_ge_6_step": n_ge_6_step,
    "higher_rule": higher_rule,
    "n6_rule": n6_rule,
    "integration_rule": (
      integration_rule
    ),
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "higher_step": higher_step,
    "n6_step": n6_step,
    "expected_final": expected_final,
    "final_step": final_step,
  }


def test_phase74_4_reuses_derived_prop59():
  data = build_phase74_4_data()

  assert (
    data[
      "prop59_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_4_reuses_derived_delta_eta13_zero():
  data = build_phase74_4_data()

  assert (
    data[
      "delta_eta13_step"
    ].rule
    == ProofRule.INFERENCE
  )

  conclusion = (
    data[
      "delta_eta13_step"
    ].conclusion
  )

  assert isinstance(
    conclusion,
    Relation,
  )

  assert (
    conclusion.relation_type
    == RelationType.ZERO
  )

  assert isinstance(
    conclusion.lhs,
    MapApplication,
  )

  assert (
    conclusion.lhs.map
    == EHP_DELTA_MAP
  )


def test_phase74_4_derives_higher_second_indeterminacy_zero():
  data = build_phase74_4_data()

  step = (
    data[
      "higher_step"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    step.conclusion,
    TodaLemma512SecondIndeterminacyHigherZeroStatement,
  )

  assert (
    step.conclusion
    .n_range
    .right
    == 7
  )


def test_phase74_4_higher_branch_keeps_ordinary_group():
  data = build_phase74_4_data()

  group = (
    data[
      "higher_step"
    ].conclusion
    .ordinary_group
  )

  assert type(
    group
  ) is HomotopyGroup


def test_phase74_4_higher_branch_uses_eta_n_plus_5():
  data = build_phase74_4_data()

  statement = (
    data[
      "higher_step"
    ].conclusion
  )

  n = (
    statement
    .ordinary_group
    .sphere_dimension
  )

  expected_index = ScalarSum(
    left=n,
    right=5,
  )

  assert (
    statement
    .right_factor
    .generator
    == GeneratorSymbol(
      family="η",
      index=expected_index,
    )
  )


def test_phase74_4_derives_n6_second_indeterminacy_zero():
  data = build_phase74_4_data()

  step = (
    data[
      "n6_step"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    step.conclusion,
    TodaLemma512SecondIndeterminacyN6ZeroStatement,
  )


def test_phase74_4_n6_group_is_pi11_s6():
  data = build_phase74_4_data()

  assert (
    data[
      "n6_step"
    ].conclusion
    .ordinary_group
    == HomotopyGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )


def test_phase74_4_n6_generator_is_delta_iota13():
  data = build_phase74_4_data()

  generator = (
    data[
      "n6_step"
    ].conclusion
    .generator
  )

  assert isinstance(
    generator,
    MapApplication,
  )

  assert (
    generator.map
    == EHP_DELTA_MAP
  )

  iota_13 = (
    generator.expression
  )

  assert (
    iota_13.generator
    == GeneratorSymbol(
      family="ι",
      index=13,
    )
  )


def test_phase74_4_n6_right_factor_is_eta11():
  data = build_phase74_4_data()

  eta_11 = (
    data[
      "n6_step"
    ].conclusion
    .right_factor
  )

  assert (
    eta_11.generator
    == GeneratorSymbol(
      family="η",
      index=11,
    )
  )


def test_phase74_4_n6_zero_composition_is_delta_iota13_eta11():
  data = build_phase74_4_data()

  statement = (
    data[
      "n6_step"
    ].conclusion
  )

  assert (
    statement.zero_composition
    == Composition(
      left=statement.generator,
      right=statement.right_factor,
    )
  )


def test_phase74_4_n6_direct_premises_are_prop59_and_delta_eta13():
  data = build_phase74_4_data()

  assert (
    data[
      "n6_step"
    ].premises
    == (
      data[
        "prop59_step"
      ],
      data[
        "delta_eta13_step"
      ],
    )
  )


def test_phase74_4_integrates_second_indeterminacy_zero():
  data = build_phase74_4_data()

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


def test_phase74_4_final_scope_is_n_at_least_6():
  data = build_phase74_4_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .n_range
    == ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=6,
    )
  )


def test_phase74_4_final_ordinary_group_is_pi_n_plus_5_s_n():
  data = build_phase74_4_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .ordinary_group
    == HomotopyGroup(
      group_dimension=ScalarSum(
        left=data[
          "n"
        ],
        right=5,
      ),
      sphere_dimension=data[
        "n"
      ],
    )
  )


def test_phase74_4_final_preserves_lemma512_bracket():
  data = build_phase74_4_data()

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


def test_phase74_4_final_step_uses_exact_four_premises():
  data = build_phase74_4_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "bracket_defined_step"
      ],
      data[
        "higher_step"
      ],
      data[
        "n6_step"
      ],
      data[
        "n_ge_6_step"
      ],
    )
  )


def test_phase74_4_rejects_given_prop59_for_higher_branch():
  data = build_phase74_4_data()

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
      "higher_rule"
    ],
    (
      given_prop59,
    ),
  ) is None


def test_phase74_4_rejects_given_delta_eta13_for_n6():
  data = build_phase74_4_data()

  given_delta_eta13 = ProofStep(
    conclusion=(
      data[
        "delta_eta13_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "n6_rule"
    ],
    (
      data[
        "prop59_step"
      ],
      given_delta_eta13,
    ),
  ) is None


def test_phase74_4_rejects_wrong_prop59_higher_zero():
  data = build_phase74_4_data()

  prop59 = (
    data[
      "prop59_step"
    ].conclusion
  )

  higher_group = (
    prop59
    .higher_five_stem_zero
    .group
  )

  wrong_prop59 = replace(
    prop59,
    higher_five_stem_zero=(
      TodaPrimaryGroupZeroStatement(
        group=TodaPrimaryGroup(
          group_dimension=(
            higher_group
            .group_dimension
          ),
          sphere_dimension=ScalarSum(
            left=(
              higher_group
              .sphere_dimension
            ),
            right=1,
          ),
        ),
      )
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_prop59,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "higher_rule"
    ],
    (
      wrong_step,
    ),
  ) is None


def test_phase74_4_rejects_wrong_delta_eta13_argument():
  data = build_phase74_4_data()

  wrong_eta = HomotopyElement(
    name="wrong η₁₃",
    dimension=13,
    source=14,
    target=13,
    generator=GeneratorSymbol(
      family="η",
      index=12,
    ),
  )

  wrong_delta = ProofStep(
    conclusion=Relation(
      lhs=MapApplication(
        map=EHP_DELTA_MAP,
        expression=wrong_eta,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "n6_rule"
    ],
    (
      data[
        "prop59_step"
      ],
      wrong_delta,
    ),
  ) is None


def test_phase74_4_rejects_wrong_final_range():
  data = build_phase74_4_data()

  wrong_range = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=data[
        "n"
      ],
      right=7,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      data[
        "bracket_defined_step"
      ],
      data[
        "higher_step"
      ],
      data[
        "n6_step"
      ],
      wrong_range,
    ),
  ) is None


def test_phase74_4_final_statement_not_present_initially():
  data = build_phase74_4_data()

  assert (
    data[
      "expected_final"
    ]
    not in tuple(
      step.conclusion
      for step in data[
        "premise_steps"
      ]
    )
  )


def test_phase74_4_reaches_fixed_point():
  data = build_phase74_4_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


