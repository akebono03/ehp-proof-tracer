from dataclasses import dataclass

from expression import Expression


@dataclass(frozen=True)
class HopfInvariantStatement:
  expression: Expression
  value: int


