from dataclasses import dataclass

from phase165_r8_rule_provider import (
    create_rule_expansion_provider,
    discover_inference_rules,
)
from proof import InferenceRule, PatternVariable, PremisePattern


@dataclass(frozen=True)
class Claim:
    value: object


def test_inverse_concrete_premise():
    x = PatternVariable("x")
    rule = InferenceRule("test", premise_patterns=(PremisePattern(statement_pattern=Claim(x)),), conclusion_pattern=Claim(x))
    result = create_rule_expansion_provider((rule,))(Claim(4))
    assert len(result) == 1
    assert result[0].subgoals == (Claim(4),)
    assert result[0].rule is rule


def test_unbound_premise_is_refused():
    x = PatternVariable("x")
    y = PatternVariable("y")
    rule = InferenceRule("unbound", premise_patterns=(PremisePattern(statement_pattern=Claim(y)),), conclusion_pattern=Claim(x))
    assert create_rule_expansion_provider((rule,))(Claim(4)) == ()


def test_rule_without_invertible_conclusion_is_refused():
    rule = InferenceRule("opaque", premise_patterns=(PremisePattern(statement_pattern=Claim(1)),))
    assert create_rule_expansion_provider((rule,))(Claim(1)) == ()


def test_non_rule_catalog_rejected():
    import pytest
    with pytest.raises(TypeError):
        create_rule_expansion_provider((object(),))


def test_factory_discovery_does_not_create_premises(tmp_path, monkeypatch):
    import sys
    from types import ModuleType
    mod = ModuleType("r8_test_rules")
    exec("from proof import InferenceRule\n"
         "def safe_inference_rule():\n"
         "    return InferenceRule('safe')\n"
         "def needs_witness_inference_rule(step):\n"
         "    raise AssertionError('should not run')\n", mod.__dict__)
    monkeypatch.setitem(sys.modules, "r8_test_rules", mod)
    rules, report = discover_inference_rules(("r8_test_rules",))
    assert len(rules) == 1
    assert "requires-input" in report.skipped_factories[0]
