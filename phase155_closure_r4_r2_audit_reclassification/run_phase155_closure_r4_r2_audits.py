from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path


def _env(root: Path) -> dict[str, str]:
  env = dict(os.environ)
  env["PYTEST_ADDOPTS"] = ""

  entries = [
    str(root),
    str(root / "tests"),
  ]

  if env.get("PYTHONPATH"):
    entries.append(env["PYTHONPATH"])

  env["PYTHONPATH"] = os.pathsep.join(entries)
  return env


def _collect(root: Path, output: Path) -> int:
  log = output / "r4_r2_collection.log"

  with log.open("w", encoding="utf-8") as handle:
    result = subprocess.run(
      [
        sys.executable,
        "-m",
        "pytest",
        "tests",
        "--collect-only",
        "-q",
      ],
      cwd=root,
      stdout=handle,
      stderr=subprocess.STDOUT,
      text=True,
    )

  if result.returncode != 0:
    raise SystemExit("Collection failed.")

  text = log.read_text(encoding="utf-8", errors="replace")
  matches = re.findall(r"(\d+)\s+tests collected", text)

  if not matches:
    raise SystemExit("Could not parse collection count.")

  return int(matches[-1])


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--repo-root", type=Path, default=Path.cwd())
  parser.add_argument("--output-dir", type=Path, required=True)
  parser.add_argument("--timeout", type=int, default=600)
  args = parser.parse_args()

  root = args.repo_root.resolve()
  output = args.output_dir.resolve()
  output.mkdir(parents=True, exist_ok=True)

  manifest_path = root / "tests" / "phase155_audit_only_nodeids.txt"
  nodeids = tuple(
    line.strip()
    for line in manifest_path.read_text(encoding="utf-8").splitlines()
    if line.strip()
  )

  if len(nodeids) != 2:
    raise SystemExit("Expected exactly two final audit-only nodeids.")

  collected = _collect(root, output)
  print("Current tests collected:", collected)

  if collected != 10384:
    raise SystemExit(
      "Unexpected current collection count: "
      + str(collected)
      + " (expected 10384)"
    )

  results = {}

  for index, nodeid in enumerate(nodeids, start=1):
    log_path = output / f"r4_r2_audit_{index}.log"

    print("")
    print("Running final audit " + str(index) + "/2")
    print(nodeid)

    started = time.monotonic()

    with log_path.open("w", encoding="utf-8") as log:
      process = subprocess.Popen(
        [
          sys.executable,
          "-m",
          "pytest",
          "--noconftest",
          nodeid,
          "-q",
          "--tb=short",
          "--durations=10",
          "-p",
          "no:cacheprovider",
          "-o",
          "addopts=",
        ],
        cwd=root,
        env=_env(root),
        stdout=log,
        stderr=subprocess.STDOUT,
        text=True,
      )

      try:
        return_code = process.wait(timeout=args.timeout)
        status = "PASS" if return_code == 0 else "FAIL"
      except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        status = "TIMEOUT"

    elapsed = time.monotonic() - started
    text = log_path.read_text(encoding="utf-8", errors="replace")
    print(text, end="" if text.endswith("\n") else "\n")

    results[str(index)] = {
      "nodeid": nodeid,
      "status": status,
      "elapsed_seconds": round(elapsed, 2),
    }

    print(
      "Audit "
      + str(index)
      + ": "
      + status
      + " in "
      + f"{elapsed:.2f}s"
    )

  all_pass = all(
    row["status"] == "PASS"
    for row in results.values()
  )

  payload = {
    "current_collected_tests": collected,
    "routine_test_count": 10382,
    "audit_only_count": 2,
    "audits": results,
    "all_audit_only_pass": all_pass,
    "phase156_deferred_duplicate_pressure": 117,
    "monolithic_repository_pytest_run": False,
  }

  (output / "audit_result.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
  )

  print("")
  print("Routine tests: 10382")
  print("Audit-only tests: 2")
  print("Phase156 deferred duplicate pressure: 117")
  print("All final audit-only PASS:", all_pass)

  return 0 if all_pass else 1


if __name__ == "__main__":
  raise SystemExit(main())
