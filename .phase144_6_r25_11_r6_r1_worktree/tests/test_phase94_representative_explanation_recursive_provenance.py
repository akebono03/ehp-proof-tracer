from functools import lru_cache

import pytest

from proof import ProofRule, ProofStep
from test_phase92_actual_ehp_extraction import (
  build_phase92_3_data,
)
from toda_explanation import (
  TodaRepresentativeExplanationResult,
  build_toda_representative_explanation,
)
from toda_proof_dependency import (
  TodaProofDependencyResult,
  TodaRecursiveProofProvenanceResult,
)


@lru_cache(maxsize=1)
def build_phase94_5_data():
  phase92_3 = (
    build_phase92_3_data()
  )

  explanation = (
    build_toda_representative_explanation(
      phase92_3[
        "group_result"
      ]
    )
  )

  return {
    "phase92_3": phase92_3,
    "phase68": phase92_3[
      "phase68"
    ],
    "group_result": phase92_3[
      "group_result"
    ],
    "explanation": explanation,
  }


def test_phase94_5_returns_representative_explanation_result():
  data = build_phase94_5_data()

  assert isinstance(
    data[
      "explanation"
    ],
    TodaRepresentativeExplanationResult,
  )


def test_phase94_5_integrates_recursive_provenance():
  data = build_phase94_5_data()

  assert isinstance(
    data[
      "explanation"
    ].recursive_provenance,
    TodaRecursiveProofProvenanceResult,
  )


def test_phase94_5_recursive_root_is_actual_group_proof_step():
  data = build_phase94_5_data()

  explanation = data[
    "explanation"
  ]

  assert (
    explanation
    .recursive_provenance
    .root_step
    is explanation
    .group_result
    .proof_step
  )

  assert (
    explanation
    .recursive_provenance
    .root_step
    is data[
      "phase68"
    ][
      "final_step"
    ]
  )


def test_phase94_5_flat_and_recursive_views_share_same_root():
  data = build_phase94_5_data()

  explanation = data[
    "explanation"
  ]

  assert isinstance(
    explanation.dependency_result,
    TodaProofDependencyResult,
  )

  assert (
    explanation
    .dependency_result
    .root_step
    is explanation
    .recursive_provenance
    .root_step
  )


def test_phase94_5_recursive_nodes_match_flat_dependencies_plus_root():
  data = build_phase94_5_data()

  explanation = data[
    "explanation"
  ]

  expected_ids = {
    id(
      explanation
      .group_result
      .proof_step
    ),
    *(
      id(
        dependency.proof_step
      )
      for dependency in (
        explanation
        .dependency_result
        .dependencies
      )
    ),
  }

  actual_ids = {
    id(
      node.proof_step
    )
    for node in (
      explanation
      .recursive_provenance
      .nodes
    )
  }

  assert actual_ids == expected_ids


def test_phase94_5_recursive_depth_matches_flat_dependency_depth():
  data = build_phase94_5_data()

  explanation = data[
    "explanation"
  ]

  node_by_step_id = {
    id(node.proof_step): node
    for node in (
      explanation
      .recursive_provenance
      .nodes
    )
  }

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
      explanation
      .dependency_result
      .dependencies
    )
  )


def test_phase94_5_recursive_edges_include_actual_hopf_zero_premises():
  data = build_phase94_5_data()

  explanation = data[
    "explanation"
  ]

  phase68 = data[
    "phase68"
  ]

  hopf_zero_edges = tuple(
    edge
    for edge in (
      explanation
      .recursive_provenance
      .edges
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


def test_phase94_5_preserves_phase93_role_filter_api():
  data = build_phase94_5_data()

  explanation = data[
    "explanation"
  ]

  assert (
    explanation.dependencies_for_role
    is not None
  )


def test_phase94_5_result_rejects_wrong_recursive_provenance_type():
  data = build_phase94_5_data()

  explanation = data[
    "explanation"
  ]

  with pytest.raises(
    TypeError,
    match=(
      "recursive_provenance must be "
      "a TodaRecursiveProofProvenanceResult"
    ),
  ):
    TodaRepresentativeExplanationResult(
      group_result=(
        explanation.group_result
      ),
      ehp_result=(
        explanation.ehp_result
      ),
      exactness_provenance=(
        explanation
        .exactness_provenance
      ),
      dependency_result=(
        explanation
        .dependency_result
      ),
      recursive_provenance=(
        "not recursive provenance"
      ),
    )


def test_phase94_5_result_rejects_recursive_root_identity_mismatch():
  data = build_phase94_5_data()

  explanation = data[
    "explanation"
  ]

  wrong_root = ProofStep(
    conclusion="wrong root",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  wrong_recursive = (
    TodaRecursiveProofProvenanceResult(
      root_step=wrong_root,
      nodes=(
        explanation
        .recursive_provenance
        .nodes[
          0
        ].__class__(
          proof_step=wrong_root,
          shortest_depth=0,
        ),
      ),
      edges=(),
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "recursive_provenance.root_step "
      "must be group_result.proof_step"
    ),
  ):
    TodaRepresentativeExplanationResult(
      group_result=(
        explanation.group_result
      ),
      ehp_result=(
        explanation.ehp_result
      ),
      exactness_provenance=(
        explanation
        .exactness_provenance
      ),
      dependency_result=(
        explanation
        .dependency_result
      ),
      recursive_provenance=(
        wrong_recursive
      ),
    )
