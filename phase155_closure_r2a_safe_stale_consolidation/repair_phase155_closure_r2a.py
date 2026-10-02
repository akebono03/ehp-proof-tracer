from __future__ import annotations

import argparse
import ast
from pathlib import Path

from phase155_closure_r2a_replacements import (
  REPLACEMENTS,
)


def _replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  tree = ast.parse(
    source
  )
  lines = source.splitlines(
    keepends=True
  )

  matches = [
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
  ]

  if len(
    matches
  ) != 1:
    raise RuntimeError(
      f"{function_name}: expected one top-level function, "
      f"found {len(matches)}"
    )

  node = matches[
    0
  ]

  if node.end_lineno is None:
    raise RuntimeError(
      f"{function_name}: AST end_lineno unavailable"
    )

  start = sum(
    len(
      line
    )
    for line in lines[
      : node.lineno - 1
    ]
  )
  end = sum(
    len(
      line
    )
    for line in lines[
      : node.end_lineno
    ]
  )

  normalized = replacement.rstrip(
    "\n"
  ) + "\n"

  return (
    source[
      :start
    ]
    + normalized
    + source[
      end:
    ]
  )


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()
  changed_files = []
  changed_functions = []

  for relative_path, functions in REPLACEMENTS.items():
    path = (
      repo_root
      / relative_path
    )

    source = path.read_text(
      encoding="utf-8-sig"
    )
    updated = source

    for function_name, replacement in functions.items():
      updated = _replace_function(
        updated,
        function_name,
        replacement,
      )
      changed_functions.append(
        (
          relative_path,
          function_name,
        )
      )

    ast.parse(
      updated
    )

    if updated != source:
      path.write_text(
        updated,
        encoding="utf-8",
      )
      changed_files.append(
        relative_path
      )

  print(
    "Changed test files:",
    len(
      changed_files
    ),
  )

  for relative_path in changed_files:
    print(
      " -",
      relative_path,
    )

  print(
    "Changed test functions:",
    len(
      changed_functions
    ),
  )
  print(
    "Import changes: none"
  )
  print(
    "Production changes: none"
  )

  if len(
    changed_functions
  ) != 38:
    raise SystemExit(
      "Expected 38 changed functions"
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
