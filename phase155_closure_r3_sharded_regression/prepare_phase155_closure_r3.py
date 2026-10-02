from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
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
    required=True,
  )
  parser.add_argument(
    "--shard-count",
    type=int,
    default=8,
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()
  package_dir = args.package_dir.resolve()
  output_dir = args.output_dir.resolve()

  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  collection_path = (
    output_dir
    / "routine_collection.json"
  )
  plan_path = (
    output_dir
    / "shard_plan.json"
  )

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

  collect_command = [
    sys.executable,
    "-m",
    "pytest",
    "tests",
    "--collect-only",
    "-q",
    "-p",
    "phase155_shard_plugin",
    "--phase155-export-collection",
    str(
      collection_path
    ),
  ]

  print(
    "Collecting routine tests only "
    "(audit-only manifest is excluded)."
  )
  completed = subprocess.run(
    collect_command,
    cwd=repo_root,
    env=env,
  )

  if completed.returncode != 0:
    return completed.returncode

  historical_log = (
    repo_root
    / "phase155_closure_output"
    / "phase155_full_pytest.log"
  )
  audit_manifest = (
    repo_root
    / "tests"
    / "phase155_audit_only_nodeids.txt"
  )

  planner_command = [
    sys.executable,
    str(
      package_dir
      / "phase155_shard_planner.py"
    ),
    "--collection",
    str(
      collection_path
    ),
    "--historical-log",
    str(
      historical_log
    ),
    "--audit-manifest",
    str(
      audit_manifest
    ),
    "--shard-count",
    str(
      args.shard_count
    ),
    "--output",
    str(
      plan_path
    ),
  ]

  return subprocess.run(
    planner_command,
    cwd=repo_root,
  ).returncode


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
