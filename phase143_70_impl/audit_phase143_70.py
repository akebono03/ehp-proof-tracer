from toda_group_proof_narrative_provenance_catalog import (
  TODA_GROUP_PROOF_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES,
)
from toda_rules import (
  TodaProp51FiniteDimensionalStatement,
  TodaProp53FiniteDimensionalStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaProp59FiniteDimensionalStatement,
)


def main():
  expected = (
    TodaProp51FiniteDimensionalStatement,
    TodaProp53FiniteDimensionalStatement,
    TodaProp56FiniteDimensionalStatement,
    TodaProp59FiniteDimensionalStatement,
  )

  print("=" * 78)
  print("Phase 143-70 provenance-only residual audit")
  print("=" * 78)

  for statement_type in expected:
    print(
      f"{statement_type.__name__}: "
      f"{statement_type in TODA_GROUP_PROOF_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES}"
    )


if __name__ == "__main__":
  main()
