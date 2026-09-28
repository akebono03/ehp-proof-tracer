from expression import (
  Composition,
  Expression,
  HomotopyElement,
  SmashProduct,
  Suspension,
)


def print_separator():
  print("=" * 60)


def build_representative_expressions():
  c = HomotopyElement(
    name="c",
    dimension=3,
    source=5,
    target=3,
  )

  c_smash_c = SmashProduct(
    left=c,
    right=c,
  )

  suspended_c_smash_c = Suspension(
    expression=c_smash_c,
  )

  return (
    c,
    c_smash_c,
    suspended_c_smash_c,
  )


def print_smash_product_representation(
  c,
  c_smash_c,
):
  print_separator()
  print("Phase 31 SmashProduct minimum representation")
  print_separator()
  print()

  print("[1] Representative operand")
  print("  c")
  print()
  print(
    "  c.source =",
    c.source,
  )
  print(
    "  c.target =",
    c.target,
  )
  print()

  print("[2] Construct smash product")
  print("  SmashProduct(")
  print("    left=c,")
  print("    right=c,")
  print("  )")
  print()
  print("  represents:")
  print("  c ∧ c")
  print()

  print("[3] Structural preservation")
  print(
    "  left == c:",
    c_smash_c.left == c,
  )
  print(
    "  right == c:",
    c_smash_c.right == c,
  )
  print(
    "  left == right:",
    (
      c_smash_c.left
      == c_smash_c.right
    ),
  )
  print(
    "  is Expression:",
    isinstance(
      c_smash_c,
      Expression,
    ),
  )


def print_suspension_representation(
  c_smash_c,
  suspended_c_smash_c,
):
  print()
  print_separator()
  print("Suspension of representative smash product")
  print_separator()
  print()

  print("[4] Construct suspension")
  print("  Suspension(")
  print("    expression=SmashProduct(")
  print("      left=c,")
  print("      right=c,")
  print("    ),")
  print("  )")
  print()
  print("  represents:")
  print("  E(c ∧ c)")
  print()

  print("[5] Structure is preserved")
  print(
    "  suspension.expression "
    "== c ∧ c:",
    (
      suspended_c_smash_c.expression
      == c_smash_c
    ),
  )
  print(
    "  inner left == c:",
    (
      suspended_c_smash_c
      .expression
      .left
      == c_smash_c.left
    ),
  )
  print(
    "  inner right == c:",
    (
      suspended_c_smash_c
      .expression
      .right
      == c_smash_c.right
    ),
  )


def print_structural_distinctions(
  c,
  c_smash_c,
  suspended_c_smash_c,
):
  print()
  print_separator()
  print("Structural distinctions")
  print_separator()
  print()

  composition = Composition(
    left=c,
    right=c,
  )

  print("[6] Distinct syntax remains distinct")
  print(
    "  c ∧ c != E(c ∧ c):",
    (
      c_smash_c
      != suspended_c_smash_c
    ),
  )
  print(
    "  c ∧ c != c ∘ c:",
    (
      c_smash_c
      != composition
    ),
  )
  print()

  print("Important:")
  print(
    "  structural distinction "
    "does not assert a new theorem"
  )
  print(
    "  no automatic normalization "
    "is performed"
  )


def print_typing_boundary(
  c_smash_c,
  suspended_c_smash_c,
):
  print()
  print_separator()
  print("Typing boundary")
  print_separator()
  print()

  print("[7] SmashProduct typing")
  print(
    "  SmashProduct has source:",
    hasattr(
      c_smash_c,
      "source",
    ),
  )
  print(
    "  SmashProduct has target:",
    hasattr(
      c_smash_c,
      "target",
    ),
  )
  print()

  print("[8] Suspension typing")
  print(
    "  E(c ∧ c).source =",
    suspended_c_smash_c.source,
  )
  print(
    "  E(c ∧ c).target =",
    suspended_c_smash_c.target,
  )
  print()

  print("[CONCLUSION]")
  print("  E(c ∧ c) is representable")
  print("  but is not automatically typed")


def print_phase31_boundary():
  print()
  print_separator()
  print("Phase 31-8 boundary")
  print_separator()
  print()

  print("Now structurally available:")
  print("  a ∧ b")
  print("  c ∧ c")
  print("  E(c ∧ c)")
  print()

  print("Structural guarantees:")
  print("  operands are preserved")
  print("  operand order is preserved")
  print("  SmashProduct is an Expression")
  print(
    "  SmashProduct is distinct "
    "from Composition"
  )
  print(
    "  suspended and unsuspended "
    "forms remain distinct"
  )
  print()

  print("Still outside Phase 31:")
  print("  SmashProduct source / target typing")
  print("  smash-product algebra")
  print(
    "  smash-product normalization"
  )
  print(
    "  H((Ec)∘a)=E(c∧c)∘H(a)"
  )
  print(
    "  Toda Prop.3.1 "
    "Barratt-Hilton"
  )
  print(
    "  symbolic (-1)^n algebra"
  )
  print(
    "  actual H((2ι₂)η₂) "
    "calculation"
  )
  print()

  print("Important:")
  print("  representation != typing")
  print(
    "  representation "
    "!= theorem knowledge"
  )


def main():
  print()
  print("EHP Proof Tracer")
  print(
    "Phase 31 SmashProduct "
    "capability demonstration"
  )
  print()

  (
    c,
    c_smash_c,
    suspended_c_smash_c,
  ) = build_representative_expressions()

  print_smash_product_representation(
    c,
    c_smash_c,
  )

  print_suspension_representation(
    c_smash_c,
    suspended_c_smash_c,
  )

  print_structural_distinctions(
    c,
    c_smash_c,
    suspended_c_smash_c,
  )

  print_typing_boundary(
    c_smash_c,
    suspended_c_smash_c,
  )

  print_phase31_boundary()

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()





