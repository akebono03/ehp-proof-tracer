"""Phase 166 closure: run full pytest, save auditable results, do not edit production."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path


def run_command(args: list[str], cwd: Path) -> dict[str, object]:
    try:
        result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, errors="replace", check=False)
        return {"command": args, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    except OSError as error:
        return {"command": args, "exit_code": None, "stdout": "", "stderr": str(error)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    options = parser.parse_args()
    repo = options.repo.resolve()
    if not (repo / "phase165_r55_nk_only_goal.py").is_file():
        print("ERROR: repository root not found", file=sys.stderr)
        return 2
    output = Path(__file__).resolve().parent / "results" / dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output.mkdir(parents=True, exist_ok=True)
    pre = run_command(["git", "status", "--short", "--branch"], repo)
    head = run_command(["git", "rev-parse", "HEAD"], repo)
    (output / "git_before.txt").write_text(str(pre["stdout"]) + str(pre["stderr"]), encoding="utf-8")
    # Keep cache and bytecode outside the existing project where possible.
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"]
    log = output / "pytest_full.log"
    print("Full suite: " + " ".join(command), flush=True)
    with log.open("w", encoding="utf-8", errors="replace") as stream:
        try:
            proc = subprocess.Popen(command, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace", env=env, bufsize=1)
            assert proc.stdout is not None
            for line in proc.stdout:
                stream.write(line)
                stream.flush()
                print(line, end="", flush=True)
            exit_code = proc.wait()
        except OSError as error:
            exit_code = 127
            stream.write(str(error) + "\n")
    post = run_command(["git", "status", "--short", "--branch"], repo)
    (output / "git_after.txt").write_text(str(post["stdout"]) + str(post["stderr"]), encoding="utf-8")
    summary = {
        "phase": "166 closure full pytest",
        "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "repository": str(repo),
        "git_head": str(head["stdout"]).strip(),
        "pytest_command": command,
        "pytest_exit_code": exit_code,
        "phase166_status": "PASS_CANDIDATE" if exit_code == 0 else "BLOCKED_BY_TEST_FAILURES",
        "note": "PASS_CANDIDATE requires review of complete report before closing the phase.",
        "production_code_modified_by_runner": False,
        "full_pytest_run": True,
        "output_dir": str(output),
    }
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\nCLOSURE_REPORT=" + str(output / "summary.json"), flush=True)
    print("FULL_PYTEST_EXIT=" + str(exit_code), flush=True)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
