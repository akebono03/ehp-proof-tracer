from __future__ import annotations

from pathlib import Path

import pytest

from phase165_r6_2_unified_registry_r3_r3.install import transform
from phase165_r6_2_unified_registry_r3_r3.provider_registry import (
    UnifiedExpansionProviderRegistry,
    build_shared_expansion_provider_registry,
)


def _provider(value):
    return (value,)


def test_register_order_and_identity():
    registry = UnifiedExpansionProviderRegistry()
    registry.register("test.a", _provider, origin="TEST")
    assert registry.providers() == (_provider,)
    assert registry.entries()[0].provider_id == "test.a"


def test_duplicate_provider_id_is_blocked():
    registry = UnifiedExpansionProviderRegistry()
    registry.register("test.a", _provider, origin="TEST")
    with pytest.raises(ValueError):
        registry.register("test.a", _provider, origin="TEST")


def test_noncallable_provider_blocked():
    with pytest.raises(TypeError):
        UnifiedExpansionProviderRegistry().register("test.a", object(), origin="TEST")


def test_fixed_and_extra_preserve_order():
    functions = [lambda value, i=i: (i, value) for i in range(5)]
    registry = build_shared_expansion_provider_registry(
        expand_generic_iso_goal=functions[0],
        expand_generic_ehp_hopf_goal=functions[1],
        expand_delta_zero_from_suspension_iso=functions[2],
        expand_diagonal_suspension=functions[3],
        extra_providers=(functions[4],),
    )
    assert registry.providers() == tuple(functions)
    assert registry.entries()[4].origin == "CALLER_EXPLICIT"


def test_installer_rejects_pi43_adapter():
    with pytest.raises(ValueError, match="adapter"):
        transform('from phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules')


def test_installer_rejects_missing_r1():
    with pytest.raises(ValueError, match="R1"):
        transform('from phase165_r3_recursive_search import GoalExpansion')


def test_installer_changes_only_known_loop():
    source = """from phase165_r3_recursive_search import GoalExpansion
unified_rules = unified_registry.rules()
def shared_expansion_provider():
    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        for provider in (
            expand_generic_iso_goal,
            expand_generic_ehp_hopf_goal,
            expand_delta_zero_from_suspension_iso,
            expand_diagonal_suspension,
            *extra_providers,
        ):
            pass
        return ()
    return expand
"""
    updated = transform(source)
    assert "shared_provider_registry.providers()" in updated
    assert transform(updated) == updated
    assert "expand_existing_pi43_rules" not in updated
