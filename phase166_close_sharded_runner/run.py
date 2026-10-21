"""Phase 166 closure: rerun previously recorded tracked test manifest in safe-size shards."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys


def partition_paths(paths: list[str], batch_size: int) -> list[list[str]]:
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    return [paths[i:i + batch_size] for i in range(0, len(paths), batch_size)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=12)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    package = Path(__file__).resolve().parent
    frozen = package / "previous_manifest.json"
    data = json.loads(frozen.read_text(encoding="utf-8"))
    tests = data["included"]
    if not isinstance(tests, list) or len(tests) != 1410 or len(set(tests)) != len(tests):
        raise SystemExit("Expected 1410 distinct test files in the prior manifest")
    missing = [p for p in tests if not (repo / p).is_file()]
    if missing:
        raise SystemExit("Manifest files missing: " + repr(missing[:10]))
    batches = partition_paths(tests, args.batch_size)
    out = package / "results" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out.mkdir(parents=True, exist_ok=True)
    summary = {
        "phase": "166 closure",
        "mode": "sharded_previously_selected_manifest",
        "manifest_file_count": len(tests),
        "manifest_excluded_count": len(data["excluded"]),
        "batches_total": len(batches),
        "batches_completed": 0,
        "pytest_run_completed": False,
        "status": "DRY_RUN" if args.dry_run else "RUNNING",
        "batch_results": [],
        "scope_review_required": True,
    }
    (out / "source_manifest.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "git_before.txt").write_text(subprocess.run(["git", "status", "--short"], cwd=repo, capture_output=True, text=True, errors="replace").stdout, encoding="utf-8")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(repo) + os.pathsep + env.get("PYTHONPATH", "")
    result_code = 0
    for index, batch in enumerate(batches, 1):
        cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--maxfail=1", *batch]
        cmd_chars = sum(len(v) + 3 for v in cmd)
        if cmd_chars > 5000:
            summary["status"] = "BLOCKED_COMMAND_LENGTH"
            summary["batch_results"].append({"batch": index, "command_chars": cmd_chars})
            result_code = 2
            break
        if args.dry_run:
            continue
        print(f"[BATCH {index}/{len(batches)}] {len(batch)} files", flush=True)
        log_file = out / f"pytest_{index:03d}.log"
        try:
            with log_file.open("w", encoding="utf-8") as log:
                proc = subprocess.Popen(cmd, cwd=repo, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
                assert proc.stdout is not None
                for line in proc.stdout:
                    log.write(line)
                    if "FAILED" in line or "ERROR" in line or "passed" in line or "collected" in line or "INTERNALERROR" in line:
                        print(line.rstrip(), flush=True)
                code = proc.wait()
        except OSError as exc:
            code = 127
            log_file.write_text(repr(exc) + "\n", encoding="utf-8")
        summary["batch_results"].append({"batch": index, "files": len(batch), "exit_code": code, "log": log_file.name})
        summary["batches_completed"] = index
        (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if code != 0:
            result_code = code
            summary["status"] = "BLOCKED_TEST_FAILURE_OR_COLLECTION"
            print(f"FAILED BATCH {index}, see {log_file}", flush=True)
            break
    else:
        if not args.dry_run:
            summary["pytest_run_completed"] = True
            summary["status"] = "SHARDED_PASS_PENDING_SCOPE_REVIEW"
    (out / "git_after.txt").write_text(subprocess.run(["git", "status", "--short"], cwd=repo, capture_output=True, text=True, errors="replace").stdout, encoding="utf-8")
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("REPORT:", out / "summary.json", flush=True)
    print("STATUS:", summary["status"], flush=True)
    return result_code


if __name__ == "__main__":
    raise SystemExit(main())
