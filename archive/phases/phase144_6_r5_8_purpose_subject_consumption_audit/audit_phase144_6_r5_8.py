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



def _contains_value(
  value,
  target,
  seen=None,
):
  if value == target:
    return True

  if seen is None:
    seen = set()

  value_id = id(
    value
  )
  if value_id in seen:
    return False
  seen.add(
    value_id
  )

  if value is None:
    return False

  if isinstance(
    value,
    (
      str,
      bytes,
      int,
      float,
      bool,
    ),
  ):
    return False

  if isinstance(
    value,
    dict,
  ):
    return any(
      _contains_value(
        key,
        target,
        seen,
      )
      or _contains_value(
        item,
        target,
        seen,
      )
      for key, item in value.items()
    )

  if isinstance(
    value,
    (
      tuple,
      list,
      set,
      frozenset,
    ),
  ):
    return any(
      _contains_value(
        item,
        target,
        seen,
      )
      for item in value
    )

  fields = getattr(
    value,
    "__dataclass_fields__",
    None,
  )
  if fields is not None:
    return any(
      _contains_value(
        getattr(
          value,
          field_name,
        ),
        target,
        seen,
      )
      for field_name in fields
    )

  return False


def _parent_consumption_evidence(
  presentation,
  blocks,
  semantic_sidecar,
  arguments,
  parent_index,
  child_index,
):
  parent = arguments[
    parent_index
  ]
  child = arguments[
    child_index
  ]
  child_subject = (
    extract_toda_group_proof_narrative_argument_purpose_subject(
      child
    )
  )

  if child_subject is None:
    return (
      False,
      (),
    )

  local_body = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      parent_index,
    )
  )
  hidden = (
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_body,
      semantic_sidecar,
      parent,
    )
  )

  evidence = []

  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      parent
    )
  )
  if (
    conclusion_step is not None
    and _contains_value(
      conclusion_step.conclusion,
      child_subject,
    )
  ):
    evidence.append(
      "parent_conclusion"
    )

  for block in local_body:
    for step in block.steps:
      if id(
        step
      ) in hidden:
        continue
      if _contains_value(
        step.conclusion,
        child_subject,
      ):
        evidence.append(
          f"visible:{block.role.value}"
        )

  deduplicated = tuple(
    dict.fromkeys(
      evidence
    )
  )
  return (
    bool(
      deduplicated
    ),
    deduplicated,
  )


def _same_subject(
  arguments,
  parent_index,
  child_index,
):
  parent_subject = (
    extract_toda_group_proof_narrative_argument_purpose_subject(
      arguments[
        parent_index
      ]
    )
  )
  child_subject = (
    extract_toda_group_proof_narrative_argument_purpose_subject(
      arguments[
        child_index
      ]
    )
  )
  return (
    parent_subject is not None
    and child_subject is not None
    and parent_subject == child_subject
  )


def main():
  print("=" * 120)
  print("Phase 144-6-R5-8 purpose-subject semantic consumption audit")
  print("=" * 120)
  print(
    "Audit only: compare root reachability with whether a parent Argument's "
    "conclusion or R4-visible local statements actually contain the child "
    "Argument's purpose subject."
  )
  print(
    "No production selection rule is implemented."
  )
  print()

  total_reachable = 0
  total_root_edges = 0
  total_consumed_root_edges = 0
  total_same_subject_root_edges = 0
  total_consumed_or_same_root_edges = 0

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
    total_reachable += len(
      reachable
    )

    print("-" * 120)
    print(
      f"TARGET n={n}, k={k} "
      f"full_depth={full_depth} "
      f"arguments={len(arguments)} "
      f"roots={roots} "
      f"root_reachable_count={len(reachable)}"
    )
    print("-" * 120)

    root_edge_targets = []
    consumed_root_targets = []
    same_subject_root_targets = []
    union_root_targets = []

    for root_index in roots:
      root = arguments[
        root_index
      ]
      print(
        f"ROOT A{root_index:02d} "
        f"subject={_safe_subject_text(root)}"
      )

      for child_index, path in compressed_edges[
        root_index
      ]:
        if child_index not in reachable:
          continue

        child = arguments[
          child_index
        ]
        consumed, evidence = (
          _parent_consumption_evidence(
            presentation,
            blocks,
            semantic_sidecar,
            arguments,
            root_index,
            child_index,
          )
        )
        same_subject = _same_subject(
          arguments,
          root_index,
          child_index,
        )
        selected_signal = (
          consumed
          or same_subject
        )

        root_edge_targets.append(
          child_index
        )
        if consumed:
          consumed_root_targets.append(
            child_index
          )
        if same_subject:
          same_subject_root_targets.append(
            child_index
          )
        if selected_signal:
          union_root_targets.append(
            child_index
          )

        print(
          f"  A{root_index:02d}->A{child_index:02d} "
          f"role={child.role.value} "
          f"depth={_conclusion_depth(child, depth_by_step_id)} "
          f"subject={_safe_subject_text(child)}"
        )
        print(
          f"    semantic_consumption={consumed} "
          f"same_purpose_subject={same_subject} "
          f"consumed_or_same={selected_signal} "
          f"evidence={evidence} "
          f"path_len={len(path) - 1}"
        )

    total_root_edges += len(
      root_edge_targets
    )
    total_consumed_root_edges += len(
      consumed_root_targets
    )
    total_same_subject_root_edges += len(
      same_subject_root_targets
    )
    total_consumed_or_same_root_edges += len(
      union_root_targets
    )

    print(
      f"root_edge_targets={tuple(root_edge_targets)}"
    )
    print(
      f"semantic_consumed_root_targets={tuple(consumed_root_targets)}"
    )
    print(
      f"same_subject_root_targets={tuple(same_subject_root_targets)}"
    )
    print(
      f"consumed_or_same_root_targets={tuple(union_root_targets)}"
    )

    print("CHAIN AUDIT")
    for parent_index in (
      tuple(
        roots
      )
      + tuple(
        reachable
      )
    ):
      for child_index, path in compressed_edges[
        parent_index
      ]:
        if child_index not in reachable:
          continue

        consumed, evidence = (
          _parent_consumption_evidence(
            presentation,
            blocks,
            semantic_sidecar,
            arguments,
            parent_index,
            child_index,
          )
        )
        same_subject = _same_subject(
          arguments,
          parent_index,
          child_index,
        )
        if not (
          consumed
          or same_subject
        ):
          continue

        parent = arguments[
          parent_index
        ]
        child = arguments[
          child_index
        ]
        print(
          f"  A{parent_index:02d}({parent.role.value})"
          f" -> A{child_index:02d}({child.role.value}) "
          f"consumed={consumed} "
          f"same_subject={same_subject} "
          f"evidence={evidence} "
          f"path_len={len(path) - 1}"
        )
    print()

  print("=" * 120)
  print("SUMMARY")
  print("=" * 120)
  print(
    f"total_root_reachable_arguments={total_reachable}"
  )
  print(
    f"total_compressed_root_edges={total_root_edges}"
  )
  print(
    f"semantic_consumed_root_edges={total_consumed_root_edges}"
  )
  print(
    f"same_subject_root_edges={total_same_subject_root_edges}"
  )
  print(
    f"consumed_or_same_root_edges={total_consumed_or_same_root_edges}"
  )
  print()
  print("=" * 120)
  print("INTERPRETATION GUIDE")
  print("=" * 120)
  print(
    "1. semantic_consumption=True means the child purpose subject occurs in "
    "the parent's conclusion or in a statement retained by the current R4 "
    "visible frontier."
  )
  print(
    "2. same_purpose_subject=True detects Argument chains about the same "
    "mathematical subject. It is intentionally separate because a group-"
    "structure Argument has a group as its subject while an Order/Definition "
    "Argument normally has an element as its subject."
  )
  print(
    "3. For pi_6^3, a promising result is that the root selects the Order "
    "Argument for nu-prime by semantic consumption and that the Order/Definition "
    "chain for nu-prime is visible in CHAIN AUDIT."
  )
  print(
    "4. For the larger groups, the signal is useful only if it substantially "
    "reduces the many deep root-reachable Definitions seen in R5-6/R5-7."
  )
  print(
    "5. This audit does not implement transitive selection. R5-9, if needed, "
    "should test a precise traversal rule only after inspecting these signals."
  )


if __name__ == "__main__":
  main()
