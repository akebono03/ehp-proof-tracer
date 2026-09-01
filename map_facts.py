from dataclasses import dataclass

from expression import MapSymbol


@dataclass(frozen=True)
class MapTypingFact:
  map: MapSymbol
  source_group_dimension: int
  source_sphere_dimension: int
  target_group_dimension: int
  target_sphere_dimension: int


HOPF_MAP = MapSymbol(
  name="H",
)


HOPF_MAP_TYPING_FACT = MapTypingFact(
  map=HOPF_MAP,
  source_group_dimension=3,
  source_sphere_dimension=2,
  target_group_dimension=3,
  target_sphere_dimension=3,
)




