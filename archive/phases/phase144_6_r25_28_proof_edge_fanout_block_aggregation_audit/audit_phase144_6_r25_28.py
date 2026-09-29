from collections import Counter, deque

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

TOP_ARGUMENTS = 6
TOP_PREMISES = 4
TOP_CHILDREN = 8


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


def _indices(
  presentation,
  blocks,
):
  step_index_by_id = {
    id(
      node.proof_step
    ): index
    for index, node in enumerate(
      presentation.nodes
    )
  }
  block_index_by_step_id = {
    id(
      step
    ): block_index
    for block_index, block in enumerate(
      blocks
    )
    for step in block.steps
  }
  block_index_by_identity = {
    id(
      block
    ): block_index
    for block_index, block in enumerate(
      blocks
    )
  }
  return (
    step_index_by_id,
    block_index_by_step_id,
    block_index_by_identity,
  )


def _step_dependencies(
  presentation,
  step_index_by_id,
):
  dependencies = [
    []
    for _ in presentation.nodes
  ]
  for edge in presentation.edges:
    parent_index = step_index_by_id[
      id(
        edge.parent_step
      )
    ]
    premise_index = step_index_by_id[
      id(
        edge.premise_step
      )
    ]
    if premise_index not in dependencies[
      parent_index
    ]:
      dependencies[
        parent_index
      ].append(
        premise_index
      )
  return tuple(
    tuple(
      row
    )
    for row in dependencies
  )


def _block_dependencies(
  presentation,
  blocks,
  block_index_by_step_id,
):
  dependencies = [
    []
    for _ in blocks
  ]
  for edge in presentation.edges:
    parent_index = block_index_by_step_id[
      id(
        edge.parent_step
      )
    ]
    premise_index = block_index_by_step_id[
      id(
        edge.premise_step
      )
    ]
    if parent_index == premise_index:
      continue
    if premise_index not in dependencies[
      parent_index
    ]:
      dependencies[
        parent_index
      ].append(
        premise_index
      )
  return tuple(
    tuple(
      row
    )
    for row in dependencies
  )


def _closure(
  dependencies,
  starts,
  excluded=(),
):
  excluded = frozenset(
    excluded
  )
  visited = set()
  active = set()

  def visit(
    index,
  ):
    if index in excluded:
      return
    if index in visited:
      return
    if index in active:
      return
    active.add(
      index
    )
    for dependency_index in dependencies[
      index
    ]:
      visit(
        dependency_index
      )
    active.remove(
      index
    )
    visited.add(
      index
    )

  for start in starts:
    visit(
      start
    )

  return frozenset(
    visited
  )


def _argument_conclusion_block_indices(
  blocks,
  arguments,
  block_index_by_identity,
):
  return tuple(
    block_index_by_identity[
      id(
        argument.conclusion_block
      )
    ]
    for argument in arguments
  )


def _step_indices_for_block(
  block,
  step_index_by_id,
):
  return tuple(
    step_index_by_id[
      id(
        step
      )
    ]
    for step in block.steps
  )


def _statement_types_for_block(
  block,
):
  return tuple(
    type(
      step.conclusion
    ).__name__
    for step in block.steps
  )


def _role_counts(
  block_indices,
  blocks,
):
  return dict(
    Counter(
      blocks[
        block_index
      ].role.value
      for block_index in block_indices
    )
  )


def _exactness_count(
  block_indices,
  blocks,
):
  return sum(
    blocks[
      block_index
    ].role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .EXACTNESS
    for block_index in block_indices
  )


def _project_steps_to_blocks(
  step_indices,
  presentation,
  block_index_by_step_id,
):
  return frozenset(
    block_index_by_step_id[
      id(
        presentation.nodes[
          step_index
        ].proof_step
      )
    ]
    for step_index in step_indices
  )


def _entry_steps_for_block_edge(
  presentation,
  parent_block_index,
  premise_block_index,
  block_index_by_step_id,
  step_index_by_id,
):
  return tuple(
    sorted(
      {
        step_index_by_id[
          id(
            edge.premise_step
          )
        ]
        for edge in presentation.edges
        if (
          block_index_by_step_id[
            id(
              edge.parent_step
            )
          ]
          == parent_block_index
          and block_index_by_step_id[
            id(
              edge.premise_step
            )
          ]
          == premise_block_index
        )
      }
    )
  )


def _shortest_block_path(
  dependencies,
  start,
  target,
  excluded=(),
):
  excluded = frozenset(
    excluded
  )
  if start in excluded:
    return ()
  queue = deque(
    (
      (
        start,
        (
          start,
        ),
      ),
    )
  )
  visited = {
    start,
  }
  while queue:
    current, path = queue.popleft()
    if current == target:
      return path
    for child in dependencies[
      current
    ]:
      if child in excluded:
        continue
      if child in visited:
        continue
      visited.add(
        child
      )
      queue.append(
        (
          child,
          path
          + (
            child,
          ),
        )
      )
  return ()


def main():
  print(
    "Phase 144-6 R25-28 proof-edge fan-out / block aggregation audit"
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
    (
      step_index_by_id,
      block_index_by_step_id,
      block_index_by_identity,
    ) = _indices(
      presentation,
      blocks,
    )
    step_dependencies = (
      _step_dependencies(
        presentation,
        step_index_by_id,
      )
    )
    block_dependencies = (
      _block_dependencies(
        presentation,
        blocks,
        block_index_by_step_id,
      )
    )
    conclusion_blocks = (
      _argument_conclusion_block_indices(
        blocks,
        arguments,
        block_index_by_identity,
      )
    )

    rows = []
    for argument_index, argument in enumerate(
      arguments
    ):
      conclusion_block = conclusion_blocks[
        argument_index
      ]
      boundary_blocks = set(
        conclusion_blocks
      )
      boundary_blocks.discard(
        conclusion_block
      )
      block_closure = _closure(
        block_dependencies,
        block_dependencies[
          conclusion_block
        ],
        excluded=boundary_blocks
        | {
          conclusion_block,
        },
      )
      rows.append(
        (
          len(
            block_closure
          ),
          argument_index,
          argument,
          conclusion_block,
          boundary_blocks,
          block_closure,
        )
      )

    rows.sort(
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
      "steps:",
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
      block_closure_count,
      argument_index,
      argument,
      conclusion_block,
      boundary_blocks,
      argument_block_closure,
    ) in rows[
      :TOP_ARGUMENTS
    ]:
      print()
      print(
        f"argument {argument_index:03d} "
        f"role={argument.role.value} "
        f"conclusion=B{conclusion_block}"
      )
      print(
        "  argument block closure:",
        block_closure_count,
        "exactness=",
        _exactness_count(
          argument_block_closure,
          blocks,
        ),
      )

      premise_rows = []
      for premise_block in block_dependencies[
        conclusion_block
      ]:
        premise_block_closure = _closure(
          block_dependencies,
          (
            premise_block,
          ),
          excluded=boundary_blocks
          | {
            conclusion_block,
          },
        )
        premise_rows.append(
          (
            len(
              premise_block_closure
            ),
            premise_block,
            premise_block_closure,
          )
        )

      premise_rows.sort(
        reverse=True,
        key=lambda row: row[0],
      )

      for (
        premise_block_count,
        premise_block,
        premise_block_closure,
      ) in premise_rows[
        :TOP_PREMISES
      ]:
        premise = blocks[
          premise_block
        ]
        premise_step_indices = (
          _step_indices_for_block(
            premise,
            step_index_by_id,
          )
        )
        entry_steps = (
          _entry_steps_for_block_edge(
            presentation,
            conclusion_block,
            premise_block,
            block_index_by_step_id,
            step_index_by_id,
          )
        )

        boundary_step_indices = {
          step_index
          for boundary_block in boundary_blocks
          for step_index in _step_indices_for_block(
            blocks[
              boundary_block
            ],
            step_index_by_id,
          )
        }
        current_conclusion_steps = set(
          _step_indices_for_block(
            blocks[
              conclusion_block
            ],
            step_index_by_id,
          )
        )
        excluded_steps = (
          boundary_step_indices
          | current_conclusion_steps
        )

        entry_step_closure = _closure(
          step_dependencies,
          entry_steps,
          excluded=excluded_steps,
        )
        all_block_step_closure = _closure(
          step_dependencies,
          premise_step_indices,
          excluded=excluded_steps,
        )
        entry_step_blocks = (
          _project_steps_to_blocks(
            entry_step_closure,
            presentation,
            block_index_by_step_id,
          )
        )
        all_block_step_blocks = (
          _project_steps_to_blocks(
            all_block_step_closure,
            presentation,
            block_index_by_step_id,
          )
        )
        aggregation_only_blocks = (
          premise_block_closure
          - entry_step_blocks
        )

        print(
          f"  premise B{premise_block} "
          f"role={premise.role.value}"
        )
        print(
          "    block steps:",
          len(
            premise.steps
          ),
          "entry steps:",
          len(
            entry_steps
          ),
        )
        print(
          "    statement types:",
          _statement_types_for_block(
            premise
          ),
        )
        print(
          "    block closure:",
          premise_block_count,
          "exactness=",
          _exactness_count(
            premise_block_closure,
            blocks,
          ),
        )
        print(
          "    entry-step closure:",
          len(
            entry_step_closure
          ),
          "projected blocks=",
          len(
            entry_step_blocks
          ),
          "exactness=",
          _exactness_count(
            entry_step_blocks,
            blocks,
          ),
        )
        print(
          "    all-block-steps closure:",
          len(
            all_block_step_closure
          ),
          "projected blocks=",
          len(
            all_block_step_blocks
          ),
          "exactness=",
          _exactness_count(
            all_block_step_blocks,
            blocks,
          ),
        )
        print(
          "    aggregation-only blocks:",
          len(
            aggregation_only_blocks
          ),
          "exactness=",
          _exactness_count(
            aggregation_only_blocks,
            blocks,
          ),
        )
        print(
          "    aggregation-only role counts:",
          _role_counts(
            aggregation_only_blocks,
            blocks,
          ),
        )

        child_rows = []
        for child_block in block_dependencies[
          premise_block
        ]:
          child_closure = _closure(
            block_dependencies,
            (
              child_block,
            ),
            excluded=boundary_blocks
            | {
              conclusion_block,
              premise_block,
            },
          )
          child_rows.append(
            (
              len(
                child_closure
              ),
              child_block,
              child_closure,
            )
          )
        child_rows.sort(
          reverse=True,
          key=lambda row: row[0],
        )

        print(
          "    direct child blocks:",
          len(
            child_rows
          ),
        )
        for (
          child_count,
          child_block,
          child_closure,
        ) in child_rows[
          :TOP_CHILDREN
        ]:
          print(
            f"      B{child_block} "
            f"role={blocks[child_block].role.value} "
            f"steps={len(blocks[child_block].steps)} "
            f"closure={child_count} "
            f"exactness={_exactness_count(child_closure, blocks)} "
            f"types={_statement_types_for_block(blocks[child_block])}"
          )

        if aggregation_only_blocks:
          largest_aggregation_block = max(
            aggregation_only_blocks,
            key=lambda block_index: len(
              _closure(
                block_dependencies,
                (
                  block_index,
                ),
                excluded=boundary_blocks
                | {
                  conclusion_block,
                  premise_block,
                },
              )
            ),
          )
          path = _shortest_block_path(
            block_dependencies,
            premise_block,
            largest_aggregation_block,
            excluded=boundary_blocks
            | {
              conclusion_block,
            },
          )
          print(
            "    sample aggregation-only path:",
            " -> ".join(
              f"B{block_index}"
              for block_index in path
            ),
          )

    print()


if __name__ == "__main__":
  main()
