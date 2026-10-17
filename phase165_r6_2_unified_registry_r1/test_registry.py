from __future__ import annotations
from pathlib import Path
import sys
from types import ModuleType
import pytest
from proof import InferenceRule
from phase165_r6_2_unified_registry_r1.unified_backward_rule_registry import (
    UnifiedBackwardRuleRegistry, build_unified_backward_rule_registry,
)
from phase165_r6_2_unified_registry_r1.install import transform


def test_register_and_duplicate_rejected():
    registry = UnifiedBackwardRuleRegistry()
    rule = InferenceRule("example")
    registry.register("a.example_inference_rule", rule, origin="TEST")
    assert registry.rules() == (rule,)
    with pytest.raises(ValueError, match="duplicate"):
        registry.register("a.example_inference_rule", rule, origin="TEST")


def test_invalid_rule_rejected():
    registry = UnifiedBackwardRuleRegistry()
    with pytest.raises(TypeError):
        registry.register("a.rule", object(), origin="TEST")


def test_discovery_skips_required_input(monkeypatch):
    module = ModuleType("unified_test_rules")
    exec("from proof import InferenceRule\n"
         "def usable_inference_rule():\n    return InferenceRule('usable')\n"
         "def requires_witness_inference_rule(witness):\n    raise AssertionError('must not call')\n", module.__dict__)
    monkeypatch.setitem(sys.modules, module.__name__, module)
    registry, report = build_unified_backward_rule_registry(module_names=(module.__name__,))
    assert report["registered"] == 1
    assert registry.entries()[0].rule_id == "unified_test_rules.usable_inference_rule"
    assert report["skipped"] == ["unified_test_rules.requires_witness_inference_rule:requires-input"]


def test_explicit_registration():
    rule = InferenceRule("extra")
    registry, report = build_unified_backward_rule_registry(module_names=(), extra_rules=(("trusted.extra", rule),))
    assert registry.entries()[0].origin == "EXPLICIT_REGISTERED"
    assert report["registered"] == 1


def test_transform_replaces_three_independent_discoveries():
    source = '''from phase165_r3_recursive_search import GoalExpansion

def shared_expansion_provider():
    from phase165_r8_rule_provider import discover_inference_rules as _discover_seeded_rules
    from phase165_r8_rule_provider import discover_inference_rules
    generic_provider = build_generic_backward_expansion_provider()
    seeded_rules, _seeded_report = _discover_seeded_rules()
    witness_rules, _witness_report = discover_inference_rules()
'''
    result = transform(source)
    assert "unified_rules = unified_registry.rules()" in result
    assert "build_generic_backward_expansion_provider(unified_rules)" in result
    assert result.count("= unified_rules") == 2
    assert transform(result) == result


def test_transform_rejects_old_adapter():
    source = "from phase165_r3_recursive_search import GoalExpansion\nfrom phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules\n"
    with pytest.raises(ValueError, match="adapter"):
        transform(source)
