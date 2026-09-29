from collections import Counter

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
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


def main():
  report = build_standard_toda_report(
    n=3,
    k=3,
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

  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
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
    "Phase 141-8 block role audit: pi_6^3"
  )
  print(
    "=" * 60
  )

  for index, block in enumerate(
    blocks,
    start=1,
  ):
    types = ", ".join(
      type(
        step.conclusion
      ).__name__
      for step in block.steps
    )

    print(
      f"[{index:02d}] "
      f"{block.role.value}: "
      f"{types}"
    )

  print(
    "=" * 60
  )

  for role, count in sorted(
    counts.items()
  ):
    print(
      f"{role}: {count}"
    )

  print(
    "OTHER blocks: "
    f"{counts.get('other', 0)}"
  )


if __name__ == "__main__":
  main()
