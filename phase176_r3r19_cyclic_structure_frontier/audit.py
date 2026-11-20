"""Phase 176 R3R19: read-only cyclic-structure frontier for pi_8^3."""
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
PACKAGE = "phase176_r3r19_cyclic_structure_frontier"
MARKER = "PHASE176_R3R19_WORKER_JSON="
REQUIRED_SOURCES = {
    "phase165_r52_r9_shared_math.py": ("def build_shared_typed_bridge(", "def shared_expansion_provider("),
    "phase165_r12_r2_quotient_rules.py": ("class CyclicStructureStatement:",),
    "phase165_r12_r5_structure_bridge.py": ("def finite_cyclic_structure_as_relation_inference_rule(",),
    "phase171_r2j_r4_r9_r9_public_cyclic_structure/source.py": ("def expand_cited_full_order_cyclic_structure(",),
    "phase175_r3_pi73_hopf_lift/rule.py": ("def expand_cited_hopf_lift(",),
    "phase176_r3r10_right_zero_transport_isolated/rule.py": ("def expand_right_zero_transport(",),
    "phase165_r52_r2_search_adapter.py": ("def search_registered_partial_proof(",),
}


def git(*args: str) -> str:
    result = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", check=False)
    if result.returncode:
        raise RuntimeError("GIT_FAILED " + " ".join(args) + " " + result.stderr.strip())
    return result.stdout.strip()


def check_sources(root: Path) -> tuple[str, ...]:
    for name, anchors in REQUIRED_SOURCES.items():
        path = root / name
        if not path.is_file():
            raise RuntimeError("SOURCE_MISSING: " + name)
        content = "".join(path.read_text(encoding="utf-8-sig").split())
        for anchor in anchors:
            if "".join(anchor.split()) not in content:
                raise RuntimeError("SOURCE_ANCHOR_MISSING: " + name)
    return tuple(REQUIRED_SOURCES)


def preflight() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if git("status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("TRACKED_FILES_DIRTY")
    paths = check_sources(ROOT)
    return {"head": git("rev-parse", "HEAD"), "source_count": len(paths),
            "sources": list(paths), "full_pytest": "NOT_RUN"}


def summarize(options: tuple[object, ...]) -> list[dict[str, object]]:
    return [{"rule": str(getattr(option.rule, "name", "UNNAMED")),
             "subgoals": [repr(child) for child in option.subgoals],
             "subgoal_count": len(option.subgoals)} for option in options]


def observe() -> dict[str, object]:
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase171_r2j_r4_r9_r9_public_cyclic_structure.source import expand_cited_full_order_cyclic_structure
    from phase175_r3_pi73_hopf_lift.rule import expand_cited_hopf_lift
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(goals) != 1 or goals[0].lhs != TodaPrimaryGroup(8, 3):
        raise RuntimeError("REGISTERED_ROOT_NOT_UNIQUE")
    target = goals[0]
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target)
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    provider = shared_expansion_provider(screened, proof_target=target)
    root_options = tuple(provider(target))
    cyclic_goals = []
    for option in root_options:
        for child in option.subgoals:
            if isinstance(child, CyclicStructureStatement) and not any(old == child for old in cyclic_goals):
                cyclic_goals.append(child)
    if len(cyclic_goals) != 1:
        raise RuntimeError("EXPECTED_ONE_DISTINCT_CYCLIC_CHILD")
    cyclic = cyclic_goals[0]
    if cyclic.group != TodaPrimaryGroup(8, 3) or cyclic.order != 2:
        raise RuntimeError("CYCLIC_CHILD_TARGET_DRIFT")
    ordinary = tuple(provider(cyclic))
    hopf = tuple(expand_cited_hopf_lift(cyclic, available))
    full_order = tuple(expand_cited_full_order_cyclic_structure(cyclic, available))
    public = search_group_from_registered_goal(n=3, k=5)
    return {
        "target": [3, 5],
        "root_candidate_count": len(root_options),
        "root_candidates": summarize(root_options),
        "distinct_cyclic_children": len(cyclic_goals),
        "cyclic_goal": repr(cyclic),
        "ordinary_cyclic_candidate_count": len(ordinary),
        "ordinary_cyclic_candidates": summarize(ordinary),
        "hopf_lift_candidate_count": len(hopf),
        "hopf_lift_candidates": summarize(hopf),
        "finite_full_order_candidate_count": len(full_order),
        "finite_full_order_candidates": summarize(full_order),
        "screened_given_count": len(available),
        "public_status": public.status.value,
        "public_open_goals": len(public.open_goals),
        "root_proof_complete": False,
        "production_modified": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def worker(timeout: int) -> dict[str, object]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    try:
        proc = subprocess.run((sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"),
                              cwd=ROOT, env=env, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("WORKER_TIMEOUT") from exc
    rows = [line[len(MARKER):] for line in proc.stdout.splitlines() if line.startswith(MARKER)]
    if proc.returncode or len(rows) != 1:
        raise RuntimeError("WORKER_FAILED: " + proc.stderr[-4000:] + proc.stdout[-500:])
    result = json.loads(rows[0])
    if (result.get("new_given") != 0 or result.get("new_mathematical_rules") != 0
            or result.get("root_proof_complete") is not False):
        raise RuntimeError("FALSE_PROOF_CLAIM")
    return result


def report_path() -> Path:
    folder = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "report.json"


def execute(dry_run: bool, timeout: int = 180) -> int:
    report: dict[str, object] = {"phase": "176_R3R19", "dry_run": dry_run,
                                 "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                                 "gate": "FAIL_R3R19", "root_proof_complete": False,
                                 "new_given": 0, "new_mathematical_rules": 0,
                                 "full_pytest": "NOT_RUN"}
    try:
        report["preflight"] = preflight()
        if not dry_run:
            report["observed"] = worker(timeout)
        report["gate"] = ("PASS_R3R19_READ_ONLY_DRYRUN" if dry_run
                          else "PASS_R3R19_CYCLIC_STRUCTURE_FRONTIER_RECORDED")
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-6000:]
    path = report_path()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R19_GATE=" + str(report["gate"]))
    print("PHASE176_R3R19_REPORT=" + str(path))
    print("PHASE176_R3R19_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    if "observed" in report:
        data = report["observed"]
        for key in ("root_candidate_count", "distinct_cyclic_children",
                    "ordinary_cyclic_candidate_count", "hopf_lift_candidate_count",
                    "finite_full_order_candidate_count", "screened_given_count",
                    "public_status", "public_open_goals"):
            print("PHASE176_R3R19_" + key.upper() + "=" + str(data[key]))
        for key in ("hopf_lift_candidates", "finite_full_order_candidates", "ordinary_cyclic_candidates"):
            print("PHASE176_R3R19_" + key.upper() + "=" + json.dumps(data[key], ensure_ascii=False))
    if "error" in report:
        print("PHASE176_R3R19_ERROR=" + str(report["error"]))
    print("PHASE176_R3R19_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if str(report["gate"]).startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    if args.worker:
        try:
            print(MARKER + json.dumps(observe(), ensure_ascii=False))
            return 0
        except Exception:
            traceback.print_exc()
            return 1
    return execute(args.dry_run, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
