from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
HELPER = "_toda_group_proof_narrative_argument_frontier_hidden_step_ids"


def main() -> int:
  source = TARGET.read_text(encoding="utf-8-sig")
  tree = ast.parse(source)

  helper = next(
    node for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name == HELPER
  )
  params = [arg.arg for arg in helper.args.args]
  if params != ["presentation", "local_body_blocks", "argument"]:
    raise RuntimeError(
      "unexpected pre-repair helper signature: " + repr(params)
    )

  calls = sorted(
    [
      node for node in ast.walk(tree)
      if isinstance(node, ast.Call)
      and isinstance(node.func, ast.Name)
      and node.func.id == HELPER
    ],
    key=lambda node: node.lineno,
  )
  if len(calls) != 2:
    raise RuntimeError(
      f"expected two duplicate helper calls; found {len(calls)}"
    )
  for call in calls:
    names = [
      arg.id if isinstance(arg, ast.Name) else None
      for arg in call.args
    ]
    if names != ["presentation", "local_body_blocks", "argument"]:
      raise RuntimeError(
        "unexpected pre-repair call args: " + repr(names)
      )

  assignments = sorted(
    [
      node for node in ast.walk(tree)
      if isinstance(node, ast.Assign)
      and any(
        isinstance(target, ast.Name)
        and target.id == "context_hidden_step_ids"
        for target in node.targets
      )
    ],
    key=lambda node: node.lineno,
  )
  if len(assignments) != 4:
    raise RuntimeError(
      "expected four duplicated context-hidden assignments; "
      f"found {len(assignments)}"
    )

  lines = source.splitlines(keepends=True)

  # Remove the second duplicated initialization + frontier-union pair.
  second_pair_start = assignments[2].lineno - 1
  second_pair_end = assignments[3].end_lineno
  del lines[second_pair_start:second_pair_end]
  source = "".join(lines)

  # Add complete blocks to the helper signature using actual newlines.
  tree = ast.parse(source)
  helper = next(
    node for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name == HELPER
  )
  lines = source.splitlines(keepends=True)
  insert_at = helper.args.args[1].lineno - 1
  indent = " " * helper.args.args[1].col_offset
  lines[insert_at:insert_at] = [
    indent + "blocks: tuple[\n",
    indent + "  TodaGroupProofNarrativeBlock,\n",
    indent + "  ...,\n",
    indent + "],\n",
  ]
  source = "".join(lines)

  # Add blocks to the one remaining helper call.
  tree = ast.parse(source)
  calls = [
    node for node in ast.walk(tree)
    if isinstance(node, ast.Call)
    and isinstance(node.func, ast.Name)
    and node.func.id == HELPER
  ]
  if len(calls) != 1:
    raise RuntimeError(
      f"expected one helper call after cleanup; found {len(calls)}"
    )
  call = calls[0]
  lines = source.splitlines(keepends=True)
  insert_at = call.args[1].lineno - 1
  indent = " " * call.args[1].col_offset
  lines[insert_at:insert_at] = [indent + "blocks,\n"]
  source = "".join(lines)

  # Verify final structure before writing.
  tree = ast.parse(source)
  helper = next(
    node for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name == HELPER
  )
  final_params = [arg.arg for arg in helper.args.args]
  final_calls = [
    node for node in ast.walk(tree)
    if isinstance(node, ast.Call)
    and isinstance(node.func, ast.Name)
    and node.func.id == HELPER
  ]
  final_assignments = [
    node for node in ast.walk(tree)
    if isinstance(node, ast.Assign)
    and any(
      isinstance(target, ast.Name)
      and target.id == "context_hidden_step_ids"
      for target in node.targets
    )
  ]
  expected = [
    "presentation",
    "blocks",
    "local_body_blocks",
    "argument",
  ]
  final_args = [
    arg.id if isinstance(arg, ast.Name) else None
    for arg in final_calls[0].args
  ]

  if final_params != expected:
    raise RuntimeError(
      "final helper signature invalid: " + repr(final_params)
    )
  if len(final_calls) != 1 or final_args != expected:
    raise RuntimeError(
      "final helper call invalid: " + repr(final_args)
    )
  if len(final_assignments) != 2:
    raise RuntimeError(
      "expected exactly initialization + frontier union; "
      f"found {len(final_assignments)} assignments"
    )

  TARGET.write_text(source, encoding="utf-8")
  print("Phase 144-6-R4-R5 duplicate cleanup applied.")
  print("helper parameters:", final_params)
  print("helper call count:", len(final_calls))
  print("helper call args:", final_args)
  print(
    "context_hidden_step_ids assignment count:",
    len(final_assignments),
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
