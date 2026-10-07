from pathlib import Path
import sys
import time


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TESTS_DIR = REPO_ROOT / "tests"

for path in (
  REPO_ROOT,
  TESTS_DIR,
):
  if str(path) not in sys.path:
    sys.path.insert(
      0,
      str(path),
    )


from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_contribution_ordering import (
  _build_visibility_occurrences,
  _necessity_for_chain,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)


def _elapsed(start):
  return time.perf_counter() - start


def main():
  print("=" * 78)
  print("Phase 159 - repair3c fix1 performance audit")
  print("Cross-group contribution selection decomposition")
  print("=" * 78)
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print()

  for n, k in TARGETS:
    print("-" * 78)
    print(
      f"TARGET n={n} k={k} pi_{n+k}^{n}"
    )

    start = time.perf_counter()
    context = _context(
      n,
      k,
    )
    print(
      f"context_seconds={_elapsed(start):.3f}"
    )

    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      _aggregate_semantic_sidecar,
      proof_chains,
    ) = context

    print(
      f"nodes={len(presentation.nodes)} "
      f"blocks={len(blocks)} "
      f"arguments={len(arguments)}"
    )

    total_chain_steps = 0
    total_necessary_pairs = 0

    for argument_index, argument in enumerate(
      arguments
    ):
      conclusion_step = (
        extract_toda_group_proof_narrative_argument_conclusion_step(
          argument
        )
      )

      if conclusion_step is None:
        print(
          f"argument={argument_index} "
          f"role={argument.role.value} conclusion=None"
        )
        continue

      local_body = (
        extract_toda_group_proof_narrative_argument_local_body_blocks(
          presentation,
          blocks,
          semantic_sidecar,
          arguments,
          argument_index,
        )
      )

      start = time.perf_counter()
      (
        chain_ids,
        anchors,
        _distances,
        necessity,
      ) = _necessity_for_chain(
        presentation,
        local_body,
        proof_chains[
          argument_index
        ],
        conclusion_step,
      )
      seconds = _elapsed(
        start
      )

      necessary_pairs = sum(
        len(
          anchor_ids
        )
        for anchor_ids in necessity.values()
      )
      total_chain_steps += len(
        chain_ids
      )
      total_necessary_pairs += necessary_pairs

      print(
        f"argument={argument_index} "
        f"role={argument.role.value} "
        f"local_blocks={len(local_body)} "
        f"providers={len(proof_chains[argument_index].providers)} "
        f"anchors={len(anchors)} "
        f"chain={len(chain_ids)} "
        f"necessity_pairs={necessary_pairs} "
        f"necessity_seconds={seconds:.3f}"
      )

    print(
      f"target_total_chain_steps={total_chain_steps} "
      f"target_total_necessity_pairs={total_necessary_pairs}"
    )

    start = time.perf_counter()
    occurrences = (
      _build_visibility_occurrences(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        proof_chains,
      )
    )
    print(
      f"visibility_occurrences={len(occurrences)} "
      f"visibility_seconds={_elapsed(start):.3f}"
    )

    start = time.perf_counter()
    ordered = (
      build_toda_group_proof_narrative_ordered_contributions(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        proof_chains,
      )
    )
    print(
      f"ordered_rows={sum(len(rows) for rows in ordered)} "
      f"ordered_seconds={_elapsed(start):.3f}"
    )

  print()
  print("=" * 78)
  print("repair3c fix1 performance audit complete")
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print("=" * 78)


if __name__ == "__main__":
  main()
