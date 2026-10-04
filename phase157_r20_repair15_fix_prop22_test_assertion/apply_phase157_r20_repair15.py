from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
TARGET = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair10_reference_local_specialization.py"
)

TEST_FUNCTION = 'def test_phase157_r20_repair10_public_references_are_dependency_specialized():\n  rendered = _render_pi6_3_repair10()\n\n  headers = (\n    "**[R1] Proposition 5.6.**",\n    "**[R2] (5.3).**",\n    "**[R3] Proposition 5.3.**",\n    "**[R4] Proposition 5.1.**",\n    "**[R5] Proposition 2.2.**",\n  )\n\n  for header in headers:\n    assert header in rendered\n\n  reference = rendered.split(\n    "---",\n    1,\n  )[0]\n\n  r3 = reference.split(\n    "**[R3] Proposition 5.3.**",\n    1,\n  )[1].split(\n    "**[R4]",\n    1,\n  )[0]\n\n  assert (\n    r"\\pi_{7}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}"\n    in r3\n  )\n  assert r"\\pi_{5}^{3}" not in r3\n  assert r"\\pi_{4}^{2}" not in r3\n\n  r4 = reference.split(\n    "**[R4] Proposition 5.1.**",\n    1,\n  )[1].split(\n    "**[R5]",\n    1,\n  )[0]\n\n  assert (\n    r"\\pi_{6}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}\\}"\n    in r4\n  )\n  assert r"\\pi_{3}^{2}" not in r4\n\n  r5 = reference.split(\n    "**[R5] Proposition 2.2.**",\n    1,\n  )[1]\n\n  assert (\n    r"H(\\alpha\\circ E\\beta)"\n    in r5\n  )\n  assert r"\\alpha" in r5\n  assert r"\\beta" in r5\n  assert "H(lpha" not in r5\n  assert "H(lpha\\\\circ eta)" not in r5\n'


def function_range(
  source: str,
  name: str,
):
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

      while (
        end < len(source)
        and source[
          end:
          end + 1
        ] == "\n"
      ):
        end += 1

      return start, end

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
      "phase157_r20_repair15_backup_"
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
    "test_phase157_r20_repair10_public_references_are_dependency_specialized",
    TEST_FUNCTION,
  )

  compile(
    source,
    str(
      TARGET
    ),
    "exec",
  )

  TARGET.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair15 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed test only:",
    TARGET,
  )
  print(
    "Production code changes: none"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
