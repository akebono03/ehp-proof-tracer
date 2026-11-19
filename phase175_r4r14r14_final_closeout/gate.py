"""Phase 175 R4R14R14: one-shot, evidence-preserving final active-suite gate.

The four historical Phase 174 checkout-pinned failures are not reclassified.
No mathematics, source registrations, proof providers or historical tests change.
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
import tempfile
import traceback
import zipfile

from phase175_r4r14r13_final_gate_preflight.audit import (
    ROOT, preflight as r13_preflight, audit as r13_audit,
)
from phase175_r4r14r12_closeout_documents.build_documents import DOCUMENT_BLOBS

PACKAGE = "phase175_r4r14r14_final_closeout"
FINAL_MARKER = "PHASE175_R4R14R14_FINAL_CLOSEOUT_20261119"
EXPECTED_LEGACY = 4
ACTIVE_COMMAND = ("-B", "-m", "pytest", "-q", "--tb=short", "--disable-warnings", "-p", "no:cacheprovider", "tests")


def evidence_dir() -> Path:
    """Write runtime evidence outside the checkout (no tracked cache mutations)."""
    return Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE


def gate_paths() -> dict[str, Path]:
    directory = evidence_dir()
    return {key: directory / name for key, name in {
        "attempt": "attempt.json", "report": "report.json", "stdout": "full_pytest_stdout.txt",
        "stderr": "full_pytest_stderr.txt", "preflight": "preflight.json",
    }.items()}


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def store_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


def parse_summary(stdout: str, exit_code: int) -> tuple[int, str]:
    """Fail closed on failures, skips, xfail, collections errors, or ambiguity."""
    if exit_code != 0:
        raise RuntimeError("FULL_PYTEST_NONZERO_EXIT: " + str(exit_code))
    lines = [line.strip() for line in stdout.splitlines()
             if re.search(r"\b\d+ passed\b", line) and re.search(r"\bin\s+\d", line)]
    if len(lines) != 1:
        raise RuntimeError("FULL_PYTEST_SUMMARY_NOT_UNIQUE")
    summary = lines[0]
    if re.search(r"\b\d+\s+(?:failed|errors?|skipped|deselected|xfailed|xpassed)\b", summary):
        raise RuntimeError("FULL_PYTEST_NONPASS_STATUS: " + summary)
    count = int(re.search(r"\b(\d+) passed\b", summary).group(1))
    if count <= 0:
        raise RuntimeError("FULL_PYTEST_EMPTY")
    return count, summary


def preflight() -> dict[str, object]:
    """Reuse exactly the R13 source/document/HEAD checks before any full test."""
    checked = r13_preflight()
    if len(checked["historical_test_names"]) != EXPECTED_LEGACY:
        raise RuntimeError("HISTORICAL_FAILURE_COUNT_CHANGED")
    if checked["legacy_guard_policy_resolved"] is not False:
        raise RuntimeError("HISTORICAL_GUARD_STATUS_CHANGED")
    if checked["document_count"] != 5:
        raise RuntimeError("DOCUMENT_COUNT_CHANGED")
    if checked["git_changes"]["unexpected_tracked"] or checked["git_changes"]["tracked_pytest_cache"]:
        raise RuntimeError("TRACKED_CHANGES_OR_CACHE_REQUIRES_REVIEW")
    remote = checked.get("origin_develop_local")
    if remote and checked["head"] != remote:
        raise RuntimeError("HEAD_DIFFERS_FROM_LOCAL_ORIGIN_DEVELOP")
    if not (ROOT / "tests" / "conftest.py").is_file():
        raise RuntimeError("ACTIVE_TESTS_DIRECTORY_MISSING")
    for name in DOCUMENT_BLOBS:
        content = (ROOT / name).read_bytes()
        if FINAL_MARKER.encode() in content:
            raise RuntimeError("DOCUMENT_ALREADY_FINALIZED: " + name)
    checked["scope"] = "active tests/ only; legacy Phase174 guards unresolved"
    checked["git_dirty_untracked"] = checked["untracked_paths"]
    return checked


def final_sections(context: dict[str, object]) -> dict[str, str]:
    """Provide only current, evidence-backed additions; retain entire R12 history."""
    common = (f"HEAD `{context['head']}`; pytest `{context['summary']}`; "
              f"stdout SHA-256 `{context['stdout_sha256']}`; "
              f"stderr SHA-256 `{context['stderr_sha256']}`.")
    english = (
        f"<!-- {FINAL_MARKER} -->\n\n"
        "## Phase 175 formally closed — active-suite scope (2026-11-19)\n\n"
        "The six registered k=4 groups (n=2–7) were independently rechecked as complete "
        "with no open goals at the R4R14R14 gate. The audited proof of "
        "$\\pi_{10}^{6}=0$ uses 14 linked ProofSteps and four literature locators. "
        "The Phase 175 end-of-phase active `tests/` suite passed once. " + common + "\n\n"
        "**Known unresolved historical policy:** four Phase 174 source-guard tests "
        "pinned to an earlier checkout/snapshot are outside the current active suite "
        "and remain known failures; they were neither fixed nor counted as passing. "
        "Formal closure applies to the registered k=4 proof scope and active suite, "
        "not the historical guards or every possible homotopy group.\n"
    )
    japanese = (
        f"<!-- {FINAL_MARKER} -->\n\n"
        "## 2026-11-19 — Phase 175 正式終了（現行アクティブテスト範囲）\n\n"
        "k=4 の登録6群（n=2〜7）は R4R14R14 終了監査で全群 `complete`、Open Goals 0。"
        "$\\pi_{10}^{6}=0$ は文献由来の先行有限巡回群と生成元零像を結合した14段階の証明木で、"
        "Proposition 4.2 (4.4)、(5.1)、Proposition 5.8、(5.9) の出典を持つ。"
        "Phase 末尾の現行 `tests/` 全体 pytest は一度実施して成功した。" + common + "\n\n"
        "**未解決の既知の境界：** Phase 174 の古い HEAD／関数スナップショットに固定された "
        "Source Guard テスト4件は現行アクティブ `tests/` 範囲外であり、既知の失敗のまま維持する。"
        "これらを PASS と見なさない。R4R14R14 は既存の数学的規則、文献 GIVEN、"
        "DB Provenance、旧 Source Guard を変更しない。正式終了の認定範囲は k=4 登録群と"
        "アクティブテストに限定し、任意の群・全文献命題の独立検証を意味しない。\n"
    )
    return {name: english if name == "README.md" else japanese for name in DOCUMENT_BLOBS}


def write_full_documents(context: dict[str, object]) -> dict[str, object]:
    """Preserve original bytes and create the complete five-file replacement bundle."""
    folder = ROOT / PACKAGE / "output"
    before_dir, after_dir = folder / "original_full", folder / "final_full"
    parts = final_sections(context)
    original: dict[str, bytes] = {}
    updated: dict[str, bytes] = {}
    for name in DOCUMENT_BLOBS:
        raw = (ROOT / name).read_bytes()
        if FINAL_MARKER.encode() in raw or b"PHASE175_R4R14R12_DOCS_20261119" not in raw:
            raise RuntimeError("DOCUMENT_PHASE_BOUNDARY_CHANGED: " + name)
        expected_hash = context["preflight"]["document_files"][name]["sha256"]
        if sha256(raw).hexdigest() != expected_hash:
            raise RuntimeError("DOCUMENT_CHANGED_DURING_GATE: " + name)
        sep = b"\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else b"\n"
        addition = parts[name].replace("\n", sep.decode()).encode("utf-8")
        updated[name] = raw + (sep if raw.endswith(b"\n") else sep + sep) + addition
        original[name] = raw
        for destination, value in ((before_dir / name, raw), (after_dir / name, updated[name])):
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(value)
            if destination.read_bytes() != value:
                raise RuntimeError("DOCUMENT_BACKUP_OR_OUTPUT_FAILED: " + name)
    archive = folder / "phase175_r4r14r14_final_five_full_documents.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in DOCUMENT_BLOBS:
            zf.write(after_dir / name, arcname=name)
    with zipfile.ZipFile(archive) as zf:
        for name in DOCUMENT_BLOBS:
            if zf.read(name) != updated[name]:
                raise RuntimeError("DOCUMENT_ARCHIVE_FAILED: " + name)
    applied: list[str] = []
    try:
        for name in DOCUMENT_BLOBS:
            target = ROOT / name
            if target.read_bytes() != original[name]:
                raise RuntimeError("CONCURRENT_DOCUMENT_CHANGE: " + name)
            temp = target.with_name(target.name + ".r4r14r14_tmp")
            temp.write_bytes(updated[name])
            os.replace(temp, target)
            applied.append(name)
        for name in DOCUMENT_BLOBS:
            if (ROOT / name).read_bytes() != updated[name]:
                raise RuntimeError("APPLIED_DOCUMENT_DIFFERS: " + name)
    except Exception:
        for name in reversed(applied):
            target = ROOT / name
            temp = target.with_name(target.name + ".r4r14r14_rollback")
            temp.write_bytes(original[name])
            os.replace(temp, target)
        raise
    return {
        "archive": str(archive),
        "files": [{"path": name, "before_sha256": sha256(original[name]).hexdigest(),
                   "after_sha256": sha256(updated[name]).hexdigest(),
                   "full_bytes": len(updated[name])} for name in DOCUMENT_BLOBS],
    }


def run(dry_run: bool, timeout: int) -> int:
    paths = gate_paths()
    if any(path.exists() for path in paths.values()):
        # Important: an earlier DryRun does NOT reserve the one-shot final attempt.
        if not dry_run or paths["attempt"].exists() or paths["report"].exists():
            print("R4R14R14_GATE=FAIL_EXISTING_ATTEMPT_OR_REPORT_REQUIRES_REVIEW")
            print("R4R14R14_EVIDENCE=" + str(evidence_dir()))
            return 1
    try:
        snapshot = preflight()
        if not dry_run:
            snapshot["groups"] = r13_audit(timeout)["groups"]
        if dry_run:
            print("R4R14R14_GATE=PASS_READ_ONLY_DRYRUN")
            print("R4R14R14_HEAD=" + snapshot["head"])
            print("R4R14R14_FULL_PYTEST=NOT_RUN")
            print("R4R14R14_LEGACY_GUARD=FOUR_KNOWN_FAILURES_UNRESOLVED")
            print("(END)")
            return 0
        paths["attempt"].parent.mkdir(parents=True, exist_ok=True)
        attempt = {"phase": "175-R4R14R14", "started_utc": datetime.now(timezone.utc).isoformat(),
                   "head": snapshot["head"], "status": "STARTED", "command": [sys.executable, *ACTIVE_COMMAND],
                   "historical_guard_failures_not_counted": EXPECTED_LEGACY}
        # Atomic exclusive creation: never rerun a full suite on an uncertain attempt.
        with paths["attempt"].open("x", encoding="utf-8") as stream:
            json.dump(attempt, stream, ensure_ascii=False, indent=2)
        store_json(paths["preflight"], snapshot)
    except Exception as exc:
        print("R4R14R14_GATE=FAIL_PREFLIGHT")
        print("R4R14R14_ERROR=" + type(exc).__name__ + ": " + str(exc))
        return 1
    print("R4R14R14_FULL_PYTEST=STARTED_ONE_PHASE_END_RUN", flush=True)
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    with paths["stdout"].open("w", encoding="utf-8") as out, paths["stderr"].open("w", encoding="utf-8") as err:
        result = subprocess.run([sys.executable, *ACTIVE_COMMAND], cwd=ROOT, stdout=out, stderr=err, env=env, check=False)
    stdout = paths["stdout"].read_text(encoding="utf-8", errors="replace")
    stderr = paths["stderr"].read_text(encoding="utf-8", errors="replace")
    report = {
        "phase": "175-R4R14R14", "gate": "FAIL_R4R14R14", "head": snapshot["head"],
        "preflight": snapshot, "full_pytest_exit": result.returncode,
        "stdout_sha256": sha256(paths["stdout"].read_bytes()).hexdigest(),
        "stderr_sha256": sha256(paths["stderr"].read_bytes()).hexdigest(),
        "historical_source_guard": "FOUR_KNOWN_FAILURES_NOT_RERUN_NOT_PASSING",
        "active_scope": "tests/", "phase175_formally_closed": False,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
    }
    try:
        passed, summary = parse_summary(stdout, result.returncode)
        report["passed"] = passed
        report["summary"] = summary
        report["documents"] = write_full_documents(report)
        report["gate"] = "PASS_R4R14R14_PHASE175_ACTIVE_SCOPE_CLOSED_WITH_HISTORICAL_GUARD_OPEN"
        report["phase175_formally_closed"] = True
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-6000:]
    store_json(paths["report"], report)
    print("R4R14R14_GATE=" + report["gate"])
    print("R4R14R14_HEAD=" + report["head"])
    print("R4R14R14_FULL_PYTEST_EXIT=" + str(result.returncode))
    print("R4R14R14_PYTEST_TAIL_BEGIN")
    for line in stdout.splitlines()[-15:]:
        print(line)
    for line in stderr.splitlines()[-8:]:
        print("STDERR: " + line)
    print("R4R14R14_PYTEST_TAIL_END")
    if "error" in report:
        print("R4R14R14_ERROR=" + report["error"])
    print("R4R14R14_EVIDENCE=" + str(evidence_dir()))
    print("R4R14R14_LEGACY_GUARD=FOUR_KNOWN_FAILURES_NOT_PASSING")
    print("R4R14R14_PHASE_CLOSED=" + str(report["phase175_formally_closed"]).upper())
    print("(END)")
    return 0 if report["phase175_formally_closed"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    args = parser.parse_args()
    if args.timeout_seconds < 30:
        parser.error("timeout-seconds must be at least 30")
    return run(args.dry_run, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
