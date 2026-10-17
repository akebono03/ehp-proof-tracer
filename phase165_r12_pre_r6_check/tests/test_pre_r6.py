"""Focused checks; no target proof or synthetic GIVEN assumptions."""
from phase165_r12_pre_r6_check.audit import R2_ID, R5_ID, audit, missing_premise_variables
from phase165_r10_rule_registry import build_rule_registry
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r8_rule_provider import DEFAULT_RULE_MODULES
from homotopy_groups import TodaPrimaryGroup
from expression import eta


def test_both_rules_auto_registered():
    registry = build_rule_registry(DEFAULT_RULE_MODULES)
    assert registry.by_id(R2_ID).rule is not None
    assert registry.by_id(R5_ID).rule is not None


def test_r2_requires_unbound_map_domain_and_generator():
    registry = build_rule_registry(DEFAULT_RULE_MODULES)
    rule = registry.by_id(R2_ID).rule
    goal = CyclicStructureStatement(TodaPrimaryGroup(4, 3), eta(3), 2)
    assert missing_premise_variables(rule, goal) == ["domain", "map", "source_generator"]


def test_root_bridge_does_not_certify_proof():
    result = audit()
    assert result["r5_registered"]
    assert result["r5_root_subgoal"].startswith("CyclicStructureStatement(")
    assert result["pi43_proof_certified"] is False
    assert result["typed_source_witness_availability"] == "NOT_EVALUATED_BY_THIS_AUDIT"


def test_r5_no_identical_pattern_duplicate():
    result = audit()
    assert result["r5_exact_pattern_duplicates"] == []
