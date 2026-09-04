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
  PreimageSubgroup,
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
  assert PreimageSubgroup not in get_args(
    SubgroupTerm
  )


def test_phase41_2_preimage_subgroup_represents_critical_degree_preimage():
  subgroup = PrimaryComponent(
    group_dimension=10,
    sphere_dimension=6,
    prime=2,
  )

  preimage = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=subgroup,
  )

  assert preimage.map is SUSPENSION_MAP
  assert preimage.subgroup is subgroup


def test_phase41_2_preimage_subgroup_uses_map_symbol():
  type_hints = get_type_hints(
    PreimageSubgroup
  )

  assert type_hints[
    "map"
  ] is MapSymbol


def test_phase41_2_preimage_subgroup_uses_primary_component_target():
  type_hints = get_type_hints(
    PreimageSubgroup
  )

  assert type_hints[
    "subgroup"
  ] is PrimaryComponent


def test_phase41_2_preimage_subgroup_structural_equality_uses_map_and_subgroup():
  subgroup = PrimaryComponent(
    group_dimension=10,
    sphere_dimension=6,
    prime=2,
  )

  same_subgroup = PrimaryComponent(
    group_dimension=10,
    sphere_dimension=6,
    prime=2,
  )

  different_subgroup = PrimaryComponent(
    group_dimension=10,
    sphere_dimension=6,
    prime=3,
  )

  first = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=subgroup,
  )

  same = PreimageSubgroup(
    map=MapSymbol(
      name="E",
    ),
    subgroup=same_subgroup,
  )

  different_map = PreimageSubgroup(
    map=MapSymbol(
      name="H",
    ),
    subgroup=subgroup,
  )

  different_target = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=different_subgroup,
  )

  assert first == same
  assert first != different_map
  assert first != different_target


def test_phase41_2_preimage_subgroup_preserves_target_structurally():
  subgroup = PrimaryComponent(
    group_dimension=10,
    sphere_dimension=6,
    prime=2,
  )

  preimage = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=subgroup,
  )

  assert preimage.subgroup == PrimaryComponent(
    group_dimension=10,
    sphere_dimension=6,
    prime=2,
  )


def test_phase41_2_preimage_subgroup_has_only_minimum_representation_fields():
  preimage = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=PrimaryComponent(
      group_dimension=10,
      sphere_dimension=6,
      prime=2,
    ),
  )

  assert not hasattr(
    preimage,
    "element",
  )

  assert not hasattr(
    preimage,
    "membership",
  )

  assert not hasattr(
    preimage,
    "source",
  )

  assert not hasattr(
    preimage,
    "theorem",
  )

  assert not hasattr(
    preimage,
    "provenance",
  )


def test_phase41_3_preimage_subgroup_is_distinct_from_concrete_subgroup():
  preimage = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=PrimaryComponent(
      group_dimension=10,
      sphere_dimension=6,
      prime=2,
    ),
  )

  assert not isinstance(
    preimage,
    Subgroup,
  )


def test_phase41_3_preimage_subgroup_is_distinct_from_image_subgroup_reference():
  preimage = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=PrimaryComponent(
      group_dimension=10,
      sphere_dimension=6,
      prime=2,
    ),
  )

  assert not isinstance(
    preimage,
    ImageSubgroupReference,
  )


def test_phase41_3_preimage_subgroup_is_distinct_from_kernel_subgroup_reference():
  preimage = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=PrimaryComponent(
      group_dimension=10,
      sphere_dimension=6,
      prime=2,
    ),
  )

  assert not isinstance(
    preimage,
    KernelSubgroupReference,
  )


def test_phase41_3_preimage_subgroup_is_distinct_from_target_primary_component():
  target = PrimaryComponent(
    group_dimension=10,
    sphere_dimension=6,
    prime=2,
  )

  preimage = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=target,
  )

  assert not isinstance(
    preimage,
    PrimaryComponent,
  )

  assert preimage != target


def test_phase41_3_preimage_subgroup_is_not_an_element_preimage_representation():
  preimage = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=PrimaryComponent(
      group_dimension=10,
      sphere_dimension=6,
      prime=2,
    ),
  )

  assert not hasattr(
    preimage,
    "element",
  )

  assert not hasattr(
    preimage,
    "preimage_element",
  )

  assert not hasattr(
    preimage,
    "value",
  )






