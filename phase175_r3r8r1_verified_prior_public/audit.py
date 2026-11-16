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
