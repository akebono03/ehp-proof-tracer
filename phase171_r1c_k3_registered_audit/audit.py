"""Read-only registered 3-stem audit (k=3, variable n >= 2).

This module does not add mathematical premises, infer groups from missing CSV
entries, or change existing project sources. Each registered (n, 3) goal is
searched independently and checked against the public trust-gated Web route.
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

EXPECTED_HEAD = "715b00d67d4b3ff4b34bf87229842d14960ea6bb"
EXPECTED_BRANCH = "develop"
EXPECTED_CSV_BLOB = "b7e98a4469e0dcf2c5ea16691a7225951fd36395"
STEM = 3
SENTINEL = "__PHASE171_R1C_WORKER__="


def run_git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=root, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if process.returncode != 0:
        message = process.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {message}")
    return process.stdout.decode("utf-8", errors="replace").strip()


def tracked_digest(root: Path) -> str:
    process = subprocess.run(
        ["git", "diff", "--binary", "HEAD", "--"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if process.returncode != 0:
        raise RuntimeError("cannot obtain tracked diff")
    return sha256(process.stdout).hexdigest()


def registered_three_stem(csv_path: Path) -> tuple[dict, ...]:
    """Enumerate explicit CSV coordinates, deduplicating generator rows."""
    counts: dict[int, int] = {}
    with csv_path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or not {"n", "k", "id"}.issubset(reader.fieldnames):
            raise ValueError("sphere.csv requires n, k, id columns")
        for line_number, row in enumerate(reader, start=2):
            k_text = (row.get("k") or "").strip()
            n_text = (row.get("n") or "").strip()
            if k_text != str(STEM):
                continue
            # Toda's CSV uses an empty row such as "3,,,,,,,,,,,,,," at each
            # stem boundary. It is not a registered group coordinate.
            if not n_text and all(
                not (row.get(column) or "").strip()
                for column in reader.fieldnames if column != "k"
            ):
                continue
            if not n_text.isdecimal() or int(n_text) < 2:
                raise ValueError(f"invalid n for k=3 at CSV row {line_number}")
            n = int(n_text)
            counts[n] = counts.get(n, 0) + 1
    if not counts:
        raise ValueError("no explicitly registered k=3 goals")
    return tuple({"n": n, "k": STEM, "csv_rows": counts[n]}
                 for n in sorted(counts))


def preflight(root: Path) -> dict:
    """Pin the reviewed Git state without contacting or modifying origin."""
    branch = run_git(root, "branch", "--show-current")
    head = run_git(root, "rev-parse", "HEAD")
    if branch != EXPECTED_BRANCH or head != EXPECTED_HEAD:
        raise RuntimeError(f"unreviewed branch or HEAD: {branch} {head}")
    origin = run_git(root, "rev-parse", "--verify", "refs/remotes/origin/develop")
    if origin != EXPECTED_HEAD:
        raise RuntimeError(f"origin/develop mismatch: {origin}")
    if run_git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked working tree is not clean")
    csv_blob = run_git(root, "rev-parse", "HEAD:data/sphere.csv")
    if csv_blob != EXPECTED_CSV_BLOB:
        raise RuntimeError("unreviewed sphere.csv blob")
    required = (
        "data/sphere.csv",
        "phase165_r55_nk_only_goal.py",
        "phase169_r10e4_ordered_db_prior/db_prior.py",
        "web_group_proof.py",
        "phase168_r3_41p13_trust_boundary/verification.py",
    )
    missing = [name for name in required if not (root / name).is_file()]
    if missing:
        raise RuntimeError(f"missing current sources: {missing}")
    return {"branch": branch, "head": head, "origin_develop": origin,
            "csv_blob": csv_blob, "tracked_digest": tracked_digest(root),
            "tracked_clean": True}


def worker(n: int) -> int:
    """Run standard typed-goal search and public Web verification, unmodified."""
    row = {"n": n, "k": STEM, "group_dimension": n + STEM,
           "result": "WORKER_FAILURE", "web_error": None}
    try:
        from phase169_r10e4_ordered_db_prior.db_prior import (
            exact_prior_database_result,
            group_coordinates,
        )
        from phase165_r52_partial_proof import ProofSearchStatus
        from phase165_r55_nk_only_goal import search_group_from_registered_goal
        from web_group_proof import build_standard_web_group_proof_view

        target = exact_prior_database_result(n, STEM)
        row["target_typed"] = target is not None
        row["target_type"] = type(target).__name__ if target is not None else None
        row["target_coordinates"] = (
            list(group_coordinates(target))
            if target is not None and group_coordinates(target) is not None
            else None
        )
        result = search_group_from_registered_goal(n=n, k=STEM)
        row["search_status"] = getattr(result.status, "value", str(result.status))
        row["proven_steps"] = len(result.proven_steps)
        row["open_goals"] = len(result.open_goals)
        row["diagnostics"] = [str(item)[:1000] for item in result.diagnostics[:10]]
        row["open_goal_samples"] = [str(item)[:1000] for item in result.open_goals[:5]]
        row["root_conclusion_matches_target"] = bool(
            target is not None and type(result.conclusion) is type(target)
            and result.conclusion == target
        )
        row["search_complete"] = bool(
            result.status is ProofSearchStatus.COMPLETE
            and not result.open_goals and result.proven_steps
            and result.conclusion is not None
        )
        row.update(web_key=None, web_partial=None, web_steps=0, web_lines=0)
        try:
            view = build_standard_web_group_proof_view(
                n=n, k=STEM, max_depth=2,
                mode="narrative", citation_source="model",
            )
            row["web_key"] = view.key
            row["web_partial"] = view.partial_result
            row["web_steps"] = len(view.steps)
            row["web_lines"] = len(view.rendered_lines)
        except Exception as exc:
            row["web_error"] = f"{type(exc).__name__}: {exc}"[:1500]
        row["result"] = classify_worker(row, n)
        exit_code = 0
    except Exception as exc:
        row["exception"] = f"{type(exc).__name__}: {exc}"[:1500]
        row["traceback"] = traceback.format_exc()[-3000:]
        exit_code = 1
    print(SENTINEL + json.dumps(row, ensure_ascii=False, sort_keys=True), flush=True)
    return exit_code


def qualifies_complete(row: dict, n: int) -> bool:
    return (
        row.get("n") == n and row.get("k") == STEM
        and row.get("group_dimension") == n + STEM
        and row.get("target_typed") is True
        and row.get("target_coordinates") == [n, STEM]
        and row.get("root_conclusion_matches_target") is True
        and row.get("search_status") == "complete"
        and row.get("search_complete") is True
        and type(row.get("proven_steps")) is int and row["proven_steps"] > 0
        and type(row.get("open_goals")) is int and row["open_goals"] == 0
        and row.get("web_key") == "generic-complete-proof"
        and row.get("web_partial") is False
        and type(row.get("web_steps")) is int and row["web_steps"] > 0
        and type(row.get("web_lines")) is int and row["web_lines"] > 0
        and row.get("web_error") is None
    )


def classify_worker(row: dict, n: int) -> str:
    if qualifies_complete(row, n):
        return "COMPLETE_AND_WEB_VERIFIED"
    if row.get("target_typed") is not True:
        return "TYPED_TARGET_UNAVAILABLE"
    if row.get("search_status") != "complete" or row.get("open_goals") != 0:
        return "PROOF_UNFINISHED"
    if row.get("root_conclusion_matches_target") is not True:
        return "CONCLUSION_MISMATCH"
    return "WEB_UNVERIFIED"


def parse_worker_output(output: str, exit_code: int, n: int) -> dict:
    markers = [line[len(SENTINEL):] for line in output.splitlines()
               if line.startswith(SENTINEL)]
    if len(markers) != 1:
        return {"n": n, "k": STEM, "result": "WORKER_FAILURE",
                "exit_code": exit_code, "marker_count": len(markers),
                "diagnostics": [output[-1500:]]}
    try:
        row = json.loads(markers[0])
    except json.JSONDecodeError as exc:
        return {"n": n, "k": STEM, "result": "WORKER_FAILURE",
                "exit_code": exit_code, "diagnostics": [str(exc)]}
    if not isinstance(row, dict) or row.get("n") != n or row.get("k") != STEM:
        return {"n": n, "k": STEM, "result": "WORKER_FAILURE",
                "exit_code": exit_code, "diagnostics": ["worker goal mismatch"]}
    if exit_code != 0 or row.get("result") == "WORKER_FAILURE":
        row["result"] = "WORKER_FAILURE"
        row["exit_code"] = exit_code
    elif row.get("result") != classify_worker(row, n):
        row["result"] = "WORKER_FAILURE"
        row["diagnostics"] = ["worker classification mismatch"]
    return row


def execute_worker(root: Path, n: int, timeout_seconds: int, output: Path) -> dict:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    path = output / f"n_{n:03d}.log"
    try:
        process = subprocess.run(
            [sys.executable, "-B", str(Path(__file__).resolve()),
             "--worker", "--n", str(n)],
            cwd=root, env=env, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, encoding="utf-8",
            errors="replace", timeout=timeout_seconds, check=False,
        )
        path.write_text(process.stdout, encoding="utf-8")
        return parse_worker_output(process.stdout, process.returncode, n)
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or b""
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")
        path.write_text(raw, encoding="utf-8")
        return {"n": n, "k": STEM, "result": "WORKER_FAILURE",
                "diagnostics": ["timeout"], "timeout_seconds": timeout_seconds}


def summarize_rows(rows: list[dict], domain: tuple[dict, ...]) -> dict:
    expected = [item["n"] for item in domain]
    actual = [item.get("n") for item in rows]
    if actual != expected or any(row.get("k") != STEM for row in rows):
        raise ValueError("worker rows do not match registered k=3 domain")
    complete = sum(row.get("result") == "COMPLETE_AND_WEB_VERIFIED" for row in rows)
    failures = sum(row.get("result") == "WORKER_FAILURE" for row in rows)
    return {"domain_checked": len(rows), "domain_complete": complete,
            "domain_gaps": len(rows) - complete, "worker_failures": failures}


def write_json(path: Path, report: dict) -> None:
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temp, path)


def write_markdown(path: Path, report: dict) -> None:
    lines = ["# Phase 171 R1C — 3-stem 全登録座標監査", "",
             "対象は k=3、n は現行 data/sphere.csv の明示登録のみ。",
             "未完成群を証明済みと扱わず、正式文書・コードは変更しない。", "",
             f"- 対象群: {report.get('domain_checked', 0)}",
             f"- 完成・Web検証済み: {report.get('domain_complete', 0)}",
             f"- 未完成・未検証: {report.get('domain_gaps', 0)}",
             f"- Worker failures: {report.get('worker_failures', 0)}", "",
             "| n | 群 | CSV行 | Typed goal | Search | Steps | Open | Web | Result |",
             "|---:|---|---:|---|---|---:|---:|---|---|"]
    registered = {entry["n"]: entry["csv_rows"] for entry in report.get("domain", [])}
    for row in report.get("rows", []):
        n = row["n"]
        lines.append(
            f"| {n} | $\\pi_{{{n + STEM}}}^{{{n}}}$ | {registered.get(n, 0)} | "
            f"{row.get('target_typed', '?')} | {row.get('search_status', '?')} | "
            f"{row.get('proven_steps', '?')} | {row.get('open_goals', '?')} | "
            f"{row.get('web_key', '?')} | {row.get('result', '?')} |"
        )
    lines.extend(["", "詳細は audit.json および n_XXX.log を参照。", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def audit(root: Path, *, dry_run: bool, timeout_seconds: int) -> int:
    recovery = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    recovery.mkdir(parents=True, exist_ok=True)
    output = recovery / ("phase171_r1c_k3_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    print("PHASE171_R1C_MODE=AUDIT_ONLY", flush=True)
    print(f"PHASE171_R1C_OUTPUT={output}", flush=True)
    report: dict = {"phase": "171 R1C", "mode": "AUDIT_ONLY",
                    "stem": STEM, "dry_run": dry_run, "full_pytest": False,
                    "production_modified": False, "rows": []}
    before = None
    exit_code = 2
    try:
        before = preflight(root)
        report["preflight"] = before
        domain = registered_three_stem(root / "data" / "sphere.csv")
        report["domain"] = list(domain)
        print(f"PHASE171_R1C_DOMAIN_REGISTERED={len(domain)}", flush=True)
        print("PHASE171_R1C_N=" + ",".join(str(item["n"]) for item in domain), flush=True)
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
            exit_code = 0
            print("PHASE171_R1C_DRY_RUN=PASS", flush=True)
        else:
            for item in domain:
                n = item["n"]
                row = execute_worker(root, n, timeout_seconds, output)
                report["rows"].append(row)
                report.update(summarize_rows(report["rows"], tuple(domain[:len(report["rows"])])))
                write_json(output / "audit.json", report)
                print(f"PHASE171_R1C_n={n} RESULT={row['result']}", flush=True)
            report.update(summarize_rows(report["rows"], domain))
            report["result"] = (
                "AUDIT_COMPLETE_WITH_WORKER_FAILURES" if report["worker_failures"]
                else "AUDIT_COMPLETE_WITH_GAPS" if report["domain_gaps"]
                else "ALL_REGISTERED_COMPLETE"
            )
            for key in ("domain_checked", "domain_complete", "domain_gaps", "worker_failures"):
                print(f"PHASE171_R1C_{key.upper()}={report[key]}", flush=True)
            exit_code = 1 if report["worker_failures"] else 0
    except Exception as exc:
        report["result"] = "AUDIT_ERROR"
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["traceback"] = traceback.format_exc()[-3000:]
        print(f"PHASE171_R1C_ERROR={report['error']}", flush=True)
    finally:
        if before is not None:
            try:
                after = preflight(root)
                report["tracked_unchanged"] = after == before
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = f"{type(exc).__name__}: {exc}"
            if not report["tracked_unchanged"]:
                report["result"] = "TRACKED_STATE_CHANGED"
                exit_code = 2
        else:
            report["tracked_unchanged"] = None
        write_json(output / "audit.json", report)
        if not dry_run:
            write_markdown(output / "audit.md", report)
        print(f"PHASE171_R1C_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print(f"PHASE171_R1C_REPORT={output / 'audit.json'}", flush=True)
        print(f"PHASE171_R1C_RESULT={report['result']}", flush=True)
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=False, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--n", type=int)
    args = parser.parse_args()
    if args.worker:
        if args.n is None or args.n < 2:
            parser.error("worker requires n >= 2")
        return worker(args.n)
    if args.root is None:
        parser.error("--root required for main audit")
    if args.timeout_seconds < 1:
        parser.error("timeout must be positive")
    return audit(args.root.resolve(), dry_run=args.dry_run,
                 timeout_seconds=args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
