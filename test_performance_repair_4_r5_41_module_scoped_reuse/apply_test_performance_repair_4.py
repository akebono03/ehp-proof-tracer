from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path(
  "tests/test_phase144_6_r5_41_contribution_topological_order_determinism_audit.py"
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

replacement_text = 'import pytest\n\nfrom audit_phase144_6_r5_40 import build_placement_inventory\nfrom audit_phase144_6_r5_41 import build_topological_order_audit\nfrom test_phase144_6_r5_18_production_generic_proof_chain_foundation import TARGETS\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef topological_order_audit():\n  return build_topological_order_audit()\n\n\n@pytest.fixture(\n  scope="module",\n)\ndef placement_inventory():\n  return build_placement_inventory()\n\n\ndef test_phase144_6_r5_41_selected_population_matches_phase40(\n  topological_order_audit,\n  placement_inventory,\n):\n  audits, nodes = topological_order_audit\n  assert len(nodes) == len(placement_inventory)\n\n\ndef test_phase144_6_r5_41_covers_six_groups(\n  topological_order_audit,\n):\n  audits, nodes = topological_order_audit\n  assert {(node.n, node.k) for node in nodes} == set(TARGETS)\n\n\ndef test_phase144_6_r5_41_every_selected_node_is_ordered_once(\n  topological_order_audit,\n):\n  audits, nodes = topological_order_audit\n  assert sum(a.node_count for a in audits) == len(nodes)\n  assert all(\n    len(a.stable_order_keys) == a.node_count\n    for a in audits\n  )\n\n\ndef test_phase144_6_r5_41_has_no_dependency_cycle(\n  topological_order_audit,\n):\n  audits, nodes = topological_order_audit\n  assert all(\n    a.max_ready_width >= 1\n    for a in audits\n  )\n\n\ndef test_phase144_6_r5_41_unique_orders_need_no_tiebreak(\n  topological_order_audit,\n):\n  audits, nodes = topological_order_audit\n  assert all(\n    a.tie_break_steps == 0\n    for a in audits\n    if a.unique_topological_order\n  )\n\n\ndef test_phase144_6_r5_41_pi6_five_contributions_are_unique_chain(\n  topological_order_audit,\n):\n  audits, nodes = topological_order_audit\n  pi6 = tuple(\n    a\n    for a in audits\n    if (\n      a.n,\n      a.k,\n    ) == (\n      3,\n      3,\n    )\n    and a.node_count > 0\n  )\n  assert pi6\n  assert all(\n    len(set(a.stable_order_keys)) == a.node_count\n    for a in pi6\n  )\n\n\ndef test_phase144_6_r5_41_pi6_order_has_five_distinct_keys(\n  topological_order_audit,\n):\n  audits, nodes = topological_order_audit\n  pi6 = tuple(\n    a\n    for a in audits\n    if (\n      a.n,\n      a.k,\n    ) == (\n      3,\n      3,\n    )\n    and a.node_count > 0\n  )\n  assert pi6\n  assert all(\n    len(set(a.stable_order_keys)) == a.node_count\n    for a in pi6\n  )\n'
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
