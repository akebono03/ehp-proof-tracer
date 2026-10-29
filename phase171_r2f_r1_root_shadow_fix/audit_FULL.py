"""Read-only audit for the typed order-four extension of pi_6^3.

This code neither adds a ProofStep nor changes any inference rule or source.
A mathematical argument is not reported as a completed machine proof.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import fields, is_dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

EXPECTED_TARGET = "shared:0:boundary:Proposition 5.6:pi6_3_group_relation"
EXPECTED_DOUBLE_SUFFIX = "toda:adopted:eq5.3:nu_prime_double_relation"
EXPECTED_HOPF_SUFFIX = "toda:adopted:eq5.3:nu_prime_hopf_relation"
LOCATORS = (
    "Proposition 2.2", "Proposition 4.2 (4.4)", "(5.2)",
    "Proposition 5.3", "(5.3)", "Proposition 5.6",
)


def git_read(root: Path, *arguments: str) -> bytes:
    """Execute only listed read-only Git invocations and require success."""
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("rev-parse", "--verify", "refs/remotes/origin/develop"),
        ("status", "--porcelain=v1", "--untracked-files=all"),
        ("diff", "--binary", "HEAD", "--"),
    }
    if arguments not in allowed:
        raise ValueError("Git operation not authorized for R2F audit")
    process = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, check=False,
    )
    if process.returncode:
        raise RuntimeError(
            "git " + " ".join(arguments) + ": "
            + process.stderr.decode("utf-8", errors="replace")
        )
    return process.stdout


def snapshot(root: Path) -> dict:
    """Record committed identity and exact tracked/untracked worktree state."""
    branch = git_read(root, "branch", "--show-current").decode().strip()
    if branch != "develop":
        raise RuntimeError("R2F requires develop but never switches branches")
    head = git_read(root, "rev-parse", "HEAD").decode().strip()
    try:
        upstream = git_read(root, "rev-parse", "--verify", "refs/remotes/origin/develop").decode().strip()
    except RuntimeError:
        upstream = None
    return {
        "branch": branch,
        "head": head,
        "origin_develop_local_ref": upstream,
        "head_equals_local_origin_ref": head == upstream,
        "status": git_read(root, "status", "--porcelain=v1", "--untracked-files=all").decode(
            "utf-8", errors="replace"
        ).splitlines(),
        "tracked_diff_sha256": sha256(git_read(root, "diff", "--binary", "HEAD", "--")).hexdigest(),
    }


def typed_differences(left: object, right: object, *, limit: int = 20) -> list[dict]:
    """Compare dataclass fields exactly; never accept name-only generator aliases."""
    differences: list[dict] = []

    def visit(a: object, b: object, path: str, depth: int) -> None:
        if len(differences) >= limit:
            return
        if type(a) is not type(b):
            differences.append({
                "path": path, "reason": "type_mismatch",
                "left": type(a).__name__, "right": type(b).__name__,
            })
            return
        if depth >= 12:
            if a != b:
                differences.append({"path": path, "reason": "depth_limit"})
            return
        if is_dataclass(a) and not isinstance(a, type):
            for field in fields(a):
                visit(getattr(a, field.name), getattr(b, field.name), path + "." + field.name, depth + 1)
            return
        if a != b:
            differences.append({
                "path": path, "reason": "value_mismatch",
                "left": repr(a)[:250], "right": repr(b)[:250],
            })

    visit(left, right, "generator", 0)
    return differences


def matching_cited_steps(bridge: object, suffix: str) -> tuple:
    """Require screened, no-premise, registered fixed GIVENs with exact identity."""
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    matches = []
    for link in bridge.proof_links:
        step = link.step
        if not link.assertion_id.endswith(suffix) or step is None:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and step.rule is ProofRule.GIVEN
                and not step.premises
                and step.conclusion == assertion.content):
            matches.append((link.assertion_id, step.conclusion))
    return tuple(matches)


def source_inventory(bridge: object) -> dict:
    """Count screened assertions, never count unscreened archive metadata as proof."""
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    output = {}
    for locator in LOCATORS:
        entries = []
        for link in bridge.proof_links:
            step = link.step
            if step is None:
                continue
            assertion = bridge.registry.assertion(link.assertion_id)
            reference = bridge.registry.reference(assertion.reference_id)
            if reference.locator != locator:
                continue
            if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                    or step.rule is not ProofRule.GIVEN
                    or step.premises or step.conclusion != assertion.content):
                continue
            entries.append({
                "id": link.assertion_id,
                "type": type(step.conclusion).__name__,
                "text": repr(step.conclusion)[:1200],
                "position": reference.publication_position,
            })
        output[locator] = {"count": len(entries), "steps": entries[:16]}
    return output


def expansion_inventory(goal: object, provider: object, bridge: object) -> dict:
    """Observe first-level proposals without treating a proposed premise as known."""
    from proof import ProofRule

    options = provider(goal)
    if not isinstance(options, tuple):
        raise TypeError("provider must return a tuple")
    counter = Counter()
    details = []
    for option in options:
        name = str(getattr(option.rule, "name", type(option.rule).__name__))
        counter[name] += 1
        if len(details) >= 16:
            continue
        children = []
        for child in option.subgoals[:10]:
            cited_matches = tuple(
                link.assertion_id for link in bridge.proof_links
                if link.step is not None
                and link.step.rule is ProofRule.GIVEN
                and not link.step.premises
                and link.step.conclusion == child
            )
            children.append({
                "type": type(child).__name__,
                "goal": repr(child)[:1200],
                "exact_screened_given_ids": cited_matches,
            })
        details.append({"rule": name, "subgoals": children})
    return {"count": len(options), "rules": dict(sorted(counter.items())), "examples": details}


def requirement_assessment(inventory: dict, *, double_present: bool, hopf_present: bool,
                           cyclic_expansions: int) -> list[dict]:
    """List known evidence and unproved obligations without asserting impossibility."""
    evidence = (
        ("prop22_hopf_composition", "Proposition 2.2",
         "H(nu' o eta_6)=eta_5^2 の型付き導出"),
        ("prop53_eta_squared", "Proposition 5.3",
         "pi_7^5 および pi_5^3 の位数2・生成性の特殊化"),
        ("toda52_pi52", "(5.2)",
         "pi_5^2 の群構造と生成元 eta_2^3 の輸送"),
        ("ehp_exact_window", "Proposition 4.2 (4.4)",
         "pi_7^3→pi_7^5→pi_5^2→pi_6^3→pi_6^5 の完全性"),
    )
    rows = [{
        "key": key,
        "screened_fixed_given_count": inventory[locator]["count"],
        "obligation": obligation,
        "certified_as_completed_inference": False,
    } for key, locator, obligation in evidence]
    rows.extend((
        {"key": "nu_prime_hopf", "screened_fixed_given_count": int(hopf_present),
         "obligation": "H(nu')=eta_5 と H の全射性を区別", "certified_as_completed_inference": False},
        {"key": "nu_prime_double", "screened_fixed_given_count": int(double_present),
         "obligation": "2nu'=eta_3 eta_4 eta_5 と E(eta_2^3) を同一視する証明",
         "certified_as_completed_inference": False},
        {"key": "finite_extension_structure", "screened_fixed_given_count": 0,
         "obligation": "E の単射・H の全射・完全性と Z/2×Z/2 から |pi_6^3|=4 を導く",
         "certified_as_completed_inference": False},
        {"key": "order_and_generator", "screened_fixed_given_count": 0,
         "obligation": "非零の 2nu' と位数4の群から位数4・生成性を導く",
         "certified_as_completed_inference": False},
    ))
    if cyclic_expansions:
        rows[-1]["note"] = "既存の巡回群構造への候補は存在するが証明ではない"
    return rows


def run(root: Path, *, dry_run: bool, search: bool) -> int:
    """Audit the current local worktree without modifying repository files."""
    before = snapshot(root)
    print("PHASE171_R2F_BRANCH=" + before["branch"], flush=True)
    print("PHASE171_R2F_HEAD=" + before["head"], flush=True)
    print("PHASE171_R2F_TRACKED_DIFF_SHA256=" + before["tracked_diff_sha256"], flush=True)
    if dry_run:
        if snapshot(root) != before:
            raise RuntimeError("worktree changed during DryRun")
        print("PHASE171_R2F_DRY_RUN=PASS", flush=True)
        print("PHASE171_R2F_RESULT=PASS_AUDIT_ONLY", flush=True)
        return 0

    from expression import Multiple
    from homotopy_groups import FiniteCyclicGroup
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase166_r3c_publication_order import precedes_citing_assertion
    from proof import ProofRule

    complete = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(complete, n=3, k=3)
    if len(candidates) != 1:
        raise RuntimeError("expected one typed pi_6^3 DB goal")
    goal = candidates[0]
    if not isinstance(goal.rhs, FiniteCyclicGroup) or goal.rhs.order != 4:
        raise RuntimeError("unexpected pi_6^3 target group")
    citing = resolve_specialized_goal_citing_id(complete, goal)
    if citing != EXPECTED_TARGET:
        raise RuntimeError("unexpected source identity for pi_6^3 goal: " + repr(citing))
    screened = screen_shared_proof_context(
        complete, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    doubles = matching_cited_steps(screened, EXPECTED_DOUBLE_SUFFIX)
    hopfs = matching_cited_steps(screened, EXPECTED_HOPF_SUFFIX)
    if len(doubles) != 1 or len(hopfs) != 1:
        raise RuntimeError("R2E double and R3H Hopf must each be uniquely screened GIVENs")
    double_assertion = screened.registry.assertion(doubles[0][0])
    double_reference = screened.registry.reference(double_assertion.reference_id)
    if (double_reference.locator != "(5.3)"
            or double_reference.publication_position != 8100
            or not precedes_citing_assertion(screened, doubles[0][0], citing)):
        raise RuntimeError("R2E source does not precede the target at the reviewed position")
    relation = doubles[0][1]
    if not isinstance(relation.lhs, Multiple) or relation.lhs.coefficient != 2:
        raise RuntimeError("R2E conclusion is not a typed 2*generator equality")
    if any(link.step is not None and link.step.conclusion == goal
           for link in screened.proof_links):
        raise RuntimeError("forbidden direct target proof link was found")

    cyclic = CyclicStructureStatement(goal.lhs, goal.rhs.generator, 4)
    provider = shared_expansion_provider(screened, proof_target=goal)
    root_frontier = expansion_inventory(goal, provider, screened)
    cyclic_frontier = expansion_inventory(cyclic, provider, screened)
    sources = source_inventory(screened)
    assessment = requirement_assessment(
        sources, double_present=True, hopf_present=True,
        cyclic_expansions=cyclic_frontier["count"],
    )
    runtime_search = None
    if search:
        from phase165_r55_nk_only_goal import search_group_from_registered_goal
        result = search_group_from_registered_goal(n=3, k=3, bridge=complete)
        runtime_search = {
            "status": str(result.status),
            "conclusion_is_goal": result.conclusion == goal,
            "inference_step_count": sum(step.rule is ProofRule.INFERENCE
                                        for step in result.proven_steps),
            "given_step_count": sum(step.rule is ProofRule.GIVEN
                                    for step in result.proven_steps),
            "open_goals": [repr(x)[:1000] for x in result.open_goals[:16]],
        }
    report = {
        "phase": "171 R2F", "mode": "READ_ONLY_TYPED_GAP", "read_only": True,
        "git_before": before,
        "target": repr(goal), "citing_id": citing,
        "double_given_id": doubles[0][0], "hopf_given_id": hopfs[0][0],
        "double_publication_position": double_reference.publication_position,
        "double_precedes_target": True,
        "double_relation": repr(relation),
        "db_generator": repr(goal.rhs.generator),
        "nu_prime_from_double": repr(relation.lhs.expression),
        "generator_typed_equal": goal.rhs.generator == relation.lhs.expression,
        "generator_differences": typed_differences(goal.rhs.generator, relation.lhs.expression),
        "sources": sources,
        "root_expansions": root_frontier, "cyclic_expansions": cyclic_frontier,
        "remaining_obligations": assessment,
        "runtime_search": runtime_search,
        "root_proof_certified_by_this_audit": False,
    }
    if snapshot(root) != before:
        raise RuntimeError("worktree changed during source inspection")
    report["git_after_identical"] = True
    report_dir = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    report_dir = report_dir / ("phase171_r2f_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    report_dir.mkdir(parents=True, exist_ok=False)
    report_path = report_dir / "audit.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PHASE171_R2F_DOUBLE_SOURCE=PASS", flush=True)
    print("PHASE171_R2F_HOPF_SOURCE=PASS", flush=True)
    print("PHASE171_R2F_DB_GENERATOR_TYPED_EQUAL=" + str(report["generator_typed_equal"]), flush=True)
    print("PHASE171_R2F_ROOT_RULES=" + json.dumps(root_frontier["rules"], ensure_ascii=False), flush=True)
    print("PHASE171_R2F_CYCLIC_RULES=" + json.dumps(cyclic_frontier["rules"], ensure_ascii=False), flush=True)
    for row in assessment:
        print("PHASE171_R2F_OBLIGATION=" + json.dumps(row, ensure_ascii=False), flush=True)
    if runtime_search is not None:
        print("PHASE171_R2F_SEARCH=" + json.dumps(runtime_search, ensure_ascii=False), flush=True)
    print("PHASE171_R2F_REPORT=" + str(report_path), flush=True)
    print("PHASE171_R2F_WORKTREE_UNCHANGED=True", flush=True)
    print("PHASE171_R2F_RESULT=PASS_AUDIT_ONLY", flush=True)
    return 0


def main() -> int:
    """Run the audit in dry-run, frontier, or optional existing-search mode."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--search", action="store_true")
    args = parser.parse_args()
    try:
        return run(args.root.resolve(), dry_run=args.dry_run, search=args.search)
    except Exception as exc:
        print("PHASE171_R2F_ERROR=" + f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        print(traceback.format_exc()[-3000:], file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
