from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  GeneratorSymbol,
  IteratedSuspension,
  Multiple,
  ScalarPower,
  ScalarProduct,
  ScalarSum,
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
from test_phase77_sigma8_iterated_suspension_bridge import (
  build_phase77_5b_data,
)
from test_phase77_theorem36_bracket_sum import (
  build_phase77_5a_data,
)
from toda_rules import (
  Toda36Lemma516BracketSumContainmentStatement,
  TodaLemma516BracketSumContainmentStatement,
  TodaLemma516ScaledCompositionBridgeStatement,
  TodaLemma516Sigma8IteratedSuspensionBridgeStatement,
  TodaLemma516SigmaTPlus8DefinitionStatement,
  toda_lemma516_scaled_bracket_sum_inference_rule,
  toda_lemma516_scaled_composition_bridge_inference_rule,
  toda_lemma516_sigma_t_plus_8_definition_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase77_5c_data():
  phase77_5a = (
    build_phase77_5a_data()
  )

  phase77_5b = (
    build_phase77_5b_data()
  )

  bracket_sum_step = (
    phase77_5a[
      "bracket_sum_step"
    ]
  )

  suspension_bridge_step = (
    phase77_5b[
      "bridge_step"
    ]
  )

  sigma_definition_rule = (
    toda_lemma516_sigma_t_plus_8_definition_inference_rule()
  )

  sigma_definition_result = (
    run_inference_until_stable_with_history(
      sigma_definition_rule,
      (
        suspension_bridge_step,
      ),
    )
  )

  sigma_definition_step = next(
    step
    for step in sigma_definition_result.steps
    if isinstance(
      step.conclusion,
      TodaLemma516SigmaTPlus8DefinitionStatement,
    )
  )

  composition_rule = (
    toda_lemma516_scaled_composition_bridge_inference_rule()
  )

  composition_premises = (
    bracket_sum_step,
    suspension_bridge_step,
    sigma_definition_step,
  )

  composition_result = (
    run_inference_until_stable_with_history(
      composition_rule,
      composition_premises,
    )
  )

  composition_step = next(
    step
    for step in composition_result.steps
    if isinstance(
      step.conclusion,
      TodaLemma516ScaledCompositionBridgeStatement,
    )
  )

  final_rule = (
    toda_lemma516_scaled_bracket_sum_inference_rule()
  )

  final_premises = (
    bracket_sum_step,
    composition_step,
  )

  final_result = (
    run_inference_until_stable_with_history(
      final_rule,
      final_premises,
    )
  )

  final_step = next(
    step
    for step in final_result.steps
    if isinstance(
      step.conclusion,
      TodaLemma516BracketSumContainmentStatement,
    )
  )

  return {
    "phase77_5a": phase77_5a,
    "phase77_5b": phase77_5b,
    "bracket_sum_step": (
      bracket_sum_step
    ),
    "suspension_bridge_step": (
      suspension_bridge_step
    ),
    "sigma_definition_rule": (
      sigma_definition_rule
    ),
    "sigma_definition_result": (
      sigma_definition_result
    ),
    "sigma_definition_step": (
      sigma_definition_step
    ),
    "composition_rule": (
      composition_rule
    ),
    "composition_premises": (
      composition_premises
    ),
    "composition_result": (
      composition_result
    ),
    "composition_step": (
      composition_step
    ),
    "final_rule": final_rule,
    "final_premises": final_premises,
    "final_result": final_result,
    "final_step": final_step,
  }


def test_phase77_5c_sigma_definition_is_inference():
  data = build_phase77_5c_data()

  step = data[
    "sigma_definition_step"
  ]

  assert isinstance(
    step.conclusion,
    TodaLemma516SigmaTPlus8DefinitionStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_5c_sigma_t_plus_8_has_expected_structure():
  data = build_phase77_5c_data()

  definition = (
    data[
      "sigma_definition_step"
    ].conclusion
  )

  t = definition.t

  sigma = (
    definition
    .sigma_t_plus_8
  )

  assert (
    sigma.dimension
    == ScalarSum(
      left=t,
      right=8,
    )
  )

  assert (
    sigma.source
    == ScalarSum(
      left=t,
      right=15,
    )
  )

  assert (
    sigma.target
    == ScalarSum(
      left=t,
      right=8,
    )
  )

  assert (
    sigma.generator
    == GeneratorSymbol(
      family="σ",
      index=ScalarSum(
        left=t,
        right=8,
      ),
    )
  )


def test_phase77_5c_sigma_definition_is_et_sigma8():
  data = build_phase77_5c_data()

  definition = (
    data[
      "sigma_definition_step"
    ].conclusion
  )

  suspension_bridge = (
    data[
      "suspension_bridge_step"
    ].conclusion
  )

  assert (
    definition.iterated_suspension
    == IteratedSuspension(
      expression=(
        suspension_bridge
        .sigma8
      ),
      exponent=definition.t,
    )
  )


def test_phase77_5c_composition_bridge_is_inference():
  data = build_phase77_5c_data()

  assert isinstance(
    data[
      "composition_step"
    ].conclusion,
    TodaLemma516ScaledCompositionBridgeStatement,
  )

  assert (
    data[
      "composition_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase77_5c_scaled_left_side_is_e4_beta_sigma_t_plus_8():
  data = build_phase77_5c_data()

  bracket_sum = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  definition = (
    data[
      "sigma_definition_step"
    ].conclusion
  )

  bridge = (
    data[
      "composition_step"
    ].conclusion
  )

  assert isinstance(
    bracket_sum,
    Toda36Lemma516BracketSumContainmentStatement,
  )

  assert (
    bridge.scaled_composed_value
    == Composition(
      left=(
        bracket_sum
        .element
        .left
      ),
      right=(
        definition
        .sigma_t_plus_8
      ),
    )
  )


def test_phase77_5c_composition_relation_is_expected():
  data = build_phase77_5c_data()

  bracket_sum = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  bridge = (
    data[
      "composition_step"
    ].conclusion
  )

  expected = Relation(
    lhs=(
      bridge
      .scaled_composed_value
    ),
    rhs=Multiple(
      coefficient=(
        bridge
        .odd_parameter
      ),
      expression=(
        bracket_sum
        .element
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    bridge.relation
    == expected
  )


def test_phase77_5c_reuses_same_odd_parameter():
  data = build_phase77_5c_data()

  suspension_bridge = (
    data[
      "suspension_bridge_step"
    ].conclusion
  )

  composition_bridge = (
    data[
      "composition_step"
    ].conclusion
  )

  assert isinstance(
    suspension_bridge,
    TodaLemma516Sigma8IteratedSuspensionBridgeStatement,
  )

  assert (
    composition_bridge.odd_parameter
    is suspension_bridge.odd_parameter
  )

  assert (
    composition_bridge.odd_parameter_statement
    is suspension_bridge.odd_parameter_statement
  )


def test_phase77_5c_final_statement_is_inference():
  data = build_phase77_5c_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaLemma516BracketSumContainmentStatement,
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase77_5c_final_element_is_e4_beta_sigma_t_plus_8():
  data = build_phase77_5c_data()

  final_statement = (
    data[
      "final_step"
    ].conclusion
  )

  composition_bridge = (
    data[
      "composition_step"
    ].conclusion
  )

  assert (
    final_statement.element
    is (
      composition_bridge
      .scaled_composed_value
    )
  )


def test_phase77_5c_final_first_coefficient_is_sign_m_times_x():
  data = build_phase77_5c_data()

  final_statement = (
    data[
      "final_step"
    ].conclusion
  )

  x = (
    final_statement
    .odd_parameter
  )

  m = (
    data[
      "bracket_sum_step"
    ]
    .conclusion
    .m
  )

  assert (
    final_statement
    .first_coefficient
    == ScalarProduct(
      left=ScalarPower(
        base=-1,
        exponent=m,
      ),
      right=x,
    )
  )


def test_phase77_5c_final_second_coefficient_is_sign_t_times_x():
  data = build_phase77_5c_data()

  final_statement = (
    data[
      "final_step"
    ].conclusion
  )

  x = (
    final_statement
    .odd_parameter
  )

  t = (
    data[
      "bracket_sum_step"
    ]
    .conclusion
    .t
  )

  assert (
    final_statement
    .second_coefficient
    == ScalarProduct(
      left=ScalarPower(
        base=-1,
        exponent=t,
      ),
      right=x,
    )
  )


def test_phase77_5c_reuses_original_bracket_objects():
  data = build_phase77_5c_data()

  source = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  final_statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    final_statement
    .first_bracket
    is source.first_bracket
  )

  assert (
    final_statement
    .second_bracket
    is source.second_bracket
  )


def test_phase77_5c_final_preserves_odd_statement():
  data = build_phase77_5c_data()

  bridge = (
    data[
      "composition_step"
    ].conclusion
  )

  final_statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    final_statement
    .odd_parameter
    is bridge.odd_parameter
  )

  assert (
    final_statement
    .odd_parameter_statement
    is bridge.odd_parameter_statement
  )


def test_phase77_5c_composition_direct_premises_are_expected():
  data = build_phase77_5c_data()

  assert (
    data[
      "composition_step"
    ].premises
    == data[
      "composition_premises"
    ]
  )


def test_phase77_5c_final_direct_premises_are_expected():
  data = build_phase77_5c_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "bracket_sum_step"
      ],
      data[
        "composition_step"
      ],
    )
  )


def test_phase77_5c_all_new_results_reach_fixed_point():
  data = build_phase77_5c_data()

  assert (
    data[
      "sigma_definition_result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    data[
      "composition_result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    data[
      "final_result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase77_5c_rejects_given_bracket_sum():
  data = build_phase77_5c_data()

  bracket_sum = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  wrong_step = ProofStep(
    conclusion=bracket_sum,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    data[
      "composition_rule"
    ],
    (
      wrong_step,
      data[
        "suspension_bridge_step"
      ],
      data[
        "sigma_definition_step"
      ],
    ),
  )

  assert match is None


def test_phase77_5c_rejects_given_composition_bridge():
  data = build_phase77_5c_data()

  bridge = (
    data[
      "composition_step"
    ].conclusion
  )

  wrong_step = ProofStep(
    conclusion=bridge,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "bracket_sum_step"
      ],
      wrong_step,
    ),
  )

  assert match is None


def test_phase77_5c_rejects_wrong_odd_parameter():
  data = build_phase77_5c_data()

  bridge = (
    data[
      "composition_step"
    ].conclusion
  )

  wrong_x = replace(
    bridge.odd_parameter,
    name="z",
  )

  wrong_bridge = replace(
    bridge,
    odd_parameter=wrong_x,
  )

  wrong_step = ProofStep(
    conclusion=wrong_bridge,
    premises=(
      data[
        "composition_step"
      ].premises
    ),
    rule=ProofRule.INFERENCE,
  )

  match = find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "bracket_sum_step"
      ],
      wrong_step,
    ),
  )

  assert match is None


