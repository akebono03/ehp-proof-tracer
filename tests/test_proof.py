from proof import (
  Proof,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)


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





