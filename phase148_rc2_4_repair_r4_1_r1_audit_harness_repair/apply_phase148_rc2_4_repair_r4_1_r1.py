from pathlib import Path


TARGET = Path(
  "phase148_rc2_4_repair_r4_1_numbered_equation_dependency_audit"
) / "audit_phase148_rc2_4_repair_r4_1.py"


OLD_IMPORT = """from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
"""

NEW_IMPORT = """from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
"""


OLD_FUNCTION = """def _argument_locations(
  arguments,
  blocks,
  proof_step,
):
  result = []

  for index, argument in enumerate(
    arguments
  ):
    local_block_indexes = tuple(
      block_index
      for block_index, block in enumerate(
        blocks
      )
      if (
        block in argument.body_blocks
        and proof_step in block.steps
      )
    )
    if local_block_indexes:
      result.append(
        (
          index,
          argument.role.value,
          local_block_indexes,
        )
      )

  return tuple(
    result
  )
"""

NEW_FUNCTION = """def _argument_locations(
  presentation,
  sidecar,
  arguments,
  blocks,
  proof_step,
):
  result = []

  for index, argument in enumerate(
    arguments
  ):
    model_support_indexes = tuple(
      block_index
      for block_index, block in enumerate(
        blocks
      )
      if (
        block in argument.supporting_blocks
        and proof_step in block.steps
      )
    )
    conclusion_indexes = tuple(
      block_index
      for block_index, block in enumerate(
        blocks
      )
      if (
        block is argument.conclusion_block
        and proof_step in block.steps
      )
    )
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        index,
      )
    )
    local_body_indexes = tuple(
      block_index
      for block_index, block in enumerate(
        blocks
      )
      if (
        block in local_body_blocks
        and proof_step in block.steps
      )
    )

    if (
      model_support_indexes
      or conclusion_indexes
      or local_body_indexes
    ):
      result.append(
        (
          index,
          argument.role.value,
          {
            "supporting": model_support_indexes,
            "conclusion": conclusion_indexes,
            "local_body": local_body_indexes,
          },
        )
      )

  return tuple(
    result
  )
"""


OLD_CALL = """          _argument_locations(
            complete[
              "arguments"
            ],
            complete[
              "blocks"
            ],
            proof_step,
          )
"""

NEW_CALL = """          _argument_locations(
            complete[
              "closure"
            ],
            complete[
              "sidecar"
            ],
            complete[
              "arguments"
            ],
            complete[
              "blocks"
            ],
            proof_step,
          )
"""


def main() -> int:
  text = TARGET.read_text(
    encoding="utf-8"
  )

  if NEW_FUNCTION in text:
    print(
      "R4.1-R1 audit harness repair already applied."
    )
    return 0

  if text.count(
    OLD_IMPORT
  ) != 1:
    raise RuntimeError(
      "Expected exactly one multi-renderer import block."
    )

  if text.count(
    OLD_FUNCTION
  ) != 1:
    raise RuntimeError(
      "Expected exactly one stale _argument_locations function."
    )

  if text.count(
    OLD_CALL
  ) != 1:
    raise RuntimeError(
      "Expected exactly one stale _argument_locations call."
    )

  text = text.replace(
    OLD_IMPORT,
    NEW_IMPORT,
    1,
  )
  text = text.replace(
    OLD_FUNCTION,
    NEW_FUNCTION,
    1,
  )
  text = text.replace(
    OLD_CALL,
    NEW_CALL,
    1,
  )

  TARGET.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "R4.1-R1 audit harness repair applied."
  )
  print(
    "Production changes: none."
  )
  print(
    "Argument ownership now reports supporting / "
    "conclusion / renderer local_body separately."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
