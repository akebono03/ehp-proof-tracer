from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path


EXPECTED_AUDIT_NODEIDS = (
  (
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::"
    "test_phase144_6_r5_43_11d_final_completion_invariants_pass"
  ),
  (
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::"
    "test_phase144_6_r5_43_11d_renderer_remains_generic"
  ),
  (
    "tests/test_phase153_r3_10_public_reference_connection_repair.py::"
    "test_phase153_r3_10_all_group_reference_population_invariants"
  ),
  (
    "tests/test_phase153_r3_11_reference_body_ownership_repair.py::"
    "test_phase153_r3_11_all_112_groups_have_no_exact_selected_statement_body_duplicates"
  ),
  (
    "tests/test_phase97_actual_representative_targets_top_level_api.py::"
    "test_phase97_5_representative_goal_source_provenance_survives_cross_layer_api"
  ),
)


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


def _read_manifest(
  repo_root: Path,
) -> tuple[str, ...]:
  path = (
    repo_root
    / "tests"
    / "phase155_audit_only_nodeids.txt"
  )

  if not path.exists():
    raise SystemExit(
      "Audit-only manifest not found: "
      + str(
        path
      )
    )

  nodeids = tuple(
    line.strip()
    for line in path.read_text(
      encoding="utf-8"
    ).splitlines()
    if line.strip()
  )

  if set(
    nodeids
  ) != set(
    EXPECTED_AUDIT_NODEIDS
  ):
    raise SystemExit(
      "Audit-only manifest differs from the reviewed exact five.\n"
      + "actual="
      + repr(
        sorted(
          nodeids
        )
      )
    )

  if len(
    nodeids
  ) != 5:
    raise SystemExit(
      "Audit-only manifest must contain exactly five nodeids."
    )

  return nodeids


def _collect_current_tests(
  repo_root: Path,
  output_dir: Path,
) -> int:
  log_path = (
    output_dir
    / "collection.log"
  )

  command = [
    sys.executable,
    "-m",
    "pytest",
    "tests",
    "--collect-only",
    "-q",
  ]

  started = time.monotonic()

  with log_path.open(
    "w",
    encoding="utf-8",
  ) as log:
    completed = subprocess.run(
      command,
      cwd=repo_root,
      stdout=log,
      stderr=subprocess.STDOUT,
      text=True,
    )

  elapsed = (
    time.monotonic()
    - started
  )

  if completed.returncode != 0:
    raise SystemExit(
      "Current test collection failed. "
      + "See "
      + str(
        log_path
      )
    )

  text = log_path.read_text(
    encoding="utf-8",
    errors="replace",
  )
  matches = re.findall(
    r"(\d+)\s+tests collected",
    text,
  )

  if not matches:
    raise SystemExit(
      "Could not parse collected test count from "
      + str(
        log_path
      )
    )

  count = int(
    matches[
      -1
    ]
  )

  print(
    "Current tests collected:",
    count,
  )
  print(
    "Collection elapsed:",
    f"{elapsed:.2f}s",
  )

  return count


def _run_one(
  repo_root: Path,
  output_dir: Path,
  index: int,
  nodeid: str,
  timeout_seconds: int,
) -> tuple[str, float]:
  log_path = (
    output_dir
    / (
      "audit_"
      + str(
        index
      )
      + ".log"
    )
  )

  command = [
    sys.executable,
    "-m",
    "pytest",
    nodeid,
    "-q",
    "--tb=short",
    "--durations=10",
    "-p",
    "no:cacheprovider",
  ]

  started = time.monotonic()

  with log_path.open(
    "w",
    encoding="utf-8",
  ) as log:
    process = subprocess.Popen(
      command,
      cwd=repo_root,
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
          "\nPHASE155_R4_AUDIT_TIMEOUT "
          + str(
            timeout_seconds
          )
          + "s\n"
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

  return (
    (
      "PASS"
      if return_code == 0
      else "FAIL"
    ),
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
  output_dir = args.output_dir.resolve()
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  manifest = _read_manifest(
    repo_root
  )
  collected = _collect_current_tests(
    repo_root,
    output_dir,
  )

  if collected < len(
    manifest
  ):
    raise SystemExit(
      "Collected test count is smaller than audit-only count."
    )

  checkpoint_path = (
    output_dir
    / "audit_checkpoint.json"
  )
  checkpoint = _load_json(
    checkpoint_path,
    {
      "audits": {},
    },
  )

  for index, nodeid in enumerate(
    manifest,
    start=1,
  ):
    key = str(
      index
    )
    previous = checkpoint[
      "audits"
    ].get(
      key
    )

    if (
      previous is not None
      and previous.get(
        "status"
      )
      == "PASS"
      and previous.get(
        "nodeid"
      )
      == nodeid
    ):
      print(
        "Audit "
        + str(
          index
        )
        + ": already PASS, skipping."
      )
      continue

    print("")
    print(
      "=============================================================="
    )
    print(
      "Running Phase155 audit-only "
      + str(
        index
      )
      + "/5"
    )
    print(
      "=============================================================="
    )
    print(
      nodeid
    )

    status, elapsed = _run_one(
      repo_root,
      output_dir,
      index,
      nodeid,
      args.timeout_seconds,
    )

    checkpoint[
      "audits"
    ][
      key
    ] = {
      "nodeid": nodeid,
      "status": status,
      "elapsed_seconds": round(
        elapsed,
        2,
      ),
    }
    _save_json(
      checkpoint_path,
      checkpoint,
    )

    print(
      "Audit "
      + str(
        index
      )
      + ": "
      + status
      + " in "
      + f"{elapsed:.2f}s"
    )

  all_pass = all(
    checkpoint[
      "audits"
    ].get(
      str(
        index
      ),
      {},
    ).get(
      "status"
    )
    == "PASS"
    for index in range(
      1,
      6,
    )
  )

  result = {
    "current_collected_tests": collected,
    "audit_only_count": 5,
    "routine_test_count": collected - 5,
    "audits": checkpoint[
      "audits"
    ],
    "all_audit_only_pass": all_pass,
    "monolithic_repository_pytest_run": False,
  }

  result_path = (
    output_dir
    / "audit_result.json"
  )
  _save_json(
    result_path,
    result,
  )

  print("")
  print(
    "Current collected tests:",
    collected,
  )
  print(
    "Routine tests:",
    collected - 5,
  )
  print(
    "Audit-only tests:",
    5,
  )
  print(
    "All audit-only PASS:",
    all_pass,
  )
  print(
    "Monolithic repository-wide pytest: NOT run"
  )

  return (
    0
    if all_pass
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
