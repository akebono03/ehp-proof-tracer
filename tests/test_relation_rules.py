from expression import (
  Composition,
  Zero,
  eta,
  nu,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  relation_proof_step,
)
from relation_rules import (
  zero_composition_equality_implies_zero_inference_rule,
)


def test_zero_composition_equality_implies_zero():
  composition = Composition(
    left=nu(4),
    right=eta(3),
  )

  zero_composition_step = ProofStep(
    conclusion=Relation(
      lhs=composition,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  equality_step = relation_proof_step(
    Relation(
      lhs=eta(4),
      rhs=composition,
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = (
    zero_composition_equality_implies_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      zero_composition_step,
      equality_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    Relation(
      lhs=eta(4),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    zero_composition_step,
    equality_step,
  )


def test_zero_composition_equality_rule_rejects_noncomposition_zero_relation():
  zero_step = relation_proof_step(
    Relation(
      lhs=eta(3),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  equality_step = relation_proof_step(
    Relation(
      lhs=eta(4),
      rhs=eta(3),
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = (
    zero_composition_equality_implies_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      zero_step,
      equality_step,
    ),
  )

  assert match is None






