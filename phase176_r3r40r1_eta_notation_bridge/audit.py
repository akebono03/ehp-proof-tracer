"""Read-only real shared-DFS audit with explicitly scoped notation proposals."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import sys
import tempfile

PACKAGE = "phase176_r3r40r1_eta_notation_bridge"
ROOT = Path(__file__).resolve().parent.parent


def source_guard() -> None:
    from phase176_r3r40_toda55_connection_audit.audit import source_guard as prior_guard
    prior_guard()
    for filename in (
        "phase165_r12_r21_eta_generator_chain.py",
        "phase165_r12_r28_presentation_connection.py",
        "phase171_r2i_eta_hopf_bridge/source.py",
        "phase176_r3r40r1_eta_notation_bridge/source.py",
    ):
        ast.parse((ROOT / filename).read_text(encoding="utf-8-sig"), filename=filename)


def probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
    from map_facts import EHP_H_MAP
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
    from phase176_r3r27r1_toda55_quadruple_isolated.source import (
        RULE_NAME, Toda55UniversalQuadrupleStatement, canonical_quadruple_goal, quadruple_inputs,
    )
    from phase176_r3r39_public_equality_transport.source import right_hopf_transport_backward_plan
    from phase176_r3r40r1_eta_notation_bridge.source import connection_backward_plan, eta_notation_backward_plan
    from proof import ProofRule, Relation
    from unified_statement_registry import AssertionOrigin

    alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    gamma = Composition(eta6, eta7)
    transported = Relation(MapApplication(EHP_H_MAP, Composition(alpha, gamma)), Composition(eta5, gamma))
    forward = canonical_quadruple_goal(5)
    if forward is None:
        raise RuntimeError("CANONICAL_QUADRUPLE_MISSING")
    print("PHASE176_R3R40R1_TRANSPORT_CUBE_REPR=" + repr(transported.rhs))
    print("PHASE176_R3R40R1_TODA55_CUBE_REPR=" + repr(forward.rhs))
    goal = Relation(transported.lhs, forward.lhs)
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    root = roots[0]
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root)
    links = tuple(link for link in screened.proof_links
                  if link.step is not None and link.step.rule is ProofRule.GIVEN
                  and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
                  and screened.registry.assertion(link.assertion_id).content == link.step.conclusion)
    available = tuple(link.step.conclusion for link in links)
    sources = tuple(link for link in links if link.step.conclusion == Toda55UniversalQuadrupleStatement())
    if (len(sources) != 1 or available.count(TodaEtaFamilyGeneralDefinition()) != 1
            or available.count(TodaProp22RightFormula()) != 1):
        raise RuntimeError("SCREENED_SOURCES_MISSING_OR_AMBIGUOUS")
    notation = eta_notation_backward_plan(transported.rhs, forward.rhs, available)
    if transported.rhs != forward.rhs and not notation:
        raise RuntimeError("NO_TYPED_ETA_NOTATION_PLAN")
    plan = connection_backward_plan(transported, forward, available)
    transport_plan = right_hopf_transport_backward_plan(transported, available)
    if not plan or len(transport_plan) != 6:
        raise RuntimeError("CONNECTION_PLAN_MISSING")
    if any(item in available for item in (root, transported, forward, goal) + tuple(target for target, _ in plan)):
        raise RuntimeError("DERIVED_GOAL_PRESENT_AS_GIVEN")
    stages = dict(plan)
    default = shared_expansion_provider(screened, proof_target=root)

    def provider(target):
        # Prioritize only the explicit audit plan. All other obligations go to
        # the unmodified shared provider; no pre-completed proof is supplied.
        if isinstance(target, Relation) and target in stages:
            candidate = (stages[target],)
            if retain_ordered_root_expansions(root, target, candidate) != candidate:
                raise RuntimeError("ROOT_ORDER_GATE_REJECTED")
            return candidate + default(target)
        return default(target)

    events = []
    result = reconstruct_registered_goal(goal, screened, sources[0].assertion_id, provider,
        lookup_mode="typed_reference", progress_observer=lambda kind, target, step: events.append((kind, target)))
    visited = []

    def visit(step):
        if any(step is earlier for earlier in visited):
            return
        visited.append(step)
        for child in step.premises:
            visit(child)

    visit(result)
    if result.conclusion != goal or result.rule is not ProofRule.INFERENCE:
        raise RuntimeError("FINAL_GOAL_NOT_INFERRED")
    for target, expansion in tuple(transport_plan) + plan:
        if not any(step.conclusion == target and step.rule is ProofRule.INFERENCE
                   and step.inference_rule.name == expansion.rule.name
                   and tuple(child.conclusion for child in step.premises) == expansion.subgoals
                   for step in visited):
            raise RuntimeError("TREE_STAGE_MISSING:" + expansion.rule.name + ":" + repr(target))
    quad = next((step for step in visited if step.conclusion == forward), None)
    if (quad is None or quad.rule is not ProofRule.INFERENCE or quad.inference_rule.name != RULE_NAME
            or tuple(child.conclusion for child in quad.premises) != quadruple_inputs(forward)
            or quad.premises[0].rule is not ProofRule.INFERENCE
            or any(child.rule is not ProofRule.GIVEN for child in quad.premises[1:])):
        raise RuntimeError("TODA55_TREE_MISSING")
    witness_targets = tuple(dict.fromkeys(child for _, option in notation for child in option.subgoals
                                         if isinstance(child, GeneratorSuspension)))
    for witness in witness_targets:
        if not any(step.conclusion == witness and step.rule is ProofRule.INFERENCE for step in visited):
            raise RuntimeError("ETA_WITNESS_NOT_INFERRED")
    givens = tuple(step for step in visited if step.rule is ProofRule.GIVEN)
    if any(not any(step is link.step for link in links) for step in givens):
        raise RuntimeError("UNSCREENED_GIVEN")
    for required in (Toda55UniversalQuadrupleStatement(), TodaEtaFamilyGeneralDefinition(), TodaProp22RightFormula()):
        if not any(step.conclusion == required for step in givens):
            raise RuntimeError("CITED_ANCESTOR_MISSING:" + repr(required))
    if not any(kind == "proved" and target == goal for kind, target in events):
        raise RuntimeError("FINAL_DFS_EVENT_MISSING")
    generator = getattr(root.rhs, "generator", None)
    return {
        "gate": "PASS_R3R40R1_AUDIT_DFS_TYPED_ETA_NOTATION",
        "raw_eta_cube_equal": transported.rhs == forward.rhs,
        "notation_steps": len(notation),
        "independently_inferred_eta_witnesses": len(witness_targets),
        "notation_connection_proved": True,
        "r3r39_six_steps_preserved": True,
        "toda55_inferred_with_cited_ancestors": True,
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
        result = {"gate": "PASS_R3R40R1_DRYRUN", "full_pytest": "NOT_RUN"} if args.dry_run else probe()
    except Exception as error:
        result = {"gate": "FAIL_R3R40R1", "error": type(error).__name__ + ": " + str(error), "full_pytest": "NOT_RUN"}
    destination = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE / "report.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key, value in result.items():
        print("PHASE176_R3R40R1_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    print("(END)")
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
