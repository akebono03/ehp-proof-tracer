import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from test_phase93_actual_dependency_extraction import (
  build_synthetic_group_result,
)
from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
  get_single_candidate,
)
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)
from toda_proof_flow_presentation import (
  TodaProofFlowEdgePresentation,
  TodaProofFlowNodePresentation,
  TodaReadableProofFlowPresentation,
  build_toda_readable_proof_flow_presentation,
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


def test_phase96_6_actual_pi9_5_builds_readable_flow():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  provenance = (
    candidate
    .explanation
    .recursive_provenance
  )

  presentation = (
    build_toda_readable_proof_flow_presentation(
      provenance
    )
  )

  assert isinstance(
    presentation,
    TodaReadableProofFlowPresentation,
  )
  assert (
    presentation.source_provenance
    is provenance
  )
  assert (
    presentation.root.step.source_step
    is provenance.root_step
  )


def test_phase96_6_actual_pi9_5_dependency_first_order_places_each_premise_before_parent():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  presentation = (
    build_toda_readable_proof_flow_presentation(
      candidate
      .explanation
      .recursive_provenance
    )
  )

  position_by_step_id = {
    id(node.step.source_step): index
    for index, node in enumerate(
      presentation.nodes
    )
  }

  assert all(
    (
      position_by_step_id[
        id(edge.premise.step.source_step)
      ]
      < position_by_step_id[
        id(edge.parent.step.source_step)
      ]
    )
    for edge in presentation.edges
  )


def test_phase96_6_actual_pi9_5_root_is_last_in_dependency_first_flow():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  presentation = (
    build_toda_readable_proof_flow_presentation(
      candidate
      .explanation
      .recursive_provenance
    )
  )

  assert (
    presentation.nodes[
      -1
    ].step.source_step
    is candidate
    .explanation
    .recursive_provenance
    .root_step
  )


def test_phase96_6_shared_dependency_is_presented_once_and_reused_by_edges():
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

  provenance = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase96.shared",
      )
    )
  )

  presentation = (
    build_toda_readable_proof_flow_presentation(
      provenance
    )
  )

  shared_nodes = tuple(
    node
    for node in presentation.nodes
    if (
      node.step.source_step
      is shared_step
    )
  )

  assert len(
    shared_nodes
  ) == 1

  shared_node = shared_nodes[
    0
  ]

  assert (
    shared_node.incoming_use_count
    == 2
  )
  assert (
    shared_node.is_shared_dependency
  )

  incoming_edges = tuple(
    edge
    for edge in presentation.edges
    if (
      edge.premise
      is shared_node
    )
  )

  assert len(
    incoming_edges
  ) == 2
  assert (
    incoming_edges[
      0
    ].parent.step.source_step
    is first_step
  )
  assert (
    incoming_edges[
      1
    ].parent.step.source_step
    is second_step
  )


def test_phase96_6_shared_dependency_flow_order_is_stable():
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

  provenance = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase96.shared-order",
      )
    )
  )

  presentation = (
    build_toda_readable_proof_flow_presentation(
      provenance
    )
  )

  assert tuple(
    node.step.source_step
    for node in presentation.nodes
  ) == (
    shared_step,
    first_step,
    second_step,
    root_step,
  )


def test_phase96_6_edge_order_and_original_premise_index_are_preserved():
  first_leaf = build_test_step(
    "first leaf",
  )

  second_leaf = build_test_step(
    "second leaf",
  )

  parent = build_test_step(
    "parent",
    premises=(
      "non proof premise",
      first_leaf,
      second_leaf,
    ),
  )

  root = build_test_step(
    "root",
    premises=(
      parent,
    ),
  )

  provenance = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root,
        "phase96.edge-order",
      )
    )
  )

  presentation = (
    build_toda_readable_proof_flow_presentation(
      provenance
    )
  )

  assert all(
    isinstance(
      edge,
      TodaProofFlowEdgePresentation,
    )
    for edge in presentation.edges
  )

  assert tuple(
    edge.source_edge
    for edge in presentation.edges
  ) == provenance.edges

  parent_edges = tuple(
    edge
    for edge in presentation.edges
    if (
      edge.parent.step.source_step
      is parent
    )
  )

  assert tuple(
    edge.premise_index
    for edge in parent_edges
  ) == (
    1,
    2,
  )


def test_phase96_6_equal_but_distinct_steps_remain_distinct_presentations():
  first_step = build_test_step(
    "same",
  )

  second_step = build_test_step(
    "same",
  )

  assert first_step == second_step
  assert first_step is not second_step

  root_step = build_test_step(
    "root",
    premises=(
      first_step,
      second_step,
    ),
  )

  provenance = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase96.equal-distinct",
      )
    )
  )

  presentation = (
    build_toda_readable_proof_flow_presentation(
      provenance
    )
  )

  same_nodes = tuple(
    node
    for node in presentation.nodes
    if (
      node.step.source_step
      is first_step
      or node.step.source_step
      is second_step
    )
  )

  assert len(
    same_nodes
  ) == 2


def test_phase96_6_cycle_is_safe_and_keeps_each_node_once():
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

  provenance = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase96.cycle",
      )
    )
  )

  presentation = (
    build_toda_readable_proof_flow_presentation(
      provenance
    )
  )

  assert len(
    presentation.nodes
  ) == 2

  assert {
    id(node.step.source_step)
    for node in presentation.nodes
  } == {
    id(root_step),
    id(child_step),
  }

  assert len(
    presentation.edges
  ) == 2


def test_phase96_6_self_cycle_is_safe_and_keeps_single_node():
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

  provenance = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase96.self-cycle",
      )
    )
  )

  presentation = (
    build_toda_readable_proof_flow_presentation(
      provenance
    )
  )

  assert len(
    presentation.nodes
  ) == 1
  assert (
    presentation.nodes[
      0
    ].step.source_step
    is root_step
  )
  assert len(
    presentation.edges
  ) == 1


def test_phase96_6_repository_metadata_can_be_attached_without_changing_flow_order():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  provenance = (
    candidate
    .explanation
    .recursive_provenance
  )

  root_entry = (
    candidate
    .group_result
    .source_entry
  )

  presentation = (
    build_toda_readable_proof_flow_presentation(
      provenance,
      (
        root_entry,
      ),
    )
  )

  assert (
    presentation.root
    .step
    .repository_sources[
      0
    ].source_entry
    is root_entry
  )

  assert (
    presentation.nodes[
      -1
    ]
    is presentation.root
  )


def test_phase96_6_flow_nodes_preserve_source_node_identity():
  data = build_phase95_20_data()

  candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  provenance = (
    candidate
    .explanation
    .recursive_provenance
  )

  presentation = (
    build_toda_readable_proof_flow_presentation(
      provenance
    )
  )

  source_node_ids = {
    id(node)
    for node in provenance.nodes
  }

  assert all(
    id(node.source_node)
    in source_node_ids
    for node in presentation.nodes
  )


def test_phase96_6_builder_rejects_non_provenance():
  with pytest.raises(
    TypeError,
    match=(
      "provenance must be "
      "a TodaRecursiveProofProvenanceResult"
    ),
  ):
    build_toda_readable_proof_flow_presentation(
      "not-provenance"
    )


def test_phase96_6_builder_rejects_non_tuple_repository_entries():
  root_step = build_test_step(
    "root",
  )

  provenance = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase96.invalid-repository",
      )
    )
  )

  with pytest.raises(
    TypeError,
    match=(
      "repository_entries must be a tuple"
    ),
  ):
    build_toda_readable_proof_flow_presentation(
      provenance,
      [],
    )


def test_phase96_6_node_rejects_negative_incoming_use_count():
  root_step = build_test_step(
    "root",
  )

  provenance = (
    extract_toda_recursive_proof_provenance(
      build_synthetic_group_result(
        root_step,
        "phase96.invalid-count",
      )
    )
  )

  source_node = provenance.nodes[
    0
  ]

  from toda_proof_presentation import (
    build_toda_proof_step_presentation,
  )

  with pytest.raises(
    ValueError,
    match=(
      "incoming_use_count must be "
      "non-negative"
    ),
  ):
    TodaProofFlowNodePresentation(
      source_node=source_node,
      step=(
        build_toda_proof_step_presentation(
          root_step
        )
      ),
      incoming_use_count=-1,
    )
