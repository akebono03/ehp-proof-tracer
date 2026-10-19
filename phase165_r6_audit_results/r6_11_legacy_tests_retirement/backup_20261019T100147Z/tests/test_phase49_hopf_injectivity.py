from typing import (
  get_type_hints,
)

from expression import (
  MapSymbol,
)
from homotopy_groups import (
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from low_dimensional_facts import (
  pi_2_1_zero_fact,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
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
  TodaHopfInvariantInjectiveStatement,
  TodaProp42ExactnessStatement,
  toda_exactness_zero_left_implies_hopf_injective_inference_rule,
)


def build_phase49_3_data():
  pi_2_1 = TodaPrimaryGroup(
    group_dimension=2,
    sphere_dimension=1,
  )

  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi_3_3 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )

  window = TodaEHPExactnessWindow(
    source_term=pi_2_1,
    middle_term=pi_3_2,
    target_term=pi_3_3,
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
  )

  exactness = TodaProp42ExactnessStatement(
    window=window,
  )

  zero_statement = (
    pi_2_1_zero_fact()
  )

  hopf_map = TodaHopfInvariantMap(
    source_group=pi_3_2,
    target_group=pi_3_3,
  )

  injectivity = (
    TodaHopfInvariantInjectiveStatement(
      map=hopf_map,
    )
  )

  return {
    "pi_2_1": pi_2_1,
    "pi_3_2": pi_3_2,
    "pi_3_3": pi_3_3,
    "window": window,
    "exactness": exactness,
    "zero_statement": zero_statement,
    "hopf_map": hopf_map,
    "injectivity": injectivity,
  }


def build_phase49_3_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "zero_statement"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "exactness"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase49_3_hopf_map_source_type():
  type_hints = get_type_hints(
    TodaHopfInvariantMap
  )

  assert type_hints[
    "source_group"
  ] is TodaPrimaryGroup


def test_phase49_3_hopf_map_target_type():
  type_hints = get_type_hints(
    TodaHopfInvariantMap
  )

  assert type_hints[
    "target_group"
  ] is TodaPrimaryGroup


def test_phase49_3_hopf_map_preserves_source():
  data = build_phase49_3_data()

  assert data[
    "hopf_map"
  ].source_group == (
    data[
      "pi_3_2"
    ]
  )


def test_phase49_3_hopf_map_preserves_target():
  data = build_phase49_3_data()

  assert data[
    "hopf_map"
  ].target_group == (
    data[
      "pi_3_3"
    ]
  )


def test_phase49_3_hopf_map_is_not_map_symbol():
  data = build_phase49_3_data()

  assert not isinstance(
    data[
      "hopf_map"
    ],
    MapSymbol,
  )


def test_phase49_3_hopf_map_is_not_canonical_h_symbol():
  data = build_phase49_3_data()

  assert (
    data[
      "hopf_map"
    ]
    != EHP_H_MAP
  )


def test_phase49_3_injective_statement_uses_specific_hopf_map():
  type_hints = get_type_hints(
    TodaHopfInvariantInjectiveStatement
  )

  assert type_hints[
    "map"
  ] is TodaHopfInvariantMap


def test_phase49_3_specific_h_injectivity_is_not_generic_injectivity():
  data = build_phase49_3_data()

  generic = InjectiveMapStatement(
    map=EHP_H_MAP,
  )

  assert (
    data[
      "injectivity"
    ]
    != generic
  )


def test_phase49_3_rule_requires_zero_group_and_toda_exactness():
  rule = (
    toda_exactness_zero_left_implies_hopf_injective_inference_rule()
  )

  assert len(
    rule.premise_patterns
  ) == 2

  assert (
    rule.premise_patterns[
      0
    ].statement_type
    is TodaPrimaryGroupZeroStatement
  )

  assert (
    rule.premise_patterns[
      1
    ].statement_type
    is TodaProp42ExactnessStatement
  )


def test_phase49_3_valid_instance_has_inference_match():
  data = build_phase49_3_data()

  match = find_inference_match(
    toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
    build_phase49_3_steps(
      data
    ),
  )

  assert match is not None


def test_phase49_3_valid_instance_derives_h_injectivity():
  data = build_phase49_3_data()

  result = (
    run_inference_until_stable_with_history(
      toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
      build_phase49_3_steps(
        data
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "injectivity"
  ] in conclusions


def test_phase49_3_valid_instance_derives_exactly_one_h_injectivity():
  data = build_phase49_3_data()

  result = (
    run_inference_until_stable_with_history(
      toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
      build_phase49_3_steps(
        data
      ),
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaHopfInvariantInjectiveStatement,
    )
  )

  assert len(
    derived
  ) == 1


def test_phase49_3_derived_h_injectivity_preserves_premises():
  data = build_phase49_3_data()

  steps = build_phase49_3_steps(
    data
  )

  result = (
    run_inference_until_stable_with_history(
      toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
      steps,
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaHopfInvariantInjectiveStatement,
    )
  )

  assert derived.premises == steps


def test_phase49_3_derived_h_injectivity_preserves_proof_rule():
  data = build_phase49_3_data()

  result = (
    run_inference_until_stable_with_history(
      toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
      build_phase49_3_steps(
        data
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaHopfInvariantInjectiveStatement,
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )


def test_phase49_3_valid_instance_reaches_fixed_point_in_one_round():
  data = build_phase49_3_data()

  result = (
    run_inference_until_stable_with_history(
      toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
      build_phase49_3_steps(
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


def test_phase49_3_missing_zero_group_is_rejected():
  data = build_phase49_3_data()

  exactness_step = ProofStep(
    conclusion=data[
      "exactness"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
    (
      exactness_step,
    ),
  ) is None


def test_phase49_3_missing_exactness_is_rejected():
  data = build_phase49_3_data()

  zero_step = ProofStep(
    conclusion=data[
      "zero_statement"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
    (
      zero_step,
    ),
  ) is None


def test_phase49_3_wrong_zero_group_is_rejected():
  data = build_phase49_3_data()

  wrong_zero = (
    TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=1,
        sphere_dimension=1,
      ),
    )
  )

  steps = (
    ProofStep(
      conclusion=wrong_zero,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "exactness"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
    steps,
  ) is None


def test_phase49_3_h_delta_exactness_is_rejected():
  data = build_phase49_3_data()

  wrong_window = (
    TodaEHPExactnessWindow(
      source_term=data[
        "pi_2_1"
      ],
      middle_term=data[
        "pi_3_2"
      ],
      target_term=data[
        "pi_3_3"
      ],
      first_map=EHP_H_MAP,
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
        "zero_statement"
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
    toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
    steps,
  ) is None


def test_phase49_3_cross_instance_zero_group_is_rejected():
  data = build_phase49_3_data()

  other_zero = (
    TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=2,
        sphere_dimension=2,
      ),
    )
  )

  steps = (
    ProofStep(
      conclusion=other_zero,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "exactness"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
    steps,
  ) is None


def test_phase49_3_different_hopf_map_instances_are_distinct():
  first = TodaHopfInvariantMap(
    source_group=TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    ),
  )

  second = TodaHopfInvariantMap(
    source_group=TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=5,
    ),
  )

  assert first != second




