from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path(
  "tests/test_phase144_6_r5_43_4_dependency_aware_contribution_connector.py"
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

replacement_text = 'import pytest\n\nfrom test_phase144_6_r5_18_production_generic_proof_chain_foundation import (\n  _context,\n)\nfrom toda_group_proof_generic_narrative_renderer import (\n  _render_generic_narrative_step,\n)\nfrom toda_group_proof_narrative_argument_multi_renderer import (\n  render_toda_group_proof_narrative_multi_argument_markdown,\n)\nfrom toda_group_proof_narrative_contribution_ordering import (\n  build_toda_group_proof_narrative_ordered_contributions,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _contribution_connector_lines,\n  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,\n)\n\n\ndef _pi6_data():\n  (\n    presentation,\n    semantic_sidecar,\n    blocks,\n    arguments,\n    aggregate_semantic_sidecar,\n    proof_chains,\n  ) = _context(3, 3)\n  base = render_toda_group_proof_narrative_multi_argument_markdown(\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n  )\n  ordered = build_toda_group_proof_narrative_ordered_contributions(\n    presentation,\n    blocks,\n    semantic_sidecar,\n    arguments,\n    proof_chains,\n    current_markdown=base,\n  )\n  connected = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  contributions = next(\n    rows\n    for rows in ordered\n    if rows\n  )\n  return (\n    presentation,\n    base,\n    connected,\n    ordered,\n    contributions,\n  )\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef pi6_data():\n  return _pi6_data()\n\n\ndef test_phase144_6_r5_43_4_only_direct_contribution_dependency_gets_direct_connector(\n  pi6_data,\n):\n  (\n    presentation,\n    base,\n    connected,\n    ordered,\n    contributions,\n  ) = pi6_data\n  connector_by_target_step_id = (\n    _contribution_connector_lines(\n      presentation,\n      ordered,\n    )\n  )\n  direct_connector_targets = {\n    step_id\n    for step_id, connector\n    in connector_by_target_step_id.items()\n    if connector == "これより、"\n  }\n\n  assert direct_connector_targets == {\n    id(\n      contributions[4].proof_step\n    ),\n  }\n\n\ndef test_phase144_6_r5_43_4_c4_to_c5_has_connector(\n  pi6_data,\n):\n  (\n    presentation,\n    base,\n    connected,\n    ordered,\n    contributions,\n  ) = pi6_data\n  c4 = _render_generic_narrative_step(\n    contributions[3].proof_step\n  )\n  c5 = _render_generic_narrative_step(\n    contributions[4].proof_step\n  )\n  expected = (\n    c4\n    + "\\n\\nこれより、\\n\\n"\n    + c5\n  )\n\n  assert expected in connected\n\n\ndef test_phase144_6_r5_43_4_transitive_c1_c2_c3_do_not_get_false_direct_connectors(\n  pi6_data,\n):\n  (\n    presentation,\n    base,\n    connected,\n    ordered,\n    contributions,\n  ) = pi6_data\n  c1 = _render_generic_narrative_step(\n    contributions[0].proof_step\n  )\n  c2 = _render_generic_narrative_step(\n    contributions[1].proof_step\n  )\n  c3 = _render_generic_narrative_step(\n    contributions[2].proof_step\n  )\n\n  assert (\n    c1\n    + "\\n\\nこれより、\\n\\n"\n    + c2\n  ) not in connected\n  assert (\n    c2\n    + "\\n\\nこれより、\\n\\n"\n    + c3\n  ) not in connected\n\n\ndef test_phase144_6_r5_43_4_no_connector_is_inferred_from_visual_adjacency_after_c5(\n  pi6_data,\n):\n  (\n    presentation,\n    base,\n    connected,\n    ordered,\n    contributions,\n  ) = pi6_data\n  c5 = _render_generic_narrative_step(\n    contributions[4].proof_step\n  )\n  h_surjective = (\n    "$H: \\\\pi_{6}^{3} \\\\to \\\\pi_{6}^{5}$ "\n    "は全射である."\n  )\n\n  assert (\n    c5\n    + "\\n\\nこれより、\\n\\n"\n    + h_surjective\n  ) not in connected\n\n\ndef test_phase144_6_r5_43_4_preserves_r5_43_2_placement_and_uniqueness(\n  pi6_data,\n):\n  (\n    presentation,\n    base,\n    connected,\n    ordered,\n    contributions,\n  ) = pi6_data\n  lines = tuple(\n    _render_generic_narrative_step(\n      contribution.proof_step\n    )\n    for contribution in contributions\n  )\n  positions = tuple(\n    connected.index(\n      line\n    )\n    for line in lines\n  )\n  conclusion = (\n    "$\\\\pi_{6}^{3} = "\n    "\\\\mathbb{Z}/4\\\\{\\\\nu\'\\\\}$"\n  )\n  final_connector_index = connected.rfind(\n    "以上より、",\n    0,\n    connected.index(\n      conclusion\n    ),\n  )\n\n  assert positions == tuple(\n    sorted(\n      positions\n    )\n  )\n  assert all(\n    connected.count(\n      line\n    ) == 1\n    for line in lines\n  )\n  assert all(\n    position < final_connector_index\n    for position in positions\n  )\n\n\ndef test_phase144_6_r5_43_4_has_no_pi6_specific_branch():\n  import inspect\n  import toda_group_proof_narrative_contribution_renderer as module\n\n  source = inspect.getsource(\n    module\n  )\n\n  assert "n == 3" not in source\n  assert "k == 3" not in source\n  assert "_pi6" not in source.lower()\n'
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
