"""Phase 175 R4R14R13: read-only final-gate preflight.

Confirm the five R12 complete documents, six live k=4 group searches,
and the already certified pi_10^6 proof tree. Do not run full pytest,
change an earlier Source Guard, write proof facts, or close the phase.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase175_r4r14r13_final_gate_preflight"
REVIEWED_ANCESTOR = "29a06166390c21a30d7a0bd4144597dd16eb2f56"
MARKER = "R4R14R13_WORKER_JSON="
PAIRS = tuple((n, 4) for n in range(2, 8))
REPORT = "EHP_Phase175_R4R14R13_final_gate_preflight.json"


def git(*arguments: str, check: bool = True) -> tuple[int, str]:
    """Read Git status, refs or object identities without modifying the tree."""
    result = subprocess.run(
        ("git",) + arguments, cwd=ROOT, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if check and result.returncode:
        raise RuntimeError("GIT_FAILED " + " ".join(arguments) + ": " + result.stderr.strip())
    return result.returncode, result.stdout.strip()


def classify_dirty_paths(paths: tuple[str, ...], documents: tuple[str, ...]) -> dict[str, object]:
    """Treat only the R12 document paths and tracked pytest cache as expected."""
    docs = sorted(p for p in paths if p in documents)
    cache = sorted(p for p in paths if p.startswith(".pytest_cache/"))
    unexpected = sorted(p for p in paths if p not in documents and not p.startswith(".pytest_cache/"))
    return {
        "modified_documents": docs,
        "tracked_pytest_cache": cache,
        "unexpected_tracked": unexpected,
        "cache_requires_explicit_cleanup_decision": bool(cache),
    }


def validate_documents(root: Path) -> dict[str, dict[str, object]]:
    """Verify exact R12 full-file outputs and their complete historical sources."""
    from phase175_r4r14r12_closeout_documents.build_documents import (
        DOCUMENT_BLOBS, MARKER as R12_MARKER, render_full,
    )

    output: dict[str, dict[str, object]] = {}
    for name, pinned_blob in DOCUMENT_BLOBS.items():
        before = root / "phase175_r4r14r12_closeout_documents" / "original" / name
        after = root / "phase175_r4r14r12_closeout_documents" / "output" / name
        current = root / name
        if not all(path.is_file() for path in (before, after, current)):
            raise RuntimeError("MISSING_COMPLETE_DOCUMENT_OR_R12_ARCHIVE: " + name)
        original_bytes = before.read_bytes()
        full_bytes = after.read_bytes()
        active_bytes = current.read_bytes()
        baseline = subprocess.run(
            ("git", "show", REVIEWED_ANCESTOR + ":" + name),
            cwd=root, capture_output=True, check=False,
        )
        if baseline.returncode or baseline.stdout != original_bytes:
            raise RuntimeError("R12_ORIGINAL_NOT_REVIEWED_BASELINE: " + name)
        hash_process = subprocess.run(
            ("git", "hash-object", "--stdin"), input=original_bytes,
            cwd=root, capture_output=True, check=False,
        )
        if hash_process.returncode or hash_process.stdout.decode("ascii").strip() != pinned_blob:
            raise RuntimeError("R12_ORIGINAL_GIT_BLOB_MISMATCH: " + name)
        source = original_bytes.decode("utf-8-sig")
        expected = render_full(name, source).encode("utf-8")
        if expected != full_bytes or full_bytes != active_bytes:
            raise RuntimeError("R12_COMPLETE_DOCUMENT_DIFFERS: " + name)
        if active_bytes.count(R12_MARKER.encode("ascii")) != 1:
            raise RuntimeError("R12_DOCUMENT_MARKER_NOT_UNIQUE: " + name)
        if not active_bytes.startswith(source.split("\n", 1)[0].encode("utf-8")):
            raise RuntimeError("R12_DOCUMENT_TITLE_CHANGED: " + name)
        output[name] = {
            "historical_source_git_blob": pinned_blob,
            "original_bytes": len(original_bytes),
            "complete_current_bytes": len(active_bytes),
            "sha256": hashlib.sha256(active_bytes).hexdigest(),
            "r12_full_output_verified": True,
            "history_retained": True,
        }
    if len(output) != 5:
        raise RuntimeError("FIVE_DOCUMENTS_REQUIRED")
    return output


def preflight() -> dict[str, object]:
    """Check current branch, source ancestry, R12 documents, and explicit blockers."""
    from phase175_r4r14r11_closeout_preflight.audit import KNOWN_LEGACY_FAILURES
    from phase175_r4r14r12_closeout_documents.build_documents import DOCUMENT_BLOBS

    if Path(git("rev-parse", "--show-toplevel")[1]).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current")[1] != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    head = git("rev-parse", "HEAD")[1]
    if git("merge-base", "--is-ancestor", REVIEWED_ANCESTOR, "HEAD", check=False)[0]:
        raise RuntimeError("REVIEWED_R12_ANCESTOR_NOT_FOUND")
    staged = git("diff", "--cached", "--name-only")[1].splitlines()
    if staged:
        raise RuntimeError("STAGED_CHANGES_REQUIRE_REVIEW: " + repr(staged))
    changed = tuple(git("diff", "--name-only")[1].splitlines())
    paths = classify_dirty_paths(changed, tuple(DOCUMENT_BLOBS))
    if paths["unexpected_tracked"]:
        raise RuntimeError("UNREVIEWED_TRACKED_CHANGES: " + repr(paths["unexpected_tracked"]))
    if git("diff", "--check", check=False)[0]:
        raise RuntimeError("GIT_DIFF_CHECK_FAILED")
    document_records = validate_documents(ROOT)
    untracked = git("ls-files", "--others", "--exclude-standard")[1].splitlines()
    return {
        "head": head,
        "origin_develop_local": git("rev-parse", "--verify", "origin/develop", check=False)[1] or None,
        "reviewed_ancestor": REVIEWED_ANCESTOR,
        "document_files": document_records,
        "document_count": len(document_records),
        "git_changes": paths,
        "untracked_paths": untracked,
        "historical_source_guard": "FOUR_KNOWN_FAILURES_NOT_RERUN_AND_NOT_PASSING",
        "historical_test_names": list(KNOWN_LEGACY_FAILURES),
        "legacy_guard_policy_resolved": False,
        "full_pytest": "NOT_RUN",
    }


def observe_one(n: int, k: int) -> dict[str, object]:
    """Read the current canonical typed search; no synthetic proof or prior replay."""
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_partial_proof import ProofSearchStatus

    result = search_group_from_registered_goal(n=n, k=k)
    expected_group = TodaPrimaryGroup(n + k, n)
    actual_group = (
        result.conclusion.group if isinstance(result.conclusion, TodaPrimaryGroupZeroStatement)
        else getattr(result.conclusion, "lhs", None)
    )
    root_steps = [step for step in result.proven_steps if step.conclusion == result.conclusion]
    passed = (
        result.status is ProofSearchStatus.COMPLETE
        and result.conclusion is not None
        and actual_group == expected_group
        and not result.open_goals
        and len(root_steps) == 1
    )
    if not passed:
        raise RuntimeError("K4_GROUP_NOT_VERIFIED_COMPLETE: " + repr((n, k, result.status)))
    row = {
        "n": n, "k": k, "status": "complete", "open_goals": 0,
        "proven_steps": len(result.proven_steps),
        "conclusion": str(result.conclusion),
        "root_rule": getattr(root_steps[0].inference_rule, "name", None),
    }
    if n == 6:
        from phase175_r4r14r10_complete_proof_audit.audit import audit_live_proof
        proof = audit_live_proof()
        if (proof["search_status"] != "complete"
                or proof["tree_steps"] != 14
                or proof["open_goals"]
                or proof["literature_step_is_verified_db"]
                or not proof["literature_fixed_origin"]
                or set(proof["given_leaf_locators"]) != {
                    "(5.1)", "(5.9)", "Proposition 4.2 (4.4)", "Proposition 5.8"
                }):
            raise RuntimeError("PI10_6_PROOF_TREE_OR_REFERENCE_REGRESSION")
        row["complete_tree_steps"] = proof["tree_steps"]
        row["complete_tree_locators"] = proof["given_leaf_locators"]
        row["literature_and_db_distinct"] = True
    return row


def collect_worker(n: int, k: int, timeout: int) -> dict[str, object]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        completed = subprocess.run(
            (sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker", "--n", str(n), "--k", str(k)),
            cwd=ROOT, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=False, timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("K4_SEARCH_TIMEOUT: " + str((n, k))) from exc
    markers = [line[len(MARKER):] for line in completed.stdout.splitlines() if line.startswith(MARKER)]
    if completed.returncode or len(markers) != 1:
        raise RuntimeError("K4_SEARCH_WORKER_FAILED " + repr((n, k)) + ": " + completed.stderr[-1600:])
    row = json.loads(markers[0])
    if not isinstance(row, dict) or (row.get("n"), row.get("k")) != (n, k):
        raise RuntimeError("K4_WORKER_RESULT_MISMATCH")
    return row


def audit(timeout: int) -> dict[str, object]:
    rows = [collect_worker(n, k, timeout) for n, k in PAIRS]
    if len(rows) != 6 or any(row["status"] != "complete" or row["open_goals"] != 0 for row in rows):
        raise RuntimeError("SIX_K4_COMPLETED_GROUPS_REQUIRED")
    return {
        "groups": rows, "complete_groups": len(rows),
        "unresolved_groups": 0, "new_given": 0, "new_mathematical_rules": 0,
        "phase175_formally_closed": False,
        "final_gate_requires_full_pytest": True,
        "historical_guard_policy_requires_review": True,
    }


def run(dry_run: bool, timeout: int) -> int:
    report: dict[str, object] = {
        "phase": "175_R4R14R13", "mode": "READ_ONLY_PREFLIGHT", "dry_run": dry_run,
        "gate": "FAIL_R4R14R13", "full_pytest": "NOT_RUN", "phase_closed": False,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    try:
        report["preflight"] = preflight()
        if not dry_run:
            report["observed"] = audit(timeout)
        report["gate"] = (
            "PASS_R4R14R13_DRYRUN" if dry_run
            else "PASS_R4R14R13_FINAL_GATE_PREFLIGHT_WITH_OPEN_LEGACY_POLICY"
        )
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-6500:]
    path = Path(os.environ.get("TEMP") or tempfile.gettempdir()) / REPORT
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print("R4R14R13_GATE=" + report["gate"])
    print("R4R14R13_REPORT=" + str(path))
    print("R4R14R13_HEAD=" + str(report.get("preflight", {}).get("head", "UNKNOWN")))
    if "preflight" in report:
        print("R4R14R13_DOCUMENTS=" + str(report["preflight"]["document_count"]))
        print("R4R14R13_LEGACY_GUARD=" + report["preflight"]["historical_source_guard"])
        print("R4R14R13_TRACKED_CACHE=" + repr(report["preflight"]["git_changes"]["tracked_pytest_cache"]))
    if "observed" in report:
        for row in report["observed"]["groups"]:
            print("R4R14R13_GROUP=" + repr((row["n"], row["k"])) + " STATUS=" + row["status"] + " OPEN=" + str(row["open_goals"]))
    if "error" in report:
        print("R4R14R13_ERROR=" + report["error"])
    print("R4R14R13_FULL_PYTEST=NOT_RUN")
    print("R4R14R13_PHASE_CLOSED=FALSE")
    print("(END)")
    return 1 if "error" in report else 0


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
            print(MARKER + json.dumps(observe_one(args.n, args.k), ensure_ascii=False))
            return 0
        except Exception:
            traceback.print_exc()
            return 2
    if args.timeout_seconds < 30:
        parser.error("timeout must be at least 30 seconds")
    return run(args.dry_run, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
