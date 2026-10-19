"""R6 test runner: logs, controlled chunking, interrupt and restart support.

This file does not change the implementation or pytest test sources.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BATCH_SIZE = 25
BASELINES = ("pi3_2", "pi4_3")


def save_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def execute(cmd: list[str], log: Path, *, append: bool = False) -> int:
    print("RUN", " ".join(cmd[:7]), flush=True)
    with log.open("a" if append else "w", encoding="utf-8") as handle:
        handle.write(f"\n[{now()}] COMMAND: {cmd!r}\n")
        handle.flush()
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
        try:
            assert proc.stdout is not None
            for line in proc.stdout:
                handle.write(line)
                handle.flush()
                print(line, end="", flush=True)
            code = proc.wait()
            handle.write(f"[{now()}] EXIT CODE: {code}\n")
            handle.flush()
            return code
        except KeyboardInterrupt:
            # Do not mark this batch complete; the next invocation retries it.
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
            handle.write(f"[{now()}] INTERRUPTED; batch NOT marked completed\n")
            handle.flush()
            raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    os.chdir(root)
    results = root / "phase165_r6_audit_results"
    results.mkdir(parents=True, exist_ok=True)
    bundle = Path(__file__).resolve().parent
    required = [
        root / "phase165_r3_architecture_guard/tests/test_phase165_r3_architecture_guard.py",
        root / "phase165_r4_golden_baseline/tests/test_phase165_r4_golden_baseline.py",
        *(root / f"phase165_r4_golden_baseline/baselines/{name}.json" for name in BASELINES),
    ]
    for path in required:
        if not path.is_file():
            print(f"ERROR: missing prerequisite: {path}", flush=True)
            return 2
    before = {name: digest(root / f"phase165_r4_golden_baseline/baselines/{name}.json") for name in BASELINES}
    report_path = results / "audit_result.json"
    state_path = results / "resume_state.json"
    inventory_path = results / "collected_nodeids.json"
    state: dict = {"version": 2, "scope": "current-roots-v1", "batch_size": BATCH_SIZE, "batches": {}, "started_at": now()}
    report = {
        "phase": "165 R6", "status": "IN_PROGRESS", "timestamp": now(),
        "r3_exit_code": None, "r4_exit_code": None,
        "full_pytest_run": False, "full_pytest_exit_code": None,
        "baseline_hashes_before": before, "baseline_hashes_after": None,
        "baselines_unchanged": None, "browser_visual_check": "NOT_VERIFIED",
        "phase_closure": "PENDING",
    }
    try:
        for label, path in (("r3", required[0]), ("r4", required[1])):
            code = execute([sys.executable, "-m", "pytest", "-q", str(path)], results / f"{label}_pytest.log")
            report[f"{label}_exit_code"] = code
            save_json(report_path, report)
            if code != 0:
                report["status"] = f"{label.upper()}_FAILED"
                return 1
        if state_path.exists() and inventory_path.exists():
            state = json.loads(state_path.read_text(encoding="utf-8"))
            nodeids = json.loads(inventory_path.read_text(encoding="utf-8"))
            if state.get("version") != 2 or state.get("scope") != "current-roots-v1" or state.get("batch_size") != BATCH_SIZE:
                print("ERROR: incompatible resume state; do not overwrite automatically", flush=True)
                return 2
            print(f"RESUME: {len(state['batches'])} completed batches", flush=True)
        else:
            if state_path.exists() != inventory_path.exists():
                print("ERROR: incomplete inventory/state pair; manual review required", flush=True)
                return 2
            code = execute([sys.executable, str(bundle / "collect_nodeids.py"), str(root), str(inventory_path), str(results / "collection_scope.json")], results / "collection.log")
            if code != 0:
                report["status"] = "COLLECTION_FAILED"
                report["collection_scope_report"] = "collection_scope.json"
                return 1
            nodeids = json.loads(inventory_path.read_text(encoding="utf-8"))
            state["inventory_sha256"] = digest(inventory_path)
            save_json(state_path, state)
        if digest(inventory_path) != state.get("inventory_sha256"):
            print("ERROR: inventory changed; refusing to resume", flush=True)
            return 2
        batches = [nodeids[i:i + BATCH_SIZE] for i in range(0, len(nodeids), BATCH_SIZE)]
        report["full_pytest_run"] = True
        report["total_tests"] = len(nodeids)
        report["total_batches"] = len(batches)
        save_json(report_path, report)
        for index, batch in enumerate(batches, 1):
            key = str(index)
            if key in state["batches"]:
                continue
            batch_hash = hashlib.sha256("\n".join(batch).encode("utf-8")).hexdigest()
            print(f"BATCH {index}/{len(batches)} | tests {len(batch)} | completed {len(state['batches'])}/{len(batches)}", flush=True)
            code = execute([sys.executable, "-m", "pytest", "-q", *batch], results / "full_pytest.log", append=True)
            state["batches"][key] = {"exit_code": code, "test_count": len(batch), "nodeids_sha256": batch_hash, "finished_at": now()}
            save_json(state_path, state)
            report["completed_batches"] = len(state["batches"])
            report["failed_batches"] = [int(k) for k, v in state["batches"].items() if v["exit_code"] != 0]
            save_json(report_path, report)
        errors = [int(k) for k, value in state["batches"].items() if value["exit_code"] != 0]
        report["failed_batches"] = sorted(errors)
        report["full_pytest_exit_code"] = 0 if not errors else 1
        report["status"] = "AUTOMATED_PASS" if not errors else "FULL_PYTEST_FAILED"
        current_hashes = {name: digest(root / f"phase165_r4_golden_baseline/baselines/{name}.json") for name in BASELINES}
        if current_hashes != before:
            report["status"] = "BASELINE_CHANGED"
            return 1
        return 0 if not errors else 1
    except KeyboardInterrupt:
        report["status"] = "INTERRUPTED"
        print("INTERRUPTED: completed batches retained. Run the same command to resume.", flush=True)
        return 130
    except Exception as exc:
        report["status"] = "RUNNER_ERROR"
        report["error"] = repr(exc)
        print(f"RUNNER ERROR: {exc!r}", flush=True)
        return 2
    finally:
        after = {name: digest(root / f"phase165_r4_golden_baseline/baselines/{name}.json") for name in BASELINES}
        report["baseline_hashes_after"] = after
        report["baselines_unchanged"] = before == after
        if not report["baselines_unchanged"]:
            report["status"] = "BASELINE_CHANGED"
        report["timestamp"] = now()
        save_json(report_path, report)
        print(f"Report: {report_path}", flush=True)
        print(f"Status: {report['status']}; baseline unchanged: {report['baselines_unchanged']}", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
