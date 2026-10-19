from typing import (
  get_type_hints,
)

from homotopy_groups import (
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
)
from low_dimensional_facts import (
  e_pi_1_1_to_pi_2_2_isomorphism_fact,
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
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaDeltaZeroStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
  toda_exactness_injective_right_implies_delta_zero_inference_rule,
  toda_exactness_zero_delta_implies_hopf_surjective_inference_rule,
  toda_suspension_isomorphism_implies_injective_inference_rule,
)


def build_phase49_4_data():
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi_3_3 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )

  pi_1_1 = TodaPrimaryGroup(
    group_dimension=1,
    sphere_dimension=1,
  )

  pi_2_2 = TodaPrimaryGroup(
    group_dimension=2,
    sphere_dimension=2,
  )

  suspension_map = TodaSuspensionMap(
    source_group=pi_1_1,
    target_group=pi_2_2,
  )

  suspension_isomorphism = (
    e_pi_1_1_to_pi_2_2_isomorphism_fact()
  )

  suspension_injectivity = (
    TodaSuspensionInjectiveStatement(
      map=suspension_map,
    )
  )

  delta_e_window = (
    TodaEHPExactnessWindow(
      source_term=pi_3_3,
      middle_term=pi_1_1,
      target_term=pi_2_2,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    )
  )

  delta_e_exactness = (
    TodaProp42ExactnessStatement(
      window=delta_e_window,
    )
  )

  delta_map = TodaDeltaMap(
    source_group=pi_3_3,
    target_group=pi_1_1,
  )

  delta_zero = TodaDeltaZeroStatement(
    map=delta_map,
  )

  h_delta_window = (
    TodaEHPExactnessWindow(
      source_term=pi_3_2,
      middle_term=pi_3_3,
      target_term=pi_1_1,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    )
  )

  h_delta_exactness = (
    TodaProp42ExactnessStatement(
      window=h_delta_window,
    )
  )

  hopf_map = TodaHopfInvariantMap(
    source_group=pi_3_2,
    target_group=pi_3_3,
  )

  hopf_surjectivity = (
    TodaHopfInvariantSurjectiveStatement(
      map=hopf_map,
    )
  )

  return {
    "pi_3_2": pi_3_2,
    "pi_3_3": pi_3_3,
    "pi_1_1": pi_1_1,
    "pi_2_2": pi_2_2,
    "suspension_map": suspension_map,
    "suspension_isomorphism": (
      suspension_isomorphism
    ),
    "suspension_injectivity": (
      suspension_injectivity
    ),
    "delta_e_window": delta_e_window,
    "delta_e_exactness": (
      delta_e_exactness
    ),
    "delta_map": delta_map,
    "delta_zero": delta_zero,
    "h_delta_window": h_delta_window,
    "h_delta_exactness": (
      h_delta_exactness
    ),
    "hopf_map": hopf_map,
    "hopf_surjectivity": (
      hopf_surjectivity
    ),
  }


def build_phase49_4_initial_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "suspension_isomorphism"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_e_exactness"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "h_delta_exactness"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def build_phase49_4_rules():
  return (
    toda_suspension_isomorphism_implies_injective_inference_rule(),
    toda_exactness_injective_right_implies_delta_zero_inference_rule(),
    toda_exactness_zero_delta_implies_hopf_surjective_inference_rule(),
  )


def test_phase49_4_delta_map_source_type():
  type_hints = get_type_hints(
    TodaDeltaMap
  )

  assert type_hints[
    "source_group"
  ] is TodaPrimaryGroup


def test_phase49_4_delta_map_target_type():
  type_hints = get_type_hints(
    TodaDeltaMap
  )

  assert type_hints[
    "target_group"
  ] is TodaPrimaryGroup


def test_phase49_4_delta_map_preserves_specific_instance():
  data = build_phase49_4_data()

  assert data[
    "delta_map"
  ] == TodaDeltaMap(
    source_group=data[
      "pi_3_3"
    ],
    target_group=data[
      "pi_1_1"
    ],
  )


def test_phase49_4_suspension_injective_statement_uses_specific_map():
  type_hints = get_type_hints(
    TodaSuspensionInjectiveStatement
  )

  assert type_hints[
    "map"
  ] is TodaSuspensionMap


def test_phase49_4_delta_zero_statement_uses_specific_map():
  type_hints = get_type_hints(
    TodaDeltaZeroStatement
  )

  assert type_hints[
    "map"
  ] is TodaDeltaMap


def test_phase49_4_hopf_surjective_statement_uses_specific_map():
  type_hints = get_type_hints(
    TodaHopfInvariantSurjectiveStatement
  )

  assert type_hints[
    "map"
  ] is TodaHopfInvariantMap


def test_phase49_4_suspension_isomorphism_rule_matches():
  data = build_phase49_4_data()

  step = ProofStep(
    conclusion=data[
      "suspension_isomorphism"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_suspension_isomorphism_implies_injective_inference_rule(),
    (
      step,
    ),
  ) is not None


def test_phase49_4_suspension_isomorphism_derives_injectivity():
  data = build_phase49_4_data()

  step = ProofStep(
    conclusion=data[
      "suspension_isomorphism"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      toda_suspension_isomorphism_implies_injective_inference_rule(),
      (
        step,
      ),
    )
  )

  conclusions = tuple(
    derived.conclusion
    for derived in result.steps
  )

  assert data[
    "suspension_injectivity"
  ] in conclusions


def test_phase49_4_delta_zero_rule_matches_valid_instance():
  data = build_phase49_4_data()

  steps = (
    ProofStep(
      conclusion=data[
        "suspension_injectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_e_exactness"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_exactness_injective_right_implies_delta_zero_inference_rule(),
    steps,
  ) is not None


def test_phase49_4_delta_zero_rule_derives_expected_delta_zero():
  data = build_phase49_4_data()

  steps = (
    ProofStep(
      conclusion=data[
        "suspension_injectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_e_exactness"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  result = (
    run_inference_until_stable_with_history(
      toda_exactness_injective_right_implies_delta_zero_inference_rule(),
      steps,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "delta_zero"
  ] in conclusions


def test_phase49_4_delta_zero_rule_rejects_wrong_e_instance():
  data = build_phase49_4_data()

  wrong_injectivity = (
    TodaSuspensionInjectiveStatement(
      map=TodaSuspensionMap(
        source_group=data[
          "pi_2_2"
        ],
        target_group=data[
          "pi_3_3"
        ],
      ),
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_injectivity,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_e_exactness"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_exactness_injective_right_implies_delta_zero_inference_rule(),
    steps,
  ) is None


def test_phase49_4_delta_zero_rule_rejects_wrong_map_order():
  data = build_phase49_4_data()

  wrong_window = (
    TodaEHPExactnessWindow(
      source_term=data[
        "pi_3_3"
      ],
      middle_term=data[
        "pi_1_1"
      ],
      target_term=data[
        "pi_2_2"
      ],
      first_map=EHP_H_MAP,
      second_map=EHP_E_MAP,
    )
  )

  wrong_exactness = (
    TodaProp42ExactnessStatement(
      window=wrong_window,
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "suspension_injectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_exactness,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_exactness_injective_right_implies_delta_zero_inference_rule(),
    steps,
  ) is None


def test_phase49_4_hopf_surjectivity_rule_matches_valid_instance():
  data = build_phase49_4_data()

  steps = (
    ProofStep(
      conclusion=data[
        "delta_zero"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "h_delta_exactness"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_exactness_zero_delta_implies_hopf_surjective_inference_rule(),
    steps,
  ) is not None


def test_phase49_4_hopf_surjectivity_rule_derives_expected_result():
  data = build_phase49_4_data()

  steps = (
    ProofStep(
      conclusion=data[
        "delta_zero"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "h_delta_exactness"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  result = (
    run_inference_until_stable_with_history(
      toda_exactness_zero_delta_implies_hopf_surjective_inference_rule(),
      steps,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "hopf_surjectivity"
  ] in conclusions


def test_phase49_4_hopf_surjectivity_rejects_wrong_delta_instance():
  data = build_phase49_4_data()

  wrong_delta_zero = (
    TodaDeltaZeroStatement(
      map=TodaDeltaMap(
        source_group=data[
          "pi_1_1"
        ],
        target_group=data[
          "pi_2_2"
        ],
      ),
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_delta_zero,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "h_delta_exactness"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_exactness_zero_delta_implies_hopf_surjective_inference_rule(),
    steps,
  ) is None


def test_phase49_4_hopf_surjectivity_rejects_wrong_map_order():
  data = build_phase49_4_data()

  wrong_window = (
    TodaEHPExactnessWindow(
      source_term=data[
        "pi_3_2"
      ],
      middle_term=data[
        "pi_3_3"
      ],
      target_term=data[
        "pi_1_1"
      ],
      first_map=EHP_E_MAP,
      second_map=EHP_DELTA_MAP,
    )
  )

  wrong_exactness = (
    TodaProp42ExactnessStatement(
      window=wrong_window,
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "delta_zero"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_exactness,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_exactness_zero_delta_implies_hopf_surjective_inference_rule(),
    steps,
  ) is None


def test_phase49_4_end_to_end_derives_e_injectivity():
  data = build_phase49_4_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_4_rules(),
      build_phase49_4_initial_steps(
        data
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "suspension_injectivity"
  ] in conclusions


def test_phase49_4_end_to_end_derives_delta_zero():
  data = build_phase49_4_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_4_rules(),
      build_phase49_4_initial_steps(
        data
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "delta_zero"
  ] in conclusions


def test_phase49_4_end_to_end_derives_h_surjectivity():
  data = build_phase49_4_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_4_rules(),
      build_phase49_4_initial_steps(
        data
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "hopf_surjectivity"
  ] in conclusions


def test_phase49_4_end_to_end_reaches_fixed_point_in_three_rounds():
  data = build_phase49_4_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_4_rules(),
      build_phase49_4_initial_steps(
        data
      ),
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3


def test_phase49_4_round_one_derives_only_e_injectivity():
  data = build_phase49_4_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_4_rules(),
      build_phase49_4_initial_steps(
        data
      ),
    )
  )

  new_steps = (
    result.round_results[
      0
    ].new_steps
  )

  assert len(
    new_steps
  ) == 1

  assert isinstance(
    new_steps[
      0
    ].conclusion,
    TodaSuspensionInjectiveStatement,
  )


def test_phase49_4_round_two_derives_only_delta_zero():
  data = build_phase49_4_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_4_rules(),
      build_phase49_4_initial_steps(
        data
      ),
    )
  )

  new_steps = (
    result.round_results[
      1
    ].new_steps
  )

  assert len(
    new_steps
  ) == 1

  assert isinstance(
    new_steps[
      0
    ].conclusion,
    TodaDeltaZeroStatement,
  )


def test_phase49_4_round_three_derives_only_h_surjectivity():
  data = build_phase49_4_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_4_rules(),
      build_phase49_4_initial_steps(
        data
      ),
    )
  )

  new_steps = (
    result.round_results[
      2
    ].new_steps
  )

  assert len(
    new_steps
  ) == 1

  assert isinstance(
    new_steps[
      0
    ].conclusion,
    TodaHopfInvariantSurjectiveStatement,
  )


def test_phase49_4_h_surjectivity_preserves_specific_source_and_target():
  data = build_phase49_4_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_4_rules(),
      build_phase49_4_initial_steps(
        data
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaHopfInvariantSurjectiveStatement,
    )
  )

  assert derived.conclusion.map.source_group == (
    data[
      "pi_3_2"
    ]
  )

  assert derived.conclusion.map.target_group == (
    data[
      "pi_3_3"
    ]
  )


def test_phase49_4_all_derived_steps_preserve_inference_provenance():
  data = build_phase49_4_data()

  result = (
    run_inference_until_stable_with_history(
      build_phase49_4_rules(),
      build_phase49_4_initial_steps(
        data
      ),
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if step.rule
    == ProofRule.INFERENCE
  )

  assert len(
    derived
  ) == 3

  assert all(
    step.inference_rule
    is not None
    for step in derived
  )


def test_phase49_4_original_isomorphism_fact_is_instance_aware():
  fact = (
    e_pi_1_1_to_pi_2_2_isomorphism_fact()
  )

  assert isinstance(
    fact,
    TodaSuspensionIsomorphismStatement,
  )

  assert fact.map.source_group == (
    TodaPrimaryGroup(
      group_dimension=1,
      sphere_dimension=1,
    )
  )

  assert fact.map.target_group == (
    TodaPrimaryGroup(
      group_dimension=2,
      sphere_dimension=2,
    )
  )


