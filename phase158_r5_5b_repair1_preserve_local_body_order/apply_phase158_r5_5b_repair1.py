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


OLD_WEB_TEXT = '''def _web_text(
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

  for line in view.rendered_lines:
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


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      label
      + ": expected exactly one match, found "
      + str(
        count
      )
    )

  return text.replace(
    old,
    new,
    1,
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
      "phase158_r5_5b_repair1_backup_"
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
  renderer_text = replace_once(
    renderer_text,
    OLD_MERGE,
    NEW_MERGE,
    "local body/evidence merge",
  )
  MULTI_RENDERER.write_text(
    renderer_text,
    encoding="utf-8",
    newline="\n",
  )

  test_text = R5_TEST.read_text(
    encoding="utf-8"
  )
  test_text = replace_once(
    test_text,
    OLD_WEB_TEXT,
    NEW_WEB_TEXT,
    "Web proof-body helper",
  )
  R5_TEST.write_text(
    test_text,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 158-R5-5b repair1 applied."
  )
  print(
    "Backup: "
    + str(
      backup_dir
    )
  )
  print(
    "Changed production function:"
  )
  print(
    "  render_toda_group_proof_narrative_multi_argument_markdown"
  )
  print(
    "Changed focused test helper:"
  )
  print(
    "  _web_text"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
