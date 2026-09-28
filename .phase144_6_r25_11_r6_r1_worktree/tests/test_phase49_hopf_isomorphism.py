from typing import (
  get_type_hints,
)

from homotopy_groups import (
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_H_MAP,
)
from map_property_rules import (
  IsomorphismStatement,
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
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  toda_hopf_injective_surjective_implies_isomorphism_inference_rule,
)


def build_phase49_5_data():
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi_3_3 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
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

  surjectivity = (
    TodaHopfInvariantSurjectiveStatement(
      map=hopf_map,
    )
  )

  isomorphism = (
    TodaHopfInvariantIsomorphismStatement(
      map=hopf_map,
    )
  )

  return {
    "pi_3_2": pi_3_2,
    "pi_3_3": pi_3_3,
    "hopf_map": hopf_map,
    "injectivity": injectivity,
    "surjectivity": surjectivity,
    "isomorphism": isomorphism,
  }


def build_phase49_5_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "injectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "surjectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase49_5_isomorphism_statement_uses_specific_hopf_map():
  type_hints = get_type_hints(
    TodaHopfInvariantIsomorphismStatement
  )

  assert type_hints[
    "map"
  ] is TodaHopfInvariantMap


def test_phase49_5_isomorphism_preserves_source_instance():
  data = build_phase49_5_data()

  assert data[
    "isomorphism"
  ].map.source_group == (
    data[
      "pi_3_2"
    ]
  )


def test_phase49_5_isomorphism_preserves_target_instance():
  data = build_phase49_5_data()

  assert data[
    "isomorphism"
  ].map.target_group == (
    data[
      "pi_3_3"
    ]
  )


def test_phase49_5_specific_isomorphism_is_not_generic_isomorphism():
  data = build_phase49_5_data()

  generic = IsomorphismStatement(
    map=EHP_H_MAP,
  )

  assert (
    data[
      "isomorphism"
    ]
    != generic
  )


def test_phase49_5_rule_requires_injectivity_and_surjectivity():
  rule = (
    toda_hopf_injective_surjective_implies_isomorphism_inference_rule()
  )

  assert len(
    rule.premise_patterns
  ) == 2

  assert (
    rule.premise_patterns[
      0
    ].statement_type
    is TodaHopfInvariantInjectiveStatement
  )

  assert (
    rule.premise_patterns[
      1
    ].statement_type
    is TodaHopfInvariantSurjectiveStatement
  )


def test_phase49_5_valid_instance_has_inference_match():
  data = build_phase49_5_data()

  assert find_inference_match(
    toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
    build_phase49_5_steps(
      data
    ),
  ) is not None


def test_phase49_5_valid_instance_derives_isomorphism():
  data = build_phase49_5_data()

  result = (
    run_inference_until_stable_with_history(
      toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
      build_phase49_5_steps(
        data
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert data[
    "isomorphism"
  ] in conclusions


def test_phase49_5_valid_instance_derives_exactly_one_isomorphism():
  data = build_phase49_5_data()

  result = (
    run_inference_until_stable_with_history(
      toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
      build_phase49_5_steps(
        data
      ),
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaHopfInvariantIsomorphismStatement,
    )
  )

  assert len(
    derived
  ) == 1


def test_phase49_5_derived_isomorphism_preserves_both_premises():
  data = build_phase49_5_data()

  steps = build_phase49_5_steps(
    data
  )

  result = (
    run_inference_until_stable_with_history(
      toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
      steps,
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaHopfInvariantIsomorphismStatement,
    )
  )

  assert derived.premises == steps


def test_phase49_5_derived_isomorphism_preserves_proof_rule():
  data = build_phase49_5_data()

  result = (
    run_inference_until_stable_with_history(
      toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
      build_phase49_5_steps(
        data
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaHopfInvariantIsomorphismStatement,
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )


def test_phase49_5_derived_isomorphism_preserves_inference_rule():
  data = build_phase49_5_data()

  rule = (
    toda_hopf_injective_surjective_implies_isomorphism_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      build_phase49_5_steps(
        data
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaHopfInvariantIsomorphismStatement,
    )
  )

  assert derived.inference_rule == (
    rule
  )


def test_phase49_5_valid_instance_reaches_fixed_point_in_one_round():
  data = build_phase49_5_data()

  result = (
    run_inference_until_stable_with_history(
      toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
      build_phase49_5_steps(
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


def test_phase49_5_missing_injectivity_is_rejected():
  data = build_phase49_5_data()

  step = ProofStep(
    conclusion=data[
      "surjectivity"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
    (
      step,
    ),
  ) is None


def test_phase49_5_missing_surjectivity_is_rejected():
  data = build_phase49_5_data()

  step = ProofStep(
    conclusion=data[
      "injectivity"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
    (
      step,
    ),
  ) is None


def test_phase49_5_cross_source_instance_is_rejected():
  data = build_phase49_5_data()

  other_map = TodaHopfInvariantMap(
    source_group=TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    ),
    target_group=data[
      "pi_3_3"
    ],
  )

  other_surjectivity = (
    TodaHopfInvariantSurjectiveStatement(
      map=other_map,
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "injectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=other_surjectivity,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase49_5_cross_target_instance_is_rejected():
  data = build_phase49_5_data()

  other_map = TodaHopfInvariantMap(
    source_group=data[
      "pi_3_2"
    ],
    target_group=TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=5,
    ),
  )

  other_surjectivity = (
    TodaHopfInvariantSurjectiveStatement(
      map=other_map,
    )
  )

  steps = (
    ProofStep(
      conclusion=data[
        "injectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=other_surjectivity,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase49_5_different_hopf_isomorphism_instances_are_distinct():
  first = (
    TodaHopfInvariantIsomorphismStatement(
      map=TodaHopfInvariantMap(
        source_group=TodaPrimaryGroup(
          group_dimension=3,
          sphere_dimension=2,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=3,
          sphere_dimension=3,
        ),
      ),
    )
  )

  second = (
    TodaHopfInvariantIsomorphismStatement(
      map=TodaHopfInvariantMap(
        source_group=TodaPrimaryGroup(
          group_dimension=4,
          sphere_dimension=3,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=4,
          sphere_dimension=5,
        ),
      ),
    )
  )

  assert first != second


