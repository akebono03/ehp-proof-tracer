from audit_phase144_6_r5_41 import build_topological_order_audit
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import TARGETS


def test_phase144_6_r5_41_selected_population_matches_phase40():
  audits, nodes = build_topological_order_audit()
  assert len(nodes) == 190


def test_phase144_6_r5_41_covers_six_groups():
  audits, nodes = build_topological_order_audit()
  assert {(node.n, node.k) for node in nodes} == set(TARGETS)


def test_phase144_6_r5_41_every_selected_node_is_ordered_once():
  audits, nodes = build_topological_order_audit()
  assert sum(a.node_count for a in audits) == len(nodes)
  assert all(len(a.stable_order_keys) == a.node_count for a in audits)


def test_phase144_6_r5_41_has_no_dependency_cycle():
  audits, nodes = build_topological_order_audit()
  assert all(a.max_ready_width >= 1 for a in audits)


def test_phase144_6_r5_41_unique_orders_need_no_tiebreak():
  audits, nodes = build_topological_order_audit()
  assert all(
    a.tie_break_steps == 0
    for a in audits
    if a.unique_topological_order
  )


def test_phase144_6_r5_41_pi6_five_contributions_are_unique_chain():
  audits, nodes = build_topological_order_audit()
  pi6 = tuple(a for a in audits if (a.n, a.k) == (3, 3) and a.node_count == 5)
  assert len(pi6) == 1
  assert pi6[0].unique_topological_order
  assert pi6[0].max_ready_width == 1
  assert pi6[0].tie_break_steps == 0


def test_phase144_6_r5_41_pi6_order_has_five_distinct_keys():
  audits, nodes = build_topological_order_audit()
  pi6 = next(a for a in audits if (a.n, a.k) == (3, 3) and a.node_count == 5)
  assert len(set(pi6.stable_order_keys)) == 5
