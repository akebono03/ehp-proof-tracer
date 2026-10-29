"""Read-only Phase 171 R1C k=3 gap diagnostics from an existing audit.json.

The tool does not rerun proof search, alter database entries, or certify proofs.
It reports the three observed incomplete registered goals without changing Git.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

EXPECTED_HEAD = "715b00d67d4b3ff4b34bf87229842d14960ea6bb"
REVIEWED_CURRENT_HEAD = "30c6c5eec6c3a4bbea8ffe0fd5d84e1f600e6f33"
ALLOWED_WORKTREE_HEADS = frozenset({EXPECTED_HEAD, REVIEWED_CURRENT_HEAD})
EXPECTED_BRANCH = "develop"
EXPECTED_STEM = 3
EXPECTED_DOMAIN_SIZE = 32
EXPECTED_INCOMPLETE = (3, 4, 5)
ACCEPTED_RESULTS = frozenset({
    "COMPLETE_AND_WEB_VERIFIED",
    "PROOF_UNFINISHED",
    "TYPED_TARGET_UNAVAILABLE",
    "CONCLUSION_MISMATCH",
    "WEB_UNVERIFIED",
    "WORKER_FAILURE",
})
DIAGNOSTIC_FIELDS = (
    "target_typed", "target_type", "target_coordinates",
    "search_status", "proven_steps", "open_goals", "open_goal_samples",
    "diagnostics", "search_complete", "root_conclusion_matches_target",
    "web_key", "web_partial", "web_steps", "web_lines", "web_error",
    "exception", "traceback",
)


def git(root: Path, *args: str) -> str:
    """Run read-only Git inspection; fail on errors."""
    process = subprocess.run(
        ["git", *args], cwd=root, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if process.returncode:
        error = process.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)}: {error}")
    return process.stdout.decode("utf-8", errors="replace").strip()


def tracked_state(root: Path) -> dict:
    """Reject a changed production tree; ignore untracked audit directories."""
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    origin = git(root, "rev-parse", "--verify", "refs/remotes/origin/develop")
    if branch != EXPECTED_BRANCH or head not in ALLOWED_WORKTREE_HEADS or origin != head:
        raise RuntimeError(f"unexpected Git state: {branch}, {head}, {origin}")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked files have uncommitted changes")
    diff = subprocess.run(
        ["git", "diff", "--binary", "HEAD", "--"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if diff.returncode:
        raise RuntimeError("could not inspect tracked diff")
    return {"branch": branch, "head": head, "origin_develop": origin,
            "tracked_digest": sha256(diff.stdout).hexdigest(), "tracked_clean": True}


def validate_report(report: object) -> tuple[dict, ...]:
    """Validate the original R1C completed 32-row audit before diagnosing it."""
    if not isinstance(report, dict):
        raise ValueError("audit.json must contain an object")
    if report.get("phase") != "171 R1C" or report.get("stem") != EXPECTED_STEM:
        raise ValueError("wrong audit phase or stem")
    if report.get("dry_run") is not False:
        raise ValueError("dry-run audit cannot be used")
    if report.get("result") != "AUDIT_COMPLETE_WITH_GAPS":
        raise ValueError("audit did not finish with recorded gaps")
    if report.get("tracked_unchanged") is not True:
        raise ValueError("R1C did not verify unchanged tracked files")
    preflight = report.get("preflight")
    if not isinstance(preflight, dict) or preflight.get("head") != EXPECTED_HEAD:
        raise ValueError("unexpected reviewed HEAD in audit")
    domain, rows = report.get("domain"), report.get("rows")
    if not isinstance(domain, list) or not isinstance(rows, list):
        raise ValueError("missing domain or rows")
    if len(domain) != EXPECTED_DOMAIN_SIZE or len(rows) != EXPECTED_DOMAIN_SIZE:
        raise ValueError("R1C domain or worker count differs from 32")
    ns = []
    for registered, row in zip(domain, rows):
        if not isinstance(registered, dict) or not isinstance(row, dict):
            raise ValueError("invalid domain or worker row")
        n = registered.get("n")
        if type(n) is not int or n < 2 or registered.get("k") != EXPECTED_STEM:
            raise ValueError("invalid registered group coordinate")
        if row.get("n") != n or row.get("k") != EXPECTED_STEM:
            raise ValueError("worker row does not match registered coordinate")
        if type(registered.get("csv_rows")) is not int or registered["csv_rows"] < 1:
            raise ValueError("invalid registered CSV row count")
        if row.get("result") not in ACCEPTED_RESULTS:
            raise ValueError(f"unknown worker result at n={n}")
        ns.append(n)
    if ns != sorted(set(ns)):
        raise ValueError("registered n coordinates must be unique and sorted")
    complete = sum(row["result"] == "COMPLETE_AND_WEB_VERIFIED" for row in rows)
    failures = sum(row["result"] == "WORKER_FAILURE" for row in rows)
    gaps = tuple(row["n"] for row in rows
                 if row["result"] != "COMPLETE_AND_WEB_VERIFIED")
    if (report.get("domain_checked"), report.get("domain_complete"),
        report.get("domain_gaps"), report.get("worker_failures")) != (
        EXPECTED_DOMAIN_SIZE, complete, len(gaps), failures,
    ):
        raise ValueError("R1C summary counters do not match worker rows")
    if failures or gaps != EXPECTED_INCOMPLETE:
        raise ValueError(f"unexpected gap coordinates or worker failures: {gaps}")
    return tuple(row for row in rows
                 if row["result"] != "COMPLETE_AND_WEB_VERIFIED")


def diagnostic_category(row: dict) -> str:
    """Classify observable symptoms only, not mathematical root causes."""
    if row.get("target_typed") is not True:
        return "TYPED_GOAL_NOT_RESOLVED"
    if row.get("search_status") != "complete" or row.get("open_goals") != 0:
        return "SEARCH_UNFINISHED"
    if row.get("root_conclusion_matches_target") is not True:
        return "CONCLUSION_NOT_MATCHED"
    return "WEB_VERIFICATION_NOT_COMPLETE"


def extract_details(gaps: tuple[dict, ...]) -> tuple[dict, ...]:
    """Preserve original diagnostic strings, open goal examples and Web fields."""
    return tuple({
        "n": row["n"], "k": EXPECTED_STEM,
        "group_dimension": row.get("group_dimension", row["n"] + EXPECTED_STEM),
        "result": row["result"],
        "observed_category": diagnostic_category(row),
        **{name: row.get(name) for name in DIAGNOSTIC_FIELDS},
    } for row in gaps)


def render_markdown(details: tuple[dict, ...], source: Path) -> str:
    """Write a human-readable evidence report, with no proof claims."""
    lines = [
        "# Phase 171 R1D — 3-stem 未完成3群の詳細診断", "",
        "R1C の既存監査結果だけを再分析。新しい証明・推論・引用は追加しない。", "",
        f"入力監査: `{source.name}`", "",
        "| n | Goal | 状態 | Search | Steps | Open | Web |",
        "|---:|---|---|---|---:|---:|---|",
    ]
    for row in details:
        n = row["n"]
        lines.append(
            f"| {n} | $\\pi_{{{n + 3}}}^{{{n}}}$ | {row['observed_category']} | "
            f"{row['search_status']} | {row['proven_steps']} | "
            f"{row['open_goals']} | {row['web_key']} |"
        )
    for row in details:
        n = row["n"]
        lines += ["", f"## $\\pi_{{{n + 3}}}^{{{n}}}$", "",
                  "```json", json.dumps(row, ensure_ascii=False, indent=2), "```"]
    lines += ["", "`observed_category` は現象の分類であり、原因の確定ではない。", ""]
    return "\n".join(lines)


def run(root: Path, report_path: Path, *, dry_run: bool = False) -> int:
    """Read, verify, and report without writing to the repository."""
    before = tracked_state(root)
    report = json.loads(report_path.read_text(encoding="utf-8-sig"))
    gaps = validate_report(report)
    details = extract_details(gaps)
    print("PHASE171_R1D_MODE=READ_ONLY_REPORT_TRIAGE", flush=True)
    print(f"PHASE171_R1D_SOURCE={report_path}", flush=True)
    print(f"PHASE171_R1D_GAPS={len(details)}", flush=True)
    print("PHASE171_R1D_N=" + ",".join(str(row["n"]) for row in details), flush=True)
    for row in details:
        print("PHASE171_R1D_DETAIL=" + json.dumps(row, ensure_ascii=False, sort_keys=True), flush=True)
    if dry_run:
        print("PHASE171_R1D_DRY_RUN=PASS", flush=True)
    else:
        recovery = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
        output = recovery / ("phase171_r1d_k3_gaps_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        output.mkdir(parents=True, exist_ok=False)
        payload = {"phase": "171 R1D", "read_only": True,
                   "source": str(report_path), "reviewed_head": EXPECTED_HEAD,
                   "complete": report["domain_complete"], "checked": report["domain_checked"],
                   "gaps": list(details)}
        (output / "gap_details.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        (output / "gap_details.md").write_text(
            render_markdown(details, report_path), encoding="utf-8")
        print(f"PHASE171_R1D_OUTPUT={output}", flush=True)
        print(f"PHASE171_R1D_REPORT={output / 'gap_details.json'}", flush=True)
    after = tracked_state(root)
    unchanged = before == after
    print(f"PHASE171_R1D_TRACKED_UNCHANGED={unchanged}", flush=True)
    print("PHASE171_R1D_RESULT=" + ("PASS" if unchanged else "TRACKED_CHANGED"), flush=True)
    return 0 if unchanged else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), args.report.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
