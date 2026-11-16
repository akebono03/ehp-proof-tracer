"""Phase 175 R3R5: source-first read-only pi7^3 EHP injectivity frontier."""
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

from phase175_r3r5_pi73_lemma57_frontier.source import verify_reviewed_toda_source

PACKAGE = "phase175_r3r5_pi73_lemma57_frontier"
MARKER = "__PHASE175_R3R5_WORKER__="


def latest_verified_r3_report() -> Path:
    """Require actual R3R4 successful normal-run evidence, never DryRun data."""
    local = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = local / "EHPProofTracerAudit" / "phase175_r3_pi73_hopf_lift"
    for path in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
            result = report.get("worker", {}).get("data", {})
            rows = result.get("subgoal_observations", [])
            statuses = {item["name"]: item["status"] for item in rows}
            if (
                report.get("phase") == "175-R3"
                and report.get("dry_run") is False
                and report.get("result") == "PASS_R3_PI73_HOPF_FRONTIER_RECORDED"
                and report.get("tracked_unchanged") is True
                and report.get("new_given") == 0
                and result.get("target_direct_given_excluded") is True
                and result.get("hopf_lift_candidate_count") == 1
                and statuses.get("hopf_injectivity") == "UNRESOLVED"
                and statuses.get("cyclic_codomain") == "INFERRED"
                and statuses.get("hopf_generator_image") == "INFERRED"
                and statuses.get("source_bound_cyclic_codomain") == "INFERRED"
            ):
                return path
        except (ValueError, OSError, TypeError, KeyError, UnicodeError):
            continue
    raise RuntimeError("R3R5_NO_VERIFIED_R3R4_NORMAL_REPORT")


def scoped_preflight(root: Path) -> dict[str, object]:
    """Reuse the exact R3R4 reviewed source, worktree, R2 lineage guards."""
    from phase175_r3_pi73_hopf_lift import audit as r3

    checked = r3.preflight(root)
    r2_path = r3.select_r2_report(None)
    previous = json.loads(r2_path.read_text(encoding="utf-8"))
    r3.validate_r2(previous)
    lineage = r3.verify_lineage(root, previous, checked)
    source = verify_reviewed_toda_source(root)
    return {
        "r3_source_guard": checked,
        "r2_lineage": lineage,
        "r2_report_path": str(r2_path),
        "toda_lemma57_source": source,
    }


def worker() -> int:
    """Run independent typed searches without inserting any theorem facts."""
    try:
        from phase175_r3r5_pi73_lemma57_frontier.frontier import inspect_ehp_injectivity_frontier
        payload = {"status": "INSPECTED", "data": inspect_ehp_injectivity_frontier()}
    except Exception as exc:
        payload = {
            "status": "WORKER_ERROR",
            "error": type(exc).__name__ + ": " + str(exc),
            "traceback": traceback.format_exc()[-6000:],
        }
    print(MARKER + json.dumps(payload, ensure_ascii=False), flush=True)
    return 0


def launch_worker(root: Path, seconds: int, folder: Path) -> dict[str, object]:
    """Bound long recursive proof search; preserve its diagnostics."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        result = subprocess.run(
            [sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker", "--root", str(root)],
            cwd=root, env=env, capture_output=True,
            text=True, encoding="utf-8", errors="replace",
            timeout=seconds, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or b""
        output = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
        (folder / "worker.log").write_text(output, encoding="utf-8")
        return {"status": "TIMEOUT", "seconds": seconds}
    (folder / "worker.log").write_text(
        result.stdout + "\nSTDERR:\n" + result.stderr, encoding="utf-8",
    )
    lines = [line[len(MARKER):] for line in result.stdout.splitlines() if line.startswith(MARKER)]
    if result.returncode or len(lines) != 1:
        return {"status": "INVALID_WORKER", "return_code": result.returncode, "markers": len(lines)}
    try:
        payload = json.loads(lines[0])
    except json.JSONDecodeError:
        return {"status": "INVALID_JSON"}
    return payload if isinstance(payload, dict) else {"status": "INVALID_PAYLOAD"}


def write_report(folder: Path, report: dict[str, object]) -> None:
    """Persist evidence outside the repository and show individual open goals."""
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    rows = [
        "# Phase 175 R3R5 — $\\pi_7^3$ / Toda Lemma 5.7 source frontier",
        "",
        "- Gate: `" + str(report.get("result")) + "`",
        "- No production changes; no new GIVEN and no complete proof imported",
        "- Full pytest: not run",
        "",
    ]
    source = report.get("preflight", {}).get("toda_lemma57_source", {})
    if isinstance(source, dict):
        rows.extend([
            "## 出典の照合", "",
            "- Toda " + str(source.get("locator")),
            "- Git blob: `" + str(source.get("source_blob")) + "`",
            "- Lemma 5.7 is earlier than Proposition 5.8",
            "- TeX source text alone is not a new GIVEN", "",
        ])
    result = report.get("worker", {}).get("data", {})
    if isinstance(result, dict):
        rows += ["## 既存規則と前提の独立探索", ""]
        for entry in result.get("obligations", []):
            rows.append("- **" + str(entry["name"]) + "**: " + str(entry["status"])
                        + " (routes=" + str(entry["offered_routes"]) + ")")
            if entry.get("diagnostic"):
                rows.append("  - " + str(entry["diagnostic"]))
            for name in entry.get("observed_unresolved", [])[:5]:
                rows.append("  - open: `" + str(name).replace("`", "'") + "`")
    if report.get("error"):
        rows += ["", "## エラー", "", "`" + str(report["error"]) + "`"]
    (folder / "report.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def run(root: Path, dry_run: bool, timeout_seconds: int) -> int:
    """Check source pins and R3 evidence before a bounded, read-only audit."""
    local = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = local / "EHPProofTracerAudit" / PACKAGE / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    )
    folder.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {
        "phase": "175-R3R5", "mode": "READ_ONLY_LEMMA57_SOURCE_FRONTIER",
        "dry_run": dry_run, "new_given": 0,
        "new_math_rules": 0, "production_changes": [], "full_pytest_executed": False,
        "result": "NOT_STARTED",
    }
    checked = None
    code = 2
    print("PHASE175_R3R5_OUTPUT=" + str(folder), flush=True)
    try:
        checked = scoped_preflight(root)
        report["preflight"] = checked
        prior = latest_verified_r3_report()
        report["r3r4_report"] = str(prior)
        print("PHASE175_R3R5_SOURCE_GUARD=PASS", flush=True)
        print("PHASE175_R3R5_LEMMA57_SOURCE=PASS", flush=True)
        print("PHASE175_R3R5_R3R4_EVIDENCE=PASS", flush=True)
        if dry_run:
            report["result"] = "PASS_R3R5_READ_ONLY_DRYRUN"
            code = 0
        else:
            outcome = launch_worker(root, timeout_seconds, folder)
            report["worker"] = outcome
            if outcome.get("status") != "INSPECTED":
                raise RuntimeError("R3R5_TYPED_WORKER_FAILED: " + str(outcome))
            data = outcome.get("data", {})
            if (data.get("target_direct_given_excluded") is not True
                    or data.get("source_lemma57_new_given") is not False
                    or data.get("new_mathematical_rules") != 0
                    or data.get("production_modified") is not False
                    or data.get("hopf_lift_proposals") != 1
                    or data.get("zero_image_generic_bridge_candidates") != 1):
                raise RuntimeError("R3R5_UNSUPPORTED_TYPED_RESULT")
            statuses = {row["name"]: row["status"] for row in data["obligations"]}
            expected = {
                "ehp_exactness", "lower_pi62_group", "zero_generator_image",
                "zero_suspension_image", "hopf_injectivity",
            }
            if set(statuses) != expected:
                raise RuntimeError("R3R5_MISSING_OBLIGATION_OBSERVATION")
            for name in (
                "ehp_exactness", "lower_pi62_group", "zero_generator_image",
                "zero_suspension_image", "hopf_injectivity",
            ):
                print("PHASE175_R3R5_" + name.upper() + "=" + statuses[name], flush=True)
            print("PHASE175_R3R5_PUBLIC_PROVIDER_MODIFIED=False", flush=True)
            report["result"] = "PASS_R3R5_LEMMA57_FRONTIER_RECORDED"
            code = 0
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-5000:]
        report["result"] = "R3R5_REFUSED_OR_WORKER_ERROR"
        print("PHASE175_R3R5_ERROR=" + report["error"], flush=True)
    finally:
        if checked is not None:
            try:
                report["tracked_unchanged"] = scoped_preflight(root) == checked
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = str(exc)
            if report["tracked_unchanged"] is not True:
                report["result"] = "R3R5_TRACKED_STATE_CHANGED"
                code = 2
        else:
            report["tracked_unchanged"] = None
        write_report(folder, report)
        print("PHASE175_R3R5_REPORT=" + str(folder / "report.json"), flush=True)
        print("PHASE175_R3R5_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE175_R3R5_GATE=" + str(report["result"]), flush=True)
        print("(END)", flush=True)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("positive timeout required")
    if args.worker:
        return worker()
    return run(args.root.resolve(), args.dry_run, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
