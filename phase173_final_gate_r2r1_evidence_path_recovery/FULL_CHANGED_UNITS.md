# Phase 173 Final Gate R2R1 — 全変更単位・文書全文

変更対象（既存）は `phase173_final_gate_r2_recovery/gate.py` と `phase173_final_gate_r2_recovery/run.ps1` の2ファイルのみ。新規は R2R1 のパッチ・テスト・文書である。既存 Python の import 変更はない。`gate.py` の変更後全文、`run.ps1` の全文、パッチ・テスト・文書全文を以下に記載する。実装内に `...` による省略はない。

## replacement/gate.py

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
        "remote_head": snapshot.get("remote_head", snapshot["head"]),
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
    print("PHASE173_FINAL_R2_REMOTE_HEAD=" + str(snapshot["remote_head"]))
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

```

## replacement/run.ps1

```powershell
param(
    [switch]$DryRun,
    [string]$PreviousEvidencePath
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
    throw 'Selected prior-evidence directory is incomplete; nothing will be overwritten.'
}
Write-Output "PHASE173_FINAL_R2_PRIOR_EVIDENCE_DIR=$PreviousEvidence"
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
        --repo $Root --prior $PreviousEvidence --attempt $Attempt --report $Report
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
                --repo $Root --prior $PreviousEvidence --attempt $Attempt --report $Report
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
                --repo $Root --prior $PreviousEvidence --attempt $Attempt `
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

## patch.py

```python
"""Guarded two-file repair of the R2 preflight; does not touch production code."""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
from pathlib import Path


ORIGINAL_SHA256 = {
    "gate.py": "f282ff57ca4db29a4c8d0630f168084cafa205d30c7569e8e57c37a984d9a83c",
    "run.ps1": "0892e7245ef11e3225aa7202ef738488da824372009514f1fc3d5094b633a93c",
}
REPLACEMENT_SHA256 = {
    "gate.py": "71a2cea4ef928d7d2bc82e6ac90cf1233a1460ba1cecdf03d32627f9b8f19db2",
    "run.ps1": "d67c0b3ffdce14654fa62585e2205af9ad13d6eaa514437c8c65face251987ab",
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
            raise RuntimeError("Reviewed R2R1 replacement has changed: " + name)
        if present not in (old_sha, desired):
            raise RuntimeError("R2 source has unreviewed local edits: " + name)
        state = "ALREADY_PATCHED" if present == desired else "REVIEWED_OLD"
        result.append((target, replacement, state))
    return tuple(result)


def _atomic_write(path: Path, content: bytes) -> None:
    """Replace one reviewed file without leaving truncated output."""
    temporary = path.with_name(path.name + ".phase173_r2r1_tmp")
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
    return tuple("R2R1_PATCHED_FILE=" + str(target.relative_to(repo))
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
    parser = argparse.ArgumentParser(description="Phase 173 R2R1 evidence-location patch")
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
        print(f"PHASE173_FINAL_R2R1_SOURCE={target.name}:{state}")
        print(f"PHASE173_FINAL_R2R1_REPLACEMENT_SHA256={target.name}:{digest(replacement.read_bytes())}")
    if args.rollback:
        for name in rollback_reviewed_patch(repo, package):
            print("PHASE173_FINAL_R2R1_ROLLED_BACK=" + name)
    elif args.apply:
        for marker in apply_reviewed_patch(repo, package):
            print(marker)
        print("PHASE173_FINAL_R2R1_INSTALL=PASS")
    else:
        print("PHASE173_FINAL_R2R1_DRY_RUN=PASS")
        print("PHASE173_FINAL_R2R1_PRODUCTION_WRITES=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## run.ps1

```powershell
param([switch]$DryRun)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:GIT_PAGER = 'cat'
$env:PAGER = 'cat'

$Package = $PSScriptRoot
$Root = (Resolve-Path (Join-Path $Package '..')).Path
$GitRoot = (& git -C $Root --no-pager rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($GitRoot)) {
    throw 'Git repository root not found'
}
if (-not [string]::Equals(
    [IO.Path]::GetFullPath($Root).TrimEnd([char]'\', [char]'/'),
    [IO.Path]::GetFullPath($GitRoot).TrimEnd([char]'\', [char]'/'),
    [StringComparison]::OrdinalIgnoreCase
)) {
    throw 'Extract Phase 173 R2R1 ZIP at repository root'
}

Push-Location $Root
try {
    Write-Output 'PHASE173_FINAL_R2R1_SCOPE=PRIOR_EVIDENCE_PATH_AND_REVIEWED_FAST_FORWARD'
    Write-Output 'PHASE173_FINAL_R2R1_GIT_RESET_CLEAN_STAGE_COMMIT=NONE'
    Write-Output 'PHASE173_FINAL_R2R1_FULL_PYTEST=False'
    $BeforeIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Unable to record Git index tree' }

    Write-Output '=== R2R1 REVIEWED PATCH CONTRACT TESTS ==='
    & python -B -m pytest -q -p no:cacheprovider `
        phase173_final_gate_r2r1_evidence_path_recovery/tests/test_patch_contract.py
    if ($LASTEXITCODE -ne 0) { throw 'R2R1 patch contract tests failed' }

    if ($DryRun) {
        & python -B -m phase173_final_gate_r2r1_evidence_path_recovery.patch `
            --repo $Root --package $Package
        if ($LASTEXITCODE -ne 0) { throw 'R2R1 DryRun source guard failed' }
        Write-Output 'PHASE173_FINAL_R2R1_DRY_RUN=PASS'
    }
    else {
        & python -B -m phase173_final_gate_r2r1_evidence_path_recovery.patch `
            --repo $Root --package $Package --apply
        if ($LASTEXITCODE -ne 0) { throw 'R2R1 install failed' }
        Write-Output '=== R2R1 CORRECTED R2 GATE FOCUSED TESTS ==='
        & python -B -m pytest -q -p no:cacheprovider `
            phase173_final_gate_r2_recovery/tests/test_gate_contract.py `
            phase173_final_gate_r2r1_evidence_path_recovery/tests/test_patch_contract.py
        if ($LASTEXITCODE -ne 0) {
            & python -B -m phase173_final_gate_r2r1_evidence_path_recovery.patch `
                --repo $Root --package $Package --rollback
            throw 'R2R1 focused pytest failed; original files restored'
        }
        Write-Output 'PHASE173_FINAL_R2R1_FOCUSED_PYTEST=PASS'
        Write-Output 'PHASE173_FINAL_R2R1_APPLY=PASS'
    }

    $AfterIndex = (& git --no-pager write-tree).Trim()
    if ($LASTEXITCODE -ne 0 -or $BeforeIndex -ne $AfterIndex) {
        throw 'R2R1 modified Git index'
    }
    Write-Output 'PHASE173_FINAL_R2R1_GIT_INDEX_PRESERVED=PASS'
    & git --no-pager status -sb
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read Git status' }
    & git --no-pager diff --stat
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read Git diff' }
}
finally {
    Pop-Location
}

```

## tests/test_patch_contract.py

```python
"""Review source-safety and unchanged R2 mathematical proof boundaries."""
from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_final_gate_r2r1_evidence_path_recovery import patch


PACKAGE = Path(__file__).resolve().parents[1]
REPLACEMENT_GATE = PACKAGE / "replacement" / "gate.py"
REPLACEMENT_RUNNER = PACKAGE / "replacement" / "run.ps1"


def _load_replacement_gate():
    spec = importlib.util.spec_from_file_location("phase173_r2r1_gate_review", REPLACEMENT_GATE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _copy_originals(tmp_path: Path) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    target = repo / patch.TARGET_DIR
    target.mkdir(parents=True)
    new_package = tmp_path / "package"
    (new_package / "replacement").mkdir(parents=True)
    for name, original in patch.ORIGINAL_SHA256.items():
        fixture = PACKAGE / "tests" / "fixtures" / name
        assert patch.digest(fixture.read_bytes()) == original
        shutil.copyfile(fixture, target / name)
        shutil.copyfile(PACKAGE / "replacement" / name,
                        new_package / "replacement" / name)
    return repo, new_package


def test_replacements_are_whole_valid_source_files() -> None:
    import ast

    source = REPLACEMENT_GATE.read_text(encoding="utf-8")
    ast.parse(source)
    assert "def validate_snapshot" in source
    assert "def verify_prior_failure" in source
    assert "def finalize" in source
    assert "-PreviousEvidencePath" not in source
    script = REPLACEMENT_RUNNER.read_text(encoding="utf-8")
    assert "[string]$PreviousEvidencePath" in script
    assert "C:\\Users\\oomae\\AppData\\Local" in script
    assert "Test-CompletePreviousEvidence" in script
    assert "PHASE173_FINAL_R2_PRIOR_EVIDENCE_DIR=" in script
    for name in (
        "phase173_full_test_report.json",
        "phase173_full_test_attempt.json",
        "active_suite_stdout.txt",
        "active_suite_stderr.txt",
    ):
        assert name in script


def test_original_hashes_are_pinned() -> None:
    assert set(patch.ORIGINAL_SHA256) == {"gate.py", "run.ps1"}
    assert all(len(value) == 64 for value in patch.ORIGINAL_SHA256.values())
    assert patch.digest(b"hello") != patch.digest(b"HELLO")


def test_actual_reviewed_patch_apply_idempotent_and_rollback(tmp_path: Path) -> None:
    repo, new_package = _copy_originals(tmp_path)
    source_dir = repo / patch.TARGET_DIR
    applied = patch.apply_reviewed_patch(repo, new_package)
    assert len(applied) == 2
    assert all(state == "ALREADY_PATCHED"
               for _, _, state in patch.reviewed_files(repo, new_package))
    for name in patch.ORIGINAL_SHA256:
        assert (new_package / "original_backups" / name).read_bytes() == (
            PACKAGE / "tests" / "fixtures" / name
        ).read_bytes()
        assert (source_dir / name).read_bytes() == (
            PACKAGE / "replacement" / name
        ).read_bytes()
    assert patch.apply_reviewed_patch(repo, new_package) == ()
    restored = patch.rollback_reviewed_patch(repo, new_package)
    assert len(restored) == 2
    for name in patch.ORIGINAL_SHA256:
        assert patch.digest((source_dir / name).read_bytes()) == patch.ORIGINAL_SHA256[name]


def test_unreviewed_source_is_refused(tmp_path: Path) -> None:
    repo = tmp_path
    target = repo / patch.TARGET_DIR
    target.mkdir()
    (target / "gate.py").write_text("unsafe modification", encoding="utf-8")
    (target / "run.ps1").write_bytes(REPLACEMENT_RUNNER.read_bytes())
    with pytest.raises(RuntimeError, match="unreviewed local edits"):
        patch.reviewed_files(repo, PACKAGE)


def test_missing_source_is_refused(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="missing"):
        patch.reviewed_files(tmp_path, PACKAGE)


def test_fully_patched_source_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / patch.TARGET_DIR
    target.mkdir()
    for name in patch.ORIGINAL_SHA256:
        shutil.copyfile(PACKAGE / "replacement" / name, target / name)
    states = patch.reviewed_files(tmp_path, PACKAGE)
    assert all(state == "ALREADY_PATCHED" for _, _, state in states)


def test_atomic_write_refuses_stale_temp_file(tmp_path: Path) -> None:
    target = tmp_path / "source.py"
    target.write_text("old", encoding="utf-8")
    temp = tmp_path / "source.py.phase173_r2r1_tmp"
    temp.write_text("unreviewed", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Stale temporary"):
        patch._atomic_write(target, b"new")
    assert target.read_text(encoding="utf-8") == "old"
    assert temp.read_text(encoding="utf-8") == "unreviewed"


def test_reviewed_gate_accepts_only_approved_remote_fast_forward(tmp_path: Path) -> None:
    gate = _load_replacement_gate()
    for path in gate.REPAIRED_TEST_SHA256:
        file = tmp_path / path
        file.parent.mkdir(parents=True, exist_ok=True)
        # Replace reviewed hashes with a synthetic but precisely hashed test.
        file.write_bytes(b"reviewed_r1_fix = True\r\n")
    gate.REPAIRED_TEST_SHA256 = {
        key: gate.normalized_digest(b"reviewed_r1_fix = True\n")
        for key in gate.REPAIRED_TEST_SHA256
    }
    remote = "25b1ee1f7c848356604061991db06265cfccb296"
    def fake_git(repo: Path, *args: str, allow_nonzero: bool = False):
        if args == ("rev-parse", "--show-toplevel"):
            answer = str(repo)
        elif args == ("branch", "--show-current"):
            answer = "develop"
        elif args == ("rev-parse", "HEAD"):
            answer = gate.REVIEWED_BASE
        elif args == ("rev-parse", "origin/develop"):
            answer = remote
        elif args[0] == "rev-parse" and args[1].startswith("origin/develop:"):
            path = args[1].removeprefix("origin/develop:")
            answer = gate.APPROVED_REMOTE_R1_BLOBS.get(path, gate.REVIEWED_BLOBS.get(path, ""))
        elif args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            answer = gate.REVIEWED_BLOBS.get(args[1][5:], "")
        elif args[:2] == ("diff", "--name-only"):
            answer = "\n".join(gate.REPAIRED_TEST_SHA256)
        elif args == ("write-tree",):
            answer = "immutable-index-tree"
        else:
            answer = ""
        return SimpleNamespace(stdout=answer, returncode=0, stderr="")
    gate.git = fake_git
    snapshot = gate.validate_snapshot(tmp_path)
    assert snapshot["head"] == gate.REVIEWED_BASE
    assert snapshot["remote_head"] == remote
    assert snapshot["repaired_test_count"] == 3


def test_reviewed_gate_refuses_diverging_remote(tmp_path: Path) -> None:
    gate = _load_replacement_gate()
    original = gate.git
    def fake_git(repo: Path, *args: str, allow_nonzero: bool = False):
        if args == ("rev-parse", "--show-toplevel"):
            return SimpleNamespace(stdout=str(repo), returncode=0, stderr="")
        if args == ("branch", "--show-current"):
            return SimpleNamespace(stdout="develop", returncode=0, stderr="")
        if args == ("rev-parse", "HEAD"):
            return SimpleNamespace(stdout=gate.REVIEWED_BASE, returncode=0, stderr="")
        if args == ("rev-parse", "origin/develop"):
            return SimpleNamespace(stdout="not-on-same-history", returncode=0, stderr="")
        if args[:2] == ("merge-base", "--is-ancestor"):
            # The remote does not descend from the reviewed base.
            return SimpleNamespace(stdout="", returncode=1, stderr="")
        return original(repo, *args, allow_nonzero=allow_nonzero)
    gate.git = fake_git
    with pytest.raises(RuntimeError, match="not descended"):
        gate.validate_snapshot(tmp_path)


def test_existing_failure_evidence_check_is_unchanged() -> None:
    gate = _load_replacement_gate()
    assert len(gate.EXPECTED_PREVIOUS_FAILURES) == 5
    assert gate.EXPECTED_ACTIVE_PASSED == 3546
    assert gate.ACTIVE_SUITE_COMMAND.endswith("tests")
    assert gate.verify_prior_failure.__doc__.startswith("Require the precise")


def test_no_restart_of_full_pytest_in_patch_runner() -> None:
    script = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "phase173_final_gate_r2_recovery/tests/test_gate_contract.py" in script
    assert "PHASE173_FINAL_R2R1_FULL_PYTEST=False" in script
    assert "PHASE173_FINAL_R2R1_APPLY=PASS" in script

```

## README.md

```markdown
# Phase 173 Final Gate R2R1 — Previous Evidence Location Recovery

This package repairs **only** the existing `phase173_final_gate_r2_recovery/gate.py` and `run.ps1` preflight/runner. It does not change mathematical proof rules, renderers, registered statements, project documentation, or the active `tests/` suite. It does not execute a full suite during patch installation.

## Verified failure and cause

The 2026-11-04 corrective R2 `-DryRun` stopped at `verify_prior_failure()` with `Previous Phase 173 failure evidence is incomplete` **after 14 gate tests passed**. The active suite was not re-executed. R2 originally used the current user's `%LOCALAPPDATA%`, but the earlier failed Phase 173 final gate reported its original evidence under `C:\Users\oomae\AppData\Local\EHPProofTracerRecovery\phase173_final_gate`. The subsequent command was executed as `C:\Users\user\...`. This account-path difference explains why the prior file set could not be found; actual access to the earlier path still needs to be verified on Windows.

Separately, the reviewed GitHub `develop` advanced from `ac9149beaf91eeef382bc816234bd2d895398667` to `25b1ee1f7c848356604061991db06265cfccb296` by committing the three approved Phase 167 reference tests and final gate packages. The corrected snapshot check accepts this specific *type* of reviewed fast-forward, including local unstaged tests identical to the approved R1 patch. It does not fetch or merge files into the user's local checkout, stage changes, reset branches, or erase the original failure.

## Inputs and precise boundaries

Original source files must be byte-for-byte the earlier R2 distribution (`gate.py` SHA-256 `f282ff57...`, `run.ps1` SHA-256 `0892e724...`) or already equal the fully reviewed replacement. The patch program rejects any unknown local alterations and preserves the original bytes under `phase173_final_gate_r2r1_evidence_path_recovery/original_backups/` before replacement.

The repaired `run.ps1` selects one **existing** four-file prior-evidence directory, in this order: explicitly supplied `-PreviousEvidencePath`, complete evidence under current `%LOCALAPPDATA%`, and complete evidence under the previously reported `C:\Users\oomae\AppData\Local\EHPProofTracerRecovery\phase173_final_gate`. A missing/inaccessible directory produces an explicit missing-file report and does not start the active suite. The original data are **read only**, never silently fabricated, copied, overwritten or removed. The existing R2 verifier still checks the previous report's `FAIL`, pytest exit code 1, five named failures, and `5 failed, 3541 passed` summary.

The reviewed code hashes, committed path allowlist, and exact three repaired-test SHA-256 digests remain required. If `origin/develop` advances beyond the reviewed source or changes any non-approved file, the corrected gate still fails closed. Local and remote history must be an actual fast-forward, not a divergence. Source blobs are checked on both sides of a reviewed HEAD mismatch.

## Install and execute

From the Git repository root in PowerShell:

```powershell
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\EHP_Phase173_FINAL_GATE_R2R1_PRIOR_EVIDENCE_PATH_FIX.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_final_gate_r2r1_evidence_path_recovery\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R2R1 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_final_gate_r2r1_evidence_path_recovery\run.ps1"
if ($LASTEXITCODE -ne 0) { throw 'R2R1 install failed' }
```

This performs **focused tests only**. To run the repaired R2 gate, call the original R2 path, optionally specifying an actual previous-evidence directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_final_gate_r2_recovery\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw 'Corrected R2 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_final_gate_r2_recovery\run.ps1"
if ($LASTEXITCODE -ne 0) { throw 'Corrected R2 final gate failed' }
```

If the original failure files are at a different location, add `-PreviousEvidencePath 'C:\actual\path\to\phase173_final_gate'` to **both** corrected R2 calls. Do not create dummy reports or reuse the new R2 evidence directory as the old failure source.

## Completion conditions

R2R1 patch: `PHASE173_FINAL_R2R1_INSTALL=PASS`, `PHASE173_FINAL_R2R1_FOCUSED_PYTEST=PASS`, `PHASE173_FINAL_R2R1_APPLY=PASS`, and Git index preservation. Corrected R2 dry run: `PHASE173_FINAL_R2_PRIOR_FAILURE_PRESERVED=PASS` and `PHASE173_FINAL_R2_PREFLIGHT=PASS`. The subsequent normal R2 run must report `3546 passed` and exit code zero **before** claiming the final active suite succeeded. Phase 173 remains formally open until the final evidence is documented and reviewed; browser pixel-level MathJax layout is independently unconfirmed.

```

## design.md

```markdown
# Phase 173 Final Gate R2R1 — 過去の失敗証拠の参照先修正

## 適用前の監査

2026-11-04 の R2 `-DryRun` は限定 Gate テスト14件を PASS した後、`verify_prior_failure()` が `Previous Phase 173 failure evidence is incomplete` で停止した。これは全体 pytest の再実行前である。R2 は `$env:LOCALAPPDATA` 配下に4ファイルがあることを要求する。一方、第1回の全体テストの失敗ログは `C:\Users\oomae\AppData\Local\EHPProofTracerRecovery\phase173_final_gate\` に記録され、今回の実行プロファイルは `C:\Users\user` になっている。原因候補は実際の保存先と検査先の不一致であり、前回記録の存在およびアクセス可能性は Windows 環境での検査が必要である。

GitHub `akebono03/ehp-proof-tracer` の `develop` について、修正前基準 `ac9149beaf91eeef382bc816234bd2d895398667` と、現行 `25b1ee1f7c848356604061991db06265cfccb296` の差分を確認した。追加対象は最終 Gate 補助ファイルと Phase 167 の3テストで、数学的な Proof Tree / Renderer の変更はない。R2 Gate の元コード・関連14テストを確認済みである。

## 変更対象

- `phase173_final_gate_r2_recovery/gate.py`
  - 既存 `validate_snapshot()`：ローカルとリモートの承認済み fast-forward（早送り）を、差分対象・既存の15 Source Blob・修正済み3テストの SHA-256 で検査する。divergence（履歴分岐）、未審査の変更は拒否する。
  - 既存 `finalize()`：テスト報告に `remote_head` を追加する。従来のテスト用 snapshot で未指定の場合はローカル HEAD を使い既存 API を維持する。
  - 既存 `main()`：remote HEAD をログに明示する。
  - 新規定数 `BASE_R1_TEST_BLOBS` と `APPROVED_REMOTE_R1_BLOBS`：上記承認済み3テストの Git Blob を保持する。
- `phase173_final_gate_r2_recovery/run.ps1`：`-PreviousEvidencePath` オプションを追加。元の失敗レポートが保存されたアカウントと現在のアカウントを区別し、完全な4ファイルが存在する場合だけ続行する。元の失敗証拠を直接読み取り、コピー・削除・上書きをしない。
- 新規 `phase173_final_gate_r2r1_evidence_path_recovery/patch.py`、`run.ps1`、`tests/test_patch_contract.py`：元 R2 ソースのバイト一致検査、バックアップ、安全な置き換え、限定テストを実装する。

既存数学実装、既存の5件の失敗内容、証明の Trust Boundary（信頼境界）、テストの集合、文書5件は変更しない。

## 実行境界

R2R1 の `DryRun` と通常適用は、Gate 補助ファイルの修復と関連 pytest のみ。**全体 pytest を実行しない。** 修復が成功した後に、元の `phase173_final_gate_r2_recovery/run.ps1` を `-DryRun`、通常実行の順に別途実行する。正常時には現行 `tests/` の 3,546件 PASS、終了コード0を期待するが、この ZIP の作成時点ではその実測結果をまだ確認していない。

失敗記録のファイル名は `phase173_full_test_report.json`、`phase173_full_test_attempt.json`、`active_suite_stdout.txt`、`active_suite_stderr.txt` である。存在確認に成功しても R2 の `verify_prior_failure()` で形式、5件の名前、件数まで検査する。ユーザーが元ファイルにアクセスできない場合、`-PreviousEvidencePath` で元の実在ディレクトリを指定する。ファイルを架空に生成して Gate を通さない。

新しい R2 結果は現在のプロファイルの `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_final_gate_r2\` に別保存し、以前の `phase173_final_gate` を変更しない。成功後も Phase 173 終了文書への追記と最終レビューが必要である。

```

