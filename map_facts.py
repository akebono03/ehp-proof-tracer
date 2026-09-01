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


