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

  parameters = [arg.arg for arg in helper.args.args]
  print("helper parameters before:", parameters)

  lines = source.splitlines(keepends=True)

  if parameters == ["presentation", "local_body_blocks", "argument"]:
    insert_at = helper.args.args[1].lineno - 1
    indent = " " * helper.args.args[1].col_offset
    actual_lines = [
      indent + "blocks: tuple[\n",
      indent + "  TodaGroupProofNarrativeBlock,\n",
      indent + "  ...,\n",
      indent + "],\n",
    ]
    lines[insert_at:insert_at] = actual_lines
    source = "".join(lines)
  elif parameters != [
    "presentation",
    "blocks",
    "local_body_blocks",
    "argument",
  ]:
    raise RuntimeError(
      "unexpected helper parameters: " + repr(parameters)
    )

  tree = ast.parse(source)
  calls = [
    node
    for node in ast.walk(tree)
    if isinstance(node, ast.Call)
    and isinstance(node.func, ast.Name)
    and node.func.id == HELPER
  ]
  if len(calls) != 1:
    raise RuntimeError(
      f"expected exactly one helper call; found {len(calls)}"
    )

  call = calls[0]
  call_args = [
    arg.id if isinstance(arg, ast.Name) else None
    for arg in call.args
  ]
  print("helper call args before:", call_args)

  if call_args == ["presentation", "local_body_blocks", "argument"]:
    lines = source.splitlines(keepends=True)
    insert_at = call.args[1].lineno - 1
    indent = " " * call.args[1].col_offset
    lines[insert_at:insert_at] = [indent + "blocks,\n"]
    source = "".join(lines)
  elif call_args != [
    "presentation",
    "blocks",
    "local_body_blocks",
    "argument",
  ]:
    raise RuntimeError(
      "unexpected helper call args: " + repr(call_args)
    )

  tree = ast.parse(source)
  helper = next(
    node
    for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name == HELPER
  )
  final_parameters = [arg.arg for arg in helper.args.args]
  final_calls = [
    node
    for node in ast.walk(tree)
    if isinstance(node, ast.Call)
    and isinstance(node.func, ast.Name)
    and node.func.id == HELPER
  ]
  final_args = [
    arg.id if isinstance(arg, ast.Name) else None
    for arg in final_calls[0].args
  ]

  expected = [
    "presentation",
    "blocks",
    "local_body_blocks",
    "argument",
  ]
  if final_parameters != expected:
    raise RuntimeError(
      "final helper signature verification failed: "
      + repr(final_parameters)
    )
  if final_args != expected:
    raise RuntimeError(
      "final helper call verification failed: "
      + repr(final_args)
    )

  TARGET.write_text(source, encoding="utf-8")

  print("helper parameters after:", final_parameters)
  print("helper call args after:", final_args)
  print("Phase 144-6-R4-R4 repair applied.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
