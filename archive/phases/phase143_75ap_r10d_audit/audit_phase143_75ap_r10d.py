from pathlib import Path
import ast

TARGET_NAMES = {
  "render_toda_group_proof_narrative_argument_body_markdown",
  "extract_toda_group_proof_narrative_argument_local_body_blocks",
  "_insert_toda_group_proof_narrative_transition_connector",
}

excluded_parts = {
  ".git",
  ".pytest_cache",
  "__pycache__",
  ".venv",
  "venv",
}

print("=" * 78)
print("Phase 143-75AP R10D body/local-block definition audit")
print("=" * 78)

for path in sorted(Path(".").rglob("*.py")):
  if any(part in excluded_parts for part in path.parts):
    continue

  text = path.read_text(
    encoding="utf-8",
    errors="replace",
  )

  if not any(name in text for name in TARGET_NAMES):
    continue

  try:
    tree = ast.parse(text)
  except SyntaxError:
    continue

  lines = text.splitlines()

  definitions = [
    node
    for node in ast.walk(tree)
    if isinstance(node, ast.FunctionDef)
    and node.name in TARGET_NAMES
  ]

  if not definitions:
    continue

  print()
  print("=" * 78)
  print(path)
  print("-" * 78)

  for fn in sorted(
    definitions,
    key=lambda node: node.lineno,
  ):
    print()
    print(
      f"FUNCTION {fn.name}: "
      f"lines {fn.lineno}-{fn.end_lineno}"
    )

    for number in range(
      fn.lineno - 1,
      fn.end_lineno,
    ):
      print(
        f"{number + 1:5}: {lines[number]}"
      )
