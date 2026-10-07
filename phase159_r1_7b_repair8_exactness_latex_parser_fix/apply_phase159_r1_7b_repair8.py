from __future__ import annotations

import ast
from pathlib import Path
import shutil


ROOT = Path.cwd()
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
BACKUP_DIR = ROOT / "phase159_r1_7b_repair8_backup_before_apply"

NEW_EXACTNESS_STEP = 'def _phase159_r1_7b_exactness_step_latex(\n  proof_step: ProofStep,\n) -> str | None:\n  statement = proof_step.conclusion\n\n  if not isinstance(\n    statement,\n    TodaProp42ExactnessStatement,\n  ):\n    return None\n\n  window = statement.window\n\n  return (\n    render_toda_primary_group_latex(\n      window.source_term\n    )\n    + r" \\xrightarrow{"\n    + window.first_map.name\n    + r"} "\n    + render_toda_primary_group_latex(\n      window.middle_term\n    )\n    + r" \\xrightarrow{"\n    + window.second_map.name\n    + r"} "\n    + render_toda_primary_group_latex(\n      window.target_term\n    )\n  )\n'
NEW_INLINE_PARSER = 'def _phase159_r1_7b_inline_exactness_latex(\n  line: str,\n) -> str | None:\n  stripped = line.strip()\n  verbose_suffix = "$ は完全である."\n\n  if (\n    stripped.startswith(\n      "$"\n    )\n    and stripped.endswith(\n      verbose_suffix\n    )\n  ):\n    latex = stripped[\n      1:-len(\n        verbose_suffix\n      )\n    ]\n  elif (\n    stripped.startswith(\n      "$"\n    )\n    and stripped.endswith(\n      "$."\n    )\n  ):\n    latex = stripped[\n      1:-2\n    ]\n  elif (\n    stripped.startswith(\n      "$"\n    )\n    and stripped.endswith(\n      "$"\n    )\n  ):\n    latex = stripped[\n      1:-1\n    ]\n  else:\n    return None\n\n  if latex.count(\n    r"\\xrightarrow{"\n  ) < 2:\n    return None\n\n  if not latex.startswith(\n    r"\\pi_{"\n  ):\n    return None\n\n  return latex\n'


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

  replacement_text = (
    replacement.rstrip()
    + "\n\n"
  )

  return "".join(
    (
      *lines[:start],
      replacement_text,
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

  source = replace_function(
    source,
    "_phase159_r1_7b_exactness_step_latex",
    NEW_EXACTNESS_STEP,
  )
  source = replace_function(
    source,
    "_phase159_r1_7b_inline_exactness_latex",
    NEW_INLINE_PARSER,
  )

  ast.parse(
    source
  )

  RENDERER.write_text(
    source,
    encoding="utf-8",
  )

  print(
    "Phase 159-R1-7b repair8 applied."
  )
  print(
    "Production file: "
    "toda_group_proof_narrative_renderer.py"
  )
  print(
    "Changed functions:"
  )
  print(
    "  _phase159_r1_7b_exactness_step_latex"
  )
  print(
    "  _phase159_r1_7b_inline_exactness_latex"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
