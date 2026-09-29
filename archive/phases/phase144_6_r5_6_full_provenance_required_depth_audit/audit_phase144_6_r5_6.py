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


def _build_at_depth(
  group_result,
  depth,
):
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


def _reachable_argument_indices(
  direct_argument_dependencies,
  roots,
):
  visited = set()
  pending = list(
    roots
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

  for root_index in roots:
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


def _step_depth_by_id(
  provenance,
):
  return {
    id(node.proof_step): node.shortest_depth
    for node in provenance.nodes
  }


def _argument_conclusion_depth(
  argument,
  step_depth_by_id,
):
  return max(
    step_depth_by_id[
      id(step)
    ]
    for step in argument.conclusion_block.steps
  )


def _argument_signature(
  argument,
):
  return (
    argument.role.value,
    tuple(
      type(step.conclusion).__name__
      for step in argument.conclusion_block.steps
    ),
  )


def _root_required_signature(
  arguments,
  root_reachable,
):
  return tuple(
    _argument_signature(
      arguments[index]
    )
    for index in root_reachable
  )


def _first_depth_matching_full_required_signature(
  group_result,
  full_signature,
  full_depth,
):
  matches = []

  for depth in range(
    full_depth + 1
  ):
    (
      _,
      presentation,
      _,
      blocks,
      arguments,
      direct_dependencies,
    ) = _build_at_depth(
      group_result,
      depth,
    )

    compressed = (
      _compressed_direct_argument_dependencies(
        blocks,
        arguments,
        direct_dependencies,
      )
    )
    roots = _root_indices(
      presentation,
      arguments,
    )
    reachable = _reachable_argument_indices(
      compressed,
      roots,
    )
    signature = _root_required_signature(
      arguments,
      reachable,
    )

    if signature == full_signature:
      matches.append(
        depth
      )

  if not matches:
    return None

  return min(
    matches
  )


def main():
  print("=" * 120)
  print("Phase 144-6-R5-6 Full-provenance required Narrative depth audit")
  print("=" * 120)
  print(
    "Question: can full provenance determine the required Narrative depth "
    "before rendering a truncated replay?"
  )
  print()

  all_conclusion_predictions_match = True
  any_full_depth_excess = False

  for n, k in TARGETS:
    print("-" * 120)
    print(f"TARGET n={n}, k={k}")
    print("-" * 120)

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

    (
      _,
      full_presentation,
      _,
      full_blocks,
      full_arguments,
      full_direct_dependencies,
    ) = _build_at_depth(
      group_result,
      full_depth,
    )

    compressed = (
      _compressed_direct_argument_dependencies(
        full_blocks,
        full_arguments,
        full_direct_dependencies,
      )
    )
    roots = _root_indices(
      full_presentation,
      full_arguments,
    )
    required = _reachable_argument_indices(
      compressed,
      roots,
    )

    step_depth_by_id = _step_depth_by_id(
      provenance
    )

    required_conclusion_depths = tuple(
      (
        index,
        _argument_conclusion_depth(
          full_arguments[index],
          step_depth_by_id,
        ),
      )
      for index in required
    )

    predicted_depth = max(
      (
        depth
        for _, depth in required_conclusion_depths
      ),
      default=0,
    )

    full_signature = (
      _root_required_signature(
        full_arguments,
        required,
      )
    )

    first_matching_depth = (
      _first_depth_matching_full_required_signature(
        group_result,
        full_signature,
        full_depth,
      )
    )

    prediction_matches = (
      predicted_depth
      == first_matching_depth
    )
    all_conclusion_predictions_match = (
      all_conclusion_predictions_match
      and prediction_matches
    )

    if predicted_depth < full_depth:
      any_full_depth_excess = True

    print(
      f"full_provenance_nodes={len(provenance.nodes)} "
      f"full_provenance_edges={len(provenance.edges)} "
      f"full_depth={full_depth}"
    )
    print(
      f"full_arguments={len(full_arguments)} "
      f"roots={roots}"
    )
    print(
      f"full_compressed_root_reachable={required}"
    )
    print(
      f"required_argument_conclusion_depths="
      f"{required_conclusion_depths}"
    )
    print(
      f"predicted_depth_from_required_conclusions="
      f"{predicted_depth}"
    )
    print(
      f"first_depth_matching_full_required_signature="
      f"{first_matching_depth}"
    )
    print(
      f"prediction_matches="
      f"{prediction_matches}"
    )
    print(
      f"full_depth_excess="
      f"{full_depth - predicted_depth}"
    )

    for index in required:
      argument = full_arguments[
        index
      ]
      print(
        f"  A{index:02d}: "
        f"role={argument.role.value} "
        f"conclusion_depth="
        f"{_argument_conclusion_depth(argument, step_depth_by_id)} "
        f"children={compressed[index]} "
        f"conclusion_types="
        f"{tuple(type(step.conclusion).__name__ for step in argument.conclusion_block.steps)}"
      )

    print()

  print("=" * 120)
  print("INTERPRETATION GUIDE")
  print("=" * 120)
  print(
    "If prediction_matches=True for all six targets, the maximum shortest_depth "
    "of full-provenance root-required Argument conclusions is a viable candidate "
    "for precomputing Narrative depth."
  )
  print(
    "If prediction_matches=False, Argument conclusion depth alone is insufficient; "
    "supporting blocks required to construct the same Narrative Argument structure "
    "must also contribute to the depth calculation."
  )
  print(
    "A positive full_depth_excess shows that rendering the entire provenance is "
    "deeper than necessary for the root-required Argument signature."
  )
  print(
    "This audit does not yet claim that every root-reachable Argument should be "
    "visible in prose. It tests only whether the full graph can determine a stable "
    "required Argument set and its replay depth in advance."
  )
  print()
  print(
    f"all_conclusion_predictions_match="
    f"{all_conclusion_predictions_match}"
  )
  print(
    f"any_full_depth_excess="
    f"{any_full_depth_excess}"
  )


if __name__ == "__main__":
  main()
