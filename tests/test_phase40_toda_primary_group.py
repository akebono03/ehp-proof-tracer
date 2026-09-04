from typing import (
  get_type_hints,
)

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  HomotopyElement,
  ScalarSymbol,
  ScalarValue,
)
from homotopy_groups import (
  PrimaryComponent,
  TodaPrimaryGroup,
)


def test_phase40_1_primary_component_uses_existing_scalar_value_dimensions():
  type_hints = get_type_hints(
    PrimaryComponent
  )

  assert type_hints[
    "group_dimension"
  ] == ScalarValue

  assert type_hints[
    "sphere_dimension"
  ] == ScalarValue


def test_phase40_1_homotopy_group_membership_uses_same_scalar_value_dimensions():
  type_hints = get_type_hints(
    HomotopyGroupMembershipStatement
  )

  assert type_hints[
    "group_dimension"
  ] == ScalarValue

  assert type_hints[
    "sphere_dimension"
  ] == ScalarValue


def test_phase40_1_primary_component_and_homotopy_group_membership_share_concrete_dimensions():
  component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  membership = HomotopyGroupMembershipStatement(
    element=HomotopyElement(
      name="a",
      dimension=3,
    ),
    group_dimension=8,
    sphere_dimension=5,
  )

  assert component.group_dimension == (
    membership.group_dimension
  )

  assert component.sphere_dimension == (
    membership.sphere_dimension
  )


def test_phase40_1_primary_component_and_homotopy_group_membership_share_symbolic_dimensions():
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

  membership = HomotopyGroupMembershipStatement(
    element=HomotopyElement(
      name="a",
      dimension=1,
    ),
    group_dimension=i,
    sphere_dimension=n,
  )

  assert component.group_dimension is i
  assert component.sphere_dimension is n

  assert membership.group_dimension is i
  assert membership.sphere_dimension is n


def test_phase40_2_toda_primary_group_represents_concrete_group():
  group = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=5,
  )

  assert group.group_dimension == 8
  assert group.sphere_dimension == 5


def test_phase40_2_toda_primary_group_supports_symbolic_dimensions():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=n,
  )

  assert group.group_dimension is i
  assert group.sphere_dimension is n


def test_phase40_2_toda_primary_group_structural_equality_uses_both_dimensions():
  first = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=5,
  )

  same = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=5,
  )

  different_group_dimension = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  different_sphere_dimension = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=6,
  )

  assert first == same
  assert first != different_group_dimension
  assert first != different_sphere_dimension


def test_phase40_3_toda_primary_group_is_distinct_from_primary_component():
  toda_group = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=5,
  )

  primary_component = PrimaryComponent(
    group_dimension=8,
    sphere_dimension=5,
    prime=2,
  )

  assert not isinstance(
    toda_group,
    PrimaryComponent,
  )

  assert toda_group != primary_component


def test_phase40_3_toda_primary_group_is_distinct_from_homotopy_group_membership():
  toda_group = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=5,
  )

  membership = HomotopyGroupMembershipStatement(
    element=HomotopyElement(
      name="a",
      dimension=3,
    ),
    group_dimension=8,
    sphere_dimension=5,
  )

  assert not isinstance(
    toda_group,
    HomotopyGroupMembershipStatement,
  )

  assert toda_group != membership


def test_phase40_3_toda_primary_group_has_no_prime_field():
  group = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=5,
  )

  assert not hasattr(
    group,
    "prime",
  )


def test_phase40_3_toda_primary_group_has_no_membership_element():
  group = TodaPrimaryGroup(
    group_dimension=8,
    sphere_dimension=5,
  )

  assert not hasattr(
    group,
    "element",
  )





