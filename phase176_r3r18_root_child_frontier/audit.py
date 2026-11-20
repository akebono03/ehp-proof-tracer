"""Phase 176 R3R18: read-only root-candidate child frontier inventory."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r18_root_child_frontier"


def git(*args: str) -> str:
    p = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {p.stderr.strip()}")
    return p.stdout.strip()


def source_guard() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_ROOT")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if git("status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("TRACKED_FILES_DIRTY")
    needed = {
        "phase165_r52_r9_shared_math.py": ("def build_shared_typed_bridge(", "def shared_expansion_provider("),
        "phase165_r55_nk_only_goal.py": ("def search_group_from_registered_goal(",),
        "phase165_r52_r2_search_adapter.py": ("def search_registered_partial_proof(",),
        "phase165_r12_r5_structure_bridge.py": ("finite cyclic structure gives group relation",),
        "phase176_r3r10_right_zero_transport_isolated/rule.py": ("def expand_right_zero_transport(",),
    }
    for name, tokens in needed.items():
        path = ROOT / name
        if not path.is_file():
            raise RuntimeError("MISSING_SOURCE: " + name)
        text = path.read_text(encoding="utf-8-sig")
        if not all(token in text for token in tokens):
            raise RuntimeError("SOURCE_DRIFT: " + name)
    return {"head": git("rev-parse", "HEAD"), "checked_files": len(needed)}


def summarize(options, limit=40):
    items = tuple(options)
    return {"count": len(items), "truncated": len(items) > limit,
            "items": [{"rule": str(getattr(o.rule, "name", "UNKNOWN")),
                       "subgoal_count": len(o.subgoals),
                       "subgoals": [repr(g) for g in o.subgoals]}
                      for o in items[:limit]]}


def observe():
    from homotopy_groups import TodaPrimaryGroup
    from proof import Relation
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal

    result = search_group_from_registered_goal(n=3, k=5)
    goals = tuple(g for g in result.open_goals
                  if isinstance(g, Relation) and g.lhs == TodaPrimaryGroup(8, 3))
    if not goals:
        raise RuntimeError("EXPECTED_VISIBLE_TYPED_ROOT")
    root = goals[0]
    screened = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    provider = shared_expansion_provider(screened, proof_target=root)
    root_options = tuple(provider(root))
    children = []
    for i, option in enumerate(root_options):
        for j, child in enumerate(option.subgoals):
            children.append({"root_option": i, "child_index": j,
                             "goal": repr(child), "kind": type(child).__name__,
                             "candidate_details": summarize(provider(child), 16),
                             "screened_direct_given_count": sum(1 for link in screened.proof_links
                                 if link.step is not None and type(link.step.conclusion) is type(child)
                                 and link.step.conclusion == child)})
    return {"search_status": result.status.value,
            "open_goals": len(result.open_goals),
            "root_goal": repr(root), "root_options": summarize(root_options),
            "child_frontier": children,
            "recursive_public_root_complete": False,
            "note": "Candidate counts are not proof counts; child candidate discovery does not certify recursive solvability."}


def output_path():
    folder = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "report.json"


def execute(dry_run: bool) -> int:
    report = {"phase": "176_R3R18", "dry_run": dry_run,
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "gate": "FAIL_R3R18", "full_pytest": "NOT_RUN",
              "production_modified": False, "new_given": 0}
    try:
        report["preflight"] = source_guard()
        if not dry_run:
            report["observed"] = observe()
        report["gate"] = "PASS_R3R18_READ_ONLY_DRYRUN" if dry_run else "PASS_R3R18_ROOT_CHILD_FRONTIER_RECORDED"
    except Exception as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
    path = output_path()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R18_GATE=" + report["gate"])
    print("PHASE176_R3R18_REPORT=" + str(path))
    if "preflight" in report:
        print("PHASE176_R3R18_HEAD=" + report["preflight"]["head"])
    if "observed" in report:
        row = report["observed"]
        print("PHASE176_R3R18_PUBLIC_STATUS=" + row["search_status"])
        print("PHASE176_R3R18_ROOT_CANDIDATES=" + str(row["root_options"]["count"]))
        for i, item in enumerate(row["root_options"]["items"]):
            print(f"PHASE176_R3R18_ROOT_{i}_RULE=" + item["rule"])
            print(f"PHASE176_R3R18_ROOT_{i}_SUBGOALS=" + repr(item["subgoals"]))
        for row_index, child in enumerate(row["child_frontier"]):
            print(f"PHASE176_R3R18_CHILD_{row_index}_CANDIDATES=" + str(child["candidate_details"]["count"]))
            print(f"PHASE176_R3R18_CHILD_{row_index}_DIRECT_GIVEN=" + str(child["screened_direct_given_count"]))
    if "error" in report:
        print("PHASE176_R3R18_ERROR=" + report["error"])
    print("PHASE176_R3R18_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    return execute(p.parse_args().dry_run)


if __name__ == "__main__":
    sys.exit(main())
