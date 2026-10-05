from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MULTI_RENDERER = (
  ROOT
  / "toda_group_proof_narrative_argument_multi_renderer.py"
)
R5_TEST = (
  ROOT
  / "tests"
  / "test_phase158_r5_5b_public_generic_order_route.py"
)


OLD_MERGE = '''    local_body_block_ids = {
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
'''

NEW_MERGE = '''    local_body_block_ids = {
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
    missing_evidence_blocks = tuple(
      block
      for block in blocks
      if (
        id(
          block
        ) in evidence_block_ids
        and id(
          block
        ) not in local_body_block_ids
      )
    )

    if missing_evidence_blocks:
      conclusion_position = next(
        (
          index
          for index, block in enumerate(
            local_body_blocks
          )
          if block is argument.conclusion_block
        ),
        len(
          local_body_blocks
        ),
      )
      local_body_blocks = (
        local_body_blocks[
          :conclusion_position
        ]
        + missing_evidence_blocks
        + local_body_blocks[
          conclusion_position:
        ]
      )
'''


NEW_WEB_TEXT = '''def _web_text(
  n: int,
  k: int,
) -> str:
  view = build_standard_web_group_proof_view(
    n,
    k,
    max_depth=2,
    mode="narrative",
  )
  parts = []
  in_proof = False

  for line in view.rendered_lines:
    if (
      line.kind == "heading"
      and line.prefix == "証明"
    ):
      in_proof = True
      continue

    if not in_proof:
      continue

    if line.segments:
      parts.append(
        "".join(
          segment.value
          for segment in line.segments
        )
      )
    else:
      parts.append(
        line.prefix
        + (
          ""
          if line.statement_latex is None
          else line.statement_latex
        )
        + line.suffix
      )

  return "\n".join(
    parts
  )
'''


def replace_top_level_function(
  text: str,
  function_name: str,
  replacement: str,
) -> str:
  marker = (
    "def "
    + function_name
    + "("
  )
  start = text.find(
    marker
  )

  if start < 0:
    raise RuntimeError(
      "function not found: "
      + function_name
    )

  next_start = text.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_start < 0:
    end = len(
      text
    )
  else:
    end = next_start + 1

  return (
    text[
      :start
    ]
    + replacement.rstrip()
    + "\n\n"
    + text[
      end:
    ].lstrip(
      "\n"
    )
  )


def main() -> int:
  for path in (
    MULTI_RENDERER,
    R5_TEST,
  ):
    if not path.exists():
      raise RuntimeError(
        "missing expected file: "
        + str(
          path
        )
      )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase158_r5_5b_repair1a_backup_"
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
  shutil.copy2(
    R5_TEST,
    backup_dir
    / R5_TEST.name,
  )

  renderer_text = MULTI_RENDERER.read_text(
    encoding="utf-8"
  )

  if NEW_MERGE in renderer_text:
    production_status = (
      "already applied"
    )
  elif OLD_MERGE in renderer_text:
    renderer_text = renderer_text.replace(
      OLD_MERGE,
      NEW_MERGE,
      1,
    )
    MULTI_RENDERER.write_text(
      renderer_text,
      encoding="utf-8",
      newline="\n",
    )
    production_status = (
      "applied now"
    )
  else:
    raise RuntimeError(
      "Neither old nor new local-body merge "
      "was found in production renderer."
    )

  test_text = R5_TEST.read_text(
    encoding="utf-8"
  )
  test_text = replace_top_level_function(
    test_text,
    "_web_text",
    NEW_WEB_TEXT,
  )
  R5_TEST.write_text(
    test_text,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 158-R5-5b repair1a applied."
  )
  print(
    "Backup: "
    + str(
      backup_dir
    )
  )
  print(
    "Production local-body ordering repair: "
    + production_status
  )
  print(
    "Test helper _web_text: replaced by function boundary"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
