from dataclasses import dataclass
from types import ModuleType
import sys

import pytest

from phase165_r10_rule_registry import build_rule_registry
from phase165_r8_rule_provider import discover_inference_rules


def test_r10_public_discovery_equals_registry():
    registry = build_rule_registry(("ehp_rules", "relation_rules"))
    rules, report = discover_inference_rules(("ehp_rules", "relation_rules"))
    assert tuple(rule.name for rule in rules) == tuple(e.rule.name for e in registry.entries)
    assert len({e.rule_id for e in registry.entries}) == len(registry.entries)
    assert all(e.rule_id == e.factory_module + "." + e.factory_name for e in registry.entries)
    assert report.skipped_factories == registry.skipped_factories


def test_r10_duplicate_rule_id_rejected(monkeypatch):
    module = ModuleType("r10_duplicate_rules")
    exec("from proof import InferenceRule\ndef sample_inference_rule():\n    return InferenceRule('sample')\n", module.__dict__)
    monkeypatch.setitem(sys.modules, module.__name__, module)
    with pytest.raises(ValueError, match="duplicate rule ID"):
        build_rule_registry((module.__name__, module.__name__))


def test_r10_factories_with_required_inputs_not_executed(monkeypatch):
    module = ModuleType("r10_required_rules")
    exec("from proof import InferenceRule\ndef safe_inference_rule():\n    return InferenceRule('safe')\ndef witness_inference_rule(step):\n    raise AssertionError('must not execute')\n", module.__dict__)
    monkeypatch.setitem(sys.modules, module.__name__, module)
    registry = build_rule_registry((module.__name__,))
    assert len(registry.entries) == 1
    assert registry.entries[0].rule_id == "r10_required_rules.safe_inference_rule"
    assert registry.skipped_factories == ("r10_required_rules.witness_inference_rule:requires-input",)
