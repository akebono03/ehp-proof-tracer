from __future__ import annotations

import argparse
import ast
from pathlib import Path


TARGET_PATH = Path(
  "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py"
)
TARGET_FUNCTION = (
  "test_phase150_rc4_7a_pi16_9_numbers_normalized_references"
)


def _function_source(
  source: str,
  function_name: str,
) -> str:
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
      if node.end_lineno is None:
        raise RuntimeError(
          "missing end_lineno"
        )

      return "".join(
        lines[
          node.lineno - 1:
          node.end_lineno
        ]
      )

  raise RuntimeError(
    "function not found: "
    + function_name
  )


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  args = parser.parse_args()

  path = (
    args.repo_root.resolve()
    / TARGET_PATH
  )

  source = path.read_text(
    encoding="utf-8-sig"
  )
  function_source = (
    _function_source(
      source,
      TARGET_FUNCTION,
    )
  )

  checks = {
    "uses_current_reference_intro": (
      'assert "使用する結果を先にまとめる." in rendered'
      in function_source
    ),
    "requires_normalized_r1_marker": (
      'assert "**[R1] " in rendered'
      in function_source
    ),
    "does_not_require_section_heading": (
      '## 使用する結果'
      not in function_source
    ),
    "does_not_freeze_reference_names": (
      "Proposition 5.15"
      not in function_source
      and "Lemma 5.14"
      not in function_source
      and "Theorem 3.6"
      not in function_source
      and "Lemma 5.13"
      not in function_source
    ),
  }

  for name, value in checks.items():
    print(
      name + ":",
      (
        "PASS"
        if value
        else "FAIL"
      ),
    )

  validated = all(
    checks.values()
  )

  print(
    "R6-R1-R2 source repair validated:",
    validated,
  )

  return (
    0
    if validated
    else 2
  )


if __name__ == "__main__":
  raise SystemExit(main())
