"""Phase 175 R3R8: guarded public wiring and real Group query verification."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase175_r3r7_lemma54_membership import audit as previous
from phase175_r3r8_pi73_public_connection import install

PACKAGE = "phase175_r3r8_pi73_public_connection"
MARKER = "__PHASE175_R3R8_WORKER__="
FOCUSED_TESTS = (
    "phase175_r3r8_pi73_public_connection/tests",
    "phase175_r3r7_lemma54_membership/tests/test_rule.py",
    "phase175_r3r6_lemma57_general/tests/test_rule.py",
    "phase175_r3_pi73_hopf_lift/tests/test_rule.py",
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
    raise RuntimeError("R3R8_NO_VALID_COMPLETED_R3R7_NORMAL_AUDIT")


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
        raise RuntimeError("R3R8_FOCUSED_PYTEST_TIMEOUT") from exc
    output = completed.stdout + "\nSTDERR:\n" + completed.stderr
    (folder / "focused_pytest.log").write_text(output, encoding="utf-8")
    tail = completed.stdout.strip().splitlines()
    for line in tail[-3:]:
        print("PHASE175_R3R8_PYTEST_OUTPUT=" + line[:500], flush=True)
    if completed.returncode:
        raise RuntimeError("R3R8_FOCUSED_PYTEST_FAILED: " + output[-1600:])
    print("PHASE175_R3R8_FOCUSED_PYTEST=PASS", flush=True)


def write_report(folder: Path, report: dict[str, object]) -> None:
    """All evidence and backup files remain outside the Git checkout."""
    (folder / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 175 R3R8 — 通常 Group query 公開接続", "",
        "- Gate: `" + str(report.get("result")) + "`",
        "- 対象: $\\pi_7^3=\\mathbb Z/2\\{\\nu'\\eta_6\\}$",
        "- 新規結論 GIVEN: 0、保存済み証明再利用: 0",
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
        "phase": "175-R3R8", "dry_run": dry_run, "result": "NOT_STARTED",
        "new_specific_given": 0, "new_mathematical_rules": 0,
        "full_pytest": False, "modified_file": str(install.TARGET),
    }
    installed = False
    result_code = 2
    print("PHASE175_R3R8_OUTPUT=" + str(folder), flush=True)
    try:
        report["preflight_source_guard"] = previous.scoped_preflight(root)
        report["r3r7_report"] = str(latest_successful_r3r7())
        report["patch_preflight"] = install.preflight(root)
        print("PHASE175_R3R8_SOURCE_GUARD=PASS", flush=True)
        print("PHASE175_R3R8_R3R7_SIX_INFERENCES=PASS", flush=True)
        if dry_run:
            # Check all source and patch contracts but do not modify any file.
            report["result"] = "PASS_R3R8_READ_ONLY_DRYRUN"
            result_code = 0
        else:
            report["installation"] = install.apply(root, folder)
            installed = True
            print("PHASE175_R3R8_PATCH_APPLIED=ONE_FUNCTION", flush=True)
            focused_pytest(root, folder, seconds)
            inspected = run_worker(root, folder, seconds)
            report["worker"] = inspected
            if inspected.get("status") != "INSPECTED":
                raise RuntimeError("R3R8_PUBLIC_WORKER_FAILED: " + str(inspected))
            data = inspected.get("data", {})
            print("PHASE175_R3R8_SEARCH=" + str(data.get("search_status")), flush=True)
            print("PHASE175_R3R8_TRUST_VERIFIED=" + str(data.get("trust_verified")), flush=True)
            print("PHASE175_R3R8_WEB_KEY=" + str(data.get("web_key")), flush=True)
            print("PHASE175_R3R8_WEB_REFERENCES=" + str(data.get("reference_count")), flush=True)
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
                raise RuntimeError("R3R8_PUBLIC_VERIFICATION_INCOMPLETE: " + str({
                    key: data.get(key) for key in (
                        "audit_result", "search_status", "search_open_count",
                        "search_proven_count", "trust_verified", "model_error",
                        "web_key", "web_error", "exception",
                    )
                }))
            install.verify_postflight(root, report["installation"])
            report["result"] = "PASS_R3R8_PUBLIC_PI73_COMPLETE_AND_WEB_VERIFIED"
            result_code = 0
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-6000:]
        report["result"] = "R3R8_REFUSED_OR_PUBLIC_VERIFICATION_FAILED"
        print("PHASE175_R3R8_ERROR=" + report["error"], flush=True)
    finally:
        if installed and result_code != 0:
            try:
                install.rollback(root, folder)
                report["rolled_back"] = True
                print("PHASE175_R3R8_ROLLBACK=PASS", flush=True)
            except Exception as exc:
                report["rolled_back"] = False
                report["rollback_error"] = str(exc)
                report["result"] = "R3R8_ROLLBACK_FAILED"
        report["tracked_unchanged"] = bool(dry_run or (result_code != 0 and report.get("rolled_back")))
        write_report(folder, report)
        print("PHASE175_R3R8_REPORT=" + str(folder / "report.json"), flush=True)
        print("PHASE175_R3R8_GATE=" + str(report["result"]), flush=True)
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
