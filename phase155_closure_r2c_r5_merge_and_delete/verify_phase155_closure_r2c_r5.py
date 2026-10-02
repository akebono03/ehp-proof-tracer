from __future__ import annotations

import argparse
import ast
import subprocess
import sys
from pathlib import Path


DELETED_OR_REPLACED_OLD = {
  "tests/test_phase153_r2_public_reference_semantic_fact.py::test_phase153_r2_public_pi10_6_excludes_obsolete_45_reference",
  "tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_selected_statements_are_publicly_visible",
  "tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_public_reference_markers_cover_structured_entries",
  "tests/test_phase153_r3_5_reference_body_duplicate_suppression.py::test_phase153_r3_5_public_pi10_6_keeps_current_reference_baseline_without_obsolete_45",
  "tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py::test_phase153_r3_9_all_reference_entries_have_selected_statement",
  "tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_integrates_calculation_source_metadata",
  "tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_result_source_and_goal_source_remain_distinct",
  "tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_representative_goal_sources_preserve_theorem_phase_and_branch",
  "tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_all_representative_results_keep_result_and_goal_sources_distinct",
  "tests/test_phase97_actual_representative_targets_top_level_api.py::test_phase97_5_representative_goal_source_provenance_survives_top_level_api",
  "tests/test_phase98_representative_convenience_validation.py::test_phase98_6_shortest_path_preserves_goal_source_provenance",
}

NEW_FUNCTIONS = {
  "tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_group_reference_population_invariants",
  "tests/test_phase97_actual_representative_targets_top_level_api.py::test_phase97_5_representative_goal_source_provenance_survives_cross_layer_api",
}


def _functions(
  path: Path,
) -> set[str]:
  tree = ast.parse(
    path.read_text(
      encoding="utf-8-sig"
    )
  )
  return {
    node.name
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()

  for nodeid in sorted(
    DELETED_OR_REPLACED_OLD
  ):
    relative_path, function_name = (
      nodeid.split(
        "::",
        1,
      )
    )
    functions = _functions(
      repo_root
      / relative_path
    )

    if function_name in functions:
      raise SystemExit(
        "Old redundant/merged function still exists: "
        + nodeid
      )

  for nodeid in sorted(
    NEW_FUNCTIONS
  ):
    relative_path, function_name = (
      nodeid.split(
        "::",
        1,
      )
    )
    functions = _functions(
      repo_root
      / relative_path
    )

    if function_name not in functions:
      raise SystemExit(
        "Merged replacement function missing: "
        + nodeid
      )

  result = subprocess.run(
    [
      sys.executable,
      "-m",
      "pytest",
      (
        "tests/test_phase155_audit_boundary.py::"
        "test_phase155_audit_boundary_has_5_exact_nodeids"
      ),
      (
        "tests/test_phase155_audit_boundary.py::"
        "test_phase155_audit_boundary_contains_only_reviewed_phase144_phase153_or_phase97_tests"
      ),
      (
        "tests/test_phase155_audit_boundary.py::"
        "test_phase155_audit_boundary_keeps_function_level_nodeids"
      ),
      "-q",
      "--tb=line",
      "-p",
      "no:cacheprovider",
    ],
    cwd=repo_root,
  )

  if result.returncode != 0:
    return result.returncode

  print("")
  print(
    "Closure-R2C-R5 static deletion/merge verification: PASS"
  )
  print(
    "Merged heavy audits executed: 0"
  )
  print(
    "Repository-wide pytest: NOT run"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
