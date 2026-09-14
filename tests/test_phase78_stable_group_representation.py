from typing import (
  get_type_hints,
)

from homotopy_groups import (
  HomotopyGroup,
  PrimaryComponent,
  StableHomotopyGroup,
  StablePrimaryComponent,
  TodaPrimaryGroup,
)


def test_phase78_4_stable_homotopy_group_represents_stem():
  group = StableHomotopyGroup(
    stem=0,
  )

  assert group.stem == 0


def test_phase78_4_stable_homotopy_group_stem_is_concrete_integer():
  type_hints = get_type_hints(
    StableHomotopyGroup
  )

  assert type_hints[
    "stem"
  ] is int


def test_phase78_4_stable_primary_component_preserves_group_and_prime():
  group = StableHomotopyGroup(
    stem=7,
  )

  component = StablePrimaryComponent(
    group=group,
    prime=2,
  )

  assert component.group is group
  assert component.prime == 2


def test_phase78_4_stable_primary_component_type_hints_are_explicit():
  type_hints = get_type_hints(
    StablePrimaryComponent
  )

  assert (
    type_hints[
      "group"
    ]
    is StableHomotopyGroup
  )

  assert type_hints[
    "prime"
  ] is int


def test_phase78_4_g0_does_not_require_primary_component():
  group = StableHomotopyGroup(
    stem=0,
  )

  assert not hasattr(
    group,
    "prime",
  )

  assert not isinstance(
    group,
    StablePrimaryComponent,
  )


def test_phase78_4_g7_two_primary_component_is_representable():
  component = StablePrimaryComponent(
    group=StableHomotopyGroup(
      stem=7,
    ),
    prime=2,
  )

  assert component == StablePrimaryComponent(
    group=StableHomotopyGroup(
      stem=7,
    ),
    prime=2,
  )


def test_phase78_4_stable_group_is_distinct_from_ordinary_homotopy_group():
  stable_group = StableHomotopyGroup(
    stem=7,
  )

  ordinary_group = HomotopyGroup(
    group_dimension=16,
    sphere_dimension=9,
  )

  assert not isinstance(
    stable_group,
    HomotopyGroup,
  )

  assert stable_group != ordinary_group


def test_phase78_4_stable_primary_component_is_distinct_from_unstable_primary_component():
  stable_component = StablePrimaryComponent(
    group=StableHomotopyGroup(
      stem=7,
    ),
    prime=2,
  )

  unstable_component = PrimaryComponent(
    group_dimension=16,
    sphere_dimension=9,
    prime=2,
  )

  assert not isinstance(
    stable_component,
    PrimaryComponent,
  )

  assert (
    stable_component
    != unstable_component
  )


def test_phase78_4_stable_group_is_distinct_from_toda_primary_group():
  stable_group = StableHomotopyGroup(
    stem=7,
  )

  toda_group = TodaPrimaryGroup(
    group_dimension=16,
    sphere_dimension=9,
  )

  assert not isinstance(
    stable_group,
    TodaPrimaryGroup,
  )

  assert stable_group != toda_group


def test_phase78_4_stable_representations_have_no_finite_sphere_dimensions():
  stable_group = StableHomotopyGroup(
    stem=7,
  )

  stable_component = StablePrimaryComponent(
    group=stable_group,
    prime=2,
  )

  for value in (
    stable_group,
    stable_component,
  ):
    assert not hasattr(
      value,
      "group_dimension",
    )

    assert not hasattr(
      value,
      "sphere_dimension",
    )


def test_phase78_4_stable_representations_have_no_theorem_semantics():
  stable_group = StableHomotopyGroup(
    stem=7,
  )

  stable_component = StablePrimaryComponent(
    group=stable_group,
    prime=2,
  )

  for value in (
    stable_group,
    stable_component,
  ):
    assert not hasattr(
      value,
      "theorem",
    )

    assert not hasattr(
      value,
      "source",
    )

    assert not hasattr(
      value,
      "provenance",
    )

    assert not hasattr(
      value,
      "generator",
    )

    assert not hasattr(
      value,
      "order",
    )


