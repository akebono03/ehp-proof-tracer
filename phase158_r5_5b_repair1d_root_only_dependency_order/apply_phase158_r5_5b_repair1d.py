from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MULTI_RENDERER = (
  ROOT
  / "toda_group_proof_narrative_argument_multi_renderer.py"
)

CURRENT_MERGE = '    local_body_block_ids = {\n      id(\n        block\n      )\n      for block in local_body_blocks\n    }\n    evidence_block_ids = {\n      id(\n        block\n      )\n      for block in evidence\n    }\n    missing_evidence_blocks = tuple(\n      block\n      for block in blocks\n      if (\n        id(\n          block\n        ) in evidence_block_ids\n        and id(\n          block\n        ) not in local_body_block_ids\n      )\n    )\n\n    if missing_evidence_blocks:\n      conclusion_position = next(\n        (\n          index\n          for index, block in enumerate(\n            local_body_blocks\n          )\n          if block is argument.conclusion_block\n        ),\n        len(\n          local_body_blocks\n        ),\n      )\n      local_body_blocks = (\n        local_body_blocks[\n          :conclusion_position\n        ]\n        + missing_evidence_blocks\n        + local_body_blocks[\n          conclusion_position:\n        ]\n      )\n'
REFINED_MERGE = '    local_body_block_ids = {\n      id(\n        block\n      )\n      for block in local_body_blocks\n    }\n    evidence_block_ids = {\n      id(\n        block\n      )\n      for block in evidence\n    }\n\n    if (\n      argument.conclusion_block.role\n      is TodaGroupProofNarrativeMathematicalBlockRole\n      .TARGET\n    ):\n      missing_evidence_blocks = tuple(\n        block\n        for block in blocks\n        if (\n          id(\n            block\n          ) in evidence_block_ids\n          and id(\n            block\n          ) not in local_body_block_ids\n        )\n      )\n\n      if missing_evidence_blocks:\n        conclusion_position = next(\n          (\n            index\n            for index, block in enumerate(\n              local_body_blocks\n            )\n            if block is argument.conclusion_block\n          ),\n          len(\n            local_body_blocks\n          ),\n        )\n        local_body_blocks = (\n          local_body_blocks[\n            :conclusion_position\n          ]\n          + missing_evidence_blocks\n          + local_body_blocks[\n            conclusion_position:\n          ]\n        )\n    else:\n      local_body_blocks = tuple(\n        block\n        for block in blocks\n        if (\n          id(\n            block\n          ) in local_body_block_ids\n          or id(\n            block\n          ) in evidence_block_ids\n        )\n      )\n'


def main() -> int:
  if not MULTI_RENDERER.exists():
    raise RuntimeError(
      "missing expected file: "
      + str(
        MULTI_RENDERER
      )
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase158_r5_5b_repair1d_backup_"
      + timestamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    MULTI_RENDERER,
    backup_dir
    / MULTI_RENDERER.name,
  )

  text = MULTI_RENDERER.read_text(
    encoding="utf-8"
  )

  if REFINED_MERGE in text:
    status = "already applied"
  elif CURRENT_MERGE in text:
    text = text.replace(
      CURRENT_MERGE,
      REFINED_MERGE,
      1,
    )
    MULTI_RENDERER.write_text(
      text,
      encoding="utf-8",
      newline="\n",
    )
    status = "applied now"
  else:
    raise RuntimeError(
      "Expected repair1 local-body merge was not found."
    )

  print(
    "Phase 158-R5-5b repair1d applied."
  )
  print(
    "Backup: "
    + str(
      backup_dir
    )
  )
  print(
    "Root-only dependency-order refinement: "
    + status
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
