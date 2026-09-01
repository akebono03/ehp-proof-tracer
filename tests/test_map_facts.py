from expression import MapSymbol
from map_facts import (
  HOPF_MAP,
  HOPF_MAP_TYPING_FACT,
  MapTypingFact,
)


def test_phase29_1_hopf_map_is_map_symbol():
  assert isinstance(
    HOPF_MAP,
    MapSymbol,
  )


def test_phase29_1_hopf_map_has_expected_name():
  assert HOPF_MAP.name == "H"


def test_phase29_1_hopf_map_matches_structural_h_identity():
  assert HOPF_MAP == MapSymbol(
    name="H",
  )


def test_phase29_1_hopf_map_does_not_equal_different_map():
  assert HOPF_MAP != MapSymbol(
    name="E",
  )


def test_phase29_2_map_typing_fact_preserves_map():
  h = MapSymbol(
    name="H",
  )

  fact = MapTypingFact(
    map=h,
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert fact.map == h


def test_phase29_2_map_typing_fact_preserves_domain_dimensions():
  fact = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert fact.source_group_dimension == 3
  assert fact.source_sphere_dimension == 2


def test_phase29_2_map_typing_fact_preserves_codomain_dimensions():
  fact = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert fact.target_group_dimension == 3
  assert fact.target_sphere_dimension == 3


def test_phase29_2_map_typing_fact_has_structural_equality():
  left = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  right = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert left == right


def test_phase29_2_map_identity_is_part_of_typing_fact_identity():
  h_fact = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  f_fact = MapTypingFact(
    map=MapSymbol(
      name="f",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert h_fact != f_fact


def test_phase29_2_source_group_dimension_is_structural():
  original = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  different = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=4,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert original != different


def test_phase29_2_source_sphere_dimension_is_structural():
  original = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  different = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=3,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert original != different


def test_phase29_2_target_group_dimension_is_structural():
  original = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  different = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=4,
    target_sphere_dimension=3,
  )

  assert original != different


def test_phase29_2_target_sphere_dimension_is_structural():
  original = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  different = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=4,
  )

  assert original != different


def test_phase29_2_map_symbol_does_not_contain_typing_implicitly():
  h = MapSymbol(
    name="H",
  )

  fact = MapTypingFact(
    map=h,
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert fact.map == h
  assert not hasattr(
    h,
    "source_group_dimension",
  )
  assert not hasattr(
    h,
    "source_sphere_dimension",
  )
  assert not hasattr(
    h,
    "target_group_dimension",
  )
  assert not hasattr(
    h,
    "target_sphere_dimension",
  )


def test_phase29_3_hopf_map_typing_fact_is_map_typing_fact():
  assert isinstance(
    HOPF_MAP_TYPING_FACT,
    MapTypingFact,
  )


def test_phase29_3_hopf_map_typing_fact_uses_production_hopf_map():
  assert HOPF_MAP_TYPING_FACT.map is (
    HOPF_MAP
  )


def test_phase29_3_hopf_map_typing_fact_has_expected_domain():
  assert (
    HOPF_MAP_TYPING_FACT
    .source_group_dimension
    == 3
  )

  assert (
    HOPF_MAP_TYPING_FACT
    .source_sphere_dimension
    == 2
  )


def test_phase29_3_hopf_map_typing_fact_has_expected_codomain():
  assert (
    HOPF_MAP_TYPING_FACT
    .target_group_dimension
    == 3
  )

  assert (
    HOPF_MAP_TYPING_FACT
    .target_sphere_dimension
    == 3
  )


def test_phase29_3_hopf_map_typing_fact_has_expected_structure():
  expected = MapTypingFact(
    map=HOPF_MAP,
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert HOPF_MAP_TYPING_FACT == (
    expected
  )


def test_phase29_3_hopf_map_typing_fact_does_not_change_map_symbol():
  assert HOPF_MAP == MapSymbol(
    name="H",
  )

  assert not hasattr(
    HOPF_MAP,
    "source_group_dimension",
  )

  assert not hasattr(
    HOPF_MAP,
    "source_sphere_dimension",
  )

  assert not hasattr(
    HOPF_MAP,
    "target_group_dimension",
  )

  assert not hasattr(
    HOPF_MAP,
    "target_sphere_dimension",
  )





