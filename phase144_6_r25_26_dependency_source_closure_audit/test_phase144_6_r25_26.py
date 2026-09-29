from phase144_6_r25_26_dependency_source_closure_audit.audit_phase144_6_r25_26 import (
  TARGETS,
  _closure,
  _data,
  _dependency_sources,
)


def test_phase144_6_r25_26_dependency_sources_recombine_to_production_shape():
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

    assert len(
      proof_dependencies
    ) == len(
      blocks
    )
    assert len(
      semantic_dependencies
    ) == len(
      blocks
    )
    assert len(
      combined_dependencies
    ) == len(
      blocks
    )

    for index in range(
      len(
        blocks
      )
    ):
      expected = []
      for dependency_index in (
        proof_dependencies[index]
        + semantic_dependencies[index]
      ):
        if (
          dependency_index != index
          and dependency_index not in expected
        ):
          expected.append(
            dependency_index
          )

      assert combined_dependencies[
        index
      ] == tuple(
        expected
      )


def test_phase144_6_r25_26_six_groups_have_argument_closures():
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
      _,
      _,
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

    closures = []
    for argument_index, conclusion_index in enumerate(
      conclusion_indices
    ):
      boundary = set(
        conclusion_indices
      )
      boundary.discard(
        conclusion_index
      )
      closures.append(
        _closure(
          combined_dependencies,
          conclusion_index,
          boundary,
        )
      )

    assert any(
      closures
    )
