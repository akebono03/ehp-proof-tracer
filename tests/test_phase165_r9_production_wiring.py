"""Focused R9 checks: real automatic wiring with no citation promotion."""
from dataclasses import dataclass

import pytest

import phase165_goal_only_search as entry
import phase165_r9_production_wiring as wiring
from homotopy_groups import TodaPrimaryGroup
from phase165_r3_recursive_search import RegisteredGoalUnresolved
from phase165_r8_rule_provider import build_production_rule_provider


def test_production_inputs_contain_live_registry_and_rules():
    inputs = wiring.discover_goal_search_inputs()
    assert inputs.bridge.registry._assertions
    assert callable(inputs.expansion_provider)
    assert inputs.rule_report.rule_names
    assert inputs.verified_assertion_ids == ()
    assert inputs.bridge.proof_links == ()


def test_real_rule_provider_is_constructed():
    provider, report = build_production_rule_provider()
    assert callable(provider)
    assert len(report.rule_names) > 0


def test_goal_entry_auto_discovers_inputs_before_failing_closed(monkeypatch):
    called = []
    real = wiring.discover_goal_search_inputs
    def record():
        called.append(True)
        return real()
    monkeypatch.setattr(wiring, "discover_goal_search_inputs", record)
    with pytest.raises(entry.GoalSearchIncompleteError, match="legacy proof selection is disabled"):
        entry.construct_registered_group_proof(n=3, k=2)
    assert called == [True]


def test_goal_entry_passes_real_provider_to_r3(monkeypatch):
    @dataclass(frozen=True)
    class Equation:
        lhs: object
    goal = Equation(TodaPrimaryGroup(group_dimension=5, sphere_dimension=3))
    observed = []
    def fake_reconstruct(target, bridge, citing_assertion_id, provider, *, verified_assertion_ids):
        observed.append((target, bridge, citing_assertion_id, provider, verified_assertion_ids))
        return type("Step", (), {"conclusion": target})()
    monkeypatch.setattr(entry, "reconstruct_registered_goal", fake_reconstruct)
    step = entry.construct_registered_group_proof(
        n=3, k=2, goal=goal, citing_assertion_id="a-review-context"
    )
    assert step.conclusion is goal
    assert len(observed) == 1
    assert callable(observed[0][3])
    assert observed[0][4] == ()


def test_unverified_goal_does_not_gain_free_proof():
    inputs = wiring.discover_goal_search_inputs()
    from phase165_r3_recursive_search import reconstruct_registered_goal
    assertion_id = next(iter(inputs.bridge.registry._assertions))
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal(
            object(), inputs.bridge, assertion_id, inputs.expansion_provider,
            verified_assertion_ids=inputs.verified_assertion_ids,
        )
