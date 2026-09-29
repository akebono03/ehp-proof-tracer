from collections import deque

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
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
  (8, 7),  # pi_15^8
  (9, 7),  # pi_16^9
)

MAX_DEPTH = 8


def _group_result(n, k):
  report = build_standard_toda_report(n, k)
  return report.group_result


def _step_label(step):
  conclusion = getattr(step, "conclusion", None)
  rule = getattr(step, "inference_rule", None)
  rule_name = getattr(rule, "name", None)
  return f"{type(conclusion).__name__}: {conclusion!r} [rule={rule_name!r}]"


def _build_state(n, k, depth):
  group_result = _group_result(n, k)
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=depth,
  )
  presentation = build_toda_group_proof_presentation(replay)
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar,
  )
  return (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  )


def _block_index_by_step_id(blocks):
  return {
    id(step): block_index
    for block_index, block in enumerate(blocks)
    for step in block.steps
  }


def _argument_index_by_conclusion_block_id(arguments):
  return {
    id(argument.conclusion_block): argument_index
    for argument_index, argument in enumerate(arguments)
  }


def _direct_block_dependencies(
  presentation,
  semantic_sidecar,
  blocks,
):
  block_index = _block_index_by_step_id(blocks)
  dependencies = [set() for _ in blocks]
  edge_kinds = {}

  def add(dependent_step, prerequisite_step, kind):
    dependent = block_index[id(dependent_step)]
    prerequisite = block_index[id(prerequisite_step)]
    if dependent == prerequisite:
      return
    dependencies[dependent].add(prerequisite)
    edge_kinds.setdefault(
      (dependent, prerequisite),
      set(),
    ).add(kind)

  for edge in presentation.edges:
    add(
      edge.parent_step,
      edge.premise_step,
      "presentation",
    )

  for semantic in semantic_sidecar.dependency_semantics:
    add(
      semantic.dependent_step,
      semantic.prerequisite_step,
      "semantic:" + semantic.role.value,
    )

  return (
    tuple(tuple(sorted(items)) for items in dependencies),
    edge_kinds,
  )


def _reachable_paths(dependencies, start):
  paths = {start: (start,)}
  queue = deque((start,))

  while queue:
    current = queue.popleft()
    for prerequisite in dependencies[current]:
      if prerequisite in paths:
        continue
      paths[prerequisite] = (
        paths[current] + (prerequisite,)
      )
      queue.append(prerequisite)

  return paths


def _block_role(block):
  role = getattr(block, "role", None)
  return getattr(role, "value", str(role))


def _argument_role(argument):
  role = getattr(argument, "role", None)
  return getattr(role, "value", str(role))


def _print_block(block_index, blocks):
  block = blocks[block_index]
  print(
    f"B{block_index:02d} role={_block_role(block)} "
    f"steps={len(block.steps)}"
  )
  for step in block.steps:
    print("      " + _step_label(step))


def _classify_gap(
  root_conclusion_index,
  gap_conclusion_index,
  path,
  root_argument,
  blocks,
):
  supporting_ids = {
    id(block)
    for block in root_argument.supporting_blocks
  }

  if len(path) == 2:
    return "DIRECT_ARGUMENT_DEPENDENCY"

  first_hop = path[1]
  if id(blocks[first_hop]) in supporting_ids:
    return "VIA_ROOT_SUPPORTING_BLOCK"

  if gap_conclusion_index in path[1:-1]:
    return "PATH_PASSES_ARGUMENT_CONCLUSION"

  return "DEEP_TRANSITIVE_DEPENDENCY"


def audit_target(n, k):
  print("=" * 100)
  print(f"TARGET pi_{n + k}^{n}")
  print("=" * 100)

  for depth in range(MAX_DEPTH + 1):
    try:
      (
        presentation,
        semantic_sidecar,
        blocks,
        arguments,
      ) = _build_state(n, k, depth)
    except Exception as exc:
      print(
        f"depth={depth}: ERROR "
        f"{type(exc).__name__}: {exc}"
      )
      continue

    if not arguments:
      print(
        f"depth={depth}: nodes={len(presentation.nodes)} "
        "arguments=0"
      )
      continue

    root_index = None
    root_step_id = id(presentation.root_step)
    for argument_index, argument in enumerate(arguments):
      if any(
        id(step) == root_step_id
        for step in argument.conclusion_block.steps
      ):
        root_index = argument_index
        break

    if root_index is None:
      print(
        f"depth={depth}: nodes={len(presentation.nodes)} "
        f"arguments={len(arguments)} root_argument=NONE"
      )
      continue

    dependencies, edge_kinds = _direct_block_dependencies(
      presentation,
      semantic_sidecar,
      blocks,
    )
    block_index_by_id = {
      id(block): index
      for index, block in enumerate(blocks)
    }
    argument_by_conclusion_block = (
      _argument_index_by_conclusion_block_id(arguments)
    )

    root_argument = arguments[root_index]
    root_conclusion_index = block_index_by_id[
      id(root_argument.conclusion_block)
    ]
    paths = _reachable_paths(
      dependencies,
      root_conclusion_index,
    )

    closure_argument_indices = []
    for block_index in paths:
      argument_index = argument_by_conclusion_block.get(
        id(blocks[block_index])
      )
      if (
        argument_index is not None
        and argument_index != root_index
      ):
        closure_argument_indices.append(argument_index)

    closure_argument_indices = tuple(
      sorted(set(closure_argument_indices))
    )
    direct_children = tuple(
      root_argument.child_argument_indices
    )
    gaps = tuple(
      index
      for index in closure_argument_indices
      if index not in direct_children
    )

    print()
    print(
      f"depth={depth} nodes={len(presentation.nodes)} "
      f"blocks={len(blocks)} arguments={len(arguments)} "
      f"semantic_dependencies="
      f"{len(semantic_sidecar.dependency_semantics)}"
    )
    print(
      f"root=A{root_index:02d} "
      f"role={_argument_role(root_argument)} "
      f"direct_children={direct_children} "
      f"closure_arguments={closure_argument_indices} "
      f"gaps={gaps}"
    )

    for gap_index in gaps:
      gap_argument = arguments[gap_index]
      gap_conclusion_index = block_index_by_id[
        id(gap_argument.conclusion_block)
      ]
      path = paths[gap_conclusion_index]
      classification = _classify_gap(
        root_conclusion_index,
        gap_conclusion_index,
        path,
        root_argument,
        blocks,
      )

      print("-" * 100)
      print(
        f"GAP A{gap_index:02d} "
        f"role={_argument_role(gap_argument)} "
        f"class={classification}"
      )
      print(
        "path="
        + " -> ".join(
          f"B{block_index:02d}"
          for block_index in path
        )
      )

      for left, right in zip(path, path[1:]):
        kinds = ",".join(
          sorted(
            edge_kinds.get(
              (left, right),
              {"unknown"},
            )
          )
        )
        print(
          f"  B{left:02d} -> B{right:02d} "
          f"[{kinds}]"
        )

      print("  GAP CONCLUSION:")
      _print_block(
        gap_conclusion_index,
        blocks,
      )

      print("  PATH BLOCKS:")
      for block_index in path:
        _print_block(
          block_index,
          blocks,
        )

  print()


def main():
  print(
    "Phase 144-6-R5-4 Argument dependency gap audit"
  )
  print(
    "No production code is modified by this audit."
  )
  print()

  for n, k in TARGETS:
    audit_target(n, k)

  print("=" * 100)
  print("INTERPRETATION GUIDE")
  print("=" * 100)
  print(
    "DIRECT_ARGUMENT_DEPENDENCY: the gap argument "
    "conclusion is a direct dependency of the root; "
    "child_argument_indices should normally already "
    "contain it."
  )
  print(
    "VIA_ROOT_SUPPORTING_BLOCK: the root depends on a "
    "supporting block, and that supporting block depends "
    "transitively on another argument conclusion. This "
    "is the main suspected structural gap."
  )
  print(
    "DEEP_TRANSITIVE_DEPENDENCY: the argument conclusion "
    "is deeper in the proof closure. It must not be "
    "treated as Narrative-required merely because it is "
    "reachable."
  )
  print(
    "Inspect the printed path and edge kinds before "
    "designing the R5 completion policy."
  )


if __name__ == "__main__":
  main()
