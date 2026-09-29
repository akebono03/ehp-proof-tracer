from phase144_6_r25_28_proof_edge_fanout_block_aggregation_audit.audit_phase144_6_r25_28 import (
  TARGETS,
  _block_dependencies,
  _closure,
  _data,
  _indices,
  _project_steps_to_blocks,
  _step_dependencies,
)


def test_phase144_6_r25_28_every_step_belongs_to_exactly_one_block():
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

    assert len(
      block_index_by_step_id
    ) == len(
      presentation.nodes
    )

    assert set(
      block_index_by_step_id
    ) == {
      id(
        node.proof_step
      )
      for node in presentation.nodes
    }


def test_phase144_6_r25_28_step_projection_is_subset_of_block_closure():
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

    for block_index, block in enumerate(
      blocks
    ):
      step_indices = tuple(
        step_index_by_id[
          id(
            step
          )
        ]
        for step in block.steps
      )
      step_closure = _closure(
        step_dependencies,
        step_indices,
      )
      projected_blocks = (
        _project_steps_to_blocks(
          step_closure,
          presentation,
          block_index_by_step_id,
        )
      )
      block_closure = _closure(
        block_dependencies,
        (
          block_index,
        ),
      )

      assert projected_blocks <= block_closure
