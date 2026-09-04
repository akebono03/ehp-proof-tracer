from expression import (
  ScalarSymbol,
)
from homotopy_groups import (
  PrimaryComponent,
  TodaPrimaryGroup,
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


def toda_primary_group_text(
  group,
):
  return (
    "π_"
    f"{scalar_text(group.group_dimension)}"
    "^"
    f"{scalar_text(group.sphere_dimension)}"
  )


def build_phase40_representative_groups():
  concrete_group = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=5,
  )

  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  symbolic_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=n,
  )

  critical_degree_group = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  matching_primary_component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  return {
    "concrete_group": (
      concrete_group
    ),
    "symbolic_group": (
      symbolic_group
    ),
    "critical_degree_group": (
      critical_degree_group
    ),
    "matching_primary_component": (
      matching_primary_component
    ),
  }


def print_phase40_groups(
  result,
):
  print_separator()
  print(
    "TodaPrimaryGroup "
    "minimum representation"
  )
  print_separator()
  print()

  print("[1] Concrete Toda primary group")
  print(
    " ",
    toda_primary_group_text(
      result[
        "concrete_group"
      ]
    ),
  )
  print()

  print("[2] Symbolic Toda primary group")
  print(
    " ",
    toda_primary_group_text(
      result[
        "symbolic_group"
      ]
    ),
  )
  print()

  print(
    "[3] Critical-degree "
    "structural object"
  )
  print(
    " ",
    toda_primary_group_text(
      result[
        "critical_degree_group"
      ]
    ),
  )


def print_phase40_distinction(
  result,
):
  print()
  print_separator()
  print("Structural distinction")
  print_separator()
  print()

  concrete_group = result[
    "concrete_group"
  ]

  primary_component = result[
    "matching_primary_component"
  ]

  print(
    "TodaPrimaryGroup != "
    "PrimaryComponent =",
    concrete_group != primary_component,
  )

  print(
    "TodaPrimaryGroup has prime =",
    hasattr(
      concrete_group,
      "prime",
    ),
  )

  print(
    "TodaPrimaryGroup has "
    "membership element =",
    hasattr(
      concrete_group,
      "element",
    ),
  )


def print_phase40_boundary(
  result,
):
  print()
  print_separator()
  print("Phase 40 completion boundary")
  print_separator()
  print()

  critical_group = result[
    "critical_degree_group"
  ]

  print("Now representable:")
  print(
    "  π_i^n"
  )
  print(
    "  concrete dimensions"
  )
  print(
    "  symbolic dimensions"
  )
  print(
    "  compound ScalarValue dimensions"
  )
  print(
    "  critical-degree structural object"
  )
  print()

  print("Not encoded by TodaPrimaryGroup:")
  print(
    "  evaluated Toda (4.3) "
    "definition =",
    hasattr(
      critical_group,
      "evaluated_definition",
    ),
  )
  print(
    "  preimage subgroup =",
    hasattr(
      critical_group,
      "preimage_subgroup",
    ),
  )
  print(
    "  automatic PrimaryComponent "
    "conversion =",
    hasattr(
      critical_group,
      "to_primary_component",
    ),
  )
  print(
    "  theorem provenance =",
    hasattr(
      critical_group,
      "provenance",
    ),
  )


def main():
  print()
  print("EHP Proof Tracer")
  print("Phase 40 capability demonstration")
  print()

  result = (
    build_phase40_representative_groups()
  )

  print_phase40_groups(
    result
  )

  print_phase40_distinction(
    result
  )

  print_phase40_boundary(
    result
  )

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()



