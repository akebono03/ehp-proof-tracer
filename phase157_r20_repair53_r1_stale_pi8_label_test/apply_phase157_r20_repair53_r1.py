from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
TARGET = (
  ROOT
  / "tests"
  / "test_phase134_9_pi8_5_narrative.py"
)
REPLACEMENT = 'def test_phase134_9_pi8_5_keeps_phase133_labels(\n  capsys,\n):\n  rendered = _render_pi8_5(\n    capsys\n  )\n\n  assert (\n    "Toda Proposition 5.6 のうち,"\n    in rendered\n  )\n  assert "## 使用する結果" in rendered\n  assert "## 証明" in rendered\n  assert (\n    r"\\pi_{8}^{5} = "\n    r"\\mathbb{Z}/8\\{\\nu_{5}\\}"\n    in rendered\n  )\n'


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
      return start, end

  raise RuntimeError(
    "function not found: "
    + name
  )


def main() -> int:
  if not TARGET.is_file():
    raise RuntimeError(
      "Run from repository root."
    )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  name = (
    "test_phase134_9_pi8_5_keeps_phase133_labels"
  )
  start, end = function_range(
    source,
    name,
  )

  current = source[
    start:
    end
  ]

  expected_old = (
    "Toda (5.6) の ν₄ 分解"
  )

  if expected_old not in current:
    raise RuntimeError(
      "Expected stale Phase133 label assertion "
      "was not found in the target test."
    )

  updated = (
    source[
      :start
    ]
    + REPLACEMENT.rstrip()
    + source[
      end:
    ]
  )

  compile(
    updated,
    str(
      TARGET
    ),
    "exec",
  )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r20_repair53_r1_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TARGET,
    backup / TARGET.name,
  )

  TARGET.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair53-r1 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed test file:",
    TARGET,
  )
  print("")
  print(
    "Production code changes: none"
  )
  print(
    "Import changes: none"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
