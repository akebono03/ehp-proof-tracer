from phase144_6_r25_27_proof_edge_ownership_boundary_audit.audit_phase144_6_r25_27 import (
  TARGETS,
  _argument_conclusion_indices,
  _closure_from_block,
  _data,
  _premise_union,
  _proof_dependencies,
)


def test_phase144_6_r25_27_proof_dependency_rows_match_block_count():
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

    assert len(
      dependencies
    ) == len(
      blocks
    )

    assert all(
      dependency_index != block_index
      for block_index, row in enumerate(
        dependencies
      )
      for dependency_index in row
    )


def test_phase144_6_r25_27_direct_premise_union_matches_argument_proof_closure():
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

    for argument_index, conclusion_index in enumerate(
      conclusion_indices
    ):
      boundary = set(
        conclusion_indices
      )
      boundary.discard(
        conclusion_index
      )
      premise_closures = tuple(
        _closure_from_block(
          dependencies,
          premise_index,
          boundary,
          excluded_indices=(
            conclusion_index,
          ),
        )
        for premise_index in dependencies[
          conclusion_index
        ]
      )
      union = _premise_union(
        premise_closures
      )

      expected = set()

      def visit(
        block_index,
      ):
        if block_index in boundary:
          return
        if block_index in expected:
          return

        expected.add(
          block_index
        )

        for dependency_index in dependencies[
          block_index
        ]:
          visit(
            dependency_index
          )

      for premise_index in dependencies[
        conclusion_index
      ]:
        visit(
          premise_index
        )

      expected.discard(
        conclusion_index
      )

      assert union == frozenset(
        expected
      )
