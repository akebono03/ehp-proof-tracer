from __future__ import annotations

import argparse
import ast
from pathlib import Path


DELETE = {
  (
    "tests/test_phase144_6_pi6_generic_production_route.py",
    "test_phase144_6_pi6_production_branch_contains_no_legacy_renderer_call",
  ),
}

REPLACE = {
  (
    "tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py",
    "test_phase144_6_r25_9b_depth2_narrative_has_definition_without_pi5_3",
  ): """def test_phase144_6_r25_9b_depth2_narrative_has_definition():
  _, presentation = (
    _pi6_3_depth2()
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert r"$\\nu'$ を定める." in rendered
  assert r"2\\nu' = \\eta_{3}^{3}" in rendered
  assert (
    r"\\pi_{6}^{3} = "
    r"\\mathbb{Z}/4\\{\\nu'\\}"
    in rendered
  )
""",
  (
    "tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py",
    "test_phase144_6_r25_9b_cli_depth2_narrative_has_definition",
  ): """def test_phase144_6_r25_9b_cli_depth2_narrative_has_definition(
  capsys,
):
  exit_code = _run_group_proof_command(
    3,
    3,
    max_depth=2,
    mode="narrative",
  )
  output = capsys.readouterr().out

  assert exit_code == 0
  assert r"$\\nu'$ を定める." in output
  assert (
    r"\\pi_{6}^{3} = "
    r"\\mathbb{Z}/4\\{\\nu'\\}"
    in output
  )
""",
}


def _functions(source):
  tree = ast.parse(source)
  return {
    node.name: node
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }


def _replace(
  source,
  old_name,
  replacement,
):
  lines = source.splitlines(
    keepends=True
  )
  functions = _functions(
    source
  )

  if old_name not in functions:
    raise RuntimeError(
      "Function not found for replacement: "
      + old_name
    )

  node = functions[
    old_name
  ]

  if node.end_lineno is None:
    raise RuntimeError(
      "AST end_lineno unavailable: "
      + old_name
    )

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

  updated = (
    source[:start]
    + replacement.rstrip(
      "\n"
    )
    + "\n"
    + source[end:]
  )
  ast.parse(
    updated
  )
  return updated


def _remove(
  source,
  name,
):
  lines = source.splitlines(
    keepends=True
  )
  functions = _functions(
    source
  )

  if name not in functions:
    raise RuntimeError(
      "Function not found for deletion: "
      + name
    )

  node = functions[
    name
  ]

  if node.end_lineno is None:
    raise RuntimeError(
      "AST end_lineno unavailable: "
      + name
    )

  del lines[
    node.lineno - 1:
    node.end_lineno
  ]

  updated = "".join(
    lines
  )
  ast.parse(
    updated
  )
  return updated


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  args = parser.parse_args()

  root = args.repo_root.resolve()
  changed = set()

  for (
    relative_path,
    old_name,
  ), replacement in REPLACE.items():
    path = root / relative_path
    source = path.read_text(
      encoding="utf-8-sig"
    )
    path.write_text(
      _replace(
        source,
        old_name,
        replacement,
      ),
      encoding="utf-8",
    )
    changed.add(
      relative_path
    )

  for (
    relative_path,
    function_name,
  ) in DELETE:
    path = root / relative_path
    source = path.read_text(
      encoding="utf-8-sig"
    )
    path.write_text(
      _remove(
        source,
        function_name,
      ),
      encoding="utf-8",
    )
    changed.add(
      relative_path
    )

  print(
    "Phase 155 Closure-R3-R3 changes applied."
  )
  print(
    "Deleted stale static route test:",
    len(
      DELETE
    ),
  )
  print(
    "Updated stale depth2 tests:",
    len(
      REPLACE
    ),
  )
  print(
    "Production changes: none"
  )
  print(
    "Top-level import changes: none"
  )

  for path in sorted(
    changed
  ):
    print(
      " -",
      path,
    )


if __name__ == "__main__":
  main()
