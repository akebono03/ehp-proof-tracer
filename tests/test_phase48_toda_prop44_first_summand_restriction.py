from typing import (
  get_type_hints,
)

from expression import (
  Composition,
  HomotopyElement,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
  TodaSuspensionMap,
)
from map_property_rules import (
  InjectiveMapStatement,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaProp44FirstSummandRestrictionStatement,
  toda_prop44_first_summand_restriction_inference_rule,
)


def build_phase48_3_data(
  i_name="i",
  n_name="n",
):
  i = ScalarSymbol(
    name=i_name,
  )

  n = ScalarSymbol(
    name=n_name,
  )

  i_minus_one = ScalarSum(
    left=i,
    right=-1,
  )

  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  two_n_minus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  first_summand = TodaPrimaryGroup(
    group_dimension=i_minus_one,
    sphere_dimension=n_minus_one,
  )

  second_summand = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=two_n_minus_one,
  )

  source_group = DirectSumGroup(
    summands=(
      first_summand,
      second_summand,
    ),
  )

  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=n,
  )

  alpha = HomotopyElement(
    name="α",
    dimension=two_n_minus_one,
  )

  beta = HomotopyElement(
    name="β",
    dimension=i_minus_one,
  )

  gamma = HomotopyElement(
    name="γ",
    dimension=i,
  )

  formula = Sum(
    left=Suspension(
      expression=beta,
    ),
    right=Composition(
      left=alpha,
      right=gamma,
    ),
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=source_group,
      target_group=target_group,
      alpha=alpha,
      beta=beta,
      gamma=gamma,
      formula=formula,
    )
  )

  suspension_map = TodaSuspensionMap(
    source_group=first_summand,
    target_group=target_group,
  )

  return {
    "i": i,
    "n": n,
    "i_minus_one": i_minus_one,
    "n_minus_one": n_minus_one,
    "two_n_minus_one": (
      two_n_minus_one
    ),
    "first_summand": first_summand,
    "second_summand": second_summand,
    "source_group": source_group,
    "target_group": target_group,
    "alpha": alpha,
    "beta": beta,
    "gamma": gamma,
    "formula": formula,
    "decomposition_map": (
      decomposition_map
    ),
    "suspension_map": suspension_map,
  }


def build_phase48_3_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase48_3_statement_decomposition_map_type():
  type_hints = get_type_hints(
    TodaProp44FirstSummandRestrictionStatement
  )

  assert type_hints[
    "decomposition_map"
  ] is TodaProp44DecompositionMap


def test_phase48_3_statement_suspension_map_type():
  type_hints = get_type_hints(
    TodaProp44FirstSummandRestrictionStatement
  )

  assert type_hints[
    "suspension_map"
  ] is TodaSuspensionMap


def test_phase48_3_statement_preserves_decomposition_map():
  data = build_phase48_3_data()

  statement = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=data[
        "decomposition_map"
      ],
      suspension_map=data[
        "suspension_map"
      ],
    )
  )

  assert statement.decomposition_map == (
    data[
      "decomposition_map"
    ]
  )


def test_phase48_3_statement_preserves_suspension_map():
  data = build_phase48_3_data()

  statement = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=data[
        "decomposition_map"
      ],
      suspension_map=data[
        "suspension_map"
      ],
    )
  )

  assert statement.suspension_map == (
    data[
      "suspension_map"
    ]
  )


def test_phase48_3_different_i_instances_are_distinct():
  first = build_phase48_3_data(
    i_name="i",
  )

  second = build_phase48_3_data(
    i_name="j",
  )

  first_statement = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=first[
        "decomposition_map"
      ],
      suspension_map=first[
        "suspension_map"
      ],
    )
  )

  second_statement = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=second[
        "decomposition_map"
      ],
      suspension_map=second[
        "suspension_map"
      ],
    )
  )

  assert (
    first_statement
    != second_statement
  )


def test_phase48_3_different_n_instances_are_distinct():
  first = build_phase48_3_data(
    n_name="n",
  )

  second = build_phase48_3_data(
    n_name="m",
  )

  first_statement = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=first[
        "decomposition_map"
      ],
      suspension_map=first[
        "suspension_map"
      ],
    )
  )

  second_statement = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=second[
        "decomposition_map"
      ],
      suspension_map=second[
        "suspension_map"
      ],
    )
  )

  assert (
    first_statement
    != second_statement
  )


def test_phase48_3_rule_requires_map_and_suspension_map():
  rule = (
    toda_prop44_first_summand_restriction_inference_rule()
  )

  assert len(
    rule.premise_patterns
  ) == 2

  assert (
    rule.premise_patterns[
      0
    ].statement_type
    is TodaProp44DecompositionMap
  )

  assert (
    rule.premise_patterns[
      1
    ].statement_type
    is TodaSuspensionMap
  )


def test_phase48_3_rule_matches_valid_instance():
  data = build_phase48_3_data()

  assert find_inference_match(
    toda_prop44_first_summand_restriction_inference_rule(),
    build_phase48_3_steps(
      data
    ),
  ) is not None


def test_phase48_3_rule_derives_restriction_statement():
  data = build_phase48_3_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_first_summand_restriction_inference_rule(),
      build_phase48_3_steps(
        data
      ),
    )
  )

  expected = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=data[
        "decomposition_map"
      ],
      suspension_map=data[
        "suspension_map"
      ],
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase48_3_valid_instance_derives_exactly_one_statement():
  data = build_phase48_3_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_first_summand_restriction_inference_rule(),
      build_phase48_3_steps(
        data
      ),
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44FirstSummandRestrictionStatement,
    )
  )

  assert len(
    derived
  ) == 1


def test_phase48_3_derived_statement_preserves_provenance():
  data = build_phase48_3_data()

  steps = build_phase48_3_steps(
    data
  )

  rule = (
    toda_prop44_first_summand_restriction_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      steps,
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaProp44FirstSummandRestrictionStatement,
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )

  assert derived.premises == steps

  assert derived.inference_rule == (
    rule
  )


def test_phase48_3_valid_instance_reaches_fixed_point_in_one_round():
  data = build_phase48_3_data()

  result = (
    run_inference_until_stable_with_history(
      toda_prop44_first_summand_restriction_inference_rule(),
      build_phase48_3_steps(
        data
      ),
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert len(
    result.round_results[
      0
    ].new_steps
  ) == 1


def test_phase48_3_rule_rejects_missing_decomposition_map():
  data = build_phase48_3_data()

  steps = build_phase48_3_steps(
    data
  )

  assert find_inference_match(
    toda_prop44_first_summand_restriction_inference_rule(),
    (
      steps[
        1
      ],
    ),
  ) is None


def test_phase48_3_rule_rejects_missing_suspension_map():
  data = build_phase48_3_data()

  steps = build_phase48_3_steps(
    data
  )

  assert find_inference_match(
    toda_prop44_first_summand_restriction_inference_rule(),
    (
      steps[
        0
      ],
    ),
  ) is None


def test_phase48_3_rule_rejects_wrong_suspension_source():
  data = build_phase48_3_data()

  wrong_suspension = TodaSuspensionMap(
    source_group=data[
      "second_summand"
    ],
    target_group=data[
      "target_group"
    ],
  )

  steps = (
    ProofStep(
      conclusion=data[
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_suspension,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_first_summand_restriction_inference_rule(),
    steps,
  ) is None


def test_phase48_3_rule_rejects_wrong_suspension_target():
  data = build_phase48_3_data()

  wrong_target = TodaPrimaryGroup(
    group_dimension=ScalarSymbol(
      name="j",
    ),
    sphere_dimension=data[
      "n"
    ],
  )

  wrong_suspension = TodaSuspensionMap(
    source_group=data[
      "first_summand"
    ],
    target_group=wrong_target,
  )

  steps = (
    ProofStep(
      conclusion=data[
        "decomposition_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_suspension,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_first_summand_restriction_inference_rule(),
    steps,
  ) is None


def test_phase48_3_rule_rejects_reversed_source_summands():
  data = build_phase48_3_data()

  wrong_map = (
    TodaProp44DecompositionMap(
      source_group=DirectSumGroup(
        summands=(
          data[
            "second_summand"
          ],
          data[
            "first_summand"
          ],
        ),
      ),
      target_group=data[
        "target_group"
      ],
      alpha=data[
        "alpha"
      ],
      beta=data[
        "beta"
      ],
      gamma=data[
        "gamma"
      ],
      formula=data[
        "formula"
      ],
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_first_summand_restriction_inference_rule(),
    steps,
  ) is None


def test_phase48_3_rule_rejects_wrong_formula():
  data = build_phase48_3_data()

  wrong_formula = HomotopyElement(
    name="δ",
    dimension=data[
      "i"
    ],
  )

  wrong_map = (
    TodaProp44DecompositionMap(
      source_group=data[
        "source_group"
      ],
      target_group=data[
        "target_group"
      ],
      alpha=data[
        "alpha"
      ],
      beta=data[
        "beta"
      ],
      gamma=data[
        "gamma"
      ],
      formula=wrong_formula,
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_first_summand_restriction_inference_rule(),
    steps,
  ) is None


def test_phase48_3_rule_rejects_partial_formula():
  data = build_phase48_3_data()

  wrong_map = (
    TodaProp44DecompositionMap(
      source_group=data[
        "source_group"
      ],
      target_group=data[
        "target_group"
      ],
      alpha=data[
        "alpha"
      ],
      beta=data[
        "beta"
      ],
      gamma=data[
        "gamma"
      ],
      formula=Suspension(
        expression=data[
          "beta"
        ],
      ),
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_prop44_first_summand_restriction_inference_rule(),
    steps,
  ) is None


def test_phase48_3_statement_does_not_assert_injectivity():
  data = build_phase48_3_data()

  statement = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=data[
        "decomposition_map"
      ],
      suspension_map=data[
        "suspension_map"
      ],
    )
  )

  assert not isinstance(
    statement,
    InjectiveMapStatement,
  )

  assert not hasattr(
    statement,
    "injective",
  )

  assert not hasattr(
    statement,
    "is_injective",
  )


def test_phase48_3_statement_does_not_assert_isomorphism():
  data = build_phase48_3_data()

  statement = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=data[
        "decomposition_map"
      ],
      suspension_map=data[
        "suspension_map"
      ],
    )
  )

  assert not hasattr(
    statement,
    "isomorphism",
  )

  assert not hasattr(
    statement,
    "is_isomorphism",
  )


def test_phase48_3_does_not_introduce_general_inclusion_map():
  data = build_phase48_3_data()

  statement = (
    TodaProp44FirstSummandRestrictionStatement(
      decomposition_map=data[
        "decomposition_map"
      ],
      suspension_map=data[
        "suspension_map"
      ],
    )
  )

  assert not hasattr(
    statement,
    "inclusion_map",
  )

  assert not hasattr(
    statement,
    "embedding_map",
  )

  assert not hasattr(
    statement,
    "projection_map",
  )



