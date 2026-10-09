"""Focused observational checks; no production changes."""
from phase162_r4_a_stable_tree_narrative_audit.phase162_r4_a_audit import audit, collect_steps
from tests.test_phase143_19_method_evidence import _method_evidence_data


def test_r4_a_tree_traversal_preserves_root_and_premises():
    presentation, _, _, _ = _method_evidence_data(4, 1)
    steps = collect_steps(presentation.root_step)
    assert steps
    assert steps[0]["conclusion_repr"] == repr(presentation.root_step.conclusion)
    assert all(step["premise_count"] >= 0 for step in steps)
    assert len({step["object_id"] for step in steps}) == len(steps)


def test_r4_a_comparison_is_observational_and_retains_outputs():
    report = audit()
    assert report["presentation_node_count"] >= 1
    assert report["root_nodes_in_presentation"] == 1
    assert "## 証明" in report["public_markdown"]
    assert isinstance(report["baseline_markdown"], str)
    assert report["baseline_markdown"] or report["baseline_error"]
    assert set(report["checks"]) == {
        "toda45", "base_group", "generator_transport", "target_structure"
    }
    assert all(item["status"] in {
        "TREE_PRESENT_CANDIDATE", "PRESENTATION_ONLY_CANDIDATE",
        "RENDERER_ONLY_CANDIDATE", "MISSING"
    } for item in report["checks"].values())
