from expression import (
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaEHPExactnessWindow,
  TodaEHPSequence,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_applicable_inference_rules,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
  toda_prop42_delta_e_exactness_inference_rule,
  toda_prop42_e_h_exactness_inference_rule,
  toda_prop42_h_delta_exactness_inference_rule,
)


def build_phase45_5_symbolic_sequence(
  i,
  n,
):
  i_plus_one = ScalarSum(
    left=i,
    right=1,
  )

  i_minus_one = ScalarSum(
    left=i,
    right=-1,
  )

  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )

  two_n_plus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=1,
  )

  return TodaEHPSequence(
    terms=(
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=n,
      ),
      TodaPrimaryGroup(
        group_dimension=i_plus_one,
        sphere_dimension=n_plus_one,
      ),
      TodaPrimaryGroup(
        group_dimension=i_plus_one,
        sphere_dimension=two_n_plus_one,
      ),
      TodaPrimaryGroup(
        group_dimension=i_minus_one,
        sphere_dimension=n,
      ),
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=n_plus_one,
      ),
    ),
    maps=(
      EHP_E_MAP,
      EHP_H_MAP,
      EHP_DELTA_MAP,
      EHP_E_MAP,
    ),
  )


def build_phase45_5_windows(
  i,
  n,
):
  sequence = (
    build_phase45_5_symbolic_sequence(
      i,
      n,
    )
  )

  return (
    TodaEHPExactnessWindow(
      source_term=sequence.terms[
        0
      ],
      middle_term=sequence.terms[
        1
      ],
      target_term=sequence.terms[
        2
      ],
      first_map=sequence.maps[
        0
      ],
      second_map=sequence.maps[
        1
      ],
    ),
    TodaEHPExactnessWindow(
      source_term=sequence.terms[
        1
      ],
      middle_term=sequence.terms[
        2
      ],
      target_term=sequence.terms[
        3
      ],
      first_map=sequence.maps[
        1
      ],
      second_map=sequence.maps[
        2
      ],
    ),
    TodaEHPExactnessWindow(
      source_term=sequence.terms[
        2
      ],
      middle_term=sequence.terms[
        3
      ],
      target_term=sequence.terms[
        4
      ],
      first_map=sequence.maps[
        2
      ],
      second_map=sequence.maps[
        3
      ],
    ),
  )


def build_phase45_5_window_steps(
  i,
  n,
):
  windows = (
    build_phase45_5_windows(
      i,
      n,
    )
  )

  return tuple(
    ProofStep(
      conclusion=window,
      premises=(),
      rule=ProofRule.GIVEN,
    )
    for window in windows
  )


def test_phase45_5_e_h_rule_matches_first_prop42_window():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  first_step = (
    build_phase45_5_window_steps(
      i,
      n,
    )[
      0
    ]
  )

  rule = (
    toda_prop42_e_h_exactness_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_step,
    ),
  )

  assert match is not None

  assert match.premises == (
    first_step,
  )


def test_phase45_5_e_h_rule_derives_exactness_statement():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  first_step = (
    build_phase45_5_window_steps(
      i,
      n,
    )[
      0
    ]
  )

  rule = (
    toda_prop42_e_h_exactness_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        first_step,
      ),
    )
  )

  expected = (
    TodaProp42ExactnessStatement(
      window=first_step.conclusion,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase45_5_h_delta_rule_matches_second_prop42_window():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  second_step = (
    build_phase45_5_window_steps(
      i,
      n,
    )[
      1
    ]
  )

  rule = (
    toda_prop42_h_delta_exactness_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      second_step,
    ),
  )

  assert match is not None

  assert match.premises == (
    second_step,
  )


def test_phase45_5_h_delta_rule_derives_exactness_statement():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  second_step = (
    build_phase45_5_window_steps(
      i,
      n,
    )[
      1
    ]
  )

  rule = (
    toda_prop42_h_delta_exactness_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        second_step,
      ),
    )
  )

  expected = (
    TodaProp42ExactnessStatement(
      window=second_step.conclusion,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase45_5_delta_e_rule_matches_third_prop42_window():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  third_step = (
    build_phase45_5_window_steps(
      i,
      n,
    )[
      2
    ]
  )

  rule = (
    toda_prop42_delta_e_exactness_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      third_step,
    ),
  )

  assert match is not None

  assert match.premises == (
    third_step,
  )


def test_phase45_5_delta_e_rule_derives_exactness_statement():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  third_step = (
    build_phase45_5_window_steps(
      i,
      n,
    )[
      2
    ]
  )

  rule = (
    toda_prop42_delta_e_exactness_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        third_step,
      ),
    )
  )

  expected = (
    TodaProp42ExactnessStatement(
      window=third_step.conclusion,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase45_5_each_window_has_exactly_one_applicable_rule():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  steps = (
    build_phase45_5_window_steps(
      i,
      n,
    )
  )

  rules = (
    toda_prop42_e_h_exactness_inference_rule(),
    toda_prop42_h_delta_exactness_inference_rule(),
    toda_prop42_delta_e_exactness_inference_rule(),
  )

  expected_names = (
    "Toda Proposition 4.2 E-H exactness",
    (
      "Toda Proposition 4.2 "
      "H-Delta exactness"
    ),
    (
      "Toda Proposition 4.2 "
      "Delta-E exactness"
    ),
  )

  for step, expected_name in zip(
    steps,
    expected_names,
  ):
    applicable = tuple(
      rule
      for rule in rules
      if find_inference_match(
        rule,
        (
          step,
        ),
      )
      is not None
    )

    assert len(
      applicable
    ) == 1

    assert (
      applicable[
        0
      ].name
      == expected_name
    )


def test_phase45_5_all_three_windows_derive_three_exactness_statements():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  steps = (
    build_phase45_5_window_steps(
      i,
      n,
    )
  )

  rules = (
    toda_prop42_e_h_exactness_inference_rule(),
    toda_prop42_h_delta_exactness_inference_rule(),
    toda_prop42_delta_e_exactness_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      steps,
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        TodaProp42ExactnessStatement,
      )
    )
  )

  assert len(
    derived
  ) == 3

  assert tuple(
    step.conclusion.window
    for step in derived
  ) == tuple(
    step.conclusion
    for step in steps
  )


def test_phase45_5_all_three_theorem_results_preserve_provenance():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  premise_steps = (
    build_phase45_5_window_steps(
      i,
      n,
    )
  )

  rules = (
    toda_prop42_e_h_exactness_inference_rule(),
    toda_prop42_h_delta_exactness_inference_rule(),
    toda_prop42_delta_e_exactness_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  derived_steps = tuple(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        TodaProp42ExactnessStatement,
      )
    )
  )

  for premise_step, derived_step in zip(
    premise_steps,
    derived_steps,
  ):
    assert derived_step.premises == (
      premise_step,
    )

    assert (
      derived_step.inference_rule
      in rules
    )


def test_phase45_5_three_rules_reach_fixed_point_in_one_round():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  premise_steps = (
    build_phase45_5_window_steps(
      i,
      n,
    )
  )

  rules = (
    toda_prop42_e_h_exactness_inference_rule(),
    toda_prop42_h_delta_exactness_inference_rule(),
    toda_prop42_delta_e_exactness_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    result.round_count
    == 1
  )

  assert len(
    result.round_results[
      0
    ].new_steps
  ) == 3


def test_phase45_5_e_h_rule_rejects_wrong_map_pair():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  window = (
    build_phase45_5_windows(
      i,
      n,
    )[
      0
    ]
  )

  wrong_window = (
    TodaEHPExactnessWindow(
      source_term=window.source_term,
      middle_term=window.middle_term,
      target_term=window.target_term,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    )
  )

  step = ProofStep(
    conclusion=wrong_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_prop42_e_h_exactness_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      step,
    ),
  ) is None


def test_phase45_5_e_h_rule_rejects_wrong_target_dimension():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  window = (
    build_phase45_5_windows(
      i,
      n,
    )[
      0
    ]
  )

  wrong_window = (
    TodaEHPExactnessWindow(
      source_term=window.source_term,
      middle_term=window.middle_term,
      target_term=TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=n,
      ),
      first_map=window.first_map,
      second_map=window.second_map,
    )
  )

  step = ProofStep(
    conclusion=wrong_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_prop42_e_h_exactness_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      step,
    ),
  ) is None


def test_phase45_5_h_delta_rule_rejects_wrong_target_shape():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  window = (
    build_phase45_5_windows(
      i,
      n,
    )[
      1
    ]
  )

  wrong_window = (
    TodaEHPExactnessWindow(
      source_term=window.source_term,
      middle_term=window.middle_term,
      target_term=TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=n,
      ),
      first_map=window.first_map,
      second_map=window.second_map,
    )
  )

  step = ProofStep(
    conclusion=wrong_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_prop42_h_delta_exactness_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      step,
    ),
  ) is None


def test_phase45_5_delta_e_rule_rejects_wrong_middle_dimension():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  window = (
    build_phase45_5_windows(
      i,
      n,
    )[
      2
    ]
  )

  wrong_window = (
    TodaEHPExactnessWindow(
      source_term=window.source_term,
      middle_term=TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=n,
      ),
      target_term=window.target_term,
      first_map=window.first_map,
      second_map=window.second_map,
    )
  )

  step = ProofStep(
    conclusion=wrong_window,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_prop42_delta_e_exactness_inference_rule()
  )

  assert find_inference_match(
    rule,
    (
      step,
    ),
  ) is None


def test_phase45_5_different_symbolic_instances_remain_distinct():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  j = ScalarSymbol(
    name="j",
  )

  m = ScalarSymbol(
    name="m",
  )

  first_window = (
    build_phase45_5_windows(
      i,
      n,
    )[
      0
    ]
  )

  second_window = (
    build_phase45_5_windows(
      j,
      m,
    )[
      0
    ]
  )

  first_statement = (
    TodaProp42ExactnessStatement(
      window=first_window,
    )
  )

  second_statement = (
    TodaProp42ExactnessStatement(
      window=second_window,
    )
  )

  assert (
    first_statement
    != second_statement
  )


def test_phase45_5_theorem_statement_preserves_full_window():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  window = (
    build_phase45_5_windows(
      i,
      n,
    )[
      0
    ]
  )

  statement = (
    TodaProp42ExactnessStatement(
      window=window,
    )
  )

  assert statement.window == window

  assert statement.window.source_term == (
    window.source_term
  )

  assert statement.window.middle_term == (
    window.middle_term
  )

  assert statement.window.target_term == (
    window.target_term
  )

  assert statement.window.first_map == (
    EHP_E_MAP
  )

  assert statement.window.second_map == (
    EHP_H_MAP
  )


