from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = (
  ROOT
  / "toda_group_proof_narrative_argument_body_renderer.py"
)

NEW_IMPORT = 'from toda_group_proof_generic_narrative_renderer import (\n  _generic_narrative_dependency_labels,\n  _generic_narrative_sentence_lead,\n  _generic_short_exact_sequence_reason_prose,\n  _render_generic_narrative_proof_block,\n  _render_generic_narrative_step,\n)\n'
NEW_HELPER = 'def _is_toda_group_proof_narrative_rendered_reflexive_equality_step(\n  proof_step: ProofStep,\n) -> bool:\n  if not isinstance(\n    proof_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "proof_step must be a ProofStep"\n    )\n\n  statement = proof_step.conclusion\n\n  if (\n    not isinstance(\n      statement,\n      Relation,\n    )\n    or statement.relation_type\n    is not RelationType.EQUALITY\n  ):\n    return False\n\n  try:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n  except (\n    TypeError,\n    ValueError,\n  ):\n    return False\n\n  if (\n    not rendered.startswith(\n      "$"\n    )\n    or not rendered.endswith(\n      "$"\n    )\n  ):\n    return False\n\n  equation = rendered[\n    1:-1\n  ]\n  separator = " = "\n\n  if separator not in equation:\n    return False\n\n  lhs_rendered, rhs_rendered = equation.split(\n    separator,\n    1,\n  )\n\n  return (\n    lhs_rendered\n    == rhs_rendered\n  )\n'


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
      "generic renderer import block not found"
    )

  end = source.find(
    ")\n",
    start,
  )

  if end < 0:
    raise RuntimeError(
      "generic renderer import block end not found"
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
      "phase158_r5_5b_repair1j_backup_"
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
    "_is_toda_group_proof_narrative_rendered_reflexive_equality_step",
    NEW_HELPER,
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
    "Phase 158-R5-5b repair1j applied."
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
    "Changed helper: "
    "_is_toda_group_proof_narrative_rendered_reflexive_equality_step"
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
