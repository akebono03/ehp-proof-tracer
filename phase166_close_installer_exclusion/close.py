"""Phase 166 closing suite: exclude installer entrypoints from pytest collection."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    candidates = sorted(repo.rglob("install_and_test.py"))
    excluded = [str(p.relative_to(repo)).replace("\\", "/") for p in candidates]
    run_dir = Path(__file__).resolve().parent / "results" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--ignore-glob=*install_and_test.py"]
    report = {
        "phase": "166 closure", "excluded_filename_pattern": "*install_and_test.py",
        "matched_installer_paths": excluded,
        "command": command, "pytest_exit_code": None,
        "production_code_modified_by_runner": False,
        "result": "NOT_RUN",
    }
    for label, cmd in (("git_before", ["git", "status", "--short"]), ("git_revision", ["git", "rev-parse", "HEAD"])):
        try:
            proc = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, errors="replace", timeout=30)
            (run_dir / (label + ".txt")).write_text(proc.stdout + proc.stderr, encoding="utf-8")
        except (OSError, subprocess.TimeoutExpired) as exc:
            (run_dir / (label + ".txt")).write_text(repr(exc), encoding="utf-8")
    print("Excluded installer files:", len(excluded), flush=True)
    for path in excluded:
        print("  ", path, flush=True)
    print("COMMAND:", " ".join(command), flush=True)
    print("LOG:", run_dir / "pytest_full.log", flush=True)
    try:
        with (run_dir / "pytest_full.log").open("w", encoding="utf-8") as output:
            proc = subprocess.Popen(
                command, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
                env={**os.environ, "PYTHONPATH": str(repo) + os.pathsep + os.environ.get("PYTHONPATH", "")},
            )
            assert proc.stdout is not None
            for line in proc.stdout:
                output.write(line)
                print(line, end="", flush=True)
            report["pytest_exit_code"] = proc.wait()
    except OSError as exc:
        report["launch_error"] = repr(exc)
        report["pytest_exit_code"] = 127
    report["result"] = "PASS" if report["pytest_exit_code"] == 0 else "BLOCKED"
    try:
        proc = subprocess.run(["git", "status", "--short"], cwd=repo, capture_output=True, text=True, errors="replace", timeout=30)
        (run_dir / "git_after.txt").write_text(proc.stdout + proc.stderr, encoding="utf-8")
    except (OSError, subprocess.TimeoutExpired) as exc:
        (run_dir / "git_after.txt").write_text(repr(exc), encoding="utf-8")
    (run_dir / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("CLOSURE_REPORT=" + str(run_dir / "summary.json"), flush=True)
    print("STATUS=" + report["result"], flush=True)
    return int(report["pytest_exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
