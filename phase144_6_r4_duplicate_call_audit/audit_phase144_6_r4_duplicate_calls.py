from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
HELPER = "_toda_group_proof_narrative_argument_frontier_hidden_step_ids"

source = TARGET.read_text(encoding="utf-8-sig")
tree = ast.parse(source)

helper = next(
  (
    node
    for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name == HELPER
  ),
  None,
)

print("=" * 100)
print("Phase 144-6-R4 duplicate helper-call audit")
print("=" * 100)

if helper is None:
  print("helper: NOT FOUND")
else:
  print(
    "helper parameters:",
    [arg.arg for arg in helper.args.args],
  )
  print(
    f"helper lines: {helper.lineno}-{helper.end_lineno}"
  )

calls = [
  node
  for node in ast.walk(tree)
  if isinstance(node, ast.Call)
  and isinstance(node.func, ast.Name)
  and node.func.id == HELPER
]

print("helper call count:", len(calls))
lines = source.splitlines()

for index, call in enumerate(
  sorted(calls, key=lambda node: node.lineno),
  start=1,
):
  print()
  print("-" * 100)
  print(
    f"CALL {index}: lines {call.lineno}-{call.end_lineno}"
  )
  print(
    "args:",
    [
      arg.id if isinstance(arg, ast.Name) else ast.dump(arg)
      for arg in call.args
    ],
  )
  start = max(1, call.lineno - 12)
  end = min(len(lines), call.end_lineno + 12)
  for line_number in range(start, end + 1):
    marker = ">>" if call.lineno <= line_number <= call.end_lineno else "  "
    print(
      f"{marker} {line_number:4}: {lines[line_number - 1]}"
    )

print()
print("=" * 100)
print("context_hidden_step_ids assignments")
print("=" * 100)
for node in ast.walk(tree):
  if not isinstance(node, ast.Assign):
    continue
  if not any(
    isinstance(target, ast.Name)
    and target.id == "context_hidden_step_ids"
    for target in node.targets
  ):
    continue
  print(f"assignment lines: {node.lineno}-{node.end_lineno}")
  for line_number in range(
    max(1, node.lineno - 2),
    min(len(lines), node.end_lineno + 2) + 1,
  ):
    print(
      f"  {line_number:4}: {lines[line_number - 1]}"
    )
  print()
