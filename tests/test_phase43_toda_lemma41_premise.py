from expression import (
  GeneratorSymbol,
  HomotopyElement,
  WhiteheadProduct,
  Zero,
)
from proof import (
  ProofRule,
  Relation,
  RelationType,
  relation_proof_step,
)


def build_phase43_1_representative_whitehead_product():
  iota_4 = HomotopyElement(
    name="ι₄",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  return WhiteheadProduct(
    left=iota_4,
    right=iota_4,
  )


def test_phase43_1_whitehead_product_can_be_relation_lhs():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  relation = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.EQUALITY,
  )

  assert relation.lhs is product
  assert relation.rhs == Zero()
  assert (
    relation.relation_type
    == RelationType.EQUALITY
  )


def test_phase43_1_whitehead_product_can_use_existing_zero_relation():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  relation = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert relation.lhs is product
  assert relation.rhs == Zero()
  assert (
    relation.relation_type
    == RelationType.ZERO
  )


def test_phase43_1_whitehead_product_zero_relation_preserves_structure():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  relation = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert relation.lhs == WhiteheadProduct(
    left=HomotopyElement(
      name="ι₄",
      dimension=4,
      generator=GeneratorSymbol(
        family="ι",
        index=4,
      ),
    ),
    right=HomotopyElement(
      name="ι₄",
      dimension=4,
      generator=GeneratorSymbol(
        family="ι",
        index=4,
      ),
    ),
  )


def test_phase43_1_zero_relation_is_distinct_from_equality_to_zero():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  zero_relation = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  equality_relation = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.EQUALITY,
  )

  assert zero_relation != equality_relation


def test_phase43_1_whitehead_product_zero_relation_can_be_proof_step():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  relation = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  step = relation_proof_step(
    relation
  )

  assert step.conclusion == relation
  assert step.premises == ()
  assert step.rule == ProofRule.RELATION


def test_phase43_1_current_relation_type_has_no_inequality():
  assert not hasattr(
    RelationType,
    "INEQUALITY",
  )



