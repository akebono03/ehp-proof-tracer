"""Read-only Phase 175 R4R14R11 preflight, not the final phase gate.

Observe actual current k=4 search states in separate workers. Historical test
failures remain explicitly outstanding; no source guards are bypassed or changed.
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
PACKAGE = "phase175_r4r14r11_closeout_preflight"
MARKER = "R4R14R11_WORKER_JSON="
REVIEWED_ANCESTOR = "e83d5a45f52bf6b755f46e8574de1208247c7ba8"
PAIRS = ((3, 4), (5, 4), (6, 4))
EXPECTED_SOURCE_FILES = (
    "phase165_r52_r9_shared_math.py",
    "phase175_r4r14r9_literature_zero_image/rule.py",
    "phase175_r4r14r9_literature_zero_image/provider.py",
    "phase175_r4r14r6_surjective_zero_codomain/rule.py",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py",
    "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py",
)
KNOWN_LEGACY_FAILURES = (
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_guard.py::test_checkout_protects_real_upstream_sources",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_guard.py::test_wrong_source_sha_is_rejected",
    "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_source_guard.py::test_checked_source_guard_after_install",
    "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_source_guard.py::test_import_and_full_function_emitted_from_actual_file",
)


def git(*arguments: str, check: bool = True) -> tuple[int, str]:
    """Read Git metadata; never fetch, reset, stage, or alter the checkout."""
    result = subprocess.run(
        ("git",) + arguments, cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if check and result.returncode:
        raise RuntimeError("GIT_COMMAND_FAILED: " + " ".join(arguments) + " " + result.stderr.strip())
    return result.returncode, result.stdout.strip()


def classify_checkout(paths: tuple[str, ...]) -> dict[str, object]:
    """Report rather than silently reset tracked pytest caches or source changes."""
    cached = tuple(p for p in paths if p.startswith(".pytest_cache/"))
    source = tuple(p for p in paths if not p.startswith(".pytest_cache/"))
    return {
        "tracked_cache_changes": list(cached),
        "tracked_non_cache_changes": list(source),
        "tracked_cache_cleanup_needed": bool(cached),
        "source_worktree_clean": not source,
    }


def preflight() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")[1]).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current")[1] != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    head = git("rev-parse", "HEAD")[1]
    if git("merge-base", "--is-ancestor", REVIEWED_ANCESTOR, "HEAD", check=False)[0]:
        raise RuntimeError("R4R14R9_REVIEWED_ANCESTOR_MISSING")
    staged = tuple(git("diff", "--cached", "--name-only")[1].splitlines())
    if staged:
        raise RuntimeError("STAGED_CHANGES_REQUIRE_REVIEW: " + repr(staged))
    changes = tuple(git("diff", "--name-only")[1].splitlines())
    tree = classify_checkout(changes)
    if tree["tracked_non_cache_changes"]:
        raise RuntimeError("PRODUCTION_OR_OTHER_TRACKED_CHANGES_REQUIRE_REVIEW: " + repr(tree["tracked_non_cache_changes"]))
    pins = {}
    for path in EXPECTED_SOURCE_FILES:
        if not (ROOT / path).is_file():
            raise RuntimeError("REQUIRED_SOURCE_MISSING: " + path)
        pins[path] = git("rev-parse", "HEAD:" + path)[1]
    untracked = tuple(git("ls-files", "--others", "--exclude-standard")[1].splitlines())
    external_untracked = tuple(p for p in untracked if not p.startswith(PACKAGE + "/"))
    return {
        "head": head,
        "origin_develop_local": git("rev-parse", "--verify", "origin/develop", check=False)[1] or None,
        "source_blobs_at_head": pins,
        "known_historical_guard_tests": list(KNOWN_LEGACY_FAILURES),
        "historical_guard_status": "FOUR_KNOWN_FAILURES_RETAINED_NOT_RERUN",
        "untracked_outside_audit": list(external_untracked),
        **tree,
    }


def observe_one(n: int, k: int) -> dict[str, object]:
    """Run the canonical actual source-first search, never synthesize a result."""
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_partial_proof import ProofSearchStatus
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    result = search_group_from_registered_goal(n=n, k=k)
    status = getattr(result.status, "value", str(result.status))
    zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(n + k, n))
    details = {
        "n": n, "k": k, "status": status,
        "proved_steps": len(result.proven_steps),
        "open_goals": [str(x)[:1300] for x in result.open_goals],
        "conclusion": str(result.conclusion)[:1800] if result.conclusion is not None else None,
        "zero_group_conclusion": result.conclusion == zero,
        "diagnostics": [str(x)[:1600] for x in result.diagnostics],
    }
    if n == 6:
        if (result.status is not ProofSearchStatus.COMPLETE
                or result.conclusion != zero or result.open_goals):
            raise RuntimeError("PI10_6_COMPLETION_REGRESSED")
        from phase175_r4r14r10_complete_proof_audit.audit import audit_live_proof
        tree = audit_live_proof()
        if tree["search_status"] != "complete" or tree["open_goals"]:
            raise RuntimeError("R4R14R10_TREE_REGRESSED")
        details["completed_proof_tree"] = {
            "tree_steps": tree["tree_steps"],
            "given_locators": tree["given_leaf_locators"],
            "literature_fixed_origin": tree["literature_fixed_origin"],
            "literature_step_is_verified_db": tree["literature_step_is_verified_db"],
            "root_rule": tree["root_rule"],
            "zero_image_rule": tree["zero_image_rule"],
        }
    return details


def collect_worker(n: int, k: int, timeout: int) -> dict[str, object]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        result = subprocess.run(
            (sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker", "--n", str(n), "--k", str(k)),
            cwd=ROOT, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"SEARCH_TIMEOUT_{n}_{k}") from exc
    markers = [line[len(MARKER):] for line in result.stdout.splitlines() if line.startswith(MARKER)]
    if result.returncode or len(markers) != 1:
        raise RuntimeError(f"SEARCH_WORKER_FAILED_{n}_{k}: " + result.stderr[-1700:])
    row = json.loads(markers[0])
    if type(row) is not dict or (row.get("n"), row.get("k")) != (n, k):
        raise RuntimeError("SEARCH_WORKER_RESULT_MISMATCH")
    return row


def audit(timeout: int) -> dict[str, object]:
    rows = [collect_worker(n, k, timeout) for n, k in PAIRS]
    by_n = {row["n"]: row for row in rows}
    if by_n[6]["status"] != "complete" or not by_n[6]["zero_group_conclusion"]:
        raise RuntimeError("PI10_6_NOT_COMPLETE")
    unfinished = [row for row in rows if row["status"] != "complete"]
    return {
        "checked_groups": [f"pi_{n+k}^{n}" for n, k in PAIRS],
        "rows": rows,
        "observed_incomplete": [f"pi_{r['n']+r['k']}^{r['n']}" for r in unfinished],
        "phase175_final_gate_ready": False,
        "phase175_final_gate_reason": "Other k=4 groups and historical source guards require closeout policy review",
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changed_by_audit": False,
        "full_pytest": "NOT_RUN",
    }


def run(dry_run: bool, timeout: int) -> int:
    report = {
        "phase": "175_R4R14R11", "dry_run": dry_run,
        "gate": "FAIL_R4R14R11_PREFLIGHT", "full_pytest": "NOT_RUN",
    }
    try:
        report["preflight"] = preflight()
        if not dry_run:
            report["actual_search"] = audit(timeout)
        report["gate"] = (
            "PASS_R4R14R11_READ_ONLY_DRYRUN" if dry_run
            else "PASS_R4R14R11_CLOSEOUT_PREFLIGHT_WITH_OPEN_POLICY"
        )
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-7000:]
    path = Path(os.environ.get("TEMP") or tempfile.gettempdir()) / "EHP_Phase175_R4R14R11_closeout_preflight.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print("R4R14R11_GATE=" + str(report["gate"]))
    print("R4R14R11_REPORT=" + str(path))
    print("R4R14R11_HEAD=" + str(report.get("preflight", {}).get("head", "UNKNOWN")))
    if "actual_search" in report:
        for row in report["actual_search"]["rows"]:
            print("R4R14R11_GROUP=" + f"({row['n']},{row['k']})" + " STATUS=" + row["status"] + " OPEN=" + str(len(row["open_goals"])))
        print("R4R14R11_PHASE_FINAL_GATE=NOT_RUN")
    if "error" in report:
        print("R4R14R11_ERROR=" + str(report["error"]))
        print("(END)")
        return 1
    print("R4R14R11_NEW_GIVEN=0")
    print("R4R14R11_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--k", type=int, default=4)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    args = parser.parse_args()
    if args.worker:
        try:
            print(MARKER + json.dumps(observe_one(args.n, args.k), ensure_ascii=False, default=str))
            return 0
        except Exception:
            traceback.print_exc()
            return 2
    if args.timeout_seconds < 30:
        parser.error("timeout-seconds must be >= 30")
    return run(args.dry_run, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
