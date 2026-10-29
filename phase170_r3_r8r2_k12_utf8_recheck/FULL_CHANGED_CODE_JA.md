# Phase 170 R3-R8R2 — 新規コード全文

既存ファイルは変更しない。以下に新規監査ファイルとテスト関数を全文掲載する。

## `runner.py`

```python
"""Audit-only UTF-8 retry for Phase 170 R3-R8 k=12 after commit 170-3-8.

Run the previously reviewed worker directly, without altering repository code.
Optionally combine its result with the validated R3-R8 full-domain audit.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

EXPECTED_BRANCH = "develop"
EXPECTED_HEAD = "114a67d708edba3d17da673a218034fcd804aa15"
EXPECTED_BLOBS = {
    "phase170_r3_r8_n2_exhaustive_audit/audit.py": "6d95546bf165f11029a7d56d18c03013b3ecafed",
    "phase168_r2_toda52_transport.py": "3bf9dfa2080e330e7030f0f0a7762f3fb1fa8fff",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
}
WORKER_RELATIVE = "phase170_r3_r8_n2_exhaustive_audit/audit.py"
SENTINEL = "__R3R8_RESULT__="
K = 12


def git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode:
        raise RuntimeError(
            f"git {' '.join(args)} exited {process.returncode}: {process.stderr.strip()}"
        )
    return process.stdout.strip()


def preflight(root: Path) -> dict:
    """Require the exact reviewed 170-3-8 commit with no tracked changes."""
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if branch != EXPECTED_BRANCH or head != EXPECTED_HEAD:
        raise RuntimeError(f"unreviewed branch or HEAD: {branch} {head}")
    if git(root, "diff", "--name-only"):
        raise RuntimeError("unstaged tracked changes are present")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("staged tracked changes are present")
    for path, expected_blob in EXPECTED_BLOBS.items():
        committed = git(root, "rev-parse", f"HEAD:{path}")
        if committed != expected_blob:
            raise RuntimeError(f"unreviewed committed file: {path}")
        if not (root / path).is_file():
            raise RuntimeError(f"required file is missing: {path}")
    return {"branch": branch, "head": head,
            "committed_verified_paths": list(EXPECTED_BLOBS)}


def eligible_prior_report(report: dict) -> bool:
    """Only join the exact verified 32/33 run with its sole k=12 crash."""
    rows = report.get("rows")
    if not isinstance(rows, list) or len(rows) != 34:
        return False
    if set(row.get("k") for row in rows if isinstance(row, dict)) != set(range(34)):
        return False
    if report.get("domain_checked") != 33 or report.get("domain_complete") != 32:
        return False
    if report.get("domain_gaps") != 1 or report.get("tracked_unchanged") is not True:
        return False
    pre = report.get("preflight") or {}
    if pre.get("branch") != "develop" or pre.get("head") != "f479e0aabdfeefa69ad986e20c0f69ce0efd7bbd":
        return False
    if rows[0].get("k") != 0 or rows[0].get("result") != "OUTSIDE_TODA_5_2_DOMAIN":
        return False
    problems = [row for row in rows if row.get("k", -1) >= 1
                and row.get("result") != "COMPLETE_AND_WEB_VERIFIED"]
    return len(problems) == 1 and problems[0].get("k") == K and problems[0].get("result") == "WORKER_FAILED"


def find_prior_report(recovery_dir: Path) -> tuple[Path, dict] | None:
    """Find the user's previous immutable observational report, not guessed data."""
    for path in sorted(recovery_dir.glob("phase170_r3_r8_n2_*/audit.json"), reverse=True):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        if isinstance(report, dict) and eligible_prior_report(report):
            return path, report
    return None


def parse_worker_output(output: str, exit_code: int) -> dict:
    """Parse one standalone worker result, including diagnostics on failure."""
    values = [line[len(SENTINEL):] for line in output.splitlines()
              if line.startswith(SENTINEL)]
    if exit_code != 0 or len(values) != 1:
        return {"k": K, "result": "WORKER_FAILED", "exit": exit_code,
                "diagnostics": [output[-1800:]]}
    try:
        row = json.loads(values[0])
    except json.JSONDecodeError as exc:
        return {"k": K, "result": "WORKER_FAILED", "exit": exit_code,
                "diagnostics": [f"invalid worker JSON: {exc}"]}
    if not isinstance(row, dict) or row.get("k") != K:
        return {"k": K, "result": "WORKER_FAILED", "exit": exit_code,
                "diagnostics": ["unexpected worker result or k"]}
    return row


def combine(previous: dict | None, new_row: dict) -> dict:
    """Preserve all prior observations and replace only the retried k=12 row."""
    if previous is None:
        return {"scope": "SINGLE_K", "rows": [new_row],
                "checked": 1,
                "complete": int(new_row.get("result") == "COMPLETE_AND_WEB_VERIFIED"),
                "gaps": int(new_row.get("result") != "COMPLETE_AND_WEB_VERIFIED")}
    if not eligible_prior_report(previous):
        raise ValueError("previous report is not the reviewed 32/33 audit")
    rows = [dict(new_row) if r["k"] == K else dict(r) for r in previous["rows"]]
    domain = [r for r in rows if r["k"] >= 1]
    complete = sum(r.get("result") == "COMPLETE_AND_WEB_VERIFIED" for r in domain)
    return {"scope": "COMBINED_33_K", "rows": rows,
            "checked": len(domain), "complete": complete, "gaps": len(domain) - complete}


def run(root: Path, *, dry_run: bool, timeout_seconds: int) -> int:
    home = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery"
    home.mkdir(parents=True, exist_ok=True)
    output = home / ("phase170_r3_r8r2_k12_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    print("PHASE170_R3R8R2_MODE=AUDIT_ONLY_UTF8_SINGLE_K", flush=True)
    print(f"PHASE170_R3R8R2_OUTPUT={output}", flush=True)
    report = {"phase": "170 R3-R8R2", "mode": "AUDIT_ONLY_UTF8_SINGLE_K",
              "dry_run": dry_run, "production_modified": False,
              "full_pytest": False, "k": K}
    exit_code = 2
    try:
        before = preflight(root)
        report["preflight"] = before
        prior = find_prior_report(home)
        report["previous_report"] = str(prior[0]) if prior is not None else None
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
            print("PHASE170_R3R8R2_DRY_RUN=PASS", flush=True)
            exit_code = 0
        else:
            worker_path = root / WORKER_RELATIVE
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
            try:
                worker = subprocess.run(
                    [sys.executable, "-B", str(worker_path), "--worker", "--k", str(K)],
                    cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8", errors="replace", check=False,
                    timeout=timeout_seconds,
                )
                (output / "k_012.log").write_text(worker.stdout, encoding="utf-8")
                row = parse_worker_output(worker.stdout, worker.returncode)
            except subprocess.TimeoutExpired as exc:
                raw = exc.stdout or b""
                if isinstance(raw, bytes):
                    raw = raw.decode("utf-8", errors="replace")
                (output / "k_012.log").write_text(raw, encoding="utf-8")
                row = {"k": K, "result": "TIMEOUT", "timeout_seconds": timeout_seconds}
            report["worker_row"] = row
            combined = combine(prior[1] if prior else None, row)
            report["combined"] = combined
            report["result"] = "AUDIT_VERIFIED" if combined["gaps"] == 0 else "AUDIT_WITH_GAPS"
            print(f"PHASE170_R3R8R2_k={K}_RESULT={row['result']}", flush=True)
            print(f"PHASE170_R3R8R2_SCOPE={combined['scope']}", flush=True)
            print(f"PHASE170_R3R8R2_DOMAIN_CHECKED={combined['checked']}", flush=True)
            print(f"PHASE170_R3R8R2_DOMAIN_COMPLETE={combined['complete']}", flush=True)
            print(f"PHASE170_R3R8R2_DOMAIN_GAPS={combined['gaps']}", flush=True)
            print(f"PHASE170_R3R8R2_RESULT={report['result']}", flush=True)
            exit_code = 0
    except Exception as exc:
        report["result"] = "REFUSED_OR_ERROR"
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["traceback"] = traceback.format_exc()[-2200:]
        print(f"PHASE170_R3R8R2_REFUSED={report['error']}", flush=True)
    finally:
        try:
            after = preflight(root)
            report["tracked_unchanged"] = after == report.get("preflight")
        except Exception as exc:
            report["tracked_unchanged"] = False
            report["postflight_error"] = f"{type(exc).__name__}: {exc}"
        (output / "audit.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"PHASE170_R3R8R2_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print(f"PHASE170_R3R8R2_REPORT={output / 'audit.json'}", flush=True)
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        parser.error("timeout must be positive")
    return run(args.root.resolve(), dry_run=args.dry_run, timeout_seconds=args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 180
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$Arguments = @('-B', (Join-Path $PSScriptRoot 'runner.py'), '--root', $Root, '--timeout-seconds', "$TimeoutSeconds")
if ($DryRun) { $Arguments += '--dry-run' }
& python @Arguments
exit $LASTEXITCODE
```

## `tests/test_contract.py`

```python
"""Isolated contract tests for R3-R8R2. No application imports required."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase170_r3_r8r2_k12_utf8_recheck import runner


def previous_report() -> dict:
    rows = [{"k": 0, "result": "OUTSIDE_TODA_5_2_DOMAIN"}]
    rows += [{"k": k, "result": "WORKER_FAILED" if k == 12 else "COMPLETE_AND_WEB_VERIFIED"}
             for k in range(1, 34)]
    return {"preflight": {"branch": "develop", "head": "f479e0aabdfeefa69ad986e20c0f69ce0efd7bbd"},
            "rows": rows, "domain_checked": 33, "domain_complete": 32, "domain_gaps": 1,
            "tracked_unchanged": True}


def test_reviewed_previous_report_is_eligible():
    assert runner.eligible_prior_report(previous_report())


def test_incomplete_previous_report_is_rejected():
    report = previous_report()
    report["domain_complete"] = 33
    assert not runner.eligible_prior_report(report)


def test_unrelated_failure_is_rejected():
    report = previous_report()
    report["rows"][13]["result"] = "WORKER_EXCEPTION"
    assert not runner.eligible_prior_report(report)


def test_worker_utf8_json_parses_subscripts():
    raw = runner.SENTINEL + json.dumps({"k": 12, "result": "COMPLETE_AND_WEB_VERIFIED", "note": "η₂"}, ensure_ascii=False)
    assert runner.parse_worker_output(raw, 0)["note"] == "η₂"


def test_worker_wrong_exit_is_not_complete():
    raw = runner.SENTINEL + json.dumps({"k": 12, "result": "COMPLETE_AND_WEB_VERIFIED"})
    assert runner.parse_worker_output(raw, 1)["result"] == "WORKER_FAILED"


def test_worker_multiple_sentinels_is_rejected():
    raw = runner.SENTINEL + '{"k": 12}\n' + runner.SENTINEL + '{"k": 12}'
    assert runner.parse_worker_output(raw, 0)["result"] == "WORKER_FAILED"


def test_combined_33_success_preserves_prior_results():
    report = previous_report()
    row = {"k": 12, "result": "COMPLETE_AND_WEB_VERIFIED", "proof_steps": 3}
    joined = runner.combine(report, row)
    assert joined["scope"] == "COMBINED_33_K"
    assert joined["checked"] == 33
    assert joined["complete"] == 33
    assert joined["gaps"] == 0
    assert joined["rows"][11] == report["rows"][11]
    assert joined["rows"][12]["proof_steps"] == 3


def test_combined_gap_remains_visible():
    joined = runner.combine(previous_report(), {"k": 12, "result": "PROOF_UNFINISHED"})
    assert joined["checked"] == 33 and joined["complete"] == 32 and joined["gaps"] == 1


def test_single_k_result_if_previous_audit_missing():
    result = runner.combine(None, {"k": 12, "result": "COMPLETE_AND_WEB_VERIFIED"})
    assert result["scope"] == "SINGLE_K" and result["checked"] == 1


def test_preflight_accepts_only_reviewed_clean_commit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    for f in runner.EXPECTED_BLOBS:
        p = tmp_path / f
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"fixture")
    answers = {
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): runner.EXPECTED_HEAD,
        ("diff", "--name-only"): "",
        ("diff", "--cached", "--name-only"): "",
    }
    for path, sha in runner.EXPECTED_BLOBS.items():
        answers[("rev-parse", f"HEAD:{path}")] = sha
    monkeypatch.setattr(runner, "git", lambda _root, *args: answers[args])
    result = runner.preflight(tmp_path)
    assert result["head"] == runner.EXPECTED_HEAD
    answers[("diff", "--name-only")] = "phase168_r2_toda52_transport.py"
    with pytest.raises(RuntimeError, match="unstaged tracked changes"):
        runner.preflight(tmp_path)


def test_prior_report_discovery(tmp_path: Path):
    folder = tmp_path / "phase170_r3_r8_n2_old"
    folder.mkdir()
    (folder / "audit.json").write_text(json.dumps(previous_report()), encoding="utf-8")
    result = runner.find_prior_report(tmp_path)
    assert result is not None and result[0] == folder / "audit.json"


def test_worker_subprocess_forces_utf8(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from types import SimpleNamespace

    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(runner, "preflight", lambda root: {"branch": "develop", "head": runner.EXPECTED_HEAD})
    monkeypatch.setattr(runner, "find_prior_report", lambda root: None)
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured["env"] = kwargs["env"]
        output = runner.SENTINEL + json.dumps(
            {"k": 12, "result": "COMPLETE_AND_WEB_VERIFIED", "note": "η₂"},
            ensure_ascii=False,
        ) + "\n"
        return SimpleNamespace(stdout=output, returncode=0)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    assert runner.run(tmp_path, dry_run=False, timeout_seconds=60) == 0
    assert captured["env"]["PYTHONIOENCODING"] == "utf-8"
    assert captured["env"]["PYTHONUTF8"] == "1"
    assert captured["command"][-2:] == ["--k", "12"]
    reports = list((tmp_path / "EHPProofTracerRecovery").glob("phase170_r3_r8r2_k12_*/audit.json"))
    assert len(reports) == 1
    result = json.loads(reports[0].read_text(encoding="utf-8"))
    assert result["worker_row"]["note"] == "η₂"
    assert result["tracked_unchanged"] is True
```

## `__init__.py`

```python
"""Read-only k=12 UTF-8 recheck tooling."""
```
