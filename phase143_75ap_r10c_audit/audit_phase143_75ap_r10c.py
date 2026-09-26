from pathlib import Path
import ast

TARGET_NAMES = {
  "render_toda_group_proof_narrative_transition_connector",
  "extract_toda_group_proof_narrative_transitions",
}

excluded_parts = {
  ".git",
  ".pytest_cache",
  "__pycache__",
  ".venv",
  "venv",
}

print("=" * 78)
print("Phase 143-75AP R10C transition call-site audit")
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

  call_lines = []

  for node in ast.walk(tree):
    if not isinstance(node, ast.Call):
      continue

    func = node.func

    if (
      isinstance(func, ast.Name)
      and func.id in TARGET_NAMES
    ):
      call_lines.append(node.lineno)

  if not call_lines:
    continue

  print()
  print("=" * 78)
  print(path)
  print("-" * 78)

  functions = [
    node
    for node in ast.walk(tree)
    if isinstance(
      node,
      (
        ast.FunctionDef,
        ast.AsyncFunctionDef,
      ),
    )
  ]

  shown = set()

  for call_line in sorted(set(call_lines)):
    owners = [
      fn
      for fn in functions
      if fn.lineno <= call_line <= fn.end_lineno
    ]

    if owners:
      owner = min(
        owners,
        key=lambda fn: fn.end_lineno - fn.lineno,
      )
      start = owner.lineno
      end = owner.end_lineno
      label = owner.name
    else:
      start = max(1, call_line - 20)
      end = min(len(lines), call_line + 40)
      label = "<module>"

    key = (start, end)

    if key in shown:
      continue

    shown.add(key)

    print()
    print(
      f"FUNCTION {label}: lines {start}-{end}"
    )

    for number in range(start - 1, end):
      print(
        f"{number + 1:5}: {lines[number]}"
      )
