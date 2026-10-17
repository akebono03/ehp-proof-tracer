"""Read-only Phase 165 pre-R6 contract audit. No synthetic reference promotion."""
from __future__ import annotations

import json
from expression import eta
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r10_rule_registry import build_rule_registry
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r57_r23_conclusion_unification import unify_inference_conclusion
from phase165_r57_r26_generic_search_connection import build_generic_backward_expansion_provider
from phase165_r8_rule_provider import DEFAULT_RULE_MODULES, _pattern_variable_names
from proof import Relation, RelationType

R2_ID = "phase165_r12_r2_quotient_rules.infinite_cyclic_quotient_structure_inference_rule"
R5_ID = "phase165_r12_r5_structure_bridge.finite_cyclic_structure_as_relation_inference_rule"


def missing_premise_variables(rule, goal):
    matched = unify_inference_conclusion(rule, goal)
    if matched is None:
        return None
    bound = {binding.variable.name for binding in matched.bindings}
    required = set()
    for premise in rule.premise_patterns:
        template = premise.relation_pattern if premise.relation_pattern is not None else premise.statement_pattern
        if template is None:
            return None
        required.update(_pattern_variable_names(template))
    return sorted(required - bound)


def audit():
    registry = build_rule_registry(DEFAULT_RULE_MODULES)
    goal = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta(3)), RelationType.EQUALITY)
    rules = registry.rules()
    provider = build_generic_backward_expansion_provider(rules)
    root = provider(goal)
    r5 = registry.by_id(R5_ID).rule
    r2 = registry.by_id(R2_ID).rule
    r5_options = [item for item in root if item.rule is r5]
    if len(r5_options) != 1 or len(r5_options[0].subgoals) != 1:
        raise AssertionError("R5 root bridge must yield exactly one cyclic-structure premise")
    cyclic_goal = r5_options[0].subgoals[0]
    if cyclic_goal != CyclicStructureStatement(goal.lhs, eta(3), 2):
        raise AssertionError("R5 bridge generated a mismatched goal")
    unbound = missing_premise_variables(r2, cyclic_goal)
    if unbound is None:
        raise AssertionError("R2 conclusion cannot unify with R5 cyclic-structure goal")
    cyclic_proposals = provider(cyclic_goal)
    duplicate_pairs = []
    for i, first in enumerate(registry.entries):
        for second in registry.entries[i + 1:]:
            if (first.rule.conclusion_pattern == second.rule.conclusion_pattern
                and first.rule.premise_patterns == second.rule.premise_patterns):
                duplicate_pairs.append([first.rule_id, second.rule_id])
    r5_duplicates = [pair for pair in duplicate_pairs if R5_ID in pair]
    return {
        "phase": "165 R12 pre-R6",
        "mode": "READ_ONLY_TYPED_CONNECTION_AUDIT",
        "registry_rules": len(registry.entries),
        "r5_registered": registry.by_id(R5_ID).rule is r5,
        "r2_registered": registry.by_id(R2_ID).rule is r2,
        "r5_exact_pattern_duplicates": r5_duplicates,
        "all_exact_pattern_duplicate_pairs": duplicate_pairs,
        "root_expansions": len(root),
        "r5_root_subgoal": repr(cyclic_goal),
        "r2_cyclic_goal_unbound_variables": unbound,
        "r2_expands_from_cyclic_goal_without_extra_binding": any(x.rule is r2 for x in cyclic_proposals),
        "cyclic_goal_expansion_count": len(cyclic_proposals),
        "typed_source_witness_availability": "NOT_EVALUATED_BY_THIS_AUDIT",
        "pi43_proof_certified": False,
        "full_pytest_run": False,
        "note": "Pattern duplication is only syntactic and does not prove mathematical equivalence or lack of it.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
