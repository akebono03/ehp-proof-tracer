from typing import (
  get_type_hints,
)

from expression import (
  Composition,
  Expression,
  HomotopyElement,
  SmashProduct,
  WhiteheadProduct,
)


def test_phase42_1_composition_is_expression():
  left = HomotopyElement(
    name="a",
    dimension=4,
    source=3,
    target=2,
  )

  right = HomotopyElement(
    name="b",
    dimension=5,
    source=4,
    target=3,
  )

  composition = Composition(
    left=left,
    right=right,
  )

  assert isinstance(
    composition,
    Expression,
  )


def test_phase42_1_smash_product_is_expression():
  left = HomotopyElement(
    name="a",
    dimension=4,
  )

  right = HomotopyElement(
    name="b",
    dimension=5,
  )

  smash_product = SmashProduct(
    left=left,
    right=right,
  )

  assert isinstance(
    smash_product,
    Expression,
  )


def test_phase42_1_composition_operands_use_expression():
  type_hints = get_type_hints(
    Composition
  )

  assert type_hints[
    "left"
  ] is Expression

  assert type_hints[
    "right"
  ] is Expression


def test_phase42_1_smash_product_operands_use_expression():
  type_hints = get_type_hints(
    SmashProduct
  )

  assert type_hints[
    "left"
  ] is Expression

  assert type_hints[
    "right"
  ] is Expression


def test_phase42_1_composition_and_smash_product_are_structurally_distinct():
  left = HomotopyElement(
    name="a",
    dimension=4,
  )

  right = HomotopyElement(
    name="b",
    dimension=5,
  )

  composition = Composition(
    left=left,
    right=right,
  )

  smash_product = SmashProduct(
    left=left,
    right=right,
  )

  assert composition != smash_product


def test_phase42_1_composition_retains_current_typing_behavior():
  left = HomotopyElement(
    name="a",
    dimension=4,
    source=3,
    target=2,
  )

  right = HomotopyElement(
    name="b",
    dimension=5,
    source=4,
    target=3,
  )

  composition = Composition(
    left=left,
    right=right,
  )

  assert composition.is_type_compatible()


def test_phase42_1_smash_product_has_no_source_or_target_typing():
  left = HomotopyElement(
    name="a",
    dimension=4,
    source=3,
    target=2,
  )

  right = HomotopyElement(
    name="b",
    dimension=5,
    source=4,
    target=3,
  )

  smash_product = SmashProduct(
    left=left,
    right=right,
  )

  assert not hasattr(
    smash_product,
    "source",
  )

  assert not hasattr(
    smash_product,
    "target",
  )


def test_phase42_1_smash_product_has_no_type_compatibility_method():
  left = HomotopyElement(
    name="a",
    dimension=4,
    source=3,
    target=2,
  )

  right = HomotopyElement(
    name="b",
    dimension=5,
    source=4,
    target=3,
  )

  smash_product = SmashProduct(
    left=left,
    right=right,
  )

  assert not hasattr(
    smash_product,
    "is_type_compatible",
  )


def test_phase42_1_composition_with_smash_product_is_constructible_but_not_type_compatible():
  left = HomotopyElement(
    name="a",
    dimension=4,
    source=3,
    target=2,
  )

  right = HomotopyElement(
    name="b",
    dimension=5,
    source=4,
    target=3,
  )

  smash_product = SmashProduct(
    left=left,
    right=right,
  )

  composition = Composition(
    left=smash_product,
    right=right,
  )

  assert composition.left is smash_product
  assert composition.right is right
  assert not composition.is_type_compatible()


def test_phase42_2_whitehead_product_is_expression():
  left = HomotopyElement(
    name="a",
    dimension=4,
  )

  right = HomotopyElement(
    name="b",
    dimension=5,
  )

  product = WhiteheadProduct(
    left=left,
    right=right,
  )

  assert isinstance(
    product,
    Expression,
  )


def test_phase42_2_whitehead_product_preserves_left_and_right():
  left = HomotopyElement(
    name="a",
    dimension=4,
  )

  right = HomotopyElement(
    name="b",
    dimension=5,
  )

  product = WhiteheadProduct(
    left=left,
    right=right,
  )

  assert product.left is left
  assert product.right is right


def test_phase42_2_whitehead_product_operands_use_expression():
  type_hints = get_type_hints(
    WhiteheadProduct
  )

  assert type_hints[
    "left"
  ] is Expression

  assert type_hints[
    "right"
  ] is Expression


def test_phase42_2_whitehead_product_has_structural_equality():
  left = HomotopyElement(
    name="a",
    dimension=4,
  )

  right = HomotopyElement(
    name="b",
    dimension=5,
  )

  first = WhiteheadProduct(
    left=left,
    right=right,
  )

  same = WhiteheadProduct(
    left=HomotopyElement(
      name="a",
      dimension=4,
    ),
    right=HomotopyElement(
      name="b",
      dimension=5,
    ),
  )

  different_left = WhiteheadProduct(
    left=HomotopyElement(
      name="c",
      dimension=4,
    ),
    right=right,
  )

  different_right = WhiteheadProduct(
    left=left,
    right=HomotopyElement(
      name="c",
      dimension=5,
    ),
  )

  assert first == same
  assert first != different_left
  assert first != different_right


def test_phase42_3_whitehead_product_is_distinct_from_composition():
  left = HomotopyElement(
    name="a",
    dimension=4,
  )

  right = HomotopyElement(
    name="b",
    dimension=5,
  )

  whitehead_product = WhiteheadProduct(
    left=left,
    right=right,
  )

  composition = Composition(
    left=left,
    right=right,
  )

  assert whitehead_product != composition


def test_phase42_3_whitehead_product_is_not_composition():
  whitehead_product = WhiteheadProduct(
    left=HomotopyElement(
      name="a",
      dimension=4,
    ),
    right=HomotopyElement(
      name="b",
      dimension=5,
    ),
  )

  assert not isinstance(
    whitehead_product,
    Composition,
  )


def test_phase42_3_whitehead_product_is_distinct_from_smash_product():
  left = HomotopyElement(
    name="a",
    dimension=4,
  )

  right = HomotopyElement(
    name="b",
    dimension=5,
  )

  whitehead_product = WhiteheadProduct(
    left=left,
    right=right,
  )

  smash_product = SmashProduct(
    left=left,
    right=right,
  )

  assert whitehead_product != smash_product


def test_phase42_3_whitehead_product_is_not_smash_product():
  whitehead_product = WhiteheadProduct(
    left=HomotopyElement(
      name="a",
      dimension=4,
    ),
    right=HomotopyElement(
      name="b",
      dimension=5,
    ),
  )

  assert not isinstance(
    whitehead_product,
    SmashProduct,
  )




