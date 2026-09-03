from typing import (
  get_type_hints,
)

from algebra import (
  Subgroup,
)
from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  HomotopyElement,
  ScalarSum,
  ScalarSymbol,
  ScalarValue,
)
from homotopy_groups import (
  PrimaryComponent,
)
from models import (
  AbelianGroup,
  GroupComponent,
)


def test_phase39_2_primary_component_represents_concrete_two_primary_group():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  assert component.group_dimension == 8
  assert component.sphere_dimension == 5
  assert component.prime == 2


def test_phase39_2_primary_component_supports_arbitrary_prime_structurally():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=3,
  )

  assert component.group_dimension == 8
  assert component.sphere_dimension == 5
  assert component.prime == 3


def test_phase39_2_primary_component_supports_symbolic_group_dimension():
  i = ScalarSymbol(
    name="i",
  )

  component = PrimaryComponent(
    group_dimension=i,
    sphere_dimension=5,
    prime=2,
  )

  assert component.group_dimension == i
  assert component.sphere_dimension == 5
  assert component.prime == 2


def test_phase39_2_primary_component_supports_symbolic_sphere_dimension():
  n = ScalarSymbol(
    name="n",
  )

  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=n,
    prime=2,
  )

  assert component.group_dimension == 8
  assert component.sphere_dimension == n
  assert component.prime == 2


def test_phase39_2_primary_component_structural_equality_uses_all_fields():
  first = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  same = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  different_prime = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=3,
  )

  different_group_dimension = PrimaryComponent(
    group_dimension=9,
    sphere_dimension=5,
    prime=2,
  )

  different_sphere_dimension = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=6,
    prime=2,
  )

  assert first == same
  assert first != different_prime
  assert first != different_group_dimension
  assert first != different_sphere_dimension


def test_phase39_3_two_primary_component_differs_from_three_primary_component():
  two_primary = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  three_primary = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=3,
  )

  assert two_primary != three_primary


def test_phase39_3_primary_components_with_different_group_dimensions_are_distinct():
  first = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  second = PrimaryComponent(
    group_dimension=9,
    sphere_dimension=5,
    prime=2,
  )

  assert first != second


def test_phase39_3_primary_components_with_different_sphere_dimensions_are_distinct():
  first = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  second = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=6,
    prime=2,
  )

  assert first != second


def test_phase39_3_primary_component_is_not_an_abelian_group():
  primary_component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  abelian_group = AbelianGroup(
    n=5,
    k=3,
    components=[
      GroupComponent(
        id=0,
        order=2,
        generator="x",
        element=[],
        gen_coe=[],
      ),
    ],
  )

  assert not isinstance(
    primary_component,
    AbelianGroup,
  )

  assert primary_component != abelian_group


def test_phase39_3_primary_component_is_not_a_subgroup():
  primary_component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  ambient_group = AbelianGroup(
    n=5,
    k=3,
    components=[
      GroupComponent(
        id=0,
        order=2,
        generator="x",
        element=[],
        gen_coe=[],
      ),
    ],
  )

  subgroup = Subgroup(
    ambient_group=ambient_group,
    elements=frozenset(),
    generators=(),
  )

  assert not isinstance(
    primary_component,
    Subgroup,
  )

  assert primary_component != subgroup


def test_phase39_3_primary_component_has_no_known_decomposition_fields():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  assert not hasattr(
    component,
    "components",
  )

  assert not hasattr(
    component,
    "orders",
  )

  assert not hasattr(
    component,
    "generators",
  )

  assert not hasattr(
    component,
    "elements",
  )


def test_phase39_4_primary_component_uses_existing_scalar_value_dimension_types():
  primary_type_hints = get_type_hints(
    PrimaryComponent
  )

  membership_type_hints = get_type_hints(
    HomotopyGroupMembershipStatement
  )

  assert primary_type_hints[
    "group_dimension"
  ] == ScalarValue

  assert primary_type_hints[
    "sphere_dimension"
  ] == ScalarValue

  assert membership_type_hints[
    "group_dimension"
  ] == ScalarValue

  assert membership_type_hints[
    "sphere_dimension"
  ] == ScalarValue


def test_phase39_4_concrete_primary_component_matches_existing_dimension_representation():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  element = HomotopyElement(
    name="a",
    dimension=3,
  )

  membership = (
    HomotopyGroupMembershipStatement(
      element=element,
      group_dimension=8,
      sphere_dimension=5,
    )
  )

  assert component.group_dimension == (
    membership.group_dimension
  )

  assert component.sphere_dimension == (
    membership.sphere_dimension
  )


def test_phase39_4_symbolic_primary_component_matches_existing_dimension_representation():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  component = PrimaryComponent(
    group_dimension=i,
    sphere_dimension=n,
    prime=2,
  )

  element = HomotopyElement(
    name="a",
    dimension=1,
  )

  membership = (
    HomotopyGroupMembershipStatement(
      element=element,
      group_dimension=i,
      sphere_dimension=n,
    )
  )

  assert component.group_dimension == (
    membership.group_dimension
  )

  assert component.sphere_dimension == (
    membership.sphere_dimension
  )

  assert component.group_dimension is i
  assert component.sphere_dimension is n


def test_phase39_4_primary_component_accepts_compound_symbolic_dimension():
  n = ScalarSymbol(
    name="n",
  )

  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )

  component = PrimaryComponent(
    group_dimension=n_plus_one,
    sphere_dimension=n,
    prime=2,
  )

  assert component.group_dimension == (
    ScalarSum(
      left=n,
      right=1,
    )
  )

  assert component.sphere_dimension == n
  assert component.prime == 2


def test_phase39_4_primary_component_prime_typing_remains_integer():
  type_hints = get_type_hints(
    PrimaryComponent
  )

  assert type_hints[
    "prime"
  ] is int


def test_phase39_5_primary_component_is_not_membership_statement():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  assert not isinstance(
    component,
    HomotopyGroupMembershipStatement,
  )

  assert not hasattr(
    component,
    "element",
  )


def test_phase39_5_primary_component_does_not_encode_finiteness():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  assert not hasattr(
    component,
    "finite",
  )

  assert not hasattr(
    component,
    "is_finite",
  )


def test_phase39_5_primary_component_has_no_automatic_subgroup_conversion():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  assert not hasattr(
    component,
    "subgroup",
  )

  assert not hasattr(
    component,
    "to_subgroup",
  )


def test_phase39_5_two_primary_component_remains_plain_primary_component():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  assert type(
    component
  ) is PrimaryComponent

  assert component.prime == 2

  assert not hasattr(
    component,
    "toda_primary_group",
  )


def test_phase39_5_primary_component_has_no_theorem_provenance():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  assert not hasattr(
    component,
    "source",
  )

  assert not hasattr(
    component,
    "theorem",
  )

  assert not hasattr(
    component,
    "provenance",
  )





