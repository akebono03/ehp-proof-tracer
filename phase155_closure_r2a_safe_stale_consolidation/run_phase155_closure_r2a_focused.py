from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from phase155_closure_r2a_batches import (
  BATCHES,
)


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase155_closure_r2a_output"
    ),
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()
  output_dir = (
    args.output_dir
    if args.output_dir.is_absolute()
    else repo_root
    / args.output_dir
  )
  checkpoints = output_dir / "checkpoints"
  logs = output_dir / "logs"
  checkpoints.mkdir(
    parents=True,
    exist_ok=True,
  )
  logs.mkdir(
    parents=True,
    exist_ok=True,
  )

  total_nodeids = sum(
    len(
      nodeids
    )
    for _name, nodeids in BATCHES
  )

  print(
    "Phase 155 Closure-R2A focused verification"
  )
  print(
    "Focused nodeids:",
    total_nodeids,
  )
  print(
    "Batches:",
    len(
      BATCHES
    ),
  )
  print(
    "Repository-wide pytest: NOT run"
  )
  print("")

  if total_nodeids != 38:
    raise SystemExit(
      "Expected exactly 38 SAFE_STALE nodeids"
    )

  failed_batches = []

  for index, (
    batch_name,
    nodeids,
  ) in enumerate(
    BATCHES,
    start=1,
  ):
    checkpoint = checkpoints / (
      batch_name
      + ".json"
    )

    if checkpoint.exists():
      payload = json.loads(
        checkpoint.read_text(
          encoding="utf-8"
        )
      )
      if payload.get(
        "status"
      ) == "PASS":
        print(
          f"[batch {index}/{len(BATCHES)}] "
          f"checkpoint PASS - skip {batch_name}"
        )
        continue

    print(
      f"[batch {index}/{len(BATCHES)}] "
      f"START {batch_name} "
      f"({len(nodeids)} tests)"
    )

    command = [
      sys.executable,
      "-m",
      "pytest",
      *nodeids,
      "-q",
      "--tb=line",
      "--durations=10",
      "--durations-min=1.0",
      "-p",
      "no:cacheprovider",
    ]

    started = time.perf_counter()
    result = subprocess.run(
      command,
      cwd=repo_root,
      capture_output=True,
      text=True,
      encoding="utf-8",
      errors="replace",
    )
    elapsed = time.perf_counter() - started

    log_path = logs / (
      batch_name
      + ".log"
    )
    log_text = result.stdout + result.stderr
    log_path.write_text(
      log_text,
      encoding="utf-8",
    )

    print(
      log_text,
      end="",
    )

    status = (
      "PASS"
      if result.returncode == 0
      else "FAIL"
    )

    checkpoint.write_text(
      json.dumps(
        {
          "batch": batch_name,
          "status": status,
          "returncode": result.returncode,
          "elapsed_seconds": elapsed,
          "nodeids": nodeids,
          "log": str(
            log_path
          ),
        },
        ensure_ascii=False,
        indent=2,
      )
      + "\n",
      encoding="utf-8",
    )

    print(
      f"[batch {index}/{len(BATCHES)}] "
      f"{status} {elapsed:.2f}s {batch_name}"
    )

    if result.returncode != 0:
      failed_batches.append(
        batch_name
      )
      break

  summary = {
    "focused_nodeids": total_nodeids,
    "batch_count": len(
      BATCHES
    ),
    "failed_batches": failed_batches,
    "repository_wide_pytest_run": False,
  }

  (
    output_dir
    / "phase155_closure_r2a_summary.json"
  ).write_text(
    json.dumps(
      summary,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  if failed_batches:
    print("")
    print(
      "Focused verification FAILED."
    )
    print(
      "PASS checkpoints are preserved."
    )
    print(
      "Repair only the failed batch before rerun."
    )
    return 1

  print("")
  print(
    "Closure-R2A focused verification: PASS"
  )
  print(
    "Repository-wide pytest: NOT run"
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
