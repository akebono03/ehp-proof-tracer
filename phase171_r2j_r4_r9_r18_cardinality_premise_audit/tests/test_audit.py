"""Focused read-only cardinality-premise and rule-matcher tests."""
from __future__ import annotations

import pytest

from phase171_r2j_r4_r9_r18_cardinality_premise_audit import audit


def test_preflight_requires_r17_and_reviewed_provider():
    ready = audit.preflight()
    assert ready["branch"] == "develop"
    assert ready["provider_blob"] == audit.REVIEWED_BLOB
    assert len(ready["r17_sha256"]) == 64


def test_rejects_mutating_git():
    with pytest.raises(ValueError):
        audit.r17.git_read("reset", "--hard")
    with pytest.raises(ValueError):
        audit.r16.git_read("checkout", "--", audit.SOURCE_MODULE)


def test_classification_identifies_specific_missing_premise():
    for name in audit.PARTS:
        statuses = {part: "proved" for part in audit.PARTS}
        statuses[name] = "unresolved"
        assert audit.classify(statuses, None, "unresolved") == "CARDINALITY_PREMISE_NOT_INDEPENDENTLY_PROVED"


def test_classification_preserves_inference_and_search_distinction():
    complete = {name: "proved" for name in audit.PARTS}
    assert audit.classify(complete, 0, "unresolved") == "CARDINALITY_MATCHER_REJECTS_PROVED_PREMISES"
    assert audit.classify(complete, 2, "unresolved") == "CARDINALITY_MATCH_AMBIGUOUS_OR_UNOBSERVED"
    assert audit.classify(complete, 1, "unresolved") == "CARDINALITY_VALID_PREMISES_BUT_RECURSIVE_PATH_UNRESOLVED"
    assert audit.classify(complete, 1, "proved") == "CARDINALITY_INDEPENDENTLY_PROVED"


def test_public_cardinality_has_one_checked_source_backed_route():
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
    bridge, root, _ = _screened_context()
    provider = shared_expansion_provider(bridge, proof_target=root)
    goal = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    option = audit.cardinality_route(provider, goal)
    assert option.rule.name == audit.ROUTE_NAME
    assert len(option.subgoals) == 3


def test_reject_wrong_cardinality_goal():
    from homotopy_groups import TodaPrimaryGroup
    from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
    with pytest.raises(ValueError):
        audit.cardinality_route(lambda goal: (), FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 8))


def test_read_only_live_audit_does_not_promote_independent_proof_to_root():
    result = audit.inspect()
    assert result["source_changes"] == 0
    assert result["new_given"] == 0
    assert result["completed_proof_imported"] is False
    assert result["public_root_status"] == "partial"
    assert result["source_comparison"]["same_id_set"] is False
    assert result["classification"] in (
        "CARDINALITY_PREMISE_NOT_INDEPENDENTLY_PROVED",
        "CARDINALITY_MATCHER_REJECTS_PROVED_PREMISES",
        "CARDINALITY_MATCH_AMBIGUOUS_OR_UNOBSERVED",
        "CARDINALITY_VALID_PREMISES_BUT_RECURSIVE_PATH_UNRESOLVED",
        "CARDINALITY_INDEPENDENTLY_PROVED",
    )
