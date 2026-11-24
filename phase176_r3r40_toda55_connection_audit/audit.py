"""Audit the Toda (5.5) connection using the canonical recursive DFS."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import sys
import tempfile

PACKAGE = "phase176_r3r40_toda55_connection_audit"
ROOT = Path(__file__).resolve().parent.parent


def source_guard() -> None:
    required = (
        "phase165_r52_r9_shared_math.py",
        "phase176_r3r27r1_toda55_quadruple_isolated/source.py",
        "phase176_r3r39_public_equality_transport/source.py",
        "phase165_r3_recursive_search.py",
        "relation_rules.py",
    )
    for filename in required:
        path = ROOT / filename
        ast.parse(path.read_text(encoding="utf-8-sig"), filename=filename)
    shared = (ROOT / required[0]).read_text(encoding="utf-8-sig")
    anchors = (
        "options.extend(public_right_hopf_transport(goal))",
        "return expand_cited_quadruple(goal, tuple(available))",
        "build_cited_toda55_quadruple_source(),",
    )
    if any(shared.count(anchor) != 1 for anchor in anchors):
        raise ValueError("EXISTING_PUBLIC_HOOKS_REQUIRED")


def probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
    from map_facts import EHP_H_MAP
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
    from phase176_r3r27r1_toda55_quadruple_isolated.source import (
        RULE_NAME, Toda55UniversalQuadrupleStatement, canonical_quadruple_goal,
        quadruple_inputs,
    )
    from phase176_r3r39_public_equality_transport.source import right_hopf_transport_backward_plan
    from phase176_r3r40_toda55_connection_audit.source import (
        build_audit_connection_provider, quadruple_hopf_backward_plan,
    )
    from proof import ProofRule, Relation, RelationType
    from unified_statement_registry import AssertionOrigin

    alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    gamma = Composition(eta6, eta7)
    transported = Relation(MapApplication(EHP_H_MAP, Composition(alpha, gamma)),
                           Composition(eta5, gamma), RelationType.EQUALITY)
    forward = canonical_quadruple_goal(5)
    if forward is None or forward.rhs != transported.rhs:
        raise RuntimeError("TYPED_ETA_CUBE_MISMATCH")
    goal = Relation(transported.lhs, forward.lhs, RelationType.EQUALITY)

    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    root = roots[0]
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root)
    links = tuple(link for link in screened.proof_links
                  if link.step is not None and link.step.rule is ProofRule.GIVEN
                  and screened.registry.assertion(link.assertion_id).origin
                  is AssertionOrigin.FIXED_STATEMENT
                  and screened.registry.assertion(link.assertion_id).content
                  == link.step.conclusion)
    available = tuple(link.step.conclusion for link in links)
    source_links = tuple(link for link in links
                         if link.step.conclusion == Toda55UniversalQuadrupleStatement())
    if len(source_links) != 1 or available.count(TodaProp22RightFormula()) != 1:
        raise RuntimeError("SOURCE_SCREENING_FAILED")
    if any(item in available for item in (root, goal, transported, forward)):
        raise RuntimeError("DERIVED_CONCLUSION_PRESENT_AS_GIVEN")
    context_id = source_links[0].assertion_id
    plan = quadruple_hopf_backward_plan(goal, available)
    if len(plan) != 2 or plan[1][1].subgoals[0] != transported:
        raise RuntimeError("TWO_STAGE_PLAN_MISSING")
    local = build_audit_connection_provider(goal, available)
    provider = shared_expansion_provider(screened, extra_providers=(local,), proof_target=root)
    for target, proposal in plan:
        if retain_ordered_root_expansions(root, target, (proposal,)) != (proposal,):
            raise RuntimeError("ROOT_ORDER_GATE_REJECTED")
        if not any(option.rule.name == proposal.rule.name and option.subgoals == proposal.subgoals
                   for option in provider(target)):
            raise RuntimeError("LOCAL_EXPANSION_NOT_REACHABLE")
    events = []
    result = reconstruct_registered_goal(
        goal, screened, context_id, provider, lookup_mode="typed_reference",
        progress_observer=lambda kind, target, step: events.append((kind, target)),
    )
    if (result.rule is not ProofRule.INFERENCE or result.conclusion != goal
            or result.inference_rule.name != "equality transitivity"
            or tuple(step.conclusion for step in result.premises) != plan[1][1].subgoals):
        raise RuntimeError("FINAL_TRANSITIVITY_TREE_MISMATCH")
    hopf, reverse = result.premises
    if (reverse.rule is not ProofRule.INFERENCE
            or reverse.inference_rule.name != "equality symmetry"
            or len(reverse.premises) != 1):
        raise RuntimeError("SYMMETRY_TREE_MISMATCH")
    quad = reverse.premises[0]
    if (quad.rule is not ProofRule.INFERENCE or quad.conclusion != forward
            or quad.inference_rule.name != RULE_NAME
            or tuple(step.conclusion for step in quad.premises) != quadruple_inputs(forward)):
        raise RuntimeError("TODA55_PROOF_TREE_MISMATCH")
    if (quad.premises[0].rule is not ProofRule.INFERENCE
            or any(step.rule is not ProofRule.GIVEN for step in quad.premises[1:])):
        raise RuntimeError("TODA55_PREMISE_PROVENANCE_MISMATCH")
    visited = []

    def visit(step):
        if any(step is old for old in visited):
            return
        visited.append(step)
        for child in step.premises:
            visit(child)

    visit(hopf)
    transport_plan = right_hopf_transport_backward_plan(transported, available)
    if len(transport_plan) != 6:
        raise RuntimeError("R3R39_PLAN_MISSING")
    for target, proposal in transport_plan:
        if not any(step.conclusion == target and step.rule is ProofRule.INFERENCE
                   and step.inference_rule.name == proposal.rule.name
                   and tuple(child.conclusion for child in step.premises) == proposal.subgoals
                   for step in visited):
            raise RuntimeError("R3R39_TREE_NOT_PRESERVED")
    visit(result)
    given_steps = tuple(step for step in visited if step.rule is ProofRule.GIVEN)
    if any(not any(step is link.step for link in links) for step in given_steps):
        raise RuntimeError("UNSCREENED_GIVEN_IN_TREE")
    if not any(step.conclusion == TodaProp22RightFormula() for step in given_steps):
        raise RuntimeError("PROP22_MISSING_IN_TREE")
    if not any(step.conclusion == Toda55UniversalQuadrupleStatement() for step in given_steps):
        raise RuntimeError("TODA55_MISSING_IN_TREE")
    if not any(kind == "proved" and target == goal for kind, target in events):
        raise RuntimeError("DFS_FINAL_EVENT_MISSING")
    generator = getattr(root.rhs, "generator", None)
    return {
        "gate": "PASS_R3R40_TODA55_AUDIT_DFS_EXISTING_RULES",
        "typed_eta_cube_exact_match": True,
        "associativity_required": False,
        "cited_toda55_count": len(source_links),
        "r3r39_six_steps_preserved": True,
        "existing_connection_rules": ["equality symmetry", "equality transitivity"],
        "audit_dfs_hopf_quadruple_proved": True,
        "registered_generator_matches_audit_expression": generator == goal.lhs.expression,
        "registered_generator_repr": repr(generator),
        "shared_default_provider_modified": False,
        "root_group_proved": False,
        "new_given": 0,
        "new_math_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        source_guard()
        result = ({"gate": "PASS_R3R40_DRYRUN", "full_pytest": "NOT_RUN"}
                  if args.dry_run else probe())
    except Exception as error:
        result = {"gate": "FAIL_R3R40", "error": type(error).__name__ + ": " + str(error),
                  "full_pytest": "NOT_RUN"}
    destination = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
                   / "EHPProofTracerAudit" / PACKAGE / "report.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key, value in result.items():
        print("PHASE176_R3R40_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    print("(END)")
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
