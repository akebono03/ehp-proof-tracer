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
class TodaIteratedSuspensionMap:
  exponent: ScalarValue
  source_group: TodaPrimaryGroup
  target_group: TodaPrimaryGroup


@dataclass(frozen=True)
class TodaEHPSequence:
  terms: tuple[
    TodaPrimaryGroup,
    ...
  ]
  maps: tuple[
    MapSymbol,
    ...
  ]

  def __post_init__(
    self,
  ) -> None:
    if len(
      self.terms
    ) != len(
      self.maps
    ) + 1:
      raise ValueError(
        "TodaEHPSequence requires "
        "exactly one more term than maps"
      )


@dataclass(frozen=True)
class TodaEHPExactnessWindow:
  source_term: TodaPrimaryGroup
  middle_term: TodaPrimaryGroup
  target_term: TodaPrimaryGroup
  first_map: MapSymbol
  second_map: MapSymbol


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
    FreeCyclicGroup
    | PrimaryComponent
    | TodaPrimaryGroup,
    ...
  ]


@dataclass(frozen=True)
class TodaProp44DecompositionMap:
  source_group: DirectSumGroup
  target_group: TodaPrimaryGroup
  alpha: Expression
  beta: Expression
  gamma: Expression
  formula: Expression



