from collections import Counter

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_evidence_contributions import (
  build_toda_group_proof_narrative_evidence_contribution_sidecar,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def main():
  total = Counter()

  print("=" * 78)
  print("Phase 144-6-R5-15M typed evidence-contribution metadata prototype")
  print("=" * 78)

  for n, k in TARGETS:
    report = build_standard_toda_report(
      n=n,
      k=k,
    )
    group_result = (
      report.candidates[
        0
      ].source_candidate.group_result
    )
    replay = (
      build_toda_group_result_proof_replay(
        group_result,
        max_depth=None,
      )
    )
    presentation = (
      build_toda_group_proof_presentation(
        replay
      )
    )
    semantic_sidecar = (
      build_toda_group_proof_narrative_semantic_sidecar(
        presentation
      )
    )
    blocks = (
      build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=semantic_sidecar,
      )
    )
    contribution_sidecar = (
      build_toda_group_proof_narrative_evidence_contribution_sidecar(
        presentation,
        blocks,
      )
    )

    counts = Counter(
      semantic.contribution.value
      for semantic in contribution_sidecar.edge_semantics
    )
    total.update(
      counts
    )

    print(f"target=({n}, {k}) edges={len(presentation.edges)}")
    for name, count in sorted(
      counts.items()
    ):
      print(f"  {name:<24} {count:5d}")

  print()
  print("TOTAL")
  print("-" * 78)
  for name, count in sorted(
    total.items()
  ):
    print(f"{name:<24} {count:5d}")

  resolved = sum(
    count
    for name, count in total.items()
    if name != "unresolved"
  )
  unresolved = total[
    "unresolved"
  ]
  all_edges = resolved + unresolved

  print()
  print(f"all_edges={all_edges}")
  print(f"resolved_edges={resolved}")
  print(f"unresolved_edges={unresolved}")
  if all_edges:
    print(
      "resolved_ratio="
      f"{resolved / all_edges:.6f}"
    )

  print()
  print("INTERPRETATION")
  print("1. Metadata is stored at premise-edge granularity in the Narrative semantic layer.")
  print("2. Existing ProofStep, InferenceRule, TodaProofEdge, and production renderer are unchanged.")
  print("3. Generic mathematical block roles and RelationType drive the first prototype.")
  print("4. OTHER statements remain UNRESOLVED instead of being guessed from rule names.")
  print("5. This prototype does not decide Narrative visibility.")
  print("6. The next audit should compare these typed annotations with the 15K visible/support ownership population.")


if __name__ == "__main__":
  main()
