from dataclasses import dataclass

from expression import (
  MapSymbol,
  ScalarValue,
)


@dataclass(frozen=True)
class PrimaryComponent:
  group_dimension: ScalarValue
  sphere_dimension: ScalarValue
  prime: int


@dataclass(frozen=True)
class TodaPrimaryGroup:
  group_dimension: ScalarValue
  sphere_dimension: ScalarValue


@dataclass(frozen=True)
class PreimageSubgroup:
  map: MapSymbol
  subgroup: PrimaryComponent



