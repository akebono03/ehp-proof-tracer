"""Phase 176 R1: read-only k=5 registration and live proof-search audit."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r1_k5_source_first_audit"
PREVIOUS_HEAD = "90e8025c31841e522b3bb36f002ec44dfd4b89aa"
REVIEWED_REMOTE_HEAD = "bc318d6a66bd124cb6707559a6d2dc42128443b3"
MARKER = "PHASE176_R1_WORKER_JSON="
DOCUMENTS = ("README.md", "docs/design.md", "docs/development_log.md", "docs/proof_records.md", "docs/roadmap.md")


def git(*args: str, check: bool = True) -> tuple[int, str]:
    result = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if check and result.returncode:
        raise RuntimeError("GIT_FAILED " + " ".join(args) + ": " + result.stderr.strip())
    return result.returncode, result.stdout.strip()


def registered_pairs(csv_path: Path) -> tuple[tuple[int, int], ...]:
    if not csv_path.is_file():
        raise RuntimeError("SPHERE_CSV_MISSING")
    with csv_path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not {"n", "k"}.issubset(reader.fieldnames or ()):
            raise RuntimeError("SPHERE_CSV_COLUMNS_MISSING")
        rows = {(int(row["n"]), int(row["k"])) for row in reader if row["n"] and row["k"] and int(row["k"]) == 5 and int(row["n"]) >= 2}
    if not rows:
        raise RuntimeError("NO_REGISTERED_K5_GROUPS")
    return tuple(sorted(rows))


def preflight() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")[1]).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current")[1] != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    head = git("rev-parse", "HEAD")[1]
    if git("merge-base", "--is-ancestor", PREVIOUS_HEAD, "HEAD", check=False)[0]:
        raise RuntimeError("PHASE175_FINAL_HEAD_NOT_ANCESTOR")
    origin_code, origin = git("rev-parse", "--verify", "origin/develop", check=False)
    if origin_code:
        origin = ""
    staged = git("diff", "--cached", "--name-only")[1].splitlines()
    modified = git("diff", "--name-only")[1].splitlines()
    if staged or modified:
        raise RuntimeError("TRACKED_WORKTREE_CHANGES_REQUIRE_REVIEW: " + repr({"staged": staged, "modified": modified}))
    for name in DOCUMENTS:
        if not (ROOT / name).is_file() or "PHASE175_R4R14R14_FINAL_CLOSEOUT_20261119" not in (ROOT / name).read_text(encoding="utf-8-sig"):
            raise RuntimeError("PHASE175_CLOSEOUT_DOCUMENT_MISSING: " + name)
    if not (ROOT / "phase175_r4r14r14_final_closeout" / "gate.py").is_file():
        raise RuntimeError("PHASE175_FINAL_GATE_MISSING")
    pairs = registered_pairs(ROOT / "data" / "sphere.csv")
    return {"head": head, "reviewed_remote_head": REVIEWED_REMOTE_HEAD,
            "matches_reviewed_remote": head == REVIEWED_REMOTE_HEAD,
            "origin_develop": origin or None, "matches_local_origin_develop": bool(origin) and head == origin,
            "phase175_final_head_is_ancestor": True, "phase175_final_documents": list(DOCUMENTS),
            "registered_pairs": [list(pair) for pair in pairs],
            "untracked_paths": git("ls-files", "--others", "--exclude-standard")[1].splitlines(),
            "historical_phase174_source_guard": "FOUR_KNOWN_FAILURES_NOT_PASSING"}


def observe(n: int, k: int) -> dict[str, object]:
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_partial_proof import ProofSearchStatus
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from web_group_proof import build_standard_web_group_proof_view

    result = search_group_from_registered_goal(n=n, k=k)
    roots = [step for step in result.proven_steps if result.conclusion is not None and step.conclusion == result.conclusion]
    expected = TodaPrimaryGroup(n + k, n)
    target = result.conclusion.group if isinstance(result.conclusion, TodaPrimaryGroupZeroStatement) else getattr(result.conclusion, "lhs", None)
    complete_consistent = (result.status is not ProofSearchStatus.COMPLETE or (
        not result.open_goals and result.conclusion is not None and target == expected and len(roots) == 1))
    row = {"n": n, "k": k, "status": result.status.value,
           "structure_status": result.structure_status.value,
           "open_goal_count": len(result.open_goals), "open_goals": [str(x) for x in result.open_goals],
           "reference_count": len(result.references), "references": list(result.references),
           "proven_step_count": len(result.proven_steps), "root_step_count": len(roots),
           "conclusion": str(result.conclusion) if result.conclusion is not None else None,
           "diagnostics": list(result.diagnostics), "complete_invariants_hold": complete_consistent}
    if not complete_consistent:
        raise RuntimeError("COMPLETE_PROOF_CONTRACT_VIOLATION: " + repr((n, k)))
    try:
        view = build_standard_web_group_proof_view(n=n, k=k, max_depth=2, mode="narrative", citation_source="model")
        row["web"] = {"status": "rendered", "view_type": type(view).__name__, "repr_sample": repr(view)[:8000]}
    except Exception as exc:
        row["web"] = {"status": "failed", "error": type(exc).__name__ + ": " + str(exc)}
    return row


def worker(n: int, k: int, timeout: int) -> dict[str, object]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        proc = subprocess.run((sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker", "--n", str(n), "--k", str(k)),
                              cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return {"n": n, "k": k, "status": "worker_timeout", "error": "TIMEOUT"}
    markers = [line[len(MARKER):] for line in proc.stdout.splitlines() if line.startswith(MARKER)]
    if proc.returncode or len(markers) != 1:
        return {"n": n, "k": k, "status": "worker_error", "exit_code": proc.returncode,
                "stderr": proc.stderr[-2500:], "stdout": proc.stdout[-1000:]}
    return json.loads(markers[0])


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    return base / "report.json"


def execute(dry_run: bool, timeout: int) -> int:
    report: dict[str, object] = {"phase": "176_R1", "mode": "SOURCE_FIRST_READ_ONLY", "dry_run": dry_run,
                                 "full_pytest": "NOT_RUN", "new_given": 0, "new_rules": 0,
                                 "timestamp_utc": datetime.now(timezone.utc).isoformat(), "gate": "FAIL_R1"}
    try:
        context = preflight()
        report["preflight"] = context
        if not dry_run:
            rows = [worker(n, k, timeout) for n, k in map(tuple, context["registered_pairs"])]
            report["groups"] = rows
            report["complete"] = sum(row.get("status") == "complete" for row in rows)
            report["incomplete"] = sum(row.get("status") in ("partial", "search_failed", "not_searched") for row in rows)
            report["worker_errors"] = sum(row.get("status") in ("worker_timeout", "worker_error") for row in rows)
            report["web_failures"] = sum(row.get("web", {}).get("status") == "failed" for row in rows)
            report["gate"] = "PASS_R1_AUDIT_WITH_WEB_GAPS" if report["web_failures"] and not report["worker_errors"] else (
                "PASS_R1_AUDIT" if not report["worker_errors"] else "FAIL_R1_WORKER_ERRORS")
        else:
            report["gate"] = "PASS_R1_READ_ONLY_DRYRUN"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-7000:]
    path = report_path()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R1_GATE=" + str(report["gate"]))
    print("PHASE176_R1_REPORT=" + str(path))
    print("PHASE176_R1_HEAD=" + str(report.get("preflight", {}).get("head", "UNKNOWN")))
    if "preflight" in report:
        print("PHASE176_R1_REGISTERED=" + str(len(report["preflight"]["registered_pairs"])))
    for row in report.get("groups", []):
        print("PHASE176_R1_GROUP=" + repr((row["n"], row["k"])) + " STATUS=" + row["status"] + " OPEN=" + str(row.get("open_goal_count", "UNKNOWN")))
    if "error" in report:
        print("PHASE176_R1_ERROR=" + report["error"])
    print("PHASE176_R1_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if str(report["gate"]).startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--n", type=int, default=2)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=90)
    args = parser.parse_args()
    if args.worker:
        try:
            print(MARKER + json.dumps(observe(args.n, args.k), ensure_ascii=False))
            return 0
        except Exception:
            traceback.print_exc()
            return 1
    return execute(args.dry_run, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
