from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  SmashProduct,
  WhiteheadProduct,
)


def print_separator():
  print("=" * 72)


def whitehead_product_text(
  product,
):
  return (
    "["
    f"{product.left.name}"
    ","
    f"{product.right.name}"
    "]"
  )


def build_phase42_representative_whitehead_product():
  iota_4 = HomotopyElement(
    name="ι₄",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  whitehead_product = WhiteheadProduct(
    left=iota_4,
    right=iota_4,
  )

  composition = Composition(
    left=iota_4,
    right=iota_4,
  )

  smash_product = SmashProduct(
    left=iota_4,
    right=iota_4,
  )

  return {
    "iota_4": iota_4,
    "whitehead_product": whitehead_product,
    "composition": composition,
    "smash_product": smash_product,
  }


def print_phase42_representation(
  result,
):
  print_separator()
  print(
    "WhiteheadProduct "
    "minimum representation"
  )
  print_separator()
  print()

  print(
    "[1] Representative Whitehead product"
  )
  print(
    " ",
    whitehead_product_text(
      result[
        "whitehead_product"
      ]
    ),
  )

  print()
  print(
    "[2] Stored structure"
  )
  print(
    "  left =",
    result[
      "whitehead_product"
    ].left.name,
  )
  print(
    "  right =",
    result[
      "whitehead_product"
    ].right.name,
  )


def print_phase42_distinction(
  result,
):
  print()
  print_separator()
  print("Structural distinction")
  print_separator()
  print()

  product = result[
    "whitehead_product"
  ]

  print(
    "WhiteheadProduct != Composition =",
    product
    != result[
      "composition"
    ],
  )

  print(
    "WhiteheadProduct != SmashProduct =",
    product
    != result[
      "smash_product"
    ],
  )

  print(
    "WhiteheadProduct is not Composition =",
    not isinstance(
      product,
      Composition,
    ),
  )

  print(
    "WhiteheadProduct is not SmashProduct =",
    not isinstance(
      product,
      SmashProduct,
    ),
  )


def print_phase42_boundary(
  result,
):
  print()
  print_separator()
  print("Phase 42 completion boundary")
  print_separator()
  print()

  product = result[
    "whitehead_product"
  ]

  print("Now representable:")
  print(
    "  [ι₄,ι₄]"
  )
  print(
    "  arbitrary Expression operands"
  )
  print()

  print("Not encoded by WhiteheadProduct:")
  print(
    "  source typing =",
    hasattr(
      product,
      "source",
    ),
  )

  print(
    "  target typing =",
    hasattr(
      product,
      "target",
    ),
  )

  print(
    "  type compatibility =",
    hasattr(
      product,
      "is_type_compatible",
    ),
  )

  print(
    "  zero theorem semantics =",
    hasattr(
      product,
      "is_zero",
    ),
  )

  print(
    "  nonzero theorem semantics =",
    hasattr(
      product,
      "is_nonzero",
    ),
  )

  print(
    "  bilinearity =",
    hasattr(
      product,
      "bilinearity",
    ),
  )

  print(
    "  antisymmetry =",
    hasattr(
      product,
      "antisymmetry",
    ),
  )

  print(
    "  Toda Lemma 4.1 evaluation =",
    hasattr(
      product,
      "toda_lemma_4_1",
    ),
  )

  print(
    "  theorem provenance =",
    hasattr(
      product,
      "provenance",
    ),
  )


def main():
  print()
  print("EHP Proof Tracer")
  print("Phase 42 capability demonstration")
  print()

  result = (
    build_phase42_representative_whitehead_product()
  )

  print_phase42_representation(
    result
  )

  print_phase42_distinction(
    result
  )

  print_phase42_boundary(
    result
  )

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()


