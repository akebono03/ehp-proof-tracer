# Phase 171 R1 — 追加コード全文

既存の本体コード、テスト、正式5文書は一切変更しない。追加位置：リポジトリ直下の `phase171_r1_n3_registered_audit/`。

新規 Python ファイルの import、関数、クラス、テスト関数は以下に省略なく収録する。

## `audit.py`

```python
"""Read-only n=3 registered group audit for Phase 171 R1.

Run the existing typed backward search and trusted public Web path without
modifying any proof rules, literature assertions, or registered goals.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

BRANCH = "develop"
HEAD = "715b00d67d4b3ff4b34bf87229842d14960ea6bb"
REVIEWED_BLOBS = {
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "phase170_r3_r8_n2_exhaustive_audit/audit.py": "6d95546bf165f11029a7d56d18c03013b3ecafed",
    "phase170_r3_r9_toda712_cited_rewrite/source712.py": "895c7b731a01b2497c053b9c8707ced9fa4a860f",
    "phase168_r2_toda52_transport.py": "f417cf7b828c898f7e957defd3b47056016cb585",
}
N = 3
REGISTERED_K = tuple(range(34))
SENTINEL = "__PHASE171_R1_WORKER__="


def git(root: Path, *arguments: str) -> str:
    process = subprocess.run(
        ["git", *arguments], cwd=root, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if process.returncode:
        raise RuntimeError(
            f"git {' '.join(arguments)} failed ({process.returncode}): "
            + process.stderr.decode("utf-8", errors="replace").strip()
        )
    return process.stdout.decode("utf-8", errors="replace").strip()


def tracked_state_digest(root: Path) -> str:
    command = ["git", "diff", "--binary", "HEAD", "--"]
    result = subprocess.run(command, cwd=root, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError("cannot inspect tracked diff")
    return sha256(result.stdout).hexdigest()


def explicit_registered_stems(csv_path: Path) -> tuple[int, ...]:
    """Deduplicate by (n,k); never use the count of CSV generator/id rows."""
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not {"n", "k", "id"}.issubset(reader.fieldnames):
            raise ValueError("sphere.csv requires n, k and id headers")
        stems: set[int] = set()
        for row in reader:
            if (row.get("n") or "").strip() != str(N):
                continue
            value = (row.get("k") or "").strip()
            if not value or not value.isdecimal():
                raise ValueError("invalid registered n=3 k: " + repr(value))
            stems.add(int(value))
    got = tuple(sorted(stems))
    if got != REGISTERED_K:
        missing = sorted(set(REGISTERED_K) - set(got))
        unexpected = sorted(set(got) - set(REGISTERED_K))
        raise RuntimeError(f"unreviewed n=3 DB scope: missing={missing}, unexpected={unexpected}")
    return got


def preflight(root: Path, *, remote: bool) -> dict:
    """Require reviewed, clean committed code. Untracked audit files are allowed."""
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if (branch, head) != (BRANCH, HEAD):
        raise RuntimeError(f"unreviewed branch or HEAD: {branch} {head}")
    if remote:
        found = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        if not found or found.split()[0] != HEAD:
            raise RuntimeError("origin/develop does not match reviewed HEAD")
    staged = git(root, "diff", "--cached", "--name-only", "--")
    unstaged = git(root, "diff", "--name-only", "HEAD", "--")
    if staged or unstaged:
        raise RuntimeError("tracked or staged changes present: " + repr((staged, unstaged)))
    for name, expected in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + name) != expected:
            raise RuntimeError("unreviewed tracked blob: " + name)
        if not (root / name).is_file():
            raise RuntimeError("reviewed file missing from checkout: " + name)
    stems = explicit_registered_stems(root / "data/sphere.csv")
    return {
        "branch": branch, "head": head, "registered_n": N,
        "registered_k": list(stems), "tracked_sha256": tracked_state_digest(root),
        "reviewed_blobs": dict(REVIEWED_BLOBS),
    }


def safe_description(value: object, limit: int = 1000) -> str:
    try:
        return str(value)[:limit]
    except Exception as exc:
        return f"<unprintable {type(value).__name__}: {type(exc).__name__}>"


def classify_observation(row: dict) -> str:
    """Only the existing search plus Web gate can establish a completed result."""
    if row.get("exception"):
        return "WORKER_EXCEPTION"
    if row.get("db_goal_typed") is not True:
        return "DB_GOAL_UNTYPED_OR_MISSING"
    if row.get("search_status") != "complete":
        return "PROOF_UNFINISHED"
    if (row.get("search_complete") is not True
            or row.get("root_matches_db_goal") is not True
            or type(row.get("open_goals")) is not int or row["open_goals"] != 0
            or type(row.get("proven_steps")) is not int or row["proven_steps"] <= 0):
        return "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"
    if (row.get("web_key") != "generic-complete-proof"
            or row.get("web_partial") is not False
            or type(row.get("web_steps")) is not int or row["web_steps"] <= 0
            or type(row.get("web_lines")) is not int or row["web_lines"] <= 0
            or row.get("web_error") is not None):
        return "WEB_NOT_VERIFIED"
    return "COMPLETE_AND_WEB_VERIFIED"


def worker(k: int) -> int:
    """Isolate normal proof search and standard Web rendering for one (3,k)."""
    row: dict = {"n": N, "k": k, "group_dimension": N + k}
    try:
        from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
        from phase165_r52_partial_proof import ProofSearchStatus
        from phase165_r55_nk_only_goal import search_group_from_registered_goal
        from web_group_proof import build_standard_web_group_proof_view

        db_target = exact_prior_database_result(N, k)
        row["db_goal_typed"] = db_target is not None
        row["db_goal_type"] = type(db_target).__name__ if db_target is not None else None
        row["db_goal_display"] = safe_description(db_target, 650) if db_target is not None else None
        result = search_group_from_registered_goal(n=N, k=k)
        row["search_status"] = getattr(result.status, "value", str(result.status))
        row["proven_steps"] = len(result.proven_steps)
        row["open_goals"] = len(result.open_goals)
        row["open_goal_text"] = [safe_description(goal) for goal in result.open_goals[:8]]
        row["diagnostics"] = [safe_description(item, 900) for item in result.diagnostics[:8]]
        row["root_matches_db_goal"] = bool(db_target is not None and result.conclusion == db_target)
        row["search_complete"] = bool(
            result.status is ProofSearchStatus.COMPLETE
            and not result.open_goals and result.proven_steps
        )
        row["givens"] = []
        row["inference_count"] = 0
        for step in result.proven_steps:
            if getattr(getattr(step, "rule", None), "name", None) == "GIVEN":
                rule = getattr(step, "inference_rule", None)
                literature = getattr(rule, "literature_reference", None)
                row["givens"].append({
                    "locator": getattr(literature, "locator", None),
                    "label": getattr(literature, "label", None),
                })
            elif getattr(getattr(step, "rule", None), "name", None) == "INFERENCE":
                row["inference_count"] += 1
        row.update(web_key=None, web_partial=None, web_steps=0, web_lines=0, web_error=None)
        try:
            view = build_standard_web_group_proof_view(
                n=N, k=k, max_depth=2, mode="narrative", citation_source="model",
            )
            row["web_key"] = view.key
            row["web_partial"] = view.partial_result
            row["web_steps"] = len(view.steps)
            row["web_lines"] = len(view.rendered_lines)
        except Exception as exc:
            row["web_error"] = f"{type(exc).__name__}: {exc}"[:1600]
    except Exception as exc:
        row["exception"] = f"{type(exc).__name__}: {exc}"[:1600]
        row["traceback"] = traceback.format_exc()[-2800:]
    row["audit_result"] = classify_observation(row)
    print(SENTINEL + json.dumps(row, ensure_ascii=False, sort_keys=True), flush=True)
    return 0


def parse_worker_output(stdout: str, returncode: int, k: int) -> dict:
    markers = [line[len(SENTINEL):] for line in stdout.splitlines()
               if line.startswith(SENTINEL)]
    if returncode != 0 or len(markers) != 1:
        return {"n": N, "k": k, "audit_result": "WORKER_FAILED",
                "returncode": returncode, "marker_count": len(markers),
                "diagnostics": [stdout[-1500:]]}
    try:
        row = json.loads(markers[0])
    except json.JSONDecodeError as exc:
        return {"n": N, "k": k, "audit_result": "INVALID_WORKER_JSON",
                "diagnostics": [safe_description(exc)]}
    if not isinstance(row, dict) or row.get("n") != N or row.get("k") != k:
        return {"n": N, "k": k, "audit_result": "WRONG_WORKER_GOAL"}
    return {**row, "audit_result": classify_observation(row)}


def launch_worker(root: Path, script: Path, k: int, timeout_seconds: int, output: Path) -> dict:
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        child = subprocess.run(
            [sys.executable, "-B", str(script), "--worker", "--k", str(k)],
            cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", check=False,
            timeout=timeout_seconds,
        )
        (output / f"k_{k:03d}.log").write_text(child.stdout, encoding="utf-8")
        return parse_worker_output(child.stdout, child.returncode, k)
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or b""
        content = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
        (output / f"k_{k:03d}.log").write_text(content, encoding="utf-8")
        return {"n": N, "k": k, "audit_result": "TIMEOUT", "timeout_seconds": timeout_seconds}


def summarize(rows: list[dict]) -> dict:
    if len({(r.get("n"), r.get("k")) for r in rows}) != len(rows):
        raise ValueError("duplicate (n,k) in audit rows")
    breakdown: dict[str, int] = {}
    for row in rows:
        key = str(row.get("audit_result", "MISSING_RESULT"))
        breakdown[key] = breakdown.get(key, 0) + 1
    complete = breakdown.get("COMPLETE_AND_WEB_VERIFIED", 0)
    worker_failures = sum(breakdown.get(name, 0) for name in (
        "WORKER_FAILED", "INVALID_WORKER_JSON", "WRONG_WORKER_GOAL", "TIMEOUT", "WORKER_EXCEPTION",
    ))
    return {"checked": len(rows), "complete": complete, "gaps": len(rows) - complete,
            "worker_failures": worker_failures, "breakdown": breakdown}


def write_json(path: Path, report: dict) -> None:
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temp, path)


def write_markdown(path: Path, report: dict) -> None:
    totals = report.get("summary") or {}
    lines = ["# Phase 171 R1 — n=3 登録済み群の監査", "",
             "本監査は証明を作らない。既存の Proof Search と標準 Web 経路の結果を観測する。", "",
             f"- 対象：{totals.get('checked', 0)} 群",
             f"- 完成・Web 検証済み：{totals.get('complete', 0)} 群",
             f"- 未完成・未検証：{totals.get('gaps', 0)} 群",
             f"- Worker の失敗：{totals.get('worker_failures', 0)} 件", "",
             "| k | 群 | DB Goal | 検索状態 | 未解決 | ProofStep | Web | 監査結果 |",
             "|---:|---|---|---|---:|---:|---|---|"]
    for row in report.get("rows", []):
        k = row["k"]
        lines.append(
            f"| {k} | $\\pi_{{{k + N}}}^{{3}}$ | {row.get('db_goal_type', '?')} | "
            f"{row.get('search_status', '?')} | {row.get('open_goals', '?')} | "
            f"{row.get('proven_steps', '?')} | {row.get('web_key', '?')} | "
            f"{row['audit_result']} |"
        )
    lines += ["", "詳細は audit.json と k_XXX.log を参照。", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def run(root: Path, *, dry_run: bool, timeout_seconds: int, check_remote: bool = True) -> int:
    recovery = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    output = recovery / ("phase171_r1_n3_audit_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    print("PHASE171_R1_MODE=AUDIT_ONLY", flush=True)
    print(f"PHASE171_R1_OUTPUT={output}", flush=True)
    report: dict = {"phase": "171 R1", "mode": "AUDIT_ONLY", "n": N,
                    "dry_run": dry_run, "full_pytest": False,
                    "production_modified": False, "rows": []}
    before = None
    code = 2
    try:
        before = preflight(root, remote=check_remote)
        report["preflight"] = before
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
            code = 0
            print("PHASE171_R1_DRY_RUN=PASS", flush=True)
        else:
            script = Path(__file__).resolve()
            for k in REGISTERED_K:
                row = launch_worker(root, script, k, timeout_seconds, output)
                report["rows"].append(row)
                report["summary"] = summarize(report["rows"])
                write_json(output / "audit.json", report)
                print(f"PHASE171_R1_k={k} RESULT={row['audit_result']}", flush=True)
            summary = summarize(report["rows"])
            report["summary"] = summary
            if summary["checked"] != len(REGISTERED_K):
                raise RuntimeError("incomplete audit coverage")
            report["result"] = (
                "AUDIT_COMPLETE_WITH_WORKER_FAILURES" if summary["worker_failures"]
                else "AUDIT_COMPLETE_ALL_VERIFIED" if not summary["gaps"]
                else "AUDIT_COMPLETE_WITH_GAPS"
            )
            write_markdown(output / "audit.md", report)
            print(f"PHASE171_R1_DOMAIN_CHECKED={summary['checked']}", flush=True)
            print(f"PHASE171_R1_DOMAIN_COMPLETE={summary['complete']}", flush=True)
            print(f"PHASE171_R1_DOMAIN_GAPS={summary['gaps']}", flush=True)
            print(f"PHASE171_R1_WORKER_FAILURES={summary['worker_failures']}", flush=True)
            # A completed observational audit can have unresolved mathematical goals.
            code = 2 if summary["worker_failures"] else 0
    except Exception as exc:
        report["result"] = "REFUSED_OR_ERROR"
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["traceback"] = traceback.format_exc()[-3000:]
        print(f"PHASE171_R1_REFUSED={report['error']}", flush=True)
    finally:
        if before is not None:
            try:
                after = preflight(root, remote=False)
                report["tracked_unchanged"] = before == after
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = f"{type(exc).__name__}: {exc}"
            if report["tracked_unchanged"] is False:
                report["result"] = "TRACKED_STATE_CHANGED"
                code = 2
        else:
            report["tracked_unchanged"] = None
        write_json(output / "audit.json", report)
        print(f"PHASE171_R1_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print(f"PHASE171_R1_REPORT={output / 'audit.json'}", flush=True)
        print(f"PHASE171_R1_RESULT={report['result']}", flush=True)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--k", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=240)
    args = parser.parse_args()
    if args.worker:
        if args.k not in REGISTERED_K:
            parser.error("worker requires a registered k in 0..33")
        return worker(args.k)
    if args.root is None:
        parser.error("--root is required")
    if args.timeout_seconds < 1:
        parser.error("--timeout-seconds must be positive")
    return run(args.root.resolve(), dry_run=args.dry_run,
               timeout_seconds=args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 240
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OriginalPythonPath = $env:PYTHONPATH
$OriginalEncoding = $env:PYTHONIOENCODING
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
            throw 'Python is required'
        }
        if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
            throw 'Git is required'
        }
        & python -B -m pytest -q -p no:cacheprovider `
            '.\phase171_r1_n3_registered_audit\tests\test_contract.py'
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 171 R1 focused pytest failed: $LASTEXITCODE"
        }
        Write-Output 'PHASE171_R1_FOCUSED_PYTEST=PASS'
        if ($DryRun) {
            & python -B '.\phase171_r1_n3_registered_audit\audit.py' `
                --root $RepoRoot --dry-run --timeout-seconds $TimeoutSeconds
        }
        else {
            & python -B '.\phase171_r1_n3_registered_audit\audit.py' `
                --root $RepoRoot --timeout-seconds $TimeoutSeconds
        }
        $AuditExit = $LASTEXITCODE
        & git status -sb
        if ($AuditExit -ne 0) {
            throw "Phase 171 R1 audit refused or worker failed: $AuditExit"
        }
        Write-Output 'PHASE171_R1=PASS'
    }
    finally {
        Pop-Location
    }
}
finally {
    $env:PYTHONPATH = $OriginalPythonPath
    $env:PYTHONIOENCODING = $OriginalEncoding
    $env:PYTHONUTF8 = $OriginalUtf8
    $env:PYTHONDONTWRITEBYTECODE = $OriginalNoBytecode
}
```

## `tests/test_contract.py`

```python
"""Focused audit-only contracts. No imported production application modules."""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase171_r1_n3_registered_audit import audit


def complete_row(k: int) -> dict:
    return {
        "n": 3, "k": k, "group_dimension": 3 + k,
        "db_goal_typed": True, "search_status": "complete",
        "root_matches_db_goal": True, "search_complete": True,
        "open_goals": 0, "proven_steps": 3,
        "web_key": "generic-complete-proof", "web_partial": False,
        "web_steps": 2, "web_lines": 3, "web_error": None,
    }


def test_registered_scope_includes_diagonal_and_all_stems() -> None:
    assert audit.N == 3
    assert audit.REGISTERED_K == tuple(range(34))
    assert audit.REGISTERED_K[0] == 0


def test_csv_deduplicates_generators_by_group_coordinates(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    body = "k,n,id,orders\n" + "".join(
        f"{k},3,0,2\n{k},3,1,2\n" for k in audit.REGISTERED_K
    )
    path.write_text(body + "33,2,0,2\n", encoding="utf-8-sig")
    assert audit.explicit_registered_stems(path) == audit.REGISTERED_K


def test_csv_missing_registered_group_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text("k,n,id\n" + "".join(f"{k},3,0\n" for k in range(33)), encoding="utf-8")
    with pytest.raises(RuntimeError, match="missing=\\[33\\]"):
        audit.explicit_registered_stems(path)


def test_csv_extra_registered_group_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text("k,n,id\n" + "".join(f"{k},3,0\n" for k in range(35)), encoding="utf-8")
    with pytest.raises(RuntimeError, match="unexpected=\\[34\\]"):
        audit.explicit_registered_stems(path)


def test_csv_rejects_malformed_k(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text("k,n,id\nbad,3,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid registered"):
        audit.explicit_registered_stems(path)


@pytest.mark.parametrize("field,value,expected", [
    ("db_goal_typed", False, "DB_GOAL_UNTYPED_OR_MISSING"),
    ("search_status", "search_failed", "PROOF_UNFINISHED"),
    ("open_goals", 1, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("proven_steps", 0, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("root_matches_db_goal", False, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("search_complete", False, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("web_key", "generic-partial-proof", "WEB_NOT_VERIFIED"),
    ("web_partial", True, "WEB_NOT_VERIFIED"),
    ("web_steps", 0, "WEB_NOT_VERIFIED"),
    ("web_lines", 0, "WEB_NOT_VERIFIED"),
    ("web_error", "UnverifiedProofTree", "WEB_NOT_VERIFIED"),
])
def test_classification_checks_search_and_web(field: str, value: object, expected: str) -> None:
    row = complete_row(12)
    row[field] = value
    assert audit.classify_observation(row) == expected


def test_worker_exception_never_claims_completion() -> None:
    row = {**complete_row(11), "exception": "ValueError: invalid source"}
    assert audit.classify_observation(row) == "WORKER_EXCEPTION"


def test_complete_row_has_verified_status() -> None:
    assert audit.classify_observation(complete_row(12)) == "COMPLETE_AND_WEB_VERIFIED"


def test_parse_worker_output_valid_utf8_and_untrusted_classification() -> None:
    row = {**complete_row(12), "audit_result": "FAKED", "diagnostics": ["η₂"]}
    raw = audit.SENTINEL + json.dumps(row, ensure_ascii=False)
    result = audit.parse_worker_output(raw, 0, 12)
    assert result["audit_result"] == "COMPLETE_AND_WEB_VERIFIED"
    assert result["diagnostics"] == ["η₂"]
    row["search_status"] = "search_failed"
    result = audit.parse_worker_output(audit.SENTINEL + json.dumps(row), 0, 12)
    assert result["audit_result"] == "PROOF_UNFINISHED"


def test_parse_worker_output_rejects_failure_double_and_wrong_target() -> None:
    raw = audit.SENTINEL + json.dumps(complete_row(5))
    assert audit.parse_worker_output(raw, 1, 5)["audit_result"] == "WORKER_FAILED"
    assert audit.parse_worker_output(raw + "\n" + raw, 0, 5)["audit_result"] == "WORKER_FAILED"
    assert audit.parse_worker_output(raw, 0, 6)["audit_result"] == "WRONG_WORKER_GOAL"
    assert audit.parse_worker_output(audit.SENTINEL + "not json", 0, 5)["audit_result"] == "INVALID_WORKER_JSON"


def test_observational_gaps_not_counted_as_completed() -> None:
    rows = [dict(n=3, k=k, audit_result="COMPLETE_AND_WEB_VERIFIED") for k in range(34)]
    assert audit.summarize(rows)["complete"] == 34
    rows[12]["audit_result"] = "PROOF_UNFINISHED"
    summary = audit.summarize(rows)
    assert summary["checked"] == 34 and summary["complete"] == 33
    assert summary["gaps"] == 1 and summary["worker_failures"] == 0
    rows[1]["audit_result"] = "WORKER_EXCEPTION"
    assert audit.summarize(rows)["worker_failures"] == 1
    with pytest.raises(ValueError, match="duplicate"):
        audit.summarize(rows + [rows[0]])


def test_runner_forces_utf8_and_records_logs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    captured = {}
    def fake_run(cmd, **kw):
        captured["cmd"] = cmd
        captured["env"] = kw["env"]
        captured["timeout"] = kw["timeout"]
        return SimpleNamespace(returncode=0, stdout=audit.SENTINEL + json.dumps(
            {**complete_row(6), "note": "η₂"}, ensure_ascii=False) + "\n")
    monkeypatch.setattr(audit.subprocess, "run", fake_run)
    r = audit.launch_worker(tmp_path, tmp_path / "audit.py", 6, 120, tmp_path)
    assert r["audit_result"] == "COMPLETE_AND_WEB_VERIFIED"
    assert captured["env"]["PYTHONIOENCODING"] == "utf-8"
    assert captured["env"]["PYTHONUTF8"] == "1"
    assert captured["env"]["PYTHONDONTWRITEBYTECODE"] == "1"
    assert captured["cmd"][-2:] == ["--k", "6"]
    assert captured["timeout"] == 120
    assert (tmp_path / "k_006.log").read_text(encoding="utf-8").find("η₂") >= 0


def test_preflight_validates_commit_and_blobs_without_mutation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    answers = {
        ("branch", "--show-current"): audit.BRANCH,
        ("rev-parse", "HEAD"): audit.HEAD,
        ("diff", "--cached", "--name-only", "--"): "",
        ("diff", "--name-only", "HEAD", "--"): "",
    }
    for name, blob in audit.REVIEWED_BLOBS.items():
        file = tmp_path / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("fixture", encoding="utf-8")
        answers[("rev-parse", "HEAD:" + name)] = blob
    monkeypatch.setattr(audit, "git", lambda _root, *args: answers[args])
    monkeypatch.setattr(audit, "tracked_state_digest", lambda _root: "sha-test")
    monkeypatch.setattr(audit, "explicit_registered_stems", lambda _path: audit.REGISTERED_K)
    before = audit.preflight(tmp_path, remote=False)
    assert before["registered_k"] == list(audit.REGISTERED_K)
    assert before["tracked_sha256"] == "sha-test"
    answers[("diff", "--name-only", "HEAD", "--")] = "web_group_proof.py"
    with pytest.raises(RuntimeError, match="tracked or staged"):
        audit.preflight(tmp_path, remote=False)


def test_preflight_rejects_commit_and_unreviewed_blob(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    answers = {
        ("branch", "--show-current"): "develop",
        ("rev-parse", "HEAD"): "obsolete",
        ("diff", "--cached", "--name-only", "--"): "",
        ("diff", "--name-only", "HEAD", "--"): "",
    }
    monkeypatch.setattr(audit, "git", lambda _root, *args: answers[args])
    with pytest.raises(RuntimeError, match="unreviewed branch or HEAD"):
        audit.preflight(tmp_path, remote=False)
    answers[("rev-parse", "HEAD")] = audit.HEAD
    for name, blob in audit.REVIEWED_BLOBS.items():
        file = tmp_path / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("fixture", encoding="utf-8")
        answers[("rev-parse", "HEAD:" + name)] = blob
    answers[("rev-parse", "HEAD:data/sphere.csv")] = "not-verified"
    with pytest.raises(RuntimeError, match="unreviewed tracked blob"):
        audit.preflight(tmp_path, remote=False)


def test_dry_run_validates_scope_without_running_workers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(audit, "preflight", lambda _root, remote: {"head": audit.HEAD})
    monkeypatch.setattr(audit, "launch_worker", lambda *args: pytest.fail("worker called in dry-run"))
    assert audit.run(tmp_path, dry_run=True, timeout_seconds=60, check_remote=False) == 0
    records = list((tmp_path / "EHPProofTracerRecovery").glob("phase171_r1_n3_audit_*/audit.json"))
    assert len(records) == 1
    report = json.loads(records[0].read_text(encoding="utf-8"))
    assert report["result"] == "DRY_RUN_PASS"
    assert report["tracked_unchanged"] is True


def test_full_audit_preserves_incomplete_observations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(audit, "preflight", lambda _root, remote: {"head": audit.HEAD})
    def fake_worker(root, script, k, timeout_seconds, output):
        return {"n": 3, "k": k, "search_status": "search_failed" if k == 12 else "complete",
                "audit_result": "PROOF_UNFINISHED" if k == 12 else "COMPLETE_AND_WEB_VERIFIED"}
    monkeypatch.setattr(audit, "launch_worker", fake_worker)
    assert audit.run(tmp_path, dry_run=False, timeout_seconds=60, check_remote=False) == 0
    files = list((tmp_path / "EHPProofTracerRecovery").glob("phase171_r1_n3_audit_*/audit.json"))
    assert len(files) == 1
    report = json.loads(files[0].read_text(encoding="utf-8"))
    assert report["summary"]["checked"] == 34
    assert report["summary"]["gaps"] == 1
    assert report["result"] == "AUDIT_COMPLETE_WITH_GAPS"
    assert (files[0].parent / "audit.md").is_file()


def test_worker_crash_requires_investigation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(audit, "preflight", lambda _root, remote: {"head": audit.HEAD})
    monkeypatch.setattr(audit, "launch_worker", lambda root, script, k, timeout_seconds, output: {
        "n": 3, "k": k,
        "audit_result": "WORKER_FAILED" if k == 1 else "COMPLETE_AND_WEB_VERIFIED",
    })
    assert audit.run(tmp_path, dry_run=False, timeout_seconds=60, check_remote=False) == 2
    files = list((tmp_path / "EHPProofTracerRecovery").glob("phase171_r1_n3_audit_*/audit.json"))
    assert len(files) == 1
    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data["result"] == "AUDIT_COMPLETE_WITH_WORKER_FAILURES"


def test_worker_uses_real_api_shapes_and_collects_citations(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    import sys
    from enum import Enum
    from types import ModuleType

    class ProofSearchStatus(Enum):
        COMPLETE = "complete"

    def fake_module(path: str, **members: object) -> None:
        module = ModuleType(path)
        for key, value in members.items():
            setattr(module, key, value)
        monkeypatch.setitem(sys.modules, path, module)

    fixed_target = object()
    given = SimpleNamespace(rule=SimpleNamespace(name="GIVEN"),
        inference_rule=SimpleNamespace(literature_reference=SimpleNamespace(
            locator="Proposition 5.8", label="Toda Proposition 5.8")))
    inference = SimpleNamespace(rule=SimpleNamespace(name="INFERENCE"), inference_rule=None)
    proof_result = SimpleNamespace(
        status=ProofSearchStatus.COMPLETE, conclusion=fixed_target,
        proven_steps=[given, inference], open_goals=[], diagnostics=[],
    )
    calls = []

    def fake_search(*, n: int, k: int):
        calls.append(("search", n, k))
        return proof_result

    def fake_view(*, n: int, k: int, max_depth: int, mode: str, citation_source: str):
        calls.append(("web", n, k, max_depth, mode, citation_source))
        return SimpleNamespace(key="generic-complete-proof", partial_result=False,
                               steps=[object()], rendered_lines=[object()])

    fake_module("phase169_r10e4_ordered_db_prior.db_prior",
                exact_prior_database_result=lambda n, k: fixed_target)
    fake_module("phase165_r52_partial_proof", ProofSearchStatus=ProofSearchStatus)
    fake_module("phase165_r55_nk_only_goal", search_group_from_registered_goal=fake_search)
    fake_module("web_group_proof", build_standard_web_group_proof_view=fake_view)
    assert audit.worker(4) == 0
    text = capsys.readouterr().out.strip()
    assert text.startswith(audit.SENTINEL)
    row = json.loads(text[len(audit.SENTINEL):])
    assert row["audit_result"] == "COMPLETE_AND_WEB_VERIFIED"
    assert row["givens"] == [{"label": "Toda Proposition 5.8", "locator": "Proposition 5.8"}]
    assert row["inference_count"] == 1
    assert calls == [("search", 3, 4), ("web", 3, 4, 2, "narrative", "model")]


def test_worker_keeps_search_failures_observable(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    import sys
    from enum import Enum
    from types import ModuleType

    class ProofSearchStatus(Enum):
        SEARCH_FAILED = "search_failed"
        COMPLETE = "complete"

    def put(path: str, **members: object) -> None:
        item = ModuleType(path)
        for key, value in members.items():
            setattr(item, key, value)
        monkeypatch.setitem(sys.modules, path, item)

    target = object()
    put("phase169_r10e4_ordered_db_prior.db_prior",
        exact_prior_database_result=lambda n, k: target)
    put("phase165_r52_partial_proof", ProofSearchStatus=ProofSearchStatus)
    put("phase165_r55_nk_only_goal", search_group_from_registered_goal=lambda n, k: SimpleNamespace(
        status=ProofSearchStatus.SEARCH_FAILED, conclusion=None, proven_steps=[],
        open_goals=["typed missing claim"], diagnostics=["source not available"]
    ))
    put("web_group_proof", build_standard_web_group_proof_view=lambda **kwargs: SimpleNamespace(
        key="generic-partial-proof", partial_result=True, steps=[], rendered_lines=[]
    ))
    assert audit.worker(15) == 0
    text = capsys.readouterr().out.strip()
    row = json.loads(text[len(audit.SENTINEL):])
    assert row["audit_result"] == "PROOF_UNFINISHED"
    assert row["open_goals"] == 1
    assert row["open_goal_text"] == ["typed missing claim"]
    assert row["diagnostics"] == ["source not available"]
```

## `__init__.py`

```python
"""Phase 171 R1 read-only audit tooling."""
```
