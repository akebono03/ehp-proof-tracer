from expression import MapSymbol
from map_facts import HOPF_MAP


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




