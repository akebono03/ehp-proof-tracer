"""Nonmutating R13 wrapper and canonical-stack regression tests."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase171_r2j_r4_r9_r13_root_cycle_audit.audit import (
    ProviderFactoryObserver,
    classify_trace,
    goal_role,
    resolution_stack_snapshot,
    same_statement,
)
from phase171_r2j_r4_r9_r12_public_symmetry_diagnostic.audit import (
    git_read,
    preflight,
)
from proof import Relation, RelationType
from phase165_r3_recursive_search import GoalExpansion
from relation_rules import equality_symmetry_inference_rule


def _goals():
    root = Relation("G", "C4", RelationType.EQUALITY)
    forward = Relation("a", "b", RelationType.EQUALITY)
    reverse = Relation("b", "a", RelationType.EQUALITY)
    return root, forward, reverse


def _fake_frame(name, module, locals_dict, back=None):
    return SimpleNamespace(
        f_code=SimpleNamespace(co_name=name),
        f_globals={"__name__": module},
        f_locals=locals_dict,
        f_back=back,
    )


def test_stack_snapshot_reports_active_forward_cycle_without_mutating_state():
    root, forward, reverse = _goals()
    active = [root, forward, reverse]
    solved = [(Relation("x", "x", RelationType.EQUALITY), object())]
    real = _fake_frame(
        "resolve", "phase165_r3_recursive_search", {"active": active, "solved": solved},
    )
    wrapper = _fake_frame("observed", "phase171_r2j_r4_r9_r13_root_cycle_audit.audit", {}, real)
    before = tuple(active)
    result = resolution_stack_snapshot(wrapper, root, forward, reverse)
    assert result["resolver_found"] is True
    assert result["active_roles"] == ["root", "forward", "reverse"]
    assert result["forward_active"] is True
    assert result["reverse_active"] is True
    assert result["forward_solved"] is False
    assert tuple(active) == before
    assert len(solved) == 1


def test_stack_snapshot_does_not_trust_noncanonical_resolver():
    root, forward, reverse = _goals()
    impostor = _fake_frame("resolve", "unrelated_module", {"active": [root, forward, reverse]})
    result = resolution_stack_snapshot(impostor, root, forward, reverse)
    assert result["resolver_found"] is False
    assert result["active_roles"] == []
    assert result["forward_active"] is False


def test_root_provider_observer_preserves_identity_order_and_subgoals():
    root, forward, reverse = _goals()
    candidate = GoalExpansion(equality_symmetry_inference_rule(), (forward,))
    calls = []

    def factory(*args, **kwargs):
        calls.append(kwargs.get("proof_target"))

        def provider(goal):
            return (candidate,)

        return provider

    watcher = ProviderFactoryObserver(factory, root, forward, reverse)
    observed = watcher(proof_target=root)
    result = observed(reverse)
    assert result is not None and result[0] is candidate
    assert calls == [root]
    assert watcher.root_provider_instances == 1
    assert watcher.focus_calls["reverse"] == 1
    assert watcher.events[0]["symmetry_exact"] == 1
    assert watcher.events[0]["routes_total"] == 1
    assert watcher.events[0]["stack"]["resolver_found"] is False
    unobserved = watcher(proof_target=forward)
    assert unobserved(reverse) == (candidate,)
    assert watcher.root_provider_instances == 1


def test_classification_distinguishes_cycle_missing_and_ambiguous():
    stack = {"forward_active": True}
    cycle = {"role": "reverse", "stack": stack, "symmetry_exact": 1, "routes_total": 1}
    assert classify_trace("partial", [cycle]) == "REVERSE_SYMMETRY_CYCLE_WITH_ACTIVE_FORWARD"
    assert classify_trace("partial", []) == "REVERSE_NOT_VISITED_IN_PUBLIC_ROOT"
    missing = {"role": "reverse", "stack": stack, "symmetry_exact": 0, "routes_total": 1}
    assert classify_trace("partial", [missing]) == "REVERSE_ROUTE_MISSING_IN_ROOT_CONTEXT"
    ambiguous = {"role": "reverse", "stack": stack, "symmetry_exact": 1, "routes_total": 2}
    assert classify_trace("partial", [ambiguous]) == "MULTIPLE_REVERSE_ROUTES_REQUIRE_AMBIGUITY_AUDIT"
    assert classify_trace("complete", [cycle]) == "ROOT_COMPLETE_REQUIRES_TRUST_BOUNDARY"


def test_statement_roles_match_by_typed_value_not_text():
    root, forward, reverse = _goals()
    assert same_statement(root, root)
    assert not same_statement(root, "G")
    assert goal_role(root, root, forward, reverse) == "root"
    assert goal_role(forward, root, forward, reverse) == "forward"
    assert goal_role(reverse, root, forward, reverse) == "reverse"
    assert goal_role(object(), root, forward, reverse) is None


def test_reviewed_baseline_and_read_only_guard():
    assert preflight()["shared_provider_blob"] == "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac"
    with pytest.raises(ValueError, match="read-only"):
        git_read("reset", "--hard")
