from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path(
  "tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py"
)

subprocess.run(
  [
    "git",
    "checkout",
    "--",
    str(TARGET).replace("\\\\", "/"),
  ],
  cwd=ROOT,
  check=True,
)

path = ROOT / TARGET
original = path.read_bytes()
newline = b"\r\n" if b"\r\n" in original else b"\n"

replacement_text = 'import pytest\n\nfrom test_phase144_6_r5_18_production_generic_proof_chain_foundation import (\n  TARGETS,\n  _context,\n)\nfrom toda_group_proof_generic_narrative_renderer import (\n  _render_generic_narrative_step,\n)\nfrom toda_group_proof_narrative_argument_multi_renderer import (\n  render_toda_group_proof_narrative_multi_argument_markdown,\n)\nfrom toda_group_proof_narrative_contribution_ordering import (\n  build_toda_group_proof_narrative_ordered_contributions,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _contribution_connector_lines,\n  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,\n)\nfrom toda_group_proof_narrative_hidden_bridge_semantics import (\n  TodaGroupProofNarrativeHiddenBridgeOperationKind,\n  TodaGroupProofNarrativeHiddenBridgeSemanticRole,\n  build_toda_group_proof_narrative_hidden_bridge_semantics,\n)\n\n\n_EXPECTED_CONNECTOR = (\n  "Proposition 5.3 を順次適用し、"\n  "suspension による安定化を用いると、"\n)\n\n\ndef _data_from_context(\n  context,\n):\n  (\n    presentation,\n    semantic_sidecar,\n    blocks,\n    arguments,\n    aggregate_semantic_sidecar,\n    proof_chains,\n  ) = context\n  base = render_toda_group_proof_narrative_multi_argument_markdown(\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n  )\n  ordered = build_toda_group_proof_narrative_ordered_contributions(\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n    proof_chains,\n    current_markdown=base,\n  )\n  connected = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n\n  return (\n    presentation,\n    ordered,\n    connected,\n  )\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef contexts_by_target():\n  return {\n    (n, k): _context(\n      n,\n      k,\n    )\n    for n, k in TARGETS\n  }\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef hidden_bridge_semantics_by_target(\n  contexts_by_target,\n):\n  return {\n    target: build_toda_group_proof_narrative_hidden_bridge_semantics(\n      context[\n        0\n      ]\n    )\n    for target, context in contexts_by_target.items()\n  }\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef data_by_target(\n  contexts_by_target,\n):\n  return {\n    target: _data_from_context(\n      context\n    )\n    for target, context in contexts_by_target.items()\n  }\n\n\ndef test_phase144_6_r5_43_10_transport_semantics_have_reference_metadata(\n  hidden_bridge_semantics_by_target,\n):\n  for n, k in TARGETS:\n    semantics = hidden_bridge_semantics_by_target[\n      (\n        n,\n        k,\n      )\n    ]\n    transports = tuple(\n      semantic\n      for semantic in semantics\n      if (\n        semantic.role\n        is TodaGroupProofNarrativeHiddenBridgeSemanticRole\n        .TRANSPORT\n      )\n    )\n\n    assert transports\n    assert {\n      semantic.reference_identity\n      for semantic in transports\n    } == {\n      "Proposition 5.3",\n    }\n\n\ndef test_phase144_6_r5_43_10_each_transport_triplet_has_one_suspension_stabilization(\n  hidden_bridge_semantics_by_target,\n):\n  for n, k in TARGETS:\n    semantics = hidden_bridge_semantics_by_target[\n      (\n        n,\n        k,\n      )\n    ]\n    transports = tuple(\n      semantic\n      for semantic in semantics\n      if (\n        semantic.role\n        is TodaGroupProofNarrativeHiddenBridgeSemanticRole\n        .TRANSPORT\n      )\n    )\n\n    assert len(\n      transports\n    ) % 3 == 0\n    assert sum(\n      1\n      for semantic in transports\n      if (\n        semantic.operation_kind\n        is TodaGroupProofNarrativeHiddenBridgeOperationKind\n        .SUSPENSION_STABILIZATION\n      )\n    ) == len(\n      transports\n    ) // 3\n\n\ndef test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3(\n  data_by_target,\n):\n  presentation, ordered, connected = data_by_target[\n    (\n      3,\n      3,\n    )\n  ]\n  contributions = next(\n    rows\n    for rows in ordered\n    if rows\n  )\n  c2 = _render_generic_narrative_step(\n    contributions[\n      1\n    ].proof_step\n  )\n  c3 = _render_generic_narrative_step(\n    contributions[\n      2\n    ].proof_step\n  )\n\n  assert (\n    c2\n    + "\\n\\n"\n    + _EXPECTED_CONNECTOR\n    + "\\n\\n"\n    + c3\n  ) in connected\n\n\ndef test_phase144_6_r5_43_10_all_sixteen_uniform_chains_receive_compression_connector(\n  data_by_target,\n):\n  connector_count = 0\n\n  for n, k in TARGETS:\n    presentation, ordered, connected = data_by_target[\n      (\n        n,\n        k,\n      )\n    ]\n    connectors = _contribution_connector_lines(\n      presentation,\n      ordered,\n    )\n    connector_count += sum(\n      1\n      for connector in connectors.values()\n      if connector == _EXPECTED_CONNECTOR\n    )\n\n  assert connector_count == 16\n\n\ndef test_phase144_6_r5_43_10_preserves_direct_connector(\n  data_by_target,\n):\n  presentation, ordered, connected = data_by_target[\n    (\n      3,\n      3,\n    )\n  ]\n  contributions = next(\n    rows\n    for rows in ordered\n    if rows\n  )\n  c4 = _render_generic_narrative_step(\n    contributions[\n      3\n    ].proof_step\n  )\n  c5 = _render_generic_narrative_step(\n    contributions[\n      4\n    ].proof_step\n  )\n\n  assert (\n    c4\n    + "\\n\\nこれより、\\n\\n"\n    + c5\n  ) in connected\n\n\ndef test_phase144_6_r5_43_10_renderer_does_not_read_inference_rule_names():\n  import inspect\n  import toda_group_proof_narrative_contribution_renderer as module\n\n  source = inspect.getsource(\n    module\n  )\n\n  assert "inference_rule" not in source\n  assert "finite-cyclic transport" not in source\n  assert "eta_4 squared stable transport" not in source\n\n\ndef test_phase144_6_r5_43_10_has_no_pi6_specific_branch():\n  import inspect\n  import toda_group_proof_narrative_contribution_renderer as module\n\n  source = inspect.getsource(\n    module\n  )\n\n  assert "n == 3" not in source\n  assert "k == 3" not in source\n  assert "_pi6" not in source.lower()\n'
replacement = replacement_text.encode("utf-8").replace(
  b"\n",
  newline,
)
path.write_bytes(replacement)

print("Updated:", TARGET)
print(
  "Preserved newline:",
  "CRLF" if newline == b"\r\n" else "LF",
)
print("Production changes: none")
print("Audit builder changes: none")
