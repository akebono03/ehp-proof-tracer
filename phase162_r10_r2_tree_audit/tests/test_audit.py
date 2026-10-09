"""Focused R10-R2 graph audit tests. No project-wide pytest."""

from phase162_r10_r2_tree_audit.audit import build_audit, ordered_ancestry, parent_chains
from proof import ProofRule, ProofStep


def test_ordered_ancestry_identity_and_shared_premises():
    premise = ProofStep(conclusion="premise", premises=(), rule=ProofRule.GIVEN)
    left = ProofStep(conclusion="left", premises=(premise,), rule=ProofRule.INFERENCE)
    right = ProofStep(conclusion="right", premises=(premise,), rule=ProofRule.INFERENCE)
    root = ProofStep(conclusion="root", premises=(left, right), rule=ProofRule.INFERENCE)
    nodes = ordered_ancestry(root)
    assert len(nodes) == 4
    assert nodes[0] is premise
    assert nodes[-1] is root
    assert len(parent_chains(root, premise)) == 2


def test_r10_r2_web_root_matches_auxiliary_goal():
    report = build_audit()
    web = report["graphs"]["web_replay"]
    auxiliary = report["graphs"]["r10_auxiliary_connection"]
    assert web["root"] == auxiliary["root"]
    assert web["summary"]["node_count"] > 0
    assert web["summary"]["hopf_nodes"]
    assert auxiliary["summary"]["hopf_nodes"]


def test_r10_r2_citation_paths_are_explicit():
    report = build_audit()
    for graph in report["graphs"].values():
        numbered = {row["node"]: row for row in graph["nodes"]}
        for node in graph["summary"]["citation_nodes"]:
            assert numbered[node]["foundational_key"]
            assert graph["node_paths"][str(node)]
        for node in graph["summary"]["hopf_nodes"]:
            assert graph["node_paths"][str(node)]
