from pathlib import Path
import ast

TARGET_NAMES = {
  "_render_generic_narrative_proof_block",
}

TARGET_TERMS = {
  "suppress_provenance_only",
  "provenance",
  "semantic",
  "aggregate",
}

excluded_parts = {
  ".git",
  ".pytest_cache",
  "__pycache__",
  ".venv",
  "venv",
}

print("=" * 78)
print("Phase 143-75AP R10E generic suppression audit")
print("=" * 78)

for path in sorted(Path(".").rglob("*.py")):
  if any(part in excluded_parts for part in path.parts):
    continue

  text = path.read_text(
    encoding="utf-8",
    errors="replace",
  )

  if "_render_generic_narrative_proof_block" not in text:
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

  if definitions:
    print()
    print("=" * 78)
    print(path)
    print("-" * 78)

    for fn in definitions:
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

for path in sorted(Path(".").rglob("*.py")):
  if any(part in excluded_parts for part in path.parts):
    continue

  text = path.read_text(
    encoding="utf-8",
    errors="replace",
  )

  if not (
    "provenance" in text.lower()
    and "semantic" in text.lower()
  ):
    continue

  lines = text.splitlines()
  hit_indices = [
    index
    for index, line in enumerate(lines)
    if any(
      term in line.lower()
      for term in TARGET_TERMS
    )
  ]

  if not hit_indices:
    continue

  print()
  print("=" * 78)
  print("RELATED:", path)
  print("-" * 78)

  shown = set()

  for index in hit_indices:
    start = max(0, index - 8)
    end = min(len(lines), index + 12)
    key = (start, end)

    if key in shown:
      continue

    shown.add(key)

    print()
    print(
      f"--- lines {start + 1}-{end} ---"
    )

    for number in range(start, end):
      print(
        f"{number + 1:5}: {lines[number]}"
      )
