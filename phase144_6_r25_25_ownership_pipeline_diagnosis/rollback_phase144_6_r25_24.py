from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
METHOD_PATH = (
  ROOT
  / "toda_group_proof_narrative_method_evidence.py"
)
MULTI_PATH = (
  ROOT
  / "toda_group_proof_narrative_argument_multi_renderer.py"
)


def main() -> int:
  current_method = METHOD_PATH.read_text(
    encoding="utf-8",
  )

  if "minimal_ownership" in current_method:
    METHOD_PATH.write_text(
      (
        HERE
        / "toda_group_proof_narrative_method_evidence_r25_23.py"
      ).read_text(
        encoding="utf-8",
      ),
      encoding="utf-8",
    )
    print(
      "Rolled back R25-24 method-evidence experiment."
    )
  else:
    print(
      "Method-evidence file is already pre-R25-24."
    )

  current_multi = MULTI_PATH.read_text(
    encoding="utf-8",
  )

  r25_24_call = """        argument_index,
        minimal_ownership=True,
      )
"""
  original_call = """        argument_index,
      )
"""

  if r25_24_call in current_multi:
    current_multi = current_multi.replace(
      r25_24_call,
      original_call,
      1,
    )

  r25_24_filter = """    local_body_blocks = tuple(
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
  original_filter = """    local_body_blocks = tuple(
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

  if r25_24_filter in current_multi:
    current_multi = current_multi.replace(
      r25_24_filter,
      original_filter,
      1,
    )

  MULTI_PATH.write_text(
    current_multi,
    encoding="utf-8",
  )

  verify_method = METHOD_PATH.read_text(
    encoding="utf-8",
  )
  verify_multi = MULTI_PATH.read_text(
    encoding="utf-8",
  )

  if "minimal_ownership" in verify_method:
    raise RuntimeError(
      "R25-24 method-evidence experiment remains."
    )

  if "minimal_ownership=True" in verify_multi:
    raise RuntimeError(
      "R25-24 renderer experiment remains."
    )

  print(
    "R25-24 production experiment rollback complete."
  )
  print(
    "No new production behavior was added."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
