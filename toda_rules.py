from dataclasses import dataclass

from expression import (
  Expression,
  TodaBracket,
)


@dataclass(frozen=True)
class TodaBracketMembershipStatement:
  element: Expression
  bracket: TodaBracket



