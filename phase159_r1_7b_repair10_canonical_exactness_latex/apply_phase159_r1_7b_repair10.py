from __future__ import annotations

import ast
from pathlib import Path
import shutil


ROOT = Path.cwd()
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
BACKUP_DIR = ROOT / "phase159_r1_7b_repair10_backup_before_apply"

NEW_FUNCTION = 'def _phase159_r1_7b_exactness_step_latex(\n  proof_step: ProofStep,\n) -> str | None:\n  statement = proof_step.conclusion\n\n  if not isinstance(\n    statement,\n    TodaProp42ExactnessStatement,\n  ):\n    return None\n\n  rendered = (\n    render_toda_proof_statement_latex(\n      statement\n    )\n  )\n\n  if rendered is None:\n    return None\n\n  suffix = (\n    r" \\text{ is exact}"\n  )\n\n  if not rendered.endswith(\n    suffix\n  ):\n    return None\n\n  return rendered[\n    :-len(\n      suffix\n    )\n  ]\n'


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  tree = ast.parse(
    source
  )

  target = next(
    (
      node
      for node in tree.body
      if (
        isinstance(
          node,
          ast.FunctionDef,
        )
        and node.name
        == function_name
      )
    ),
    None,
  )

  if target is None:
    raise RuntimeError(
      f"function not found: {function_name}"
    )

  if target.end_lineno is None:
    raise RuntimeError(
      f"function has no end line: {function_name}"
    )

  lines = source.splitlines(
    keepends=True
  )

  start = target.lineno - 1
  end = target.end_lineno

  return "".join(
    (
      *lines[:start],
      replacement.rstrip()
      + "\n\n",
      *lines[end:],
    )
  )


def main() -> int:
  if not RENDERER.exists():
    raise RuntimeError(
      f"missing renderer: {RENDERER}"
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    RENDERER,
    BACKUP_DIR / RENDERER.name,
  )

  source = RENDERER.read_text(
    encoding="utf-8-sig"
  )

  updated = replace_function(
    source,
    "_phase159_r1_7b_exactness_step_latex",
    NEW_FUNCTION,
  )

  ast.parse(
    updated
  )

  RENDERER.write_text(
    updated,
    encoding="utf-8",
  )

  print(
    "Phase 159-R1-7b repair10 applied."
  )
  print(
    "Production file: "
    "toda_group_proof_narrative_renderer.py"
  )
  print(
    "Changed function: "
    "_phase159_r1_7b_exactness_step_latex"
  )
  print(
    "Canonical exactness LaTeX renderer reused."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
