from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = (
  ROOT
  / "toda_group_proof_generic_narrative_renderer.py"
)

NEW_FUNCTION = 'def _normalize_generic_narrative_statement_latex(\n  statement,\n  latex: str,\n) -> str:\n  if not isinstance(\n    latex,\n    str,\n  ):\n    raise TypeError(\n      "latex must be a str"\n    )\n\n  if not hasattr(\n    statement,\n    "lhs",\n  ):\n    return (\n      _normalize_generic_eta_family_latex(\n        latex\n      )\n    )\n\n  if not hasattr(\n    statement,\n    "rhs",\n  ):\n    return (\n      _normalize_generic_eta_family_latex(\n        latex\n      )\n    )\n\n  replacements = []\n  search_start = 0\n\n  for expression in (\n    statement.lhs,\n    statement.rhs,\n  ):\n    rendered_expression = (\n      _try_render_generic_narrative_expression_latex(\n        expression\n      )\n    )\n\n    if rendered_expression is None:\n      continue\n\n    normalized_expression = (\n      _render_generic_narrative_expression_latex(\n        expression\n      )\n    )\n\n    expression_start = latex.find(\n      rendered_expression,\n      search_start,\n    )\n\n    if expression_start < 0:\n      continue\n\n    expression_end = (\n      expression_start\n      + len(\n        rendered_expression\n      )\n    )\n    search_start = expression_end\n\n    if (\n      normalized_expression\n      == rendered_expression\n    ):\n      continue\n\n    replacements.append(\n      (\n        expression_start,\n        expression_end,\n        normalized_expression,\n      )\n    )\n\n  normalized = latex\n\n  for (\n    expression_start,\n    expression_end,\n    normalized_expression,\n  ) in reversed(\n    replacements\n  ):\n    normalized = (\n      normalized[\n        :expression_start\n      ]\n      + normalized_expression\n      + normalized[\n        expression_end:\n      ]\n    )\n\n  return normalized\n'


def function_range(
  source: str,
  function_name: str,
) -> tuple[
  int,
  int,
]:
  tree = ast.parse(
    source
  )
  lines = source.splitlines(
    keepends=True
  )

  for node in tree.body:
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name == function_name
    ):
      start = sum(
        len(
          line
        )
        for line in lines[
          :node.lineno - 1
        ]
      )
      end = sum(
        len(
          line
        )
        for line in lines[
          :node.end_lineno
        ]
      )

      return (
        start,
        end,
      )

  raise RuntimeError(
    "function not found: "
    + function_name
  )


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  start, end = function_range(
    source,
    function_name,
  )

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n\n"
    + source[
      end:
    ].lstrip(
      "\n"
    )
  )


def main() -> int:
  if not TARGET.exists():
    raise RuntimeError(
      "missing expected file: "
      + str(
        TARGET
      )
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase158_r5_5b_repair1h_backup_"
      + timestamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TARGET,
    backup_dir
    / TARGET.name,
  )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  current_start, current_end = function_range(
    source,
    "_normalize_generic_narrative_statement_latex",
  )
  current_function = source[
    current_start:
    current_end
  ].rstrip()

  if current_function == NEW_FUNCTION.rstrip():
    status = "already applied"
    updated = source
  else:
    updated = replace_function(
      source,
      "_normalize_generic_narrative_statement_latex",
      NEW_FUNCTION,
    )
    ast.parse(
      updated
    )
    TARGET.write_text(
      updated,
      encoding="utf-8",
      newline="\n",
    )
    status = "applied now"

  print(
    "Phase 158-R5-5b repair1h applied."
  )
  print(
    "Backup: "
    + str(
      backup_dir
    )
  )
  print(
    "Independent relation-side normalization: "
    + status
  )
  print(
    "Import changes: none"
  )
  print(
    "Numbering function changes: none"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
