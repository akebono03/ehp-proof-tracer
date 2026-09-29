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


def _data(
  n,
  k,
):
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
    blocks,
    arguments,
  )


def _proof_dependencies(
  presentation,
  blocks,
):
  block_index_by_step_id = {
    id(
      step
    ): block_index
    for block_index, block in enumerate(
      blocks
    )
    for step in block.steps
  }
  dependencies = [
    []
    for _ in blocks
  ]

  for edge in presentation.edges:
    dependent_index = block_index_by_step_id[
      id(
        edge.parent_step
      )
    ]
    prerequisite_index = block_index_by_step_id[
      id(
        edge.premise_step
      )
    ]

    if dependent_index == prerequisite_index:
      continue

    if prerequisite_index in dependencies[
      dependent_index
    ]:
      continue

    dependencies[
      dependent_index
    ].append(
      prerequisite_index
    )

  return tuple(
    tuple(
      row
    )
    for row in dependencies
  )


def _closure_from_block(
  dependencies,
  start_index,
  boundary_indices,
  excluded_indices=(),
):
  visited = set()
  active = set()

  excluded_indices = frozenset(
    excluded_indices
  )

  def visit(
    block_index,
  ):
    if block_index in boundary_indices:
      return

    if block_index in excluded_indices:
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

  if (
    start_index not in boundary_indices
    and start_index not in excluded_indices
  ):
    visit(
      start_index
    )

  return frozenset(
    visited
  )


def _statement_types(
  block,
):
  return tuple(
    type(
      step.conclusion
    ).__name__
    for step in block.steps
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


def _argument_conclusion_indices(
  blocks,
  arguments,
):
  block_index_by_identity = {
    id(
      block
    ): index
    for index, block in enumerate(
      blocks
    )
  }

  return tuple(
    block_index_by_identity[
      id(
        argument.conclusion_block
      )
    ]
    for argument in arguments
  )


def _premise_union(
  premise_closures,
):
  result = set()
  for closure in premise_closures:
    result.update(
      closure
    )
  return frozenset(
    result
  )


def main():
  print(
    "Phase 144-6 R25-27 proof-edge ownership boundary audit"
  )
  print(
    "Production changes: none"
  )
  print()

  for n, k in TARGETS:
    (
      presentation,
      blocks,
      arguments,
    ) = _data(
      n,
      k,
    )
    dependencies = (
      _proof_dependencies(
        presentation,
        blocks,
      )
    )
    conclusion_indices = (
      _argument_conclusion_indices(
        blocks,
        arguments,
      )
    )

    argument_rows = []

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
      direct_premises = dependencies[
        conclusion_index
      ]
      premise_closures = tuple(
        _closure_from_block(
          dependencies,
          premise_index,
          boundary,
          excluded_indices=(
            conclusion_index,
          ),
        )
        for premise_index in direct_premises
      )
      union = _premise_union(
        premise_closures
      )

      argument_rows.append(
        (
          len(
            union
          ),
          argument_index,
          argument,
          conclusion_index,
          direct_premises,
          premise_closures,
          union,
          boundary,
        )
      )

    argument_rows.sort(
      reverse=True,
      key=lambda row: row[0],
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
      "arguments:",
      len(
        arguments
      ),
    )

    for (
      union_count,
      argument_index,
      argument,
      conclusion_index,
      direct_premises,
      premise_closures,
      union,
      boundary,
    ) in argument_rows[:8]:
      print()
      print(
        f"argument {argument_index:03d} "
        f"role={argument.role.value} "
        f"conclusion=B{conclusion_index}"
      )
      print(
        "  conclusion role:",
        blocks[
          conclusion_index
        ].role.value,
      )
      print(
        "  conclusion statement types:",
        _statement_types(
          blocks[
            conclusion_index
          ]
        ),
      )
      print(
        "  direct proof premises:",
        len(
          direct_premises
        ),
      )
      print(
        "  union closure:",
        union_count,
        "exactness=",
        _exactness_count(
          union,
          blocks,
        ),
      )

      premise_rows = []

      for premise_position, (
        premise_index,
        closure,
      ) in enumerate(
        zip(
          direct_premises,
          premise_closures,
        )
      ):
        unique_to_premise = (
          closure
          - _premise_union(
            tuple(
              other_closure
              for other_position, other_closure
              in enumerate(
                premise_closures
              )
              if other_position
              != premise_position
            )
          )
        )

        premise_rows.append(
          (
            len(
              closure
            ),
            premise_position,
            premise_index,
            closure,
            unique_to_premise,
          )
        )

      premise_rows.sort(
        reverse=True,
        key=lambda row: row[0],
      )

      for (
        closure_count,
        premise_position,
        premise_index,
        closure,
        unique_to_premise,
      ) in premise_rows:
        coverage = (
          0.0
          if not union
          else (
            100.0
            * len(
              closure
            )
            / len(
              union
            )
          )
        )
        print(
          f"  premise {premise_position}: "
          f"B{premise_index} "
          f"role={blocks[premise_index].role.value}"
        )
        print(
          "    statement types:",
          _statement_types(
            blocks[
              premise_index
            ]
          ),
        )
        print(
          "    closure:",
          closure_count,
          "coverage=",
          f"{coverage:.1f}%",
          "exactness=",
          _exactness_count(
            closure,
            blocks,
          ),
        )
        print(
          "    unique blocks:",
          len(
            unique_to_premise
          ),
          "unique exactness=",
          _exactness_count(
            unique_to_premise,
            blocks,
          ),
        )
        print(
          "    role counts:",
          _role_counts(
            closure,
            blocks,
          ),
        )
        print(
          "    direct child count:",
          len(
            dependencies[
              premise_index
            ]
          ),
        )
        print(
          "    hits argument boundary:",
          tuple(
            sorted(
              dependency_index
              for dependency_index in dependencies[
                premise_index
              ]
              if dependency_index in boundary
            )
          ),
        )

    print()


if __name__ == "__main__":
  main()
