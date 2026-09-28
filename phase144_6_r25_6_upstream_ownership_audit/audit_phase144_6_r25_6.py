from collections import deque

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
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
from toda_proof_dependency import (
  TodaProofDependencyRole,
  extract_toda_recursive_proof_provenance,
)


def _render_step(step):
  rendered = _render_generic_narrative_step(step)
  if rendered:
    return rendered
  return type(step.conclusion).__name__


def _describe(step, depth_by_id=None, role_by_id=None):
  parts = [
    f"id={id(step)}",
    f"type={type(step.conclusion).__name__}",
  ]
  if depth_by_id is not None and id(step) in depth_by_id:
    parts.append(f"depth={depth_by_id[id(step)]}")
  if role_by_id is not None and id(step) in role_by_id:
    parts.append(f"role={role_by_id[id(step)].value}")
  parts.append(f"text={_render_step(step)!r}")
  return " ".join(parts)


def _find_pi5_3(step):
  compact = _render_step(step).replace(" ", "")
  return (
    r"\pi_{5}^{3}" in compact
    or "π_{5}^{3}" in compact
    or "π_5^3" in compact
    or "pi_5^3" in compact
  )


def _shortest_paths_from_root(provenance):
  root = provenance.root_step
  children = {}
  for edge in provenance.edges:
    children.setdefault(id(edge.parent_step), []).append(
      (edge.premise_index, edge.premise_step)
    )

  paths = {id(root): ()}
  queue = deque([root])
  while queue:
    parent = queue.popleft()
    parent_path = paths[id(parent)]
    for premise_index, child in children.get(id(parent), ()):
      if id(child) in paths:
        continue
      paths[id(child)] = parent_path + (
        (parent, premise_index, child),
      )
      queue.append(child)
  return paths


def _print_path(path, depth_by_id, role_by_id):
  if not path:
    print("  path: ROOT")
    return
  print("  path:")
  for parent, premise_index, child in path:
    print(
      "    "
      + _describe(parent, depth_by_id, role_by_id)
    )
    print(f"      -- premise[{premise_index}] -->")
    print(
      "    "
      + _describe(child, depth_by_id, role_by_id)
    )


def _audit_replay_selection(group_result, target_steps):
  print("")
  print("B. Replay selection by max_depth")
  print("-" * 80)
  for max_depth in range(0, 7):
    replay = build_toda_group_result_proof_replay(
      group_result,
      max_depth=max_depth,
    )
    ids = {id(item.proof_step) for item in replay.steps}
    states = tuple(
      (name, id(step) in ids)
      for name, step in target_steps
    )
    print(
      f"max_depth={max_depth} nodes={len(replay.steps)} "
      f"targets={states}"
    )


def _audit_local_body(group_result, max_depth, pi5_steps):
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=max_depth,
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

  print("")
  print(
    f"C. Local-body ownership at max_depth={max_depth}"
  )
  print("-" * 80)
  print(
    "roles="
    + repr(tuple(argument.role.value for argument in arguments))
  )

  block_index_by_id = {
    id(block): index
    for index, block in enumerate(blocks)
  }

  for argument_index, argument in enumerate(arguments):
    local_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    local_step_ids = {
      id(step)
      for block in local_blocks
      for step in block.steps
    }
    print(
      f"A{argument_index:02d} role={argument.role.value} "
      f"conclusion_block=B{block_index_by_id[id(argument.conclusion_block)]:02d} "
      f"local_blocks="
      + repr(tuple(
        block_index_by_id[id(block)]
        for block in local_blocks
      ))
    )
    for pi5_step in pi5_steps:
      if id(pi5_step) in {
        id(node.proof_step)
        for node in presentation.nodes
      }:
        print(
          f"  pi5_3 id={id(pi5_step)} "
          f"in_local_body={id(pi5_step) in local_step_ids}"
        )

  print("")
  print("Direct block dependency edges relevant to pi_5^3")
  print("-" * 80)
  block_by_step_id = {
    id(step): block_index
    for block_index, block in enumerate(blocks)
    for step in block.steps
  }

  for pi5_step in pi5_steps:
    pi5_block = block_by_step_id.get(id(pi5_step))
    if pi5_block is None:
      continue
    print(
      f"pi5_3 id={id(pi5_step)} block=B{pi5_block:02d}"
    )
    for edge in presentation.edges:
      if edge.premise_step is pi5_step:
        parent_block = block_by_step_id.get(id(edge.parent_step))
        print(
          f"  proof edge: B{parent_block:02d} parent "
          f"-- premise[{edge.premise_index}] --> B{pi5_block:02d}"
        )
        print("    parent " + _describe(edge.parent_step))
      if edge.parent_step is pi5_step:
        premise_block = block_by_step_id.get(id(edge.premise_step))
        print(
          f"  proof edge: B{pi5_block:02d} parent "
          f"-- premise[{edge.premise_index}] --> B{premise_block:02d}"
        )
        print("    premise " + _describe(edge.premise_step))

    for semantic in sidecar.dependency_semantics:
      if semantic.prerequisite_step is pi5_step:
        dependent_block = block_by_step_id.get(
          id(semantic.dependent_step)
        )
        print(
          f"  semantic edge: B{dependent_block:02d} dependent "
          f"<-- prerequisite B{pi5_block:02d}"
        )
        print(
          "    dependent "
          + _describe(semantic.dependent_step)
        )
      if semantic.dependent_step is pi5_step:
        prerequisite_block = block_by_step_id.get(
          id(semantic.prerequisite_step)
        )
        print(
          f"  semantic edge: B{pi5_block:02d} dependent "
          f"<-- prerequisite B{prerequisite_block:02d}"
        )
        print(
          "    prerequisite "
          + _describe(semantic.prerequisite_step)
        )


def main():
  report = build_standard_toda_report(n=3, k=3)
  group_result = report.candidates[0].source_candidate.group_result
  provenance = extract_toda_recursive_proof_provenance(group_result)

  depth_by_id = {
    id(node.proof_step): node.shortest_depth
    for node in provenance.nodes
  }
  role_by_id = {
    id(node.proof_step): node.role
    for node in provenance.nodes
  }
  paths = _shortest_paths_from_root(provenance)

  definition_nodes = tuple(
    node
    for node in provenance.nodes
    if node.role is TodaProofDependencyRole.DEFINITION
  )
  pi5_nodes = tuple(
    node
    for node in provenance.nodes
    if _find_pi5_3(node.proof_step)
  )

  print("=" * 80)
  print("Phase 144-6 R25-6 upstream ownership audit")
  print("Production changes: none")
  print("=" * 80)
  print(
    f"provenance_nodes={len(provenance.nodes)} "
    f"provenance_edges={len(provenance.edges)}"
  )

  print("")
  print("A. Unbounded recursive provenance targets")
  print("-" * 80)
  print(f"definition_nodes={len(definition_nodes)}")
  for node in definition_nodes:
    print("definition " + _describe(
      node.proof_step,
      depth_by_id,
      role_by_id,
    ))
    _print_path(
      paths[id(node.proof_step)],
      depth_by_id,
      role_by_id,
    )

  print(f"pi5_3_nodes={len(pi5_nodes)}")
  for node in pi5_nodes:
    print("pi5_3 " + _describe(
      node.proof_step,
      depth_by_id,
      role_by_id,
    ))
    _print_path(
      paths[id(node.proof_step)],
      depth_by_id,
      role_by_id,
    )

  targets = (
    tuple(
      (f"definition[{index}]", node.proof_step)
      for index, node in enumerate(definition_nodes)
    )
    + tuple(
      (f"pi5_3[{index}]", node.proof_step)
      for index, node in enumerate(pi5_nodes)
    )
  )
  _audit_replay_selection(
    group_result,
    targets,
  )

  interesting_depths = sorted({
    1,
    2,
    *(
      node.shortest_depth
      for node in definition_nodes
    ),
  })
  for max_depth in interesting_depths:
    _audit_local_body(
      group_result,
      max_depth,
      tuple(node.proof_step for node in pi5_nodes),
    )

  print("")
  print("=" * 80)
  print("R25-6 AUDIT COMPLETE")
  print("No production repair was applied.")
  print("=" * 80)


if __name__ == "__main__":
  main()
