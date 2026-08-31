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

  def are_defining_compositions_type_compatible(
    self,
  ) -> bool:
    first_composition = Composition(
      left=self.first,
      right=self.second,
    )

    second_composition = Composition(
      left=self.second,
      right=self.third,
    )

    return (
      first_composition.is_type_compatible()
      and second_composition.is_type_compatible()
    )


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

  def is_type_compatible(self) -> bool:
    if not isinstance(
      self.left,
      (
        HomotopyElement,
        Suspension,
        IteratedSuspension,
      ),
    ):
      return False

    if not isinstance(
      self.right,
      (
        HomotopyElement,
        Suspension,
        IteratedSuspension,
      ),
    ):
      return False

    if self.left.source is None:
      return False

    if self.right.target is None:
      return False

    return self.left.source == self.right.target


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

  @property
  def source(self) -> int | None:
    if not isinstance(
      self.exponent,
      int,
    ):
      return None

    if self.exponent < 0:
      return None

    if isinstance(
      self.expression,
      HomotopyElement,
    ):
      if self.expression.source is None:
        return None
      return self.expression.source + self.exponent

    if isinstance(
      self.expression,
      Suspension,
    ):
      if self.expression.source is None:
        return None
      return self.expression.source + self.exponent

    return None

  @property
  def target(self) -> int | None:
    if not isinstance(
      self.exponent,
      int,
    ):
      return None

    if self.exponent < 0:
      return None

    if isinstance(
      self.expression,
      HomotopyElement,
    ):
      if self.expression.target is None:
        return None
      return self.expression.target + self.exponent

    if isinstance(
      self.expression,
      Suspension,
    ):
      if self.expression.target is None:
        return None
      return self.expression.target + self.exponent

    return None


def eta(n: int) -> HomotopyElement:
  return HomotopyElement("η", n)


def nu(n: int) -> HomotopyElement:
  return HomotopyElement("ν", n)


def sigma(n: int) -> HomotopyElement:
  return HomotopyElement("σ", n)



