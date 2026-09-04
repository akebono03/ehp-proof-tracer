from typing import (
  get_args,
  get_type_hints,
)

from algebra import (
  GroupMap,
  Subgroup,
)
from expression import (
  MapSymbol,
)
from homomorphism_rules import (
  SUSPENSION_MAP,
)
from homotopy_groups import (
  PrimaryComponent,
)
from set_rules import (
  ImageSubgroupReference,
  KernelSubgroupReference,
  MembershipStatement,
  SubgroupTerm,
)


def test_phase41_1_current_subgroup_term_contains_expected_existing_terms():
  assert set(
    get_args(
      SubgroupTerm
    )
  ) == {
    Subgroup,
    ImageSubgroupReference,
    KernelSubgroupReference,
  }


def test_phase41_1_current_membership_statement_uses_subgroup_term():
  type_hints = get_type_hints(
    MembershipStatement
  )

  assert type_hints[
    "subgroup"
  ] == SubgroupTerm


def test_phase41_1_image_subgroup_reference_uses_group_map():
  type_hints = get_type_hints(
    ImageSubgroupReference
  )

  assert type_hints[
    "group_map"
  ] is GroupMap


def test_phase41_1_kernel_subgroup_reference_uses_group_map():
  type_hints = get_type_hints(
    KernelSubgroupReference
  )

  assert type_hints[
    "group_map"
  ] is GroupMap


def test_phase41_1_proof_expression_map_identity_is_distinct_from_group_map():
  assert isinstance(
    SUSPENSION_MAP,
    MapSymbol,
  )

  assert SUSPENSION_MAP == MapSymbol(
    name="E",
  )

  assert not isinstance(
    SUSPENSION_MAP,
    GroupMap,
  )


def test_phase41_1_primary_component_is_not_current_subgroup_term():
  component = PrimaryComponent(
    group_dimension=10,
    sphere_dimension=6,
    prime=2,
  )

  assert not isinstance(
    component,
    (
      Subgroup,
      ImageSubgroupReference,
      KernelSubgroupReference,
    ),
  )


def test_phase41_1_primary_component_can_represent_critical_degree_target():
  component = PrimaryComponent(
    group_dimension=10,
    sphere_dimension=6,
    prime=2,
  )

  assert component.group_dimension == 10
  assert component.sphere_dimension == 6
  assert component.prime == 2


def test_phase41_1_preimage_subgroup_is_not_yet_part_of_current_subgroup_term():
  assert all(
    term.__name__ != "PreimageSubgroup"
    for term in get_args(
      SubgroupTerm
    )
  )



