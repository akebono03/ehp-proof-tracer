"""Run the Phase 166 closure suite without collecting a known installer script."""
from __future__ import annotations
import argparse
import datetime
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
    excluded = Path("phase165_r6_8_eta_name_fix/install_and_test.py")
    target = repo / excluded
    if not target.is_file():
        raise SystemExit(f"Missing known installer: {target}")
    run_dir = Path(__file__).resolve().parent / "results" / datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--ignore=" + excluded.as_posix()]
    report = {
        "phase": "166 closure collection guard",
        "excluded_from_collection": [excluded.as_posix()],
        "reason": "Installer performs filesystem writes and raises SystemExit when imported; not a test module.",
        "production_files_modified": False,
        "full_test_suite_with_one_installer_excluded": True,
        "command": cmd,
        "pytest_exit_code": None,
    }
    for label, command in [
        ("git_before", ["git", "status", "--short"]),
        ("git_revision", ["git", "rev-parse", "HEAD"]),
    ]:
        try:
            p = subprocess.run(command, cwd=repo, capture_output=True, text=True, errors="replace", timeout=20)
            (run_dir / (label + ".txt")).write_text(p.stdout + p.stderr, encoding="utf-8")
        except (OSError, subprocess.TimeoutExpired) as e:
            (run_dir / (label + ".txt")).write_text(repr(e), encoding="utf-8")
    log_path = run_dir / "pytest_full.log"
    print("COMMAND:", " ".join(cmd), flush=True)
    print("LOG:", log_path, flush=True)
    try:
        with log_path.open("w", encoding="utf-8") as logfile:
            proc = subprocess.Popen(cmd, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", env={**os.environ, "PYTHONPATH":str(repo)+os.pathsep+os.environ.get("PYTHONPATH","")})
            assert proc.stdout is not None
            for line in proc.stdout:
                print(line, end="", flush=True)
                logfile.write(line)
            report["pytest_exit_code"] = proc.wait()
    except OSError as exc:
        report["launch_error"] = repr(exc)
        report["pytest_exit_code"] = 127
    report["closure_status"] = "PASS" if report["pytest_exit_code"] == 0 else "BLOCKED"
    try:
        proc = subprocess.run(["git", "status", "--short"], cwd=repo, capture_output=True, text=True, errors="replace", timeout=20)
        (run_dir / "git_after.txt").write_text(proc.stdout + proc.stderr, encoding="utf-8")
    except (OSError, subprocess.TimeoutExpired) as e:
        (run_dir / "git_after.txt").write_text(repr(e), encoding="utf-8")
    (run_dir / "summary.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("CLOSURE_REPORT=" + str(run_dir / "summary.json"), flush=True)
    print("STATUS=" + report["closure_status"], flush=True)
    return int(report["pytest_exit_code"])

if __name__ == "__main__":
    raise SystemExit(main())
