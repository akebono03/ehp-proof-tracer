from functools import lru_cache

import pytest

from proof import ProofStep
from test_phase92_actual_ehp_extraction import (
  build_phase92_3_data,
)
from toda_proof_dependency import (
  TodaRecursiveProofProvenanceResult,
  classify_toda_proof_step_role,
  extract_toda_proof_dependencies,
  extract_toda_recursive_proof_provenance,
)


@lru_cache(maxsize=1)
def build_phase94_3_data():
  phase92_3 = (
    build_phase92_3_data()
  )

  group_result = (
    phase92_3[
      "group_result"
    ]
  )

  recursive_result = (
    extract_toda_recursive_proof_provenance(
      group_result
    )
  )

  dependency_result = (
    extract_toda_proof_dependencies(
      group_result
    )
  )

  return {
    "phase92_3": phase92_3,
    "phase68": phase92_3[
      "phase68"
    ],
    "group_result": group_result,
    "recursive_result": (
      recursive_result
    ),
    "dependency_result": (
      dependency_result
    ),
  }


def test_phase94_3_returns_recursive_provenance_result():
  data = build_phase94_3_data()

  assert isinstance(
    data[
      "recursive_result"
    ],
    TodaRecursiveProofProvenanceResult,
  )


def test_phase94_3_preserves_actual_root_identity():
  data = build_phase94_3_data()

  assert (
    data[
      "recursive_result"
    ].root_step
    is data[
      "group_result"
    ].proof_step
  )

  assert (
    data[
      "recursive_result"
    ].root_step
    is data[
      "phase68"
    ][
      "final_step"
    ]
  )


def test_phase94_3_root_is_first_node_at_depth_zero():
  data = build_phase94_3_data()

  root_node = (
    data[
      "recursive_result"
    ].nodes[
      0
    ]
  )

  assert (
    root_node.proof_step
    is data[
      "phase68"
    ][
      "final_step"
    ]
  )

  assert (
    root_node.shortest_depth
    == 0
  )


def test_phase94_3_node_identities_are_unique():
  data = build_phase94_3_data()

  node_ids = tuple(
    id(
      node.proof_step
    )
    for node in (
      data[
        "recursive_result"
      ].nodes
    )
  )

  assert len(
    node_ids
  ) == len(
    set(
      node_ids
    )
  )


def test_phase94_3_node_set_matches_phase93_dependencies_plus_root():
  data = build_phase94_3_data()

  recursive_result = (
    data[
      "recursive_result"
    ]
  )

  dependency_result = (
    data[
      "dependency_result"
    ]
  )

  expected_step_ids = {
    id(
      dependency_result.root_step
    ),
    *(
      id(
        dependency.proof_step
      )
      for dependency in (
        dependency_result
        .dependencies
      )
    ),
  }

  actual_step_ids = {
    id(
      node.proof_step
    )
    for node in (
      recursive_result.nodes
    )
  }

  assert (
    actual_step_ids
    == expected_step_ids
  )


def test_phase94_3_shortest_depth_matches_phase93_flat_view():
  data = build_phase94_3_data()

  recursive_result = (
    data[
      "recursive_result"
    ]
  )

  dependency_result = (
    data[
      "dependency_result"
    ]
  )

  node_by_step_id = {
    id(node.proof_step): node
    for node in (
      recursive_result.nodes
    )
  }

  assert (
    node_by_step_id[
      id(
        dependency_result.root_step
      )
    ].shortest_depth
    == 0
  )

  assert all(
    (
      node_by_step_id[
        id(
          dependency.proof_step
        )
      ].shortest_depth
      == dependency.depth
    )
    for dependency in (
      dependency_result
      .dependencies
    )
  )


def test_phase94_3_each_proof_step_premise_has_exactly_one_edge():
  data = build_phase94_3_data()

  recursive_result = (
    data[
      "recursive_result"
    ]
  )

  expected_edges = tuple(
    (
      node.proof_step,
      premise,
      premise_index,
    )
    for node in (
      recursive_result.nodes
    )
    for (
      premise_index,
      premise,
    ) in enumerate(
      node.proof_step.premises
    )
    if isinstance(
      premise,
      ProofStep,
    )
  )

  actual_edges = tuple(
    (
      edge.parent_step,
      edge.premise_step,
      edge.premise_index,
    )
    for edge in (
      recursive_result.edges
    )
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


def test_phase94_3_root_edges_preserve_actual_final_premise_order():
  data = build_phase94_3_data()

  final_step = (
    data[
      "phase68"
    ][
      "final_step"
    ]
  )

  root_edges = tuple(
    edge
    for edge in (
      data[
        "recursive_result"
      ].edges
    )
    if (
      edge.parent_step
      is final_step
    )
  )

  expected_premises = tuple(
    (
      premise_index,
      premise,
    )
    for (
      premise_index,
      premise,
    ) in enumerate(
      final_step.premises
    )
    if isinstance(
      premise,
      ProofStep,
    )
  )

  assert len(
    root_edges
  ) == len(
    expected_premises
  )

  assert all(
    (
      edge.premise_step
      is premise
      and edge.premise_index
      == premise_index
    )
    for (
      edge,
      (
        premise_index,
        premise,
      ),
    ) in zip(
      root_edges,
      expected_premises,
    )
  )


def test_phase94_3_contains_actual_hopf_zero_dependency_edges():
  data = build_phase94_3_data()

  phase68 = data[
    "phase68"
  ]

  hopf_zero_edges = tuple(
    edge
    for edge in (
      data[
        "recursive_result"
      ].edges
    )
    if (
      edge.parent_step
      is phase68[
        "hopf_zero_step"
      ]
    )
  )

  assert len(
    hopf_zero_edges
  ) == 2

  assert (
    hopf_zero_edges[
      0
    ].premise_step
    is phase68[
      "delta_injective_step"
    ]
  )

  assert (
    hopf_zero_edges[
      1
    ].premise_step
    is phase68[
      "h_delta_exactness_step"
    ]
  )

  assert tuple(
    edge.premise_index
    for edge in (
      hopf_zero_edges
    )
  ) == (
    0,
    1,
  )


def test_phase94_3_contains_exactness_to_window_edge():
  data = build_phase94_3_data()

  phase68 = data[
    "phase68"
  ]

  exactness_step = (
    phase68[
      "delta_e_exactness_step"
    ]
  )

  window_step = (
    phase68[
      "delta_e_window_step"
    ]
  )

  assert any(
    (
      edge.parent_step
      is exactness_step
      and edge.premise_step
      is window_step
      and edge.premise_index
      == 0
    )
    for edge in (
      data[
        "recursive_result"
      ].edges
    )
  )


def test_phase94_3_node_roles_match_existing_classifier():
  data = build_phase94_3_data()

  assert all(
    (
      node.role
      == classify_toda_proof_step_role(
        node.proof_step
      )
    )
    for node in (
      data[
        "recursive_result"
      ].nodes
    )
  )


def test_phase94_3_non_proof_premises_do_not_become_edges():
  data = build_phase94_3_data()

  assert all(
    isinstance(
      edge.premise_step,
      ProofStep,
    )
    for edge in (
      data[
        "recursive_result"
      ].edges
    )
  )


def test_phase94_3_rejects_non_group_result():
  with pytest.raises(
    TypeError,
    match=(
      "group_result must be "
      "a TodaGroupResult"
    ),
  ):
    extract_toda_recursive_proof_provenance(
      "not a group result"
    )
