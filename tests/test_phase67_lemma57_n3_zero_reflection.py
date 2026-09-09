from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  Suspension,
  Zero,
)
from homotopy_groups import (
  TodaPrimaryGroup,
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
from test_phase67_lemma57_first_branch import (
  build_phase67_3_data,
)
from toda_rules import (
  TodaLemma57TwoIota5ImageMembershipStatement,
  toda_lemma45_n3_suspension_zero_reflection_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase67_4_data():
  phase67_3 = (
    build_phase67_3_data()
  )

  double_suspension_zero_step = next(
    step
    for step in phase67_3[
      "result"
    ].steps
    if (
      step.conclusion
      == phase67_3[
        "final_zero"
      ]
    )
  )

  rule = (
    toda_lemma45_n3_suspension_zero_reflection_inference_rule()
  )

  premise_steps = (
    phase67_3[
      "hypothesis_step"
    ],
    double_suspension_zero_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      premise_steps,
    )
  )

  eta2_alpha = Composition(
    left=phase67_3[
      "eta_2"
    ],
    right=phase67_3[
      "alpha"
    ],
  )

  expected_statement = Relation(
    lhs=Suspension(
      expression=eta2_alpha,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
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
    "phase67_3": phase67_3,
    "double_suspension_zero_step": (
      double_suspension_zero_step
    ),
    "rule": rule,
    "premise_steps": premise_steps,
    "result": result,
    "eta2_alpha": eta2_alpha,
    "expected_statement": (
      expected_statement
    ),
    "final_step": final_step,
  }


def test_phase67_4_reuses_phase67_3_double_suspension_zero():
  data = build_phase67_4_data()

  assert (
    data[
      "double_suspension_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_4_hypothesis_has_expected_statement_type():
  data = build_phase67_4_data()

  assert isinstance(
    data[
      "phase67_3"
    ][
      "hypothesis_step"
    ].conclusion,
    TodaLemma57TwoIota5ImageMembershipStatement,
  )


def test_phase67_4_rule_matches_dependencies():
  data = build_phase67_4_data()

  assert find_inference_match(
    data[
      "rule"
    ],
    data[
      "premise_steps"
    ],
  ) is not None


def test_phase67_4_derives_single_suspension_zero():
  data = build_phase67_4_data()

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


def test_phase67_4_result_is_e_eta2_alpha_zero():
  data = build_phase67_4_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == Relation(
      lhs=Suspension(
        expression=Composition(
          left=data[
            "phase67_3"
          ][
            "eta_2"
          ],
          right=data[
            "phase67_3"
          ][
            "alpha"
          ],
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )


def test_phase67_4_preserves_exact_two_premises():
  data = build_phase67_4_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "phase67_3"
      ][
        "hypothesis_step"
      ],
      data[
        "double_suspension_zero_step"
      ],
    )
  )


def test_phase67_4_accepts_inference_hypothesis():
  data = build_phase67_4_data()

  inference_hypothesis = ProofStep(
    conclusion=(
      data[
        "phase67_3"
      ][
        "hypothesis"
      ]
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      inference_hypothesis,
      data[
        "double_suspension_zero_step"
      ],
    ),
  ) is not None


def test_phase67_4_rejects_given_double_suspension_zero():
  data = build_phase67_4_data()

  given_zero = ProofStep(
    conclusion=(
      data[
        "double_suspension_zero_step"
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
        "phase67_3"
      ][
        "hypothesis_step"
      ],
      given_zero,
    ),
  ) is None


def test_phase67_4_rejects_wrong_double_suspension_exponent():
  data = build_phase67_4_data()

  wrong_zero = ProofStep(
    conclusion=Relation(
      lhs=IteratedSuspension(
        expression=data[
          "eta2_alpha"
        ],
        exponent=3,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "phase67_3"
      ][
        "hypothesis_step"
      ],
      wrong_zero,
    ),
  ) is None


def test_phase67_4_rejects_wrong_hypothesis_source_group():
  data = build_phase67_4_data()

  original = (
    data[
      "phase67_3"
    ][
      "hypothesis"
    ]
  )

  wrong_hypothesis = replace(
    original,
    source_group=TodaPrimaryGroup(
      group_dimension=(
        original
        .source_group
        .group_dimension
      ),
      sphere_dimension=4,
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_hypothesis,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      wrong_step,
      data[
        "double_suspension_zero_step"
      ],
    ),
  ) is None


def test_phase67_4_rejects_wrong_zero_expression():
  data = build_phase67_4_data()

  wrong_zero = ProofStep(
    conclusion=Relation(
      lhs=IteratedSuspension(
        expression=(
          data[
            "phase67_3"
          ][
            "alpha"
          ]
        ),
        exponent=2,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      data[
        "phase67_3"
      ][
        "hypothesis_step"
      ],
      wrong_zero,
    ),
  ) is None


def test_phase67_4_final_result_is_not_given():
  data = build_phase67_4_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase67_4_reaches_fixed_point_in_one_round():
  data = build_phase67_4_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    data[
      "result"
    ].round_count
    == 1
  )

  assert (
    data[
      "final_step"
    ]
    in data[
      "result"
    ].round_results[
      0
    ].new_steps
  )


def test_phase67_4_rule_accepts_concrete_nu_prime_branch():
  data = build_phase67_4_data()

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  eta_2 = (
    data[
      "phase67_3"
    ][
      "eta_2"
    ]
  )

  hypothesis = (
    TodaLemma57TwoIota5ImageMembershipStatement(
      element=IteratedSuspension(
        expression=nu_prime,
        exponent=2,
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      ),
    )
  )

  hypothesis_step = ProofStep(
    conclusion=hypothesis,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  double_zero_step = ProofStep(
    conclusion=Relation(
      lhs=IteratedSuspension(
        expression=Composition(
          left=eta_2,
          right=nu_prime,
        ),
        exponent=2,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "rule"
    ],
    (
      hypothesis_step,
      double_zero_step,
    ),
  ) is not None


