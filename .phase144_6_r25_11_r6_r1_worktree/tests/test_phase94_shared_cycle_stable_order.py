from proof import (
  ProofRule,
  ProofStep,
)
from test_phase93_actual_dependency_extraction import (
  build_synthetic_group_result,
)
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)


def build_test_step(
  conclusion,
  premises=(),
):
  return ProofStep(
    conclusion=conclusion,
    premises=premises,
    rule=ProofRule.INFERENCE,
  )


def test_phase94_4_shared_node_is_returned_once_with_multiple_incoming_edges():
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

  result = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase94.shared-node",
      )
    )
  )

  shared_nodes = tuple(
    node
    for node in result.nodes
    if (
      node.proof_step
      is shared_step
    )
  )

  assert len(
    shared_nodes
  ) == 1

  incoming_edges = tuple(
    edge
    for edge in result.edges
    if (
      edge.premise_step
      is shared_step
    )
  )

  assert len(
    incoming_edges
  ) == 2

  assert (
    incoming_edges[
      0
    ].parent_step
    is first_step
  )

  assert (
    incoming_edges[
      1
    ].parent_step
    is second_step
  )


def test_phase94_4_shared_node_keeps_shortest_depth():
  shared_step = build_test_step(
    "shared",
  )

  deep_step = build_test_step(
    "deep",
    premises=(
      shared_step,
    ),
  )

  direct_step = build_test_step(
    "direct",
    premises=(
      shared_step,
    ),
  )

  other_step = build_test_step(
    "other",
    premises=(
      deep_step,
    ),
  )

  root_step = build_test_step(
    "root",
    premises=(
      direct_step,
      other_step,
    ),
  )

  result = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase94.shortest-depth",
      )
    )
  )

  shared_node = next(
    node
    for node in result.nodes
    if (
      node.proof_step
      is shared_step
    )
  )

  assert (
    shared_node.shortest_depth
    == 2
  )


def test_phase94_4_node_order_is_stable_breadth_first():
  first_child = build_test_step(
    "first child",
  )

  second_child = build_test_step(
    "second child",
  )

  first_direct = build_test_step(
    "first direct",
    premises=(
      first_child,
    ),
  )

  second_direct = build_test_step(
    "second direct",
    premises=(
      second_child,
    ),
  )

  root_step = build_test_step(
    "root",
    premises=(
      first_direct,
      second_direct,
    ),
  )

  result = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase94.node-order",
      )
    )
  )

  assert tuple(
    node.proof_step
    for node in result.nodes
  ) == (
    root_step,
    first_direct,
    second_direct,
    first_child,
    second_child,
  )

  assert tuple(
    node.shortest_depth
    for node in result.nodes
  ) == (
    0,
    1,
    1,
    2,
    2,
  )


def test_phase94_4_edge_order_is_stable_by_parent_and_premise_index():
  first_leaf = build_test_step(
    "first leaf",
  )

  second_leaf = build_test_step(
    "second leaf",
  )

  third_leaf = build_test_step(
    "third leaf",
  )

  first_direct = build_test_step(
    "first direct",
    premises=(
      first_leaf,
      second_leaf,
    ),
  )

  second_direct = build_test_step(
    "second direct",
    premises=(
      third_leaf,
    ),
  )

  root_step = build_test_step(
    "root",
    premises=(
      first_direct,
      second_direct,
    ),
  )

  result = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase94.edge-order",
      )
    )
  )

  actual_edges = tuple(
    (
      edge.parent_step,
      edge.premise_step,
      edge.premise_index,
    )
    for edge in result.edges
  )

  expected_edges = (
    (
      root_step,
      first_direct,
      0,
    ),
    (
      root_step,
      second_direct,
      1,
    ),
    (
      first_direct,
      first_leaf,
      0,
    ),
    (
      first_direct,
      second_leaf,
      1,
    ),
    (
      second_direct,
      third_leaf,
      0,
    ),
  )

  assert len(
    actual_edges
  ) == len(
    expected_edges
  )

  assert all(
    (
      actual_parent
      is expected_parent
      and actual_premise
      is expected_premise
      and actual_index
      == expected_index
    )
    for (
      (
        actual_parent,
        actual_premise,
        actual_index,
      ),
      (
        expected_parent,
        expected_premise,
        expected_index,
      ),
    ) in zip(
      actual_edges,
      expected_edges,
    )
  )


def test_phase94_4_original_premise_index_is_preserved_with_non_proof_premise():
  child_step = build_test_step(
    "child",
  )

  root_step = build_test_step(
    "root",
    premises=(
      "non proof premise",
      child_step,
    ),
  )

  result = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase94.original-index",
      )
    )
  )

  assert len(
    result.edges
  ) == 1

  assert (
    result.edges[
      0
    ].parent_step
    is root_step
  )

  assert (
    result.edges[
      0
    ].premise_step
    is child_step
  )

  assert (
    result.edges[
      0
    ].premise_index
    == 1
  )


def test_phase94_4_cycle_is_safe_and_preserves_back_edge():
  root_step = build_test_step(
    "root",
  )

  child_step = build_test_step(
    "child",
    premises=(
      root_step,
    ),
  )

  object.__setattr__(
    root_step,
    "premises",
    (
      child_step,
    ),
  )

  result = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase94.cycle",
      )
    )
  )

  assert len(
    result.nodes
  ) == 2

  assert (
    result.nodes[
      0
    ].proof_step
    is root_step
  )

  assert (
    result.nodes[
      0
    ].shortest_depth
    == 0
  )

  assert (
    result.nodes[
      1
    ].proof_step
    is child_step
  )

  assert (
    result.nodes[
      1
    ].shortest_depth
    == 1
  )

  assert len(
    result.edges
  ) == 2

  assert (
    result.edges[
      0
    ].parent_step
    is root_step
  )

  assert (
    result.edges[
      0
    ].premise_step
    is child_step
  )

  assert (
    result.edges[
      1
    ].parent_step
    is child_step
  )

  assert (
    result.edges[
      1
    ].premise_step
    is root_step
  )


def test_phase94_4_self_cycle_is_safe_and_preserves_self_edge():
  root_step = build_test_step(
    "root",
  )

  object.__setattr__(
    root_step,
    "premises",
    (
      root_step,
    ),
  )

  result = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase94.self-cycle",
      )
    )
  )

  assert len(
    result.nodes
  ) == 1

  assert (
    result.nodes[
      0
    ].proof_step
    is root_step
  )

  assert (
    result.nodes[
      0
    ].shortest_depth
    == 0
  )

  assert len(
    result.edges
  ) == 1

  assert (
    result.edges[
      0
    ].parent_step
    is root_step
  )

  assert (
    result.edges[
      0
    ].premise_step
    is root_step
  )

  assert (
    result.edges[
      0
    ].premise_index
    == 0
  )


def test_phase94_4_shared_revisit_and_cycle_revisit_are_structurally_distinct():
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

  shared_root = build_test_step(
    "shared root",
    premises=(
      first_step,
      second_step,
    ),
  )

  shared_result = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        shared_root,
        "phase94.shared-revisit",
      )
    )
  )

  cycle_root = build_test_step(
    "cycle root",
  )

  cycle_child = build_test_step(
    "cycle child",
    premises=(
      cycle_root,
    ),
  )

  object.__setattr__(
    cycle_root,
    "premises",
    (
      cycle_child,
    ),
  )

  cycle_result = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        cycle_root,
        "phase94.cycle-revisit",
      )
    )
  )

  assert sum(
    1
    for edge in shared_result.edges
    if (
      edge.premise_step
      is shared_step
    )
  ) == 2

  assert not any(
    (
      edge.premise_step
      is shared_root
    )
    for edge in shared_result.edges
  )

  assert any(
    (
      edge.parent_step
      is cycle_child
      and edge.premise_step
      is cycle_root
    )
    for edge in cycle_result.edges
  )
