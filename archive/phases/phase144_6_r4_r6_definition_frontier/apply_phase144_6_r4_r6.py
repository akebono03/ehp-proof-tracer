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
  expected = [
    "presentation",
    "blocks",
    "local_body_blocks",
    "argument",
  ]
  if params != expected:
    raise RuntimeError(
      "unexpected helper signature: " + repr(params)
    )

  helper_source = ast.get_source_segment(source, helper)
  if helper_source is None:
    raise RuntimeError("could not read helper source")

  old = """  direct_premise_ids = {
    id(
      premise_step
    )
    for premise_step in conclusion_step.premises
  }
"""
  new = """  direct_premise_ids = {
    id(
      premise_step
    )
    for premise_step in conclusion_step.premises
  }
  definition_support_premise_ids = (
    frozenset(
      id(
        support_premise_step
      )
      for premise_step in conclusion_step.premises
      for support_premise_step in premise_step.premises
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    )
    else frozenset()
  )
"""

  if helper_source.count(old) != 1:
    raise RuntimeError(
      "expected one direct_premise_ids block in helper"
    )
  new_helper_source = helper_source.replace(old, new, 1)

  # Extend the existing protected-step union, without changing any other rule.
  old_protected = """    | direct_premise_ids
    | transition_step_ids
"""
  new_protected = """    | direct_premise_ids
    | definition_support_premise_ids
    | transition_step_ids
"""
  if new_helper_source.count(old_protected) != 1:
    raise RuntimeError(
      "expected one protected-step union in helper"
    )
  new_helper_source = new_helper_source.replace(
    old_protected,
    new_protected,
    1,
  )

  start = helper.lineno - 1
  end = helper.end_lineno
  lines = source.splitlines(keepends=True)
  replacement = new_helper_source
  if not replacement.endswith("\n"):
    replacement += "\n"
  lines[start:end] = [replacement]
  source = "".join(lines)

  ast.parse(source)
  TARGET.write_text(source, encoding="utf-8")

  print("Phase 144-6-R4-R6 definition frontier applied.")
  print(
    "Definition arguments now preserve one additional "
    "premise-support layer."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
