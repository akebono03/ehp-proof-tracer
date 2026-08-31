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
  index: int | ScalarSymbol | None = None


@dataclass(frozen=True)
class IndexedTodaBracketData:
  bracket: TodaBracket
  second_base: Expression
  third_base: Expression
  suspension_exponent: int | ScalarSymbol

  def is_consistent(self) -> bool:
    return (
      self.bracket.second
      == IteratedSuspension(
        expression=self.second_base,
        exponent=self.suspension_exponent,
      )
      and self.bracket.third
      == IteratedSuspension(
        expression=self.third_base,
        exponent=self.suspension_exponent,
      )
      and self.bracket.index
      == self.suspension_exponent
    )


@dataclass(frozen=True)
class Zero(Expression):
  pass


@dataclass(frozen=True)
class HomotopyElement(Expression):
  name: str
  dimension: int
  source: int | None = None
  target: int | None = None


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

  @property
  def source(self) -> int | None:
    if isinstance(
      self.expression,
      HomotopyElement,
    ):
      if self.expression.source is None:
        return None
      return self.expression.source + 1

    if isinstance(
      self.expression,
      Suspension,
    ):
      if self.expression.source is None:
        return None
      return self.expression.source + 1

    return None

  @property
  def target(self) -> int | None:
    if isinstance(
      self.expression,
      HomotopyElement,
    ):
      if self.expression.target is None:
        return None
      return self.expression.target + 1

    if isinstance(
      self.expression,
      Suspension,
    ):
      if self.expression.target is None:
        return None
      return self.expression.target + 1

    return None


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



