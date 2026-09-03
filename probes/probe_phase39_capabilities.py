from expression import (
  ScalarSymbol,
)
from homotopy_groups import (
  PrimaryComponent,
)


def print_separator():
  print("=" * 72)


def scalar_text(
  value,
):
  if isinstance(
    value,
    ScalarSymbol,
  ):
    return value.name

  return str(
    value
  )


def primary_component_text(
  component,
):
  return (
    "π_"
    f"{scalar_text(component.group_dimension)}"
    "(S^"
    f"{scalar_text(component.sphere_dimension)}"
    ";"
    f"{component.prime}"
    ")"
  )


def build_phase39_representative_components():
  concrete_two_primary = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  concrete_three_primary = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=3,
  )

  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  symbolic_two_primary = PrimaryComponent(
    group_dimension=i,
    sphere_dimension=n,
    prime=2,
  )

  return {
    "concrete_two_primary": (
      concrete_two_primary
    ),
    "concrete_three_primary": (
      concrete_three_primary
    ),
    "symbolic_two_primary": (
      symbolic_two_primary
    ),
  }


def print_phase39_components(
  result,
):
  print_separator()
  print(
    "PrimaryComponent "
    "minimum representation"
  )
  print_separator()
  print()

  print("[1] Concrete 2-primary component")
  print(
    " ",
    primary_component_text(
      result[
        "concrete_two_primary"
      ]
    ),
  )
  print()

  print("[2] Same homotopy group, different prime")
  print(
    " ",
    primary_component_text(
      result[
        "concrete_three_primary"
      ]
    ),
  )
  print()

  print("[3] Symbolic 2-primary component")
  print(
    " ",
    primary_component_text(
      result[
        "symbolic_two_primary"
      ]
    ),
  )


def print_phase39_distinction(
  result,
):
  print()
  print_separator()
  print("Structural distinction")
  print_separator()
  print()

  two_primary = result[
    "concrete_two_primary"
  ]

  three_primary = result[
    "concrete_three_primary"
  ]

  print(
    "same dimensions + "
    "different prime are distinct =",
    two_primary != three_primary,
  )

  print(
    "2-primary prime =",
    two_primary.prime,
  )

  print(
    "3-primary prime =",
    three_primary.prime,
  )


def print_phase39_boundary(
  result,
):
  print()
  print_separator()
  print("Phase 39 completion boundary")
  print_separator()
  print()

  component = result[
    "concrete_two_primary"
  ]

  print("Now representable:")
  print(
    "  π_i(S^n;p)"
  )
  print(
    "  concrete dimensions"
  )
  print(
    "  symbolic dimensions"
  )
  print(
    "  distinct primary primes"
  )
  print()

  print("Not encoded by PrimaryComponent:")
  print(
    "  known AbelianGroup decomposition =",
    hasattr(
      component,
      "components",
    ),
  )
  print(
    "  concrete Subgroup elements =",
    hasattr(
      component,
      "elements",
    ),
  )
  print(
    "  finiteness fact =",
    hasattr(
      component,
      "finite",
    ),
  )
  print(
    "  membership element =",
    hasattr(
      component,
      "element",
    ),
  )
  print(
    "  Toda primary group =",
    hasattr(
      component,
      "toda_primary_group",
    ),
  )
  print(
    "  theorem provenance =",
    hasattr(
      component,
      "provenance",
    ),
  )


def main():
  print()
  print("EHP Proof Tracer")
  print("Phase 39 capability demonstration")
  print()

  result = (
    build_phase39_representative_components()
  )

  print_phase39_components(
    result
  )

  print_phase39_distinction(
    result
  )

  print_phase39_boundary(
    result
  )

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()



