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






def test_phase144_6_r5_43_10_renderer_does_not_hard_code_historical_rule_names():
  import inspect
  import toda_group_proof_narrative_contribution_renderer as module

  source = inspect.getsource(module)

  assert "finite-cyclic transport" not in source
  assert "eta_4 squared stable transport" not in source


