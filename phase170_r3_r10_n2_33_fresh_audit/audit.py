"""Fresh 33-stem read-only audit using the already-reviewed Phase 170 R3-R8 worker.

No mathematical inference is implemented here. The worker executes the normal
proof search and public trust-gated Web route; this harness only verifies output.
"""
from __future__ import annotations

import argparse
import ast
import csv
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

EXPECTED_HEAD = "fdf60522b6d477209e9d8d67720a63f9863e419c"
EXPECTED_BRANCH = "develop"
EXPECTED_CHANGED = frozenset({
    "phase168_r2_toda52_transport.py",
    "phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py",
})
EXPECTED_BLOBS = {
    "phase170_r3_r8_n2_exhaustive_audit/audit.py": "6d95546bf165f11029a7d56d18c03013b3ecafed",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "sources/toda/Toda_07_2.tex": "b5b366f2d2b72d7b419192fa74ab848eff098686",
}
R9_SOURCE = "phase170_r3_r9_toda712_cited_rewrite/source712.py"
WORKER = "phase170_r3_r8_n2_exhaustive_audit/audit.py"
SENTINEL = "__R3R8_RESULT__="
DOMAIN = tuple(range(1, 34))
EXPECTED_CLAUSE = (
    r"\varepsilon_3\circ\nu_{11} = \nu'\circ\ov{\nu}_6,\qquad"
    "\n"
    r"\varepsilon'\circ\eta_{13} = \nu'\circ\varepsilon_6 ."
)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return result.stdout.decode("utf-8", errors="replace").strip()


def tracked_diff_digest(root: Path) -> str:
    result = subprocess.run(
        ["git", "diff", "--binary", "HEAD", "--"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise RuntimeError("cannot capture tracked diff")
    return sha256(result.stdout).hexdigest()


def explicit_n2_stems(csv_path: Path) -> tuple[int, ...]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not {"n", "k", "id"}.issubset(reader.fieldnames):
            raise ValueError("sphere.csv lacks n/k/id columns")
        stems: set[int] = set()
        for record in reader:
            if (record.get("n") or "").strip() != "2":
                continue
            k = (record.get("k") or "").strip()
            if not k.isdecimal():
                raise ValueError("unparseable n=2 stem in sphere.csv")
            stems.add(int(k))
    missing = sorted(set(DOMAIN).difference(stems))
    if missing:
        raise RuntimeError(f"explicit n=2 DB stems missing: {missing}")
    return tuple(sorted(stems))


def checked_clause_position(root: Path) -> int:
    source = root / R9_SOURCE
    text = source.read_text(encoding="utf-8-sig")
    tree = ast.parse(text, filename=str(source))
    assignments = [node for node in tree.body if isinstance(node, ast.Assign)
                   and any(isinstance(target, ast.Name) and target.id == "CLAUSE"
                           for target in node.targets)]
    if len(assignments) != 1 or ast.literal_eval(assignments[0].value) != EXPECTED_CLAUSE:
        raise RuntimeError("R3-R9's uniquely defined CLAUSE is not the reviewed (7.12) text")
    tex = (root / "sources/toda/Toda_07_2.tex").read_text(encoding="utf-8-sig")
    if tex.count(EXPECTED_CLAUSE) != 1:
        raise RuntimeError("Toda (7.12) printed equality is missing or ambiguous")
    return tex.index(EXPECTED_CLAUSE)


def preflight(root: Path, *, check_remote: bool = True) -> dict:
    branch, head = git(root, "branch", "--show-current"), git(root, "rev-parse", "HEAD")
    if (branch, head) != (EXPECTED_BRANCH, EXPECTED_HEAD):
        raise RuntimeError(f"unreviewed branch or HEAD: {branch} {head}")
    if check_remote:
        answer = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        remote_sha = answer.split()[0] if answer else ""
        if remote_sha != EXPECTED_HEAD:
            raise RuntimeError(f"remote develop changed: {remote_sha}")
    if git(root, "diff", "--cached", "--name-only", "--"):
        raise RuntimeError("staged changes present; refusing audit")
    changes = frozenset(filter(None, git(root, "diff", "--name-only", "HEAD", "--").splitlines()))
    if changes != EXPECTED_CHANGED:
        raise RuntimeError(f"expected only installed R3-R9 changes; found: {sorted(changes)}")
    for path, blob in EXPECTED_BLOBS.items():
        if git(root, "rev-parse", f"HEAD:{path}") != blob:
            raise RuntimeError(f"committed source changed: {path}")
        if not (root / path).is_file():
            raise RuntimeError(f"required reviewed source missing: {path}")
    for path in (*EXPECTED_CHANGED, R9_SOURCE):
        if not (root / path).is_file():
            raise RuntimeError(f"required R3-R9 installed source missing: {path}")
    position = checked_clause_position(root)
    return {
        "branch": branch, "head": head,
        "tracked_changed_paths": sorted(changes),
        "tracked_diff_sha256": tracked_diff_digest(root),
        "r9_source_sha256": sha256((root / R9_SOURCE).read_bytes()).hexdigest(),
        "toda712_clause_position": position,
        "worker_sha256": sha256((root / WORKER).read_bytes()).hexdigest(),
    }


def qualified_complete(row: dict, k: int) -> bool:
    """Never trust a headline status without its checked search and Web fields."""
    return (
        row.get("k") == k and row.get("n") == 2
        and row.get("group_dimension") == k + 2
        and row.get("toda52_applicable") is True
        and row.get("target_typed") is True
        and row.get("source_precedes") is True
        and row.get("result") == "COMPLETE_AND_WEB_VERIFIED"
        and row.get("search_complete") is True
        and row.get("search_status") == "complete"
        and type(row.get("open_goals")) is int and row["open_goals"] == 0
        and type(row.get("proven_steps")) is int and row["proven_steps"] > 0
        and row.get("web_key") == "generic-complete-proof"
        and row.get("web_partial") is False
        and type(row.get("web_steps")) is int and row["web_steps"] > 0
        and type(row.get("web_lines")) is int and row["web_lines"] > 0
        and row.get("web_error") is None
    )


def parse_worker_output(output: str, exit_code: int, k: int) -> dict:
    values = [line[len(SENTINEL):] for line in output.splitlines()
              if line.startswith(SENTINEL)]
    if exit_code != 0 or len(values) != 1:
        return {"k": k, "result": "WORKER_FAILED", "audit_result": "WORKER_FAILED",
                "exit": exit_code, "marker_count": len(values),
                "diagnostics": [output[-1800:]]}
    try:
        data = json.loads(values[0])
    except json.JSONDecodeError as exc:
        return {"k": k, "result": "INVALID_WORKER_JSON", "audit_result": "INVALID_WORKER_JSON",
                "diagnostics": [str(exc)]}
    if not isinstance(data, dict) or data.get("k") != k or data.get("n") != 2:
        return {"k": k, "result": "WRONG_WORKER_GOAL", "audit_result": "WRONG_WORKER_GOAL"}
    data["audit_result"] = (
        "COMPLETE_AND_WEB_VERIFIED" if qualified_complete(data, k)
        else "PROOF_OR_WEB_NOT_VERIFIED"
    )
    return data


def run_worker(root: Path, k: int, timeout_seconds: int, output: Path) -> dict:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        process = subprocess.run(
            [sys.executable, "-B", str(root / WORKER), "--worker", "--k", str(k)],
            cwd=root, env=env, text=True, encoding="utf-8", errors="replace",
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
            timeout=timeout_seconds,
        )
        (output / f"k_{k:03d}.log").write_text(process.stdout, encoding="utf-8")
        return parse_worker_output(process.stdout, process.returncode, k)
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or b""
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")
        (output / f"k_{k:03d}.log").write_text(raw, encoding="utf-8")
        return {"k": k, "audit_result": "TIMEOUT", "result": "TIMEOUT",
                "timeout_seconds": timeout_seconds}


def domain_counts(rows: list[dict]) -> tuple[int, int, int]:
    if len(rows) != len({row.get("k") for row in rows}):
        raise ValueError("duplicate worker stem")
    complete = sum(row.get("audit_result") == "COMPLETE_AND_WEB_VERIFIED" for row in rows)
    return len(rows), complete, len(rows) - complete


def write_report(path: Path, report: dict) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def run(root: Path, *, dry_run: bool, timeout_seconds: int, check_remote: bool = True) -> int:
    recovery = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    recovery.mkdir(parents=True, exist_ok=True)
    output = recovery / ("phase170_r3_r10_n2_33_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    print("PHASE170_R3R10_MODE=AUDIT_ONLY_FRESH_33", flush=True)
    print(f"PHASE170_R3R10_OUTPUT={output}", flush=True)
    report: dict = {"phase": "170 R3-R10", "mode": "AUDIT_ONLY_FRESH_33",
                    "full_pytest": False, "production_modified": False,
                    "dry_run": dry_run, "domain": list(DOMAIN), "rows": []}
    before = None
    return_code = 2
    try:
        before = preflight(root, check_remote=check_remote)
        report["preflight"] = before
        report["explicit_n2_stems"] = list(explicit_n2_stems(root / "data" / "sphere.csv"))
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
            return_code = 0
            print("PHASE170_R3R10_DRY_RUN=PASS", flush=True)
        else:
            for k in DOMAIN:
                row = run_worker(root, k, timeout_seconds, output)
                report["rows"].append(row)
                checked, complete, gaps = domain_counts(report["rows"])
                report.update(domain_checked=checked, domain_complete=complete, domain_gaps=gaps)
                write_report(output / "audit.json", report)
                print(f"PHASE170_R3R10_k={k} RESULT={row['audit_result']}", flush=True)
            checked, complete, gaps = domain_counts(report["rows"])
            report["result"] = "DOMAIN_ALL_VERIFIED" if gaps == 0 and checked == 33 else "DOMAIN_GAPS_FOUND"
            print(f"PHASE170_R3R10_DOMAIN_CHECKED={checked}", flush=True)
            print(f"PHASE170_R3R10_DOMAIN_COMPLETE={complete}", flush=True)
            print(f"PHASE170_R3R10_DOMAIN_GAPS={gaps}", flush=True)
            return_code = 0 if report["result"] == "DOMAIN_ALL_VERIFIED" else 1
    except Exception as exc:
        report["result"] = "REFUSED_OR_ERROR"
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["traceback"] = traceback.format_exc()[-3500:]
        print(f"PHASE170_R3R10_REFUSED={report['error']}", flush=True)
    finally:
        if before is not None:
            try:
                after = preflight(root, check_remote=False)
                report["tracked_unchanged"] = after == before
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = f"{type(exc).__name__}: {exc}"
            if not report["tracked_unchanged"]:
                report["result"] = "TRACKED_STATE_CHANGED"
                return_code = 2
        else:
            report["tracked_unchanged"] = None
        write_report(output / "audit.json", report)
        print(f"PHASE170_R3R10_TRACKED_UNCHANGED={report['tracked_unchanged']}", flush=True)
        print(f"PHASE170_R3R10_REPORT={output / 'audit.json'}", flush=True)
        print(f"PHASE170_R3R10_RESULT={report['result']}", flush=True)
    return return_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=240)
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("timeout must be a positive integer")
    return run(args.root.resolve(), dry_run=args.dry_run,
               timeout_seconds=args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
