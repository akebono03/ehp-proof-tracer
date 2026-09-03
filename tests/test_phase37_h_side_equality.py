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
from probes.probe_phase35_capabilities import (
  build_phase35_end_to_end,
)
from probes.probe_phase36_capabilities import (
  build_phase36_end_to_end,
)
from proof import (
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
)
from relation_rules import (
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



