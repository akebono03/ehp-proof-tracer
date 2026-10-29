"""Phase 170 R3-R8: read-only exhaustive inspection of explicit n=2 DB entries.

The independent worker for each stem invokes ordinary proof search and the
public, trust-gated Web path.  All results are observational.  Do not promote
DB rows to additional axioms and do not modify repository files.
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

REVIEWED_HEAD_UNCOMMITTED = "84a9d8ad6110ed82b80bdeb7e9a0c5a361214de0"
REVIEWED_HEAD_COMMITTED = "f479e0aabdfeefa69ad986e20c0f69ce0efd7bbd"
REVIEWED_GIT_BLOB_BEFORE_R3R7 = "b3e104857e3a8129fb01df65ce3a38ff188ecd1f"
REVIEWED_GIT_BLOB_AFTER_R3R7 = "3bf9dfa2080e330e7030f0f0a7762f3fb1fa8fff"
REVIEWED_R3R7_FILE_SHA256 = "d2dcaab3dd6555c0b998f73835ed792ff405479c73a8687ae2accb04de638f73"
TARGET = "phase168_r2_toda52_transport.py"
SENTINEL = "__R3R8_RESULT__="


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if proc.returncode:
        raise RuntimeError(f"git {' '.join(args)} exited {proc.returncode}: {proc.stderr.strip()}")
    return proc.stdout.strip()


def checked_db_stems(csv_path: Path) -> tuple[int, ...]:
    """Use only explicit sphere.csv rows, not stable-range inferred rows."""
    with csv_path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or not {"n", "k", "id"}.issubset(reader.fieldnames):
            raise ValueError("sphere.csv is missing n/k/id columns")
        stems: set[int] = set()
        for row in reader:
            n, k = (row.get("n") or "").strip(), (row.get("k") or "").strip()
            if n == "2":
                if not k or not k.isdecimal():
                    raise ValueError(f"malformed explicit n=2 stem: {row!r}")
                stems.add(int(k))
    if not stems:
        raise ValueError("no explicit n=2 DB rows")
    return tuple(sorted(stems))


def phase170_r3r8_preflight(root: Path) -> dict:
    """Accept only byte-verified R3-R7, whether committed or uncommitted."""
    branch, head = git(root, "branch", "--show-current"), git(root, "rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError(f"unreviewed branch: {branch}")
    if head == REVIEWED_HEAD_UNCOMMITTED:
        expected_blob = REVIEWED_GIT_BLOB_BEFORE_R3R7
        expected_changes = [TARGET]
        installation = "R3R7_UNCOMMITTED"
    elif head == REVIEWED_HEAD_COMMITTED:
        expected_blob = REVIEWED_GIT_BLOB_AFTER_R3R7
        expected_changes = []
        installation = "R3R7_COMMITTED"
    else:
        raise RuntimeError(f"unreviewed branch or HEAD: {branch} {head}")
    if git(root, "rev-parse", f"HEAD:{TARGET}") != expected_blob:
        raise RuntimeError("committed source blob differs from reviewed version")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("staged tracked changes present")
    changes = git(root, "diff", "--name-only").splitlines()
    if changes != expected_changes:
        raise RuntimeError(f"unexpected tracked changes: {changes!r}")
    actual_sha = sha256((root / TARGET).read_bytes()).hexdigest()
    if actual_sha != REVIEWED_R3R7_FILE_SHA256:
        raise RuntimeError(f"R3-R7 source bytes differ: {actual_sha}")
    for relative in (
        "phase170_r3_r6_prop58_source.py",
        "phase169_r10e4_ordered_db_prior/db_prior.py",
        "phase168_r3_41p13_trust_boundary/verification.py",
        "web_group_proof.py",
        "data/sphere.csv",
        "data/HyoujiGen.csv",
    ):
        if not (root / relative).is_file():
            raise RuntimeError(f"required reviewed source missing: {relative}")
    return {
        "branch": branch,
        "head": head,
        "installation": installation,
        "r3r7_source_sha256": actual_sha,
        "tracked_changed_paths": changes,
    }


def status_kind(k: int, *, completed: bool, has_target: bool, has_source: bool) -> str:
    if k == 0:
        return "OUTSIDE_TODA_5_2_DOMAIN"
    if completed:
        return "COMPLETE_AND_WEB_VERIFIED"
    if not has_target:
        return "TARGET_DB_UNTYPED_OR_MISSING"
    if k >= 3 and not has_source:
        return "SOURCE_DB_UNTYPED_OR_MISSING"
    return "PROOF_UNFINISHED"


def worker(k: int) -> int:
    """Isolated active proof search; emit a machine-readable result even on error."""
    data = {"k": k, "n": 2, "group_dimension": k + 2, "toda52_applicable": k >= 1}
    try:
        from phase169_r10e4_ordered_db_prior.db_prior import (
            exact_prior_database_result, group_coordinates, precedes_db_goal,
        )
        target = exact_prior_database_result(2, k)
        data["target_typed"] = target is not None
        data["target_type"] = type(target).__name__ if target is not None else None
        if k >= 1:
            source = exact_prior_database_result(3, k - 1)
            data["source_typed"] = source is not None
            data["source_type"] = type(source).__name__ if source is not None else None
            data["source_coordinates"] = list(group_coordinates(source)) if source is not None and group_coordinates(source) is not None else None
            data["source_precedes"] = precedes_db_goal(3, k - 1, 2, k)
        else:
            data["source_typed"] = None
            data["source_type"] = None
            data["source_precedes"] = None
            data["source_coordinates"] = None

        from phase165_r52_partial_proof import ProofSearchStatus
        from phase165_r55_nk_only_goal import search_group_from_registered_goal
        from web_group_proof import build_standard_web_group_proof_view
        result = search_group_from_registered_goal(n=2, k=k)
        data["search_status"] = getattr(result.status, "value", str(result.status))
        data["proven_steps"] = len(result.proven_steps)
        data["open_goals"] = len(result.open_goals)
        data["diagnostics"] = [str(d)[:900] for d in result.diagnostics[:8]]
        data["root_conclusion_matches_target"] = bool(target is not None and result.conclusion == target)
        data["search_complete"] = (result.status is ProofSearchStatus.COMPLETE
                                   and not result.open_goals and bool(result.proven_steps))
        data["web_key"] = None
        data["web_partial"] = None
        data["web_steps"] = 0
        data["web_lines"] = 0
        data["web_error"] = None
        try:
            view = build_standard_web_group_proof_view(
                n=2, k=k, max_depth=2, mode="narrative", citation_source="model",
            )
            data["web_key"] = view.key
            data["web_partial"] = view.partial_result
            data["web_steps"] = len(view.steps)
            data["web_lines"] = len(view.rendered_lines)
        except Exception as exc:
            data["web_error"] = f"{type(exc).__name__}: {exc}"[:1200]
        passed = (data["search_complete"] and data["web_key"] == "generic-complete-proof"
                  and data["web_partial"] is False and data["web_steps"] > 0
                  and data["web_lines"] > 0)
        data["result"] = status_kind(k, completed=passed,
                                     has_target=bool(data["target_typed"]),
                                     has_source=bool(data["source_typed"]))
    except Exception as exc:
        data["result"] = "WORKER_EXCEPTION"
        data["exception"] = f"{type(exc).__name__}: {exc}"[:1500]
        data["traceback"] = traceback.format_exc()[-2500:]
    print(SENTINEL + json.dumps(data, ensure_ascii=False, sort_keys=True), flush=True)
    return 0


def run(root: Path, dry_run: bool, min_k: int, max_k: int | None, timeout_seconds: int) -> int:
    output = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery" / (
        "phase170_r3_r8_n2_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    )
    output.mkdir(parents=True, exist_ok=False)
    print("PHASE170_R3R8_MODE=AUDIT_ONLY", flush=True)
    print(f"PHASE170_R3R8_OUTPUT={output}", flush=True)
    report = {"phase": "170 R3-R8", "mode": "AUDIT_ONLY", "dry_run": dry_run,
              "full_pytest": False, "source_files_modified": False}
    try:
        report["preflight"] = phase170_r3r8_preflight(root)
        stems = checked_db_stems(root / "data" / "sphere.csv")
        checked = tuple(k for k in stems if k >= min_k and (max_k is None or k <= max_k))
        if not checked:
            raise RuntimeError("no explicit DB stems in requested audit range")
        report["all_explicit_n2_stems"] = list(stems)
        report["checked_stems"] = list(checked)
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
            print("PHASE170_R3R8_DRY_RUN=PASS", flush=True)
            return 0
        env = os.environ.copy()
        env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        rows = []
        script = Path(__file__).resolve()
        for k in checked:
            try:
                child = subprocess.run(
                    [sys.executable, "-B", str(script), "--worker", "--k", str(k)],
                    cwd=root, env=env, text=True, encoding="utf-8", errors="replace",
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    timeout=timeout_seconds, check=False,
                )
                (output / f"k_{k:03d}.log").write_text(child.stdout, encoding="utf-8")
                markers = [line[len(SENTINEL):] for line in child.stdout.splitlines()
                           if line.startswith(SENTINEL)]
                if len(markers) == 1:
                    row = json.loads(markers[0])
                else:
                    row = {"k": k, "result": "WORKER_DID_NOT_REPORT", "exit": child.returncode,
                           "diagnostics": [child.stdout[-1500:]]}
                if child.returncode != 0:
                    row["result"] = "WORKER_FAILED"
                    row["exit"] = child.returncode
            except subprocess.TimeoutExpired as exc:
                row = {"k": k, "result": "TIMEOUT", "timeout_seconds": timeout_seconds}
                raw = exc.stdout or b""
                if isinstance(raw, bytes):
                    raw = raw.decode("utf-8", errors="replace")
                (output / f"k_{k:03d}.log").write_text(str(raw), encoding="utf-8")
            rows.append(row)
            print(f"PHASE170_R3R8_k={k} RESULT={row['result']}", flush=True)
        report["rows"] = rows
        domain_rows = [row for row in rows if row["k"] >= 1]
        complete = [row for row in domain_rows if row["result"] == "COMPLETE_AND_WEB_VERIFIED"]
        gaps = [row for row in domain_rows if row["result"] != "COMPLETE_AND_WEB_VERIFIED"]
        report["domain_checked"] = len(domain_rows)
        report["domain_complete"] = len(complete)
        report["domain_gaps"] = len(gaps)
        report["result"] = "ALL_CHECKED_COMPLETE" if not gaps else "AUDIT_COMPLETE_WITH_GAPS"
        lines = ["# Phase 170 R3-R8 — n=2 DB 全件監査", "", "監査のみ。production source は変更していません。", "",
                 f"- チェック対象（k>=1）：{len(domain_rows)} 件", f"- 証明と Web が完成：{len(complete)} 件",
                 f"- 未完成・未検証：{len(gaps)} 件", "", "| k | π | 型付き DB 目標 | 型付き先行 DB | 結果 |", "|---:|---|---|---|---|"]
        for row in rows:
            k = row["k"]
            lines.append("| " + str(k) + " | $\\pi_{" + str(k + 2) + "}^{2}$ | "
                         + str(row.get("target_type", "?")) + " | "
                         + str(row.get("source_type", "?")) + " | "
                         + str(row["result"]) + " |")
        lines += ["", "各 k の詳細は audit.json と k_XXX.log を参照。", ""]
        (output / "audit.md").write_text("\n".join(lines), encoding="utf-8")
        print(f"PHASE170_R3R8_DOMAIN_CHECKED={len(domain_rows)}", flush=True)
        print(f"PHASE170_R3R8_DOMAIN_COMPLETE={len(complete)}", flush=True)
        print(f"PHASE170_R3R8_DOMAIN_GAPS={len(gaps)}", flush=True)
        print(f"PHASE170_R3R8_RESULT={report['result']}", flush=True)
        return 0
    except Exception as exc:
        report["result"] = "REFUSED_OR_ERROR"
        report["error"] = f"{type(exc).__name__}: {exc}"
        print(f"PHASE170_R3R8_REFUSED={report['error']}", flush=True)
        return 2
    finally:
        try:
            report["postflight"] = phase170_r3r8_preflight(root)
            report["tracked_unchanged"] = report["postflight"] == report.get("preflight")
        except Exception as exc:
            report["tracked_unchanged"] = False
            report["postflight_error"] = f"{type(exc).__name__}: {exc}"
        path = output / "audit.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"PHASE170_R3R8_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print(f"PHASE170_R3R8_REPORT={path}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--min-k", type=int, default=0)
    parser.add_argument("--max-k", type=int)
    parser.add_argument("--timeout-seconds", type=int, default=90)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--k", type=int)
    args = parser.parse_args()
    if args.worker:
        if args.k is None or args.k < 0:
            parser.error("worker requires nonnegative --k")
        return worker(args.k)
    if args.root is None:
        parser.error("parent run requires --root")
    if args.min_k < 0 or (args.max_k is not None and args.max_k < args.min_k):
        parser.error("invalid stem range")
    if args.timeout_seconds < 1:
        parser.error("timeout must be positive")
    return run(args.root.resolve(), args.dry_run, args.min_k, args.max_k, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
