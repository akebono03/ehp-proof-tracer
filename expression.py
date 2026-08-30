from dataclasses import dataclass


class Expression:
  pass


@dataclass(frozen=True)
class MapSymbol:
  name: str


@dataclass(frozen=True)
class ScalarSymbol:
  name: str


@dataclass(frozen=True)
class TodaBracket:
  first: Expression
  second: Expression
  third: Expression
  index: int | None = None


@dataclass(frozen=True)
class IndexedTodaBracketData:
  bracket: TodaBracket
  second_base: Expression
  third_base: Expression
  suspension_exponent: int


@dataclass(frozen=True)
class Zero(Expression):
  pass


@dataclass(frozen=True)
class HomotopyElement(Expression):
  name: str
  dimension: int


@dataclass(frozen=True)
class Multiple(Expression):
  coefficient: int | ScalarSymbol
  expression: Expression


@dataclass(frozen=True)
class Sum(Expression):
  left: Expression
  right: Expression


@dataclass(frozen=True)
class Composition(Expression):
  left: Expression
  right: Expression


@dataclass(frozen=True)
class MapApplication(Expression):
  map: MapSymbol
  expression: Expression


@dataclass(frozen=True)
class Suspension(Expression):
  expression: Expression


@dataclass(frozen=True)
class IteratedSuspension(Expression):
  expression: Expression
  exponent: int | ScalarSymbol


def eta(n: int) -> HomotopyElement:
  return HomotopyElement("η", n)


def nu(n: int) -> HomotopyElement:
  return HomotopyElement("ν", n)


def sigma(n: int) -> HomotopyElement:
  return HomotopyElement("σ", n)



