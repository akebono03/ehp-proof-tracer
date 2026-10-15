"""R57-R24 focused candidate-discovery tests; no full search invoked."""
from __future__ import annotations

from dataclasses import dataclass
from sys import modules
from types import ModuleType

import pytest

from phase165_r57_r24_candidate_discovery import (
    discover_catalog_goal_candidates,
    discover_explicit_goal_candidates,
    discover_factory_goal_candidates,
)
from proof import InferenceRule, PatternVariable
from rule_catalog import InferenceRuleCatalog, InferenceRuleCatalogEntry


@dataclass(frozen=True)
class TypedGoal:
    group: object
    map: object
    generator: object


def _rule(name: str = "generic") -> InferenceRule:
    return InferenceRule(
        name=name,
        conclusion_pattern=TypedGoal(
            PatternVariable("group"),
            PatternVariable("map"),
            PatternVariable("generator"),
        ),
    )


def _goal() -> TypedGoal:
    return TypedGoal("pi_4^3", "E", "eta_3")


def test_r24_catalog_discovers_typed_group_map_and_generator():
    catalog = InferenceRuleCatalog()
    rule = _rule()
    catalog.register(InferenceRuleCatalogEntry("r24.generic", rule, TypedGoal, fixed_point_safe=True))
    candidate, = discover_catalog_goal_candidates(catalog, _goal())
    assert candidate.key == "r24.generic"
    assert candidate.source == "catalog"
    assert candidate.unification.rule is rule
    assert tuple(binding.value for binding in candidate.unification.bindings) == (
        "pi_4^3", "E", "eta_3"
    )


def test_r24_catalog_excludes_unsafe_and_wrong_type():
    catalog = InferenceRuleCatalog()
    catalog.register(InferenceRuleCatalogEntry("unsafe", _rule(), TypedGoal))
    assert discover_catalog_goal_candidates(catalog, _goal()) == ()
    assert discover_catalog_goal_candidates(catalog, ("pi_4^3", "E", "eta_3")) == ()


def test_r24_catalog_preserves_compatibility_gate():
    catalog = InferenceRuleCatalog()
    catalog.register(InferenceRuleCatalogEntry(
        "blocked", _rule(), TypedGoal, fixed_point_safe=True,
        goal_compatibility=lambda goal: goal.map == "H",
    ))
    assert discover_catalog_goal_candidates(catalog, _goal()) == ()


def test_r24_catalog_rejects_wrong_conclusion_not_just_type():
    catalog = InferenceRuleCatalog()
    catalog.register(InferenceRuleCatalogEntry(
        "wrong_map", InferenceRule("fixed", conclusion_pattern=TypedGoal("pi_4^3", "H", "eta_3")),
        TypedGoal, fixed_point_safe=True,
    ))
    assert discover_catalog_goal_candidates(catalog, _goal()) == ()


def test_r24_explicit_never_inverts_opaque_builder():
    opaque = InferenceRule("opaque", conclusion_builder=lambda premises: _goal())
    assert discover_explicit_goal_candidates((opaque,), _goal()) == ()


def test_r24_explicit_deduplicates_rule_identity_not_name():
    first = _rule("same")
    second = _rule("same")
    result = discover_explicit_goal_candidates((first, first, second), _goal())
    assert len(result) == 2
    assert result[0].unification.rule is first
    assert result[1].unification.rule is second


def test_r24_unbound_goal_is_candidate_not_proof():
    candidate, = discover_explicit_goal_candidates((_rule(),), _goal())
    assert candidate.unification.goal == _goal()
    assert not hasattr(candidate, "proof_step")
    assert not hasattr(candidate, "subgoals")


def test_r24_factory_reuses_existing_r8_inventory(monkeypatch):
    module = ModuleType("r24_fixture_module")
    exec(
        "from proof import InferenceRule, PatternVariable\n"
        "from test_phase165_r57_r24_candidate_discovery import TypedGoal\n"
        "def generic_inference_rule():\n"
        "    return InferenceRule('factory', conclusion_pattern=TypedGoal(PatternVariable('g'), 'E', 'eta_3'))\n"
        "def requires_witness_inference_rule(witness):\n"
        "    raise AssertionError('never invoke')\n",
        module.__dict__,
    )
    monkeypatch.setitem(modules, "r24_fixture_module", module)
    candidates, report = discover_factory_goal_candidates(_goal(), ("r24_fixture_module",))
    assert len(candidates) == 1
    assert candidates[0].source == "factory"
    assert candidates[0].unification.bindings[0].value == "pi_4^3"
    assert any("requires-input" in item for item in report.skipped_factories)


def test_r24_rejects_invalid_inputs():
    with pytest.raises(TypeError):
        discover_catalog_goal_candidates(object(), _goal())
    with pytest.raises(TypeError):
        discover_explicit_goal_candidates((_rule(), object()), _goal())
    with pytest.raises(TypeError):
        discover_factory_goal_candidates(_goal(), ["module"])
