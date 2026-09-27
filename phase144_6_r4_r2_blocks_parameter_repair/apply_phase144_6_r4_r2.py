from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"


def main() -> int:
  source = TARGET.read_text(encoding="utf-8-sig")

  old_signature = """def _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
  presentation: TodaGroupProofPresentation,
  local_body_blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  argument: TodaGroupProofNarrativeArgument,
) -> frozenset[
  int
]:
"""
  new_signature = """def _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  local_body_blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  argument: TodaGroupProofNarrativeArgument,
) -> frozenset[
  int
]:
"""

  signature_count = source.count(old_signature)

  if signature_count != 1:
    raise RuntimeError(
      "expected exactly one R4 frontier helper signature; "
      f"found {signature_count}"
    )

  source = source.replace(
    old_signature,
    new_signature,
    1,
  )

  old_call = """      _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        local_body_blocks,
        argument,
      )
"""
  new_call = """      _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        blocks,
        local_body_blocks,
        argument,
      )
"""

  call_count = source.count(old_call)

  if call_count != 1:
    raise RuntimeError(
      "expected exactly one R4 frontier helper call; "
      f"found {call_count}"
    )

  source = source.replace(
    old_call,
    new_call,
    1,
  )

  ast.parse(source)

  TARGET.write_text(
    source,
    encoding="utf-8",
  )

  print(
    "Phase 144-6-R4-R2 blocks-parameter repair applied."
  )
  print(
    "Changed only: "
    "toda_group_proof_narrative_argument_multi_renderer.py"
  )
  print(
    "Repair: complete blocks are now passed explicitly "
    "into the frontier visibility helper."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
