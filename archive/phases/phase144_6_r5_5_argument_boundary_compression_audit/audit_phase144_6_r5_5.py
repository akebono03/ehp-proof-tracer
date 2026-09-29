from collections import deque

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  _argument_direct_dependency_indices,
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
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)

MAX_DEPTH = 6


def _build(n, k, depth):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=depth,
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
  direct_dependencies = (
    _argument_direct_dependency_indices(
      presentation,
      blocks,
      semantic_sidecar,
    )
  )
  return (
    replay,
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    direct_dependencies,
  )


def _argument_conclusion_block_indices(
  blocks,
  arguments,
):
  block_index_by_identity = {
    id(block): index
    for index, block in enumerate(blocks)
  }
  return tuple(
    block_index_by_identity[
      id(argument.conclusion_block)
    ]
    for argument in arguments
  )


def _compressed_direct_argument_dependencies(
  blocks,
  arguments,
  direct_dependencies,
):
  conclusion_block_indices = (
    _argument_conclusion_block_indices(
      blocks,
      arguments,
    )
  )
  argument_index_by_conclusion_block_index = {
    block_index: argument_index
    for argument_index, block_index in enumerate(
      conclusion_block_indices
    )
  }

  compressed = []

  for argument_index, conclusion_block_index in enumerate(
    conclusion_block_indices
  ):
    found = []
    visited_non_argument_blocks = set()
    pending = deque(
      direct_dependencies[
        conclusion_block_index
      ]
    )

    while pending:
      block_index = pending.popleft()

      boundary_argument_index = (
        argument_index_by_conclusion_block_index.get(
          block_index
        )
      )

      if boundary_argument_index is not None:
        if (
          boundary_argument_index != argument_index
          and boundary_argument_index not in found
        ):
          found.append(
            boundary_argument_index
          )
        continue

      if block_index in visited_non_argument_blocks:
        continue

      visited_non_argument_blocks.add(
        block_index
      )

      for dependency_index in direct_dependencies[
        block_index
      ]:
        pending.append(
          dependency_index
        )

    compressed.append(
      tuple(
        found
      )
    )

  return tuple(
    compressed
  )


def _reachable_argument_indices(
  direct_argument_dependencies,
  root_indices,
):
  visited = set()
  pending = list(
    root_indices
  )

  while pending:
    argument_index = pending.pop()

    for child_index in direct_argument_dependencies[
      argument_index
    ]:
      if child_index in visited:
        continue
      visited.add(
        child_index
      )
      pending.append(
        child_index
      )

  for root_index in root_indices:
    visited.discard(
      root_index
    )

  return tuple(
    index
    for index in range(
      len(
        direct_argument_dependencies
      )
    )
    if index in visited
  )


def _argument_signature(
  argument,
):
  conclusion_types = tuple(
    type(step.conclusion).__name__
    for step in argument.conclusion_block.steps
  )
  return (
    argument.role.value,
    conclusion_types,
  )


def _format_argument(
  index,
  argument,
):
  return (
    f"A{index:02d} "
    f"role={argument.role.value} "
    f"conclusion_types="
    f"{tuple(type(step.conclusion).__name__ for step in argument.conclusion_block.steps)}"
  )


def main():
  print("=" * 120)
  print("Phase 144-6-R5-5 Argument-boundary dependency compression audit")
  print("=" * 120)
  print(
    "Rule under audit: traverse block dependencies from each Argument conclusion; "
    "when another Argument conclusion is first encountered, record it as an "
    "Argument dependency and stop traversal through that boundary."
  )
  print()

  global_mismatch_count = 0
  global_late_required_count = 0

  for n, k in TARGETS:
    print("-" * 120)
    print(f"TARGET n={n}, k={k}")
    print("-" * 120)

    previous_root_signature = None

    for depth in range(
      MAX_DEPTH + 1
    ):
      (
        replay,
        presentation,
        semantic_sidecar,
        blocks,
        arguments,
        direct_dependencies,
      ) = _build(
        n,
        k,
        depth,
      )

      compressed = (
        _compressed_direct_argument_dependencies(
          blocks,
          arguments,
          direct_dependencies,
        )
      )

      existing = tuple(
        argument.child_argument_indices
        for argument in arguments
      )

      root_indices = tuple(
        index
        for index, argument in enumerate(
          arguments
        )
        if (
          argument.role
          is TodaGroupProofNarrativeArgumentRole
          .ESTABLISH_GROUP_STRUCTURE
          and argument.conclusion_block
          is not None
          and argument.conclusion_block.steps
          and argument.conclusion_block.steps[
            0
          ] is presentation.root_step
        )
      )

      compressed_root_reachable = (
        _reachable_argument_indices(
          compressed,
          root_indices,
        )
      )
      existing_root_reachable = (
        _reachable_argument_indices(
          existing,
          root_indices,
        )
      )

      added_by_compression = tuple(
        index
        for index in compressed_root_reachable
        if index not in existing_root_reachable
      )

      root_signature = tuple(
        _argument_signature(
          arguments[index]
        )
        for index in compressed_root_reachable
      )

      changed = (
        previous_root_signature is not None
        and root_signature != previous_root_signature
      )

      if changed:
        global_late_required_count += 1

      print(
        f"depth={depth}: "
        f"replay_steps={len(replay.steps)} "
        f"blocks={len(blocks)} "
        f"arguments={len(arguments)} "
        f"roots={root_indices}"
      )
      print(
        "  existing_root_reachable="
        f"{existing_root_reachable}"
      )
      print(
        "  compressed_root_reachable="
        f"{compressed_root_reachable}"
      )
      print(
        "  added_by_compression="
        f"{added_by_compression}"
      )
      if previous_root_signature is None:
        print(
          "  compressed_root_signature_changed="
          "N/A"
        )
      else:
        print(
          "  compressed_root_signature_changed="
          f"{changed}"
        )

      for root_index in root_indices:
        print(
          f"  ROOT A{root_index:02d}: "
          f"existing_children={existing[root_index]} "
          f"compressed_children={compressed[root_index]}"
        )

      for index in added_by_compression:
        global_mismatch_count += 1
        print(
          "    + "
          + _format_argument(
            index,
            arguments[index],
          )
        )

      for argument_index, argument in enumerate(
        arguments
      ):
        if compressed[
          argument_index
        ] == existing[
          argument_index
        ]:
          continue

        print(
          f"  EDGE GAP A{argument_index:02d}: "
          f"existing={existing[argument_index]} "
          f"compressed={compressed[argument_index]}"
        )
        for child_index in compressed[
          argument_index
        ]:
          if child_index in existing[
            argument_index
          ]:
            continue
          print(
            "    boundary-add "
            + _format_argument(
              child_index,
              arguments[
                child_index
              ],
            )
          )

      previous_root_signature = (
        root_signature
      )

    print()

  print("=" * 120)
  print("INTERPRETATION GUIDE")
  print("=" * 120)
  print(
    "1. compressed_children may be a strict superset of existing_children. "
    "That is expected when a dependency passes through non-Argument supporting blocks."
  )
  print(
    "2. A boundary-add is structurally stronger than an arbitrary transitive closure: "
    "the traversal stops at the first encountered Argument conclusion."
  )
  print(
    "3. If compressed_root_reachable contains the R5-4 VIA_ROOT_SUPPORTING_BLOCK gaps "
    "without pulling in arguments beyond an intervening Argument boundary, the compression rule is supported."
  )
  print(
    "4. compressed_root_signature_changed=True at a later depth means boundary compression "
    "alone is NOT a stopping criterion. It only defines Argument dependency; a separate completeness signal is still required."
  )
  print(
    "5. Inspect any unexpectedly large compressed_root_reachable set before production changes. "
    "Reachability alone must not be equated with Narrative visibility."
  )
  print()
  print(
    f"summary_boundary_additions_seen={global_mismatch_count}"
  )
  print(
    f"summary_late_signature_changes={global_late_required_count}"
  )


if __name__ == "__main__":
  main()
