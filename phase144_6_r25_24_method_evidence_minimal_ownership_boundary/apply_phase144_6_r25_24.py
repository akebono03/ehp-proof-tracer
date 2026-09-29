from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METHOD_PATH = (
  ROOT
  / "toda_group_proof_narrative_method_evidence.py"
)
MULTI_PATH = (
  ROOT
  / "toda_group_proof_narrative_argument_multi_renderer.py"
)
METHOD_SOURCE = (
  Path(__file__).resolve().parent
  / "toda_group_proof_narrative_method_evidence.py"
)


def main() -> int:
  if not METHOD_PATH.exists():
    raise RuntimeError(
      "Missing production file: "
      "toda_group_proof_narrative_method_evidence.py"
    )

  if not MULTI_PATH.exists():
    raise RuntimeError(
      "Missing production file: "
      "toda_group_proof_narrative_argument_multi_renderer.py"
    )

  current_method = METHOD_PATH.read_text(
    encoding="utf-8",
  )
  if "minimal_ownership" in current_method:
    raise RuntimeError(
      "minimal_ownership already exists; "
      "refusing to apply twice."
    )

  METHOD_PATH.write_text(
    METHOD_SOURCE.read_text(
      encoding="utf-8",
    ),
    encoding="utf-8",
  )

  current_multi = MULTI_PATH.read_text(
    encoding="utf-8",
  )

  old_call = """      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
"""
  new_call = """      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
        minimal_ownership=True,
      )
"""

  if current_multi.count(
    old_call
  ) != 1:
    raise RuntimeError(
      "Expected exactly one multi-renderer "
      "method-evidence call."
    )

  current_multi = current_multi.replace(
    old_call,
    new_call,
    1,
  )

  old_filter = """    local_body_blocks = tuple(
      block
      for block in blocks
      if (
        id(
          block
        ) in local_body_block_ids
        or id(
          block
        ) in evidence_block_ids
      )
    )
"""
  new_filter = """    local_body_blocks = tuple(
      block
      for block in blocks
      if (
        (
          block.role
          is not TodaGroupProofNarrativeMathematicalBlockRole
          .EXACTNESS
          and id(
            block
          ) in local_body_block_ids
        )
        or id(
          block
        ) in evidence_block_ids
      )
    )
"""

  if current_multi.count(
    old_filter
  ) != 1:
    raise RuntimeError(
      "Expected exactly one local-body/evidence "
      "union filter."
    )

  current_multi = current_multi.replace(
    old_filter,
    new_filter,
    1,
  )

  MULTI_PATH.write_text(
    current_multi,
    encoding="utf-8",
  )

  print(
    "R25-24 production repair applied."
  )
  print(
    "Changed: "
    "toda_group_proof_narrative_method_evidence.py"
  )
  print(
    "Changed: "
    "toda_group_proof_narrative_argument_multi_renderer.py"
  )
  print(
    "Legacy method-evidence default remains recursive."
  )
  print(
    "Generic multi renderer uses minimal exactness ownership."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
