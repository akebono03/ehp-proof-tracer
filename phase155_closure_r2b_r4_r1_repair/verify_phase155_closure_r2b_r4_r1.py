from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


NODEIDS = (
  (
    "tests/test_phase155_audit_boundary.py::"
    "test_phase155_audit_boundary_has_2_exact_nodeids"
  ),
  (
    "tests/test_phase155_audit_boundary.py::"
    "test_phase155_audit_boundary_contains_only_phase144_tests"
  ),
  (
    "tests/test_phase155_audit_boundary.py::"
    "test_phase155_audit_boundary_keeps_function_level_nodeids"
  ),
  (
    "tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py::"
    "test_phase144_6_r5_42_nonunique_phase41_arguments_are_deterministic"
  ),
  (
    "tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py::"
    "test_phase144_6_r5_43_10_pi6_transport_semantics_support_compression_connector"
  ),
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

  print(
    "Run only repaired R2B-R4 focused tests."
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
    "Closure-R2B-R4-R1 focused verification: PASS"
  )
  print(
    "Heavy audit-only tests executed: 0"
  )
  print(
    "Repository-wide pytest: NOT run"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
