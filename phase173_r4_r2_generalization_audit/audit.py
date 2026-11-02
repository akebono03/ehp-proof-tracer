"""Read-only frontier audit for Toda (5.2)/(5.6), using the existing R1 worker.

Do not treat a database presentation or a successful static match as a proof.
The exact Git commit and reviewed blobs must match before public searches run.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

BRANCH = "develop"
REVIEWED_HEAD = "e4162e013365970877658021ff3e31503d585fa2"
REVIEWED_BLOBS = {
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r52_r9_shared_math.py": "3e4c5f9c62b04d618f845b0f82d1cb1cacccdf2e",
    "phase168_r2_toda52_transport.py": "f417cf7b828c898f7e957defd3b47056016cb585",
    "phase173_r4_r1_public_connection/route.py": "fa79655aa24a88d5e7dd46d8c7a00ae04aeb15d4",
    "phase173_r4_r1_source_bound_56/rule.py": "e9921f6ae5c575e86ec4b7647133382ec613fb5f",
    "phase173_r1_nge3_audit/audit.py": "7b4e1e3b6b759706f50b392fc2d622017ee3e725",
}
FRONTIER = ((3, 4), (3, 5), (3, 6), (3, 7), (4, 3), (4, 4), (4, 5))
SENTINEL = "__PHASE173_R1_WORKER__="


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError(
            "git " + " ".join(arguments) + ": " + result.stderr.strip()[:800]
        )
    return result.stdout.strip()


def registered_pairs(csv_path: Path) -> tuple[tuple[int, int], ...]:
    result: set[tuple[int, int]] = set()
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if not {"n", "k", "id"}.issubset(reader.fieldnames or []):
            raise ValueError("sphere.csv lacks n, k, id")
        for line_number, row in enumerate(reader, 2):
            n_text = (row.get("n") or "").strip()
            if not n_text:
                continue
            if not n_text.isdecimal():
                raise ValueError(f"malformed group coordinates at row {line_number}")
            n = int(n_text)
            if n < 3:
                continue
            k_text = (row.get("k") or "").strip()
            if not k_text.isdecimal():
                raise ValueError(f"malformed group coordinates at row {line_number}")
            result.add((n, int(k_text)))
    return tuple(sorted(result))


def select_targets(registered: tuple[tuple[int, int], ...], scope: str) -> tuple[tuple[int, int], ...]:
    present = set(registered)
    if not set(FRONTIER).issubset(present):
        raise RuntimeError("reviewed frontier group is missing from sphere.csv")
    if scope == "frontier":
        return FRONTIER
    if scope == "n3-all":
        expected = {(3, k) for k in range(4, 34)}
        if not expected.issubset(present):
            raise RuntimeError("reviewed n=3, k=4..33 registration differs")
        return tuple((3, k) for k in range(4, 34)) + ((4, 3), (4, 4), (4, 5))
    raise ValueError(f"unknown scope: {scope}")


def inspect_static(root: Path) -> dict[str, object]:
    shared = (root / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8")
    transport = (root / "phase168_r2_toda52_transport.py").read_text(encoding="utf-8")
    rule = (root / "phase173_r4_r1_source_bound_56/rule.py").read_text(encoding="utf-8")
    route = (root / "phase173_r4_r1_public_connection/route.py").read_text(encoding="utf-8")
    required = (
        ("public pi74 hook", "if n == 4 and k == 3 and expansion_provider is None:", shared),
        ("Toda52 n2 guard", "if n != 2 or dimension < 6:", transport),
        ("Toda52 source n3", "source_n, source_k = 3, dimension - 3", transport),
        ("Toda56 pi74 generator guard", "and goal.lhs == TodaPrimaryGroup(7, 4)", rule),
        ("Toda56 pi63 prior", "bridge, source_n=3, source_k=3, citing_assertion_id=citing_id", rule),
        ("pi74 route", "registered_group_goal_candidates(bridge, n=4, k=3)", route),
    )
    for label, needle, haystack in required:
        if needle not in haystack:
            raise RuntimeError("reviewed static condition has changed: " + label)
    return {
        "toda52_current_proposal_direction": "n=3 to n=2 only (not an inverse public route)",
        "toda56_source_bound_root": "pi_7^4 only",
        "toda56_public_connection": "(n,k)=(4,3) only",
        "warning": "These are source-level observations, not sufficient explanations of all runtime failures.",
    }


def preflight(root: Path, *, check_remote: bool) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("root is not the Git repository root")
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if branch != BRANCH or head != REVIEWED_HEAD:
        raise RuntimeError(
            f"unreviewed checkout: branch={branch}, HEAD={head}; "
            f"expected {BRANCH} {REVIEWED_HEAD}"
        )
    status = git(root, "status", "--porcelain", "--untracked-files=no")
    if status:
        raise RuntimeError("tracked/staged changes require review: " + status[:800])
    for file, blob in REVIEWED_BLOBS.items():
        if not (root / file).is_file():
            raise RuntimeError("missing reviewed file: " + file)
        if git(root, "rev-parse", "HEAD:" + file) != blob:
            raise RuntimeError("reviewed Git blob changed: " + file)
    if check_remote:
        remote = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        if not remote or remote.split()[0] != REVIEWED_HEAD:
            raise RuntimeError("origin/develop differs from the reviewed HEAD")
    return {"branch": branch, "head": head, "tracked_clean": True,
            "remote_verified": check_remote, "reviewed_blobs": dict(REVIEWED_BLOBS)}


def parse_worker_output(output: str, exit_code: int, n: int, k: int) -> dict[str, object]:
    markers = [line[len(SENTINEL):] for line in output.splitlines() if line.startswith(SENTINEL)]
    if exit_code != 0 or len(markers) != 1:
        return {"n": n, "k": k, "observation": "WORKER_ERROR",
                "exit_code": exit_code, "marker_count": len(markers)}
    try:
        row = json.loads(markers[0])
    except json.JSONDecodeError:
        return {"n": n, "k": k, "observation": "INVALID_JSON"}
    if not isinstance(row, dict) or row.get("n") != n or row.get("k") != k:
        return {"n": n, "k": k, "observation": "WRONG_GROUP"}
    complete = (
        row.get("db_goal_typed") is True
        and row.get("search_status") == "complete"
        and row.get("search_complete") is True
        and row.get("root_matches_db_goal") is True
        and type(row.get("open_goals")) is int
        and row["open_goals"] == 0
        and type(row.get("proven_steps")) is int
        and row["proven_steps"] > 0
        and row.get("citation_model_verified") is True
        and type(row.get("citation_count")) is int
        and row["citation_count"] > 0
        and row.get("web_key") == "generic-complete-proof"
        and row.get("web_partial") is False
        and type(row.get("web_steps")) is int
        and row["web_steps"] > 0
        and type(row.get("web_lines")) is int
        and row["web_lines"] > 0
        and row.get("web_error") is None
        and not row.get("exception")
    )
    row["observation"] = (
        "COMPLETE_AND_WEB_VERIFIED" if complete else
        "WORKER_EXCEPTION" if row.get("exception") else "NOT_VERIFIED"
    )
    return row


def run_worker(root: Path, n: int, k: int, timeout: int, output_dir: Path) -> dict[str, object]:
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    log_path = output_dir / f"n_{n:03d}_k_{k:03d}.log"
    try:
        result = subprocess.run(
            [sys.executable, "-B", "-m", "phase173_r1_nge3_audit.audit",
             "--worker", "--n", str(n), "--k", str(k)],
            cwd=root, env=env, capture_output=True,
            text=True, encoding="utf-8", errors="replace", check=False,
            timeout=timeout,
        )
        combined = result.stdout + ("\n" + result.stderr if result.stderr else "")
        log_path.write_text(combined, encoding="utf-8")
        return parse_worker_output(result.stdout, result.returncode, n, k)
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or b""
        value = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else str(stdout)
        log_path.write_text(value, encoding="utf-8")
        return {"n": n, "k": k, "observation": "TIMEOUT", "timeout_seconds": timeout}


def write_report(directory: Path, report: dict[str, object]) -> None:
    temp = directory / "audit.json.tmp"
    temp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, directory / "audit.json")
    lines = [
        "# Phase 173 R4-R2 — 一般化不足の読み取り専用監査", "",
        "Toda (5.2) / (5.6) の既存公開経路と個別群の探索結果を照合する。", "",
        "- Production code: 変更なし",
        "- Full pytest: 未実施",
        "- 対象 HEAD: `" + REVIEWED_HEAD + "`",
        "- Scope: `" + str(report["scope"]) + "`", "",
        "| 群 | Search | Open Goals | Web | 判定 |",
        "|---|---|---:|---|---|",
    ]
    for row in report["rows"]:
        n, k = row["n"], row["k"]
        lines.append(
            f"| $\\pi_{{{n+k}}}^{{{n}}}$ | {row.get('search_status', '-')} | "
            f"{row.get('open_goals', '-')} | {row.get('web_key', '-')} | "
            f"{row['observation']} |"
        )
    lines.extend(["", "詳細な open_goal_text, diagnostics, references は audit.json と worker log を確認。",
                  "SOURCE_SCOPE_GAP はこの HEAD に限定した静的な観察であり、失敗原因の証明ではない。", ""])
    (directory / "audit.md").write_text("\n".join(lines), encoding="utf-8")


def run(root: Path, *, dry_run: bool, scope: str, timeout: int,
        check_remote: bool) -> int:
    recovery = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    output = recovery / ("phase173_r4_r2_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {
        "phase": "173 R4-R2", "mode": "AUDIT_ONLY", "scope": scope,
        "dry_run": dry_run, "production_modified": False, "full_pytest": False,
        "rows": [], "result": "NOT_STARTED", "reviewed_head": REVIEWED_HEAD,
    }
    code = 2
    before: dict[str, object] | None = None
    print("PHASE173_R4_R2_MODE=AUDIT_ONLY", flush=True)
    print("PHASE173_R4_R2_OUTPUT=" + str(output), flush=True)
    try:
        before = preflight(root, check_remote=check_remote)
        report["preflight"] = before
        report["static"] = inspect_static(root)
        groups = registered_pairs(root / "data/sphere.csv")
        targets = select_targets(groups, scope)
        report["selected_groups"] = [list(pair) for pair in targets]
        print("PHASE173_R4_R2_STATIC_GUARD=PASS", flush=True)
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
            code = 0
        else:
            rows: list[dict[str, object]] = []
            for n, k in targets:
                row = run_worker(root, n, k, timeout, output)
                rows.append(row)
                report["rows"] = rows
                write_report(output, report)
                print(f"PHASE173_R4_R2_n={n}_k={k} "
                      f"OBSERVATION={row['observation']} "
                      f"OPEN_GOALS={row.get('open_goals', 'unknown')}", flush=True)
            errors = {"WORKER_ERROR", "WORKER_EXCEPTION", "INVALID_JSON", "WRONG_GROUP", "TIMEOUT"}
            code = 2 if any(row["observation"] in errors for row in rows) else 0
            report["result"] = "WORKER_ERROR" if code else "OBSERVATION_COMPLETE"
            report["pi74_regression_verified"] = any(
                row["n"] == 4 and row["k"] == 3 and
                row["observation"] == "COMPLETE_AND_WEB_VERIFIED" for row in rows
            )
            if not report["pi74_regression_verified"]:
                report["result"] = "PI74_REGRESSION_NOT_VERIFIED"
                code = 2
            print("PHASE173_R4_R2_PI74_REGRESSION_VERIFIED=" +
                  str(report["pi74_regression_verified"]), flush=True)
    except Exception as exc:
        report["result"] = "REFUSED_OR_ERROR"
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["traceback"] = traceback.format_exc()[-3000:]
        print("PHASE173_R4_R2_REFUSED=" + str(report["error"]), flush=True)
    finally:
        if before is not None:
            try:
                report["tracked_unchanged"] = (
                    preflight(root, check_remote=False) ==
                    {**before, "remote_verified": False}
                )
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = f"{type(exc).__name__}: {exc}"
            if not report["tracked_unchanged"]:
                report["result"] = "TRACKED_STATE_CHANGED"
                code = 2
        else:
            report["tracked_unchanged"] = None
        write_report(output, report)
        print("PHASE173_R4_R2_REPORT=" + str(output / "audit.json"), flush=True)
        print("PHASE173_R4_R2_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE173_R4_R2_RESULT=" + str(report["result"]), flush=True)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--scope", choices=("frontier", "n3-all"), default="frontier")
    parser.add_argument("--timeout-seconds", type=int, default=240)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-remote-check", action="store_true")
    arguments = parser.parse_args()
    if arguments.timeout_seconds <= 0:
        parser.error("timeout must be positive")
    return run(arguments.root.resolve(), dry_run=arguments.dry_run,
               scope=arguments.scope, timeout=arguments.timeout_seconds,
               check_remote=not arguments.skip_remote_check)


if __name__ == "__main__":
    raise SystemExit(main())
