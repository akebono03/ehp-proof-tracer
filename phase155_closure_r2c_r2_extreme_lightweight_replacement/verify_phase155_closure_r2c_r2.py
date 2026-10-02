from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


NODEIDS = (
  (
    "tests/test_phase95_top_level_calculation_orchestration.py::"
    "test_phase95_18_preserves_multiple_aggregate_candidates_in_registration_order"
  ),
  (
    "tests/test_phase97_single_found_calculation_to_report_api.py::"
    "test_phase97_3_aggregate_found_preserves_goal_source_provenance"
  ),
  (
    "tests/test_phase97_not_found_multiple_results_top_level_handling.py::"
    "test_phase97_4_multiple_aggregate_results_preserve_goal_source_order"
  ),
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

  print(
    "Run only the three lightweight extreme replacements."
  )

  result = subprocess.run(
    [
      sys.executable,
      "-m",
      "pytest",
      *NODEIDS,
      "-q",
      "--tb=line",
      "--durations=10",
      "-p",
      "no:cacheprovider",
    ],
    cwd=repo_root,
  )

  if result.returncode != 0:
    return result.returncode

  print("")
  print(
    "Closure-R2C-R2 focused verification: PASS"
  )
  print(
    "Old extreme fixtures executed: 0"
  )
  print(
    "Repository-wide pytest: NOT run"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
