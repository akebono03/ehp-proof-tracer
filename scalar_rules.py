from dataclasses import dataclass

from expression import ScalarSymbol


@dataclass(frozen=True)
class OddScalarStatement:
  scalar: ScalarSymbol


@dataclass(frozen=True)
class EvenScalarStatement:
  scalar: ScalarSymbol


@dataclass(frozen=True)
class ScalarCongruenceStatement:
  scalar: ScalarSymbol
  residue: int
  modulus: int




