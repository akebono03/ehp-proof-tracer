from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


NODEIDS = (
  "tests/test_phase95_actual_representative_top_level_capability.py::test_phase95_20_pi9_5_preserves_order_two_generator_and_actual_ehp_provenance",
  "tests/test_phase95_actual_representative_top_level_capability.py::test_phase95_20_pi10_4_preserves_order_eight_outer_phase73_branch",
  "tests/test_phase96_proof_step_source_presentation.py::test_phase96_5_actual_pi9_5_aggregate_goal_source_preserves_theorem_phase_and_branch",
  "tests/test_phase96_proof_step_source_presentation.py::test_phase96_5_actual_aggregate_result_source_and_goal_source_remain_distinct",
  "tests/test_phase96_proof_step_source_presentation.py::test_phase96_5_actual_internal_dependency_does_not_inherit_aggregate_theorem_metadata",
  "tests/test_phase98_actual_use_facade_validation.py::test_phase98_3_facade_preserves_goal_source_provenance",
  "tests/test_phase155_audit_boundary.py::test_phase155_audit_boundary_has_3_exact_nodeids",
  "tests/test_phase155_audit_boundary.py::test_phase155_audit_boundary_contains_only_phase144_tests",
  "tests/test_phase155_audit_boundary.py::test_phase155_audit_boundary_keeps_function_level_nodeids",
)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()

  result = subprocess.run(
    [
      sys.executable,
      "-m",
      "pytest",
      *NODEIDS,
      "-q",
      "--tb=line",
      "--durations=12",
      "-p",
      "no:cacheprovider",
    ],
    cwd=repo_root,
  )

  if result.returncode != 0:
    return result.returncode

  print("")
  print(
    "Closure-R2C-R3 focused verification: PASS"
  )
  print(
    "112-group audit executed: 0"
  )
  print(
    "Repository-wide pytest: NOT run"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
