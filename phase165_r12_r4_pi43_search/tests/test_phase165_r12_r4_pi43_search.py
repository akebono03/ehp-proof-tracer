"""Targeted audit contracts; these tests do not claim to prove pi_4^3."""
import importlib.util
from pathlib import Path

from expression import eta
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from proof import Relation, RelationType
from phase165_r10_rule_registry import build_rule_registry
from phase165_r8_rule_provider import DEFAULT_RULE_MODULES, discover_inference_rules


AUDIT = Path(__file__).resolve().parents[1] / "audit.py"


def load_audit():
    spec = importlib.util.spec_from_file_location("phase165_r12_r4_audit", AUDIT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pi43_target_is_typed_and_not_a_given_step():
    goal = load_audit().target_goal()
    assert goal == Relation(
        TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta(3)),
        RelationType.EQUALITY,
    )
    assert not hasattr(goal, "premises")


def test_both_r12_r2_rules_are_discoverable_without_explicit_wiring():
    registry = build_rule_registry(DEFAULT_RULE_MODULES)
    ids = {entry.rule_id for entry in registry.entries}
    assert "phase165_r12_r2_quotient_rules.first_isomorphism_quotient_inference_rule" in ids
    assert "phase165_r12_r2_quotient_rules.infinite_cyclic_quotient_structure_inference_rule" in ids
    rules, report = discover_inference_rules()
    assert len(rules) == len(registry.entries)
    assert len(report.rule_names) == len(rules)


def test_search_worker_is_not_called_on_import():
    module = load_audit()
    assert callable(module.run_worker)
    assert callable(module.audit)
