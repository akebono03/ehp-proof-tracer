"""Audit typed Toda (5.2)/(5.6) prerequisites without deriving group results.

All stored database values are presentation candidates, not certified proofs.
This audit never modifies production code, databases or proof records.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

BRANCH = "develop"
REVIEWED_HEAD = "8be7b92a12bb3a58119d13491db5dbcffd71eb91"
REVIEWED_BLOBS = {
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r52_r9_shared_math.py": "3e4c5f9c62b04d618f845b0f82d1cb1cacccdf2e",
    "phase168_r2_toda52_transport.py": "f417cf7b828c898f7e957defd3b47056016cb585",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase173_r4_r1_source_bound_56/rule.py": "e9921f6ae5c575e86ec4b7647133382ec613fb5f",
    "phase173_r4_r1_public_connection/route.py": "fa79655aa24a88d5e7dd46d8c7a00ae04aeb15d4",
}
WEB_SENTINEL = "__PHASE173_R1_WORKER__="
SOURCE_COORDINATES = ((7, 0), (7, 1), (7, 2), (7, 3))


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if completed.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + completed.stderr.strip()[:700])
    return completed.stdout.strip()


def preflight(root: Path, *, remote: bool) -> dict:
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("not the repository root")
    if branch != BRANCH or head != REVIEWED_HEAD:
        raise RuntimeError(f"unreviewed branch/HEAD: {branch} {head}; expected {BRANCH} {REVIEWED_HEAD}")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked changes require review")
    for path, blob in REVIEWED_BLOBS.items():
        if not (root / path).is_file() or git(root, "rev-parse", "HEAD:" + path) != blob:
            raise RuntimeError("reviewed source blob mismatch: " + path)
    if remote:
        line = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        if not line or line.split()[0] != REVIEWED_HEAD:
            raise RuntimeError("remote develop differs from reviewed HEAD")
    return {"branch": branch, "head": head, "source_guard": "PASS", "remote_checked": remote}


def abstract_signature(statement: object) -> tuple[str, ...] | None:
    """Compare only abstract group structures; never certify generator images."""
    kind = type(statement).__name__
    if kind == "TodaPrimaryGroupZeroStatement":
        return ()
    if kind == "Relation":
        return abstract_signature(statement.rhs)
    if kind == "FreeCyclicGroup":
        return ("Z",)
    if kind == "FiniteCyclicGroup":
        order = getattr(statement, "order", None)
        return (f"Z/{order}",) if type(order) is int and order >= 2 else None
    if kind == "DirectSumGroup":
        summands = getattr(statement, "summands", None)
        if not isinstance(summands, tuple):
            return None
        result: list[str] = []
        for item in summands:
            signature = abstract_signature(item)
            if signature is None:
                return None
            result.extend(signature)
        return tuple(sorted(result))
    return None


def analyze_groups() -> dict:
    from phase168_r2_toda52_transport import _toda52_group_presentation_matches
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, precedes_db_goal,
    )
    from phase173_r4_r1_source_bound_56.rule import _target_generators

    n3_rows: list[dict] = []
    for i in (7, 8, 9, 10):
        source3 = exact_prior_database_result(3, i - 3)
        source2 = exact_prior_database_result(2, i - 2)
        forward_match = (
            _toda52_group_presentation_matches(source3, source2)
            if source3 is not None and source2 is not None else False
        )
        n3_rows.append({
            "group": f"pi_{i}^3", "n": 3, "k": i - 3,
            "pi_i_2_db_exists": source2 is not None,
            "pi_i_3_db_exists": source3 is not None,
            "toda52_forward_presentation_match": forward_match,
            "n2_prior_allowed_for_n3": precedes_db_goal(2, i - 2, 3, i - 3),
            "n3_prior_allowed_for_n2": precedes_db_goal(3, i - 3, 2, i - 2),
            "admitted_n2_to_n3": bool(source2 is not None and source3 is not None and
                                      admitted_db_step(source2, proof_target=source3) is not None),
            "warning": "A group isomorphism or DB value does not prove an inverse generator image.",
        })

    n4_rows: list[dict] = []
    for i in (7, 8, 9, 10):
        target = exact_prior_database_result(4, i - 4)
        first = exact_prior_database_result(3, i - 4)
        second = exact_prior_database_result(7, i - 7)
        target_shape = abstract_signature(target) if target is not None else None
        first_shape = abstract_signature(first) if first is not None else None
        second_shape = abstract_signature(second) if second is not None else None
        combine = (tuple(sorted(first_shape + second_shape))
                   if first_shape is not None and second_shape is not None else None)
        n4_rows.append({
            "group": f"pi_{i}^4", "n": 4, "k": i - 4,
            "first_input": f"pi_{i-1}^3", "second_input": f"pi_{i}^7",
            "target_db_exists": target is not None,
            "first_input_db_exists": first is not None,
            "second_input_db_exists": second is not None,
            "target_abstract_structure": target_shape,
            "sum_abstract_structure": combine,
            "abstract_structure_compatible": target_shape is not None and combine == target_shape,
            "first_input_admitted_db_prior": bool(
                first is not None and target is not None
                and admitted_db_step(first, proof_target=target) is not None
            ),
            "second_input_admitted_db_prior": bool(
                second is not None and target is not None
                and admitted_db_step(second, proof_target=target) is not None
            ),
            "existing_pi74_root_shape": bool(target is not None and _target_generators(target) is not None),
            "target_presentation": str(target)[:900],
            "first_presentation": str(first)[:900],
            "second_presentation": str(second)[:900],
            "generator_image_verified": False,
            "warning": "Compatibility and DB eligibility alone do not establish Proposition 4.4 map images.",
        })
    return {"n3_inverse_toda52": n3_rows, "n4_toda56": n4_rows}


def source_worker(root: Path, n: int, k: int, timeout: int, output: Path) -> dict:
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    cmd = [sys.executable, "-B", "-m", "phase173_r1_nge3_audit.audit",
           "--worker", "--n", str(n), "--k", str(k)]
    try:
        completed = subprocess.run(
            cmd, cwd=root, env=env, capture_output=True, check=False,
            text=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
        raw = completed.stdout + "\n" + completed.stderr
        (output / f"n_{n:03d}_k_{k:03d}.log").write_text(raw, encoding="utf-8")
        matches = [line[len(WEB_SENTINEL):] for line in completed.stdout.splitlines()
                   if line.startswith(WEB_SENTINEL)]
        if completed.returncode or len(matches) != 1:
            return {"n": n, "k": k, "status": "WORKER_ERROR", "code": completed.returncode}
        row = json.loads(matches[0])
        if not isinstance(row, dict) or row.get("n") != n or row.get("k") != k:
            return {"n": n, "k": k, "status": "WRONG_GROUP"}
        return {"n": n, "k": k, "status": row.get("search_status"),
                "web": row.get("web_key"), "open_goals": row.get("open_goals"),
                "steps": row.get("proven_steps"), "diagnostics": row.get("diagnostics", []),
                "given_references": row.get("given_references", []),
                "error": row.get("exception") or row.get("web_error")}
    except subprocess.TimeoutExpired:
        return {"n": n, "k": k, "status": "TIMEOUT"}
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        return {"n": n, "k": k, "status": "WORKER_ERROR", "error": str(exc)[:800]}


def write_report(output: Path, report: dict) -> None:
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = ["# Phase 173 R4-R3 — prerequisite frontier", "",
             "Group structure compatibility is NOT a verified derivation.", "",
             "| Target | Abstract compatible | Source 1 DB | Source 2 DB | Old root |",
             "|---|---|---|---|---|"]
    for row in report.get("matrix", {}).get("n4_toda56", []):
        lines.append(
            f"| {row['group']} | {row['abstract_structure_compatible']} | "
            f"{row['first_input_db_exists']} | {row['second_input_db_exists']} | "
            f"{row['existing_pi74_root_shape']} |"
        )
    lines.extend(["", "See audit.json for exact typed presentations and source observations.", ""])
    (output / "audit.md").write_text("\n".join(lines), encoding="utf-8")


def run(root: Path, *, dry_run: bool, timeout: int, remote: bool) -> int:
    base = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    output = base / ("phase173_r4_r3_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    report: dict = {"phase": "173 R4-R3", "mode": "AUDIT_ONLY", "reviewed_head": REVIEWED_HEAD,
                    "dry_run": dry_run, "full_pytest": False, "production_modified": False,
                    "result": "NOT_STARTED", "output": str(output)}
    rc = 2
    before = None
    print("PHASE173_R4_R3_OUTPUT=" + str(output), flush=True)
    try:
        before = preflight(root, remote=remote)
        report["preflight"] = before
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
            rc = 0
        else:
            report["matrix"] = analyze_groups()
            report["source_workers"] = []
            for n, k in SOURCE_COORDINATES:
                observed = source_worker(root, n, k, timeout, output)
                report["source_workers"].append(observed)
                print(f"PHASE173_R4_R3_SOURCE_n={n}_k={k} "
                      f"SEARCH={observed['status']} OPEN={observed.get('open_goals')}", flush=True)
            errors = {"WORKER_ERROR", "WRONG_GROUP", "TIMEOUT"}
            rc = 2 if any(row["status"] in errors or row.get("error")
                          for row in report["source_workers"]) else 0
            report["result"] = "SOURCE_WORKER_ERROR" if rc else "OBSERVATION_COMPLETE"
            for row in report["matrix"]["n4_toda56"]:
                print(f"PHASE173_R4_R3_{row['group']} ABSTRACT_MATCH="
                      f"{row['abstract_structure_compatible']} "
                      f"SOURCE_DB={row['first_input_db_exists']},{row['second_input_db_exists']} "
                      f"OLD_ROOT={row['existing_pi74_root_shape']}", flush=True)
            for row in report["matrix"]["n3_inverse_toda52"]:
                print(f"PHASE173_R4_R3_{row['group']} TODA52_FORWARD_MATCH="
                      f"{row['toda52_forward_presentation_match']} "
                      f"N2_PRIOR_ALLOWED={row['n2_prior_allowed_for_n3']}", flush=True)
    except Exception as exc:
        report["result"] = "REFUSED_OR_ERROR"
        report["error"] = f"{type(exc).__name__}: {exc}"
        print("PHASE173_R4_R3_ERROR=" + report["error"], flush=True)
        rc = 2
    finally:
        if before is not None:
            try:
                after = preflight(root, remote=False)
                report["tracked_unchanged"] = (
                    {k: v for k, v in before.items() if k != "remote_checked"}
                    == {k: v for k, v in after.items() if k != "remote_checked"}
                )
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = str(exc)[:800]
            if not report["tracked_unchanged"]:
                rc = 2
                report["result"] = "TRACKED_STATE_CHANGED"
        else:
            report["tracked_unchanged"] = None
        write_report(output, report)
        print("PHASE173_R4_R3_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE173_R4_R3_RESULT=" + report["result"], flush=True)
        print("PHASE173_R4_R3_REPORT=" + str(output / "audit.json"), flush=True)
    return rc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--skip-remote-check", action="store_true")
    options = parser.parse_args()
    if options.timeout <= 0:
        parser.error("timeout must be positive")
    return run(options.root.resolve(), dry_run=options.dry_run,
               timeout=options.timeout, remote=not options.skip_remote_check)


if __name__ == "__main__":
    raise SystemExit(main())
