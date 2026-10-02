from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--package-dir",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_closure_output"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    package_dir = args.package_dir.resolve()

    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else repo_root
        / args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    log_path = (
        output_dir
        / "phase155_full_pytest.log"
    )
    metadata_path = (
        output_dir
        / "phase155_full_pytest_metadata.json"
    )

    env = os.environ.copy()

    existing_pythonpath = env.get(
        "PYTHONPATH",
        "",
    )

    env["PYTHONPATH"] = (
        str(package_dir)
        + (
            os.pathsep
            + existing_pythonpath
            if existing_pythonpath
            else ""
        )
    )

    command = [
        sys.executable,
        "-m",
        "pytest",
        "tests",
        "-q",
        "--tb=line",
        "--durations=50",
        "--durations-min=1.0",
        "-p",
        "phase155_closure_progress_plugin",
    ]

    print(
        "Phase 155 Closure full regression"
    )
    print(
        "THIS IS THE PHASE-FINAL FULL TEST RUN."
    )
    print(
        "pytest will continue after ordinary test failures."
    )
    print(
        "Progress is printed every 100 completed tests."
    )
    print(
        "Log:",
        log_path,
    )
    print(
        "Command:",
        " ".join(command),
    )
    print("")

    started = time.perf_counter()

    with log_path.open(
        "w",
        encoding="utf-8",
    ) as log:
        process = subprocess.Popen(
            command,
            cwd=repo_root,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )

        assert process.stdout is not None

        for line in process.stdout:
            print(
                line,
                end="",
                flush=True,
            )
            log.write(
                line
            )
            log.flush()

        returncode = process.wait()

    elapsed = (
        time.perf_counter()
        - started
    )

    metadata = {
        "command": command,
        "returncode": returncode,
        "elapsed_seconds": elapsed,
        "full_repository_pytest_executed": True,
        "log_path": str(log_path),
    }

    metadata_path.write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print("")
    print(
        "Full regression return code:",
        returncode,
    )
    print(
        "Full regression elapsed:",
        f"{elapsed:.2f}s",
    )

    if returncode != 0:
        print(
            "Phase 155 Closure full regression FAILED."
        )
        print(
            "Documentation was not updated."
        )
        print(
            "Use the saved log to repair failures; "
            "pytest did not stop at the first ordinary failure."
        )
        return returncode

    print(
        "Phase 155 Closure full regression PASSED."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
