from expression import (
  Composition,
  MapApplication,
  Multiple,
)
from hopf_facts import (
  ETA_2,
)
from map_facts import (
  EHP_H_MAP,
  EHP_H_MAP_ISOMORPHISM_FACT,
  EHP_H_MAP_TYPING_FACT,
  MAP_ISOMORPHISM_FACT_REPOSITORY,
)
from map_property_rules import (
  InjectiveMapStatement,
  IsomorphismStatement,
  isomorphism_implies_injective_inference_rule,
)
from probes.probe_phase37_capabilities import (
  build_phase37_end_to_end,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from suspension_facts import (
  IOTA_2,
)


def test_phase38_1_actual_h_isomorphism_fact_is_available_from_repository():
  fact = (
    MAP_ISOMORPHISM_FACT_REPOSITORY
    .lookup(
      EHP_H_MAP_TYPING_FACT
    )
  )

  assert fact is (
    EHP_H_MAP_ISOMORPHISM_FACT
  )

  assert fact.typing is (
    EHP_H_MAP_TYPING_FACT
  )

  assert fact.typing.map is (
    EHP_H_MAP
  )


def test_phase38_1_actual_h_isomorphism_fact_materializes_canonical_h():
  isomorphism_step = (
    EHP_H_MAP_ISOMORPHISM_FACT
    .to_proof_step()
  )

  assert isomorphism_step.conclusion == (
    IsomorphismStatement(
      map=EHP_H_MAP,
    )
  )

  assert isomorphism_step.conclusion.map is (
    EHP_H_MAP
  )

  assert isomorphism_step.rule == (
    ProofRule.GIVEN
  )

  assert isomorphism_step.premises == ()

  assert isomorphism_step.inference_rule is None


def test_phase38_1_actual_h_isomorphism_matches_existing_injectivity_rule():
  isomorphism_step = (
    EHP_H_MAP_ISOMORPHISM_FACT
    .to_proof_step()
  )

  rule = (
    isomorphism_implies_injective_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      isomorphism_step,
    ),
  )

  assert match is not None

  injective_step = (
    apply_inference_match(
      match
    )
  )

  assert injective_step.conclusion == (
    InjectiveMapStatement(
      map=EHP_H_MAP,
    )
  )


def test_phase38_1_actual_h_injectivity_preserves_isomorphism_provenance():
  isomorphism_step = (
    EHP_H_MAP_ISOMORPHISM_FACT
    .to_proof_step()
  )

  rule = (
    isomorphism_implies_injective_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      isomorphism_step,
    ),
  )

  assert match is not None

  injective_step = (
    apply_inference_match(
      match
    )
  )

  assert injective_step.rule == (
    ProofRule.INFERENCE
  )

  assert injective_step.inference_rule == (
    rule
  )

  assert injective_step.premises == (
    isomorphism_step,
  )

  assert (
    injective_step.premises[0]
    is isomorphism_step
  )


def test_phase38_2_phase37_final_step_has_reflection_compatible_shape():
  result = (
    build_phase37_end_to_end()
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

  four_eta_2 = Multiple(
    coefficient=4,
    expression=ETA_2,
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
    rhs=MapApplication(
      map=EHP_H_MAP,
      expression=four_eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert isinstance(
    final_step.conclusion.lhs,
    MapApplication,
  )

  assert isinstance(
    final_step.conclusion.rhs,
    MapApplication,
  )

  assert final_step.conclusion.relation_type == (
    RelationType.EQUALITY
  )


def test_phase38_2_phase37_final_equality_uses_same_actual_h_on_both_sides():
  result = (
    build_phase37_end_to_end()
  )

  final_step = result[
    "final_step"
  ]

  lhs = final_step.conclusion.lhs
  rhs = final_step.conclusion.rhs

  assert isinstance(
    lhs,
    MapApplication,
  )

  assert isinstance(
    rhs,
    MapApplication,
  )

  assert lhs.map is (
    EHP_H_MAP
  )

  assert rhs.map is (
    EHP_H_MAP
  )

  assert lhs.map is (
    rhs.map
  )

  assert (
    lhs.expression
    != rhs.expression
  )


def test_phase38_2_phase37_final_h_matches_actual_injective_h():
  isomorphism_step = (
    EHP_H_MAP_ISOMORPHISM_FACT
    .to_proof_step()
  )

  rule = (
    isomorphism_implies_injective_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      isomorphism_step,
    ),
  )

  assert match is not None

  injective_step = (
    apply_inference_match(
      match
    )
  )

  phase37_result = (
    build_phase37_end_to_end()
  )

  h_side_equality_step = (
    phase37_result[
      "final_step"
    ]
  )

  lhs = (
    h_side_equality_step
    .conclusion
    .lhs
  )

  rhs = (
    h_side_equality_step
    .conclusion
    .rhs
  )

  assert injective_step.conclusion == (
    InjectiveMapStatement(
      map=EHP_H_MAP,
    )
  )

  assert isinstance(
    lhs,
    MapApplication,
  )

  assert isinstance(
    rhs,
    MapApplication,
  )

  assert injective_step.conclusion.map is (
    EHP_H_MAP
  )

  assert injective_step.conclusion.map is (
    lhs.map
  )

  assert injective_step.conclusion.map is (
    rhs.map
  )




