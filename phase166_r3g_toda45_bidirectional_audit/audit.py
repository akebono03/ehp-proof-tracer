"""Read-only production-path audit of Toda (4.5), forward and backward."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r12_r7_proof_order_guard import restrict_registered_ordered_claims
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog
from proof import ProofRule
from toda_rules import Toda45IsomorphismStatement
from toda_general_reference_schema import get_general_reference_statement


def inspect() -> dict:
    bridge = build_shared_typed_bridge()
    general = get_general_reference_statement("(4.5)")
    assert general is not None
    assert any(item.component_key == "stable_range_suspension_isomorphism" for item in general.components)
    given_links = tuple(link for link in bridge.proof_links if link.step is not None and link.step.rule is ProofRule.GIVEN)
    source45 = tuple(
        {"assertion_id": link.assertion_id,
         "type": type(link.step.conclusion).__name__,
         "locator": bridge.registry._references[bridge.registry.assertion(link.assertion_id).reference_id].locator}
        for link in given_links
        if bridge.registry._references[bridge.registry.assertion(link.assertion_id).reference_id].locator == "(4.5)"
    )
    concrete45 = tuple(link for link in given_links if isinstance(link.step.conclusion, Toda45IsomorphismStatement))
    cases = []
    for n, k in ((3, 1), (4, 1), (5, 1), (6, 2)):
        goals = registered_group_goal_candidates(bridge, n=n, k=k)
        catalog, diagnostic = resolve_reviewed_order_catalog(bridge, n=n, k=k)
        for goal in goals[:1]:
            assertions = tuple(bridge.registry._assertions.values())
            context_id = assertions[0].assertion_id
            context = screen_shared_proof_context(bridge, goal=goal, citing_assertion_id=context_id)
            context = restrict_registered_ordered_claims(context, goal)
            allowed = tuple(link.step.conclusion for link in context.proof_links if link.step is not None and link.step.rule is ProofRule.GIVEN)
            options = expand_registered_toda45_finite_cyclic_goal(goal, allowed)
            provider = shared_expansion_provider(context, proof_target=goal)
            expansions = provider(goal)
            cases.append({
                "n": n, "k": k,
                "reviewed_order_available": catalog is not None,
                "reviewed_order_diagnostic": diagnostic,
                "allowed_toda45_isomorphism_count": sum(isinstance(x, Toda45IsomorphismStatement) for x in allowed),
                "direct_toda45_backward_options": len(options),
                "shared_toda45_backward_options": sum("Toda 4.5" in str(getattr(x.rule, "name", "")) for x in expansions),
                "shared_expansion_count": len(expansions),
            })
    return {
        "audit": "phase166-r3g-toda45-bidirectional",
        "production_code_modified": False,
        "general_reference_registered": True,
        "general_reference_components": [x.component_key for x in general.components],
        "production_given_with_locator_4_5": source45,
        "production_concrete_toda45_given_count": len(concrete45),
        "common_search_cases": cases,
        "forward_rule_unit_test_source": "tests/test_phase46_toda_45_theorem_semantics.py",
        "backward_rule_unit_test_source": "phase165_r57_r7_toda45_backward_connection/test_phase165_r57_r7_toda45_backward_connection.py",
        "interpretation": "These checks distinguish standalone rule tests from production literature-to-rule connection. They do not claim an exhaustive proof over all integer parameters.",
    }


def main() -> None:
    result = inspect()
    filename = Path(__file__).with_name("audit_result.json")
    filename.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    print("Saved:", filename)


if __name__ == "__main__":
    main()
