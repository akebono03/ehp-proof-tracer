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
  find_inference_match,
  relation_proof_step,
)
from relation_rules import (
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
  zero_equality_implies_zero_inference_rule,
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


def test_phase43_2_whitehead_product_zero_premise_has_canonical_relation():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  premise = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert premise == Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert (
    premise.relation_type
    == RelationType.ZERO
  )

  assert premise.rhs == Zero()


def test_phase43_2_whitehead_product_zero_premise_preserves_operands():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  premise = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert isinstance(
    premise.lhs,
    WhiteheadProduct,
  )

  assert premise.lhs.left == HomotopyElement(
    name="ι₄",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  assert premise.lhs.right == HomotopyElement(
    name="ι₄",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )


def test_phase43_2_whitehead_product_zero_premise_is_structurally_reconstructible():
  premise = Relation(
    lhs=(
      build_phase43_1_representative_whitehead_product()
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  reconstructed = Relation(
    lhs=WhiteheadProduct(
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
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert premise == reconstructed


def test_phase43_2_whitehead_product_zero_premise_can_be_explicit_proof_premise():
  premise = Relation(
    lhs=(
      build_phase43_1_representative_whitehead_product()
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  step = relation_proof_step(
    premise
  )

  assert step.conclusion == premise

  assert (
    step.conclusion.relation_type
    == RelationType.ZERO
  )

  assert isinstance(
    step.conclusion.lhs,
    WhiteheadProduct,
  )

  assert step.conclusion.rhs == Zero()

  assert step.premises == ()

  assert step.rule == (
    ProofRule.RELATION
  )


def test_phase43_2_zero_premise_has_no_toda_lemma_evaluation():
  premise = Relation(
    lhs=(
      build_phase43_1_representative_whitehead_product()
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert not hasattr(
    premise,
    "toda_lemma_4_1",
  )

  assert not hasattr(
    premise,
    "case",
  )

  assert not hasattr(
    premise,
    "evaluated_group",
  )


def test_phase43_3_relation_type_has_inequality():
  assert hasattr(
    RelationType,
    "INEQUALITY",
  )

  assert (
    RelationType.INEQUALITY.value
    == "inequality"
  )


def test_phase43_3_whitehead_product_nonzero_premise_has_canonical_relation():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  premise = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.INEQUALITY,
  )

  assert premise.lhs is product
  assert premise.rhs == Zero()

  assert (
    premise.relation_type
    == RelationType.INEQUALITY
  )


def test_phase43_3_whitehead_product_nonzero_premise_preserves_operands():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  premise = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.INEQUALITY,
  )

  assert isinstance(
    premise.lhs,
    WhiteheadProduct,
  )

  assert premise.lhs.left == HomotopyElement(
    name="ι₄",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  assert premise.lhs.right == HomotopyElement(
    name="ι₄",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )


def test_phase43_3_whitehead_product_nonzero_premise_is_structurally_reconstructible():
  premise = Relation(
    lhs=(
      build_phase43_1_representative_whitehead_product()
    ),
    rhs=Zero(),
    relation_type=RelationType.INEQUALITY,
  )

  reconstructed = Relation(
    lhs=WhiteheadProduct(
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
    ),
    rhs=Zero(),
    relation_type=RelationType.INEQUALITY,
  )

  assert premise == reconstructed


def test_phase43_3_whitehead_product_zero_and_nonzero_premises_are_distinct():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  zero_premise = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  nonzero_premise = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.INEQUALITY,
  )

  assert zero_premise != nonzero_premise

  assert (
    zero_premise.relation_type
    == RelationType.ZERO
  )

  assert (
    nonzero_premise.relation_type
    == RelationType.INEQUALITY
  )


def test_phase43_3_whitehead_product_nonzero_premise_can_be_explicit_proof_premise():
  premise = Relation(
    lhs=(
      build_phase43_1_representative_whitehead_product()
    ),
    rhs=Zero(),
    relation_type=RelationType.INEQUALITY,
  )

  step = relation_proof_step(
    premise
  )

  assert step.conclusion == premise

  assert (
    step.conclusion.relation_type
    == RelationType.INEQUALITY
  )

  assert isinstance(
    step.conclusion.lhs,
    WhiteheadProduct,
  )

  assert step.conclusion.rhs == Zero()

  assert step.premises == ()

  assert step.rule == (
    ProofRule.RELATION
  )


def test_phase43_3_nonzero_premise_has_no_automatic_semantics():
  premise = Relation(
    lhs=(
      build_phase43_1_representative_whitehead_product()
    ),
    rhs=Zero(),
    relation_type=RelationType.INEQUALITY,
  )

  assert not hasattr(
    premise,
    "is_nonzero",
  )

  assert not hasattr(
    premise,
    "contradicts",
  )

  assert not hasattr(
    premise,
    "toda_lemma_4_1",
  )

  assert not hasattr(
    premise,
    "case",
  )

  assert not hasattr(
    premise,
    "evaluated_group",
  )


def test_phase43_4_relation_types_remain_structurally_distinct():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  equality_relation = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.EQUALITY,
  )

  zero_relation = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  inequality_relation = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.INEQUALITY,
  )

  assert equality_relation != zero_relation
  assert equality_relation != inequality_relation
  assert zero_relation != inequality_relation


def test_phase43_4_equality_symmetry_rejects_inequality():
  inequality_step = relation_proof_step(
    Relation(
      lhs=(
        build_phase43_1_representative_whitehead_product()
      ),
      rhs=Zero(),
      relation_type=RelationType.INEQUALITY,
    )
  )

  rule = (
    equality_symmetry_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      inequality_step,
    ),
  )

  assert match is None


def test_phase43_4_equality_transitivity_rejects_inequality():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  inequality_step = relation_proof_step(
    Relation(
      lhs=product,
      rhs=Zero(),
      relation_type=RelationType.INEQUALITY,
    )
  )

  equality_step = relation_proof_step(
    Relation(
      lhs=Zero(),
      rhs=product,
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = (
    equality_transitivity_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      inequality_step,
      equality_step,
    ),
  )

  assert match is None


def test_phase43_4_zero_propagation_rejects_inequality_as_zero_premise():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  inequality_step = relation_proof_step(
    Relation(
      lhs=product,
      rhs=Zero(),
      relation_type=RelationType.INEQUALITY,
    )
  )

  equality_step = relation_proof_step(
    Relation(
      lhs=HomotopyElement(
        name="x",
        dimension=4,
      ),
      rhs=product,
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = (
    zero_equality_implies_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      inequality_step,
      equality_step,
    ),
  )

  assert match is None


def test_phase43_4_zero_propagation_rejects_inequality_as_equality_premise():
  product = (
    build_phase43_1_representative_whitehead_product()
  )

  zero_step = relation_proof_step(
    Relation(
      lhs=product,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  inequality_step = relation_proof_step(
    Relation(
      lhs=HomotopyElement(
        name="x",
        dimension=4,
      ),
      rhs=product,
      relation_type=RelationType.INEQUALITY,
    )
  )

  rule = (
    zero_equality_implies_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      zero_step,
      inequality_step,
    ),
  )

  assert match is None






