from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
R5_TEST = (
  ROOT
  / "tests"
  / "test_phase158_r5_5b_public_generic_order_route.py"
)

NEW_WEB_TEXT = 'def _web_text(\n  n: int,\n  k: int,\n) -> str:\n  view = build_standard_web_group_proof_view(\n    n,\n    k,\n    max_depth=2,\n    mode="narrative",\n  )\n  parts = []\n  in_proof = False\n\n  for line in view.rendered_lines:\n    if (\n      line.kind == "heading"\n      and line.prefix == "証明"\n    ):\n      in_proof = True\n      continue\n\n    if not in_proof:\n      continue\n\n    if line.segments:\n      parts.append(\n        "".join(\n          segment.value\n          for segment in line.segments\n        )\n      )\n    else:\n      parts.append(\n        line.prefix\n        + (\n          ""\n          if line.statement_latex is None\n          else line.statement_latex\n        )\n        + line.suffix\n      )\n\n  return "\\n".join(\n    parts\n  )\n'


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
  if not R5_TEST.exists():
    raise RuntimeError(
      "missing expected file: "
      + str(
        R5_TEST
      )
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase158_r5_5b_repair1b_backup_"
      + timestamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    R5_TEST,
    backup_dir
    / R5_TEST.name,
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
    "Phase 158-R5-5b repair1b applied."
  )
  print(
    "Backup: "
    + str(
      backup_dir
    )
  )
  print(
    "Production code changes: none"
  )
  print(
    "Repaired test helper: _web_text"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
