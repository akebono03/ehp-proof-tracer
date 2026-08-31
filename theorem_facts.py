from dataclasses import (
  dataclass,
  replace,
)

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
  TodaBracket,
)
from proof import LiteratureReference
from toda_rules import (
  TodaBracketMembershipTheoremStatement,
  toda_bracket_membership_theorem_proof_step,
)


@dataclass(frozen=True)
class TheoremFactEntry:
  statement: TodaBracketMembershipTheoremStatement
  reference: LiteratureReference

  def materialize_statement(
    self,
  ) -> TodaBracketMembershipTheoremStatement:
    return replace(
      self.statement,
      source=self.reference,
    )

  def to_proof_step(
    self,
  ):
    return toda_bracket_membership_theorem_proof_step(
      self.materialize_statement()
    )


@dataclass(frozen=True)
class TheoremFactRepository:
  entries: tuple[
    TheoremFactEntry,
    ...
  ] = ()

  def lookup(
    self,
    statement: TodaBracketMembershipTheoremStatement,
  ) -> TheoremFactEntry | None:
    for entry in self.entries:
      if entry.statement == statement:
        return entry

    return None


EPSILON_3_TODA_MEMBERSHIP_FACT = TheoremFactEntry(
  statement=TodaBracketMembershipTheoremStatement(
    element=HomotopyElement(
      name="ε₃",
      dimension=3,
      generator=GeneratorSymbol(
        family="ε",
        index=3,
      ),
    ),
    bracket=TodaBracket(
      first=HomotopyElement(
        name="η₃",
        dimension=3,
        generator=GeneratorSymbol(
          family="η",
          index=3,
        ),
      ),
      second=Suspension(
        HomotopyElement(
          name="ν′",
          dimension=3,
          generator=GeneratorSymbol(
            family="ν",
            decoration="′",
          ),
        ),
      ),
      third=HomotopyElement(
        name="ν₇",
        dimension=7,
        generator=GeneratorSymbol(
          family="ν",
          index=7,
        ),
      ),
      index=1,
    ),
  ),
  reference=LiteratureReference(
    label="Toda",
  ),
)


THEOREM_FACT_REPOSITORY = TheoremFactRepository(
  entries=(
    EPSILON_3_TODA_MEMBERSHIP_FACT,
  ),
)


