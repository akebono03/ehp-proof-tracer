"""Phase 166 R3-AA: read-only real publication-order proof search audit."""
from __future__ import annotations

import ast
import json
from pathlib import Path

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from phase166_r3c_publication_order import precedes_citing_assertion
from proof import ProofRule, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement

TARGET_ID = "shared:2:toda:adopted:prop5.1:higher_eta_group_relation"
BASE_ID = "shared:2:toda:adopted:prop5.1:pi4_3"


def assert_legacy_gates_absent() -> dict[str, object]:
    source = Path("phase165_r52_r9_shared_math.py").read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "search_shared_group_goal"]
    if len(matches) != 1:
        raise AssertionError("search_shared_group_goal not uniquely found")
    func = matches[0]
    calls = {node.func.id for node in ast.walk(func) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    forbidden = sorted(calls & {"restrict_registered_ordered_claims", "restrict_by_proof_use_order", "resolve_registered_proof_use_order"})
    if forbidden:
        raise AssertionError("old order gates still active: " + ", ".join(forbidden))
    return {"legacy_gates_absent": True, "function": func.name}


def given_records(context):
    return [(link.assertion_id, link.step.conclusion) for link in context.proof_links
            if link.step is not None and link.step.rule is ProofRule.GIVEN]


def run():
    source_check = assert_legacy_gates_absent()
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=4, k=1)
    if len(candidates) != 1:
        raise AssertionError(f"expected exactly one pi5^4 goal: {len(candidates)}")
    goal = candidates[0]
    if goal.lhs != TodaPrimaryGroup(5, 4):
        raise AssertionError("unexpected pi5^4 goal")
    if not precedes_citing_assertion(bridge, BASE_ID, TARGET_ID):
        raise AssertionError("pi4^3 must precede pi5^4 publication boundary")
    context = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=TARGET_ID,
        explicit_publication_target=True,
    )
    context = prefer_universal_prop42_derivation(context)
    records = given_records(context)
    pi43 = [(aid, statement) for aid, statement in records
            if isinstance(statement, Relation)
            and statement.relation_type is RelationType.EQUALITY
            and statement.lhs == TodaPrimaryGroup(4, 3)
            and isinstance(statement.rhs, FiniteCyclicGroup)
            and statement.rhs.order == 2]
    toda45 = [(aid, statement) for aid, statement in records
              if isinstance(statement, Toda45IsomorphismStatement)]
    provider = shared_expansion_provider(context, proof_target=goal)
    root_options = provider(goal)
    normalization = [option for option in root_options
                     if "generator suspension normalizes" in option.rule.name]
    transports = []
    for option in normalization:
        for child in option.subgoals:
            if not (isinstance(child, Relation) and isinstance(child.rhs, FiniteCyclicGroup)
                    and isinstance(child.rhs.generator, IteratedSuspension)):
                continue
            for step in provider(child):
                transports.append({"rule": step.rule.name,
                                   "subgoals": [repr(s) for s in step.subgoals]})
    trace = []
    def observer(kind, current, step):
        if len(trace) >= 120:
            return
        if current == goal or isinstance(current, Toda45IsomorphismStatement) or (
                isinstance(current, Relation) and current.lhs in (TodaPrimaryGroup(4, 3), TodaPrimaryGroup(5, 4))):
            trace.append({"kind": str(kind), "goal": repr(current),
                          "rule": getattr(getattr(step, "inference_rule", None), "name", None)})
    try:
        root = reconstruct_registered_goal(
            goal, context, TARGET_ID, provider,
            lookup_mode="typed_reference_publication", progress_observer=observer,
        )
        result = {"complete": True, "conclusion_matches_goal": root.conclusion == goal,
                  "root_rule": getattr(root, "rule", None).name if getattr(root, "rule", None) else None,
                  "premise_count": len(getattr(root, "premises", ())) }
    except RegisteredGoalUnresolved as error:
        result = {"complete": False, "reason": str(error)}
    # Also exercise the normal Web-facing registered-goal entry point.
    from phase165_r52_partial_proof import ProofSearchStatus
    try:
        web_result = search_group_from_registered_goal(n=4, k=1, bridge=bridge)
        web = {"status": str(web_result.status), "complete": web_result.status is ProofSearchStatus.COMPLETE,
               "conclusion_matches_goal": web_result.conclusion == goal,
               "open_goals": [repr(x) for x in web_result.open_goals],
               "diagnostics": [str(x) for x in web_result.diagnostics]}
    except Exception as error:
        web = {"exception": type(error).__name__, "message": str(error)}
    report = {
        "phase": "166 R3-AA", "production_code_modified": False,
        "full_pytest_run": False, "source_check": source_check,
        "target_id": TARGET_ID,
        "publication_precedes": True,
        "given_count": len(records),
        "pi43_base": [{"id": aid, "statement": repr(value)} for aid, value in pi43],
        "toda45_sources": [{"id": aid, "statement": repr(value)} for aid, value in toda45],
        "root_rules": [option.rule.name for option in root_options],
        "normalization_count": len(normalization),
        "transport_candidates": transports,
        "direct_search": result, "web_search": web, "trace": trace,
    }
    out = Path(__file__).with_name("report.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {
        "publication_precedes": True, "pi43_count": len(pi43),
        "toda45_count": len(toda45), "normalization_count": len(normalization),
        "transport_rules": [x["rule"] for x in transports],
        "direct_search": result, "web_search": web,
        "report": str(out), "full_pytest_run": False,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not pi43 or not toda45 or not normalization or not transports:
        raise SystemExit("R3-AA: source/expansion connection incomplete; inspect report.json")
    if not result.get("complete") or not result.get("conclusion_matches_goal") or not web.get("complete"):
        raise SystemExit("R3-AA: actual pi5^4 proof not complete; inspect report.json")


if __name__ == "__main__":
    run()
