"""Focused fail-closed checks for the R9-R3 read-only Hopf frontier audit."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapSurjective
from phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic.audit import (
    _failure_class,
    _git,
    _hopf_goal,
    _proof_event,
    _unique_hopf_node,
    inspect_first_hopf_frontier,
)
from proof import InferenceRule, ProofRule, ProofStep


def _fixture():
    given = ProofStep("source", (), ProofRule.GIVEN)
    goal = _hopf_goal()
    inferred = ProofStep(
        goal, (given,), ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="synthetic h"),
    )
    return given, inferred


def test_hopf_goal_has_exact_ehp_map_types():
    goal = _hopf_goal()
    assert goal == MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))


def test_original_hopf_node_requires_genuine_inference():
    _, root = _fixture()
    assert _unique_hopf_node(root, _hopf_goal()) is root
    with pytest.raises(RuntimeError):
        _unique_hopf_node(replace(root, rule=ProofRule.GIVEN, premises=()), _hopf_goal())


def test_wrong_hopf_dimension_rejected():
    _, root = _fixture()
    wrong = MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 4), TodaPrimaryGroup(7, 7),
    ))
    with pytest.raises(RuntimeError):
        _unique_hopf_node(root, wrong)


def test_proof_event_preserves_actual_rule_kind():
    given, root = _fixture()
    result = _proof_event("proved", root.conclusion, root)
    assert result["proof_rule"] == "inference"
    assert result["inference_rule"] == "synthetic h"
    leaf = _proof_event("proved", given.conclusion, given)
    assert leaf["proof_rule"] == "given"
    assert _proof_event("unresolved", root.conclusion, None)["proof_rule"] is None


def test_proof_event_rejects_forged_observation():
    with pytest.raises(ValueError):
        _proof_event("proved", "goal", None)
    with pytest.raises(TypeError):
        _proof_event("unresolved", "goal", object())
    with pytest.raises(ValueError):
        _proof_event("verified", "goal", None)


def test_failure_class_distinguishes_premises_and_matcher():
    assert _failure_class(True, []) == "HOPF_REPLAYED"
    assert _failure_class(False, []) == "HOPF_PREMISES_NOT_ALL_RECONSTRUCTED"
    assert _failure_class(False, [{"matches": 0}]) == "HOPF_MATCHER_REJECTED_RECONSTRUCTED_PREMISES"
    assert _failure_class(False, [{"matches": 1}]) == "HOPF_MATCHED_BUT_ROOT_NOT_ADMITTED"


def test_readonly_git_commands_only():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_live_diagnostic_preserves_trust_boundary():
    report = inspect_first_hopf_frontier()
    assert report["original_inference_rule_count"] >= 2
    assert report["hopf_scoped_routes"] == 1
    assert report["new_given_added"] == 0
    assert report["production_modified"] is False
    assert report["public_web_verified"] is False
    assert report["hopf_failure_class"] in (
        "HOPF_REPLAYED",
        "HOPF_PREMISES_NOT_ALL_RECONSTRUCTED",
        "HOPF_MATCHER_REJECTED_RECONSTRUCTED_PREMISES",
        "HOPF_MATCHED_BUT_ROOT_NOT_ADMITTED",
    )
