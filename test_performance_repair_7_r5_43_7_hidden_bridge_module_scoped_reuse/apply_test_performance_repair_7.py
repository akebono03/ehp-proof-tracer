from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path(
  "tests/test_phase144_6_r5_43_7_hidden_bridge_semantic_classification_foundation.py"
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

replacement_text = 'from collections import Counter\n\nimport pytest\n\nfrom audit_phase144_6_r5_43_6 import (\n  build_hidden_bridge_inventory,\n)\nfrom test_phase144_6_r5_18_production_generic_proof_chain_foundation import (\n  TARGETS,\n  _context,\n)\nfrom toda_group_proof_narrative_hidden_bridge_semantics import (\n  TodaGroupProofNarrativeHiddenBridgeSemanticRole,\n  build_toda_group_proof_narrative_hidden_bridge_semantics,\n)\n\n\n_EXPECTED_ROLE_BY_AUDIT_CLASSIFICATION = {\n  "transport_candidate": (\n    TodaGroupProofNarrativeHiddenBridgeSemanticRole\n    .TRANSPORT\n  ),\n  "integration_provenance_candidate": (\n    TodaGroupProofNarrativeHiddenBridgeSemanticRole\n    .INTEGRATION_PROVENANCE\n  ),\n}\n\n\ndef _semantic_by_signature():\n  result = {}\n\n  for n, k in TARGETS:\n    presentation = _context(\n      n,\n      k,\n    )[0]\n    semantics = (\n      build_toda_group_proof_narrative_hidden_bridge_semantics(\n        presentation\n      )\n    )\n\n    for semantic in semantics:\n      rule = (\n        semantic.proof_step.inference_rule\n      )\n      rule_name = (\n        None\n        if rule is None\n        else rule.name\n      )\n      key = (\n        type(\n          semantic.proof_step.conclusion\n        ).__name__,\n        rule_name,\n      )\n      existing = result.get(\n        key\n      )\n\n      if (\n        existing is not None\n        and existing is not semantic.role\n      ):\n        raise AssertionError(\n          "semantic signature has conflicting roles"\n        )\n\n      result[\n        key\n      ] = semantic.role\n\n  return result\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef hidden_bridge_inventory():\n  return build_hidden_bridge_inventory()\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef semantic_by_signature():\n  return _semantic_by_signature()\n\n\ndef test_phase144_6_r5_43_7_reproduces_all_r5_43_6_hidden_bridge_signatures(\n  hidden_bridge_inventory,\n  semantic_by_signature,\n):\n  audit_rows = hidden_bridge_inventory\n\n  assert len(\n    audit_rows\n  ) == 64\n\n  for row in audit_rows:\n    signature = (\n      row[\n        "statement_type"\n      ],\n      row[\n        "rule_name"\n      ],\n    )\n    assert (\n      semantic_by_signature[\n        signature\n      ]\n      is _EXPECTED_ROLE_BY_AUDIT_CLASSIFICATION[\n        row[\n          "classification"\n        ]\n      ]\n    )\n\n\ndef test_phase144_6_r5_43_7_r5_43_6_population_has_two_semantic_roles(\n  hidden_bridge_inventory,\n  semantic_by_signature,\n):\n  audit_rows = hidden_bridge_inventory\n  actual = Counter(\n    semantic_by_signature[\n      (\n        row[\n          "statement_type"\n        ],\n        row[\n          "rule_name"\n        ],\n      )\n    ]\n    for row in audit_rows\n  )\n\n  assert actual == {\n    (\n      TodaGroupProofNarrativeHiddenBridgeSemanticRole\n      .TRANSPORT\n    ): 48,\n    (\n      TodaGroupProofNarrativeHiddenBridgeSemanticRole\n      .INTEGRATION_PROVENANCE\n    ): 16,\n  }\n\n\ndef test_phase144_6_r5_43_7_builder_returns_deterministic_presentation_order():\n  for n, k in TARGETS:\n    presentation = _context(\n      n,\n      k,\n    )[0]\n    first = (\n      build_toda_group_proof_narrative_hidden_bridge_semantics(\n        presentation\n      )\n    )\n    second = (\n      build_toda_group_proof_narrative_hidden_bridge_semantics(\n        presentation\n      )\n    )\n    node_position = {\n      id(\n        node.proof_step\n      ): index\n      for index, node in enumerate(\n        presentation.nodes\n      )\n    }\n\n    assert tuple(\n      id(\n        semantic.proof_step\n      )\n      for semantic in first\n    ) == tuple(\n      id(\n        semantic.proof_step\n      )\n      for semantic in second\n    )\n    assert tuple(\n      node_position[\n        id(\n          semantic.proof_step\n        )\n      ]\n      for semantic in first\n    ) == tuple(\n      sorted(\n        node_position[\n          id(\n            semantic.proof_step\n          )\n        ]\n        for semantic in first\n      )\n    )\n\n\ndef test_phase144_6_r5_43_7_production_module_does_not_import_audit_modules():\n  import inspect\n  import toda_group_proof_narrative_hidden_bridge_semantics as module\n\n  source = inspect.getsource(\n    module\n  )\n\n  assert "from audit_" not in source\n  assert "import audit_" not in source\n\n\ndef test_phase144_6_r5_43_7_public_route_remains_unchanged_after_r5_43_10():\n  import inspect\n  import toda_group_proof_narrative_contribution_renderer as renderer\n\n  renderer_source = inspect.getsource(\n    renderer\n  )\n\n  assert (\n    "toda_group_proof_narrative_hidden_bridge_semantics"\n    in renderer_source\n  )\n  assert "inference_rule" not in renderer_source\n  assert "n == 3" not in renderer_source\n  assert "k == 3" not in renderer_source\n'
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
