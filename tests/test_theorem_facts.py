from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
  TodaBracket,
  eta,
  nu,
)
from proof import LiteratureReference
from theorem_facts import (
  EPSILON_3_TODA_MEMBERSHIP_FACT,
  THEOREM_FACT_REPOSITORY,
  TheoremFactEntry,
  TheoremFactRepository,
)
from toda_rules import (
  TodaBracketMembershipTheoremStatement,
)


def test_phase24_theorem_fact_repository_is_empty_by_default():
  repository = TheoremFactRepository()

  assert repository.entries == ()


def test_phase24_theorem_fact_repository_preserves_toda_theorem_entry():
  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  theorem = (
    TodaBracketMembershipTheoremStatement(
      element=epsilon_3,
      bracket=TodaBracket(
        first=eta(3),
        second=Suspension(
          nu_prime,
        ),
        third=nu(7),
        index=1,
      ),
    )
  )

  reference = LiteratureReference(
    label="Toda",
  )

  entry = TheoremFactEntry(
    statement=theorem,
    reference=reference,
  )

  repository = TheoremFactRepository(
    entries=(
      entry,
    ),
  )

  assert repository.entries == (
    entry,
  )

  assert repository.entries[0].statement is theorem
  assert repository.entries[0].reference is reference


def test_phase24_2_theorem_fact_entry_preserves_literature_reference():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Chapter VI",
  )

  epsilon_3 = HomotopyElement(
    name="ε",
    dimension=3,
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
  )

  theorem = (
    TodaBracketMembershipTheoremStatement(
      element=epsilon_3,
      bracket=TodaBracket(
        first=eta(3),
        second=Suspension(
          nu_prime,
        ),
        third=nu(7),
        index=1,
      ),
    )
  )

  entry = TheoremFactEntry(
    statement=theorem,
    reference=reference,
  )

  assert entry.statement == theorem
  assert entry.reference == reference
  assert entry.reference.label == "Toda"
  assert entry.reference.author == "H. Toda"

  assert entry.reference.title == (
    "Composition Methods in "
    "Homotopy Groups of Spheres"
  )

  assert entry.reference.year == 1962
  assert entry.reference.locator == "Chapter VI"


def test_phase24_3_registers_epsilon_3_toda_membership_fact():
  entry = EPSILON_3_TODA_MEMBERSHIP_FACT
  theorem = entry.statement

  assert THEOREM_FACT_REPOSITORY.entries == (
    EPSILON_3_TODA_MEMBERSHIP_FACT,
  )

  assert entry.reference == LiteratureReference(
    label="Toda",
  )

  assert theorem.element == HomotopyElement(
    name="ε₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="ε",
      index=3,
    ),
  )

  assert theorem.bracket == TodaBracket(
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
  )


def test_phase24_4_repository_lookup_returns_matching_entry():
  result = THEOREM_FACT_REPOSITORY.lookup(
    EPSILON_3_TODA_MEMBERSHIP_FACT.statement,
  )

  assert result is EPSILON_3_TODA_MEMBERSHIP_FACT


def test_phase24_4_repository_lookup_returns_none_for_unknown_fact():
  theorem = EPSILON_3_TODA_MEMBERSHIP_FACT.statement

  unknown_theorem = TodaBracketMembershipTheoremStatement(
    element=theorem.element,
    bracket=TodaBracket(
      first=theorem.bracket.first,
      second=theorem.bracket.second,
      third=theorem.bracket.third,
      index=2,
    ),
  )

  result = THEOREM_FACT_REPOSITORY.lookup(
    unknown_theorem,
  )

  assert result is None






