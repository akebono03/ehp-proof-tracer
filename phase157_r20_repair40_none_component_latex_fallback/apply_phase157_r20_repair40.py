from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
TARGET = (
  ROOT
  / "toda_group_proof_generic_narrative_renderer.py"
)
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair40_none_component_latex_fallback.py"
)

NEW_FUNCTION = 'def _render_phase153_r3_6_component_latex(\n  component,\n) -> str | None:\n  if isinstance(\n    component,\n    ScalarGreaterEqualStatement,\n  ):\n    return (\n      _render_scalar_latex(\n        component.left\n      )\n      + r" \\ge "\n      + _render_scalar_latex(\n        component.right\n      )\n    )\n\n  try:\n    latex = (\n      render_repository_conclusion_latex(\n        component\n      )\n    )\n  except (\n    TypeError,\n    ValueError,\n  ):\n    latex = None\n\n  if latex is not None:\n    return (\n      _normalize_generic_narrative_statement_latex(\n        component,\n        latex,\n      )\n    )\n\n  try:\n    latex = (\n      render_toda_proof_statement_latex(\n        component\n      )\n    )\n  except (\n    TypeError,\n    ValueError,\n  ):\n    return None\n\n  if latex is None:\n    return None\n\n  return (\n    _normalize_generic_narrative_statement_latex(\n      component,\n      latex,\n    )\n  )\n'
TEST_SOURCE = 'from expression import (\n  ScalarSymbol,\n)\nfrom scalar_rules import (\n  OddScalarStatement,\n)\nfrom toda_group_proof_generic_narrative_renderer import (\n  _render_phase153_r3_6_component_latex,\n  _render_phase153_r3_6_component_list_prose,\n)\n\n\ndef test_phase157_r20_repair40_unsupported_odd_scalar_component_returns_none():\n  statement = OddScalarStatement(\n    scalar=ScalarSymbol(\n      name="x",\n    ),\n  )\n\n  assert (\n    _render_phase153_r3_6_component_latex(\n      statement\n    )\n    is None\n  )\n\n\ndef test_phase157_r20_repair40_component_list_skips_unsupported_odd_scalar_component():\n  statement = OddScalarStatement(\n    scalar=ScalarSymbol(\n      name="x",\n    ),\n  )\n\n  assert (\n    _render_phase153_r3_6_component_list_prose(\n      (\n        statement,\n      )\n    )\n    is None\n  )\n'


def function_range(
  source: str,
  name: str,
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
      and node.name == name
    ):
      start = sum(
        len(line)
        for line in lines[
          :node.lineno - 1
        ]
      )
      end = sum(
        len(line)
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
    + name
  )


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  start, end = function_range(
    source,
    name,
  )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def main() -> int:
  if not TARGET.is_file():
    raise RuntimeError(
      "Run from repository root."
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = (
    ROOT
    / (
      "phase157_r20_repair40_backup_"
      + timestamp
    )
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TARGET,
    backup / TARGET.name,
  )

  source = TARGET.read_text(
    encoding="utf-8"
  )
  source = replace_function(
    source,
    "_render_phase153_r3_6_component_latex",
    NEW_FUNCTION,
  )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
  )

  for token in forbidden:
    if token in source:
      raise RuntimeError(
        "target-specific token remains: "
        + token
      )

  compile(
    source,
    str(
      TARGET
    ),
    "exec",
  )
  compile(
    TEST_SOURCE,
    str(
      TEST
    ),
    "exec",
  )

  TARGET.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair40 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed production file:",
    TARGET,
  )
  print(
    "Added test:",
    TEST,
  )
  print("")
  print(
    "Architecture preflight:"
  )

  for token in forbidden:
    print(
      " ",
      token,
      "=",
      source.count(
        token
      ),
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
