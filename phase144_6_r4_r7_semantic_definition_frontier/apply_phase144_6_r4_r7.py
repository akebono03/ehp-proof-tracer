from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
HELPER = "_toda_group_proof_narrative_argument_frontier_hidden_step_ids"

NEW_HELPER = 'def _toda_group_proof_narrative_argument_frontier_hidden_step_ids(\n  presentation: TodaGroupProofPresentation,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  local_body_blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,\n  argument: TodaGroupProofNarrativeArgument,\n) -> frozenset[\n  int\n]:\n  conclusion_step = (\n    extract_toda_group_proof_narrative_argument_conclusion_step(\n      argument\n    )\n  )\n\n  if conclusion_step is None:\n    return frozenset()\n\n  direct_premise_steps = list(\n    conclusion_step.premises\n  )\n\n  if (\n    argument.role\n    is TodaGroupProofNarrativeArgumentRole\n    .ESTABLISH_DEFINITION\n  ):\n    direct_premise_steps.extend(\n      semantic.prerequisite_step\n      for semantic in semantic_sidecar.dependency_semantics\n      if (\n        semantic.dependent_step\n        is conclusion_step\n      )\n    )\n\n  direct_premise_ids = {\n    id(\n      premise_step\n    )\n    for premise_step in direct_premise_steps\n  }\n  transition_step_ids = {\n    id(\n      step\n    )\n    for transition in (\n      extract_toda_group_proof_narrative_step_transitions(\n        presentation,\n        blocks,\n      )\n    )\n    for step in (\n      transition.source_step,\n      transition.target_step,\n    )\n  }\n\n  protected_step_ids = (\n    direct_premise_ids\n    | transition_step_ids\n    | {\n      id(\n        conclusion_step\n      )\n    }\n  )\n\n  if (\n    argument.role\n    is TodaGroupProofNarrativeArgumentRole\n    .ESTABLISH_DEFINITION\n  ):\n    for proof_step in direct_premise_steps:\n      protected_step_ids.update(\n        id(\n          premise_step\n        )\n        for premise_step in proof_step.premises\n      )\n\n  return frozenset(\n    id(\n      proof_step\n    )\n    for block in local_body_blocks\n    for proof_step in block.steps\n    if (\n      id(\n        proof_step\n      ) not in protected_step_ids\n      and block.role\n      not in (\n        TodaGroupProofNarrativeMathematicalBlockRole\n        .EXACTNESS,\n        TodaGroupProofNarrativeMathematicalBlockRole\n        .REFERENCE,\n      )\n    )\n  )\n'


def main() -> int:
  source = TARGET.read_text(encoding="utf-8-sig")
  tree = ast.parse(source)
  helpers = [
    node for node in tree.body
    if isinstance(node, ast.FunctionDef) and node.name == HELPER
  ]
  if len(helpers) != 1:
    raise RuntimeError(f"expected exactly one helper; found {len(helpers)}")
  helper = helpers[0]
  params = [arg.arg for arg in helper.args.args]
  expected_before = ["presentation", "blocks", "local_body_blocks", "argument"]
  if params != expected_before:
    raise RuntimeError("unexpected pre-repair helper signature: " + repr(params))

  lines = source.splitlines(keepends=True)
  replacement = NEW_HELPER if NEW_HELPER.endswith("\n") else NEW_HELPER + "\n"
  lines[helper.lineno - 1:helper.end_lineno] = [replacement]
  source = "".join(lines)

  tree = ast.parse(source)
  calls = [
    node for node in ast.walk(tree)
    if isinstance(node, ast.Call)
    and isinstance(node.func, ast.Name)
    and node.func.id == HELPER
  ]
  if len(calls) != 1:
    raise RuntimeError(f"expected exactly one helper call; found {len(calls)}")
  call = calls[0]
  call_args = [arg.id if isinstance(arg, ast.Name) else None for arg in call.args]
  expected_call_before = ["presentation", "blocks", "local_body_blocks", "argument"]
  if call_args != expected_call_before:
    raise RuntimeError("unexpected pre-repair helper call: " + repr(call_args))

  lines = source.splitlines(keepends=True)
  insert_at = call.args[3].lineno - 1
  indent = " " * call.args[3].col_offset
  lines[insert_at:insert_at] = [indent + "semantic_sidecar,\n"]
  source = "".join(lines)

  tree = ast.parse(source)
  helper = next(
    node for node in tree.body
    if isinstance(node, ast.FunctionDef) and node.name == HELPER
  )
  calls = [
    node for node in ast.walk(tree)
    if isinstance(node, ast.Call)
    and isinstance(node.func, ast.Name)
    and node.func.id == HELPER
  ]
  final_params = [arg.arg for arg in helper.args.args]
  final_args = [arg.id if isinstance(arg, ast.Name) else None for arg in calls[0].args]
  expected_after = [
    "presentation", "blocks", "local_body_blocks", "semantic_sidecar", "argument"
  ]
  if final_params != expected_after:
    raise RuntimeError("invalid final helper signature: " + repr(final_params))
  if len(calls) != 1 or final_args != expected_after:
    raise RuntimeError("invalid final helper call: " + repr(final_args))

  TARGET.write_text(source, encoding="utf-8")
  print("Phase 144-6-R4-R7 semantic Definition frontier applied.")
  print("helper parameters:", final_params)
  print("helper call args:", final_args)
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
