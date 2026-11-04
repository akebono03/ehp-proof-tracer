"""Phase 173 end-of-phase gate: source guards and read-only test evidence.

No proof search, rendering, Git index, or repository content is modified here.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


REVIEWED_BASE = "ac9149beaf91eeef382bc816234bd2d895398667"
EXPECTED_BLOBS = {
    "tests/conftest.py": "304c7b40eb1041475fb6bc4519d3ef61fd3275e2",
    "tests/phase155_audit_only_nodeids.txt": "e65284e1e108d4ce0c81b9f1cd1e41140238dc8f",
    "phase168_r3_5_model_renderer.py": "eb34d6fd4783ca943e07de6e6d9756d0e85ff9b8",
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase165_r52_r3_web_adapter.py": "dda215780c0468cf421592aff86c79b1f5482eed",
    "web_group_proof_common.py": "0126fd71c66257fc2f4f498a5357d44a67a55884",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "web_app.py": "6f95663df5cbf028bb16d1f05dca62db2e3fc00e",
    "templates/index.html": "7af2afa40b92b8c1ec3916cf9759516c158b989f",
    "phase173_r4_r15r17r3r5_public_http_gate/tests/test_flask_public_output.py": "cd33d7bb774d05ec8016bdbca2854fe4191c14c7",
    "README.md": "109445340c559cfb2357d363c096cebbdb871168",
    "docs/design.md": "0491c27d8075829ba28151029eb19b119a293eff",
    "docs/development_log.md": "880dc8f9f2ff9408a9b4a61c7daa5d816955064c",
    "docs/roadmap.md": "d1d9661eb39674b156185bf61e74b8ee5fd9e101",
    "docs/proof_records.md": "eb310080fb85a265b474ed4a9c60ee91511cc6cf",
}
ACTIVE_SUITE_COMMAND = (
    "python -B -m pytest -q --tb=short --disable-warnings "
    "-p no:cacheprovider tests"
)


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Call read-only Git commands, leaving the index and work tree intact."""
    result = subprocess.run(
        ("git", "--no-pager", *args), cwd=repo, text=True,
        encoding="utf-8", errors="replace", stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            "Git check failed: " + " ".join(args) + "\n" + result.stderr
        )
    return result


def validate_snapshot(repo: Path) -> dict[str, object]:
    """Verify local/remote HEAD, immutable reviewed blobs, and clean tracked files."""
    repo = repo.resolve(strict=True)
    root = git(repo, "rev-parse", "--show-toplevel").stdout.strip()
    if Path(root).resolve() != repo:
        raise RuntimeError("ZIP must be extracted at repository root")
    branch = git(repo, "branch", "--show-current").stdout.strip()
    if branch != "develop":
        raise RuntimeError(f"Expected develop branch; got {branch!r}")
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    remote = git(repo, "rev-parse", "origin/develop").stdout.strip()
    if head != remote:
        raise RuntimeError(f"Local/remote HEAD differ: {head} != {remote}")
    ancestry = git(repo, "merge-base", "--is-ancestor", REVIEWED_BASE, head, check=False)
    if ancestry.returncode != 0:
        raise RuntimeError("Current HEAD is not a descendant of the reviewed base")
    changed_since_review = git(
        repo, "diff", "--name-only", REVIEWED_BASE, head,
    ).stdout.splitlines()
    unexpected = [
        path for path in changed_since_review
        if not path.startswith("phase173_final_gate/")
    ]
    if unexpected:
        raise RuntimeError(
            "Changes outside this gate were made after source review: "
            + ", ".join(unexpected)
        )
    if git(repo, "diff", "--quiet", check=False).returncode != 0:
        raise RuntimeError("Tracked worktree changes must be reviewed before phase-end gate")
    if git(repo, "diff", "--cached", "--quiet", check=False).returncode != 0:
        raise RuntimeError("Staged changes must be reviewed before phase-end gate")
    blob_checks: dict[str, str] = {}
    for path, expected in EXPECTED_BLOBS.items():
        actual = git(repo, "rev-parse", f"HEAD:{path}").stdout.strip()
        if actual != expected:
            raise RuntimeError(f"Reviewed Git blob changed: {path}: {actual} != {expected}")
        blob_checks[path] = actual
    index_tree = git(repo, "write-tree").stdout.strip()
    return {
        "head": head,
        "remote_head": remote,
        "branch": branch,
        "reviewed_base": REVIEWED_BASE,
        "git_index_tree": index_tree,
        "reviewed_blob_count": len(blob_checks),
        "reviewed_blobs": blob_checks,
    }


def parse_pytest_summary(output: str, exit_code: int) -> tuple[int, str]:
    """Recognize the end-of-run pytest PASS summary, not an earlier progress line."""
    if type(exit_code) is not int:
        raise TypeError("exit code must be an integer")
    matches: list[tuple[int, str]] = []
    for line in output.splitlines():
        if "passed" not in line:
            continue
        count = re.search(r"\b([0-9]+) passed\b", line)
        if count and re.search(r"\bin\s+[0-9]", line):
            matches.append((int(count.group(1)), line.strip()))
    if exit_code != 0:
        raise ValueError(f"active pytest exited with code {exit_code}")
    if not matches or matches[-1][0] <= 0:
        raise ValueError("no valid passed-count summary from active pytest")
    count, summary = matches[-1]
    if re.search(r"\b[1-9][0-9]*\s+(failed|error|errors)\b", summary):
        raise ValueError("active pytest output contains failures or errors")
    return count, summary


def write_report(
    repo: Path, report_file: Path, output_file: Path, error_file: Path,
    pytest_exit_code: int,
) -> dict[str, object]:
    """Persist the one phase-end full-suite outcome outside the repository."""
    snapshot = validate_snapshot(repo)
    if report_file.is_file():
        raise RuntimeError("A phase-end report already exists; do not overwrite it")
    stdout = output_file.read_text(encoding="utf-8", errors="replace")
    stderr = error_file.read_text(encoding="utf-8", errors="replace")
    status = "PASS"
    passed = None
    summary = ""
    failure_reason = None
    try:
        passed, summary = parse_pytest_summary(stdout + "\n" + stderr, pytest_exit_code)
    except (ValueError, TypeError) as exc:
        status = "FAIL"
        failure_reason = str(exc)
    report: dict[str, object] = {
        "phase": 173,
        "checkpoint": "phase_end_active_suite_gate",
        "status": status,
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "head": snapshot["head"],
        "reviewed_base": REVIEWED_BASE,
        "git_index_tree": snapshot["git_index_tree"],
        "reviewed_blob_count": snapshot["reviewed_blob_count"],
        "pytest_command": ACTIVE_SUITE_COMMAND,
        "pytest_exit_code": pytest_exit_code,
        "pytest_passed_count": passed,
        "pytest_summary": summary,
        "failure_reason": failure_reason,
        "pytest_stdout": str(output_file),
        "pytest_stderr": str(error_file),
        "web_content_user_reviewed": [[4, 8], [4, 9], [5, 3], [4, 4]],
        "browser_pixel_visual_confirmation": "not independently verified",
        "phase_formal_closeout": "pending_documentation_record_and_final_review",
    }
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 173 final gate verifier")
    parser.add_argument("action", choices=("preflight", "finalize"))
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--stdout", type=Path)
    parser.add_argument("--stderr", type=Path)
    parser.add_argument("--exit-code", type=int)
    args = parser.parse_args()
    if args.action == "preflight":
        snapshot = validate_snapshot(args.repo)
        print("PHASE173_FINAL_HEAD=" + str(snapshot["head"]))
        print("PHASE173_FINAL_REVIEWED_BLOBS=" + str(snapshot["reviewed_blob_count"]))
        print("PHASE173_FINAL_SOURCE_GUARD=PASS")
        if args.report.is_file():
            prior = json.loads(args.report.read_text(encoding="utf-8"))
            if prior.get("status") == "PASS" and prior.get("head") == snapshot["head"]:
                print("PHASE173_FINAL_PRIOR_SUCCESS=PASS")
            else:
                raise RuntimeError("Existing full-suite report must be reviewed before retry")
    else:
        if args.stdout is None or args.stderr is None or args.exit_code is None:
            parser.error("finalize requires --stdout, --stderr and --exit-code")
        report = write_report(args.repo, args.report, args.stdout, args.stderr, args.exit_code)
        print("PHASE173_FINAL_REPORT=" + str(args.report))
        print("PHASE173_FINAL_FULL_PYTEST=" + str(report["status"]))
        print("PHASE173_FINAL_FULL_PYTEST_PASSED=" + str(report["pytest_passed_count"]))
        print("PHASE173_FINAL_FULL_PYTEST_SUMMARY=" + str(report["pytest_summary"]))
        if report["status"] != "PASS":
            raise RuntimeError("Phase 173 active full pytest failed: " + str(report["failure_reason"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
