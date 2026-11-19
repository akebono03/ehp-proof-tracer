"""Phase 175 R13R3 conditional public wiring with fail-closed evidence audit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase175_r4r12r13r3_public_delta_e_bridge import installer

PACKAGE = "phase175_r4r12r13r3_public_delta_e_bridge"


def git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode:
        raise RuntimeError("R13R3_GIT_ERROR: " + " ".join(args) + " " + process.stderr.strip())
    return process.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R13R3_WRONG_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R13R3_WRONG_BRANCH")
    dirty = set(git(root, "diff", "--name-only").splitlines())
    dirty.update(git(root, "diff", "--cached", "--name-only").splitlines())
    if dirty - {".pytest_cache/v/cache/nodeids", str(installer.TARGET)}:
        raise RuntimeError("R13R3_UNREVIEWED_TRACKED_CHANGES: " + repr(sorted(dirty)))
    if str(installer.TARGET) in dirty:
        _, _, _, change = installer.plan(root)
        if change:
            raise RuntimeError("R13R3_PREEXISTING_SHARED_PROVIDER_DIRTY")
    return {"head": git(root, "rev-parse", "HEAD"), "dirty": sorted(dirty)}


def inspect() -> dict[str, object]:
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
    from phase175_r4r12r13r3_public_delta_e_bridge.provider import (
        build_public_delta_e_provider, screened_toda58_available,
    )
    bridge = build_shared_typed_bridge()
    has_citation = screened_toda58_available(bridge)
    provider = build_public_delta_e_provider(bridge)
    delta = MapInjective(canonical_toda58().map)
    emap = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 5)))
    delta_branches = provider(delta)
    e_branches = provider(emap)
    return {
        "toda58_cited_given_present": has_citation,
        "delta_injective_candidates": len(delta_branches),
        "delta_input_goal_types": [type(x).__name__ for branch in delta_branches for x in branch.subgoals],
        "e_surjective_candidates": len(e_branches),
        "e_input_goal_types": [type(x).__name__ for branch in e_branches for x in branch.subgoals],
        "parent_proofs_dispatched": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "proof_complete": False,
    }


def run(root: Path, *, dry_run: bool) -> int:
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {"phase": "175-R4R12R13R3", "dry_run": dry_run,
        "gate": "FAIL_R13R3", "full_pytest_executed": False}
    try:
        report["preflight"] = preflight(root)
        report["installation"] = installer.install(root, dry_run=dry_run, output=output)
        report["frontier"] = inspect()
        if report["frontier"]["e_surjective_candidates"] != 1:
            raise RuntimeError("R13R3_MISSING_E_SURJECTIVE_RULE")
        if report["frontier"]["delta_injective_candidates"] != 1:
            report["gate"] = "PASS_R13R3_E_CONNECTED_DELTA_TYPED_MATCH_PENDING"
        else:
            report["gate"] = "PASS_R13R3_CONDITIONAL_PROVIDER_NOT_COMPLETE"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    filename = output / ("dry_run_report.json" if dry_run else "report.json")
    filename.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R13R3_GATE=" + str(report["gate"]))
    print("PHASE175_R13R3_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    front = report.get("frontier", {})
    print("PHASE175_R13R3_TODA58_CITED=" + str(front.get("toda58_cited_given_present", "NOT_CHECKED")))
    print("PHASE175_R13R3_DELTA_CANDIDATES=" + str(front.get("delta_injective_candidates", "NOT_CHECKED")))
    print("PHASE175_R13R3_E_CANDIDATES=" + str(front.get("e_surjective_candidates", "NOT_CHECKED")))
    print("PHASE175_R13R3_NEW_GIVEN=0")
    print("PHASE175_R13R3_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R13R3_REPORT=" + str(filename))
    if "error" in report:
        print("PHASE175_R13R3_ERROR=" + report["error"])
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    options = parser.parse_args()
    return run(options.root.resolve(), dry_run=options.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
