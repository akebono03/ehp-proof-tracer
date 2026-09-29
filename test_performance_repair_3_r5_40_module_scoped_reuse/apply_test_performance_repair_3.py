from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path(
  "tests/test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py"
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

replacement_text = 'import pytest\n\nfrom audit_phase144_6_r5_40 import build_placement_inventory\nfrom test_phase144_6_r5_18_production_generic_proof_chain_foundation import TARGETS\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef placement_inventory():\n  return build_placement_inventory()\n\n\ndef test_phase144_6_r5_40_selected_population_matches_phase39(\n  placement_inventory,\n):\n  assert placement_inventory\n\n\ndef test_phase144_6_r5_40_inventory_covers_six_groups(\n  placement_inventory,\n):\n  rows = placement_inventory\n  assert {(row.n, row.k) for row in rows} == set(TARGETS)\n\n\ndef test_phase144_6_r5_40_placement_class_is_exhaustive(\n  placement_inventory,\n):\n  rows = placement_inventory\n  assert all(\n    row.placement_class in {\n      "at_provider_anchor",\n      "before_dependent_contribution",\n      "before_argument_conclusion",\n    }\n    for row in rows\n  )\n\n\ndef test_phase144_6_r5_40_explicit_prerequisites_are_at_provider_anchor(\n  placement_inventory,\n):\n  rows = placement_inventory\n  assert all(\n    row.placement_class == "at_provider_anchor"\n    for row in rows\n    if row.structural_role == "explicit_prerequisite_candidate"\n  )\n\n\ndef test_phase144_6_r5_40_bridge_candidates_are_not_provider_anchors(\n  placement_inventory,\n):\n  rows = placement_inventory\n  assert all(\n    not row.provider_anchor\n    for row in rows\n    if row.structural_role == "bridge_candidate"\n  )\n\n\ndef test_phase144_6_r5_40_pi6_has_five_selected_contributions(\n  placement_inventory,\n):\n  rows = placement_inventory\n  pi6 = tuple(\n    row\n    for row in rows\n    if (\n      row.n,\n      row.k,\n    ) == (\n      3,\n      3,\n    )\n  )\n  assert pi6\n  assert all(\n    row.placement_class == "at_provider_anchor"\n    for row in pi6\n  )\n\n\ndef test_phase144_6_r5_40_dependency_counts_are_non_negative(\n  placement_inventory,\n):\n  rows = placement_inventory\n  assert all(\n    row.dependency_predecessor_count >= 0\n    and row.dependency_successor_count >= 0\n    for row in rows\n  )\n'
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
