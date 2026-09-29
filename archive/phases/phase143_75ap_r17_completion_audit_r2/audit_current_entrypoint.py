from pathlib import Path
import ast

targets = [
  Path("tests/test_phase143_51a_r_provenance_semantic_catalog.py"),
  Path("tests/test_phase143_51b_aggregate_statement_prose.py"),
]

for path in targets:
  print("=" * 78)
  print(path)
  print("=" * 78)
  text = path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
  tree = ast.parse(text)
  lines = text.splitlines()

  # Print imports and local helper functions only; these define the current
  # construction/rendering API used by the passing Phase143 tests.
  last_import = 0
  for node in tree.body:
    if isinstance(node, (ast.Import, ast.ImportFrom)):
      last_import = max(last_import, node.end_lineno)

  for i in range(last_import):
    print(f"{i + 1:04d}: {lines[i]}")

  for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name.startswith("_"):
      print(f"\n--- {node.name} ---")
      for i in range(node.lineno - 1, node.end_lineno):
        print(f"{i + 1:04d}: {lines[i]}")
