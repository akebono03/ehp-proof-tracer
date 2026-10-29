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
    # Force Git to emit UTF-8 path names rather than octal-quoted Japanese names.
    # Keep the exact commit/addition-only allowlist; never relax the guard.
    delta = git(root, "-c", "core.quotePath=false", "diff", "--name-status", AUDITED_HEAD, "HEAD", "--")
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
