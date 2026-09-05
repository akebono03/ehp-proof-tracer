from expression import (
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
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
from toda_rules import (
  Toda45IsomorphismStatement,
  toda_45_isomorphism_inference_rule,
)


def build_phase46_4_data():
  n = ScalarSymbol(
    name="n",
  )

  k = ScalarSymbol(
    name="k",
  )

  m = ScalarSymbol(
    name="m",
  )

  stable_range = ScalarGreaterEqualStatement(
    left=n,
    right=ScalarSum(
      left=k,
      right=2,
    ),
  )

  suspension_range = ScalarGreaterEqualStatement(
    left=m,
    right=n,
  )

  suspension_map = TodaIteratedSuspensionMap(
    exponent=ScalarSum(
      left=m,
      right=ScalarProduct(
        left=-1,
        right=n,
      ),
    ),
    source_group=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=k,
      ),
      sphere_dimension=n,
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=m,
        right=k,
      ),
      sphere_dimension=m,
    ),
  )

  return {
    "n": n,
    "k": k,
    "m": m,
    "stable_range": stable_range,
    "suspension_range": suspension_range,
    "suspension_map": suspension_map,
  }


def build_phase46_4_steps():
  data = build_phase46_4_data()

  return (
    ProofStep(
      conclusion=data[
        "stable_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_range"
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


def test_phase46_4_statement_preserves_specific_map_instance():
  data = build_phase46_4_data()

  statement = Toda45IsomorphismStatement(
    map=data[
      "suspension_map"
    ],
  )

  assert statement.map == (
    data[
      "suspension_map"
    ]
  )


def test_phase46_4_statement_is_instance_aware():
  data = build_phase46_4_data()

  first = Toda45IsomorphismStatement(
    map=data[
      "suspension_map"
    ],
  )

  second = Toda45IsomorphismStatement(
    map=TodaIteratedSuspensionMap(
      exponent=1,
      source_group=(
        data[
          "suspension_map"
        ].source_group
      ),
      target_group=(
        data[
          "suspension_map"
        ].target_group
      ),
    ),
  )

  assert first != second


def test_phase46_4_rule_requires_two_range_premises_and_map():
  rule = (
    toda_45_isomorphism_inference_rule()
  )

  assert len(
    rule.premise_patterns
  ) == 3

  assert (
    rule.premise_patterns[
      0
    ].statement_type
    is ScalarGreaterEqualStatement
  )

  assert (
    rule.premise_patterns[
      1
    ].statement_type
    is ScalarGreaterEqualStatement
  )

  assert (
    rule.premise_patterns[
      2
    ].statement_type
    is TodaIteratedSuspensionMap
  )


def test_phase46_4_rule_matches_valid_toda_45_instance():
  steps = build_phase46_4_steps()

  rule = (
    toda_45_isomorphism_inference_rule()
  )

  match = find_inference_match(
    rule,
    steps,
  )

  assert match is not None

  assert match.premises == steps


def test_phase46_4_rule_derives_instance_aware_isomorphism():
  steps = build_phase46_4_steps()

  rule = (
    toda_45_isomorphism_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      steps,
    )
  )

  expected = Toda45IsomorphismStatement(
    map=steps[
      2
    ].conclusion,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase46_4_derived_step_preserves_all_three_premises():
  steps = build_phase46_4_steps()

  rule = (
    toda_45_isomorphism_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      steps,
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      Toda45IsomorphismStatement,
    )
  )

  assert len(
    derived
  ) == 1

  assert derived[
    0
  ].premises == steps

  assert (
    derived[
      0
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    derived[
      0
    ].inference_rule
    == rule
  )


def test_phase46_4_valid_instance_reaches_fixed_point_in_one_round():
  steps = build_phase46_4_steps()

  result = (
    run_inference_until_stable_with_history(
      toda_45_isomorphism_inference_rule(),
      steps,
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


def test_phase46_4_rule_rejects_wrong_stable_range_premise():
  data = build_phase46_4_data()

  steps = (
    ProofStep(
      conclusion=ScalarGreaterEqualStatement(
        left=data[
          "n"
        ],
        right=ScalarSum(
          left=data[
            "k"
          ],
          right=3,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_range"
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

  assert find_inference_match(
    toda_45_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase46_4_rule_rejects_wrong_m_greater_equal_n_premise():
  data = build_phase46_4_data()

  steps = (
    ProofStep(
      conclusion=data[
        "stable_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=ScalarGreaterEqualStatement(
        left=data[
          "n"
        ],
        right=data[
          "m"
        ],
      ),
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
    toda_45_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase46_4_rule_rejects_wrong_source_group_shape():
  data = build_phase46_4_data()

  wrong_map = TodaIteratedSuspensionMap(
    exponent=data[
      "suspension_map"
    ].exponent,
    source_group=TodaPrimaryGroup(
      group_dimension=data[
        "n"
      ],
      sphere_dimension=data[
        "n"
      ],
    ),
    target_group=(
      data[
        "suspension_map"
      ].target_group
    ),
  )

  steps = (
    ProofStep(
      conclusion=data[
        "stable_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_45_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase46_4_rule_rejects_wrong_target_group_shape():
  data = build_phase46_4_data()

  wrong_map = TodaIteratedSuspensionMap(
    exponent=data[
      "suspension_map"
    ].exponent,
    source_group=(
      data[
        "suspension_map"
      ].source_group
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=data[
        "m"
      ],
      sphere_dimension=data[
        "m"
      ],
    ),
  )

  steps = (
    ProofStep(
      conclusion=data[
        "stable_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_45_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase46_4_rule_rejects_wrong_exponent():
  data = build_phase46_4_data()

  wrong_map = TodaIteratedSuspensionMap(
    exponent=ScalarSum(
      left=data[
        "m"
      ],
      right=-1,
    ),
    source_group=(
      data[
        "suspension_map"
      ].source_group
    ),
    target_group=(
      data[
        "suspension_map"
      ].target_group
    ),
  )

  steps = (
    ProofStep(
      conclusion=data[
        "stable_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_map,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_45_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase46_4_rule_does_not_evaluate_numeric_inequalities():
  n = 3
  k = 2
  m = 2

  steps = (
    ProofStep(
      conclusion=ScalarGreaterEqualStatement(
        left=n,
        right=ScalarSum(
          left=k,
          right=2,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=ScalarGreaterEqualStatement(
        left=m,
        right=n,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=TodaIteratedSuspensionMap(
        exponent=ScalarSum(
          left=m,
          right=ScalarProduct(
            left=-1,
            right=n,
          ),
        ),
        source_group=TodaPrimaryGroup(
          group_dimension=ScalarSum(
            left=n,
            right=k,
          ),
          sphere_dimension=n,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=ScalarSum(
            left=m,
            right=k,
          ),
          sphere_dimension=m,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  match = find_inference_match(
    toda_45_isomorphism_inference_rule(),
    steps,
  )

  assert match is not None


def test_phase46_4_statement_does_not_project_to_generic_isomorphism_yet():
  data = build_phase46_4_data()

  statement = Toda45IsomorphismStatement(
    map=data[
      "suspension_map"
    ],
  )

  assert not hasattr(
    statement,
    "generic_isomorphism",
  )

  assert not hasattr(
    statement,
    "isomorphism_statement",
  )
