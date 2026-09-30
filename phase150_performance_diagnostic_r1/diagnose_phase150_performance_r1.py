from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / "phase150_performance_diagnostic"
OUT.mkdir(exist_ok=True)

COLLECT = OUT / "collected_tests.txt"
WINDOW = OUT / "window_nodeids.txt"
RESULT = OUT / "window_timing.txt"
REPORT = OUT / "REPORT.txt"

PROGRESS_FRACTION = 0.32
WINDOW_RADIUS = 120


def run_collect() -> list[str]:
    cmd = [sys.executable, "-m", "pytest", "tests", "--collect-only", "-q"]
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    COLLECT.write_text(proc.stdout, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit(
            f"pytest collection failed with exit code {proc.returncode}. "
            f"See {COLLECT}."
        )

    nodeids = []
    for line in proc.stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith("tests/") and "::" in stripped:
            nodeids.append(stripped)

    if not nodeids:
        raise SystemExit(
            "No pytest node IDs were parsed from collection output. "
            f"See {COLLECT}."
        )
    return nodeids


def main() -> int:
    nodeids = run_collect()
    total = len(nodeids)
    center = min(total - 1, max(0, int(total * PROGRESS_FRACTION)))
    start = max(0, center - WINDOW_RADIUS)
    stop = min(total, center + WINDOW_RADIUS + 1)
    selected = nodeids[start:stop]

    WINDOW.write_text("\n".join(selected) + "\n", encoding="utf-8")

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        *selected,
        "-vv",
        "--durations=50",
        "--durations-min=0.0",
    ]

    started = time.perf_counter()
    with RESULT.open("w", encoding="utf-8") as fh:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=fh,
            stderr=subprocess.STDOUT,
        )
    elapsed = time.perf_counter() - started

    report = f"""Phase 150 Performance Diagnostic R1
===================================

Production changes: none
Existing test changes: none
Documentation changes: none
Full regression: NOT run

Collected tests: {total}
Observed interrupted progress: 32%
Approximate center index: {center}
Measured window: [{start}, {stop})
Measured node IDs: {len(selected)}
Window elapsed seconds: {elapsed:.2f}
Focused pytest exit code: {proc.returncode}

Files:
- {COLLECT}
- {WINDOW}
- {RESULT}

Interpretation:
This diagnostic maps the interrupted 32% point to pytest collection order,
then executes only a bounded window around that point with verbose node IDs
and pytest duration reporting. It does not alter production behavior and
does not replace the final Phase 150 full regression.
"""
    REPORT.write_text(report, encoding="utf-8")
    print(report)
    print("Last selected node IDs:")
    for nodeid in selected[-10:]:
        print(f"  {nodeid}")
    print()
    print(f"Timing output: {RESULT}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
