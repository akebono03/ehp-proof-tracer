import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from toda_proof_dependency import (
  TodaProofDependencyRole,
  TodaProofEdge,
  TodaProofNode,
  TodaRecursiveProofProvenanceResult,
)


def build_test_step(
  conclusion,
  premises=(),
):
  return ProofStep(
    conclusion=conclusion,
    premises=premises,
    rule=ProofRule.GIVEN,
  )


def test_phase94_2_node_preserves_proof_step_identity():
  step = build_test_step(
    "node",
  )

  node = TodaProofNode(
    proof_step=step,
    shortest_depth=0,
  )

  assert node.proof_step is step


def test_phase94_2_node_preserves_shortest_depth_and_role():
  step = build_test_step(
    "node",
  )

  node = TodaProofNode(
    proof_step=step,
    shortest_depth=2,
    role=(
      TodaProofDependencyRole
      .MAP_PROPERTY
    ),
  )

  assert node.shortest_depth == 2
  assert (
    node.role
    == TodaProofDependencyRole.MAP_PROPERTY
  )


def test_phase94_2_node_allows_root_depth_zero():
  node = TodaProofNode(
    proof_step=build_test_step(
      "root",
    ),
    shortest_depth=0,
  )

  assert node.shortest_depth == 0


def test_phase94_2_node_rejects_negative_shortest_depth():
  with pytest.raises(
    ValueError,
    match=(
      "shortest_depth must be "
      "non-negative"
    ),
  ):
    TodaProofNode(
      proof_step=build_test_step(
        "node",
      ),
      shortest_depth=-1,
    )


def test_phase94_2_node_rejects_bool_shortest_depth():
  with pytest.raises(
    TypeError,
    match=(
      "shortest_depth must be an int"
    ),
  ):
    TodaProofNode(
      proof_step=build_test_step(
        "node",
      ),
      shortest_depth=True,
    )


def test_phase94_2_edge_preserves_identity_and_original_premise_index():
  premise_step = build_test_step(
    "premise",
  )

  parent_step = build_test_step(
    "parent",
    premises=(
      "non proof premise",
      premise_step,
    ),
  )

  edge = TodaProofEdge(
    parent_step=parent_step,
    premise_step=premise_step,
    premise_index=1,
  )

  assert edge.parent_step is parent_step
  assert edge.premise_step is premise_step
  assert edge.premise_index == 1


def test_phase94_2_edge_rejects_wrong_premise_index():
  first_step = build_test_step(
    "first",
  )

  second_step = build_test_step(
    "second",
  )

  parent_step = build_test_step(
    "parent",
    premises=(
      first_step,
      second_step,
    ),
  )

  with pytest.raises(
    ValueError,
    match=(
      "premise_step must be the "
      "ProofStep at premise_index"
    ),
  ):
    TodaProofEdge(
      parent_step=parent_step,
      premise_step=second_step,
      premise_index=0,
    )


def test_phase94_2_result_represents_shared_dependency_once():
  shared_step = build_test_step(
    "shared",
  )

  first_step = build_test_step(
    "first",
    premises=(
      shared_step,
    ),
  )

  second_step = build_test_step(
    "second",
    premises=(
      shared_step,
    ),
  )

  root_step = build_test_step(
    "root",
    premises=(
      first_step,
      second_step,
    ),
  )

  root_node = TodaProofNode(
    proof_step=root_step,
    shortest_depth=0,
  )

  first_node = TodaProofNode(
    proof_step=first_step,
    shortest_depth=1,
  )

  second_node = TodaProofNode(
    proof_step=second_step,
    shortest_depth=1,
  )

  shared_node = TodaProofNode(
    proof_step=shared_step,
    shortest_depth=2,
  )

  result = (
    TodaRecursiveProofProvenanceResult(
      root_step=root_step,
      nodes=(
        root_node,
        first_node,
        second_node,
        shared_node,
      ),
      edges=(
        TodaProofEdge(
          parent_step=root_step,
          premise_step=first_step,
          premise_index=0,
        ),
        TodaProofEdge(
          parent_step=root_step,
          premise_step=second_step,
          premise_index=1,
        ),
        TodaProofEdge(
          parent_step=first_step,
          premise_step=shared_step,
          premise_index=0,
        ),
        TodaProofEdge(
          parent_step=second_step,
          premise_step=shared_step,
          premise_index=0,
        ),
      ),
    )
  )

  shared_nodes = tuple(
    node
    for node in result.nodes
    if node.proof_step is shared_step
  )

  assert len(
    shared_nodes
  ) == 1

  shared_edges = tuple(
    edge
    for edge in result.edges
    if edge.premise_step is shared_step
  )

  assert len(
    shared_edges
  ) == 2


def test_phase94_2_result_preserves_edge_order():
  first_step = build_test_step(
    "first",
  )

  second_step = build_test_step(
    "second",
  )

  root_step = build_test_step(
    "root",
    premises=(
      first_step,
      second_step,
    ),
  )

  first_edge = TodaProofEdge(
    parent_step=root_step,
    premise_step=first_step,
    premise_index=0,
  )

  second_edge = TodaProofEdge(
    parent_step=root_step,
    premise_step=second_step,
    premise_index=1,
  )

  result = (
    TodaRecursiveProofProvenanceResult(
      root_step=root_step,
      nodes=(
        TodaProofNode(
          proof_step=root_step,
          shortest_depth=0,
        ),
        TodaProofNode(
          proof_step=first_step,
          shortest_depth=1,
        ),
        TodaProofNode(
          proof_step=second_step,
          shortest_depth=1,
        ),
      ),
      edges=(
        first_edge,
        second_edge,
      ),
    )
  )

  assert result.edges == (
    first_edge,
    second_edge,
  )


def test_phase94_2_result_rejects_duplicate_node_identity():
  root_step = build_test_step(
    "root",
  )

  with pytest.raises(
    ValueError,
    match=(
      "nodes must not contain "
      "the same ProofStep more than once"
    ),
  ):
    TodaRecursiveProofProvenanceResult(
      root_step=root_step,
      nodes=(
        TodaProofNode(
          proof_step=root_step,
          shortest_depth=0,
        ),
        TodaProofNode(
          proof_step=root_step,
          shortest_depth=0,
        ),
      ),
      edges=(),
    )


def test_phase94_2_result_rejects_missing_root_node():
  root_step = build_test_step(
    "root",
  )

  other_step = build_test_step(
    "other",
  )

  with pytest.raises(
    ValueError,
    match=(
      "nodes must contain root_step "
      "exactly once"
    ),
  ):
    TodaRecursiveProofProvenanceResult(
      root_step=root_step,
      nodes=(
        TodaProofNode(
          proof_step=other_step,
          shortest_depth=1,
        ),
      ),
      edges=(),
    )


def test_phase94_2_result_rejects_edge_endpoint_missing_from_nodes():
  child_step = build_test_step(
    "child",
  )

  root_step = build_test_step(
    "root",
    premises=(
      child_step,
    ),
  )

  edge = TodaProofEdge(
    parent_step=root_step,
    premise_step=child_step,
    premise_index=0,
  )

  with pytest.raises(
    ValueError,
    match=(
      "edge premise_step must appear "
      "in nodes"
    ),
  ):
    TodaRecursiveProofProvenanceResult(
      root_step=root_step,
      nodes=(
        TodaProofNode(
          proof_step=root_step,
          shortest_depth=0,
        ),
      ),
      edges=(
        edge,
      ),
    )


def test_phase94_2_equal_but_distinct_steps_remain_distinct_nodes():
  root_step = build_test_step(
    "root",
  )

  first_step = build_test_step(
    "same",
  )

  second_step = build_test_step(
    "same",
  )

  assert first_step == second_step
  assert first_step is not second_step

  result = (
    TodaRecursiveProofProvenanceResult(
      root_step=root_step,
      nodes=(
        TodaProofNode(
          proof_step=root_step,
          shortest_depth=0,
        ),
        TodaProofNode(
          proof_step=first_step,
          shortest_depth=1,
        ),
        TodaProofNode(
          proof_step=second_step,
          shortest_depth=1,
        ),
      ),
      edges=(),
    )
  )

  assert len(
    result.nodes
  ) == 3
