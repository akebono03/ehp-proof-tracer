from dataclasses import dataclass

from expression import (
  Expression,
  MapSymbol,
  ScalarValue,
)


@dataclass(frozen=True)
class PrimaryComponent:
  group_dimension: ScalarValue
  sphere_dimension: ScalarValue
  prime: int


@dataclass(frozen=True)
class PrimaryComponentMembershipStatement:
  element: Expression
  component: PrimaryComponent


@dataclass(frozen=True)
class TodaPrimaryGroup:
  group_dimension: ScalarValue
  sphere_dimension: ScalarValue


@dataclass(frozen=True)
class PreimageSubgroup:
  map: MapSymbol
  subgroup: PrimaryComponent


@dataclass(frozen=True)
class FreeCyclicGroup:
  generator: Expression


@dataclass(frozen=True)
class DirectSumGroup:
  summands: tuple[
    FreeCyclicGroup | PrimaryComponent,
    ...
  ]





