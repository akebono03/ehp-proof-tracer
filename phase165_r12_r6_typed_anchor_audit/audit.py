"""Audit R12-R2 inverse binding against actual fixed typed source witnesses.

Read-only: never constructs a GIVEN, source assertion, or a group-specific adapter.
"""
from __future__ import annotations

import json
from collections import Counter

from expression import eta
from homotopy_groups import TodaPrimaryGroup
from phase165_r10_rule_registry import build_rule_registry
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r6_2_r4_seeded_goals import generate_seeded_backward_goals
from phase165_r8_rule_provider import DEFAULT_RULE_MODULES, _pattern_variable_names
from phase165_r57_r23_conclusion_unification import unify_inference_conclusion
from proof import ProofRule
from unified_statement_registry import AssertionOrigin

RULE_ID = "phase165_r12_r2_quotient_rules.infinite_cyclic_quotient_structure_inference_rule"
PREMISE_TYPES = (
    "HomomorphismPresentationStatement",
    "KernelMultipleStatement",
    "QuotientIsomorphismStatement",
    "CyclicStructureStatement",
    "SurjectiveMapStatement",
)


def fixed_typed_steps(bridge):
    """Accept only exact fixed assertions with a matching, linked GIVEN step."""
    output = []
    for link in bridge.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if type(link.step.conclusion) is not type(assertion.content):
            continue
        if link.step.conclusion != assertion.content:
            continue
        output.append(link.step)
    return tuple(output)


def binding_report(rule, goal, steps):
    """Compare goal-only and source-seeded inverse expansions without certifying them."""
    matched = unify_inference_conclusion(rule, goal)
    if matched is None:
        raise ValueError("R2 cannot unify with the typed cyclic goal")
    bound = {item.variable.name for item in matched.bindings}
    names = set()
    for premise in rule.premise_patterns:
        template = premise.relation_pattern if premise.relation_pattern is not None else premise.statement_pattern
        if template is None:
            raise ValueError("R2 premise lacks a typed pattern")
        names.update(_pattern_variable_names(template))
    candidates = generate_seeded_backward_goals(goal, (rule,), steps)
    matches = [item for item in candidates if item.rule is rule]
    return {
        "goal_unbound_variables": sorted(names - bound),
        "source_seeded_proposals": len(matches),
        "source_seeded_subgoals": [list(map(repr, item.subgoals)) for item in matches[:6]],
        "source_seeded_proposals_truncated": len(matches) > 6,
    }


def audit():
    registry = build_rule_registry(DEFAULT_RULE_MODULES)
    rule = registry.by_id(RULE_ID).rule
    goal = CyclicStructureStatement(TodaPrimaryGroup(4, 3), eta(3), 2)
    bridge = build_shared_typed_bridge()
    steps = fixed_typed_steps(bridge)
    counts = Counter(type(step.conclusion).__name__ for step in steps)
    report = binding_report(rule, goal, steps)
    return {
        "phase": "165 R12-R6",
        "mode": "READ_ONLY_REAL_TYPED_WITNESS_BINDING",
        "registry_rules": len(registry.entries),
        "r2_rule_registered": True,
        "fixed_typed_witness_count": len(steps),
        "relevant_fixed_witness_type_counts": {name: counts.get(name, 0) for name in PREMISE_TYPES},
        "other_witness_type_count": len(steps) - sum(counts.get(name, 0) for name in PREMISE_TYPES),
        **report,
        "binding_available": bool(report["source_seeded_proposals"]),
        "pi43_proof_certified": False,
        "full_pytest_run": False,
        "note": "A seeded proposal is a goal expansion, not a proof. Absence of source binding is not a mathematical disproof.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
