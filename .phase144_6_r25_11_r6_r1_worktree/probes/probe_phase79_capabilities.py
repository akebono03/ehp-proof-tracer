import sys
from pathlib import Path


TESTS_DIR = (
  Path(__file__)
  .resolve()
  .parents[1]
  / "tests"
)

if str(TESTS_DIR) not in sys.path:
  sys.path.insert(
    0,
    str(TESTS_DIR),
  )

from test_phase79_cross_phase_repository import (
  build_phase79_7_data,
)


def build_phase79_representative_result():
  data = build_phase79_7_data()
  repository = data[
    "repository"
  ]

  phase76_entry = data[
    "phase76_entry"
  ]
  phase77_entry = data[
    "phase77_entry"
  ]
  phase78_entry = data[
    "phase78_entry"
  ]

  return {
    "data": data,
    "phase76_by_phase": (
      repository.find_by_phase(
        "76"
      )
      == (
        phase76_entry,
      )
    ),
    "phase77_by_theorem": (
      repository.find_by_theorem(
        "Toda Lemma 5.16"
      )
      == (
        phase77_entry,
      )
    ),
    "phase78_by_conclusion": (
      repository.find_by_conclusion(
        phase78_entry.step.conclusion
      )
      == (
        phase78_entry,
      )
    ),
    "identity_preserved": all(
      repository.get(
        entry.key
      ).step
      is entry.step
      for entry in (
        phase76_entry,
        phase77_entry,
        phase78_entry,
      )
    ),
    "phase76_dependency_count": len(
      repository.dependencies(
        phase76_entry
      )
    ),
    "phase77_dependency_count": len(
      repository.dependencies(
        phase77_entry
      )
    ),
    "phase78_dependency_count": len(
      repository.dependencies(
        phase78_entry
      )
    ),
  }


def _heading(
  title,
):
  print()
  print(
    "=" * 72
  )
  print(
    title
  )
  print(
    "=" * 72
  )
  print()


def main():
  result = (
    build_phase79_representative_result()
  )

  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 79 cross-phase Proof Repository "
    "capability demonstration"
  )

  _heading(
    "Registered representative proofs"
  )

  print(
    "Phase 76: Toda Equation (5.16)"
  )
  print(
    "Phase 77: Toda Lemma 5.16"
  )
  print(
    "Phase 78: Stable G_0 through G_7 integration"
  )

  _heading(
    "Cross-phase lookup"
  )

  print(
    "Phase 76 lookup by phase = "
    f"{result['phase76_by_phase']}"
  )
  print(
    "Phase 77 lookup by theorem = "
    f"{result['phase77_by_theorem']}"
  )
  print(
    "Phase 78 lookup by conclusion = "
    f"{result['phase78_by_conclusion']}"
  )
  print(
    "original ProofStep identity preserved = "
    f"{result['identity_preserved']}"
  )

  _heading(
    "Direct dependencies"
  )

  print(
    "Phase 76 direct dependencies = "
    f"{result['phase76_dependency_count']}"
  )
  print(
    "Phase 77 direct dependencies = "
    f"{result['phase77_dependency_count']}"
  )
  print(
    "Phase 78 direct dependencies = "
    f"{result['phase78_dependency_count']}"
  )

  _heading(
    "Phase 79 repository boundary"
  )

  print(
    "The repository registers existing ProofStep objects."
  )
  print(
    "It does not copy or normalize proof graphs."
  )
  print(
    "Unregistered premise nodes remain available through "
    "ProofStep.premises."
  )
  print(
    "No builder auto-execution was added."
  )
  print(
    "No automatic inference was added."
  )
  print(
    "Persistence remains disabled."
  )


if __name__ == "__main__":
  main()


