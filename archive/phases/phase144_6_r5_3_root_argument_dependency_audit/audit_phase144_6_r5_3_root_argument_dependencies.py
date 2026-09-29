from __future__ import annotations

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  _argument_direct_dependency_indices,
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)

TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def group_result(n, k):
  report = build_standard_toda_report(n=n, k=k)
  return report.candidates[0].source_candidate.group_result


def statement_text(argument):
  step = extract_toda_group_proof_narrative_argument_conclusion_step(
    argument
  )
  return None if step is None else repr(step.conclusion)


def closure_from_block(
  direct_dependencies,
  start_index,
):
  visited = set()
  active = set()

  def visit(index):
    if index in visited or index in active:
      return
    active.add(index)
    for dependency in direct_dependencies[index]:
      visit(dependency)
    active.remove(index)
    visited.add(index)

  for dependency in direct_dependencies[start_index]:
    visit(dependency)
  return visited


def build_state(n, k, depth):
  result = group_result(n, k)
  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=depth,
  )
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )
  direct_dependencies = _argument_direct_dependency_indices(
    presentation,
    blocks,
    sidecar,
  )

  block_index_by_identity = {
    id(block): index
    for index, block in enumerate(blocks)
  }
  argument_index_by_conclusion_block_index = {
    block_index_by_identity[id(argument.conclusion_block)]: index
    for index, argument in enumerate(arguments)
  }

  roots = tuple(
    index
    for index, argument in enumerate(arguments)
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
      and argument.conclusion_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.TARGET
    )
  )

  rows = []
  for root_index in roots:
    root = arguments[root_index]
    root_block_index = block_index_by_identity[id(root.conclusion_block)]
    closure_blocks = closure_from_block(
      direct_dependencies,
      root_block_index,
    )
    closure_argument_indices = tuple(
      sorted(
        argument_index_by_conclusion_block_index[block_index]
        for block_index in closure_blocks
        if block_index in argument_index_by_conclusion_block_index
      )
    )

    child_reachable = set()
    active = set()

    def visit_argument(argument_index):
      if argument_index in child_reachable:
        return
      if argument_index in active:
        return
      active.add(argument_index)
      for child_index in arguments[argument_index].child_argument_indices:
        visit_argument(child_index)
      active.remove(argument_index)
      child_reachable.add(argument_index)

    visit_argument(root_index)
    child_reachable.discard(root_index)

    rows.append(
      {
        "root_index": root_index,
        "direct_children": root.child_argument_indices,
        "child_reachable": tuple(sorted(child_reachable)),
        "closure_arguments": closure_argument_indices,
      }
    )

  signature = tuple(
    (
      argument.role.value,
      statement_text(argument),
      argument.child_argument_indices,
    )
    for argument in arguments
  )

  return {
    "replay": replay,
    "arguments": arguments,
    "roots": roots,
    "rows": rows,
    "signature": signature,
  }


print("=" * 122)
print("Phase 144-6-R5-3 root-argument dependency completeness audit")
print("=" * 122)
print(
  "Compare explicit child_argument_indices with argument conclusions "
  "reachable through the full block dependency closure."
)

for n, k in TARGETS:
  print()
  print("-" * 122)
  print(f"TARGET n={n}, k={k}")
  print("-" * 122)

  states = []
  for depth in range(0, 7):
    try:
      state = build_state(n, k, depth)
    except Exception as exc:
      print(
        f"depth={depth}: ERROR "
        f"{type(exc).__name__}: {exc}"
      )
      states.append(None)
      continue

    states.append(state)
    print(
      f"depth={depth}: "
      f"replay_steps={len(state['replay'].steps)} "
      f"arguments={len(state['arguments'])} "
      f"roots={state['roots']}"
    )

    for index, argument in enumerate(state["arguments"]):
      print(
        f"  A{index:02d} "
        f"role={argument.role.value} "
        f"children={argument.child_argument_indices} "
        f"conclusion={statement_text(argument)}"
      )

    for row in state["rows"]:
      print(
        f"  ROOT A{row['root_index']:02d}: "
        f"direct_children={row['direct_children']} "
        f"child_reachable={row['child_reachable']} "
        f"closure_arguments={row['closure_arguments']} "
        f"child_matches_closure="
        f"{row['child_reachable'] == row['closure_arguments']}"
      )

  print()
  print("successive argument-graph signature changes:")
  for depth in range(0, len(states) - 1):
    current = states[depth]
    following = states[depth + 1]
    if current is None or following is None:
      print(f"  {depth}->{depth + 1}: unavailable")
      continue
    print(
      f"  {depth}->{depth + 1}: "
      f"{current['signature'] != following['signature']}"
    )

print()
print("=" * 122)
print("Interpretation aid")
print("=" * 122)
print(
  "If child_matches_closure is consistently True, existing "
  "child_argument_indices can represent root-required argument dependencies."
)
print(
  "If it is False, completion must not rely on child_argument_indices alone; "
  "the missing dependency path must be classified before any production change."
)
print(
  "A stable root argument graph is only a candidate completion signal. "
  "One-depth stability is not sufficient unless later depths cannot add "
  "root-required arguments by construction."
)
