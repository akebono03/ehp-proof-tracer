"""Observe the actual public Web search without adding proof candidates."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
from unittest.mock import patch

PACKAGE = "phase176_r3r42_root_backward_frontier_audit"
ROOT = Path(__file__).resolve().parent.parent
REVIEWED_HEAD = "7cbf3edfa0de21a24eb249637e1e99127a176297"
REQUIRED = (
    "web_group_proof.py",
    "phase165_r55_nk_only_goal.py",
    "phase165_r52_r9_shared_math.py",
    "phase165_r52_r2_search_adapter.py",
    "phase165_r3_recursive_search.py",
    "phase165_r57_r11_proof_order_gate.py",
    "phase176_r3r41_public_quadruple_connection/source.py",
    "phase175_r3_pi73_hopf_lift/rule.py",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py",
)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True,
                                   encoding="utf-8", errors="replace").strip()


def source_guard() -> str:
    head = git("rev-parse", "HEAD")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    subprocess.run(["git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head],
                   cwd=ROOT, check=True)
    if git("status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("TRACKED_WORKTREE_NOT_CLEAN")
    for name in REQUIRED:
        ast.parse((ROOT / name).read_text(encoding="utf-8-sig"), filename=name)
    return head


def option_record(option: object) -> dict:
    rule = getattr(option, "rule", None)
    return {"rule": getattr(rule, "name", None) or type(rule).__name__,
            "subgoals": [repr(goal) for goal in option.subgoals]}


def wrap_provider(provider, calls: list):
    """Preserve exact return object, order, exceptions and call count."""
    def observed(goal):
        options = provider(goal)
        calls.append((goal, options))
        return options
    return observed


def call_records(calls: list, goal: object) -> list:
    return [{"count": len(options), "options": [option_record(o) for o in options]}
            for requested, options in calls if requested == goal]


def classify(status: str, root_calls: list, root_gates: list,
             cyclic_calls: list) -> str:
    if status == "complete":
        return "ROOT_COMPLETE"
    if not root_calls:
        return "ROOT_PROVIDER_NOT_REACHED"
    if all(row["count"] == 0 for row in root_calls):
        if any(row["before"] > 0 and row["after"] == 0 for row in root_gates):
            return "ROOT_CANDIDATES_FILTERED"
        return "ROOT_NO_CANDIDATES"
    if cyclic_calls and all(row["count"] == 0 for row in cyclic_calls):
        return "CYCLIC_CHILD_NO_CANDIDATES"
    return "ROOT_CANDIDATES_UNVERIFIED"


def independent_probes(root, context, prior, calls, steps) -> dict:
    """Inspect proposals separately, never feed these into the Web search."""
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
    from map_facts import EHP_H_MAP
    from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r14_r6_generic_iso import MapInjective
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        expand_hopf_injective_from_zero_image,
    )
    from phase175_r3_pi73_hopf_lift.rule import expand_cited_hopf_lift
    from phase176_r3r27r1_toda55_quadruple_isolated.source import canonical_quadruple_goal
    from phase176_r3r41_public_quadruple_connection.source import public_quadruple_backward_plan
    from proof import ProofRule, Relation
    from unified_statement_registry import AssertionOrigin

    available = tuple(link.step.conclusion for link in context.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN
                      and context.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
                      and context.registry.assertion(link.assertion_id).content == link.step.conclusion)
    if root in available:
        raise RuntimeError("ROOT_PRESENT_AS_SCREENED_GIVEN")
    generator = root.rhs.generator
    if not isinstance(generator, Composition):
        raise RuntimeError("ROOT_GENERATOR_NOT_COMPOSITION")
    cyclic = CyclicStructureStatement(root.lhs, generator, root.rhs.order)
    codomain = TodaPrimaryGroup(8, 5)
    injective = MapInjective(TodaHopfInvariantMap(root.lhs, codomain))
    isolated = expand_hopf_injective_from_zero_image(injective)
    forward = canonical_quadruple_goal(5)
    if forward is None:
        raise RuntimeError("CANONICAL_QUADRUPLE_MISSING")
    alpha = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    canonical = Relation(MapApplication(EHP_H_MAP, Composition(alpha, generator.right)), forward.lhs)
    registered = Relation(MapApplication(EHP_H_MAP, generator), forward.lhs)
    goals = [("cyclic_structure", cyclic), ("hopf_injective", injective),
             ("hopf_registered", registered), ("hopf_canonical", canonical)]
    if len(isolated) == 1:
        goals.extend((f"hopf_injective_premise_{i+1}", goal)
                     for i, goal in enumerate(isolated[0].subgoals))
    probes = {}
    for name, goal in goals:
        provider = shared_expansion_provider(context, proof_target=root, prior_conclusions=prior)
        options = provider(goal)
        probes[name] = {"goal": repr(goal), "candidate_count": len(options),
                        "options": [option_record(o) for o in options],
                        "actual_web_provider_calls": len(call_records(calls, goal)),
                        "actual_web_accepted_steps": sum(s.conclusion == goal for s in steps)}
    return {"goals": probes,
            "old_whole_codomain_hopf_lift_count": len(expand_cited_hopf_lift(cyclic, available)),
            "isolated_zero_image_injectivity_count": len(isolated),
            "isolated_zero_image_injectivity_options": [option_record(o) for o in isolated],
            "canonical_public_quadruple_plan_stages": len(public_quadruple_backward_plan(canonical, available)),
            "registered_public_quadruple_plan_stages": len(public_quadruple_backward_plan(registered, available)),
            "registered_generator_matches_canonical": canonical.lhs.expression == generator,
            "screened_given_count": len(available)}


def observe() -> dict:
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    import phase165_r57_r11_proof_order_gate as gate
    from web_group_proof import build_standard_web_group_proof_view
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from proof import ProofRule

    real_entry = entry.search_group_from_registered_goal
    real_adapter = shared.search_registered_partial_proof
    real_gate = gate.retain_ordered_root_expansions
    calls, gates, adapters, results = [], [], [], []

    def observed_entry(*args, **kwargs):
        result = real_entry(*args, **kwargs)
        results.append(result)
        return result

    def observed_adapter(*args, **kwargs):
        if (kwargs.get("n"), kwargs.get("k")) != (3, 5):
            return real_adapter(*args, **kwargs)
        adapters.append(dict(kwargs))
        forwarded = dict(kwargs)
        forwarded["expansion_provider"] = wrap_provider(kwargs["expansion_provider"], calls)
        return real_adapter(*args, **forwarded)

    def observed_gate(proof_target, current_goal, candidates):
        retained = real_gate(proof_target, current_goal, candidates)
        if proof_target == current_goal:
            gates.append((current_goal, candidates, retained))
        return retained

    with patch.object(entry, "search_group_from_registered_goal", new=observed_entry), \
         patch.object(shared, "search_registered_partial_proof", new=observed_adapter), \
         patch.object(gate, "retain_ordered_root_expansions", new=observed_gate):
        view = build_standard_web_group_proof_view(n=3, k=5, max_depth=2, mode="narrative")

    if len(results) != 1 or len(adapters) != 1:
        raise RuntimeError(f"UNEXPECTED_PUBLIC_ENTRY_COUNTS: results={len(results)}, adapters={len(adapters)}")
    result, invocation = results[0], adapters[0]
    root, context = invocation["goal"], invocation["bridge"]
    prior = tuple(item.root.conclusion for item in invocation.get("completed_internal_proofs", ()))
    root_calls = call_records(calls, root)
    root_gates = [{"before": len(before), "after": len(after),
                   "before_options": [option_record(o) for o in before],
                   "after_options": [option_record(o) for o in after]}
                  for goal, before, after in gates if goal == root]
    cyclic = CyclicStructureStatement(root.lhs, root.rhs.generator, root.rhs.order)
    cyclic_calls = call_records(calls, cyclic)
    steps = tuple(result.proven_steps)
    probes = independent_probes(root, context, prior, calls, steps)
    return {"gate": "PASS_R3R42_PUBLIC_ROOT_FRONTIER_RECORDED",
            "classification": classify(result.status.value, root_calls, root_gates, cyclic_calls),
            "root": repr(root), "lookup_mode": invocation.get("lookup_mode"),
            "citing_assertion_id": invocation.get("citing_assertion_id"),
            "prior_count": len(prior), "status": result.status.value,
            "web_key": view.key, "web_partial": view.partial_result,
            "web_step_count": len(view.steps), "web_rendered_lines": [repr(x) for x in view.rendered_lines],
            "root_provider_calls": root_calls, "root_gate_calls": root_gates,
            "cyclic_provider_calls": cyclic_calls,
            "all_provider_calls": [{"goal": repr(g), "count": len(o),
                                     "options": [option_record(x) for x in o]} for g, o in calls],
            "accepted_step_count": len(steps),
            "accepted_given_count": sum(s.rule is ProofRule.GIVEN for s in steps),
            "accepted_steps": [repr(s.conclusion) for s in steps],
            "open_goals": [repr(g) for g in result.open_goals],
            "diagnostics": [str(x) for x in result.diagnostics],
            "independent_probes_not_search_evidence": probes,
            "root_group_proved": result.status.value == "complete",
            "new_given": 0, "new_math_rules": 0, "full_pytest": "NOT_RUN"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        head = source_guard()
        report = {"gate": "PASS_R3R42_DRYRUN", "full_pytest": "NOT_RUN"} if args.dry_run else observe()
        if source_guard() != head:
            raise RuntimeError("HEAD_CHANGED_DURING_AUDIT")
        report["head"] = head
        report["tracked_worktree_clean"] = True
    except Exception as exc:
        report = {"gate": "FAIL_R3R42", "error": f"{type(exc).__name__}: {exc}",
                  "traceback": traceback.format_exc(), "full_pytest": "NOT_RUN"}
    destination = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE / "report.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key in ("gate", "head", "classification", "status", "web_key", "web_partial", "web_step_count",
                "accepted_step_count", "accepted_given_count", "root_group_proved", "new_given", "new_math_rules",
                "tracked_worktree_clean", "full_pytest", "error"):
        if key in report:
            print("PHASE176_R3R42_" + key.upper() + "=" + str(report[key]))
    for key in ("root_provider_calls", "root_gate_calls", "cyclic_provider_calls"):
        if key in report:
            for row in report[key]:
                print("PHASE176_R3R42_" + key.upper() + "=" + str({k: v for k, v in row.items() if k in ("count", "before", "after")}))
            if not report[key]:
                print("PHASE176_R3R42_" + key.upper() + "=NOT_REACHED")
    if "independent_probes_not_search_evidence" in report:
        probes = report["independent_probes_not_search_evidence"]
        for name, row in probes["goals"].items():
            print("PHASE176_R3R42_PROBE_" + name.upper() + "=" + str({k: v for k, v in row.items() if k not in ("goal", "options")}))
        for key, value in probes.items():
            if key not in ("goals", "isolated_zero_image_injectivity_options"):
                print("PHASE176_R3R42_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(destination))
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
