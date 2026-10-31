"""Phase 171 closeout R1: read-only worktree/content audit and focused tests.

No repository files, mathematical sources, or proof records are modified.
The JSON report is written outside the worktree under LOCALAPPDATA.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

REVIEWED_GITHUB_HEAD = "e814ec939652807d464fd76051d34a9da40328f8"
REVIEWED_BLOBS = {
    "phase168_r3_5_model_renderer.py": "94996b403f1c01f81319824565db422463714f02",
    "phase171_r20r12_verified_cyclic_narrative/projection.py": "73babd53daf6ec088e12b723a905ba40523f8120",
    "phase171_r20r13_eta_sentence_layout/projection.py": "4c1ef57ed0a20d551ae24c80d4b7ddbbb7df9c31",
    "phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py": "881d5a5cdc77220be42615236ed99ff3ec6ee164",
}
HANDOFF_TRACKED = {
    "phase171_r20r13_eta_sentence_layout/output/audit.json",
    "phase171_r20r13_eta_sentence_layout/output/web_narrative.md",
    "phase171_r20r13_eta_sentence_layout/projection.py",
}
HANDOFF_UNTRACKED_DIRS = {
    "phase171_r20r13r2_multiple_blank_eta_merge",
    "phase171_r20r13r3_content_guard_fix",
    "phase171_r20r13r4_test_count_fix",
    "phase171_closeout_r1_preflight_audit",
}
FOCUSED_TESTS = (
    "tests/test_phase167_r2_shared_reference.py",
    "tests/test_phase167_r2_unified_reference.py",
    "tests/test_phase167_r3_generic_resolver.py",
    "tests/test_phase168_r3_4_link_bridge.py",
    "phase169_r10a2_unified_one_stem/tests/test_r10a2_one_stem_projection.py",
    "phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py",
    "phase169_r4c_pi64_suspension_iso/tests/test_r4c_pi64_suspension_iso.py",
    "phase169_r4d_pi64_narrative_audit/tests/test_r4d_narrative_audit.py",
    "phase170_r3_r7_toda52_ordered_db_transport/tests/test_ordered_db_toda52.py",
    "phase171_r20r2_first_successful_search/tests/test_first_successful_search.py",
    "phase171_r20r11_verified_prior_hopf_surjectivity/tests/test_r20r11_verified_prior.py",
    "phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py",
    "phase171_r20r12r2_unindexed_nu_projection_fix/tests/test_correction.py",
    "phase171_r20r13_eta_sentence_layout/tests/test_projection.py",
    "phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py",
    "phase171_r20r13r3_content_guard_fix/tests/test_head_content_guard.py",
    "phase171_r20r13r4_test_count_fix/tests/test_install.py",
)


def command(root: Path, args: list[str], *, timeout: int = 30) -> dict[str, object]:
    try:
        result = subprocess.run(
            args, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", timeout=timeout,
            check=False,
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"returncode": -1, "stdout": "", "stderr": str(error)}


def git(root: Path, *args: str) -> dict[str, object]:
    return command(root, ["git", "-c", "core.quotePath=false", *args])


def status_snapshot(root: Path) -> dict[str, object]:
    tracked = git(root, "status", "--porcelain=v1", "--untracked-files=no")
    untracked = git(root, "ls-files", "--others", "--exclude-standard")
    changed_paths = [row[3:] for row in str(tracked["stdout"]).splitlines() if len(row) > 3]
    unexpected = sorted(set(changed_paths).difference(HANDOFF_TRACKED))
    other_untracked = sorted({
        path.split("/", 1)[0] for path in str(untracked["stdout"]).splitlines()
        if path.split("/", 1)[0] not in HANDOFF_UNTRACKED_DIRS
    })
    return {
        "tracked": tracked, "untracked_count": len(str(untracked["stdout"]).splitlines())
        if untracked["stdout"] else 0,
        "known_handoff_untracked_dirs": sorted({
            path.split("/", 1)[0] for path in str(untracked["stdout"]).splitlines()
            if path.split("/", 1)[0] in HANDOFF_UNTRACKED_DIRS
        }),
        "other_untracked_top_level": other_untracked,
        "unexpected_tracked_paths": unexpected,
    }


def review_blobs(root: Path) -> dict[str, object]:
    rows = {}
    for path, expected in REVIEWED_BLOBS.items():
        target = root / path
        actual = git(root, "hash-object", "--", path) if target.is_file() else {
            "returncode": 1, "stdout": "", "stderr": "missing file"
        }
        rows[path] = {
            "expected_github_blob_sha": expected,
            "local_blob_sha": actual["stdout"],
            "match": actual["returncode"] == 0 and actual["stdout"] == expected,
            "error": actual["stderr"],
        }
    return rows


def external_report_dir() -> Path:
    local = os.environ.get("LOCALAPPDATA")
    home = Path(local) if local else Path.home()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = home / "EHPProofTracerRecovery" / f"phase171_closeout_r1_{stamp}"
    path.mkdir(parents=True, exist_ok=False)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--run-focused", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / ".git").exists():
        print("PHASE171_CLOSEOUT_R1_ERROR=not_a_git_worktree", flush=True)
        return 2

    before = status_snapshot(root)
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    remote = git(root, "ls-remote", "origin", "refs/heads/develop")
    remote_sha = str(remote["stdout"]).split()[0] if remote["returncode"] == 0 and remote["stdout"] else None
    blobs = review_blobs(root)
    missing_tests = [p for p in FOCUSED_TESTS if not (root / p).is_file()]
    guard_ok = (branch["returncode"] == 0 and branch["stdout"] == "develop"
                and head["returncode"] == 0
                and not before["unexpected_tracked_paths"]
                and all(row["match"] for row in blobs.values())
                and not missing_tests)
    print("PHASE171_CLOSEOUT_R1_BRANCH=" + str(branch["stdout"]), flush=True)
    print("PHASE171_CLOSEOUT_R1_LOCAL_HEAD=" + str(head["stdout"]), flush=True)
    print("PHASE171_CLOSEOUT_R1_REMOTE_HEAD=" + str(remote_sha), flush=True)
    print("PHASE171_CLOSEOUT_R1_REVIEWED_REMOTE_HEAD=" + REVIEWED_GITHUB_HEAD, flush=True)
    print("PHASE171_CLOSEOUT_R1_REMOTE_QUERY=" + ("PASS" if remote_sha else "UNAVAILABLE"), flush=True)
    print("PHASE171_CLOSEOUT_R1_TRACKED_DIFF=" + str(before["tracked"]["stdout"]), flush=True)
    print("PHASE171_CLOSEOUT_R1_UNEXPECTED_TRACKED=" + str(before["unexpected_tracked_paths"]), flush=True)
    print("PHASE171_CLOSEOUT_R1_KNOWN_UNTRACKED=" + str(before["known_handoff_untracked_dirs"]), flush=True)
    for path, row in blobs.items():
        print("PHASE171_CLOSEOUT_R1_CONTENT=" + ("MATCH " if row["match"] else "DIFF ") + path, flush=True)
    print("PHASE171_CLOSEOUT_R1_FOCUSED_MANIFEST=" + str(len(FOCUSED_TESTS)), flush=True)
    print("PHASE171_CLOSEOUT_R1_FOCUSED_READY=" + str(guard_ok), flush=True)

    report: dict[str, object] = {
        "phase": "171_CLOSEOUT_R1", "mode": "READ_ONLY_PREFLIGHT",
        "reviewed_github_head": REVIEWED_GITHUB_HEAD,
        "local_head": head, "remote_query": remote,
        "remote_head": remote_sha,
        "remote_matches_reviewed": remote_sha == REVIEWED_GITHUB_HEAD,
        "branch": branch, "before": before, "reviewed_content": blobs,
        "focused_test_manifest": list(FOCUSED_TESTS), "missing_tests": missing_tests,
        "focused_ready": guard_ok, "full_pytest_executed": False,
        "proof_tree_modified": False, "production_files_modified_by_audit": False,
    }
    report_path = external_report_dir() / "audit.json"
    exit_code = 0
    if args.run_focused:
        if not guard_ok:
            print("PHASE171_CLOSEOUT_R1_FOCUSED=SKIPPED_PREFLIGHT_BLOCKED", flush=True)
            exit_code = 2
        else:
            env = os.environ.copy()
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            env["PYTHONUTF8"] = "1"
            pytest_args = [sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
                           "--disable-warnings", "-p", "no:cacheprovider", *FOCUSED_TESTS]
            tested = subprocess.run(pytest_args, cwd=root, env=env, text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    encoding="utf-8", errors="replace", check=False)
            print(tested.stdout, end="\n", flush=True)
            report["focused_test_command"] = pytest_args
            report["focused_test_output"] = tested.stdout
            report["focused_test_exit_code"] = tested.returncode
            exit_code = tested.returncode
    after = status_snapshot(root)
    report["after"] = after
    report["tracked_unchanged_by_audit"] = before["tracked"] == after["tracked"]
    if not report["tracked_unchanged_by_audit"]:
        exit_code = 3
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PHASE171_CLOSEOUT_R1_REPORT=" + str(report_path), flush=True)
    print("PHASE171_CLOSEOUT_R1_TRACKED_UNCHANGED=" + str(report["tracked_unchanged_by_audit"]), flush=True)
    result = ("PASS_PREFLIGHT" if guard_ok else "AUDIT_ONLY_BLOCKERS_FOUND") if not args.run_focused else (
        "PASS_FOCUSED" if exit_code == 0 else "BLOCKED_OR_FAILED"
    )
    print("PHASE171_CLOSEOUT_R1_RESULT=" + result, flush=True)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
