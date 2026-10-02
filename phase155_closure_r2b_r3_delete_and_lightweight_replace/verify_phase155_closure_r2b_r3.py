from __future__ import annotations

import argparse
import ast
import subprocess
import sys
from pathlib import Path


DELETED_FUNCTIONS = {
  "test_phase144_6_r5_43_6_pi6_contains_expected_transport_and_integration_candidates",
  "test_phase144_6_r5_43_8_finds_sixteen_three_step_transport_chains",
  "test_phase144_6_r5_43_8_has_one_hidden_signature_sequence",
  "test_phase144_6_r5_43_8_reports_all_forty_eight_transport_occurrences",
  "test_phase144_6_r5_43_9_all_chains_observe_same_operation_kind",
  "test_phase144_6_r5_43_9_all_three_candidate_prose_levels_are_supported_by_observed_data",
  "test_phase144_6_r5_43_11_all_sixteen_transport_chains_are_connected",
  "test_phase144_6_r5_43_11_renderer_has_no_rule_name_or_pi6_specific_branch",
}

LIGHTWEIGHT_NODEID = (
  "tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py::"
  "test_phase144_6_r5_43_11_has_no_contribution_duplicates_or_order_violations"
)


def _all_test_functions(
  tests_dir: Path,
) -> set[str]:
  result = set()

  for path in tests_dir.glob(
    "test_phase144_*.py"
  ):
    source = path.read_text(
      encoding="utf-8-sig"
    )
    tree = ast.parse(
      source
    )

    for node in tree.body:
      if isinstance(
        node,
        ast.FunctionDef,
      ):
        result.add(
          node.name
        )

  return result


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()
  tests_dir = repo_root / "tests"

  functions = _all_test_functions(
    tests_dir
  )

  lingering = (
    DELETED_FUNCTIONS
    & functions
  )

  if lingering:
    raise SystemExit(
      "Deleted functions still present: "
      + ", ".join(
        sorted(
          lingering
        )
      )
    )

  manifest_path = (
    tests_dir
    / "phase155_audit_only_nodeids.txt"
  )

  audit_nodeids = {
    line.strip()
    for line in manifest_path.read_text(
      encoding="utf-8"
    ).splitlines()
    if line.strip()
  }

  if LIGHTWEIGHT_NODEID in audit_nodeids:
    raise SystemExit(
      "Lightweight replacement is still excluded from routine pytest."
    )

  print(
    "Static deletion verification: PASS"
  )
  print(
    "Deleted functions absent:",
    len(
      DELETED_FUNCTIONS
    ),
  )
  print(
    "Lightweight replacement is routine-visible: yes"
  )
  print("")
  print(
    "Run only the lightweight replacement test."
  )

  result = subprocess.run(
    [
      sys.executable,
      "-m",
      "pytest",
      LIGHTWEIGHT_NODEID,
      "-q",
      "--tb=line",
      "--durations=5",
      "-p",
      "no:cacheprovider",
    ],
    cwd=repo_root,
  )

  if result.returncode != 0:
    return result.returncode

  print("")
  print(
    "Closure-R2B-R3 focused verification: PASS"
  )
  print(
    "Repository-wide pytest: NOT run"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
