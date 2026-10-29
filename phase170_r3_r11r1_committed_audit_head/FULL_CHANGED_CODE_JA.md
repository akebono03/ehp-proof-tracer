# Phase 170 R3-R11R1 — 新規追加コード全文

既存の本体 Python、既存テスト、既存文書は変更しない。新規ディレクトリ `phase170_r3_r11r1_committed_audit_head/` をリポジトリ直下に追加する。import・クラス・関数・テスト・起動スクリプトは各ファイル全文を掲載する。


## `closeout.py`

```python
"""Phase 170 closeout: verify the fresh 33-stem report and run the active test suite.

This audit does not alter application code or claim a proof beyond the recorded
search/Web results. Full active pytest runs only after the domain audit checks.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import traceback

EXPECTED_BRANCH = "develop"
EXPECTED_HEAD = "84db682e179203dcbddc1c2c88bc3ccbb31a830f"
AUDITED_HEAD = "08382968b5359d6c956b48acec333f127014d4c8"
REVIEWED_AUDIT_ONLY_PREFIXES = (
    "phase170_r3_r10_n2_33_fresh_audit/",
    "phase170_r3_r10r1_committed_head_audit/",
)
EXPECTED_BLOBS = {
    "phase170_r3_r8_n2_exhaustive_audit/audit.py": "6d95546bf165f11029a7d56d18c03013b3ecafed",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "sources/toda/Toda_07_2.tex": "b5b366f2d2b72d7b419192fa74ab848eff098686",
    "phase168_r2_toda52_transport.py": "f417cf7b828c898f7e957defd3b47056016cb585",
    "phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py": "bc78a9732230ce4af021bbc9b218a4153d3af96e",
    "phase170_r3_r9_toda712_cited_rewrite/source712.py": "895c7b731a01b2497c053b9c8707ced9fa4a860f",
}
WORKER_PATH = "phase170_r3_r8_n2_exhaustive_audit/audit.py"
DOMAIN = tuple(range(1, 34))
ACTIVE_TEST_ARGS = (
    "-B", "-m", "pytest", "-q", "--tb=short",
    "--disable-warnings", "-p", "no:cacheprovider", "tests",
)


def git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=root, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if process.returncode:
        error = process.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {error}")
    return process.stdout.decode("utf-8", errors="replace").strip()


def preflight(root: Path, *, check_remote: bool = True) -> dict:
    """Reject unreviewed revisions or tracked modifications without resetting them."""
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if (branch, head) != (EXPECTED_BRANCH, EXPECTED_HEAD):
        raise RuntimeError(f"unreviewed branch or HEAD: {branch} {head}")
    if check_remote:
        response = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        remote_head = response.split()[0] if response else ""
        if remote_head != EXPECTED_HEAD:
            raise RuntimeError(f"origin/develop has advanced: {remote_head}")
    # The fresh 33/33 report predates a reviewed audit-package-only commit.
    # Accept historical evidence only when the intervening commit adds solely
    # the two known audit packages, never any proof, source, or test files.
    delta = git(root, "diff", "--name-status", AUDITED_HEAD, "HEAD", "--")
    entries = delta.splitlines()
    if not entries:
        raise RuntimeError("reviewed audit-only commit additions are missing")
    for entry in entries:
        status, separator, path = entry.partition("\t")
        if (separator != "\t" or status != "A"
                or not path.startswith(REVIEWED_AUDIT_ONLY_PREFIXES)):
            raise RuntimeError(f"non-audit change after 33/33 report: {entry}")
    if git(root, "diff", "--cached", "--name-only", "--"):
        raise RuntimeError("staged tracked changes present")
    changes = git(root, "diff", "--name-only", "HEAD", "--")
    if changes:
        raise RuntimeError(f"tracked changes present: {changes}")
    for path, blob in EXPECTED_BLOBS.items():
        if git(root, "rev-parse", f"HEAD:{path}") != blob:
            raise RuntimeError(f"committed file differs from reviewed blob: {path}")
        if not (root / path).is_file():
            raise RuntimeError(f"required file is missing: {path}")
    if not (root / "tests").is_dir():
        raise RuntimeError("active tests/ directory is missing")
    return {
        "branch": branch,
        "head": head,
        "audited_head": AUDITED_HEAD,
        "reviewed_audit_additions": entries,
        "reviewed_git_blobs": dict(EXPECTED_BLOBS),
        "worker_sha256": sha256((root / WORKER_PATH).read_bytes()).hexdigest(),
    }


def valid_worker_row(row: object, k: int) -> bool:
    """Require both a completed search and a trust-gated Web result."""
    if not isinstance(row, dict):
        return False
    return (
        type(row.get("k")) is int and row["k"] == k
        and type(row.get("n")) is int and row["n"] == 2
        and type(row.get("group_dimension")) is int
        and row["group_dimension"] == k + 2
        and row.get("toda52_applicable") is True
        and row.get("target_typed") is True
        and row.get("source_precedes") is True
        and row.get("search_status") == "complete"
        and row.get("search_complete") is True
        and type(row.get("open_goals")) is int and row["open_goals"] == 0
        and type(row.get("proven_steps")) is int and row["proven_steps"] > 0
        and row.get("result") == "COMPLETE_AND_WEB_VERIFIED"
        and row.get("audit_result") == "COMPLETE_AND_WEB_VERIFIED"
        and row.get("web_key") == "generic-complete-proof"
        and row.get("web_partial") is False
        and type(row.get("web_steps")) is int and row["web_steps"] > 0
        and type(row.get("web_lines")) is int and row["web_lines"] > 0
        and row.get("web_error") is None
    )


def validate_domain_report(report: object, pre: dict) -> None:
    """Refuse stale, partial, forged-head or non-fresh audit summaries."""
    if not isinstance(report, dict):
        raise ValueError("audit report must be a JSON object")
    if (report.get("phase") != "170 R3-R10"
            or report.get("mode") != "AUDIT_ONLY_FRESH_33"
            or report.get("dry_run") is not False
            or report.get("result") != "DOMAIN_ALL_VERIFIED"
            or report.get("tracked_unchanged") is not True):
        raise ValueError("missing successful fresh-domain audit provenance")
    if (report.get("domain") != list(DOMAIN)
            or report.get("domain_checked") != 33
            or report.get("domain_complete") != 33
            or report.get("domain_gaps") != 0):
        raise ValueError("domain audit counts or scope are inconsistent")
    old_pre = report.get("preflight")
    if not isinstance(old_pre, dict):
        raise ValueError("domain audit has no preflight record")
    if (old_pre.get("branch") != pre["branch"]
            or old_pre.get("head") != AUDITED_HEAD
            or pre.get("audited_head") != AUDITED_HEAD
            or old_pre.get("tracked_changed_paths") != []
            or old_pre.get("worker_sha256") != pre["worker_sha256"]):
        raise ValueError("domain audit was not produced from this reviewed worker/HEAD")
    rows = report.get("rows")
    if not isinstance(rows, list) or len(rows) != 33:
        raise ValueError("domain audit has missing or surplus worker rows")
    if [row.get("k") if isinstance(row, dict) else None for row in rows] != list(DOMAIN):
        raise ValueError("domain audit worker coordinates are not k=1..33 in order")
    if not all(valid_worker_row(row, k) for k, row in zip(DOMAIN, rows)):
        raise ValueError("domain audit has at least one unverified proof or Web result")


def find_verified_report(recovery: Path, pre: dict, requested: Path | None) -> tuple[Path, dict]:
    """Use the latest eligible fresh report, or require the supplied exact path."""
    if requested is not None:
        candidates = [requested]
    else:
        candidates = sorted(
            recovery.glob("phase170_r3_r10_n2_33_*/audit.json"), reverse=True,
        )
    diagnostics: list[str] = []
    for path in candidates:
        try:
            raw = path.read_bytes()
            report = json.loads(raw.decode("utf-8-sig"))
            validate_domain_report(report, pre)
            return path, report
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, KeyError) as exc:
            diagnostics.append(f"{path}: {type(exc).__name__}: {exc}")
    summary = "; ".join(diagnostics[-3:])
    raise RuntimeError("no valid R3-R10 33/33 report found; " + summary)


def run_active_tests(root: Path, log_path: Path) -> tuple[int, str]:
    """Run the same active tests/ command used at Phase 169 closeout once."""
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [sys.executable, *ACTIVE_TEST_ARGS]
    print("PHASE170_R3R11_FULL_PYTEST_START", flush=True)
    print("PHASE170_R3R11_COMMAND=python " + " ".join(ACTIVE_TEST_ARGS), flush=True)
    process = subprocess.Popen(
        command, cwd=root, env=env, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, encoding="utf-8",
        errors="replace", bufsize=1,
    )
    tail = ""
    with log_path.open("w", encoding="utf-8", newline="\n") as handle:
        assert process.stdout is not None
        for line in process.stdout:
            handle.write(line)
            handle.flush()
            print(line, end="", flush=True)
            tail = (tail + line)[-20000:]
    exit_code = process.wait()
    print(f"PHASE170_R3R11_FULL_PYTEST_EXIT={exit_code}", flush=True)
    summaries = re.findall(r"(?m)^.*?\b\d+ passed\b[^\n]*$", tail)
    summary = summaries[-1].strip() if summaries else "NO_PASS_COUNT_IN_OUTPUT"
    print(f"PHASE170_R3R11_FULL_PYTEST_SUMMARY={summary}", flush=True)
    return exit_code, summary


def write_report(path: Path, data: dict) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def run(root: Path, *, dry_run: bool, requested_audit: Path | None = None,
        check_remote: bool = True) -> int:
    recovery = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    recovery.mkdir(parents=True, exist_ok=True)
    output = recovery / ("phase170_r3_r11_active_closeout_"
                         + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    report: dict = {
        "phase": "170 R3-R11", "mode": "PHASE_END_ACTIVE_SUITE",
        "dry_run": dry_run, "full_pytest": not dry_run,
        "production_modified": False,
        "active_command": ["python", *ACTIVE_TEST_ARGS],
    }
    print("PHASE170_R3R11_MODE=PHASE_END_ACTIVE_SUITE", flush=True)
    print(f"PHASE170_R3R11_OUTPUT={output}", flush=True)
    rc = 2
    pre = None
    try:
        pre = preflight(root, check_remote=check_remote)
        report["preflight"] = pre
        evidence_path, evidence = find_verified_report(recovery, pre, requested_audit)
        report["domain_report"] = str(evidence_path)
        report["domain_report_sha256"] = sha256(evidence_path.read_bytes()).hexdigest()
        report["domain_checked"] = evidence["domain_checked"]
        report["domain_complete"] = evidence["domain_complete"]
        report["domain_gaps"] = evidence["domain_gaps"]
        print("PHASE170_R3R11_DOMAIN_REPORT=VERIFIED_33_OF_33", flush=True)
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
            rc = 0
            print("PHASE170_R3R11_DRY_RUN=PASS", flush=True)
        else:
            exit_code, summary = run_active_tests(root, output / "full_pytest.log")
            report["pytest_exit"] = exit_code
            report["pytest_summary"] = summary
            report["result"] = "FULL_SUITE_PASS" if exit_code == 0 else "FULL_SUITE_FAILED"
            rc = 0 if exit_code == 0 else 1
    except Exception as exc:
        report["result"] = "REFUSED_OR_ERROR"
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["traceback"] = traceback.format_exc()[-3000:]
        print(f"PHASE170_R3R11_REFUSED={report['error']}", flush=True)
    finally:
        if pre is not None:
            try:
                post = preflight(root, check_remote=False)
                report["tracked_unchanged"] = post == pre
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = f"{type(exc).__name__}: {exc}"
            if not report["tracked_unchanged"]:
                report["result"] = "TRACKED_STATE_CHANGED"
                rc = 2
        else:
            report["tracked_unchanged"] = None
        write_report(output / "closeout.json", report)
        print(f"PHASE170_R3R11_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print(f"PHASE170_R3R11_REPORT={output / 'closeout.json'}", flush=True)
        print(f"PHASE170_R3R11_RESULT={report['result']}", flush=True)
    return rc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--audit-report", type=Path)
    args = parser.parse_args()
    return run(args.root.resolve(), dry_run=args.dry_run,
               requested_audit=args.audit_report.resolve() if args.audit_report else None)


if __name__ == "__main__":
    raise SystemExit(main())
```


## `run.ps1`

```powershell
param(
    [switch]$DryRun,
    [string]$AuditReport = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OriginalPythonPath = $env:PYTHONPATH
$OriginalPythonEncoding = $env:PYTHONIOENCODING
$OriginalUtf8 = $env:PYTHONUTF8
$OriginalNoBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    $env:PYTHONPATH = "$RepoRoot;$OriginalPythonPath"
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONUTF8 = '1'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Push-Location $RepoRoot
    try {
        if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
            throw 'python is required'
        }
        if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
            throw 'git is required'
        }
        $PythonArgs = @('-B', '.\phase170_r3_r11r1_committed_audit_head\closeout.py', '--root', $RepoRoot)
        if ($DryRun) { $PythonArgs += '--dry-run' }
        if ($AuditReport -ne '') { $PythonArgs += @('--audit-report', $AuditReport) }
        & python @PythonArgs
        $ExitCode = $LASTEXITCODE
        & git status -sb
        if ($ExitCode -ne 0) {
            throw "Phase 170 active suite closeout did not pass: exit $ExitCode"
        }
        Write-Output 'PHASE170_R3R11=PASS'
    }
    finally {
        Pop-Location
    }
}
finally {
    $env:PYTHONPATH = $OriginalPythonPath
    $env:PYTHONIOENCODING = $OriginalPythonEncoding
    $env:PYTHONUTF8 = $OriginalUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OriginalNoBytecode
}
```


## `tests/test_contract.py`

```python
"""Focused contract tests for the Phase 170 end-of-phase active-suite closeout."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from phase170_r3_r11r1_committed_audit_head import closeout


def sample_worker(k: int) -> dict:
    return {
        "k": k, "n": 2, "group_dimension": k + 2,
        "toda52_applicable": True, "target_typed": True,
        "source_precedes": True, "search_status": "complete",
        "search_complete": True, "open_goals": 0, "proven_steps": 4,
        "result": "COMPLETE_AND_WEB_VERIFIED",
        "audit_result": "COMPLETE_AND_WEB_VERIFIED",
        "web_key": "generic-complete-proof", "web_partial": False,
        "web_steps": 4, "web_lines": 4, "web_error": None,
    }


def sample_pre() -> dict:
    return {"branch": "develop", "head": closeout.EXPECTED_HEAD,
            "audited_head": closeout.AUDITED_HEAD,
            "worker_sha256": "reviewed-worker-hash"}


def sample_report() -> dict:
    return {
        "phase": "170 R3-R10", "mode": "AUDIT_ONLY_FRESH_33",
        "dry_run": False, "result": "DOMAIN_ALL_VERIFIED",
        "tracked_unchanged": True, "domain": list(range(1, 34)),
        "domain_checked": 33, "domain_complete": 33,
        "domain_gaps": 0,
        "preflight": {"branch": "develop", "head": closeout.AUDITED_HEAD,
                      "tracked_changed_paths": [],
                      "worker_sha256": "reviewed-worker-hash"},
        "rows": [sample_worker(k) for k in range(1, 34)],
    }


def test_all_33_exact_rows_and_web_checks_are_accepted() -> None:
    closeout.validate_domain_report(sample_report(), sample_pre())


def test_rejects_dry_run_even_when_counts_are_33() -> None:
    report = sample_report()
    report["dry_run"] = True
    with pytest.raises(ValueError, match="provenance"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_stale_head() -> None:
    report = sample_report()
    report["preflight"]["head"] = "0" * 40
    with pytest.raises(ValueError, match="worker/HEAD"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_mismatched_worker_hash() -> None:
    report = sample_report()
    report["preflight"]["worker_sha256"] = "different"
    with pytest.raises(ValueError, match="worker/HEAD"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_gapped_or_duplicate_coordinate() -> None:
    report = sample_report()
    report["rows"][12]["k"] = 12
    with pytest.raises(ValueError, match="coordinates"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_missing_row() -> None:
    report = sample_report()
    report["rows"].pop()
    with pytest.raises(ValueError, match="surplus worker"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_false_complete_web_partial() -> None:
    report = sample_report()
    report["rows"][11]["web_partial"] = True
    with pytest.raises(ValueError, match="unverified"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_zero_proven_steps() -> None:
    report = sample_report()
    report["rows"][11]["proven_steps"] = 0
    with pytest.raises(ValueError, match="unverified"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_missing_web_lines() -> None:
    report = sample_report()
    report["rows"][11]["web_lines"] = 0
    with pytest.raises(ValueError, match="unverified"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_search_with_unresolved_goals() -> None:
    report = sample_report()
    report["rows"][11]["open_goals"] = 2
    with pytest.raises(ValueError, match="unverified"):
        closeout.validate_domain_report(report, sample_pre())


def test_rejects_fake_report_counts() -> None:
    report = sample_report()
    report["domain_gaps"] = 1
    with pytest.raises(ValueError, match="counts"):
        closeout.validate_domain_report(report, sample_pre())


def test_selects_only_the_verified_full_audit(tmp_path: Path) -> None:
    old = tmp_path / "phase170_r3_r10_n2_33_20261029_045006_272086"
    new = tmp_path / "phase170_r3_r10_n2_33_20261029_045030_272086"
    old.mkdir()
    new.mkdir()
    (old / "audit.json").write_text(json.dumps(sample_report()), encoding="utf-8")
    (new / "audit.json").write_text(json.dumps({"dry_run": True}), encoding="utf-8")
    chosen, report = closeout.find_verified_report(tmp_path, sample_pre(), None)
    assert chosen == old / "audit.json"
    assert report["domain_complete"] == 33


def test_explicit_invalid_audit_file_must_not_fall_back(tmp_path: Path) -> None:
    good = tmp_path / "phase170_r3_r10_n2_33_20261029_045006_272086"
    good.mkdir()
    (good / "audit.json").write_text(json.dumps(sample_report()), encoding="utf-8")
    bad = tmp_path / "bad.json"
    bad.write_text('{"result":"DOMAIN_ALL_VERIFIED"}', encoding="utf-8")
    with pytest.raises(RuntimeError, match="no valid"):
        closeout.find_verified_report(tmp_path, sample_pre(), bad)


def test_active_pytest_command_matches_prior_phase_closure() -> None:
    assert closeout.ACTIVE_TEST_ARGS == (
        "-B", "-m", "pytest", "-q", "--tb=short",
        "--disable-warnings", "-p", "no:cacheprovider", "tests",
    )


def test_preflight_accepts_only_clean_reviewed_commit(tmp_path: Path,
                                                       monkeypatch: pytest.MonkeyPatch) -> None:
    for path in closeout.EXPECTED_BLOBS:
        p = tmp_path / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"reviewed fixture")
    (tmp_path / "tests").mkdir()
    expected = {
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): closeout.EXPECTED_HEAD,
        ("diff", "--name-status", closeout.AUDITED_HEAD, "HEAD", "--"):
            "A\tphase170_r3_r10_n2_33_fresh_audit/audit.py\n"
            "A\tphase170_r3_r10r1_committed_head_audit/audit.py",
        ("diff", "--cached", "--name-only", "--"): "",
        ("diff", "--name-only", "HEAD", "--"): "",
    }
    for path, blob in closeout.EXPECTED_BLOBS.items():
        expected[("rev-parse", f"HEAD:{path}")] = blob
    monkeypatch.setattr(closeout, "git", lambda root, *args: expected[args])
    assert closeout.preflight(tmp_path, check_remote=False)["audited_head"] == closeout.AUDITED_HEAD
    expected[("diff", "--name-only", "HEAD", "--")] = "phase168_r2_toda52_transport.py"
    with pytest.raises(RuntimeError, match="tracked changes"):
        closeout.preflight(tmp_path, check_remote=False)


def test_preflight_rejects_wrong_blob(tmp_path: Path,
                                      monkeypatch: pytest.MonkeyPatch) -> None:
    for path in closeout.EXPECTED_BLOBS:
        p = tmp_path / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"fixture")
    (tmp_path / "tests").mkdir()

    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return closeout.EXPECTED_HEAD
        if args == ("diff", "--name-status", closeout.AUDITED_HEAD, "HEAD", "--"):
            return "A\tphase170_r3_r10_n2_33_fresh_audit/audit.py"
        if args[0] == "diff":
            return ""
        if args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return "wrong-blob"
        raise AssertionError(args)

    monkeypatch.setattr(closeout, "git", fake_git)
    with pytest.raises(RuntimeError, match="blob"):
        closeout.preflight(tmp_path, check_remote=False)


def test_full_pytest_streams_logs_without_running_early(tmp_path: Path,
                                                        monkeypatch: pytest.MonkeyPatch) -> None:
    captured = {}

    class FakeProcess:
        stdout = iter(["... [100%]\n", "3546 passed in 30.00s\n"])

        def wait(self) -> int:
            return 0

    def fake_popen(command, **kwargs):
        captured["command"] = command
        captured["env"] = kwargs["env"]
        return FakeProcess()

    monkeypatch.setattr(closeout.subprocess, "Popen", fake_popen)
    rc, summary = closeout.run_active_tests(tmp_path, tmp_path / "full_pytest.log")
    assert rc == 0 and "3546 passed" in summary
    assert captured["command"] == [closeout.sys.executable, *closeout.ACTIVE_TEST_ARGS]
    assert captured["env"]["PYTHONUTF8"] == "1"
    assert (tmp_path / "full_pytest.log").read_text(encoding="utf-8").endswith("3546 passed in 30.00s\n")


def test_worker_requires_real_web_proof_not_only_headline() -> None:
    row = deepcopy(sample_worker(12))
    assert closeout.valid_worker_row(row, 12)
    row["web_key"] = "partial-proof"
    assert not closeout.valid_worker_row(row, 12)


def test_historical_report_accepted_only_for_exact_reviewed_audit_head() -> None:
    pre = sample_pre()
    report = sample_report()
    assert report["preflight"]["head"] != pre["head"]
    closeout.validate_domain_report(report, pre)
    report["preflight"]["head"] = pre["head"]
    with pytest.raises(ValueError, match="worker/HEAD"):
        closeout.validate_domain_report(report, pre)


def test_preflight_rejects_non_audit_commit_change(tmp_path: Path,
                                                     monkeypatch: pytest.MonkeyPatch) -> None:
    for path in closeout.EXPECTED_BLOBS:
        f = tmp_path / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(b"reviewed")
    (tmp_path / "tests").mkdir()
    delta = "A\tphase168_r2_toda52_transport.py"

    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return closeout.EXPECTED_HEAD
        if args == ("diff", "--name-status", closeout.AUDITED_HEAD, "HEAD", "--"):
            return delta
        if args[0] == "diff":
            return ""
        if args[:2] == ("rev-parse", "HEAD:"):
            raise AssertionError("unexpected")
        if args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return closeout.EXPECTED_BLOBS[args[1][5:]]
        raise AssertionError(args)

    monkeypatch.setattr(closeout, "git", fake_git)
    with pytest.raises(RuntimeError, match="non-audit change"):
        closeout.preflight(tmp_path, check_remote=False)


def test_preflight_rejects_rewrite_inside_audit_package(tmp_path: Path,
                                                          monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return closeout.EXPECTED_HEAD
        if args == ("diff", "--name-status", closeout.AUDITED_HEAD, "HEAD", "--"):
            return "M\tphase170_r3_r10_n2_33_fresh_audit/audit.py"
        raise AssertionError(args)

    monkeypatch.setattr(closeout, "git", fake_git)
    with pytest.raises(RuntimeError, match="non-audit change"):
        closeout.preflight(tmp_path, check_remote=False)


def test_preflight_rejects_missing_audit_only_delta(tmp_path: Path,
                                                       monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return closeout.EXPECTED_HEAD
        if args == ("diff", "--name-status", closeout.AUDITED_HEAD, "HEAD", "--"):
            return ""
        raise AssertionError(args)

    monkeypatch.setattr(closeout, "git", fake_git)
    with pytest.raises(RuntimeError, match="additions are missing"):
        closeout.preflight(tmp_path, check_remote=False)
```


## `__init__.py`

```python
"""Phase 170 end-of-phase active-suite audit tools (no production changes)."""
```
