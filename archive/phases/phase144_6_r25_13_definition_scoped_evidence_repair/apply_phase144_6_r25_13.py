from pathlib import Path

PATH = Path("toda_group_proof_narrative_argument_multi_renderer.py")

OLD = """    local_body_block_ids = {
      id(
        block
      )
      for block in local_body_blocks
    }
    evidence_block_ids = {
      id(
        block
      )
      for block in evidence
    }
    local_body_blocks = tuple(
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

NEW = """    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    ):
      local_body_block_ids = {
        id(
          block
        )
        for block in local_body_blocks
      }
      evidence_block_ids = {
        id(
          block
        )
        for block in evidence
      }
      local_body_blocks = tuple(
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

text = PATH.read_text(encoding="utf-8-sig")

count = text.count(OLD)
if count != 1:
    raise SystemExit(
        "Expected exactly one current evidence-union block, "
        f"found {count}. No production file was changed."
    )

PATH.write_text(
    text.replace(OLD, NEW, 1),
    encoding="utf-8",
)

print("R25-13 production repair applied.")
print("Changed only: toda_group_proof_narrative_argument_multi_renderer.py")
print("Evidence expansion is now restricted to ESTABLISH_DEFINITION.")
