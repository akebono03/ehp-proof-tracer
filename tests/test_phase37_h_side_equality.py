from expression import (
  Composition,
  MapApplication,
  Multiple,
)
from hopf_facts import (
  ETA_2,
  IOTA_3,
)
from map_facts import (
  EHP_H_MAP,
)
from map_property_rules import (
  injective_map_reflects_equality_inference_rule,
)
from probes.probe_phase35_capabilities import (
  build_phase35_end_to_end,
)
from probes.probe_phase36_capabilities import (
  build_phase36_end_to_end,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from relation_rules import (
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
)
from suspension_facts import (
  IOTA_2,
)


def test_phase37_1_phase35_final_step_has_expected_actual_h_equality():
  result = (
    build_phase35_end_to_end()
  )

  final_step = result[
    "final_step"
  ]

  two_iota_2_eta_2 = Composition(
    left=Multiple(
      coefficient=2,
      expression=IOTA_2,
    ),
    right=ETA_2,
  )

  four_iota_3 = Multiple(
    coefficient=4,
    expression=IOTA_3,
  )

  assert isinstance(
    final_step,
    ProofStep,
  )

  assert final_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=two_iota_2_eta_2,
    ),
    rhs=four_iota_3,
    relation_type=RelationType.EQUALITY,
  )


def test_phase37_1_phase36_final_step_has_expected_actual_h_equality():
  result = (
    build_phase36_end_to_end()
  )

  final_step = result[
    "final_step"
  ]

  four_eta_2 = Multiple(
    coefficient=4,
    expression=ETA_2,
  )

  four_iota_3 = Multiple(
    coefficient=4,
    expression=IOTA_3,
  )

  assert isinstance(
    final_step,
    ProofStep,
  )

  assert final_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=four_eta_2,
    ),
    rhs=four_iota_3,
    relation_type=RelationType.EQUALITY,
  )


def test_phase37_1_phase35_and_phase36_final_steps_share_exact_rhs():
  phase35_result = (
    build_phase35_end_to_end()
  )

  phase36_result = (
    build_phase36_end_to_end()
  )

  phase35_step = phase35_result[
    "final_step"
  ]

  phase36_step = phase36_result[
    "final_step"
  ]

  expected_rhs = Multiple(
    coefficient=4,
    expression=IOTA_3,
  )

  assert (
    phase35_step.conclusion.rhs
    == expected_rhs
  )

  assert (
    phase36_step.conclusion.rhs
    == expected_rhs
  )

  assert (
    phase35_step.conclusion.rhs
    == phase36_step.conclusion.rhs
  )


def test_phase37_1_phase35_and_phase36_final_steps_use_same_actual_h_map():
  phase35_result = (
    build_phase35_end_to_end()
  )

  phase36_result = (
    build_phase36_end_to_end()
  )

  phase35_lhs = (
    phase35_result[
      "final_step"
    ].conclusion.lhs
  )

  phase36_lhs = (
    phase36_result[
      "final_step"
    ].conclusion.lhs
  )

  assert isinstance(
    phase35_lhs,
    MapApplication,
  )

  assert isinstance(
    phase36_lhs,
    MapApplication,
  )

  assert phase35_lhs.map is (
    EHP_H_MAP
  )

  assert phase36_lhs.map is (
    EHP_H_MAP
  )

  assert (
    phase35_lhs.expression
    != phase36_lhs.expression
  )


def test_phase37_1_actual_final_steps_do_not_transit_without_symmetry():
  phase35_result = (
    build_phase35_end_to_end()
  )

  phase36_result = (
    build_phase36_end_to_end()
  )

  phase35_step = phase35_result[
    "final_step"
  ]

  phase36_step = phase36_result[
    "final_step"
  ]

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  match = find_inference_match(
    transitivity_rule,
    (
      phase35_step,
      phase36_step,
    ),
  )

  assert match is None


def test_phase37_2_phase36_final_equality_reverses_by_symmetry():
  phase36_result = (
    build_phase36_end_to_end()
  )

  phase36_step = phase36_result[
    "final_step"
  ]

  four_eta_2 = Multiple(
    coefficient=4,
    expression=ETA_2,
  )

  four_iota_3 = Multiple(
    coefficient=4,
    expression=IOTA_3,
  )

  assert phase36_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=four_eta_2,
    ),
    rhs=four_iota_3,
    relation_type=RelationType.EQUALITY,
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  symmetry_match = find_inference_match(
    symmetry_rule,
    (
      phase36_step,
    ),
  )

  assert symmetry_match is not None

  reversed_step = apply_inference_match(
    symmetry_match
  )

  assert reversed_step.conclusion == Relation(
    lhs=four_iota_3,
    rhs=MapApplication(
      map=EHP_H_MAP,
      expression=four_eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert reversed_step.rule == (
    ProofRule.INFERENCE
  )

  assert reversed_step.inference_rule == (
    symmetry_rule
  )

  assert reversed_step.premises == (
    phase36_step,
  )

  assert phase36_step is (
    phase36_result[
      "final_step"
    ]
  )


def test_phase37_3_actual_h_side_equality_closes_by_transitivity():
  phase35_result = (
    build_phase35_end_to_end()
  )

  phase36_result = (
    build_phase36_end_to_end()
  )

  phase35_step = phase35_result[
    "final_step"
  ]

  phase36_step = phase36_result[
    "final_step"
  ]

  four_eta_2 = Multiple(
    coefficient=4,
    expression=ETA_2,
  )

  four_iota_3 = Multiple(
    coefficient=4,
    expression=IOTA_3,
  )

  two_iota_2_eta_2 = Composition(
    left=Multiple(
      coefficient=2,
      expression=IOTA_2,
    ),
    right=ETA_2,
  )

  assert phase35_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=two_iota_2_eta_2,
    ),
    rhs=four_iota_3,
    relation_type=RelationType.EQUALITY,
  )

  assert phase36_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=four_eta_2,
    ),
    rhs=four_iota_3,
    relation_type=RelationType.EQUALITY,
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  symmetry_match = find_inference_match(
    symmetry_rule,
    (
      phase36_step,
    ),
  )

  assert symmetry_match is not None

  reversed_phase36_step = (
    apply_inference_match(
      symmetry_match
    )
  )

  assert reversed_phase36_step.conclusion == Relation(
    lhs=four_iota_3,
    rhs=MapApplication(
      map=EHP_H_MAP,
      expression=four_eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  transitivity_match = find_inference_match(
    transitivity_rule,
    (
      phase35_step,
      reversed_phase36_step,
    ),
  )

  assert transitivity_match is not None

  final_step = apply_inference_match(
    transitivity_match
  )

  assert final_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=two_iota_2_eta_2,
    ),
    rhs=MapApplication(
      map=EHP_H_MAP,
      expression=four_eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert final_step.rule == (
    ProofRule.INFERENCE
  )

  assert final_step.inference_rule == (
    transitivity_rule
  )

  assert final_step.premises == (
    phase35_step,
    reversed_phase36_step,
  )

  assert reversed_phase36_step.premises == (
    phase36_step,
  )


def test_phase37_4_end_to_end_result_preserves_phase35_and_phase36_provenance():
  phase35_result = (
    build_phase35_end_to_end()
  )

  phase36_result = (
    build_phase36_end_to_end()
  )

  phase35_step = phase35_result[
    "final_step"
  ]

  phase36_step = phase36_result[
    "final_step"
  ]

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  symmetry_match = find_inference_match(
    symmetry_rule,
    (
      phase36_step,
    ),
  )

  assert symmetry_match is not None

  reversed_phase36_step = (
    apply_inference_match(
      symmetry_match
    )
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  transitivity_match = find_inference_match(
    transitivity_rule,
    (
      phase35_step,
      reversed_phase36_step,
    ),
  )

  assert transitivity_match is not None

  final_step = apply_inference_match(
    transitivity_match
  )

  two_iota_2_eta_2 = Composition(
    left=Multiple(
      coefficient=2,
      expression=IOTA_2,
    ),
    right=ETA_2,
  )

  four_eta_2 = Multiple(
    coefficient=4,
    expression=ETA_2,
  )

  assert final_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=two_iota_2_eta_2,
    ),
    rhs=MapApplication(
      map=EHP_H_MAP,
      expression=four_eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert final_step.rule == (
    ProofRule.INFERENCE
  )

  assert final_step.premises == (
    phase35_step,
    reversed_phase36_step,
  )

  assert final_step.premises[0] is (
    phase35_result[
      "final_step"
    ]
  )

  assert (
    final_step.premises[1]
    is reversed_phase36_step
  )

  assert reversed_phase36_step.rule == (
    ProofRule.INFERENCE
  )

  assert reversed_phase36_step.premises == (
    phase36_step,
  )

  assert (
    reversed_phase36_step.premises[0]
    is phase36_result[
      "final_step"
    ]
  )

  assert phase35_step.rule == (
    ProofRule.INFERENCE
  )

  assert phase35_step.premises != ()

  assert phase36_step.rule == (
    ProofRule.INFERENCE
  )

  assert phase36_step.premises == (
    phase36_result[
      "h_four_eta_2_step"
    ],
    phase36_result[
      "four_h_eta_2_step"
    ],
  )

  assert (
    phase36_result[
      "h_four_eta_2_step"
    ].premises
    == (
      phase36_result[
        "homomorphism_step"
      ],
    )
  )

  assert (
    phase36_result[
      "four_h_eta_2_step"
    ].premises
    == (
      phase36_result[
        "h_eta_2_step"
      ],
    )
  )

  assert (
    phase36_result[
      "h_eta_2_step"
    ].premises
    == (
      phase36_result[
        "hopf_fact_step"
      ],
    )
  )


def test_phase37_5_final_result_stops_at_h_side_equality():
  phase35_result = (
    build_phase35_end_to_end()
  )

  phase36_result = (
    build_phase36_end_to_end()
  )

  phase35_step = phase35_result[
    "final_step"
  ]

  phase36_step = phase36_result[
    "final_step"
  ]

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  symmetry_match = find_inference_match(
    symmetry_rule,
    (
      phase36_step,
    ),
  )

  assert symmetry_match is not None

  reversed_phase36_step = (
    apply_inference_match(
      symmetry_match
    )
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  transitivity_match = find_inference_match(
    transitivity_rule,
    (
      phase35_step,
      reversed_phase36_step,
    ),
  )

  assert transitivity_match is not None

  final_step = apply_inference_match(
    transitivity_match
  )

  two_iota_2_eta_2 = Composition(
    left=Multiple(
      coefficient=2,
      expression=IOTA_2,
    ),
    right=ETA_2,
  )

  four_eta_2 = Multiple(
    coefficient=4,
    expression=ETA_2,
  )

  expected_h_side_equality = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=two_iota_2_eta_2,
    ),
    rhs=MapApplication(
      map=EHP_H_MAP,
      expression=four_eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  underlying_equality = Relation(
    lhs=two_iota_2_eta_2,
    rhs=four_eta_2,
    relation_type=RelationType.EQUALITY,
  )

  assert final_step.conclusion == (
    expected_h_side_equality
  )

  assert final_step.conclusion != (
    underlying_equality
  )

  assert final_step.inference_rule == (
    transitivity_rule
  )

  assert final_step.premises == (
    phase35_step,
    reversed_phase36_step,
  )

  assert (
    reversed_phase36_step.inference_rule
    == symmetry_rule
  )


def test_phase37_5_injective_reflection_requires_separate_injective_premise():
  phase35_result = (
    build_phase35_end_to_end()
  )

  phase36_result = (
    build_phase36_end_to_end()
  )

  phase35_step = phase35_result[
    "final_step"
  ]

  phase36_step = phase36_result[
    "final_step"
  ]

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  symmetry_match = find_inference_match(
    symmetry_rule,
    (
      phase36_step,
    ),
  )

  assert symmetry_match is not None

  reversed_phase36_step = (
    apply_inference_match(
      symmetry_match
    )
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  transitivity_match = find_inference_match(
    transitivity_rule,
    (
      phase35_step,
      reversed_phase36_step,
    ),
  )

  assert transitivity_match is not None

  h_side_equality_step = (
    apply_inference_match(
      transitivity_match
    )
  )

  reflection_rule = (
    injective_map_reflects_equality_inference_rule()
  )

  reflection_match = find_inference_match(
    reflection_rule,
    (
      h_side_equality_step,
    ),
  )

  assert reflection_match is None



