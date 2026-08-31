from dataclasses import dataclass

from toda_rules import (
  TodaBracketMembershipTheoremStatement,
)


@dataclass(frozen=True)
class TheoremFactRepository:
  entries: tuple[
    TodaBracketMembershipTheoremStatement,
    ...
  ] = ()




