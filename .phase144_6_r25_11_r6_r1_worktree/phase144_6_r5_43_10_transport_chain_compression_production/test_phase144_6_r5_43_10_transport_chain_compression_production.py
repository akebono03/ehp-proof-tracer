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


def _data(
  n,
  k,
):
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(
    n,
    k,
  )
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
  connected = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  return (
    presentation,
    ordered,
    connected,
  )


def test_phase144_6_r5_43_10_transport_semantics_have_reference_metadata():
  for n, k in TARGETS:
    presentation = _context(
      n,
      k,
    )[0]
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


def test_phase144_6_r5_43_10_each_transport_triplet_has_one_suspension_stabilization():
  for n, k in TARGETS:
    presentation = _context(
      n,
      k,
    )[0]
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


def test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3():
  presentation, ordered, connected = _data(
    3,
    3,
  )
  contributions = next(
    rows
    for rows in ordered
    if rows
  )
  c2 = _render_generic_narrative_step(
    contributions[
      1
    ].proof_step
  )
  c3 = _render_generic_narrative_step(
    contributions[
      2
    ].proof_step
  )

  assert (
    c2
    + "\n\n"
    + _EXPECTED_CONNECTOR
    + "\n\n"
    + c3
  ) in connected


def test_phase144_6_r5_43_10_all_sixteen_uniform_chains_receive_compression_connector():
  connector_count = 0

  for n, k in TARGETS:
    presentation, ordered, connected = _data(
      n,
      k,
    )
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


def test_phase144_6_r5_43_10_preserves_direct_connector():
  presentation, ordered, connected = _data(
    3,
    3,
  )
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

  assert (
    c4
    + "\n\nこれより、\n\n"
    + c5
  ) in connected


def test_phase144_6_r5_43_10_renderer_does_not_read_inference_rule_names():
  import inspect
  import toda_group_proof_narrative_contribution_renderer as module

  source = inspect.getsource(
    module
  )

  assert "inference_rule" not in source
  assert "finite-cyclic transport" not in source
  assert "eta_4 squared stable transport" not in source


def test_phase144_6_r5_43_10_has_no_pi6_specific_branch():
  import inspect
  import toda_group_proof_narrative_contribution_renderer as module

  source = inspect.getsource(
    module
  )

  assert "n == 3" not in source
  assert "k == 3" not in source
  assert "_pi6" not in source.lower()
