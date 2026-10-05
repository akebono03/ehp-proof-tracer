from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)

NEW_IMPORT = 'from toda_group_proof_generic_narrative_renderer import (\n  _generic_short_exact_sequence_latex,\n  _generic_short_exact_sequence_reason_prose,\n  _render_generic_narrative_step,\n)\n'
NEW_FUNCTION = 'def suppress_toda_group_proof_narrative_reflexive_equalities(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  reflexive_keys = set()\n\n  for node in presentation.nodes:\n    statement = node.proof_step.conclusion\n\n    if (\n      not isinstance(\n        statement,\n        Relation,\n      )\n      or statement.relation_type\n      is not RelationType.EQUALITY\n    ):\n      continue\n\n    try:\n      rendered = (\n        _render_generic_narrative_step(\n          node.proof_step\n        )\n      )\n    except (\n      TypeError,\n      ValueError,\n    ):\n      continue\n\n    if (\n      not rendered.startswith(\n        "$"\n      )\n      or not rendered.endswith(\n        "$"\n      )\n    ):\n      continue\n\n    equation = rendered[\n      1:-1\n    ]\n    separator = " = "\n\n    if separator not in equation:\n      continue\n\n    lhs_rendered, rhs_rendered = equation.split(\n      separator,\n      1,\n    )\n\n    if (\n      lhs_rendered\n      != rhs_rendered\n    ):\n      continue\n\n    reflexive_keys.add(\n      _phase157_r11_reference_statement_match_key(\n        rendered\n      )\n    )\n\n  if not reflexive_keys:\n    return markdown\n\n  retained = []\n\n  for paragraph in markdown.split(\n    "\\n\\n"\n  ):\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]より, "\n      )\n\n      if marker_end >= 0:\n        stripped = stripped[\n          marker_end\n          + len(\n            "]より, "\n          ):\n        ]\n\n    key = (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n    if key in reflexive_keys:\n      continue\n\n    retained.append(\n      paragraph\n    )\n\n  return "\\n\\n".join(\n    retained\n  )\n'


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


def replace_generic_renderer_import(
  source: str,
) -> str:
  start_marker = (
    "from toda_group_proof_generic_narrative_renderer import (\n"
  )
  start = source.find(
    start_marker
  )

  if start < 0:
    raise RuntimeError(
      "generic narrative renderer import not found"
    )

  end = source.find(
    ")\n",
    start,
  )

  if end < 0:
    raise RuntimeError(
      "generic narrative renderer import end not found"
    )

  end += 2

  return (
    source[
      :start
    ]
    + NEW_IMPORT
    + source[
      end:
    ]
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
      "phase158_r5_5b_repair1o_backup_"
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

  updated = replace_generic_renderer_import(
    source
  )
  updated = replace_function(
    updated,
    "suppress_toda_group_proof_narrative_reflexive_equalities",
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

  print(
    "Phase 158-R5-5b repair1o applied."
  )
  print(
    "Backup: "
    + str(
      backup_dir
    )
  )
  print(
    "Changed production file: "
    + TARGET.name
  )
  print(
    "Changed function: "
    "suppress_toda_group_proof_narrative_reflexive_equalities"
  )
  print(
    "Removed unused imports: "
    "_normalize_generic_eta_family_latex, "
    "_render_generic_narrative_expression_latex"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
