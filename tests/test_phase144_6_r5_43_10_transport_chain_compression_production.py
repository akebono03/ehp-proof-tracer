import pytest

from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_connector_lines,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_hidden_bridge_semantics import (
  TodaGroupProofNarrativeHiddenBridgeOperationKind,
  TodaGroupProofNarrativeHiddenBridgeSemanticRole,
  build_toda_group_proof_narrative_hidden_bridge_semantics,
)


_EXPECTED_CONNECTOR = (
  "Proposition 5.3 を順次適用し、"
  "suspension による安定化を用いると、"
)


def _ordered_from_context(
  context,
):
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = context
  base = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )
  ordered = build_toda_group_proof_narrative_ordered_contributions(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
    current_markdown=base,
  )

  return (
    presentation,
    ordered,
  )


def _connected_from_context(
  context,
):
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = context

  return (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )


@pytest.fixture(
  scope="module",
)
def contexts_by_target():
  return {
    (n, k): _context(
      n,
      k,
    )
    for n, k in TARGETS
  }


@pytest.fixture(
  scope="module",
)
def hidden_bridge_semantics_by_target(
  contexts_by_target,
):
  return {
    target: build_toda_group_proof_narrative_hidden_bridge_semantics(
      context[
        0
      ]
    )
    for target, context in contexts_by_target.items()
  }


@pytest.fixture(
  scope="module",
)
def ordered_by_target(
  contexts_by_target,
):
  return {
    target: _ordered_from_context(
      context
    )
    for target, context in contexts_by_target.items()
  }


@pytest.fixture(
  scope="module",
)
def pi6_connected(
  contexts_by_target,
):
  return _connected_from_context(
    contexts_by_target[
      (
        3,
        3,
      )
    ]
  )


def test_phase144_6_r5_43_10_transport_semantics_have_reference_metadata(
  hidden_bridge_semantics_by_target,
):
  for n, k in TARGETS:
    semantics = hidden_bridge_semantics_by_target[
      (
        n,
        k,
      )
    ]
    transports = tuple(
      semantic
      for semantic in semantics
      if (
        semantic.role
        is TodaGroupProofNarrativeHiddenBridgeSemanticRole
        .TRANSPORT
      )
    )

    assert transports
    assert {
      semantic.reference_identity
      for semantic in transports
    } == {
      "Proposition 5.3",
    }


def test_phase144_6_r5_43_10_each_transport_triplet_has_one_suspension_stabilization(
  hidden_bridge_semantics_by_target,
):
  for n, k in TARGETS:
    semantics = hidden_bridge_semantics_by_target[
      (
        n,
        k,
      )
    ]
    transports = tuple(
      semantic
      for semantic in semantics
      if (
        semantic.role
        is TodaGroupProofNarrativeHiddenBridgeSemanticRole
        .TRANSPORT
      )
    )

    assert len(
      transports
    ) % 3 == 0
    assert sum(
      1
      for semantic in transports
      if (
        semantic.operation_kind
        is TodaGroupProofNarrativeHiddenBridgeOperationKind
        .SUSPENSION_STABILIZATION
      )
    ) == len(
      transports
    ) // 3


def test_phase144_6_r5_43_10_pi6_transport_semantics_support_compression_connector():
  context = _context(
    3,
    3,
  )
  presentation = context[
    0
  ]

  semantics = (
    build_toda_group_proof_narrative_hidden_bridge_semantics(
      presentation
    )
  )
  transports = tuple(
    semantic
    for semantic in semantics
    if (
      semantic.role
      is TodaGroupProofNarrativeHiddenBridgeSemanticRole
      .TRANSPORT
    )
  )

  assert transports
  assert {
    semantic.reference_identity
    for semantic in transports
  } == {
    "Proposition 5.3",
  }
  assert any(
    semantic.operation_kind
    is TodaGroupProofNarrativeHiddenBridgeOperationKind
    .SUSPENSION_STABILIZATION
    for semantic in transports
  )


def test_phase144_6_r5_43_10_all_sixteen_uniform_chains_receive_compression_connector(
  ordered_by_target,
):
  connector_count = 0

  for n, k in TARGETS:
    presentation, ordered = ordered_by_target[
      (
        n,
        k,
      )
    ]
    connectors = _contribution_connector_lines(
      presentation,
      ordered,
    )
    connector_count += sum(
      1
      for connector in connectors.values()
      if connector == _EXPECTED_CONNECTOR
    )

  assert connector_count == 16


def test_phase144_6_r5_43_10_preserves_direct_connector(
  ordered_by_target,
  pi6_connected,
):
  presentation, ordered = ordered_by_target[
    (
      3,
      3,
    )
  ]
  contributions = next(
    rows
    for rows in ordered
    if rows
  )
  c4 = _render_generic_narrative_step(
    contributions[
      3
    ].proof_step
  )
  c5 = _render_generic_narrative_step(
    contributions[
      4
    ].proof_step
  )

  c4_index = pi6_connected.find(
    c4
  )
  connector_index = pi6_connected.find(
    "これより、",
    c4_index + len(
      c4
    ),
  )
  c5_index = pi6_connected.find(
    c5,
    connector_index + len(
      "これより、"
    ),
  )

  assert c4_index >= 0
  assert connector_index > c4_index
  assert c5_index > connector_index


def test_phase144_6_r5_43_10_renderer_does_not_read_inference_rule_names():
  import inspect
  import toda_group_proof_narrative_contribution_renderer as module

  source = inspect.getsource(
    module
  )

  assert "inference_rule" not in source
  assert "finite-cyclic transport" not in source
  assert "eta_4 squared stable transport" not in source


