# Phase 173 R2R2 変更対象と全文

既存ファイルの置換対象：`phase173_final_gate_r2_recovery/gate.py`、`phase173_final_gate_r2_recovery/run.ps1`。
既存の import は R2 Gate 内で変更せず、新規 `prior_evidence_status()` は `verify_prior_failure()` 直後に追加する。

## gate.py の全文

```python
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

# The only reviewed committed R1 test contracts (old base and corrected files).
# They are consulted when the remote moved ahead of a locally uncommitted fix.
BASE_R1_TEST_BLOBS = {
    "tests/test_phase167_r2_range_dedup.py": "13fc81efe267083951d59c009cd10112985fd204",
    "tests/test_phase167_r2_shared_reference.py": "e8f69cffdc2b3cbf3c48bace6a4a83ad3cb00d0e",
    "tests/test_phase167_r2_unified_reference.py": "4ab72c4ff58f24643d0f20562491870dc667f6cf",
}
APPROVED_REMOTE_R1_BLOBS = {
    "tests/test_phase167_r2_range_dedup.py": "bf5e3facdd317d0b0a99819f340f99d0025f7af1",
    "tests/test_phase167_r2_shared_reference.py": "86660e8ca8b8bf23163f825f2045fa4f1df08775",
    "tests/test_phase167_r2_unified_reference.py": "595eadbaf54a334786d6d3bd1c4fee344ca7e1de",
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
    """Check reviewed code even when origin advanced by only the R1 test fix.

    A fast-forwarded remote does not justify changing the user's HEAD or
    worktree. Both histories must contain only the explicitly reviewed R1
    correction and gate packages; local tested bytes are independently hashed.
    """
    repo = repo.resolve(strict=True)
    if Path(git(repo, "rev-parse", "--show-toplevel").stdout.strip()).resolve() != repo:
        raise RuntimeError("ZIP must be extracted at Git repository root")
    if git(repo, "branch", "--show-current").stdout.strip() != "develop":
        raise RuntimeError("Phase 173 R2 requires the develop branch")
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    remote = git(repo, "rev-parse", "origin/develop").stdout.strip()
    for commit in (head, remote):
        if git(repo, "merge-base", "--is-ancestor", REVIEWED_BASE, commit,
               allow_nonzero=True).returncode != 0:
            raise RuntimeError("HEAD is not descended from the reviewed Phase 173 gate")
    if head != remote:
        if git(repo, "merge-base", "--is-ancestor", head, remote,
               allow_nonzero=True).returncode != 0:
            raise RuntimeError("Local and origin/develop histories diverged")
        for path, expected in APPROVED_REMOTE_R1_BLOBS.items():
            remote_blob = git(repo, "rev-parse", "origin/develop:" + path).stdout.strip()
            if remote_blob not in (BASE_R1_TEST_BLOBS[path], expected):
                raise RuntimeError("Unreviewed remote test change: " + path)
    for commit in (head, remote):
        history_paths = git(
            repo, "diff", "--name-only", REVIEWED_BASE, commit
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
        # Equal HEADs share one immutable Git tree. In the reviewed
        # fast-forward case, verify both trees independently.
        commits = ("HEAD", "origin/develop") if head != remote else ("HEAD",)
        for commit in commits:
            actual = git(repo, "rev-parse", commit + ":" + path).stdout.strip()
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


def verify_prior_failure(
    prior_dir: Path, allow_missing: bool = False,
) -> dict[str, object]:
    """Require the precise five-failure baseline when files are available.

    If the user explicitly acknowledges that the original four files are not
    accessible from the present Windows profile, return no hashes. Never
    manufacture a failure report or mark missing evidence as verified.
    Reject partial archives and invalid/mismatching original files.
    """
    report_path = prior_dir / "phase173_full_test_report.json"
    stdout_path = prior_dir / "active_suite_stdout.txt"
    stderr_path = prior_dir / "active_suite_stderr.txt"
    attempt_path = prior_dir / "phase173_full_test_attempt.json"
    paths = (report_path, stdout_path, stderr_path, attempt_path)
    present = tuple(path.is_file() for path in paths)
    if not all(present):
        if allow_missing and not any(present):
            return {}
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


def prior_evidence_status(prior_hashes: dict[str, object]) -> str:
    """Describe the actual verification strength without claiming missing hashes."""
    return ("VERIFIED_FOUR_FILES" if len(prior_hashes) == 4
            else "UNAVAILABLE_ORIGINAL_FILES")


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
        "prior_failure_evidence_status": prior_evidence_status(prior_hashes),
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
        "remote_head": snapshot.get("remote_head", snapshot["head"]),
        "git_index_tree": snapshot["git_index_tree"],
        "reviewed_blob_count": snapshot["reviewed_blob_count"],
        "repaired_test_count": snapshot["repaired_test_count"],
        "prior_failure_sha256": prior_hashes,
        "prior_failure_evidence_status": prior_evidence_status(prior_hashes),
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
    parser.add_argument("--allow-missing-prior-evidence", action="store_true")
    parser.add_argument("--attempt", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--stdout", type=Path)
    parser.add_argument("--stderr", type=Path)
    parser.add_argument("--exit-code", type=int)
    args = parser.parse_args()
    snapshot = validate_snapshot(args.repo)
    prior_hashes = verify_prior_failure(
        args.prior, allow_missing=args.allow_missing_prior_evidence,
    )
    print("PHASE173_FINAL_R2_HEAD=" + str(snapshot["head"]))
    print("PHASE173_FINAL_R2_REMOTE_HEAD=" + str(snapshot["remote_head"]))
    print("PHASE173_FINAL_R2_REVIEWED_BLOBS=" + str(snapshot["reviewed_blob_count"]))
    print("PHASE173_FINAL_R2_REPAIRED_TEST_FILES=" + str(snapshot["repaired_test_count"]))
    print("PHASE173_FINAL_R2_SOURCE_GUARD=PASS")
    print("PHASE173_FINAL_R2_PRIOR_FAILURE_EVIDENCE="
          + prior_evidence_status(prior_hashes))
    print("PHASE173_FINAL_R2_PRIOR_FAILURE_PRESERVED="
          + ("PASS" if prior_hashes else "NOT_VERIFIABLE"))
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

```

## run.ps1 の全文

```powershell
param(
    [switch]$DryRun,
    [string]$PreviousEvidencePath,
    [switch]$AllowMissingPriorEvidence
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:GIT_PAGER = 'cat'
$env:PAGER = 'cat'

$Package = $PSScriptRoot
$Root = (Resolve-Path (Join-Path $Package '..')).Path
$GitRoot = (& git -C $Root --no-pager rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($GitRoot)) {
    throw 'Git repository root was not found'
}
if (-not [string]::Equals(
    [IO.Path]::GetFullPath($Root).TrimEnd([char]'\', [char]'/'),
    [IO.Path]::GetFullPath($GitRoot).TrimEnd([char]'\', [char]'/'),
    [StringComparison]::OrdinalIgnoreCase
)) {
    throw 'Extract Phase 173 R2 ZIP at repository root'
}

$RecordParent = if ([string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
    $env:TEMP
} else {
    $env:LOCALAPPDATA
}
$DefaultPrevious = Join-Path $RecordParent 'EHPProofTracerRecovery\phase173_final_gate'
$KnownPreviousProfile = 'C:\Users\oomae\AppData\Local\EHPProofTracerRecovery\phase173_final_gate'
$RequiredPreviousFiles = @(
    'phase173_full_test_report.json',
    'phase173_full_test_attempt.json',
    'active_suite_stdout.txt',
    'active_suite_stderr.txt'
)
function Test-CompletePreviousEvidence {
    param([string]$Directory)
    foreach ($File in $RequiredPreviousFiles) {
        if (-not (Test-Path -LiteralPath (Join-Path $Directory $File) -PathType Leaf)) {
            return $false
        }
    }
    return $true
}
if (-not [string]::IsNullOrWhiteSpace($PreviousEvidencePath)) {
    $PreviousEvidence = [IO.Path]::GetFullPath($PreviousEvidencePath)
} elseif (Test-CompletePreviousEvidence $DefaultPrevious) {
    $PreviousEvidence = $DefaultPrevious
} elseif (Test-CompletePreviousEvidence $KnownPreviousProfile) {
    $PreviousEvidence = $KnownPreviousProfile
} elseif ($AllowMissingPriorEvidence) {
    $PreviousEvidence = $DefaultPrevious
    Write-Output 'PHASE173_FINAL_R2_MISSING_PRIOR_ACKNOWLEDGED=True'
} else {
    Write-Output 'PHASE173_FINAL_R2_PRIOR_EVIDENCE=NOT_FOUND'
    foreach ($Directory in @($DefaultPrevious, $KnownPreviousProfile) | Select-Object -Unique) {
        $Missing = @($RequiredPreviousFiles | Where-Object {
            -not (Test-Path -LiteralPath (Join-Path $Directory $_) -PathType Leaf)
        })
        Write-Output "PHASE173_FINAL_R2_CHECKED_DIR=$Directory"
        Write-Output "PHASE173_FINAL_R2_MISSING_FILES=$($Missing -join ',')"
    }
    throw 'Original Phase 173 failure evidence is missing. Use -PreviousEvidencePath with the unmodified four-file evidence directory.'
}
if (-not (Test-CompletePreviousEvidence $PreviousEvidence)) {
    $Missing = @($RequiredPreviousFiles | Where-Object {
        -not (Test-Path -LiteralPath (Join-Path $PreviousEvidence $_) -PathType Leaf)
    })
    Write-Output "PHASE173_FINAL_R2_PRIOR_EVIDENCE_DIR=$PreviousEvidence"
    Write-Output "PHASE173_FINAL_R2_MISSING_FILES=$($Missing -join ',')"
    if (-not $AllowMissingPriorEvidence -or $Missing.Count -ne $RequiredPreviousFiles.Count) {
        throw 'Partial previous evidence cannot be treated as missing; review the original files.'
    }
    Write-Output 'PHASE173_FINAL_R2_PRIOR_FAILURE_EVIDENCE=UNAVAILABLE_ORIGINAL_FILES'
} else {
    Write-Output 'PHASE173_FINAL_R2_PRIOR_FAILURE_EVIDENCE=VERIFIED_FOUR_FILES'
}
Write-Output "PHASE173_FINAL_R2_PRIOR_EVIDENCE_DIR=$PreviousEvidence"
$PriorArguments = @()
if ($AllowMissingPriorEvidence) {
    $PriorArguments += '--allow-missing-prior-evidence'
}
$Evidence = Join-Path $RecordParent 'EHPProofTracerRecovery\phase173_final_gate_r2'
$Report = Join-Path $Evidence 'phase173_full_test_report_r2.json'
$Attempt = Join-Path $Evidence 'phase173_full_test_attempt_r2.json'
$Stdout = Join-Path $Evidence 'active_suite_stdout_r2.txt'
$Stderr = Join-Path $Evidence 'active_suite_stderr_r2.txt'

Push-Location $Root
try {
    Write-Output 'PHASE173_FINAL_R2_SCOPE=CORRECTIVE_PHASE_END_ACTIVE_SUITE'
    Write-Output 'PHASE173_FINAL_R2_GIT_STAGE_RESET_CLEAN_COMMIT=NONE'
    Write-Output 'PHASE173_FINAL_R2_PRODUCTION_WRITES=NONE'
    Write-Output 'PHASE173_FINAL_R2_PREVIOUS_REPORT=IMMUTABLE'
    Write-Output 'PHASE173_FINAL_R2_BROWSER_PIXEL_LAYOUT=UNCONFIRMED'
    $BeforeIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Unable to record Git index tree' }
    & git --no-pager fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'Unable to fetch origin/develop' }

    Write-Output '=== PHASE 173 FINAL R2 CONTRACT TESTS ==='
    & python -B -m pytest -q --tb=short -p no:cacheprovider `
        phase173_final_gate_r2_recovery/tests/test_gate_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'Final R2 gate contract tests failed' }

    & python -B -m phase173_final_gate_r2_recovery.gate preflight `
        --repo $Root --prior $PreviousEvidence @PriorArguments --attempt $Attempt --report $Report
    if ($LASTEXITCODE -ne 0) { throw 'Final R2 source/prior evidence preflight failed' }

    if ($DryRun) {
        Write-Output 'PHASE173_FINAL_R2_DRY_RUN=PASS'
        Write-Output 'PHASE173_FINAL_R2_FULL_PYTEST=NOT_RUN_IN_DRY_RUN'
    }
    else {
        if (Test-Path $Report) {
            $Recorded = Get-Content -Path $Report -Raw -Encoding UTF8 | ConvertFrom-Json
            if ($Recorded.status -ne 'PASS') { throw 'Prior R2 report is not PASS' }
            Write-Output 'PHASE173_FINAL_R2_FULL_PYTEST=PASS_PREVIOUSLY_RECORDED'
            Write-Output "PHASE173_FINAL_R2_FULL_PYTEST_PASSED=$($Recorded.pytest_passed_count)"
            Write-Output "PHASE173_FINAL_R2_REPORT=$Report"
        }
        else {
            & python -B -m phase173_final_gate_r2_recovery.gate start `
                --repo $Root --prior $PreviousEvidence @PriorArguments --attempt $Attempt --report $Report
            if ($LASTEXITCODE -ne 0) { throw 'Unable to record exclusive R2 attempt' }
            $PythonPath = (Get-Command python).Source
            Write-Output '=== PHASE 173 R2 ACTIVE FULL PYTEST (CORRECTIVE EXECUTION) ==='
            $Args = @('-B', '-m', 'pytest', '-q', '--tb=short', '--disable-warnings',
                '-p', 'no:cacheprovider', 'tests')
            $Process = Start-Process -FilePath $PythonPath -ArgumentList $Args `
                -WorkingDirectory $Root -RedirectStandardOutput $Stdout `
                -RedirectStandardError $Stderr -NoNewWindow -Wait -PassThru
            $TestExit = $Process.ExitCode
            Write-Output "PHASE173_FINAL_R2_PYTEST_EXIT=$TestExit"
            if (Test-Path $Stdout) { Get-Content $Stdout -Tail 45 }
            if ((Test-Path $Stderr) -and (Get-Item $Stderr).Length -gt 0) {
                Write-Output '=== R2 PYTEST STDERR ==='
                Get-Content $Stderr -Tail 30
            }
            & python -B -m phase173_final_gate_r2_recovery.gate finalize `
                --repo $Root --prior $PreviousEvidence @PriorArguments --attempt $Attempt `
                --report $Report --stdout $Stdout --stderr $Stderr --exit-code $TestExit
            if ($LASTEXITCODE -ne 0) { throw 'Phase 173 R2 active pytest failed' }
        }
        Write-Output 'PHASE173_FINAL_R2_GATE=PASS'
        Write-Output 'PHASE173_FINAL_R2_PHASE_FORMALLY_CLOSED=NO_DOCUMENTATION_PENDING'
    }

    $AfterIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0 -or $AfterIndex -ne $BeforeIndex) {
        throw 'Phase 173 R2 modified the Git index'
    }
    Write-Output 'PHASE173_FINAL_R2_GIT_INDEX_PRESERVED=PASS'
    & git --no-pager status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read final Git status' }
    & git --no-pager diff --stat
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read final Git diff'
    }
}
finally {
    Pop-Location
}

```

## patch.py の全文

```python
"""Guarded two-file repair of the R2 preflight; does not touch production code."""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
from pathlib import Path


ORIGINAL_SHA256 = {
    "gate.py": "71a2cea4ef928d7d2bc82e6ac90cf1233a1460ba1cecdf03d32627f9b8f19db2",
    "run.ps1": "d67c0b3ffdce14654fa62585e2205af9ad13d6eaa514437c8c65face251987ab",
}
REPLACEMENT_SHA256 = {
    "gate.py": "b832c2c3499ec29e44f000571f1a37da7451d865ed303708bb63a65217244881",
    "run.ps1": "6e20fb62a603052370950cc754393fc6f7f11a30314fcc933f3972884010d0ec",
}
TARGET_DIR = "phase173_final_gate_r2_recovery"


def digest(data: bytes) -> str:
    """Hash complete bytes; do not normalize source code or mathematical data."""
    return hashlib.sha256(data).hexdigest()


def reviewed_files(repo: Path, package: Path) -> tuple[tuple[Path, Path, str], ...]:
    """Fail on altered R2 input or on missing release replacements."""
    result: list[tuple[Path, Path, str]] = []
    for name, old_sha in ORIGINAL_SHA256.items():
        target = repo / TARGET_DIR / name
        replacement = package / "replacement" / name
        if not target.is_file() or not replacement.is_file():
            raise RuntimeError("R2 source or reviewed replacement is missing: " + name)
        present = digest(target.read_bytes())
        desired = digest(replacement.read_bytes())
        if desired != REPLACEMENT_SHA256[name]:
            raise RuntimeError("Reviewed R2R2 replacement has changed: " + name)
        if present not in (old_sha, desired):
            raise RuntimeError("R2 source has unreviewed local edits: " + name)
        state = "ALREADY_PATCHED" if present == desired else "REVIEWED_OLD"
        result.append((target, replacement, state))
    return tuple(result)


def _atomic_write(path: Path, content: bytes) -> None:
    """Replace one reviewed file without leaving truncated output."""
    temporary = path.with_name(path.name + ".phase173_r2r2_tmp")
    if temporary.exists():
        raise RuntimeError("Stale temporary file needs manual review: " + str(temporary))
    try:
        with temporary.open("xb") as stream:
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def apply_reviewed_patch(repo: Path, package: Path) -> tuple[str, ...]:
    """Back up original bytes before applying only the two reviewed files."""
    files = reviewed_files(repo, package)
    backup_dir = package / "original_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    for target, replacement, state in files:
        backup = backup_dir / target.name
        if backup.exists():
            if digest(backup.read_bytes()) != ORIGINAL_SHA256[target.name]:
                raise RuntimeError("An existing original backup differs: " + str(backup))
        elif state == "REVIEWED_OLD":
            with backup.open("xb") as output:
                output.write(target.read_bytes())
        elif state == "ALREADY_PATCHED":
            # Do not invent an original backup after the original has vanished.
            continue
    before = {target: target.read_bytes() for target, _, _ in files}
    changed: list[Path] = []
    try:
        for target, replacement, state in files:
            if state == "REVIEWED_OLD":
                _atomic_write(target, replacement.read_bytes())
                changed.append(target)
        if any(state != "ALREADY_PATCHED" for _, _, state in reviewed_files(repo, package)):
            raise RuntimeError("R2 patch did not reach the reviewed state")
    except Exception:
        for target in reversed(changed):
            _atomic_write(target, before[target])
        raise
    return tuple("R2R2_PATCHED_FILE=" + str(target.relative_to(repo))
                 for target in changed)


def rollback_reviewed_patch(repo: Path, package: Path) -> tuple[str, ...]:
    """Restore backed-up originals only if targets still equal our replacements."""
    files = reviewed_files(repo, package)
    backup_dir = package / "original_backups"
    changed: list[str] = []
    for target, _, state in files:
        if state == "ALREADY_PATCHED":
            backup = backup_dir / target.name
            if not backup.is_file() or digest(backup.read_bytes()) != ORIGINAL_SHA256[target.name]:
                raise RuntimeError("R2 original backup missing; refusing rollback: " + target.name)
            _atomic_write(target, backup.read_bytes())
            changed.append(str(target.relative_to(repo)))
    return tuple(changed)


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 173 R2R2 evidence-location patch")
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve(strict=True)
    package = args.package.resolve(strict=True)
    if args.apply and args.rollback:
        parser.error("--apply and --rollback are mutually exclusive")
    git_root = subprocess.run(
        ("git", "rev-parse", "--show-toplevel"), cwd=repo, capture_output=True,
        encoding="utf-8", errors="replace", check=True,
    ).stdout.strip()
    if Path(git_root).resolve() != repo:
        raise RuntimeError("Extract at EHP repository root")
    for target, replacement, state in reviewed_files(repo, package):
        print(f"PHASE173_FINAL_R2R2_SOURCE={target.name}:{state}")
        print(f"PHASE173_FINAL_R2R2_REPLACEMENT_SHA256={target.name}:{digest(replacement.read_bytes())}")
    if args.rollback:
        for name in rollback_reviewed_patch(repo, package):
            print("PHASE173_FINAL_R2R2_ROLLED_BACK=" + name)
    elif args.apply:
        for marker in apply_reviewed_patch(repo, package):
            print(marker)
        print("PHASE173_FINAL_R2R2_INSTALL=PASS")
    else:
        print("PHASE173_FINAL_R2R2_DRY_RUN=PASS")
        print("PHASE173_FINAL_R2R2_PRODUCTION_WRITES=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## 追加テストファイル（import・テスト関数すべて）の全文

```python
"""Focused tests for the opt-in missing-historical-evidence R2R2 patch."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil

import pytest

from phase173_final_gate_r2r2_missing_evidence import patch


PACKAGE = Path(__file__).resolve().parents[1]
REPLACEMENT_GATE = PACKAGE / "replacement" / "gate.py"
REPLACEMENT_RUNNER = PACKAGE / "replacement" / "run.ps1"
ORIGINAL_BACKUP = PACKAGE / "tests" / "fixtures"


def _gate():
    spec = importlib.util.spec_from_file_location("r2r2_reviewed_gate", REPLACEMENT_GATE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _valid_prior(gate, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "phase173_full_test_report.json").write_text(
        json.dumps({"phase": 173, "head": gate.REVIEWED_BASE,
                    "status": "FAIL", "pytest_exit_code": 1}), encoding="utf-8"
    )
    output = "\n".join("FAILED " + name.replace("/", "\\")
                       for name in gate.EXPECTED_PREVIOUS_FAILURES)
    (directory / "active_suite_stdout.txt").write_text(
        output + "\n5 failed, 3541 passed in 34.43s\n", encoding="utf-8"
    )
    (directory / "active_suite_stderr.txt").write_text("", encoding="utf-8")
    (directory / "phase173_full_test_attempt.json").write_text(
        json.dumps({"status": "STARTED"}), encoding="utf-8"
    )


def test_reviewed_sources_have_pinned_hashes_and_valid_python() -> None:
    import ast
    ast.parse(REPLACEMENT_GATE.read_text(encoding="utf-8"))
    assert set(patch.ORIGINAL_SHA256) == {"gate.py", "run.ps1"}
    for name in patch.ORIGINAL_SHA256:
        assert patch.digest(REPLACEMENT_GATE.read_bytes() if name == "gate.py"
                            else REPLACEMENT_RUNNER.read_bytes()) == patch.REPLACEMENT_SHA256[name]
        assert len(patch.ORIGINAL_SHA256[name]) == 64


def test_default_mode_still_rejects_absent_evidence(tmp_path: Path) -> None:
    gate = _gate()
    with pytest.raises(RuntimeError, match="evidence is incomplete"):
        gate.verify_prior_failure(tmp_path)


def test_explicit_missing_mode_returns_no_hashes_without_writes(tmp_path: Path) -> None:
    gate = _gate()
    prior = tmp_path / "other_profile"
    assert gate.verify_prior_failure(prior, allow_missing=True) == {}
    assert not prior.exists()
    assert gate.prior_evidence_status({}) == "UNAVAILABLE_ORIGINAL_FILES"


def test_partial_originals_never_accepted_even_with_opt_in(tmp_path: Path) -> None:
    gate = _gate()
    (tmp_path / "active_suite_stdout.txt").write_text("", encoding="utf-8")
    with pytest.raises(RuntimeError, match="evidence is incomplete"):
        gate.verify_prior_failure(tmp_path, allow_missing=True)


def test_verified_four_file_evidence_remains_verified(tmp_path: Path) -> None:
    gate = _gate()
    _valid_prior(gate, tmp_path)
    found = gate.verify_prior_failure(tmp_path, allow_missing=True)
    assert len(found) == 4
    assert all(len(x) == 64 for x in found.values())
    assert gate.prior_evidence_status(found) == "VERIFIED_FOUR_FILES"


def test_invalid_complete_baseline_is_not_accepted(tmp_path: Path) -> None:
    gate = _gate()
    _valid_prior(gate, tmp_path)
    (tmp_path / "active_suite_stdout.txt").write_text("5 failed, 3541 passed\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Missing reviewed failure"):
        gate.verify_prior_failure(tmp_path, allow_missing=True)


def test_run_requires_explicit_missing_evidence_switch() -> None:
    script = REPLACEMENT_RUNNER.read_text(encoding="utf-8")
    assert "[switch]$AllowMissingPriorEvidence" in script
    assert "if ($AllowMissingPriorEvidence)" in script
    assert "--allow-missing-prior-evidence" in script
    assert "@PriorArguments --attempt" in script
    assert "Partial previous evidence" in script
    assert script.count("@PriorArguments --attempt") == 3


def test_missing_evidence_is_not_claimed_as_verified_in_public_gate() -> None:
    source = REPLACEMENT_GATE.read_text(encoding="utf-8")
    assert '("PASS" if prior_hashes else "NOT_VERIFIABLE")' in source
    assert '"NOT_VERIFIABLE"' in source
    assert '"prior_failure_evidence_status": prior_evidence_status(prior_hashes)' in source
    assert "return {}" in source


def test_gate_preserves_full_suite_size_and_reviewed_source_checks() -> None:
    gate = _gate()
    assert gate.EXPECTED_ACTIVE_PASSED == 3546
    assert len(gate.REVIEWED_BLOBS) == 15
    assert len(gate.REPAIRED_TEST_SHA256) == 3
    assert gate.parse_success_summary("3546 passed in 47.03s", 0)[0] == 3546
    with pytest.raises(ValueError):
        gate.parse_success_summary("3541 passed in 47.03s", 0)


def test_reviewed_two_file_patcher_is_idempotent_and_restores_backup(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    target = repo / patch.TARGET_DIR
    target.mkdir(parents=True)
    pack = tmp_path / "package"
    (pack / "replacement").mkdir(parents=True)
    for name in patch.ORIGINAL_SHA256:
        original = ORIGINAL_BACKUP / name
        assert patch.digest(original.read_bytes()) == patch.ORIGINAL_SHA256[name]
        shutil.copyfile(original, target / name)
        shutil.copyfile(PACKAGE / "replacement" / name, pack / "replacement" / name)
    result = patch.apply_reviewed_patch(repo, pack)
    assert len(result) == 2
    assert patch.apply_reviewed_patch(repo, pack) == ()
    assert len(patch.rollback_reviewed_patch(repo, pack)) == 2
    for name in patch.ORIGINAL_SHA256:
        assert patch.digest((target / name).read_bytes()) == patch.ORIGINAL_SHA256[name]


def test_patcher_refuses_unknown_changes(tmp_path: Path) -> None:
    target = tmp_path / patch.TARGET_DIR
    target.mkdir()
    (target / "gate.py").write_text("tampered", encoding="utf-8")
    (target / "run.ps1").write_bytes(REPLACEMENT_RUNNER.read_bytes())
    with pytest.raises(RuntimeError, match="unreviewed"):
        patch.reviewed_files(tmp_path, PACKAGE)


def test_unavailable_prior_still_writes_honest_new_report(tmp_path: Path) -> None:
    gate = _gate()
    snapshot = {"head": gate.REVIEWED_BASE, "remote_head": gate.REVIEWED_BASE,
                "git_index_tree": "tree123", "reviewed_blob_count": 15,
                "repaired_test_count": 3}
    attempt = tmp_path / "attempt.json"
    report = tmp_path / "report.json"
    stdout = tmp_path / "stdout.txt"
    stderr = tmp_path / "stderr.txt"
    gate.start_attempt(attempt, snapshot, {})
    stdout.write_text("3546 passed in 44.03s\n", encoding="utf-8")
    stderr.write_text("", encoding="utf-8")
    result = gate.finalize(snapshot, {}, attempt, report, stdout, stderr, 0)
    assert result["status"] == "PASS"
    assert result["pytest_passed_count"] == 3546
    assert result["prior_failure_sha256"] == {}
    assert result["prior_failure_evidence_status"] == "UNAVAILABLE_ORIGINAL_FILES"
    assert report.is_file()
    assert gate.validate_recorded_success(report, snapshot, {})
    with pytest.raises(RuntimeError, match="report exists"):
        gate.finalize(snapshot, {}, attempt, report, stdout, stderr, 0)


def test_preflight_reports_missing_artifacts_as_unverified(tmp_path: Path, monkeypatch, capsys) -> None:
    import sys
    gate = _gate()
    monkeypatch.setattr(gate, "validate_snapshot", lambda repo: {
        "head": gate.REVIEWED_BASE, "remote_head": gate.REVIEWED_BASE,
        "reviewed_blob_count": 15, "repaired_test_count": 3,
        "git_index_tree": "unchanged"
    })
    monkeypatch.setattr(sys, "argv", ["gate", "preflight", "--repo", str(tmp_path),
        "--prior", str(tmp_path / "missing"),
        "--attempt", str(tmp_path / "attempt.json"),
        "--report", str(tmp_path / "report.json"),
        "--allow-missing-prior-evidence"])
    assert gate.main() == 0
    output = capsys.readouterr().out
    assert "PHASE173_FINAL_R2_PRIOR_FAILURE_PRESERVED=NOT_VERIFIABLE" in output
    assert "PHASE173_FINAL_R2_SOURCE_GUARD=PASS" in output
    assert "PHASE173_FINAL_R2_PREFLIGHT=PASS" in output

```
