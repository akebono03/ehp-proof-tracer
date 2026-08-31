from dataclasses import dataclass

from proof import LiteratureReference
from toda_rules import (
  TodaBracketMembershipTheoremStatement,
)


@dataclass(frozen=True)
class TheoremFactEntry:
  statement: TodaBracketMembershipTheoremStatement
  reference: LiteratureReference


@dataclass(frozen=True)
class TheoremFactRepository:
  entries: tuple[
    TheoremFactEntry,
    ...
  ] = ()



