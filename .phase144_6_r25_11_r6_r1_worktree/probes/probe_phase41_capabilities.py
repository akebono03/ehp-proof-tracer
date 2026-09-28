from algebra import (
  Subgroup,
)
from expression import (
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homomorphism_rules import (
  SUSPENSION_MAP,
)
from homotopy_groups import (
  PreimageSubgroup,
  PrimaryComponent,
  TodaPrimaryGroup,
)
from set_rules import (
  ImageSubgroupReference,
  KernelSubgroupReference,
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

  if isinstance(
    value,
    ScalarProduct,
  ):
    return (
      f"{scalar_text(value.left)}"
      f"{scalar_text(value.right)}"
    )

  if isinstance(
    value,
    ScalarSum,
  ):
    return (
      f"{scalar_text(value.left)}"
      "+"
      f"{scalar_text(value.right)}"
    )

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


def preimage_subgroup_text(
  preimage,
):
  return (
    f"{preimage.map.name}"
    "^-1("
    f"{primary_component_text(preimage.subgroup)}"
    ")"
  )


def build_phase41_representative_preimages():
  concrete_target = PrimaryComponent(
    group_dimension=10,
    sphere_dimension=6,
    prime=2,
  )

  concrete_preimage = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=concrete_target,
  )

  n = ScalarSymbol(
    name="n",
  )

  symbolic_target = PrimaryComponent(
    group_dimension=ScalarProduct(
      left=2,
      right=n,
    ),
    sphere_dimension=ScalarSum(
      left=n,
      right=1,
    ),
    prime=2,
  )

  symbolic_preimage = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=symbolic_target,
  )

  critical_toda_group = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  return {
    "concrete_preimage": (
      concrete_preimage
    ),
    "symbolic_preimage": (
      symbolic_preimage
    ),
    "critical_toda_group": (
      critical_toda_group
    ),
  }


def print_phase41_preimages(
  result,
):
  print_separator()
  print(
    "PreimageSubgroup "
    "minimum representation"
  )
  print_separator()
  print()

  print(
    "[1] Concrete suspension preimage"
  )
  print(
    " ",
    preimage_subgroup_text(
      result[
        "concrete_preimage"
      ]
    ),
  )
  print()

  print(
    "[2] Symbolic critical-degree target"
  )
  print(
    " ",
    preimage_subgroup_text(
      result[
        "symbolic_preimage"
      ]
    ),
  )


def print_phase41_distinction(
  result,
):
  print()
  print_separator()
  print("Structural distinction")
  print_separator()
  print()

  concrete_preimage = result[
    "concrete_preimage"
  ]

  print(
    "PreimageSubgroup != Subgroup =",
    not isinstance(
      concrete_preimage,
      Subgroup,
    ),
  )

  print(
    "PreimageSubgroup != "
    "ImageSubgroupReference =",
    not isinstance(
      concrete_preimage,
      ImageSubgroupReference,
    ),
  )

  print(
    "PreimageSubgroup != "
    "KernelSubgroupReference =",
    not isinstance(
      concrete_preimage,
      KernelSubgroupReference,
    ),
  )

  print(
    "PreimageSubgroup != "
    "PrimaryComponent =",
    not isinstance(
      concrete_preimage,
      PrimaryComponent,
    ),
  )


def print_phase41_boundary(
  result,
):
  print()
  print_separator()
  print("Phase 41 completion boundary")
  print_separator()
  print()

  concrete_preimage = result[
    "concrete_preimage"
  ]

  critical_toda_group = result[
    "critical_toda_group"
  ]

  print("Now representable:")
  print(
    "  E^-1(π_10(S^6;2))"
  )
  print(
    "  E^-1(π_2n(S^(n+1);2))"
  )
  print(
    "  arbitrary MapSymbol preimage structure"
  )
  print()

  print("Not encoded by PreimageSubgroup:")
  print(
    "  membership element =",
    hasattr(
      concrete_preimage,
      "element",
    ),
  )

  print(
    "  membership equivalence =",
    hasattr(
      concrete_preimage,
      "membership_equivalence",
    ),
  )

  print(
    "  theorem provenance =",
    hasattr(
      concrete_preimage,
      "provenance",
    ),
  )

  print()

  print("Not encoded by TodaPrimaryGroup:")
  print(
    "  automatic preimage conversion =",
    hasattr(
      critical_toda_group,
      "to_preimage_subgroup",
    ),
  )

  print(
    "  evaluated Toda (4.3) definition =",
    hasattr(
      critical_toda_group,
      "evaluated_definition",
    ),
  )


def main():
  print()
  print("EHP Proof Tracer")
  print("Phase 41 capability demonstration")
  print()

  result = (
    build_phase41_representative_preimages()
  )

  print_phase41_preimages(
    result
  )

  print_phase41_distinction(
    result
  )

  print_phase41_boundary(
    result
  )

  print()
  print_separator()
  print("Demo complete")
  print_separator()


if __name__ == "__main__":
  main()



