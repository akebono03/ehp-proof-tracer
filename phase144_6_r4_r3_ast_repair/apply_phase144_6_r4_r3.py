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

  parameter_names = [
    argument.arg
    for argument in helper.args.args
  ]
  print("helper parameters before:", parameter_names)

  if parameter_names == [
    "presentation",
    "local_body_blocks",
    "argument",
  ]:
    insertion_line = helper.args.args[1].lineno - 1
    lines = source.splitlines(keepends=True)
    lines[insertion_line:insertion_line] = [
      "  blocks: tuple[\\n",
      "    TodaGroupProofNarrativeBlock,\\n",
      "    ...,\\n",
      "  ],\\n",
    ]
    source = "".join(lines)
  elif parameter_names != [
    "presentation",
    "blocks",
    "local_body_blocks",
    "argument",
  ]:
    raise RuntimeError(
      "unexpected R4 helper parameters: "
      + repr(parameter_names)
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
      f"expected one R4 helper call; found {len(calls)}"
    )

  call = calls[0]
  arg_names = [
    arg.id if isinstance(arg, ast.Name) else None
    for arg in call.args
  ]
  print("helper call args before:", arg_names)

  if arg_names == [
    "presentation",
    "local_body_blocks",
    "argument",
  ]:
    lines = source.splitlines(keepends=True)
    insert_at = call.args[1].lineno - 1
    indent = " " * call.args[1].col_offset
    lines[insert_at:insert_at] = [
      indent + "blocks,\\n"
    ]
    source = "".join(lines)
  elif arg_names != [
    "presentation",
    "blocks",
    "local_body_blocks",
    "argument",
  ]:
    raise RuntimeError(
      "unexpected R4 helper call args: "
      + repr(arg_names)
    )

  tree = ast.parse(source)
  helper = next(
    node
    for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name == HELPER
  )
  final_parameters = [
    argument.arg
    for argument in helper.args.args
  ]
  calls = [
    node
    for node in ast.walk(tree)
    if isinstance(node, ast.Call)
    and isinstance(node.func, ast.Name)
    and node.func.id == HELPER
  ]
  final_args = [
    arg.id if isinstance(arg, ast.Name) else None
    for arg in calls[0].args
  ]

  if final_parameters != [
    "presentation",
    "blocks",
    "local_body_blocks",
    "argument",
  ]:
    raise RuntimeError(
      "final helper signature verification failed"
    )
  if final_args != [
    "presentation",
    "blocks",
    "local_body_blocks",
    "argument",
  ]:
    raise RuntimeError(
      "final helper call verification failed"
    )

  TARGET.write_text(source, encoding="utf-8")
  print("helper parameters after:", final_parameters)
  print("helper call args after:", final_args)
  print("Phase 144-6-R4-R3 AST repair applied.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
