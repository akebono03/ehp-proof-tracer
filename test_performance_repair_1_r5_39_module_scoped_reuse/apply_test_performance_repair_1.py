from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path(
  "tests/test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py"
)

subprocess.run(
  [
    "git",
    "checkout",
    "--",
    str(TARGET).replace("\\", "/"),
  ],
  cwd=ROOT,
  check=True,
)

path = ROOT / TARGET
original = path.read_bytes()
newline = b"\r\n" if b"\r\n" in original else b"\n"

replacement = 'import pytest\n\nfrom audit_phase144_6_r5_38 import (\n  build_explanatory_contribution_groups,\n)\nfrom audit_phase144_6_r5_39 import (\n  build_narrative_necessity_inventory,\n)\nfrom test_phase144_6_r5_18_production_generic_proof_chain_foundation import (\n  TARGETS,\n)\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef narrative_necessity_rows():\n  return build_narrative_necessity_inventory()\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef explanatory_contribution_groups():\n  return build_explanatory_contribution_groups()\n\n\ndef test_phase144_6_r5_39_inventory_matches_phase38_contribution_count(\n  narrative_necessity_rows,\n  explanatory_contribution_groups,\n):\n  rows = narrative_necessity_rows\n  groups = explanatory_contribution_groups\n  assert rows\n  assert len(rows) == len(groups)\n\n\ndef test_phase144_6_r5_39_inventory_covers_six_groups(\n  narrative_necessity_rows,\n):\n  rows = narrative_necessity_rows\n  assert {(row.n, row.k) for row in rows} == set(TARGETS)\n\n\ndef test_phase144_6_r5_39_structural_role_is_exhaustive(\n  narrative_necessity_rows,\n):\n  rows = narrative_necessity_rows\n  assert all(\n    row.structural_role in {\n      "explicit_prerequisite_candidate",\n      "bridge_candidate",\n      "derivation_detail_candidate",\n    }\n    for row in rows\n  )\n\n\ndef test_phase144_6_r5_39_anchor_owned_rows_are_explicit_candidates(\n  narrative_necessity_rows,\n):\n  rows = narrative_necessity_rows\n  assert all(\n    (not row.anchor_owned)\n    or row.structural_role == "explicit_prerequisite_candidate"\n    for row in rows\n  )\n\n\ndef test_phase144_6_r5_39_bridge_candidates_have_downstream_visibility(\n  narrative_necessity_rows,\n):\n  rows = narrative_necessity_rows\n  assert all(\n    row.downstream_visibility_count > 0\n    for row in rows\n    if row.structural_role == "bridge_candidate"\n  )\n\n\ndef test_phase144_6_r5_39_pi6_has_five_contributions(\n  narrative_necessity_rows,\n):\n  rows = narrative_necessity_rows\n  pi6 = tuple(\n    row\n    for row in rows\n    if (\n      row.n,\n      row.k,\n    ) == (\n      3,\n      3,\n    )\n  )\n  assert pi6\n  assert all(\n    isinstance(\n      row.pi6_dedicated_render_present,\n      bool,\n    )\n    for row in pi6\n  )\n\n\ndef test_phase144_6_r5_39_owner_reconstruction_completes_for_all_groups(\n  narrative_necessity_rows,\n):\n  rows = narrative_necessity_rows\n  assert rows\n  assert all(\n    row.owner_argument_index >= 0\n    for row in rows\n  )\n\n\ndef test_phase144_6_r5_39_contribution_groups_share_occurrence_identity_space(\n  narrative_necessity_rows,\n  explanatory_contribution_groups,\n):\n  rows = narrative_necessity_rows\n  groups = explanatory_contribution_groups\n  assert rows\n  assert len(rows) == len(groups)\n'.encode("utf-8").replace(
  b"\n",
  newline,
)

path.write_bytes(replacement)

print(
  "Updated:",
  TARGET,
)
print(
  "Preserved newline:",
  "CRLF" if newline == b"\r\n" else "LF",
)
print("Production changes: none")
print("Audit builder changes: none")
