from typing import (
  get_type_hints,
)

import homotopy_groups
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


def test_phase40_1_toda_primary_group_is_not_yet_implemented():
  assert not hasattr(
    homotopy_groups,
    "TodaPrimaryGroup",
  )




