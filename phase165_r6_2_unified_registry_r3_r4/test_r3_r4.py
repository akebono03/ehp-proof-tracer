from __future__ import annotations

import ast
import pytest

from phase165_r6_2_unified_registry_r3_r4.context_provider_registry import build_context_expansion_provider_registry
from phase165_r6_2_unified_registry_r3_r4.install import OLD, NEW, transform


def _registry(available=("fixed",), prior=("prior",)):
    calls = []
    def stub(label):
        def expand(goal, statements):
            calls.append((label, goal, statements))
            return ()
        return expand
    registry = build_context_expansion_provider_registry(
        available=available, prior_conclusions=prior,
        expand_registered_toda45_finite_cyclic_goal=stub("stable"),
        expand_registered_eta_specialization=stub("eta"),
        expand_registered_delta_image_goal=stub("delta"),
        expand_cited_general_specialization=stub("general"),
    )
    return registry, calls


def test_all_four_providers_registered_in_order():
    registry, calls = _registry()
    assert len(registry.entries()) == 4
    assert [entry.origin for entry in registry.entries()] == ["SHARED_CITED_CONTEXT"] * 4
    for provider in registry.providers():
        assert provider("goal") == ()
    assert [call[0] for call in calls] == ["stable", "eta", "delta", "general"]


def test_citation_context_and_prior_order_preserved():
    registry, calls = _registry(("given-1", "given-2"), ("prior-1",))
    for provider in registry.providers():
        provider("G")
    assert calls[0][2] == ("given-1", "given-2", "prior-1")
    assert all(call[2] == ("given-1", "given-2") for call in calls[1:])


def test_no_cross_goal_state_leak():
    registry, calls = _registry()
    for provider in registry.providers():
        provider("A")
        provider("B")
    assert [c[1] for c in calls] == ["A", "B"] * 4


def test_non_tuple_context_rejected():
    with pytest.raises(TypeError):
        _registry(available=["bad"])


def test_invalid_provider_rejected():
    with pytest.raises(TypeError):
        build_context_expansion_provider_registry(
            available=(), prior_conclusions=(),
            expand_registered_toda45_finite_cyclic_goal=None,
            expand_registered_eta_specialization=lambda g, a: (),
            expand_registered_delta_image_goal=lambda g, a: (),
            expand_cited_general_specialization=lambda g, a: (),
        )


def _base_source():
    return ('from phase165_r3_recursive_search import GoalExpansion\n'
            'unified_rules = unified_registry.rules()\n'
            'shared_provider_registry.providers()\n'
            'def wrapper():\n'
            '    def expand(goal: object) -> tuple[GoalExpansion, ...]:\n'
            '        options = []\n' + OLD + '\n'
            '        return options\n')


def test_transform_replaces_exactly_four_calls():
    src = _base_source()
    output = transform(src)
    ast.parse(output)
    assert NEW in output and OLD not in output
    assert "build_context_expansion_provider_registry(" in output
    assert transform(output) == output


def test_transform_rejects_legacy_adapter():
    with pytest.raises(ValueError, match="dedicated"):
        transform(_base_source() + "\nexpand_existing_pi43_rules\n")


def test_transform_rejects_missing_r3_3():
    with pytest.raises(ValueError, match="R3-3"):
        transform(_base_source().replace("shared_provider_registry.providers()", "None"))
