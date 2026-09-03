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
from proof import (
  ProofRule,
  apply_inference_match,
  find_inference_match,
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



