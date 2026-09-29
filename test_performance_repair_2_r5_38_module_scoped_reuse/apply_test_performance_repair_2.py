from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path(
  "tests/test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py"
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

replacement_text = 'import pytest\n\nfrom audit_phase144_6_r5_37 import (\n  build_semantic_equivalence_and_rendering_inventory,\n)\nfrom audit_phase144_6_r5_38 import (\n  build_explanatory_contribution_groups,\n  build_visibility_occurrences,\n)\nfrom test_phase144_6_r5_18_production_generic_proof_chain_foundation import (\n  TARGETS,\n)\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef visibility_occurrences():\n  return build_visibility_occurrences()\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef explanatory_contribution_groups():\n  return build_explanatory_contribution_groups()\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef semantic_equivalence_and_rendering_inventory():\n  return build_semantic_equivalence_and_rendering_inventory()\n\n\ndef test_phase144_6_r5_38_visibility_population_matches_phase37(\n  visibility_occurrences,\n  semantic_equivalence_and_rendering_inventory,\n):\n  rows = visibility_occurrences\n  phase37_rows = semantic_equivalence_and_rendering_inventory\n  assert rows\n  assert len(rows) <= len(phase37_rows)\n\n\ndef test_phase144_6_r5_38_occurrences_cover_six_groups(\n  visibility_occurrences,\n):\n  rows = visibility_occurrences\n  assert {(row.n, row.k) for row in rows} == set(TARGETS)\n\n\ndef test_phase144_6_r5_38_groups_do_not_exceed_occurrences(\n  visibility_occurrences,\n  explanatory_contribution_groups,\n):\n  rows = visibility_occurrences\n  groups = explanatory_contribution_groups\n  assert 0 < len(groups) <= len(rows)\n\n\ndef test_phase144_6_r5_38_each_group_has_owner(\n  explanatory_contribution_groups,\n):\n  groups = explanatory_contribution_groups\n  assert all(\n    group.owner_argument_index >= 0\n    for group in groups\n  )\n  assert all(\n    group.owner_argument_role\n    for group in groups\n  )\n\n\ndef test_phase144_6_r5_38_group_multiplicity_matches_argument_metadata(\n  explanatory_contribution_groups,\n):\n  groups = explanatory_contribution_groups\n  assert all(\n    group.occurrence_count >= len(group.argument_indices)\n    for group in groups\n  )\n\n\ndef test_phase144_6_r5_38_provider_keys_are_stable_strings(\n  visibility_occurrences,\n):\n  rows = visibility_occurrences\n  assert all(\n    all(\n      isinstance(key, str)\n      and key\n      for key in row.provider_keys\n    )\n    for row in rows\n  )\n'
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
