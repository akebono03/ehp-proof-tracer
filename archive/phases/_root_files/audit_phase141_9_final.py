from collections import Counter
import inspect

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
  recognize_toda_group_proof_narrative_step_role,
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


def _presentation(
  n,
  k,
):
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
      max_depth=3,
    )
  )

  return build_toda_group_proof_presentation(
    replay
  )


def _audit_one(
  label,
  n,
  k,
):
  presentation = _presentation(
    n,
    k,
  )

  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )

  counts = Counter(
    block.role.value
    for block in blocks
  )

  print(
    f"{label}: "
    f"{len(presentation.nodes)} nodes, "
    f"{len(blocks)} blocks"
  )

  print(
    "  roles: "
    + ", ".join(
      f"{role}={count}"
      for role, count in sorted(
        counts.items()
      )
    )
  )

  print(
    "  OTHER blocks: "
    f"{counts.get('other', 0)}"
  )

  block_steps = tuple(
    proof_step
    for block in blocks
    for proof_step in block.steps
  )

  exact_coverage = (
    len(
      block_steps
    )
    == len(
      presentation.nodes
    )
    and len(
      {
        id(
          proof_step
        )
        for proof_step in block_steps
      }
    )
    == len(
      presentation.nodes
    )
  )

  print(
    "  exact node coverage: "
    f"{exact_coverage}"
  )

  print()


def main():
  print(
    "Phase 141-9 final block-layer audit"
  )
  print(
    "=" * 72
  )

  _audit_one(
    "pi_6^3",
    3,
    3,
  )

  _audit_one(
    "pi_8^5",
    5,
    3,
  )

  _audit_one(
    "pi_15^8",
    8,
    7,
  )

  recognizer_source = inspect.getsource(
    recognize_toda_group_proof_narrative_step_role
  )
  builder_source = inspect.getsource(
    build_toda_group_proof_narrative_blocks
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
  )

  print(
    "generic block-layer hardcode audit"
  )

  for fragment in forbidden_fragments:
    found = (
      fragment in recognizer_source
      or fragment in builder_source
    )

    print(
      f"  {fragment!r}: "
      f"{'FOUND' if found else 'not found'}"
    )

  print()
  print(
    "Phase 142 contract:"
  )
  print(
    "  ProofStep graph"
  )
  print(
    "    + narrative semantic sidecar"
  )
  print(
    "    -> mathematical NarrativeBlock sequence"
  )
  print(
    "    -> generic renderer"
  )
  print(
    "  Renderer must not infer new mathematical facts."
  )


if __name__ == "__main__":
  main()
