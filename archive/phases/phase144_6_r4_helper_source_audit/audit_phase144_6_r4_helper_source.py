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

if helper is None:
  raise RuntimeError("R4 frontier helper not found")

print("=" * 100)
print("Phase 144-6-R4 current frontier helper source")
print("=" * 100)
print(
  "parameters:",
  [arg.arg for arg in helper.args.args],
)
print(
  f"lines: {helper.lineno}-{helper.end_lineno}"
)
print("-" * 100)

lines = source.splitlines()
for line_number in range(
  helper.lineno,
  helper.end_lineno + 1,
):
  print(
    f"{line_number:4}: {lines[line_number - 1]}"
  )

print("=" * 100)
print("helper calls")
print("=" * 100)

calls = sorted(
  [
    node
    for node in ast.walk(tree)
    if isinstance(node, ast.Call)
    and isinstance(node.func, ast.Name)
    and node.func.id == HELPER
  ],
  key=lambda node: node.lineno,
)

print("count:", len(calls))
for index, call in enumerate(calls, start=1):
  print(
    f"call {index}: lines {call.lineno}-{call.end_lineno}"
  )
  print(
    "args:",
    [
      arg.id if isinstance(arg, ast.Name) else ast.dump(arg)
      for arg in call.args
    ],
  )
