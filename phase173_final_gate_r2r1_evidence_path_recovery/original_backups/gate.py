"""Phase 173 corrective final gate after the documented Phase 167 test-contract repair.

The first failed phase-end run remains immutable. This gate validates exactly
three reviewed test fixes, then records one new active-suite execution without
editing project code, Git index, or the previous gate evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


REVIEWED_BASE = "ac9149beaf91eeef382bc816234bd2d895398667"
EXPECTED_ACTIVE_PASSED = 3546
ACTIVE_SUITE_COMMAND = (
    "python -B -m pytest -q --tb=short --disable-warnings "
    "-p no:cacheprovider tests"
)
REVIEWED_BLOBS = {
    "tests/conftest.py": "304c7b40eb1041475fb6bc4519d3ef61fd3275e2",
    "tests/phase155_audit_only_nodeids.txt": "e65284e1e108d4ce0c81b9f1cd1e41140238dc8f",
    "phase168_r3_5_model_renderer.py": "eb34d6fd4783ca943e07de6e6d9756d0e85ff9b8",
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase165_r52_r3_web_adapter.py": "dda215780c0468cf421592aff86c79b1f5482eed",
    "web_group_proof_common.py": "0126fd71c66257fc2f4f498a5357d44a67a55884",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "web_app.py": "6f95663df5cbf028bb16d1f05dca62db2e3fc00e",
    "templates/index.html": "7af2afa40b92b8c1ec3916cf9759516c158b989f",
    "phase173_r4_r15r17r3r5_public_http_gate/tests/test_flask_public_output.py":
        "cd33d7bb774d05ec8016bdbca2854fe4191c14c7",
    "README.md": "109445340c559cfb2357d363c096cebbdb871168",
    "docs/design.md": "0491c27d8075829ba28151029eb19b119a293eff",
    "docs/development_log.md": "880dc8f9f2ff9408a9b4a61c7daa5d816955064c",
    "docs/roadmap.md": "d1d9661eb39674b156185bf61e74b8ee5fd9e101",
    "docs/proof_records.md": "eb310080fb85a265b474ed4a9c60ee91511cc6cf",
}
REPAIRED_TEST_SHA256 = {
    "tests/test_phase167_r2_range_dedup.py":
        "dab6685774e77b47332c3b2c1b4ef6731526391abc9861248503e5f9956e09cb",
    "tests/test_phase167_r2_shared_reference.py":
        "045bc41dcfeec5bad41b70cd53db95f5a36a7cb2743d4dbdcea70c1b777918af",
    "tests/test_phase167_r2_unified_reference.py":
        "94d3dfdebe21ace512e34def701ba1e1daace8d8b4927544342faeae3aa66a0e",
}
ALLOWED_NEW_PACKAGE_PREFIXES = (
    "phase173_final_gate/",
    "phase173_final_gate_r1_phase167_reference_contract/",
    "phase173_final_gate_r2_recovery/",
)
EXPECTED_PREVIOUS_FAILURES = (
    "tests/test_phase167_r2_range_dedup.py::test_phase167_r2_pi32_diagonal_range_once",
    "tests/test_phase167_r2_range_dedup.py::test_phase167_r2_pi43_diagonal_range_once",
    "tests/test_phase167_r2_shared_reference.py::test_phase167_r2_pi43_reference_has_two_general_results",
    "tests/test_phase167_r2_unified_reference.py::test_phase167_r2_pi32_reference_uses_general_form",
    "tests/test_phase167_r2_unified_reference.py::test_phase167_r2_pi43_reference_uses_general_form",
)


def git(repo: Path, *arguments: str, allow_nonzero: bool = False) -> subprocess.CompletedProcess[str]:
    """Read Git metadata without staging, resetting, cleaning, or committing."""
    result = subprocess.run(
        ("git", "--no-pager", *arguments), cwd=repo,
        text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode != 0 and not allow_nonzero:
        raise RuntimeError(
            "Git failed: " + " ".join(arguments) + ": " + result.stderr.strip()
        )
    return result


def normalized_digest(content: bytes) -> str:
    """Hash UTF-8 Python code, ignoring only Windows/Linux line endings."""
    data = content.decode("utf-8-sig")
    normalized = data.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def permitted_committed_changes(paths: list[str]) -> bool:
    """Allow only the three contract tests and already-reviewed gate packages."""
    return all(
        path in REPAIRED_TEST_SHA256
        or path.startswith(ALLOWED_NEW_PACKAGE_PREFIXES)
        for path in paths
    )


def validate_snapshot(repo: Path) -> dict[str, object]:
    """Fail closed on unreviewed code, unstaged differences, or Git divergence."""
    repo = repo.resolve(strict=True)
    if Path(git(repo, "rev-parse", "--show-toplevel").stdout.strip()).resolve() != repo:
        raise RuntimeError("ZIP must be extracted at Git repository root")
    if git(repo, "branch", "--show-current").stdout.strip() != "develop":
        raise RuntimeError("Phase 173 R2 requires the develop branch")
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    remote = git(repo, "rev-parse", "origin/develop").stdout.strip()
    if head != remote:
        raise RuntimeError("Local and origin/develop HEAD differ")
    if git(repo, "merge-base", "--is-ancestor", REVIEWED_BASE, head,
           allow_nonzero=True).returncode != 0:
        raise RuntimeError("HEAD is not descended from the reviewed Phase 173 gate")
    history_paths = git(
        repo, "diff", "--name-only", REVIEWED_BASE, "HEAD"
    ).stdout.splitlines()
    if not permitted_committed_changes(history_paths):
        raise RuntimeError("Unreviewed committed change since Phase 173 gate: "
                           + ", ".join(history_paths))
    if git(repo, "diff", "--cached", "--quiet", allow_nonzero=True).returncode != 0:
        raise RuntimeError("Staged changes are not allowed during this final gate")
    modified = git(repo, "diff", "--name-only").stdout.splitlines()
    if any(path not in REPAIRED_TEST_SHA256 for path in modified):
        raise RuntimeError("Unreviewed tracked worktree changes: " + ", ".join(modified))
    for path, expected in REVIEWED_BLOBS.items():
        actual = git(repo, "rev-parse", "HEAD:" + path).stdout.strip()
        if actual != expected:
            raise RuntimeError("Reviewed source blob changed: " + path)
    for path, expected in REPAIRED_TEST_SHA256.items():
        actual = normalized_digest((repo / path).read_bytes())
        if actual != expected:
            raise RuntimeError("R1 reviewed test fix missing or modified: " + path)
    return {
        "head": head,
        "remote_head": remote,
        "reviewed_base": REVIEWED_BASE,
        "reviewed_blob_count": len(REVIEWED_BLOBS),
        "repaired_test_count": len(REPAIRED_TEST_SHA256),
        "git_index_tree": git(repo, "write-tree").stdout.strip(),
    }


def sha256_file(path: Path) -> str:
    """Return content hash for immutable evidence files."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_prior_failure(prior_dir: Path) -> dict[str, object]:
    """Require the precise five-failure baseline and do not overwrite its files."""
    report_path = prior_dir / "phase173_full_test_report.json"
    stdout_path = prior_dir / "active_suite_stdout.txt"
    stderr_path = prior_dir / "active_suite_stderr.txt"
    attempt_path = prior_dir / "phase173_full_test_attempt.json"
    paths = (report_path, stdout_path, stderr_path, attempt_path)
    if not all(path.is_file() for path in paths):
        raise RuntimeError("Previous Phase 173 failure evidence is incomplete")
    prior = json.loads(report_path.read_text(encoding="utf-8-sig"))
    if (prior.get("phase") != 173
            or prior.get("head") != REVIEWED_BASE
            or prior.get("status") != "FAIL"
            or prior.get("pytest_exit_code") != 1):
        raise RuntimeError("Previous report does not match the reviewed failed gate")
    output = stdout_path.read_text(encoding="utf-8", errors="replace")
    normalized = output.replace("\\", "/")
    for case in EXPECTED_PREVIOUS_FAILURES:
        if "FAILED " + case not in normalized:
            raise RuntimeError("Missing reviewed failure in previous stdout: " + case)
    if not re.search(r"\b5 failed, 3541 passed\b", normalized):
        raise RuntimeError("Previous pytest summary differs from reviewed baseline")
    return {path.name: sha256_file(path) for path in paths}


def parse_success_summary(output: str, exit_code: int) -> tuple[int, str]:
    """Accept only a successful, full-size active-suite final pytest summary."""
    if type(exit_code) is not int or exit_code != 0:
        raise ValueError("active pytest did not exit with code zero")
    matches = []
    for line in output.splitlines():
        found = re.search(r"\b([0-9]+) passed in [0-9]", line)
        if found:
            matches.append((int(found.group(1)), line.strip()))
    if not matches:
        raise ValueError("complete pytest success summary was not found")
    count, summary = matches[-1]
    if count != EXPECTED_ACTIVE_PASSED:
        raise ValueError(
            f"active test count changed: {count} != {EXPECTED_ACTIVE_PASSED}"
        )
    if re.search(r"\b[1-9][0-9]*\s+(failed|error|errors)\b", summary):
        raise ValueError("pytest summary reports failures or errors")
    return count, summary


def validate_recorded_success(
    report_file: Path, snapshot: dict[str, object], prior_hashes: dict[str, object],
) -> bool:
    """Do not execute a second suite after the exact R2 success is recorded."""
    if not report_file.is_file():
        return False
    report = json.loads(report_file.read_text(encoding="utf-8-sig"))
    if (report.get("status") != "PASS"
            or report.get("head") != snapshot["head"]
            or report.get("git_index_tree") != snapshot["git_index_tree"]
            or report.get("pytest_passed_count") != EXPECTED_ACTIVE_PASSED
            or report.get("prior_failure_sha256") != prior_hashes):
        raise RuntimeError("An R2 report exists but is not a matching success")
    return True


def start_attempt(
    attempt_file: Path, snapshot: dict[str, object], prior_hashes: dict[str, object],
) -> None:
    """Create an exclusive one-attempt marker before launching the active suite."""
    attempt_file.parent.mkdir(parents=True, exist_ok=True)
    attempt = {
        "phase": 173,
        "checkpoint": "phase_end_corrective_r2",
        "status": "STARTED",
        "head": snapshot["head"],
        "git_index_tree": snapshot["git_index_tree"],
        "prior_failure_sha256": prior_hashes,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "pytest_command": ACTIVE_SUITE_COMMAND,
    }
    with attempt_file.open("x", encoding="utf-8") as output:
        json.dump(attempt, output, ensure_ascii=False, indent=2)
        output.write("\n")


def finalize(
    snapshot: dict[str, object], prior_hashes: dict[str, object],
    attempt_file: Path, report_file: Path, stdout_file: Path, stderr_file: Path,
    exit_code: int,
) -> dict[str, object]:
    """Record pass or fail once without deleting any historical result."""
    if report_file.exists():
        raise RuntimeError("R2 report exists: refusing to replace earlier evidence")
    attempt = json.loads(attempt_file.read_text(encoding="utf-8-sig"))
    if (attempt.get("status") != "STARTED"
            or attempt.get("head") != snapshot["head"]
            or attempt.get("git_index_tree") != snapshot["git_index_tree"]
            or attempt.get("prior_failure_sha256") != prior_hashes):
        raise RuntimeError("R2 attempt does not match the pre-test snapshot")
    stdout = stdout_file.read_text(encoding="utf-8", errors="replace")
    stderr = stderr_file.read_text(encoding="utf-8", errors="replace")
    status = "PASS"
    passed: int | None = None
    summary = ""
    failure_reason: str | None = None
    try:
        passed, summary = parse_success_summary(stdout + "\n" + stderr, exit_code)
    except ValueError as error:
        status, failure_reason = "FAIL", str(error)
    report = {
        "phase": 173,
        "checkpoint": "phase_end_corrective_r2",
        "status": status,
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "head": snapshot["head"],
        "git_index_tree": snapshot["git_index_tree"],
        "reviewed_blob_count": snapshot["reviewed_blob_count"],
        "repaired_test_count": snapshot["repaired_test_count"],
        "prior_failure_sha256": prior_hashes,
        "pytest_command": ACTIVE_SUITE_COMMAND,
        "pytest_exit_code": exit_code,
        "pytest_passed_count": passed,
        "pytest_summary": summary,
        "failure_reason": failure_reason,
        "pytest_stdout": str(stdout_file),
        "pytest_stderr": str(stderr_file),
        "browser_content_checked": [[4, 8], [4, 9], [5, 3], [4, 4]],
        "browser_pixel_layout": "not independently verified",
        "phase_formally_closed": False,
        "phase_closeout_documents": "pending final record after successful gate",
    }
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with report_file.open("x", encoding="utf-8") as output:
        json.dump(report, output, ensure_ascii=False, indent=2)
        output.write("\n")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 173 corrective final Gate R2")
    parser.add_argument("action", choices=("preflight", "start", "finalize"))
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--prior", type=Path, required=True)
    parser.add_argument("--attempt", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--stdout", type=Path)
    parser.add_argument("--stderr", type=Path)
    parser.add_argument("--exit-code", type=int)
    args = parser.parse_args()
    snapshot = validate_snapshot(args.repo)
    prior_hashes = verify_prior_failure(args.prior)
    print("PHASE173_FINAL_R2_HEAD=" + str(snapshot["head"]))
    print("PHASE173_FINAL_R2_REVIEWED_BLOBS=" + str(snapshot["reviewed_blob_count"]))
    print("PHASE173_FINAL_R2_REPAIRED_TEST_FILES=" + str(snapshot["repaired_test_count"]))
    print("PHASE173_FINAL_R2_SOURCE_GUARD=PASS")
    print("PHASE173_FINAL_R2_PRIOR_FAILURE_PRESERVED=PASS")
    if args.action == "preflight":
        if validate_recorded_success(args.report, snapshot, prior_hashes):
            print("PHASE173_FINAL_R2_PRIOR_SUCCESS=PASS")
        elif args.attempt.exists():
            raise RuntimeError("An R2 test attempt exists without matching PASS report")
        print("PHASE173_FINAL_R2_PREFLIGHT=PASS")
    elif args.action == "start":
        if args.report.exists() or args.attempt.exists():
            raise RuntimeError("R2 test attempt/report exists; refusing repeated execution")
        start_attempt(args.attempt, snapshot, prior_hashes)
        print("PHASE173_FINAL_R2_ATTEMPT_CREATED=PASS")
    else:
        if args.stdout is None or args.stderr is None or args.exit_code is None:
            parser.error("finalize requires stdout, stderr and exit-code")
        report = finalize(
            snapshot, prior_hashes, args.attempt, args.report,
            args.stdout, args.stderr, args.exit_code,
        )
        print("PHASE173_FINAL_R2_REPORT=" + str(args.report))
        print("PHASE173_FINAL_R2_FULL_PYTEST=" + str(report["status"]))
        print("PHASE173_FINAL_R2_FULL_PYTEST_PASSED=" + str(report["pytest_passed_count"]))
        print("PHASE173_FINAL_R2_FULL_PYTEST_SUMMARY=" + str(report["pytest_summary"]))
        if report["status"] != "PASS":
            raise RuntimeError("Phase 173 R2 full pytest failed: " + str(report["failure_reason"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
