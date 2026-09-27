from collections import deque

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  _argument_direct_dependency_indices,
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
  extract_toda_group_proof_narrative_argument_purpose_subject,
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
  extract_toda_recursive_proof_provenance,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def _group_result(n, k):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  return (
    report.candidates[
      0
    ].source_candidate.group_result
  )


def _full_state(n, k):
  group_result = _group_result(
    n,
    k,
  )
  provenance = (
    extract_toda_recursive_proof_provenance(
      group_result
    )
  )
  full_depth = max(
    node.shortest_depth
    for node in provenance.nodes
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=full_depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )
  dependencies = _argument_direct_dependency_indices(
    presentation,
    blocks,
    semantic_sidecar,
  )
  return (
    provenance,
    full_depth,
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    dependencies,
  )


def _argument_block_indices(
  blocks,
  arguments,
):
  block_index_by_id = {
    id(block): index
    for index, block in enumerate(blocks)
  }
  return tuple(
    block_index_by_id[
      id(argument.conclusion_block)
    ]
    for argument in arguments
  )


def _compressed_edges_with_paths(
  blocks,
  arguments,
  dependencies,
):
  conclusion_indices = _argument_block_indices(
    blocks,
    arguments,
  )
  argument_by_block = {
    block_index: argument_index
    for argument_index, block_index in enumerate(
      conclusion_indices
    )
  }
  result = []

  for source_argument_index, source_block_index in enumerate(
    conclusion_indices
  ):
    found = {}
    pending = deque(
      (
        dependency_index,
        (
          source_block_index,
          dependency_index,
        ),
      )
      for dependency_index in dependencies[
        source_block_index
      ]
    )
    visited = set()

    while pending:
      block_index, path = pending.popleft()

      boundary_argument_index = argument_by_block.get(
        block_index
      )
      if boundary_argument_index is not None:
        if boundary_argument_index != source_argument_index:
          found.setdefault(
            boundary_argument_index,
            path,
          )
        continue

      if block_index in visited:
        continue
      visited.add(
        block_index
      )

      for dependency_index in dependencies[
        block_index
      ]:
        pending.append(
          (
            dependency_index,
            path + (
              dependency_index,
            ),
          )
        )

    result.append(
      tuple(
        (
          target_argument_index,
          found[
            target_argument_index
          ],
        )
        for target_argument_index in found
      )
    )

  return tuple(
    result
  )


def _root_indices(
  presentation,
  arguments,
):
  return tuple(
    index
    for index, argument in enumerate(
      arguments
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE
      and any(
        step is presentation.root_step
        for step in argument.conclusion_block.steps
      )
    )
  )


def _root_reachable(
  compressed_edges,
  roots,
):
  visited = set()
  pending = list(
    roots
  )

  while pending:
    source_index = pending.pop()
    for target_index, _ in compressed_edges[
      source_index
    ]:
      if target_index in visited:
        continue
      visited.add(
        target_index
      )
      pending.append(
        target_index
      )

  for root_index in roots:
    visited.discard(
      root_index
    )

  return tuple(
    index
    for index in range(
      len(
        compressed_edges
      )
    )
    if index in visited
  )


def _visible_step_ids_for_argument(
  presentation,
  blocks,
  semantic_sidecar,
  arguments,
  argument_index,
):
  argument = arguments[
    argument_index
  ]
  local_body = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
  )
  hidden = (
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_body,
      semantic_sidecar,
      argument,
    )
  )
  return frozenset(
    id(step)
    for block in local_body
    for step in block.steps
    if id(step) not in hidden
  )


def _edge_frontier_contact(
  path,
  blocks,
  visible_step_ids,
):
  non_boundary_indices = path[
    1:-1
  ]
  visible_path_blocks = []

  for block_index in non_boundary_indices:
    block = blocks[
      block_index
    ]
    if any(
      id(step) in visible_step_ids
      for step in block.steps
    ):
      visible_path_blocks.append(
        block_index
      )

  return tuple(
    visible_path_blocks
  )


def _safe_subject_text(
  argument,
):
  subject = (
    extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )
  )
  if subject is None:
    return "None"
  return str(
    subject
  )


def _conclusion_type_names(
  argument,
):
  return tuple(
    type(step.conclusion).__name__
    for step in argument.conclusion_block.steps
  )


def _conclusion_depth(
  argument,
  depth_by_step_id,
):
  return max(
    depth_by_step_id[
      id(step)
    ]
    for step in argument.conclusion_block.steps
  )


def main():
  print("=" * 120)
  print("Phase 144-6-R5-7 Narrative-required Argument selection audit")
  print("=" * 120)
  print(
    "Audit question: among full-provenance root-reachable Arguments, which "
    "compressed Argument edges actually touch the parent's R4 visible Narrative frontier?"
  )
  print(
    "No selection rule is implemented. This script inventories structural signals only."
  )
  print()

  total_root_reachable = 0
  total_edges = 0
  total_frontier_contact_edges = 0
  total_no_frontier_contact_edges = 0

  for n, k in TARGETS:
    (
      provenance,
      full_depth,
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      dependencies,
    ) = _full_state(
      n,
      k,
    )

    depth_by_step_id = {
      id(node.proof_step): node.shortest_depth
      for node in provenance.nodes
    }
    compressed_edges = _compressed_edges_with_paths(
      blocks,
      arguments,
      dependencies,
    )
    roots = _root_indices(
      presentation,
      arguments,
    )
    reachable = _root_reachable(
      compressed_edges,
      roots,
    )
    total_root_reachable += len(
      reachable
    )

    visible_by_argument = {
      index: _visible_step_ids_for_argument(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        index,
      )
      for index in (
        set(
          roots
        )
        | set(
          reachable
        )
      )
    }

    print("-" * 120)
    print(
      f"TARGET n={n}, k={k} "
      f"full_depth={full_depth} "
      f"arguments={len(arguments)} "
      f"roots={roots} "
      f"root_reachable_count={len(reachable)}"
    )
    print("-" * 120)

    incoming = {
      index: []
      for index in reachable
    }

    traversal_sources = tuple(
      roots
    ) + tuple(
      reachable
    )

    for source_index in traversal_sources:
      if source_index >= len(
        compressed_edges
      ):
        continue

      visible_step_ids = visible_by_argument.get(
        source_index,
        frozenset(),
      )

      for target_index, path in compressed_edges[
        source_index
      ]:
        if target_index not in incoming:
          continue

        contact_blocks = _edge_frontier_contact(
          path,
          blocks,
          visible_step_ids,
        )
        has_contact = bool(
          contact_blocks
        )
        total_edges += 1
        if has_contact:
          total_frontier_contact_edges += 1
        else:
          total_no_frontier_contact_edges += 1

        incoming[
          target_index
        ].append(
          (
            source_index,
            path,
            contact_blocks,
          )
        )

    for target_index in reachable:
      argument = arguments[
        target_index
      ]
      incoming_edges = incoming[
        target_index
      ]
      contact_incoming = tuple(
        item
        for item in incoming_edges
        if item[
          2
        ]
      )
      direct_from_root = any(
        source_index in roots
        for source_index, _, _ in incoming_edges
      )

      print(
        f"A{target_index:02d} "
        f"role={argument.role.value} "
        f"depth={_conclusion_depth(argument, depth_by_step_id)} "
        f"subject={_safe_subject_text(argument)} "
        f"conclusion_types={_conclusion_type_names(argument)}"
      )
      print(
        f"  incoming_boundary_edges={len(incoming_edges)} "
        f"frontier_contact_incoming={len(contact_incoming)} "
        f"direct_from_root={direct_from_root}"
      )

      for (
        source_index,
        path,
        contact_blocks,
      ) in incoming_edges:
        path_roles = tuple(
          blocks[
            block_index
          ].role.value
          for block_index in path
        )
        print(
          f"    A{source_index:02d}->A{target_index:02d} "
          f"path_len={len(path) - 1} "
          f"frontier_contact={bool(contact_blocks)} "
          f"contact_blocks={contact_blocks} "
          f"path_roles={path_roles}"
        )

    print()

  print("=" * 120)
  print("SUMMARY")
  print("=" * 120)
  print(
    f"total_root_reachable_arguments={total_root_reachable}"
  )
  print(
    f"total_compressed_edges_into_root_closure={total_edges}"
  )
  print(
    f"frontier_contact_edges={total_frontier_contact_edges}"
  )
  print(
    f"no_frontier_contact_edges={total_no_frontier_contact_edges}"
  )
  print()
  print("=" * 120)
  print("INTERPRETATION GUIDE")
  print("=" * 120)
  print(
    "1. frontier_contact=True means the compressed dependency path passes through "
    "at least one non-Argument block that the current R4 frontier would keep visible "
    "inside the parent Argument."
  )
  print(
    "2. frontier_contact=False means the child Argument is reachable through proof "
    "dependencies, but the intermediate path contributes nothing to the parent's "
    "current visible Narrative frontier."
  )
  print(
    "3. If the small benchmark pi_6^3 required Order/Definition Arguments have "
    "frontier contact while deep closure-only Arguments in the larger groups mostly "
    "do not, frontier contact is a promising generic Narrative-required signal."
  )
  print(
    "4. If both desired and clearly deep/internal Arguments show the same contact "
    "pattern, frontier contact alone is insufficient and R5-8 must inspect stronger "
    "semantic signals such as purpose-subject consumption or discourse ownership."
  )
  print(
    "5. Do not interpret root reachability itself as Narrative visibility. "
    "R5-6 already showed that full root closure can absorb nearly every Argument."
  )


if __name__ == "__main__":
  main()
