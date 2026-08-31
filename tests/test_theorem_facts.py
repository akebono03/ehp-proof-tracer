from expression import (
  HomotopyElement,
  Suspension,
  TodaBracket,
  eta,
  nu,
)
from proof import LiteratureReference
from theorem_facts import (
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



