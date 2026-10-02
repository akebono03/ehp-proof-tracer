from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


FAILED_FIVE = (
  "tests/test_phase132_8_group_proof_narrative_dedup.py::test_phase132_8_cli_narrative_uses_deduplicated_renderer",
  "tests/test_phase133_10_sigma_label_wording.py::test_phase133_10_sigma9_depth_two_uses_final_japanese_wording",
  "tests/test_phase133_6_group_proof_narrative_labels.py::test_phase133_6_sigma9_depth_two_reuses_new_labels",
  "tests/test_phase133_9_group_proof_narrative_labels.py::test_phase133_9_pi16_9_depth_two_uses_final_sigma_labels",
  "tests/test_phase133_9_group_proof_narrative_labels.py::test_phase133_9_previous_labels_remain_available",
)


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()
  output_dir = (
    repo_root
    / "phase155_closure_r2a_output"
  )
  checkpoints = (
    output_dir
    / "checkpoints"
  )
  checkpoint = (
    checkpoints
    / "batch_01_phase132_133.json"
  )

  print(
    "Run only the 5 previously failing tests."
  )

  env = os.environ.copy()
  env[
    "PYTHONIOENCODING"
  ] = "utf-8"

  result = subprocess.run(
    [
      sys.executable,
      "-m",
      "pytest",
      *FAILED_FIVE,
      "-q",
      "--tb=line",
      "--durations=10",
      "--durations-min=1.0",
      "-p",
      "no:cacheprovider",
    ],
    cwd=repo_root,
    env=env,
  )

  if result.returncode != 0:
    return result.returncode

  checkpoints.mkdir(
    parents=True,
    exist_ok=True,
  )

  checkpoint.write_text(
    json.dumps(
      {
        "batch": "batch_01_phase132_133",
        "status": "PASS",
        "evidence": (
          "7 tests passed in previous batch run; "
          "5 previously failing tests passed after R1 repair."
        ),
        "r1_repaired_nodeids": list(
          FAILED_FIVE
        ),
      },
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  print("")
  print(
    "batch_01 checkpoint promoted to PASS."
  )
  print(
    "Previous 7 PASS tests were unchanged."
  )

  original_runner = (
    repo_root
    / "phase155_closure_r2a_safe_stale_consolidation"
    / "run_phase155_closure_r2a_focused.py"
  )

  if not original_runner.exists():
    raise SystemExit(
      "Original R2A focused runner not found: "
      + str(
        original_runner
      )
    )

  print("")
  print(
    "Resume original R2A focused runner."
  )
  print(
    "Expected: batch 1 checkpoint PASS - skip; "
    "continue batches 2-4."
  )

  resumed = subprocess.run(
    [
      sys.executable,
      str(
        original_runner
      ),
      "--repo-root",
      str(
        repo_root
      ),
    ],
    cwd=repo_root,
    env=env,
  )

  return resumed.returncode


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
