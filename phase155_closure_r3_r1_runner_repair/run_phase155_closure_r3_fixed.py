from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def _load_json(
  path: Path,
  default,
):
  if not path.exists():
    return default

  return json.loads(
    path.read_text(
      encoding="utf-8"
    )
  )


def _save_json(
  path: Path,
  value,
):
  path.write_text(
    json.dumps(
      value,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )


def _run_shard(
  *,
  repo_root: Path,
  package_dir: Path,
  plan_path: Path,
  shard_index: int,
  timeout_seconds: int,
  log_path: Path,
) -> tuple[str, float]:
  env = dict(
    os.environ
  )

  old_pythonpath = env.get(
    "PYTHONPATH",
    "",
  )
  env[
    "PYTHONPATH"
  ] = (
    str(
      package_dir
    )
    + (
      os.pathsep
      + old_pythonpath
      if old_pythonpath
      else ""
    )
  )

  command = [
    sys.executable,
    "-m",
    "pytest",
    "tests",
    "-q",
    "--tb=short",
    "--durations=20",
    "-p",
    "phase155_shard_plugin",
    "--phase155-shard-plan",
    str(
      plan_path
    ),
    "--phase155-shard-index",
    str(
      shard_index
    ),
  ]

  print("")
  print(
    "=============================================================="
  )
  print(
    f"Running Phase155 shard {shard_index}"
  )
  print(
    "=============================================================="
  )
  print(
    "Log:",
    log_path,
  )

  started = time.monotonic()

  with log_path.open(
    "w",
    encoding="utf-8",
  ) as log:
    process = subprocess.Popen(
      command,
      cwd=repo_root,
      env=env,
      stdout=log,
      stderr=subprocess.STDOUT,
      text=True,
    )

    try:
      return_code = process.wait(
        timeout=timeout_seconds
      )
    except subprocess.TimeoutExpired:
      process.kill()
      process.wait()
      elapsed = (
        time.monotonic()
        - started
      )
      with log_path.open(
        "a",
        encoding="utf-8",
      ) as timeout_log:
        timeout_log.write(
          "\nPHASE155_SHARD_TIMEOUT "
          + str(
            timeout_seconds
          )
          + "s\n"
        )

      print(
        "Shard "
        + str(
          shard_index
        )
        + " timed out after "
        + str(
          timeout_seconds
        )
        + "s."
      )
      return (
        "TIMEOUT",
        elapsed,
      )

  elapsed = (
    time.monotonic()
    - started
  )

  log_text = log_path.read_text(
    encoding="utf-8",
    errors="replace",
  )
  print(
    log_text,
    end=(
      ""
      if log_text.endswith(
        "\n"
      )
      else "\n"
    ),
  )

  if return_code == 0:
    return (
      "PASS",
      elapsed,
    )

  return (
    "FAIL",
    elapsed,
  )


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
    "--plan",
    type=Path,
    required=True,
  )
  parser.add_argument(
    "--output-dir",
    type=Path,
    required=True,
  )
  parser.add_argument(
    "--timeout-seconds",
    type=int,
    default=600,
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()
  package_dir = args.package_dir.resolve()
  plan_path = args.plan.resolve()
  output_dir = args.output_dir.resolve()

  plan = json.loads(
    plan_path.read_text(
      encoding="utf-8"
    )
  )
  shard_count = int(
    plan[
      "shard_count"
    ]
  )

  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  checkpoint_path = (
    output_dir
    / "checkpoint.json"
  )
  checkpoint = _load_json(
    checkpoint_path,
    {
      "shards": {},
    },
  )

  for shard_index in range(
    1,
    shard_count + 1,
  ):
    key = str(
      shard_index
    )
    previous = checkpoint[
      "shards"
    ].get(
      key
    )

    if (
      previous is not None
      and previous.get(
        "status"
      )
      == "PASS"
    ):
      print(
        f"Shard {shard_index}: already PASS, skipping."
      )
      continue

    log_path = (
      output_dir
      / (
        "shard_"
        + str(
          shard_index
        ).zfill(
          2
        )
        + ".log"
      )
    )

    status, elapsed = _run_shard(
      repo_root=repo_root,
      package_dir=package_dir,
      plan_path=plan_path,
      shard_index=shard_index,
      timeout_seconds=args.timeout_seconds,
      log_path=log_path,
    )

    checkpoint[
      "shards"
    ][
      key
    ] = {
      "status": status,
      "elapsed_seconds": round(
        elapsed,
        2,
      ),
      "log": str(
        log_path
      ),
    }
    _save_json(
      checkpoint_path,
      checkpoint,
    )

    print(
      f"Shard {shard_index}: {status} "
      f"in {elapsed:.2f}s"
    )

  statuses = {
    index: checkpoint[
      "shards"
    ].get(
      str(
        index
      ),
      {
        "status": "NOT_RUN",
      },
    )[
      "status"
    ]
    for index in range(
      1,
      shard_count + 1
    )
  }

  summary_path = (
    output_dir
    / "summary.txt"
  )

  lines = [
    "Phase 155 Closure-R3 sharded regression",
    "",
  ]

  for index in range(
    1,
    shard_count + 1
  ):
    row = checkpoint[
      "shards"
    ].get(
      str(
        index
      ),
      {}
    )
    lines.append(
      "Shard "
      + str(
        index
      )
      + ": "
      + row.get(
        "status",
        "NOT_RUN",
      )
      + (
        " ("
        + str(
          row.get(
            "elapsed_seconds"
          )
        )
        + "s)"
        if "elapsed_seconds" in row
        else ""
      )
    )

  all_pass = all(
    status == "PASS"
    for status in statuses.values()
  )

  lines.extend(
    [
      "",
      "Audit-only tests executed: 0",
      "Repository-wide monolithic pytest: NOT run",
      (
        "Closure-R3 result: PASS"
        if all_pass
        else "Closure-R3 result: INCOMPLETE"
      ),
    ]
  )

  summary_path.write_text(
    "\n".join(
      lines
    )
    + "\n",
    encoding="utf-8",
  )

  print("")
  print(
    summary_path.read_text(
      encoding="utf-8"
    )
  )

  if all_pass:
    return 0

  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
