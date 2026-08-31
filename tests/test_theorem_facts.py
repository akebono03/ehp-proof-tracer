from expression import (
  HomotopyElement,
  Suspension,
  TodaBracket,
  eta,
  nu,
)
from theorem_facts import (
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

  repository = TheoremFactRepository(
    entries=(
      theorem,
    ),
  )

  assert repository.entries == (
    theorem,
  )

  assert repository.entries[0] is theorem


