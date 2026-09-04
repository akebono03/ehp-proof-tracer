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
from probes.probe_phase41_capabilities import (
  build_phase41_representative_preimages,
  preimage_subgroup_text,
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


def test_phase41_4_preimage_subgroup_map_type_remains_map_symbol():
  type_hints = get_type_hints(
    PreimageSubgroup
  )

  assert type_hints[
    "map"
  ] is MapSymbol


def test_phase41_4_preimage_subgroup_target_type_remains_primary_component():
  type_hints = get_type_hints(
    PreimageSubgroup
  )

  assert type_hints[
    "subgroup"
  ] is PrimaryComponent


def test_phase41_4_preimage_subgroup_accepts_symbolic_critical_degree_target():
  n = ScalarSymbol(
    name="n",
  )

  target = PrimaryComponent(
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

  preimage = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=target,
  )

  assert preimage.map is SUSPENSION_MAP

  assert preimage.subgroup == PrimaryComponent(
    group_dimension=ScalarProduct(
      left=2,
      right=ScalarSymbol(
        name="n",
      ),
    ),
    sphere_dimension=ScalarSum(
      left=ScalarSymbol(
        name="n",
      ),
      right=1,
    ),
    prime=2,
  )


def test_phase41_4_preimage_subgroup_preserves_compound_dimensions_structurally():
  n = ScalarSymbol(
    name="n",
  )

  group_dimension = ScalarProduct(
    left=2,
    right=n,
  )

  sphere_dimension = ScalarSum(
    left=n,
    right=1,
  )

  preimage = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=PrimaryComponent(
      group_dimension=group_dimension,
      sphere_dimension=sphere_dimension,
      prime=2,
    ),
  )

  assert preimage.subgroup.group_dimension is (
    group_dimension
  )

  assert preimage.subgroup.sphere_dimension is (
    sphere_dimension
  )

  assert preimage.subgroup.group_dimension != ScalarSymbol(
    name="2n",
  )

  assert preimage.subgroup.sphere_dimension != ScalarSymbol(
    name="n+1",
  )


def test_phase41_4_preimage_subgroup_preserves_primary_component_prime():
  preimage = PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=PrimaryComponent(
      group_dimension=10,
      sphere_dimension=6,
      prime=2,
    ),
  )

  assert preimage.subgroup.prime == 2


def test_phase41_4_preimage_subgroup_map_representation_is_not_limited_to_suspension():
  map_symbol = MapSymbol(
    name="f",
  )

  target = PrimaryComponent(
    group_dimension=10,
    sphere_dimension=6,
    prime=2,
  )

  preimage = PreimageSubgroup(
    map=map_symbol,
    subgroup=target,
  )

  assert preimage.map is map_symbol
  assert preimage.subgroup is target


def test_phase41_5_preimage_subgroup_is_not_membership_statement():
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
    MembershipStatement,
  )


def test_phase41_5_preimage_subgroup_has_no_membership_element():
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
    "member",
  )


def test_phase41_5_preimage_subgroup_has_no_membership_theorem_semantics():
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
    "contains",
  )

  assert not hasattr(
    preimage,
    "membership_rule",
  )

  assert not hasattr(
    preimage,
    "membership_equivalence",
  )


def test_phase41_5_preimage_subgroup_has_no_toda_evaluated_definition():
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
    "definition",
  )

  assert not hasattr(
    preimage,
    "evaluated_definition",
  )

  assert not hasattr(
    preimage,
    "toda_definition",
  )


def test_phase41_5_preimage_subgroup_has_no_toda_primary_group_conversion():
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
    "toda_primary_group",
  )

  assert not hasattr(
    preimage,
    "to_toda_primary_group",
  )


def test_phase41_5_toda_primary_group_has_no_preimage_conversion():
  toda_group = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  assert not hasattr(
    toda_group,
    "preimage",
  )

  assert not hasattr(
    toda_group,
    "preimage_subgroup",
  )

  assert not hasattr(
    toda_group,
    "to_preimage_subgroup",
  )


def test_phase41_5_preimage_subgroup_has_no_theorem_provenance():
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


def test_phase41_6_representative_builder_constructs_concrete_preimage():
  result = (
    build_phase41_representative_preimages()
  )

  assert result[
    "concrete_preimage"
  ] == PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=PrimaryComponent(
      group_dimension=10,
      sphere_dimension=6,
      prime=2,
    ),
  )


def test_phase41_6_representative_builder_constructs_symbolic_preimage():
  result = (
    build_phase41_representative_preimages()
  )

  n = ScalarSymbol(
    name="n",
  )

  assert result[
    "symbolic_preimage"
  ] == PreimageSubgroup(
    map=SUSPENSION_MAP,
    subgroup=PrimaryComponent(
      group_dimension=ScalarProduct(
        left=2,
        right=n,
      ),
      sphere_dimension=ScalarSum(
        left=n,
        right=1,
      ),
      prime=2,
    ),
  )


def test_phase41_6_preimage_subgroup_text_displays_representative_notation():
  result = (
    build_phase41_representative_preimages()
  )

  assert preimage_subgroup_text(
    result[
      "concrete_preimage"
    ]
  ) == "E^-1(π_10(S^6;2))"

  assert preimage_subgroup_text(
    result[
      "symbolic_preimage"
    ]
  ) == "E^-1(π_2n(S^n+1;2))"


def test_phase41_6_representative_builder_preserves_phase41_boundary():
  result = (
    build_phase41_representative_preimages()
  )

  preimage = result[
    "concrete_preimage"
  ]

  toda_group = result[
    "critical_toda_group"
  ]

  assert not isinstance(
    preimage,
    Subgroup,
  )

  assert not isinstance(
    preimage,
    ImageSubgroupReference,
  )

  assert not isinstance(
    preimage,
    KernelSubgroupReference,
  )

  assert not hasattr(
    preimage,
    "element",
  )

  assert not hasattr(
    preimage,
    "membership_equivalence",
  )

  assert not hasattr(
    preimage,
    "provenance",
  )

  assert not hasattr(
    toda_group,
    "to_preimage_subgroup",
  )

  assert not hasattr(
    toda_group,
    "evaluated_definition",
  )



