import pytest
from proof import (
  Proof,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  relation_proof_step,
)
from expression import Multiple, Zero, eta
from repository import RelationRepository


def test_relation():
  relation = Relation(
    lhs="2η3",
    rhs="0",
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  assert relation.lhs == "2η3"
  assert relation.rhs == "0"
  assert relation.relation_type == RelationType.ZERO
  assert relation.source == "Toda"


def test_proof_step():
  relation = Relation(
    lhs="2η3",
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  step = ProofStep(
    conclusion="η3 has order dividing 2",
    premises=(relation,),
    rule=ProofRule.RELATION,
  )

  assert step.conclusion == "η3 has order dividing 2"
  assert step.premises == (relation,)
  assert step.rule == ProofRule.RELATION


def test_proof():
  step1 = ProofStep(
    conclusion="ker(H) = <ν6η9²>",
    premises=(),
    rule=ProofRule.KERNEL_COMPUTATION,
  )

  step2 = ProofStep(
    conclusion="im(E) = ker(H)",
    premises=(step1,),
    rule=ProofRule.EHP_EXACTNESS,
  )

  proof = Proof(
    conclusion="desired result",
    steps=[step1, step2],
  )

  assert proof.conclusion == "desired result"
  assert proof.steps == [step1, step2]

def test_relation_with_expression():
  relation = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert relation.lhs == Multiple(2, eta(3))
  assert relation.rhs == Zero()

def test_relation_proof_step():
  relation = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  step = relation_proof_step(
    relation
  )

  assert step.conclusion == relation
  assert step.premises == ()
  assert step.rule == ProofRule.RELATION

def test_relation_proof_step_rejects_non_relation():
  with pytest.raises(TypeError):
    relation_proof_step(
      "2η3 = 0"
    )

def test_relation_repository_to_proof_step():
  relation = Relation(
    lhs=Multiple(2, eta(3)),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
    source="Toda",
  )

  repository = RelationRepository([
    relation,
  ])

  relations = repository.find_relations(
    lhs=Multiple(2, eta(3)),
  )

  step = relation_proof_step(
    relations[0]
  )

  assert step.conclusion == relation
  assert step.premises == ()
  assert step.rule == ProofRule.RELATION








