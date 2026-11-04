# Phase 173 Final R2 — 完全な追加コードと import

新規ディレクトリ `phase173_final_gate_r2_recovery/` に限る。既存の関数・クラス・import は変更しない。
`gate.py` の import、定数、全関数、`run.ps1` 全文、テストの import と全テスト関数を掲載する。

## `gate.py` 全文

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
```

## `run.ps1` 全文

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
$PreviousEvidence = Join-Path $RecordParent 'EHPProofTracerRecovery\phase173_final_gate'
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

## `tests/test_gate_contract.py` 全文

```python
"""Corrective phase-end gate contracts: exact fixes, evidence and retry safety."""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_final_gate_r2_recovery import gate


def test_reviewed_replacement_hashes_match_r1_source() -> None:
    reviewed = Path(__file__).resolve().parents[1] / "reviewed_test_replacements"
    for path, digest in gate.REPAIRED_TEST_SHA256.items():
        assert gate.normalized_digest((reviewed / Path(path).name).read_bytes()) == digest


def test_line_ending_only_differences_produce_equal_hash() -> None:
    content = b"a = 1\nb = 2\n"
    windows = b"a = 1\r\nb = 2\r\n"
    assert gate.normalized_digest(content) == gate.normalized_digest(windows)


def test_actual_statement_edits_do_not_pass_digest() -> None:
    assert gate.normalized_digest(b"a = 1\n") != gate.normalized_digest(b"a = 2\n")


def test_reviewed_history_allows_only_gate_packages_and_three_fixes() -> None:
    assert gate.permitted_committed_changes([
        "tests/test_phase167_r2_range_dedup.py",
        "phase173_final_gate/run.ps1",
        "phase173_final_gate_r1_phase167_reference_contract/README.md",
        "phase173_final_gate_r2_recovery/gate.py",
    ])
    assert not gate.permitted_committed_changes([
        "phase168_r3_5_model_renderer.py",
    ])


def _prior_files(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    payload = {
        "phase": 173,
        "head": gate.REVIEWED_BASE,
        "status": "FAIL",
        "pytest_exit_code": 1,
    }
    (directory / "phase173_full_test_report.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )
    output = "\n".join(
        "FAILED " + name.replace("/", "\\")
        for name in gate.EXPECTED_PREVIOUS_FAILURES
    ) + "\n5 failed, 3541 passed in 34.43s\n"
    (directory / "active_suite_stdout.txt").write_text(output, encoding="utf-8")
    (directory / "active_suite_stderr.txt").write_text("", encoding="utf-8")
    (directory / "phase173_full_test_attempt.json").write_text(
        '{"status":"STARTED"}', encoding="utf-8"
    )


def test_prior_failure_evidence_is_read_only_and_complete(tmp_path: Path) -> None:
    _prior_files(tmp_path)
    before = (tmp_path / "phase173_full_test_report.json").read_bytes()
    hashes = gate.verify_prior_failure(tmp_path)
    assert len(hashes) == 4
    assert hashes["phase173_full_test_report.json"] == gate.sha256_file(
        tmp_path / "phase173_full_test_report.json"
    )
    assert (tmp_path / "phase173_full_test_report.json").read_bytes() == before


def test_prior_failure_rejects_missing_expected_case(tmp_path: Path) -> None:
    _prior_files(tmp_path)
    file = tmp_path / "active_suite_stdout.txt"
    file.write_text("5 failed, 3541 passed in 34.43s\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Missing reviewed failure"):
        gate.verify_prior_failure(tmp_path)


def test_prior_failure_rejects_wrong_result_status(tmp_path: Path) -> None:
    _prior_files(tmp_path)
    file = tmp_path / "phase173_full_test_report.json"
    report = json.loads(file.read_text(encoding="utf-8"))
    report["status"] = "PASS"
    file.write_text(json.dumps(report), encoding="utf-8")
    with pytest.raises(RuntimeError, match="does not match"):
        gate.verify_prior_failure(tmp_path)


def test_summary_requires_exact_active_count() -> None:
    count, summary = gate.parse_success_summary(
        "..... [100%]\n3546 passed in 51.20s\n", 0
    )
    assert count == gate.EXPECTED_ACTIVE_PASSED
    assert summary == "3546 passed in 51.20s"
    with pytest.raises(ValueError, match="count changed"):
        gate.parse_success_summary("3545 passed in 51.20s\n", 0)


def test_summary_rejects_nonzero_exit_and_bad_counts() -> None:
    with pytest.raises(ValueError, match="code zero"):
        gate.parse_success_summary("5 failed, 3541 passed in 34.43s", 1)
    with pytest.raises(ValueError, match="not found"):
        gate.parse_success_summary("no completed test summary", 0)


def _snapshot() -> dict[str, object]:
    return {
        "head": gate.REVIEWED_BASE,
        "git_index_tree": "reviewed-git-index-tree",
        "reviewed_blob_count": 15,
        "repaired_test_count": 3,
    }


def test_exclusive_attempt_refuses_duplicate(tmp_path: Path) -> None:
    attempt = tmp_path / "attempt.json"
    gate.start_attempt(attempt, _snapshot(), {"old": "sha256"})
    assert json.loads(attempt.read_text(encoding="utf-8"))["status"] == "STARTED"
    with pytest.raises(FileExistsError):
        gate.start_attempt(attempt, _snapshot(), {"old": "sha256"})


def test_success_report_is_recorded_once_and_matched(tmp_path: Path) -> None:
    snapshot = _snapshot()
    prior = {"old": "sha256"}
    attempt = tmp_path / "attempt.json"
    report_file = tmp_path / "report.json"
    stdout = tmp_path / "stdout.txt"
    stderr = tmp_path / "stderr.txt"
    gate.start_attempt(attempt, snapshot, prior)
    stdout.write_text("3546 passed in 36.00s\n", encoding="utf-8")
    stderr.write_text("", encoding="utf-8")
    report = gate.finalize(snapshot, prior, attempt, report_file, stdout, stderr, 0)
    assert report["status"] == "PASS"
    assert report["phase_formally_closed"] is False
    assert gate.validate_recorded_success(report_file, snapshot, prior) is True
    with pytest.raises(RuntimeError, match="refusing to replace"):
        gate.finalize(snapshot, prior, attempt, report_file, stdout, stderr, 0)


def test_failed_corrective_run_still_saves_distinct_report(tmp_path: Path) -> None:
    snapshot = _snapshot()
    attempt = tmp_path / "attempt.json"
    report_file = tmp_path / "report.json"
    stdout = tmp_path / "stdout.txt"
    stderr = tmp_path / "stderr.txt"
    prior = {"old": "sha256"}
    gate.start_attempt(attempt, snapshot, prior)
    stdout.write_text("1 failed, 3545 passed in 36.00s", encoding="utf-8")
    stderr.write_text("", encoding="utf-8")
    recorded = gate.finalize(snapshot, prior, attempt, report_file, stdout, stderr, 1)
    assert recorded["status"] == "FAIL"
    with pytest.raises(RuntimeError, match="not a matching success"):
        gate.validate_recorded_success(report_file, snapshot, prior)


def test_stale_prior_evidence_cannot_be_reused(tmp_path: Path) -> None:
    snapshot = _snapshot()
    attempt = tmp_path / "attempt.json"
    report_file = tmp_path / "report.json"
    stdout = tmp_path / "stdout.txt"
    stderr = tmp_path / "stderr.txt"
    gate.start_attempt(attempt, snapshot, {"old": "sha256"})
    stdout.write_text("3546 passed in 36.00s", encoding="utf-8")
    stderr.write_text("", encoding="utf-8")
    with pytest.raises(RuntimeError, match="does not match"):
        gate.finalize(snapshot, {"old": "different"}, attempt,
                      report_file, stdout, stderr, 0)
    assert not report_file.exists()


def test_snapshot_checks_guarded_changes_with_mock_git(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    original = dict(gate.REPAIRED_TEST_SHA256)
    try:
        for path in original:
            location = tmp_path / path
            location.parent.mkdir(parents=True, exist_ok=True)
            location.write_bytes(b"reviewed = True\r\n")
        monkeypatch.setattr(
            gate, "REPAIRED_TEST_SHA256",
            {key: gate.normalized_digest(b"reviewed = True\n") for key in original},
        )
        def mocked_git(repo: Path, *args: str, allow_nonzero: bool = False):
            if args == ("rev-parse", "--show-toplevel"):
                value = str(repo)
            elif args == ("branch", "--show-current"):
                value = "develop"
            elif args == ("rev-parse", "HEAD"):
                value = gate.REVIEWED_BASE
            elif args == ("rev-parse", "origin/develop"):
                value = gate.REVIEWED_BASE
            elif args[0] == "rev-parse" and args[1].startswith("HEAD:"):
                value = gate.REVIEWED_BLOBS[args[1][5:]]
            elif args[:2] == ("diff", "--name-only"):
                value = "\n".join(original.keys())
            elif args == ("write-tree",):
                value = "mock-index-tree"
            else:
                value = ""
            return SimpleNamespace(stdout=value, returncode=0, stderr="")
        monkeypatch.setattr(gate, "git", mocked_git)
        snapshot = gate.validate_snapshot(tmp_path)
        assert snapshot["repaired_test_count"] == 3
        assert snapshot["reviewed_blob_count"] == 15
    finally:
        gate.REPAIRED_TEST_SHA256.clear()
        gate.REPAIRED_TEST_SHA256.update(original)
```

## `reviewed_test_replacements/test_phase167_r2_range_dedup.py`（R1 監査済み内容）

```python
"""Phase 167 reference rules under the Phase 168 common Model Renderer."""
from web_group_proof import build_standard_web_group_proof_view


def _reference_text(n: int, k: int) -> str:
    view = build_standard_web_group_proof_view(n, k, 2, "narrative")
    assert view.key == "generic-complete-proof"
    lines = view.rendered_lines

    def is_section(line, title):
        return (line.kind in ("text", "heading")
                and line.prefix == title and line.statement_latex is None
                and line.suffix == "")

    first = next(i for i, line in enumerate(lines)
                 if is_section(line, "使用する結果"))
    # The canonical Web layout replaces the old Proof heading with a
    # single separator; Reference assertions must exclude the proof body.
    separators = [
        i for i, line in enumerate(lines)
        if i > first and line.kind == "separator"
    ]
    assert len(separators) == 1
    last = separators[0]
    assert first < last
    return "\n".join(
        " ".join((line.prefix, line.statement_latex or "", line.suffix))
        for line in lines[first + 1:last]
    )


def test_phase167_r2_pi32_diagonal_range_once():
    reference = _reference_text(2, 1)
    diagonal = next(line for line in reference.splitlines() if r"\pi_{n}^{n}" in line)
    assert diagonal.count(r"n\ge 1") == 1
    assert reference.count(r"\pi_{n}^{n}") == 1
    assert r"\pi_i^1=0" in reference
    assert "Proposition 5.1" in reference


def test_phase167_r2_pi43_diagonal_range_once():
    reference = _reference_text(3, 1)
    diagonal = next(line for line in reference.splitlines() if r"\pi_{n}^{n}" in line)
    assert diagonal.count(r"n\ge 1") == 1
    assert reference.count(r"\pi_{n}^{n}") == 1
    assert r"\pi_i^n=0" in reference
    assert "Proposition 5.1" in reference
```

## `reviewed_test_replacements/test_phase167_r2_shared_reference.py`（R1 監査済み内容）

```python
"""Phase 167 shared reference projection under the Phase 168 Web route."""
from web_group_proof import build_standard_web_group_proof_view
from toda_group_proof_narrative_references import (
    TodaGroupProofNarrativeReferenceEntry,
    render_toda_group_proof_narrative_reference_entries_markdown,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep


def test_phase167_r2_pi43_reference_has_two_general_results():
    view = build_standard_web_group_proof_view(3, 1, 2, "narrative")
    assert view.key == "generic-complete-proof"
    lines = view.rendered_lines

    def is_section(line, title):
        return (line.kind in ("text", "heading")
                and line.prefix == title and line.statement_latex is None
                and line.suffix == "")

    reference_index = next(
        i for i, line in enumerate(lines)
        if is_section(line, "使用する結果")
    )
    # The common Web layout turns the former Proof heading into exactly one
    # separator. Keep the boundary semantic instead of relying on the old title.
    separators = [
        i for i, line in enumerate(lines)
        if i > reference_index and line.kind == "separator"
    ]
    assert len(separators) == 1
    proof_index = separators[0]
    reference_lines = lines[reference_index + 1:proof_index]
    reference_text = "\n".join(
        " ".join((line.prefix, line.statement_latex or "", line.suffix))
        for line in reference_lines
    )
    assert r"\pi_{n}^{n}" in reference_text
    assert r"\pi_i^n=0" in reference_text
    assert "Proposition 5.1" in reference_text
    assert reference_text.count(r"\pi_{n}^{n}") == 1


def test_phase167_r2_other_references_keep_common_statement_lines():
    ref = LiteratureReference(label="Generic source", locator="Generic source")
    step = ProofStep(
        conclusion="general claim",
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="generic",
            literature_reference=ref,
        ),
    )
    entry = TodaGroupProofNarrativeReferenceEntry(
        number=1,
        reference=ref,
        proof_steps=(step,),
    )
    rendered = render_toda_group_proof_narrative_reference_entries_markdown(
        (entry,),
        {1: ("$x=y$",)},
    )
    assert "$x=y$" in rendered
    assert "**[R1] Generic source.**" in rendered
```

## `reviewed_test_replacements/test_phase167_r2_unified_reference.py`（R1 監査済み内容）

```python
"""Phase 167 general references against the current common Renderer output."""
from web_group_proof import build_standard_web_group_proof_view


def _reference_text(n: int, k: int) -> str:
    view = build_standard_web_group_proof_view(n, k, 2, "narrative")
    assert view.key == "generic-complete-proof"
    lines = view.rendered_lines

    def is_section(line, title):
        return (line.kind in ("text", "heading")
                and line.prefix == title and line.statement_latex is None
                and line.suffix == "")

    first = next(i for i, line in enumerate(lines)
                 if is_section(line, "使用する結果"))
    # The canonical Web layout replaces the old Proof heading with a
    # single separator; Reference assertions must exclude the proof body.
    separators = [
        i for i, line in enumerate(lines)
        if i > first and line.kind == "separator"
    ]
    assert len(separators) == 1
    last = separators[0]
    assert first < last
    return "\n".join(
        " ".join((line.prefix, line.statement_latex or "", line.suffix))
        for line in lines[first + 1:last]
    )


def test_phase167_r2_pi32_reference_uses_general_form():
    text = _reference_text(2, 1)
    assert r"\pi_i^1=0" in text
    assert r"\pi_{n}^{n}" in text
    assert r"\pi_{3}^{3}" not in text
    assert r"\pi_{2}^{1}" not in text
    assert "Proposition 5.1" in text


def test_phase167_r2_pi43_reference_uses_general_form():
    text = _reference_text(3, 1)
    assert r"\pi_{n}^{n}" in text
    assert r"\pi_i^n=0" in text
    assert text.count(r"\pi_{n}^{n}") == 1
    assert "Proposition 5.1" in text
```
