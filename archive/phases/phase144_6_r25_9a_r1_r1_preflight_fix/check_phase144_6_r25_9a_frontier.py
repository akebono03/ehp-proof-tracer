import ast
from pathlib import Path

TARGET = Path(
  "toda_group_proof_narrative_argument_multi_renderer.py"
)
HELPER = (
  "_toda_group_proof_narrative_argument_frontier_hidden_step_ids"
)

source = TARGET.read_text(
  encoding="utf-8-sig"
)
tree = ast.parse(
  source
)

helpers = [
  node
  for node in tree.body
  if (
    isinstance(
      node,
      ast.FunctionDef,
    )
    and node.name == HELPER
  )
]

if len(helpers) != 1:
  raise RuntimeError(
    f"expected exactly one {HELPER}; found {len(helpers)}"
  )

helper = helpers[0]

role_guards = [
  node
  for node in ast.walk(
    helper
  )
  if (
    isinstance(
      node,
      ast.If,
    )
    and "ESTABLISH_DEFINITION"
    in ast.get_source_segment(
      source,
      node.test,
    )
  )
]

if not role_guards:
  raise RuntimeError(
    "R25-9A ESTABLISH_DEFINITION role guard "
    "is not present in the frontier helper"
  )

guarded_second_level_loops = []

for role_guard in role_guards:
  for node in role_guard.body:
    for child in ast.walk(
      node
    ):
      if not isinstance(
        child,
        ast.For,
      ):
        continue

      loop_source = ast.get_source_segment(
        source,
        child,
      )

      if (
        "direct_premise_steps"
        in loop_source
        and ".premises"
        in loop_source
        and "protected_step_ids"
        in loop_source
      ):
        guarded_second_level_loops.append(
          child
        )

unguarded_second_level_loops = []

for node in helper.body:
  if not isinstance(
    node,
    ast.For,
  ):
    continue

  loop_source = ast.get_source_segment(
    source,
    node,
  )

  if (
    "direct_premise_steps"
    in loop_source
    and ".premises"
    in loop_source
    and "protected_step_ids"
    in loop_source
  ):
    unguarded_second_level_loops.append(
      node
    )

if not guarded_second_level_loops:
  raise RuntimeError(
    "R25-9A guarded second-level premise protection "
    "was not found"
  )

if unguarded_second_level_loops:
  raise RuntimeError(
    "unguarded second-level premise protection still exists"
  )

print(
  "R25-9A frontier repair AST preflight: PASS"
)
print(
  "ESTABLISH_DEFINITION guarded second-level loops:",
  len(
    guarded_second_level_loops
  ),
)
