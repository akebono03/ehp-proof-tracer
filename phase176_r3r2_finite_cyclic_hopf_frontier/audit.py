"""Phase 176 R3R2: read-only finite-cyclic Hopf frontier audit.

No source assertions, mathematical rules, or proof steps are created here.
Every proposal is labelled as a proposal, not verified evidence.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r2_finite_cyclic_hopf_frontier"
REVIEWED_HEAD = "b837ba9819a5a1b166f13739b160b4880b4599e2"
MARKER = "PHASE176_R3R2_WORKER_JSON="
REQUIRED_FILES = (
    "phase176_r3_n3_rule_sufficiency_audit/audit.py",
    "phase165_r55_nk_only_goal.py",
    "phase165_r52_r9_shared_math.py",
    "phase165_r14_r6_generic_iso.py",
    "phase165_r14_r9_ehp_exactness.py",
    "phase165_r12_r2_quotient_rules.py",
    "phase165_r12_r12_ehp_consequences.py",
    "phase174_r3_r7_r56_cyclic_generator_bridge/rule.py",
    "phase171_r2h_prop22_cited_hopf/source.py",
    "sources/toda/Toda_05_2.tex",
    "sources/toda/Toda_02_2.tex",
)


def git(*args: str, check: bool = True) -> tuple[int, str]:
    result = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", check=False)
    if check and result.returncode:
        raise RuntimeError("GIT_READ_ERROR " + " ".join(args) + " " + result.stderr.strip())
    return result.returncode, result.stdout.strip()


def preflight() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")[1]).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current")[1] != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if git("merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD", check=False)[0]:
        raise RuntimeError("REVIEWED_R3_HEAD_NOT_ANCESTOR")
    if git("status", "--porcelain", "--untracked-files=no")[1]:
        raise RuntimeError("TRACKED_CHANGES_REQUIRE_REVIEW")
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    if missing:
        raise RuntimeError("REVIEWED_FILES_MISSING " + repr(missing))
    from phase176_r3_n3_rule_sufficiency_audit.audit import check_source_anchors
    anchors = check_source_anchors(ROOT)
    if any(not row["present"] for row in anchors.values()):
        raise RuntimeError("R3_SOURCE_ANCHOR_REGRESSION")
    return {
        "head": git("rev-parse", "HEAD")[1],
        "origin_develop": git("rev-parse", "--verify", "origin/develop", check=False)[1] or None,
        "reviewed_r3_head_is_ancestor": True,
        "source_anchors": anchors,
        "historical_source_guards": "FOUR_KNOWN_FAILURES_NOT_PASSING",
        "full_pytest": "NOT_RUN",
    }


def describe(statement: object) -> dict[str, str]:
    return {"type": type(statement).__module__ + "." + type(statement).__name__,
            "repr": repr(statement)[:2400]}


def proposal_summary(goal: object, provider: object) -> dict[str, object]:
    try:
        proposals = tuple(provider(goal))
    except Exception as exc:
        return {"status": "ERROR", "error": type(exc).__name__ + ": " + str(exc)}
    return {"status": "INSPECTED_NOT_PROVED", "count": len(proposals),
            "rules": [getattr(item.rule, "name", str(type(item.rule))) for item in proposals[:16]],
            "subgoals": [[describe(x) for x in item.subgoals] for item in proposals[:16]],
            "truncated": len(proposals) > 16}


def inspect_expected_hopf_geometry() -> dict[str, object]:
    from homotopy_groups import TodaPrimaryGroup, TodaHopfInvariantMap, TodaDeltaMap
    from phase165_r14_r6_generic_iso import MapInjective, GeneratorImage
    from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
    from homotopy_groups import TodaEHPExactnessWindow
    from map_facts import EHP_H_MAP, EHP_DELTA_MAP
    from toda_rules import TodaProp42ExactnessStatement
    from phase165_r12_r11_prop42_unified import prop42_exactness_indices

    a = TodaPrimaryGroup(8, 3)
    b = TodaPrimaryGroup(8, 5)
    c = TodaPrimaryGroup(6, 2)
    hopf = TodaHopfInvariantMap(a, b)
    delta = TodaDeltaMap(b, c)
    exact_window = TodaEHPExactnessWindow(a, b, c, EHP_H_MAP, EHP_DELTA_MAP)
    bridge = build_shared_typed_bridge()
    provider = shared_expansion_provider(bridge, proof_target=None)
    inject = MapInjective(hopf)
    equality = EHPImageEqualsKernelStatement(exact_window)
    return {
        "hopf": describe(hopf), "delta": describe(delta),
        "ehp_window_indices_valid": prop42_exactness_indices(TodaProp42ExactnessStatement(exact_window)) is not None,
        "hopf_injective_generic": proposal_summary(inject, expand_generic_ehp_hopf_goal),
        "hopf_injective_shared": proposal_summary(inject, provider),
        "hopf_image_equals_delta_kernel_shared": proposal_summary(equality, provider),
        "generator_image_type_available": GeneratorImage.__module__ + "." + GeneratorImage.__name__,
        "registry_fixed_sources": sum(a.origin.value == "fixed_statement" for a in bridge.registry._assertions.values()),
        "matched_source_locators": sorted({
            bridge.registry._references[a.reference_id].locator
            for a in bridge.registry._assertions.values()
            if any(t in bridge.registry._references[a.reference_id].locator.lower()
                   for t in ("5.7", "5.5", "5.3", "5.6", "5.8", "2.2", "4.2", "4.4"))
        }),
    }


def observe() -> dict[str, object]:
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r14_r6_generic_iso import MapInjective
    from phase174_r3_r7_r56_cyclic_generator_bridge.rule import expand_cyclic_generator_from_hopf
    from proof import Relation, RelationType
    from homotopy_groups import FiniteCyclicGroup

    result = search_group_from_registered_goal(n=3, k=5)
    goals = tuple(result.open_goals)
    cyclic = tuple(g for g in goals if isinstance(g, CyclicStructureStatement))
    if result.status.value != "search_failed" or len(goals) != 3 or len(cyclic) != 1:
        raise RuntimeError("R3_K5_GOAL_DRIFT_REVIEW_REQUIRED: " + repr((result.status, len(goals), len(cyclic))))
    target = cyclic[0]
    if target.group.group_dimension != 8 or target.group.sphere_dimension != 3 or target.order != 2:
        raise RuntimeError("CYCLIC_TARGET_DRIFT")
    bridge = build_shared_typed_bridge()
    provider = shared_expansion_provider(bridge, proof_target=result.open_goals[-1])
    finite_relation = Relation(target.group, FiniteCyclicGroup(target.order, target.generator), RelationType.EQUALITY)
    return {
        "status": result.status.value,
        "open_goal_count": len(goals),
        "root_goals": [describe(g) for g in goals],
        "cyclic_goal": describe(target),
        "cyclic_goal_proposals": proposal_summary(target, provider),
        "finite_relation_proposals": proposal_summary(finite_relation, provider),
        "r56_free_cyclic_rule_for_finite_goal": len(expand_cyclic_generator_from_hopf(finite_relation)),
        "r56_rule_is_not_finite": True,
        "geometry": inspect_expected_hopf_geometry(),
        "recommendation": "AUDIT_TYPES_AND_SOURCE_PREMISES_BEFORE_GENERAL_FINITE_GENERATOR_RULE",
        "proof_complete": False,
        "new_given": 0, "new_rules": 0,
    }


def report_file() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    root.mkdir(parents=True, exist_ok=True)
    return root / "report.json"


def worker(timeout: int) -> dict[str, object]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    try:
        p = subprocess.run((sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"),
                           cwd=ROOT, env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", check=False, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("R3R2_WORKER_TIMEOUT") from exc
    markers = [line[len(MARKER):] for line in p.stdout.splitlines() if line.startswith(MARKER)]
    if p.returncode or len(markers) != 1:
        raise RuntimeError("R3R2_WORKER_FAILED exit=" + str(p.returncode) + " stderr=" + p.stderr[-4500:])
    value = json.loads(markers[0])
    if value.get("proof_complete") is not False:
        raise RuntimeError("AUDIT_NOT_ALLOWED_TO_CLAIM_PROOF")
    return value


def run(dry_run: bool, timeout: int) -> int:
    report: dict[str, object] = {"phase": "176_R3R2", "mode": "READ_ONLY_HOPF_FRONTIER",
                                 "dry_run": dry_run, "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                                 "full_pytest": "NOT_RUN", "new_given": 0, "new_rules": 0,
                                 "gate": "FAIL_R3R2"}
    try:
        report["preflight"] = preflight()
        if not dry_run:
            report["observed"] = worker(timeout)
        report["gate"] = "PASS_R3R2_READ_ONLY_DRYRUN" if dry_run else "PASS_R3R2_FRONTIER_AUDIT"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-8000:]
    path = report_file()
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print("PHASE176_R3R2_GATE=" + report["gate"])
    print("PHASE176_R3R2_REPORT=" + str(path))
    print("PHASE176_R3R2_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    if "observed" in report:
        o = report["observed"]
        print("PHASE176_R3R2_GROUP=(3,5) STATUS=" + o["status"] + " OPEN=" + str(o["open_goal_count"]))
        print("PHASE176_R3R2_CYCLIC_PROPOSALS=" + str(o["cyclic_goal_proposals"].get("count", "ERROR")))
        print("PHASE176_R3R2_HOPF_INJECTIVE_PROPOSALS=" + str(o["geometry"]["hopf_injective_shared"].get("count", "ERROR")))
    if "error" in report:
        print("PHASE176_R3R2_ERROR=" + report["error"])
    print("PHASE176_R3R2_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    if args.worker:
        try:
            print(MARKER + json.dumps(observe(), ensure_ascii=False))
            return 0
        except Exception:
            traceback.print_exc()
            return 1
    return run(args.dry_run, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
