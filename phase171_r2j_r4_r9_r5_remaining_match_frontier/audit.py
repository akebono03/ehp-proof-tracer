"""Trace the first remaining canonical matcher failure after bound Hopf repair.

The audit rebuilds R4-R8's inference rule graph and uses R9-R4's existing
SourceBoundGoal provider. No completed ProofStep is handed to the search, and
no GIVEN or public route is added. All matcher attempts are observations.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
from unittest.mock import patch

import phase165_r3_recursive_search as search_engine
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree,
    verify_proof_tree_for_narrative,
)
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r2_scoped_search_bridge.source import (
    inference_expansion_catalog,
    walk_proof_ancestry,
)
from phase171_r2j_r4_r9_r4_source_bound_hopf.audit import hopf_goal
from phase171_r2j_r4_r9_r4_source_bound_hopf.source import source_bound_hopf_provider
from proof import ProofRule, ProofStep

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if arguments not in allowed:
        raise ValueError("read-only Git commands only")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT,
        check=True, capture_output=True, text=True,
    ).stdout.strip()


def _classify_match_attempt(record: dict) -> str:
    """Explain a genuine zero-match event without claiming its cause as fact."""
    if record["matches"]:
        return "MATCH_ACCEPTED"
    if record["actual_conclusions"] != record["expected_conclusions"]:
        return "PREMISE_CONCLUSION_MISMATCH"
    if record["actual_proof_rules"] != record["expected_proof_rules"]:
        return "PREMISE_PROOF_RULE_MISMATCH"
    return "MATCHER_PATTERN_OR_GUARD_REJECTION"


def _proof_event(kind: str, goal: object, step: ProofStep | None) -> dict:
    if kind not in ("proved", "unresolved"):
        raise ValueError("unknown canonical search event")
    if kind == "proved" and not isinstance(step, ProofStep):
        raise TypeError("proved event requires ProofStep")
    return {
        "kind": kind,
        "goal_type": type(goal).__name__,
        "goal": repr(goal)[:1100],
        "proof_rule": step.rule.value if step is not None else None,
    }


def inspect_remaining_match_frontier() -> dict:
    """Observe canonical reconstruction with the existing, local R9-R4 repair."""
    screened, target, citing = _screened_context()
    root, _, previous = build_cyclic_pi63_proof()
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != target
        or previous["new_given_added"] != 0
    ):
        raise RuntimeError("validated inferred R4-R8 group root is required")
    catalog = inference_expansion_catalog(root)
    nodes = walk_proof_ancestry(root)
    rule_nodes = {id(step.inference_rule): step for step in nodes
                  if step.rule is ProofRule.INFERENCE}
    ordinary = shared_expansion_provider(screened, proof_target=target)
    provider, bound, source_id = source_bound_hopf_provider(
        root, screened, citing, hopf_goal(), ordinary,
    )
    original_matcher = search_engine.find_inference_matches_for_rule
    attempts: list[dict] = []
    events: list[dict] = []

    def observe(kind: str, goal: object, step: ProofStep | None) -> None:
        if len(events) < 600:
            events.append(_proof_event(kind, goal, step))

    def trace(rule, premises):
        matches = original_matcher(rule, premises)
        original = rule_nodes.get(id(rule))
        if original is not None and len(attempts) < 300:
            expected = original.premises
            item = {
                "conclusion": repr(original.conclusion)[:1100],
                "conclusion_type": type(original.conclusion).__name__,
                "inference_rule": rule.name,
                "matches": len(matches),
                "actual_proof_rules": [step.rule.value for step in premises],
                "expected_proof_rules": [step.rule.value for step in expected],
                "actual_conclusions": [repr(step.conclusion)[:1100] for step in premises],
                "expected_conclusions": [repr(step.conclusion)[:1100] for step in expected],
            }
            item["classification"] = _classify_match_attempt(item)
            attempts.append(item)
        return matches

    result = None
    failure = None
    with patch.object(search_engine, "find_inference_matches_for_rule", side_effect=trace):
        try:
            result = search_engine.reconstruct_registered_goal(
                target, screened, citing, provider,
                lookup_mode="typed_reference_publication",
                progress_observer=observe,
            )
        except search_engine.RegisteredGoalUnresolved as exc:
            failure = str(exc)
    complete = bool(result is not None and result.rule is ProofRule.INFERENCE
                    and result.conclusion == target)
    if result is not None and not complete:
        raise RuntimeError("unexpected completed canonical root")
    accepted = False
    trust_result = None
    if complete:
        from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
        proof_result = make_partial_proof_result(
            n=3, k=3, status=ProofSearchStatus.COMPLETE,
            proven_steps=walk_proof_ancestry(result), conclusion=target,
        )
        try:
            trust_result = verify_proof_tree_for_narrative(
                proof_result, screened, citing_assertion_id=citing,
            )
            accepted = True
        except UnverifiedProofTree as exc:
            trust_result = str(exc)
    rejected = [record for record in attempts if record["matches"] == 0]
    unresolved = [row for row in events if row["kind"] == "unresolved"]
    hopf_rebuilt = any(row["kind"] == "proved" and row["goal"] == repr(hopf_goal())[:1100]
                       and row["proof_rule"] == ProofRule.INFERENCE.value for row in events)
    if not hopf_rebuilt:
        raise RuntimeError("R9-R4 Hopf repair regressed during frontier replay")
    first = rejected[0] if rejected else None
    classification = (
        first["classification"] if first is not None else
        "UNRESOLVED_SUBGOAL_BEFORE_MATCH" if unresolved else
        "RECONSTRUCTED" if complete else "NO_MATCHER_FAILURE_RECORDED"
    )
    return {
        "phase": "171-R2J-R4-R9-R5",
        "mode": "AUDIT_ONLY_REMAINING_MATCHER_FRONTIER",
        "head_target": repr(target),
        "source_bound_assertion_id": source_id,
        "source_bound_conclusion": repr(bound.conclusion),
        "inferred_rule_catalog": len(catalog),
        "hopf_surjectivity_rebuilt": hopf_rebuilt,
        "canonical_search_status": "complete" if complete else "partial",
        "canonical_error": failure,
        "matcher_attempts": len(attempts),
        "rejected_matcher_attempts": len(rejected),
        "first_rejection_class": classification,
        "first_rejected_match": first,
        "first_unresolved_goal": unresolved[0] if unresolved else None,
        "unresolved_goals": unresolved[:30],
        "rejected_matches": rejected[:25],
        "all_match_attempts": attempts[:70],
        "trust_boundary_accepted": accepted,
        "trust_boundary_result": trust_result,
        "new_given_added": 0,
        "public_provider_modified": False,
        "public_web_verified": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    tracked_before = _git("status", "--porcelain", "--untracked-files=no")
    if branch != "develop":
        raise RuntimeError("R9-R5 requires develop")
    for name in (
        "phase171_r2j_r4_r9_r4_source_bound_hopf/source.py",
        "phase171_r2j_r4_r8_cyclic_structure/audit.py",
    ):
        if not (ROOT / name).is_file():
            raise RuntimeError("missing prerequisite: " + name)
    print("PHASE171_R2J_R4_R9_R5_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R5_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R5_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = inspect_remaining_match_frontier()
    if _git("status", "--porcelain", "--untracked-files=no") != tracked_before:
        raise RuntimeError("tracked files modified during read-only R9-R5 audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(parents=True, exist_ok=True)
    path = OUTPUT / "audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R5_HOPF_REBUILT=" + str(report["hopf_surjectivity_rebuilt"]), flush=True)
    print("PHASE171_R2J_R4_R9_R5_MATCH_ATTEMPTS=" + str(report["matcher_attempts"]), flush=True)
    print("PHASE171_R2J_R4_R9_R5_REJECTED=" + str(report["rejected_matcher_attempts"]), flush=True)
    print("PHASE171_R2J_R4_R9_R5_FRONTIER=" + report["first_rejection_class"], flush=True)
    if report["first_rejected_match"] is not None:
        print("PHASE171_R2J_R4_R9_R5_FIRST_RULE=" + report["first_rejected_match"]["inference_rule"], flush=True)
    elif report["first_unresolved_goal"] is not None:
        print("PHASE171_R2J_R4_R9_R5_FIRST_GOAL=" + report["first_unresolved_goal"]["goal_type"], flush=True)
    print("PHASE171_R2J_R4_R9_R5_SCOPED_SEARCH=" + report["canonical_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R5_TRUST_VERIFIED=" + str(report["trust_boundary_accepted"]), flush=True)
    print("PHASE171_R2J_R4_R9_R5_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R5_PUBLIC_WEB_VERIFIED=False", flush=True)
    print("PHASE171_R2J_R4_R9_R5_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R5_REPORT=" + str(path), flush=True)
    print("PHASE171_R2J_R4_R9_R5_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
