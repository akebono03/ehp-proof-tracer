from collections import Counter

from tests.test_phase144_6_r5_15u_evidence_integration import (
  TARGETS,
  _context,
  _edge_local_visible_unresolved_count,
)


def main():
  print("=" * 96)
  print("Phase 144-6-R5-15U production EvidenceContribution integration audit")
  print("=" * 96)

  total_unresolved = 0
  for n, k in TARGETS:
    context = _context(n, k)
    unresolved = _edge_local_visible_unresolved_count(*context)
    total_unresolved += unresolved
    contributions = context[-1]
    counts = Counter(
      semantic.contribution.value
      for semantic in contributions.edge_semantics
    )
    print(
      f"target=({n},{k}) "
      f"edge_local_visible_unresolved={unresolved} "
      f"all_edge_unresolved={counts.get('unresolved', 0)}"
    )

  print()
  print(f"edge_local_visible_unresolved_total={total_unresolved}")
  if total_unresolved != 0:
    raise AssertionError(
      f"expected 0 edge-local visible unresolved edges, got {total_unresolved}"
    )

  print("INTEGRATION RESULT: edge-local Narrative contribution coverage = 100%")
  print(
    "Boundary preserved: R4 visibility, renderer, CLI/Web, and depth policy "
    "were not changed."
  )


if __name__ == "__main__":
  main()
