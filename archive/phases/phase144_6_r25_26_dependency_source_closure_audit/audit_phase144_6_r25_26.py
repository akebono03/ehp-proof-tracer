from collections import Counter

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
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
  build_complete_toda_group_result_proof_replay,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def _data(n, k):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[0]
    .source_candidate
    .group_result
  )
  replay = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=sidecar,
    )
  )
  return (
    presentation,
    sidecar,
    blocks,
    arguments,
  )


def _block_index_by_step_id(blocks):
  return {
    id(step): block_index
    for block_index, block in enumerate(
      blocks
    )
    for step in block.steps
  }


def _empty_dependencies(blocks):
  return [
    []
    for _ in blocks
  ]


def _add_dependency(
  dependencies,
  dependent_index,
  prerequisite_index,
):
  if dependent_index == prerequisite_index:
    return
  if prerequisite_index in dependencies[
    dependent_index
  ]:
    return
  dependencies[
    dependent_index
  ].append(
    prerequisite_index
  )


def _dependency_sources(
  presentation,
  sidecar,
  blocks,
):
  index_by_step_id = (
    _block_index_by_step_id(
      blocks
    )
  )
  proof = _empty_dependencies(
    blocks
  )
  semantic = _empty_dependencies(
    blocks
  )

  for edge in presentation.edges:
    _add_dependency(
      proof,
      index_by_step_id[
        id(
          edge.parent_step
        )
      ],
      index_by_step_id[
        id(
          edge.premise_step
        )
      ],
    )

  for item in sidecar.dependency_semantics:
    _add_dependency(
      semantic,
      index_by_step_id[
        id(
          item.dependent_step
        )
      ],
      index_by_step_id[
        id(
          item.prerequisite_step
        )
      ],
    )

  combined = _empty_dependencies(
    blocks
  )
  for index in range(
    len(
      blocks
    )
  ):
    for dependency_index in (
      proof[index]
      + semantic[index]
    ):
      _add_dependency(
        combined,
        index,
        dependency_index,
      )

  return (
    tuple(
      tuple(row)
      for row in proof
    ),
    tuple(
      tuple(row)
      for row in semantic
    ),
    tuple(
      tuple(row)
      for row in combined
    ),
  )


def _closure(
  dependencies,
  start_index,
  boundary_indices,
):
  visited = set()
  active = set()

  def visit(block_index):
    if block_index in boundary_indices:
      return
    if block_index in visited:
      return
    if block_index in active:
      return

    active.add(
      block_index
    )
    for dependency_index in dependencies[
      block_index
    ]:
      visit(
        dependency_index
      )
    active.remove(
      block_index
    )
    visited.add(
      block_index
    )

  for dependency_index in dependencies[
    start_index
  ]:
    visit(
      dependency_index
    )

  visited.discard(
    start_index
  )
  return frozenset(
    visited
  )


def _exactness_count(
  indices,
  blocks,
):
  return sum(
    blocks[index].role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .EXACTNESS
    for index in indices
  )


def _role_counts(
  indices,
  blocks,
):
  return dict(
    Counter(
      blocks[index].role.value
      for index in indices
    )
  )


def main():
  print(
    "Phase 144-6 R25-26 dependency-source closure audit"
  )
  print(
    "Production changes: none"
  )
  print()

  for n, k in TARGETS:
    (
      presentation,
      sidecar,
      blocks,
      arguments,
    ) = _data(
      n,
      k,
    )
    (
      proof_dependencies,
      semantic_dependencies,
      combined_dependencies,
    ) = _dependency_sources(
      presentation,
      sidecar,
      blocks,
    )

    conclusion_indices = tuple(
      next(
        index
        for index, block in enumerate(
          blocks
        )
        if block is argument.conclusion_block
      )
      for argument in arguments
    )

    print(
      "=" * 78
    )
    print(
      f"pi_{n + k}^{n}"
    )
    print(
      "=" * 78
    )
    print(
      "nodes:",
      len(
        presentation.nodes
      ),
    )
    print(
      "blocks:",
      len(
        blocks
      ),
    )
    print(
      "proof edges:",
      len(
        presentation.edges
      ),
    )
    print(
      "semantic dependencies:",
      len(
        sidecar.dependency_semantics
      ),
    )
    print(
      "arguments:",
      len(
        arguments
      ),
    )

    rows = []

    for argument_index, argument in enumerate(
      arguments
    ):
      conclusion_index = conclusion_indices[
        argument_index
      ]
      boundary = set(
        conclusion_indices
      )
      boundary.discard(
        conclusion_index
      )

      proof_closure = _closure(
        proof_dependencies,
        conclusion_index,
        boundary,
      )
      semantic_closure = _closure(
        semantic_dependencies,
        conclusion_index,
        boundary,
      )
      combined_closure = _closure(
        combined_dependencies,
        conclusion_index,
        boundary,
      )

      proof_only = (
        combined_closure
        - semantic_closure
      )
      semantic_only = (
        combined_closure
        - proof_closure
      )
      interaction_only = (
        combined_closure
        - (
          proof_closure
          | semantic_closure
        )
      )

      rows.append(
        (
          len(
            combined_closure
          ),
          argument_index,
          argument,
          conclusion_index,
          proof_closure,
          semantic_closure,
          combined_closure,
          proof_only,
          semantic_only,
          interaction_only,
        )
      )

    rows.sort(
      reverse=True,
      key=lambda row: row[0],
    )

    for (
      combined_count,
      argument_index,
      argument,
      conclusion_index,
      proof_closure,
      semantic_closure,
      combined_closure,
      proof_only,
      semantic_only,
      interaction_only,
    ) in rows[:8]:
      print()
      print(
        f"argument {argument_index:03d} "
        f"role={argument.role.value} "
        f"conclusion=B{conclusion_index}"
      )
      print(
        "  direct proof:",
        len(
          proof_dependencies[
            conclusion_index
          ]
        ),
        "direct semantic:",
        len(
          semantic_dependencies[
            conclusion_index
          ]
        ),
        "direct combined:",
        len(
          combined_dependencies[
            conclusion_index
          ]
        ),
      )
      print(
        "  proof closure:",
        len(
          proof_closure
        ),
        "exactness=",
        _exactness_count(
          proof_closure,
          blocks,
        ),
      )
      print(
        "  semantic closure:",
        len(
          semantic_closure
        ),
        "exactness=",
        _exactness_count(
          semantic_closure,
          blocks,
        ),
      )
      print(
        "  combined closure:",
        combined_count,
        "exactness=",
        _exactness_count(
          combined_closure,
          blocks,
        ),
      )
      print(
        "  combined-minus-semantic:",
        len(
          proof_only
        ),
      )
      print(
        "  combined-minus-proof:",
        len(
          semantic_only
        ),
      )
      print(
        "  interaction-only:",
        len(
          interaction_only
        ),
        "exactness=",
        _exactness_count(
          interaction_only,
          blocks,
        ),
      )
      print(
        "  combined role counts:",
        _role_counts(
          combined_closure,
          blocks,
        ),
      )

    print()


if __name__ == "__main__":
  main()
