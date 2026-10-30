"""Focused R17 context-comparison and independent-goal audit tests."""
from __future__ import annotations

import pytest

from phase171_r2j_r4_r9_r17_public_context_path_audit import audit


def _states(default="unresolved"):
    return {name: default for name in audit.PROBES}


def test_refuses_mutating_git_commands():
    with pytest.raises(ValueError):
        audit.git_read("reset", "--hard")
    with pytest.raises(ValueError):
        audit.git_read("add", "phase165_r52_r9_shared_math.py")


def test_r16_baseline_and_provider_are_reviewed():
    ready = audit.preflight()
    assert ready["branch"] == "develop"
    assert ready["provider_blob"] == audit.r16.REVIEWED_PROVIDER_BLOB
    assert len(ready["r16_sha256"]) == 64


def test_source_comparison_detects_differences_without_normalizing_ids():
    result = audit.source_comparison(("a", "b"), ("b", "a"))
    assert result["same_ordered_ids"] is False
    assert result["same_id_set"] is True
    assert result["screened_only"] == []
    assert result["public_only"] == []
    changed = audit.source_comparison(("a", "b"), ("a", "c"))
    assert changed["screened_only"] == ["b"]
    assert changed["public_only"] == ["c"]


def test_map_disagreement_takes_priority():
    screened = _states("proved")
    public = _states("proved")
    public["hopf_7"] = "unresolved"
    assert audit.classify({"screened": screened, "public": public}, "partial") == "PUBLIC_CONTEXT_MAP_DISAGREEMENT"


def test_deeper_dependency_failures_have_separate_classes():
    base = _states("proved")
    for goal, expected in (
        ("short_exact", "SHORT_EXACT_COMPOSITION_MISSING"),
        ("cardinality", "CARDINALITY_COMPOSITION_MISSING"),
        ("element_order", "ELEMENT_ORDER_COMPOSITION_MISSING"),
        ("cyclic_structure", "CYCLIC_STRUCTURE_COMPOSITION_MISSING"),
    ):
        public = dict(base)
        public[goal] = "unresolved"
        assert audit.classify({"screened": base, "public": public}, "partial") == expected


def test_proved_subgoals_do_not_claim_group_completion():
    complete_individually = _states("proved")
    pair = {"screened": complete_individually, "public": complete_individually}
    assert audit.classify(pair, "partial") == "ROOT_PATH_DEPENDENT_DESPITE_INDEPENDENT_SUBGOALS"
    assert audit.classify(pair, "complete") == "PUBLIC_ROOT_COMPLETE_NEEDS_TRUST_BOUNDARY_REVIEW"
