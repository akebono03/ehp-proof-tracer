"""R12-R3: shared registry -> backward search -> checked ProofStep integration.

Synthetic group-map names are deliberate: these tests do not certify Toda data.
"""
import pytest

from expression import MapSymbol
from map_property_rules import (
    ImageWholeStatement,
    IsomorphismStatement,
    KernelZeroStatement,
    InjectiveMapStatement,
    SurjectiveMapStatement,
)
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from phase165_r8_rule_provider import build_production_rule_provider, discover_inference_rules
from phase165_r10_rule_registry import build_rule_registry
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)


def _fixed_bridge(statements):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry("test:fixed", ReferenceKind.PROPOSITION, "Synthetic fixture"))
    registry.add_reference(LiteratureEntry("test:goal", ReferenceKind.PROPOSITION, "Synthetic target"))
    links = []
    for index, statement in enumerate(statements):
        assertion_id = f"test:fixed:{index}"
        registry.add_assertion(AssertionEntry(
            assertion_id, "test:fixed", AssertionKind.STATEMENT, statement,
        ))
        links.append(ProofStepLink(assertion_id, step=ProofStep(
            conclusion=statement, premises=(), rule=ProofRule.GIVEN,
        )))
    registry.add_assertion(AssertionEntry(
        "test:goal:assertion", "test:goal", AssertionKind.STATEMENT, "search request only",
    ))
    return RegistryBridgeResult(registry, (), tuple(links))


def test_r12_r3_shared_rules_chain_without_group_adapter():
    group_map = MapSymbol(name="synthetic_f")
    bridge = _fixed_bridge((KernelZeroStatement(group_map), ImageWholeStatement(group_map)))
    provider, report = build_production_rule_provider()
    result = reconstruct_registered_goal(
        IsomorphismStatement(group_map), bridge, "test:goal:assertion",
        provider, lookup_mode="typed_reference",
    )
    assert report.rule_names
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == IsomorphismStatement(group_map)
    assert len(result.premises) == 2
    assert {type(step.conclusion) for step in result.premises} == {
        InjectiveMapStatement, SurjectiveMapStatement,
    }
    for step in result.premises:
        assert step.rule is ProofRule.INFERENCE
        assert len(step.premises) == 1
        assert step.premises[0].rule is ProofRule.GIVEN


def test_r12_r3_missing_premise_does_not_become_given():
    group_map = MapSymbol(name="synthetic_missing")
    bridge = _fixed_bridge((KernelZeroStatement(group_map),))
    provider, _ = build_production_rule_provider()
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal(
            IsomorphismStatement(group_map), bridge, "test:goal:assertion",
            provider, lookup_mode="typed_reference",
        )


def test_r12_r3_r12_r2_factories_are_auto_discovered():
    import phase165_r12_r2_quotient_rules as added
    factory_names = tuple(
        name for name, value in vars(added).items()
        if name.endswith("_inference_rule") and callable(value)
        and getattr(value, "__module__", None) == added.__name__
    )
    assert len(factory_names) == 2, factory_names
    from phase165_r8_rule_provider import DEFAULT_RULE_MODULES
    assert "phase165_r12_r2_quotient_rules" in DEFAULT_RULE_MODULES
    registry = build_rule_registry(DEFAULT_RULE_MODULES)
    registered = {entry.rule_id for entry in registry.entries}
    assert {f"phase165_r12_r2_quotient_rules.{name}" for name in factory_names} <= registered
    rules, report = discover_inference_rules()
    assert len(rules) == len(registry.entries)
    assert len(report.rule_names) == len(rules)
