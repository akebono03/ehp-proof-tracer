# Phase 175 R3R8R1R2 — 変更コード全文

## 変更対象（最初に列挙）

- 新規 `phase175_r3r8r1_verified_prior_public/worktree_guard.py`：モジュール定数と `reviewed_tracked_snapshot()` をモジュール先頭に追加。
- 既存 `phase175_r3r8r1_verified_prior_public/audit.py`：import 全体、`R3R8R1_REVIEWED_FILES`、`extended_scoped_preflight()` を変更。他の関数は維持。以下に置換後の**ファイル全文**を記載。
- 既存 `phase175_r3r8r1_verified_prior_public/install.py`：import 全体、`preflight()`、`verify_postflight()` を変更。以下に置換後の**ファイル全文**を記載。
- 新規 `phase175_r3r8r1_verified_prior_public/tests/test_worktree_guard.py`：テストファイル全体を追加。
- 既存 `phase175_r3r8r1_verified_prior_public/tests/test_lineage.py`：既存のパラメータ化テストへ1件追加。テストファイル全文を記載。

今回の ZIP では `phase165_r52_r9_shared_math.py` の直接変更は行わない。R3R8R1 の `run.ps1` と `route.py`、`rule.py`、`search_shared_group_goal_FULL.py.txt` は変更しない。


## worktree_guard.py（全文）

```python
"""Successor-only worktree guard for the Phase 175 R3R8R1 public installer.

The earlier Phase 175 R3 guard remains unchanged.  Its R1/R2 source pins
are rechecked by the caller after this narrowly scoped status validation.
"""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import subprocess

from phase175_r3_pi73_hopf_lift import audit as r3


PACKAGE_NAME = "phase175_r3r8r1_verified_prior_public"
PUBLIC_TARGET = "phase165_r52_r9_shared_math.py"

# No prefix or wildcard acceptance. These are precisely the inspected files
# shipped in the R3R8R1/R3R8R1R1 package lineage, plus the present guard/tests.
REVIEWED_SUCCESSOR_WORKTREE_FILES = frozenset({
    PACKAGE_NAME + "/AUDIT_PLAN_JA.md",
    PACKAGE_NAME + "/CODE_FULL_JA.md",
    PACKAGE_NAME + "/README.md",
    PACKAGE_NAME + "/TEST_RESULTS_JA.md",
    PACKAGE_NAME + "/__init__.py",
    PACKAGE_NAME + "/audit.py",
    PACKAGE_NAME + "/install.py",
    PACKAGE_NAME + "/route.py",
    PACKAGE_NAME + "/rule.py",
    PACKAGE_NAME + "/run.ps1",
    PACKAGE_NAME + "/search_shared_group_goal_FULL.py.txt",
    PACKAGE_NAME + "/worktree_guard.py",
    PACKAGE_NAME + "/tests/__init__.py",
    PACKAGE_NAME + "/tests/test_install.py",
    PACKAGE_NAME + "/tests/test_lineage.py",
    PACKAGE_NAME + "/tests/test_public_search.py",
    PACKAGE_NAME + "/tests/test_route.py",
    PACKAGE_NAME + "/tests/test_verified_prior.py",
    PACKAGE_NAME + "/tests/test_worktree_guard.py",
})


def reviewed_tracked_snapshot(
    root: Path, *, allow_public_target: bool = False,
) -> dict[str, str]:
    """Hash only explicitly reviewed, unstaged tracked edits.

    Reject staged changes, renamed/deleted files, production modifications,
    unexpected files and duplicate status records. Untracked audit files are
    left under the original R1 policy. No Git mutation or status spoofing.
    """
    root = Path(root).resolve()
    process = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=no", "-z"],
        cwd=root, capture_output=True, check=False,
    )
    if process.returncode:
        raise RuntimeError("R3R8R1R2_GIT_STATUS_READ_FAILED")
    snapshot: dict[str, str] = {}
    for raw in process.stdout.split(b"\0"):
        if not raw:
            continue
        try:
            record = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise RuntimeError("R3R8R1R2_INVALID_GIT_STATUS_ENCODING") from exc
        if len(record) < 4 or record[:2] != " M" or record[2] != " ":
            raise RuntimeError("R3R8R1R2_STAGED_OR_OTHER_TRACKED_CHANGE: " + repr(record))
        relative = record[3:]
        allowed = (r3.R3_ALLOWED_TRACKED_EDITS | REVIEWED_SUCCESSOR_WORKTREE_FILES)
        if allow_public_target:
            allowed = allowed | {PUBLIC_TARGET}
        if relative not in allowed or relative in snapshot:
            raise RuntimeError("R3R8R1R2_PROTECTED_TRACKED_CHANGE: " + relative)
        candidate = root / relative
        if not candidate.is_file() or candidate.is_symlink():
            raise RuntimeError("R3R8R1R2_AUDIT_FILE_MISSING_OR_SYMLINK: " + relative)
        snapshot[relative] = sha256(candidate.read_bytes()).hexdigest()
    return dict(sorted(snapshot.items()))
```


## audit.py（全文）

```python
"""Phase 175 R3R8R1: guarded public wiring and real Group query verification."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase175_r3r6_lemma57_general import audit as r3r6
from phase175_r3r7_lemma54_membership import audit as previous
from phase175_r3r8r1_verified_prior_public import install
from phase175_r3r8r1_verified_prior_public.worktree_guard import (
    reviewed_tracked_snapshot,
)

PACKAGE = "phase175_r3r8r1_verified_prior_public"
MARKER = "__PHASE175_R3R8R1_WORKER__="
FOCUSED_TESTS = (
    "phase175_r3r8r1_verified_prior_public/tests",
    "phase175_r3r7_lemma54_membership/tests/test_rule.py",
    "phase175_r3r6_lemma57_general/tests/test_rule.py",
    "phase175_r3_pi73_hopf_lift/tests/test_rule.py",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py",
    "phase173_r4_r1_public_connection/tests",
)
EXPECTED_R3R7 = frozenset({
    "lemma54_double_relation",
    "double_suspension_membership",
    "lemma57_zero_generator_image",
    "zero_suspension_image",
    "hopf_injectivity",
    "pi73_cyclic_lift",
})


# Explicit additions already reviewed in the R3R8 public-route stage.
# The preceding R3R7 guard correctly excludes files added after R3R7; this
# stage checks those successors without altering the historic R3R7 policy.
R3R8_REVIEWED_FILES = frozenset({
    "phase175_r3r8_pi73_public_connection/README.md",
    "phase175_r3r8_pi73_public_connection/AUDIT_PLAN_JA.md",
    "phase175_r3r8_pi73_public_connection/CODE_FULL_JA.md",
    "phase175_r3r8_pi73_public_connection/TEST_RESULTS_JA.md",
    "phase175_r3r8_pi73_public_connection/__init__.py",
    "phase175_r3r8_pi73_public_connection/audit.py",
    "phase175_r3r8_pi73_public_connection/install.py",
    "phase175_r3r8_pi73_public_connection/route.py",
    "phase175_r3r8_pi73_public_connection/run.ps1",
    "phase175_r3r8_pi73_public_connection/search_shared_group_goal_FULL.py.txt",
    "phase175_r3r8_pi73_public_connection/tests/__init__.py",
    "phase175_r3r8_pi73_public_connection/tests/test_install.py",
    "phase175_r3r8_pi73_public_connection/tests/test_route.py",
})

R3R8R1_REVIEWED_FILES = frozenset({
    "phase175_r3r8r1_verified_prior_public/README.md",
    "phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md",
    "phase175_r3r8r1_verified_prior_public/CODE_FULL_JA.md",
    "phase175_r3r8r1_verified_prior_public/TEST_RESULTS_JA.md",
    "phase175_r3r8r1_verified_prior_public/__init__.py",
    "phase175_r3r8r1_verified_prior_public/audit.py",
    "phase175_r3r8r1_verified_prior_public/install.py",
    "phase175_r3r8r1_verified_prior_public/route.py",
    "phase175_r3r8r1_verified_prior_public/rule.py",
    "phase175_r3r8r1_verified_prior_public/run.ps1",
    "phase175_r3r8r1_verified_prior_public/search_shared_group_goal_FULL.py.txt",
    "phase175_r3r8r1_verified_prior_public/tests/__init__.py",
    "phase175_r3r8r1_verified_prior_public/tests/test_install.py",
    "phase175_r3r8r1_verified_prior_public/tests/test_public_search.py",
    "phase175_r3r8r1_verified_prior_public/tests/test_route.py",
    "phase175_r3r8r1_verified_prior_public/tests/test_verified_prior.py",
    "phase175_r3r8r1_verified_prior_public/tests/test_lineage.py",
    "phase175_r3r8r1_verified_prior_public/worktree_guard.py",
    "phase175_r3r8r1_verified_prior_public/tests/test_worktree_guard.py",
})


def verify_extended_lineage(
    root: Path, r2_report: dict, checked: dict,
) -> dict[str, object]:
    """Allow exact reviewed audit-package additions, never production edits.

    Preserve the R3R7 ancestor, additive-only, and known-name checks. A
    committed R3R8 package is not an unknown production change: its contents
    are allowed by an explicit filename allowlist, not by a prefix wildcard.
    """
    old = r2_report.get("preflight", {}).get("head")
    new = checked.get("head")
    if (not isinstance(old, str) or not isinstance(new, str)
            or re.fullmatch(r"[a-f0-9]{40}", old) is None
            or re.fullmatch(r"[a-f0-9]{40}", new) is None
            or r3r6._lineage_git(root, "rev-parse", "HEAD") != new):
        raise RuntimeError("R3R8R1R1_INVALID_VERIFIED_HEAD")
    if old == new:
        return {"mode": "SAME_HEAD", "audit_only_paths": [], "reviewed_successors": []}
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", old, new],
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode:
        raise RuntimeError("R3R8R1R1_R2_HEAD_NOT_ANCESTOR")
    changes = r3r6._lineage_git(
        root, "diff", "--name-status", "--no-renames", old, new,
    )
    allowed_prior = (
        r3r6.R3_LINEAGE_ALLOWED_ADDITIONS
        | r3r6.R3R5_ALLOWED_ADDITIONS
        | r3r6.R3R6_ALLOWED_ADDITIONS
        | previous.ALLOWED_NEW_FILES
    )
    paths: list[str] = []
    successors: list[str] = []
    for line in changes.splitlines():
        status, tab, path = line.partition("\t")
        if tab != "\t" or status != "A":
            raise RuntimeError("R3R8R1R1_NON_AUDIT_CHANGE_IN_LINEAGE")
        if path.startswith(r3r6.R2_PACKAGE + "/") or path in allowed_prior:
            paths.append(path)
        elif path in R3R8_REVIEWED_FILES or path in R3R8R1_REVIEWED_FILES:
            paths.append(path)
            successors.append(path)
        else:
            raise RuntimeError("R3R8R1R1_UNKNOWN_LINEAGE_ADDITION: " + path)
    if not paths:
        raise RuntimeError("R3R8R1R1_EMPTY_DESCENDANT_DIFF")
    return {
        "mode": "AUDIT_ONLY_DESCENDANT",
        "audit_only_paths": paths,
        "reviewed_successors": successors,
    }


def extended_scoped_preflight(root: Path) -> dict[str, object]:
    """Re-run the original R3 and R2 guards plus a successor-aware lineage.

    This never bypasses the source-text pinning and never rewrites R3R7's
    historical allowlist. Unknown changes remain fail-closed.
    """
    from phase175_r3_pi73_hopf_lift import audit as r3

    if r3.R3_LINEAGE_ALLOWED_ADDITIONS != r3r6.R3_LINEAGE_ALLOWED_ADDITIONS:
        raise RuntimeError("R3R8R1R1_R3_SOURCE_GUARD_POLICY_CHANGED")
    snapshot = reviewed_tracked_snapshot(root)
    if not snapshot or set(snapshot).issubset(r3.R3_ALLOWED_TRACKED_EDITS):
        checked = r3.preflight(root)
    else:
        # R3's historic filter admits only its own old filenames.  The
        # successor filter has already rejected unknown or staged changes.
        # Reuse R3's complete R1/R2 pin checks without calling that older
        # worktree-specific allowlist again.
        checked = r3.scoped_r2_preflight(root, snapshot)
        for relative, expected in r3.EXTRA_PINS.items():
            if (not (root / relative).is_file()
                    or r3.git(root, "rev-parse", "HEAD:" + relative) != expected):
                raise RuntimeError("R3R8R1R2_R3_SOURCE_PIN_MISMATCH: " + relative)
        checked = {
            **checked,
            "r3_extra_pins": dict(r3.EXTRA_PINS),
            "r3r8r1_reviewed_tracked_edits": snapshot,
            "r3r8r1_scoped_source_guard": "REVIEWED_SUCCESSOR_UNSTAGED_ONLY",
        }
    report_file = r3.select_r2_report(None)
    r2_report = json.loads(report_file.read_text(encoding="utf-8"))
    r3.validate_r2(r2_report)
    lineage = verify_extended_lineage(root, r2_report, checked)
    source = previous.verify_lemma54_before_lemma57(root)
    return {
        "r3_source_guard": checked,
        "r2_lineage": lineage,
        "r2_report_path": str(report_file),
        "lemma54_lemma57_source": source,
    }


def latest_successful_r3r7() -> Path:
    """Use actual user-executed normal R3R7 evidence, never a claimed result."""
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    directory = base / "EHPProofTracerAudit" / "phase175_r3r7_lemma54_membership"
    for path in sorted(directory.glob("*/report.json"), reverse=True):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
            worker = report.get("worker")
            data = worker.get("data") if isinstance(worker, dict) else None
            if not isinstance(data, dict):
                continue
            rows = data.get("observations", ())
            actual = {row["name"]: row["status"] for row in rows}
            if (report.get("phase") == "175-R3R7"
                    and report.get("dry_run") is False
                    and report.get("result") == "PASS_R3R7_ISOLATED_PI73_CYCLIC_INFERRED"
                    and report.get("tracked_unchanged") is True
                    and data.get("new_specific_given") == 0
                    and data.get("new_production_rules") == 0
                    and data.get("public_provider_modified") is False
                    and set(actual) == EXPECTED_R3R7
                    and all(value == "INFERRED" for value in actual.values())):
                return path
        except (OSError, UnicodeError, KeyError, ValueError, TypeError):
            continue
    raise RuntimeError("R3R8R1_NO_VALID_COMPLETED_R3R7_NORMAL_AUDIT")


def worker() -> int:
    """Reuse the real R1 auditor: typed search + trust check + common Web renderer."""
    try:
        from phase175_r1_k4_audit.audit import inspect_one_group
        result = {"status": "INSPECTED", "data": inspect_one_group(3, 4)}
    except Exception as exc:
        result = {"status": "ERROR", "error": type(exc).__name__ + ": " + str(exc),
                  "traceback": traceback.format_exc()[-7000:]}
    print(MARKER + json.dumps(result, ensure_ascii=False), flush=True)
    return 0


def run_worker(root: Path, folder: Path, seconds: int) -> dict:
    """Constrain full public path inspection in a child process."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        completed = subprocess.run(
            [sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"],
            cwd=root, env=env, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=seconds, check=False,
        )
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "seconds": seconds}
    (folder / "worker.log").write_text(
        completed.stdout + "\nSTDERR:\n" + completed.stderr, encoding="utf-8",
    )
    rows = [line[len(MARKER):] for line in completed.stdout.splitlines()
            if line.startswith(MARKER)]
    if completed.returncode or len(rows) != 1:
        return {"status": "INVALID_WORKER", "code": completed.returncode,
                "marker_count": len(rows)}
    try:
        value = json.loads(rows[0])
    except json.JSONDecodeError:
        return {"status": "INVALID_WORKER_JSON"}
    return value if isinstance(value, dict) else {"status": "INVALID_WORKER_PAYLOAD"}


def focused_pytest(root: Path, folder: Path, seconds: int) -> None:
    """Run targeted tests only; record errors without a full-suite run."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    args = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
            *FOCUSED_TESTS]
    try:
        completed = subprocess.run(
            args, cwd=root, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=seconds, env=env, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("R3R8R1_FOCUSED_PYTEST_TIMEOUT") from exc
    output = completed.stdout + "\nSTDERR:\n" + completed.stderr
    (folder / "focused_pytest.log").write_text(output, encoding="utf-8")
    tail = completed.stdout.strip().splitlines()
    for line in tail[-3:]:
        print("PHASE175_R3R8R1_PYTEST_OUTPUT=" + line[:500], flush=True)
    if completed.returncode:
        raise RuntimeError("R3R8R1_FOCUSED_PYTEST_FAILED: " + output[-1600:])
    print("PHASE175_R3R8R1_FOCUSED_PYTEST=PASS", flush=True)


def write_report(folder: Path, report: dict[str, object]) -> None:
    """All evidence and backup files remain outside the Git checkout."""
    (folder / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 175 R3R8R1 — 通常 Group query 公開接続", "",
        "- Gate: `" + str(report.get("result")) + "`",
        "- 対象: $\\pi_7^3=\\mathbb Z/2\\{\\nu'\\eta_6\\}$",
        "- 新規結論 GIVEN: 0、保存済み証明再利用: 0",
        "- 検証済み先行 DB を許容する一般推論規則の追加: 2件",
        "- 全体 pytest: 未実施", "",
    ]
    worker_result = report.get("worker", {})
    if isinstance(worker_result, dict):
        data = worker_result.get("data", {})
        if isinstance(data, dict):
            lines += [
                "## 実測結果", "",
                "- Search: `" + str(data.get("search_status")) + "`",
                "- 完成証明: `" + str(data.get("audit_result")) + "`",
                "- 未解決 Goal: " + str(data.get("search_open_count")),
                "- 証明ステップ数: " + str(data.get("search_proven_count")),
                "- Trust boundary: " + str(data.get("trust_verified")),
                "- Web key: `" + str(data.get("web_key")) + "`",
                "- Reference 件数: " + str(data.get("reference_count")), "",
            ]
            if data.get("exception"):
                lines.append("- 例外: `" + str(data["exception"]) + "`")
            if data.get("web_error"):
                lines.append("- Web 例外: `" + str(data["web_error"]) + "`")
    if report.get("error"):
        lines += ["## 失敗", "", "`" + str(report["error"]) + "`"]
    (folder / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(root: Path, dry_run: bool, seconds: int) -> int:
    """Preflight and real verification, rolling back a failed public install."""
    root = Path(root).resolve()
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S_%fZ"
    )
    folder.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {
        "phase": "175-R3R8R1", "dry_run": dry_run, "result": "NOT_STARTED",
        "new_specific_given": 0, "new_mathematical_rules": 2,
        "full_pytest": False, "modified_file": str(install.TARGET),
    }
    installed = False
    result_code = 2
    print("PHASE175_R3R8R1_OUTPUT=" + str(folder), flush=True)
    try:
        report["preflight_source_guard"] = extended_scoped_preflight(root)
        report["r3r7_report"] = str(latest_successful_r3r7())
        report["patch_preflight"] = install.preflight(root)
        print("PHASE175_R3R8R1_SOURCE_GUARD=PASS", flush=True)
        print("PHASE175_R3R8R1_R3R7_SIX_INFERENCES=PASS", flush=True)
        if dry_run:
            # Check all source and patch contracts but do not modify any file.
            report["result"] = "PASS_R3R8R1_READ_ONLY_DRYRUN"
            result_code = 0
        else:
            report["installation"] = install.apply(root, folder)
            installed = True
            print("PHASE175_R3R8R1_PATCH_APPLIED=ONE_FUNCTION", flush=True)
            focused_pytest(root, folder, seconds)
            inspected = run_worker(root, folder, seconds)
            report["worker"] = inspected
            if inspected.get("status") != "INSPECTED":
                raise RuntimeError("R3R8R1_PUBLIC_WORKER_FAILED: " + str(inspected))
            data = inspected.get("data", {})
            print("PHASE175_R3R8R1_SEARCH=" + str(data.get("search_status")), flush=True)
            print("PHASE175_R3R8R1_TRUST_VERIFIED=" + str(data.get("trust_verified")), flush=True)
            print("PHASE175_R3R8R1_WEB_KEY=" + str(data.get("web_key")), flush=True)
            print("PHASE175_R3R8R1_WEB_REFERENCES=" + str(data.get("reference_count")), flush=True)
            if not (
                data.get("audit_result") == "COMPLETE_AND_WEB_VERIFIED"
                and data.get("search_status") == "complete"
                and data.get("search_open_count") == 0
                and data.get("search_conclusion_matches_db") is True
                and data.get("trust_verified") is True
                and data.get("model_root_verified") is True
                and data.get("web_key") == "generic-complete-proof"
                and data.get("web_partial") is False
                and isinstance(data.get("reference_count"), int)
                and data["reference_count"] >= 2
            ):
                raise RuntimeError("R3R8R1_PUBLIC_VERIFICATION_INCOMPLETE: " + str({
                    key: data.get(key) for key in (
                        "audit_result", "search_status", "search_open_count",
                        "search_proven_count", "trust_verified", "model_error",
                        "web_key", "web_error", "exception",
                    )
                }))
            install.verify_postflight(root, report["installation"])
            report["result"] = "PASS_R3R8R1_PUBLIC_PI73_COMPLETE_AND_WEB_VERIFIED"
            result_code = 0
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-6000:]
        report["result"] = "R3R8R1_REFUSED_OR_PUBLIC_VERIFICATION_FAILED"
        print("PHASE175_R3R8R1_ERROR=" + report["error"], flush=True)
    finally:
        if installed and result_code != 0:
            try:
                install.rollback(root, folder)
                report["rolled_back"] = True
                print("PHASE175_R3R8R1_ROLLBACK=PASS", flush=True)
            except Exception as exc:
                report["rolled_back"] = False
                report["rollback_error"] = str(exc)
                report["result"] = "R3R8R1_ROLLBACK_FAILED"
        report["tracked_unchanged"] = bool(dry_run or (result_code != 0 and report.get("rolled_back")))
        write_report(folder, report)
        print("PHASE175_R3R8R1_REPORT=" + str(folder / "report.json"), flush=True)
        print("PHASE175_R3R8R1_GATE=" + str(report["result"]), flush=True)
        print("(END)", flush=True)
    return result_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=install.ROOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("timeout must be positive")
    if args.worker:
        return worker()
    return run(args.root, args.dry_run, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
```


## install.py（全文）

```python
"""Guarded single-function installer for the R3R8 public proof-search route.

Only a fixed insertion into search_shared_group_goal is permitted. DryRun
never writes to the worktree, and a failed normal audit can restore its exact
original bytes; no Git staging, reset or commit is performed.
"""
from __future__ import annotations

import ast
from hashlib import sha256
from pathlib import Path
import subprocess

from phase175_r3r8r1_verified_prior_public.worktree_guard import (
    reviewed_tracked_snapshot,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = Path("phase165_r52_r9_shared_math.py")
PINNED_GIT_BLOB = "9fa11b383812570fae1a26868c98992a5934a327"
ANCHOR = "    if citing_assertion_id is not None and expansion_provider is None:\n"
PUBLIC_INSERTION = (
    "    # R3R8R1: connect the R3R7 cited general EHP proof chain, not a saved result.\n"
    "    if n == 3 and k == 4 and expansion_provider is None:\n"
    "        from phase175_r3r8r1_verified_prior_public.route import (\n"
    "            prepare_pi73_public_connection,\n"
    "        )\n"
    "        pi73_connection = prepare_pi73_public_connection(\n"
    "            bridge=bridge, goal=goal, citing_assertion_id=citing_assertion_id,\n"
    "            prior_conclusions=tuple(item.root.conclusion for item in prior),\n"
    "        )\n"
    "        if pi73_connection is not None:\n"
    "            bridge, citing_assertion_id, expansion_provider = pi73_connection\n"
)


def git(root: Path, *args: str) -> str:
    """Only execute nonmutating Git commands."""
    if not args or args[0] not in {"rev-parse", "branch", "diff", "status"}:
        raise ValueError("R3R8 read-only Git operation required")
    process = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode:
        raise RuntimeError("R3R8R1_GIT_QUERY_FAILED: " + " ".join(args))
    return process.stdout.rstrip("\r\n")


def find_function(text: str) -> tuple[int, int]:
    """Find exactly one complete top-level function using Python's AST."""
    parsed = ast.parse(text)
    matches = [node for node in parsed.body
               if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
               and node.name == "search_shared_group_goal"]
    if len(matches) != 1 or not isinstance(matches[0], ast.FunctionDef):
        raise RuntimeError("R3R8R1_SEARCH_FUNCTION_NOT_UNIQUE")
    node = matches[0]
    lines = text.splitlines(keepends=True)
    return (sum(len(line) for line in lines[:node.lineno - 1]),
            sum(len(line) for line in lines[:node.end_lineno]))


def preflight(root: Path = ROOT) -> dict[str, object]:
    """Verify exact tracked original, reviewed function contract and clean index."""
    root = Path(root).resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R3R8R1_NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R3R8R1_WRONG_BRANCH")
    if git(root, "rev-parse", "HEAD:" + TARGET.as_posix()) != PINNED_GIT_BLOB:
        raise RuntimeError("R3R8R1_UNREVIEWED_PRODUCTION_BLOB")
    # The prior R3R7 handoff explicitly recorded a clean tracked worktree.
    # A later audited ZIP may replace files already committed at this HEAD.
    # Those changes are allowed only under the exact successor-file policy;
    # the production target itself must still be clean before installation.
    tracked_before = reviewed_tracked_snapshot(root)
    content = (root / TARGET).read_bytes()
    if content.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R3R8R1_UNEXPECTED_BOM")
    original = content.decode("utf-8").replace("\r\n", "\n")
    start, end = find_function(original)
    original_function = original[start:end]
    if original_function.count(ANCHOR) != 1 or PUBLIC_INSERTION in original:
        raise RuntimeError("R3R8R1_UNREVIEWED_ROUTING_ANCHOR")
    template = (PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(encoding="utf-8")
    if template.count(PUBLIC_INSERTION) != 1:
        raise RuntimeError("R3R8R1_FULL_FUNCTION_TEMPLATE_INVALID")
    old_ast = ast.dump(ast.parse(original_function), include_attributes=False)
    source_ast = ast.dump(ast.parse(template.replace(PUBLIC_INSERTION, "")), include_attributes=False)
    if old_ast != source_ast:
        raise RuntimeError("R3R8R1_EXISTING_FUNCTION_CHANGED_SINCE_REVIEW")
    compiled = original[:start] + original_function.replace(
        ANCHOR, PUBLIC_INSERTION + ANCHOR, 1,
    ) + original[end:]
    compile(compiled, str(root / TARGET), "exec")
    worktree_text = content.decode("utf-8")
    newline = "\r\n" if "\r\n" in worktree_text else "\n"
    actual_anchor = ANCHOR.replace("\n", newline)
    actual_insertion = PUBLIC_INSERTION.replace("\n", newline)
    if worktree_text.count(actual_anchor) != 1:
        raise RuntimeError("R3R8R1_WORKTREE_EOL_ANCHOR_CHANGED")
    candidate_bytes = worktree_text.replace(
        actual_anchor, actual_insertion + actual_anchor, 1,
    ).encode("utf-8")
    return {
        "head": git(root, "rev-parse", "HEAD"),
        "original_git_blob": PINNED_GIT_BLOB,
        "original_sha256": sha256(content).hexdigest(),
        "candidate_sha256": sha256(candidate_bytes).hexdigest(),
        "function_name": "search_shared_group_goal",
        "modified_tracked_files": [TARGET.as_posix()],
        "reviewed_tracked_before": tracked_before,
        "new_specific_given": 0,
        "new_proof_replay": 0,
        "whole_pytest_executed": False,
    }


def apply(root: Path, backup_folder: Path) -> dict[str, object]:
    """Replace one function only; preserve the input bytes for rollback."""
    evidence = preflight(root)
    root = Path(root).resolve()
    path = root / TARGET
    before = path.read_bytes()
    original = before.decode("utf-8")
    newline = "\r\n" if "\r\n" in original else "\n"
    anchor = ANCHOR.replace("\n", newline)
    insertion = PUBLIC_INSERTION.replace("\n", newline)
    if original.count(anchor) != 1:
        raise RuntimeError("R3R8R1_SOURCE_ANCHOR_DRIFT")
    final = original.replace(anchor, insertion + anchor, 1).encode("utf-8")
    if sha256(final).hexdigest() != evidence["candidate_sha256"]:
        raise RuntimeError("R3R8R1_CANDIDATE_HASH_CHANGED")
    backup_folder.mkdir(parents=True, exist_ok=True)
    (backup_folder / "phase165_r52_r9_shared_math.py.before").write_bytes(before)
    path.write_bytes(final)
    actual = path.read_bytes()
    if actual != final:
        raise RuntimeError("R3R8R1_WRITE_VERIFICATION_FAILED")
    return {**evidence, "installed_sha256": sha256(actual).hexdigest()}


def verify_postflight(root: Path, evidence: dict[str, object]) -> None:
    """After success, only the one reviewed public function may be dirty."""
    actual = (Path(root) / TARGET).read_bytes()
    if sha256(actual).hexdigest() != evidence["installed_sha256"]:
        raise RuntimeError("R3R8R1_PATCH_MUTATED_AFTER_INSTALL")
    snapshot = reviewed_tracked_snapshot(root, allow_public_target=True)
    public_sha = snapshot.pop(TARGET.as_posix(), None)
    if public_sha != evidence["installed_sha256"]:
        raise RuntimeError("R3R8R1R2_PUBLIC_PATCH_NOT_ONLY_REVIEWED_TARGET")
    if snapshot != evidence["reviewed_tracked_before"]:
        raise RuntimeError("R3R8R1R2_REVIEWED_WORKTREE_CHANGED_DURING_RUN")


def rollback(root: Path, backup_folder: Path) -> None:
    """Restore byte-identical clean original on failed installation or audit."""
    original = (backup_folder / "phase165_r52_r9_shared_math.py.before").read_bytes()
    (Path(root) / TARGET).write_bytes(original)
    if (Path(root) / TARGET).read_bytes() != original:
        raise RuntimeError("R3R8R1_ROLLBACK_VERIFICATION_FAILED")
```


## tests/test_worktree_guard.py（全文）

```python
"""Real-Git tests for the successor-only tracked-file exception."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import subprocess

import pytest

from phase175_r3_pi73_hopf_lift import audit as r3
from phase175_r3r8r1_verified_prior_public.worktree_guard import (
    PUBLIC_TARGET,
    REVIEWED_SUCCESSOR_WORKTREE_FILES,
    reviewed_tracked_snapshot,
)


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout.strip()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    for name in (
        PUBLIC_TARGET,
        "phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md",
        "phase175_r3r8r1_verified_prior_public/audit.py",
        "phase175_r3_pi73_hopf_lift/README.md",
        "production_other.py",
    ):
        file = root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("reviewed baseline\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "-c", "user.name=EHP Audit Test",
        "-c", "user.email=test@example.invalid", "commit", "-q", "-m", "baseline")
    return root


@pytest.mark.parametrize("name", (
    "phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md",
    "phase175_r3r8r1_verified_prior_public/audit.py",
    "phase175_r3_pi73_hopf_lift/README.md",
))
def test_named_unstaged_audit_change_is_hashed(repo: Path, name: str) -> None:
    (repo / name).write_text("reviewed replacement\n", encoding="utf-8")
    snapshot = reviewed_tracked_snapshot(repo)
    assert snapshot == {
        name: sha256((repo / name).read_bytes()).hexdigest(),
    }


def test_reviewed_successor_filename_whitelist_is_explicit() -> None:
    assert "phase175_r3r8r1_verified_prior_public/audit.py" in REVIEWED_SUCCESSOR_WORKTREE_FILES
    assert PUBLIC_TARGET not in REVIEWED_SUCCESSOR_WORKTREE_FILES
    assert "production_other.py" not in REVIEWED_SUCCESSOR_WORKTREE_FILES
    assert not any(name.endswith("/*") for name in REVIEWED_SUCCESSOR_WORKTREE_FILES)
    assert "phase175_r3_pi73_hopf_lift/README.md" in r3.R3_ALLOWED_TRACKED_EDITS


@pytest.mark.parametrize("name", (PUBLIC_TARGET, "production_other.py"))
def test_production_modifications_are_rejected_before_install(repo: Path, name: str) -> None:
    (repo / name).write_text("unauthorized modification\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R3R8R1R2_PROTECTED_TRACKED_CHANGE"):
        reviewed_tracked_snapshot(repo)


def test_public_target_only_allowed_after_patch(repo: Path) -> None:
    name = "phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md"
    (repo / name).write_text("reviewed replacement\n", encoding="utf-8")
    prior = reviewed_tracked_snapshot(repo)
    (repo / PUBLIC_TARGET).write_text("exact public patch fixture\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R3R8R1R2_PROTECTED_TRACKED_CHANGE"):
        reviewed_tracked_snapshot(repo)
    actual = reviewed_tracked_snapshot(repo, allow_public_target=True)
    assert actual.pop(PUBLIC_TARGET) == sha256((repo / PUBLIC_TARGET).read_bytes()).hexdigest()
    assert actual == prior


def test_untracked_successor_files_do_not_override_old_policy(repo: Path) -> None:
    new = repo / "phase175_r3r8r1_verified_prior_public/worktree_guard.py"
    new.write_text("new audited file\n", encoding="utf-8")
    assert reviewed_tracked_snapshot(repo) == {}


def test_unlisted_successor_tracking_is_rejected(repo: Path) -> None:
    new = repo / "phase175_r3r8r1_verified_prior_public/unknown.py"
    new.write_text("unreviewed\n", encoding="utf-8")
    git(repo, "add", "-N", str(new.relative_to(repo)))
    with pytest.raises(RuntimeError, match="R3R8R1R2_STAGED_OR_OTHER_TRACKED_CHANGE"):
        reviewed_tracked_snapshot(repo)


def test_staged_reviewed_edit_rejected(repo: Path) -> None:
    name = "phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md"
    (repo / name).write_text("staged replacement\n", encoding="utf-8")
    git(repo, "add", name)
    with pytest.raises(RuntimeError, match="R3R8R1R2_STAGED_OR_OTHER_TRACKED_CHANGE"):
        reviewed_tracked_snapshot(repo)


def test_dirty_production_cannot_be_hidden_by_a_reviewed_change(repo: Path) -> None:
    doc = repo / "phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md"
    doc.write_text("reviewed replacement\n", encoding="utf-8")
    (repo / "production_other.py").write_text("unreviewed\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R3R8R1R2_PROTECTED_TRACKED_CHANGE"):
        reviewed_tracked_snapshot(repo)


def test_installer_accepts_reviewed_dirty_docs_and_preserves_them(
    repo: Path, monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    from phase175_r3r8r1_verified_prior_public import install

    git(repo, "branch", "-m", "develop")
    template = (install.PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    original = template.replace(install.PUBLIC_INSERTION, "")
    (repo / PUBLIC_TARGET).write_text(original, encoding="utf-8")
    git(repo, "add", PUBLIC_TARGET)
    git(repo, "-c", "user.name=EHP Audit Test",
        "-c", "user.email=test@example.invalid", "commit", "-q", "-m", "source fixture")
    committed_blob = git(repo, "rev-parse", "HEAD:" + PUBLIC_TARGET)
    monkeypatch.setattr(install, "PINNED_GIT_BLOB", committed_blob)

    doc = repo / "phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md"
    doc.write_text("reviewed replacement\n", encoding="utf-8")
    before_doc = reviewed_tracked_snapshot(repo)
    assert set(before_doc) == {str(doc.relative_to(repo)).replace("\\", "/")}

    evidence = install.preflight(repo)
    assert evidence["reviewed_tracked_before"] == before_doc
    backup_dir = tmp_path / "backup"
    installed = install.apply(repo, backup_dir)
    install.verify_postflight(repo, installed)
    assert (repo / PUBLIC_TARGET).read_text(encoding="utf-8") != original
    install.rollback(repo, backup_dir)
    assert (repo / PUBLIC_TARGET).read_text(encoding="utf-8") == original
    assert reviewed_tracked_snapshot(repo) == before_doc
```


## tests/test_lineage.py（全文）

```python
"""Regression tests for Phase 175 successor lineage without weakening R3R7."""
from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from phase175_r3r8r1_verified_prior_public import audit


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def commit(root: Path, message: str) -> str:
    git(root, "add", "-A")
    git(root, "-c", "user.name=EHP Audit Test",
        "-c", "user.email=test@example.invalid", "commit", "-q", "-m", message)
    return git(root, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path: Path):
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    (root / "baseline.py").write_text("production = 1\n", encoding="utf-8")
    start = commit(root, "source baseline")
    return root, start


@pytest.mark.parametrize("path", [
    "phase175_r3r8_pi73_public_connection/AUDIT_PLAN_JA.md",
    "phase175_r3r8_pi73_public_connection/route.py",
    "phase175_r3r8r1_verified_prior_public/rule.py",
    "phase175_r3r8r1_verified_prior_public/worktree_guard.py",
    "phase175_r3r7_lemma54_membership/audit.py",
])
def test_reviewed_additive_successor_accepted(repo, path: str) -> None:
    root, start = repo
    file_path = root / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("reviewed package file\n", encoding="utf-8")
    end = commit(root, "reviewed package addition")
    result = audit.verify_extended_lineage(
        root, {"preflight": {"head": start}}, {"head": end},
    )
    assert result["audit_only_paths"] == [path]
    assert result["reviewed_successors"] == (
        [path] if path in audit.R3R8_REVIEWED_FILES
        or path in audit.R3R8R1_REVIEWED_FILES else []
    )


@pytest.mark.parametrize("path", [
    "phase175_r3r8_pi73_public_connection/unreviewed.py",
    "phase175_r3r8r1_verified_prior_public/unreviewed.py",
    "phase175_r3r7_lemma54_membership/unreviewed.py",
    "src/new_production_rule.py",
])
def test_unknown_addition_still_rejected(repo, path: str) -> None:
    root, start = repo
    file_path = root / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("unreviewed\n", encoding="utf-8")
    end = commit(root, "unknown file")
    with pytest.raises(RuntimeError, match="R3R8R1R1_UNKNOWN_LINEAGE_ADDITION"):
        audit.verify_extended_lineage(
            root, {"preflight": {"head": start}}, {"head": end},
        )


def test_tracked_production_modification_rejected(repo) -> None:
    root, start = repo
    (root / "baseline.py").write_text("production = 2\n", encoding="utf-8")
    end = commit(root, "modify production")
    with pytest.raises(RuntimeError, match="R3R8R1R1_NON_AUDIT_CHANGE_IN_LINEAGE"):
        audit.verify_extended_lineage(
            root, {"preflight": {"head": start}}, {"head": end},
        )


def test_unrelated_head_rejected(repo, tmp_path: Path) -> None:
    root, start = repo
    second = tmp_path / "unrelated"
    second.mkdir()
    git(second, "init", "-q")
    (second / "file.py").write_text("x = 1\n", encoding="utf-8")
    unrelated = commit(second, "different root")
    with pytest.raises(RuntimeError, match="R3R8R1R1_R2_HEAD_NOT_ANCESTOR"):
        audit.verify_extended_lineage(
            root, {"preflight": {"head": unrelated}}, {"head": start},
        )


def test_dirty_or_forged_current_head_rejected(repo) -> None:
    root, start = repo
    with pytest.raises(RuntimeError, match="R3R8R1R1_INVALID_VERIFIED_HEAD"):
        audit.verify_extended_lineage(
            root, {"preflight": {"head": start}}, {"head": "0" * 40},
        )
```
