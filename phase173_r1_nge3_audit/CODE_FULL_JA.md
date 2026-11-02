# Phase 173 R1 — 新規コード・新規テスト全文

新規ファイルの追加位置はリポジトリ直下 `phase173_r1_nge3_audit/`。既存関数やクラスの置換はない。

全ファイルを省略なしで示す。

## `audit.py`

```python
"""Phase 173 R1: audit registered n>=3 proof searches without changing production code."""
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
REVIEWED_HEAD = "11ea331f322883e2f2cf34b9e865dea2134f5058"
REVIEWED_BLOBS = {
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r52_partial_proof.py": "669fb947f1f9b4670d10723f8a562e60c015b249",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase168_r3_4_link_bridge.py": "c3a6233a57c41e61e6649ee33c7a336d7aa1c664",
    "phase165_r52_r9_shared_math.py": "2718c55789af7f442ac2c086d016d3d6f7ca3133",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "phase171_r1_n3_registered_audit/audit.py": "aceddc0294099647d2487432c471ca2cd1219bc8",
}
PRIORITY_EXTRA = ((4, 3), (5, 3), (6, 3), (7, 3))
SENTINEL = "__PHASE173_R1_WORKER__="
EXECUTION_FAILURES = frozenset({
    "WORKER_EXCEPTION", "WORKER_FAILED", "TIMEOUT", "INVALID_WORKER_JSON",
    "WRONG_WORKER_GOAL",
})


def git(root: Path, *arguments: str) -> str:
    command = ["git", *arguments]
    result = subprocess.run(
        command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"git {' '.join(arguments)} failed ({result.returncode}): {result.stderr.strip()}"
        )
    return result.stdout.strip()


def registered_groups(path: Path) -> tuple[tuple[int, int], ...]:
    """Read explicit n>=3 CSV coordinates; never infer a missing group."""
    coordinates: set[tuple[int, int]] = set()
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or not {"n", "k", "id"}.issubset(reader.fieldnames):
            raise ValueError("sphere.csv requires n,k,id headers")
        for line, row in enumerate(reader, start=2):
            n_text = (row.get("n") or "").strip()
            k_text = (row.get("k") or "").strip()
            if not n_text:
                continue
            if not n_text.isdecimal():
                raise ValueError(f"malformed n at CSV row {line}: {n_text!r}")
            n = int(n_text)
            if n < 3:
                continue
            if not k_text.isdecimal():
                raise ValueError(f"malformed k at CSV row {line}: {k_text!r}")
            coordinates.add((n, int(k_text)))
    if not coordinates:
        raise ValueError("no explicit registered n>=3 groups")
    return tuple(sorted(coordinates))


def select_groups(
    all_groups: tuple[tuple[int, int], ...], scope: str,
) -> tuple[tuple[int, int], ...]:
    if scope == "all":
        return all_groups
    if scope != "priority":
        raise ValueError(f"unknown audit scope: {scope}")
    present = set(all_groups)
    n3 = {pair for pair in present if pair[0] == 3}
    if len(n3) != 34 or {k for _, k in n3} != set(range(34)):
        raise RuntimeError("n=3 registered scope differs from reviewed k=0..33")
    if not set(PRIORITY_EXTRA).issubset(present):
        raise RuntimeError("a required priority group is not registered")
    return tuple(sorted(n3 | set(PRIORITY_EXTRA)))


def preflight(root: Path, *, check_remote: bool) -> dict:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("audit directory is not the Git repository root")
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if branch != BRANCH or head != REVIEWED_HEAD:
        raise RuntimeError(
            f"unreviewed checkout: branch={branch} HEAD={head}; expected {BRANCH} {REVIEWED_HEAD}"
        )
    if check_remote:
        remote = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        if not remote or remote.split()[0] != REVIEWED_HEAD:
            raise RuntimeError("GitHub origin/develop differs from reviewed HEAD")
    status = git(root, "status", "--porcelain", "--untracked-files=no")
    if status:
        raise RuntimeError("tracked or staged local changes require review: " + status[:1000])
    for path, expected in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + path) != expected:
            raise RuntimeError("unreviewed source Git blob: " + path)
        if not (root / path).is_file():
            raise RuntimeError("source file missing: " + path)
    groups = registered_groups(root / "data/sphere.csv")
    if len(groups) != 797:
        raise RuntimeError(f"registered group count changed: {len(groups)} != 797")
    return {
        "branch": branch, "head": head, "tracked_status": status,
        "registered_count": len(groups),
        "registered_groups_sha256": sha256(repr(groups).encode("ascii")).hexdigest(),
        "reviewed_blobs": dict(REVIEWED_BLOBS),
    }


def safe_text(value: object, limit: int = 1200) -> str:
    try:
        return str(value)[:limit]
    except Exception as exc:
        return f"unprintable {type(value).__name__}: {type(exc).__name__}"


def classify_observation(row: dict) -> str:
    if row.get("exception"):
        return "WORKER_EXCEPTION"
    if row.get("db_goal_typed") is not True:
        return "DB_GOAL_UNTYPED_OR_MISSING"
    if row.get("search_status") != "complete":
        return "PROOF_UNFINISHED"
    if (row.get("search_complete") is not True
            or row.get("root_matches_db_goal") is not True
            or type(row.get("open_goals")) is not int or row["open_goals"] != 0
            or type(row.get("proven_steps")) is not int or row["proven_steps"] < 1):
        return "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"
    if row.get("citation_model_verified") is not True:
        return "CITATION_MODEL_NOT_VERIFIED"
    if (row.get("web_key") != "generic-complete-proof"
            or row.get("web_partial") is not False
            or type(row.get("web_steps")) is not int or row["web_steps"] < 1
            or type(row.get("web_lines")) is not int or row["web_lines"] < 1
            or row.get("web_error") is not None):
        return "WEB_NOT_VERIFIED"
    return "COMPLETE_AND_WEB_VERIFIED"


def worker(n: int, k: int) -> int:
    row: dict = {"n": n, "k": k, "group_dimension": n + k}
    try:
        from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
        from phase165_r52_partial_proof import ProofSearchStatus
        from phase165_r52_r9_shared_math import build_shared_typed_bridge
        from phase165_r55_nk_only_goal import search_group_from_registered_goal
        from web_group_proof import build_standard_web_group_proof_view

        target = exact_prior_database_result(n, k)
        row["db_goal_typed"] = target is not None
        row["db_goal_type"] = type(target).__name__ if target is not None else None
        row["db_goal_display"] = safe_text(target, 650) if target is not None else None
        bridge = build_shared_typed_bridge()
        contexts: list[object] = []
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=contexts.append,
        )
        row["search_status"] = getattr(result.status, "value", str(result.status))
        row["proven_steps"] = len(result.proven_steps)
        row["open_goals"] = len(result.open_goals)
        row["open_goal_text"] = [safe_text(goal) for goal in result.open_goals[:12]]
        row["diagnostics"] = [safe_text(item) for item in result.diagnostics[:12]]
        row["search_references"] = [safe_text(x) for x in result.references]
        row["root_matches_db_goal"] = bool(target is not None and result.conclusion == target)
        row["search_complete"] = bool(
            result.status is ProofSearchStatus.COMPLETE
            and not result.open_goals and result.proven_steps
        )
        row["inference_count"] = 0
        row["given_references"] = []
        for step in result.proven_steps:
            rule = getattr(getattr(step, "rule", None), "name", "")
            if rule == "INFERENCE":
                row["inference_count"] += 1
            elif rule == "GIVEN":
                literature = getattr(getattr(step, "inference_rule", None), "literature_reference", None)
                row["given_references"].append({
                    "label": getattr(literature, "label", None),
                    "locator": getattr(literature, "locator", None),
                })
        row["citation_model_verified"] = False
        row["citation_count"] = None
        row["citations"] = []
        row["citation_error"] = None
        if row["search_complete"] and contexts:
            try:
                from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
                model = build_linked_proof_narrative_model(result, contexts[-1])
                row["citation_count"] = len(model.citations)
                row["citations"] = [
                    {
                        "number": item.number,
                        "label": item.reference.label,
                        "locator": item.reference.locator,
                    }
                    for item in model.citations
                ]
                row["citation_model_verified"] = True
            except Exception as exc:
                row["citation_error"] = f"{type(exc).__name__}: {exc}"[:1600]
        elif row["search_complete"]:
            row["citation_error"] = "completed search has no screened context"
        row.update(web_key=None, web_partial=None, web_steps=0, web_lines=0, web_error=None)
        try:
            view = build_standard_web_group_proof_view(
                n=n, k=k, max_depth=2, mode="narrative", citation_source="model",
            )
            row["web_key"] = view.key
            row["web_partial"] = view.partial_result
            row["web_steps"] = len(view.steps)
            row["web_lines"] = len(view.rendered_lines)
        except Exception as exc:
            row["web_error"] = f"{type(exc).__name__}: {exc}"[:1600]
    except Exception as exc:
        row["exception"] = f"{type(exc).__name__}: {exc}"[:1600]
        row["traceback"] = traceback.format_exc()[-3000:]
    row["audit_result"] = classify_observation(row)
    print(SENTINEL + json.dumps(row, ensure_ascii=False, sort_keys=True), flush=True)
    return 0


def parse_worker_output(stdout: str, exit_code: int, n: int, k: int) -> dict:
    markers = [line[len(SENTINEL):] for line in stdout.splitlines() if line.startswith(SENTINEL)]
    if exit_code or len(markers) != 1:
        return {"n": n, "k": k, "audit_result": "WORKER_FAILED",
                "exit_code": exit_code, "marker_count": len(markers),
                "diagnostics": [stdout[-1500:]]}
    try:
        row = json.loads(markers[0])
    except json.JSONDecodeError as exc:
        return {"n": n, "k": k, "audit_result": "INVALID_WORKER_JSON",
                "diagnostics": [safe_text(exc)]}
    if not isinstance(row, dict) or row.get("n") != n or row.get("k") != k:
        return {"n": n, "k": k, "audit_result": "WRONG_WORKER_GOAL"}
    return {**row, "audit_result": classify_observation(row)}


def launch_worker(
    root: Path, n: int, k: int, timeout_seconds: int, output: Path,
) -> dict:
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    log_path = output / f"n_{n:03d}_k_{k:03d}.log"
    try:
        process = subprocess.run(
            [sys.executable, "-B", "-m", "phase173_r1_nge3_audit.audit",
             "--worker", "--n", str(n), "--k", str(k)],
            cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", check=False,
            timeout=timeout_seconds,
        )
        log_path.write_text(process.stdout, encoding="utf-8")
        return parse_worker_output(process.stdout, process.returncode, n, k)
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or b""
        value = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
        log_path.write_text(value, encoding="utf-8")
        return {"n": n, "k": k, "audit_result": "TIMEOUT",
                "timeout_seconds": timeout_seconds}


def summarize(rows: list[dict], *, registered_count: int, selected_count: int) -> dict:
    if len({(row.get("n"), row.get("k")) for row in rows}) != len(rows):
        raise ValueError("duplicate group coordinates")
    counts: dict[str, int] = {}
    for row in rows:
        result = row.get("audit_result", "MISSING_RESULT")
        counts[result] = counts.get(result, 0) + 1
    complete = counts.get("COMPLETE_AND_WEB_VERIFIED", 0)
    problems = sum(counts.get(key, 0) for key in EXECUTION_FAILURES)
    return {
        "registered_total": registered_count,
        "scope_total": selected_count,
        "checked": len(rows),
        "not_checked_in_scope": selected_count - len(rows),
        "not_selected": registered_count - selected_count,
        "complete": complete,
        "incomplete_or_unverified": len(rows) - complete,
        "execution_failures": problems,
        "breakdown": counts,
    }


def write_json(path: Path, report: dict) -> None:
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


def write_markdown(path: Path, report: dict) -> None:
    summary = report["summary"]
    lines = [
        "# Phase 173 R1 — $n\\ge3$ 登録済み群の証明探索監査", "",
        "AUDIT_ONLY。探索を観測し、数学的規則・データ・文書は変更しない。", "",
        f"- 選択範囲：{report['scope']}",
        f"- 全登録：{summary['registered_total']} 群",
        f"- 今回の対象：{summary['scope_total']} 群",
        f"- 検査済：{summary['checked']} 群",
        f"- Web 完成検証済：{summary['complete']} 群",
        f"- 未完成・未検証：{summary['incomplete_or_unverified']} 群",
        f"- 対象外（未監査）：{summary['not_selected']} 群", "",
        "| 群 | DB typed | Search | Step | Open | Citation | Web | 判定 |",
        "|---|---|---|---:|---:|---:|---|---|",
    ]
    for row in report["rows"]:
        n, k = row["n"], row["k"]
        lines.append(
            f"| $\\pi_{{{n+k}}}^{{{n}}}$ | {row.get('db_goal_typed')} | "
            f"{row.get('search_status')} | {row.get('proven_steps')} | "
            f"{row.get('open_goals')} | {row.get('citation_count')} | "
            f"{row.get('web_key')} | {row['audit_result']} |"
        )
    lines += ["", "詳細な Subgoal・Diagnostics・Reference は audit.json と各 worker log を参照。", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    root: Path, *, scope: str, dry_run: bool, timeout_seconds: int,
    check_remote: bool = True,
) -> int:
    recovery = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    output = recovery / ("phase173_r1_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    report: dict = {
        "phase": "173 R1", "mode": "AUDIT_ONLY", "scope": scope,
        "dry_run": dry_run, "full_pytest": False, "production_modified": False,
        "rows": [], "result": "NOT_STARTED",
    }
    print("PHASE173_R1_MODE=AUDIT_ONLY", flush=True)
    print(f"PHASE173_R1_OUTPUT={output}", flush=True)
    before: dict | None = None
    code = 2
    try:
        before = preflight(root, check_remote=check_remote)
        report["preflight"] = before
        all_groups = registered_groups(root / "data/sphere.csv")
        chosen = select_groups(all_groups, scope)
        report["selected_groups"] = [list(pair) for pair in chosen]
        report["summary"] = summarize(
            report["rows"], registered_count=len(all_groups), selected_count=len(chosen),
        )
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
            print("PHASE173_R1_DRY_RUN=PASS", flush=True)
            code = 0
        else:
            for n, k in chosen:
                row = launch_worker(root, n, k, timeout_seconds, output)
                report["rows"].append(row)
                report["summary"] = summarize(
                    report["rows"], registered_count=len(all_groups),
                    selected_count=len(chosen),
                )
                write_json(output / "audit.json", report)
                print(f"PHASE173_R1_n={n}_k={k} RESULT={row['audit_result']}", flush=True)
            summary = report["summary"]
            if summary["checked"] != len(chosen):
                raise RuntimeError("missing audit observations")
            code = 2 if summary["execution_failures"] else 0
            report["result"] = (
                "AUDIT_REQUIRES_INVESTIGATION" if code else
                "AUDIT_COMPLETE_ALL_VERIFIED" if not summary["incomplete_or_unverified"]
                else "AUDIT_COMPLETE_WITH_PROOF_GAPS"
            )
            write_markdown(output / "audit.md", report)
            print("PHASE173_R1_SCOPE_CHECKED=" + str(summary["checked"]), flush=True)
            print("PHASE173_R1_WEB_COMPLETE=" + str(summary["complete"]), flush=True)
            print("PHASE173_R1_UNSELECTED=" + str(summary["not_selected"]), flush=True)
    except Exception as exc:
        report["result"] = "REFUSED_OR_ERROR"
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["traceback"] = traceback.format_exc()[-3000:]
        print("PHASE173_R1_REFUSED=" + report["error"], flush=True)
    finally:
        if before is not None:
            try:
                after = preflight(root, check_remote=False)
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
        print(f"PHASE173_R1_REPORT={output / 'audit.json'}", flush=True)
        print(f"PHASE173_R1_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print(f"PHASE173_R1_RESULT={report['result']}", flush=True)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--scope", choices=("priority", "all"), default="priority")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--n", type=int)
    parser.add_argument("--k", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-remote-check", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=240)
    args = parser.parse_args()
    if args.worker:
        if args.n is None or args.n < 3 or args.k is None or args.k < 0:
            parser.error("worker requires n>=3 and k>=0")
        return worker(args.n, args.k)
    if args.root is None:
        parser.error("--root is required")
    if args.timeout_seconds < 1:
        parser.error("timeout must be positive")
    return run(
        args.root.resolve(), scope=args.scope, dry_run=args.dry_run,
        timeout_seconds=args.timeout_seconds,
        check_remote=not args.skip_remote_check,
    )


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param(
    [switch]$DryRun,
    [ValidateSet('priority', 'all')][string]$Scope = 'priority',
    [int]$TimeoutSeconds = 240,
    [switch]$SkipRemoteCheck
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
        Write-Output 'PHASE173_R1_GIT_STATUS_BEFORE'
        & git status -sb
        & python -B -m pytest -q --disable-warnings -p no:cacheprovider `
            '.\phase173_r1_nge3_audit\tests\test_audit.py'
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 173 R1 focused pytest failed: $LASTEXITCODE"
        }
        Write-Output 'PHASE173_R1_FOCUSED_PYTEST=PASS'
        $PythonArgs = @(
            '-B', '-m', 'phase173_r1_nge3_audit.audit',
            '--root', $RepoRoot, '--scope', $Scope,
            '--timeout-seconds', [string]$TimeoutSeconds
        )
        if ($DryRun) { $PythonArgs += '--dry-run' }
        if ($SkipRemoteCheck) { $PythonArgs += '--skip-remote-check' }
        & python @PythonArgs
        $AuditExit = $LASTEXITCODE
        Write-Output 'PHASE173_R1_GIT_STATUS_AFTER'
        & git status -sb
        if ($AuditExit -ne 0) {
            throw "Phase 173 R1 audit requires investigation: $AuditExit"
        }
        Write-Output 'PHASE173_R1=PASS'
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

## `tests/test_audit.py`

```python
"""Focused offline contracts for the Phase 173 R1 read-only audit."""
from __future__ import annotations

from enum import Enum
import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import pytest

from phase173_r1_nge3_audit import audit


def verified_row(n: int, k: int) -> dict:
    return {
        "n": n, "k": k, "db_goal_typed": True,
        "search_status": "complete", "search_complete": True,
        "root_matches_db_goal": True, "open_goals": 0, "proven_steps": 2,
        "citation_model_verified": True, "citation_count": 1,
        "web_key": "generic-complete-proof", "web_partial": False,
        "web_steps": 2, "web_lines": 5, "web_error": None,
    }


def test_registered_groups_deduplicated_and_excludes_n2(tmp_path: Path) -> None:
    csv_path = tmp_path / "sphere.csv"
    csv_path.write_text(
        "k,n,id\n3,3,0\n3,3,1\n3,4,0\n3,5,0\n3,6,0\n3,7,0\n2,2,0\n0,65,0\n"
        ",,\n", encoding="utf-8-sig",
    )
    assert audit.registered_groups(csv_path) == (
        (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (65, 0),
    )


def test_invalid_registered_csv_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text("k,n,id\nbad,3,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed k"):
        audit.registered_groups(path)
    path.write_text("k,n,id\n0,bad,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed n"):
        audit.registered_groups(path)
    path.write_text("k,n\n3,3\n", encoding="utf-8")
    with pytest.raises(ValueError, match="headers"):
        audit.registered_groups(path)


def test_priority_scope_has_38_and_all_scope_keeps_unselected() -> None:
    groups = tuple(sorted(
        {(3, k) for k in range(34)} | set(audit.PRIORITY_EXTRA) | {(9, 11)}
    ))
    selected = audit.select_groups(groups, "priority")
    assert len(selected) == 38
    assert (3, 3) in selected
    assert all(target in selected for target in audit.PRIORITY_EXTRA)
    assert audit.select_groups(groups, "all") == groups
    assert audit.summarize([], registered_count=len(groups), selected_count=len(selected))[
        "not_selected"
    ] == 1
    with pytest.raises(ValueError, match="unknown"):
        audit.select_groups(groups, "other")


def test_priority_scope_rejects_missing_targets_or_stems() -> None:
    groups = tuple(sorted({(3, k) for k in range(34)} | set(audit.PRIORITY_EXTRA)))
    with pytest.raises(RuntimeError, match="n=3"):
        audit.select_groups(groups[1:], "priority")
    without = tuple(pair for pair in groups if pair != (5, 3))
    with pytest.raises(RuntimeError, match="priority"):
        audit.select_groups(without, "priority")


@pytest.mark.parametrize("field,value,expected", [
    ("db_goal_typed", False, "DB_GOAL_UNTYPED_OR_MISSING"),
    ("search_status", "search_failed", "PROOF_UNFINISHED"),
    ("open_goals", 1, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("proven_steps", 0, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("root_matches_db_goal", False, "SEARCH_COMPLETE_BUT_NOT_ROOT_VERIFIED"),
    ("citation_model_verified", False, "CITATION_MODEL_NOT_VERIFIED"),
    ("web_key", "generic-partial-proof", "WEB_NOT_VERIFIED"),
    ("web_partial", True, "WEB_NOT_VERIFIED"),
    ("web_lines", 0, "WEB_NOT_VERIFIED"),
    ("web_error", "TrustError", "WEB_NOT_VERIFIED"),
])
def test_classification_never_invents_complete_proof(
    field: str, value: object, expected: str,
) -> None:
    row = verified_row(3, 3)
    row[field] = value
    assert audit.classify_observation(row) == expected


def test_worker_exception_preempts_other_checks() -> None:
    assert audit.classify_observation({
        **verified_row(3, 3), "exception": "broken"
    }) == "WORKER_EXCEPTION"
    assert audit.classify_observation(verified_row(3, 3)) == "COMPLETE_AND_WEB_VERIFIED"


def test_parse_worker_reclassifies_untrusted_claims() -> None:
    row = {**verified_row(3, 3), "audit_result": "FAKE"}
    text = audit.SENTINEL + json.dumps(row)
    assert audit.parse_worker_output(text, 0, 3, 3)["audit_result"] == (
        "COMPLETE_AND_WEB_VERIFIED"
    )
    assert audit.parse_worker_output(text, 1, 3, 3)["audit_result"] == "WORKER_FAILED"
    assert audit.parse_worker_output(text + "\n" + text, 0, 3, 3)["audit_result"] == (
        "WORKER_FAILED"
    )
    assert audit.parse_worker_output(text, 0, 3, 4)["audit_result"] == "WRONG_WORKER_GOAL"
    assert audit.parse_worker_output(audit.SENTINEL + "bad", 0, 3, 3)[
        "audit_result"
    ] == "INVALID_WORKER_JSON"


def test_report_distinguishes_proof_gaps_from_worker_crashes() -> None:
    rows = [
        {**verified_row(3, 3), "audit_result": "COMPLETE_AND_WEB_VERIFIED"},
        {"n": 4, "k": 3, "audit_result": "PROOF_UNFINISHED"},
    ]
    summary = audit.summarize(rows, registered_count=797, selected_count=38)
    assert summary["checked"] == 2
    assert summary["complete"] == 1
    assert summary["incomplete_or_unverified"] == 1
    assert summary["not_selected"] == 759
    assert summary["not_checked_in_scope"] == 36
    assert summary["execution_failures"] == 0
    rows.append({"n": 5, "k": 3, "audit_result": "WORKER_EXCEPTION"})
    assert audit.summarize(rows, registered_count=797, selected_count=38)[
        "execution_failures"
    ] == 1
    with pytest.raises(ValueError, match="duplicate"):
        audit.summarize(rows + [rows[0]], registered_count=797, selected_count=38)


def test_preflight_rejects_dirty_tracked_files_and_wrong_head(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    responses = {
        ("rev-parse", "--show-toplevel"): str(tmp_path.resolve()),
        ("branch", "--show-current"): audit.BRANCH,
        ("rev-parse", "HEAD"): audit.REVIEWED_HEAD,
        ("status", "--porcelain", "--untracked-files=no"): "",
    }
    for filename, blob in audit.REVIEWED_BLOBS.items():
        responses[("rev-parse", "HEAD:" + filename)] = blob
        path = tmp_path / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture", encoding="utf-8")
    monkeypatch.setattr(audit, "git", lambda _root, *args: responses[args])
    monkeypatch.setattr(audit, "registered_groups", lambda _path: tuple((n, 0) for n in range(3, 800)))
    assert audit.preflight(tmp_path, check_remote=False)["head"] == audit.REVIEWED_HEAD
    responses[("status", "--porcelain", "--untracked-files=no")] = " M README.md"
    with pytest.raises(RuntimeError, match="tracked or staged"):
        audit.preflight(tmp_path, check_remote=False)
    responses[("status", "--porcelain", "--untracked-files=no")] = ""
    responses[("rev-parse", "HEAD")] = "another-head"
    with pytest.raises(RuntimeError, match="unreviewed checkout"):
        audit.preflight(tmp_path, check_remote=False)


def test_worker_uses_existing_apis_and_captures_model_references(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    class ProofSearchStatus(Enum):
        COMPLETE = "complete"

    def module(path: str, **objects: object) -> None:
        item = ModuleType(path)
        for key, value in objects.items():
            setattr(item, key, value)
        monkeypatch.setitem(sys.modules, path, item)

    goal = object()
    reference = SimpleNamespace(label="Toda Proposition", locator="(5.2)")
    given = SimpleNamespace(rule=SimpleNamespace(name="GIVEN"),
                            inference_rule=SimpleNamespace(literature_reference=reference))
    inferred = SimpleNamespace(rule=SimpleNamespace(name="INFERENCE"), inference_rule=None)
    result = SimpleNamespace(
        status=ProofSearchStatus.COMPLETE, conclusion=goal, references=("Toda",),
        proven_steps=(given, inferred), open_goals=(), diagnostics=(),
    )
    calls: list[tuple] = []

    def fake_search(*, n: int, k: int, bridge: object, context_sink):
        calls.append(("search", n, k))
        context_sink("screened")
        return result

    def fake_web(*, n: int, k: int, max_depth: int, mode: str, citation_source: str):
        calls.append(("web", n, k, max_depth, mode, citation_source))
        return SimpleNamespace(key="generic-complete-proof", partial_result=False,
                               steps=[1], rendered_lines=[1])

    model = SimpleNamespace(citations=(SimpleNamespace(
        number=1, reference=reference,
    ),))
    module("phase169_r10e4_ordered_db_prior.db_prior",
           exact_prior_database_result=lambda n, k: goal)
    module("phase165_r52_partial_proof", ProofSearchStatus=ProofSearchStatus)
    module("phase165_r52_r9_shared_math", build_shared_typed_bridge=lambda: "bridge")
    module("phase165_r55_nk_only_goal", search_group_from_registered_goal=fake_search)
    module("phase168_r3_4_link_bridge",
           build_linked_proof_narrative_model=lambda result, bridge: model)
    module("web_group_proof", build_standard_web_group_proof_view=fake_web)
    assert audit.worker(3, 3) == 0
    output = capsys.readouterr().out.strip()
    assert output.startswith(audit.SENTINEL)
    row = json.loads(output[len(audit.SENTINEL):])
    assert row["audit_result"] == "COMPLETE_AND_WEB_VERIFIED"
    assert row["citation_count"] == 1
    assert row["citations"] == [{"number": 1, "label": "Toda Proposition", "locator": "(5.2)"}]
    assert row["given_references"] == [{"label": "Toda Proposition", "locator": "(5.2)"}]
    assert calls == [("search", 3, 3), ("web", 3, 3, 2, "narrative", "model")]


def test_worker_does_not_promote_failed_search(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    class ProofSearchStatus(Enum):
        SEARCH_FAILED = "search_failed"
        COMPLETE = "complete"

    def module(path: str, **objects: object) -> None:
        item = ModuleType(path)
        for key, value in objects.items():
            setattr(item, key, value)
        monkeypatch.setitem(sys.modules, path, item)

    module("phase169_r10e4_ordered_db_prior.db_prior",
           exact_prior_database_result=lambda n, k: object())
    module("phase165_r52_partial_proof", ProofSearchStatus=ProofSearchStatus)
    module("phase165_r52_r9_shared_math", build_shared_typed_bridge=lambda: object())
    module("phase165_r55_nk_only_goal", search_group_from_registered_goal=lambda **kw:
           SimpleNamespace(status=ProofSearchStatus.SEARCH_FAILED,
                           conclusion=None, proven_steps=(), open_goals=("unsolved",),
                           diagnostics=("missing source",), references=()))
    module("web_group_proof", build_standard_web_group_proof_view=lambda **kw:
           SimpleNamespace(key="generic-partial-proof", partial_result=True,
                           steps=(), rendered_lines=()))
    assert audit.worker(4, 3) == 0
    line = capsys.readouterr().out.strip()
    row = json.loads(line[len(audit.SENTINEL):])
    assert row["search_status"] == "search_failed"
    assert row["open_goal_text"] == ["unsolved"]
    assert row["audit_result"] == "PROOF_UNFINISHED"


def test_dry_run_never_launches_a_worker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    all_groups = tuple(sorted({(3, k) for k in range(34)} | set(audit.PRIORITY_EXTRA)))
    monkeypatch.setattr(audit, "preflight", lambda root, check_remote: {"head": audit.REVIEWED_HEAD})
    monkeypatch.setattr(audit, "registered_groups", lambda _path: all_groups)
    monkeypatch.setattr(audit, "launch_worker", lambda *args: pytest.fail("worker launched"))
    assert audit.run(tmp_path, scope="priority", dry_run=True,
                     timeout_seconds=60, check_remote=False) == 0
    files = list((tmp_path / "EHPProofTracerRecovery").glob("phase173_r1_*/audit.json"))
    assert len(files) == 1
    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data["summary"]["checked"] == 0
    assert data["summary"]["scope_total"] == 38
    assert data["result"] == "DRY_RUN_PASS"
    assert data["tracked_unchanged"] is True


def test_proof_gaps_allow_completed_audit_but_worker_failures_do_not(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    groups = ((3, 3), (4, 3))
    monkeypatch.setattr(audit, "preflight", lambda root, check_remote: {"head": audit.REVIEWED_HEAD})
    monkeypatch.setattr(audit, "registered_groups", lambda _path: groups)
    monkeypatch.setattr(audit, "launch_worker", lambda root, n, k, timeout_seconds, output:
                        {"n": n, "k": k, "audit_result": "PROOF_UNFINISHED"})
    assert audit.run(tmp_path, scope="all", dry_run=False,
                     timeout_seconds=30, check_remote=False) == 0
    report = list((tmp_path / "EHPProofTracerRecovery").glob("phase173_r1_*/audit.json"))
    data = json.loads(report[0].read_text(encoding="utf-8"))
    assert data["result"] == "AUDIT_COMPLETE_WITH_PROOF_GAPS"
    assert data["summary"]["incomplete_or_unverified"] == 2
    assert (report[0].parent / "audit.md").is_file()
    monkeypatch.setattr(audit, "launch_worker", lambda root, n, k, timeout_seconds, output:
                        {"n": n, "k": k, "audit_result": "WORKER_FAILED"})
    assert audit.run(tmp_path, scope="all", dry_run=False,
                     timeout_seconds=30, check_remote=False) == 2
```

## `__init__.py`

```python
"""Phase 173 R1 audit-only package."""
```

