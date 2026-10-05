from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()

TARGETS = (
  (
    ROOT / "tests" / "test_phase134_24_pi15_8_narrative.py",
    "test_phase134_24_pi15_8_narrative_has_mathematical_structure",
    'def test_phase134_24_pi15_8_narrative_has_mathematical_structure(\n):\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _pi15_8_presentation()\n    )\n  )\n\n  assert "# Group proof narrative" in rendered\n  assert "## 証明対象" in rendered\n  assert "## 使用する結果" in rendered\n  assert "## 証明" in rendered\n  assert "Proposition 4.4.**" in rendered\n  assert (\n    r"\\left(α, \\beta\\right) \\mapsto "\n    r"Eα + \\sigma_{8}\\beta"\n    in rendered\n  )\n',
  ),
  (
    ROOT / "tests" / "test_phase150_rc4_7a_cross_group_reference_normalization.py",
    "test_phase150_rc4_7a_pi15_8_special_renderer_is_unchanged",
    'def test_phase150_rc4_7a_pi15_8_special_renderer_is_unchanged(\n):\n  rendered = _render_group(8, 7)\n\n  assert "Proposition 4.4.**" in rendered\n  assert (\n    r"\\left(α, \\beta\\right) \\mapsto "\n    r"Eα + \\sigma_{8}\\beta"\n    in rendered\n  )\n  assert "直和因子の順序を入れ替えると," in rendered\n',
  ),
  (
    ROOT / "tests" / "test_phase157_r20_repair53_r3_fixed_reference_attribution.py",
    "test_phase157_r20_repair53_r3_public_pi15_8_restores_prop44_reference",
    'def test_phase157_r20_repair53_r3_public_pi15_8_restores_prop44_reference():\n  (\n    raw,\n    presentation,\n    prop44_step,\n  ) = _repair53_r3_data()\n\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n\n  assert "Proposition 4.4.**" in rendered\n  assert "Proposition 5.15" in rendered\n  assert (\n    r"\\pi_{14}^{7} = "\n    r"\\mathbb{Z}/8\\{\\sigma\'\\}"\n    in rendered\n  )\n  assert (\n    r"\\left(α, \\beta\\right) \\mapsto "\n    r"Eα + \\sigma_{8}\\beta"\n    in rendered\n  )\n',
  ),
)


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


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  start, end = function_range(
    source,
    name,
  )

  current = source[
    start:
    end
  ]

  if (
    "Toda Proposition 4.4 の分解同型"
    not in current
  ):
    raise RuntimeError(
      "expected stale Proposition 4.4 title assertion "
      "not found in "
      + name
    )

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + source[
      end:
    ]
  )


def main() -> int:
  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r20_repair53_r3a_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  updated_files = []

  for path, name, replacement in TARGETS:
    if not path.is_file():
      raise RuntimeError(
        "required test file not found: "
        + str(
          path
        )
      )

    source = path.read_text(
      encoding="utf-8"
    )
    updated = replace_function(
      source,
      name,
      replacement,
    )

    compile(
      updated,
      str(
        path
      ),
      "exec",
    )

    shutil.copy2(
      path,
      backup / path.name,
    )
    path.write_text(
      updated,
      encoding="utf-8",
      newline="\n",
    )
    updated_files.append(
      path
    )

  print(
    "Phase157-R20 repair53-r3a applied."
  )
  print(
    "Backup:",
    backup,
  )

  for path in updated_files:
    print(
      "Changed test file:",
      path,
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
