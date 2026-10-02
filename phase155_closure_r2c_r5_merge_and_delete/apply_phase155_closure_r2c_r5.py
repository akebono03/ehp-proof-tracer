from __future__ import annotations

import argparse
import ast
from pathlib import Path


EXPECTED_MERGE_FIVE = {'tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_public_reference_markers_cover_structured_entries', 'tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py::test_phase153_r3_9_all_reference_entries_have_selected_statement', 'tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_representative_goal_sources_preserve_theorem_phase_and_branch', 'tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_selected_statements_are_publicly_visible', 'tests/test_phase97_actual_representative_targets_top_level_api.py::test_phase97_5_representative_goal_source_provenance_survives_top_level_api'}
EXPECTED_DELETE_SIX = {'tests/test_phase153_r2_public_reference_semantic_fact.py::test_phase153_r2_public_pi10_6_excludes_obsolete_45_reference', 'tests/test_phase153_r3_5_reference_body_duplicate_suppression.py::test_phase153_r3_5_public_pi10_6_keeps_current_reference_baseline_without_obsolete_45', 'tests/test_phase98_representative_convenience_validation.py::test_phase98_6_shortest_path_preserves_goal_source_provenance', 'tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_integrates_calculation_source_metadata', 'tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_result_source_and_goal_source_remain_distinct', 'tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_all_representative_results_keep_result_and_goal_sources_distinct'}

NEW_AUDIT_ONLY = {'tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_group_reference_population_invariants', 'tests/test_phase97_actual_representative_targets_top_level_api.py::test_phase97_5_representative_goal_source_provenance_survives_cross_layer_api'}

REPLACE = {
  (
    "tests/test_phase153_r3_10_public_reference_connection_repair.py",
    "test_phase153_r3_10_all_selected_statements_are_publicly_visible",
  ): 'def test_phase153_r3_10_all_group_reference_population_invariants():\n  missing_statements = []\n  missing_markers = []\n  entries_without_selected_statement = []\n\n  for (\n    n,\n    k,\n    raw_presentation,\n    presentation,\n  ) in _phase153_r3_10_presentations():\n    entries = (\n      build_toda_group_proof_narrative_reference_entries(\n        presentation\n      )\n    )\n\n    if not entries:\n      continue\n\n    selected_by_number = (\n      _toda_group_proof_narrative_reference_statement_lines_by_number(\n        presentation,\n        entries,\n      )\n    )\n    canonical_reference_section = (\n      render_toda_group_proof_narrative_reference_entries_markdown(\n        entries,\n        selected_by_number,\n      )\n    )\n    rendered = (\n      render_toda_group_proof_narrative_markdown(\n        raw_presentation\n      )\n    )\n    public_reference_section = (\n      _phase153_r3_10_public_reference_section(\n        rendered,\n        canonical_reference_section,\n      )\n    )\n\n    assert public_reference_section, (\n      n,\n      k,\n      rendered,\n    )\n\n    for entry in entries:\n      statement_lines = (\n        selected_by_number.get(\n          entry.number,\n          (),\n        )\n      )\n\n      if not statement_lines:\n        entries_without_selected_statement.append(\n          (\n            n,\n            k,\n            entry.number,\n            entry.reference.locator\n            or entry.reference.label,\n          )\n        )\n\n      marker = (\n        "[R"\n        + str(\n          entry.number\n        )\n        + "]"\n      )\n\n      if marker not in public_reference_section:\n        missing_markers.append(\n          (\n            n,\n            k,\n            entry.number,\n            entry.reference.locator\n            or entry.reference.label,\n          )\n        )\n\n      for statement_line in statement_lines:\n        if statement_line in public_reference_section:\n          continue\n\n        missing_statements.append(\n          (\n            n,\n            k,\n            entry.number,\n            entry.reference.locator\n            or entry.reference.label,\n            statement_line,\n          )\n        )\n\n  assert entries_without_selected_statement == []\n  assert missing_markers == []\n  assert missing_statements == []\n',
  (
    "tests/test_phase97_actual_representative_targets_top_level_api.py",
    "test_phase97_5_representative_goal_source_provenance_survives_top_level_api",
  ): 'def test_phase97_5_representative_goal_source_provenance_survives_cross_layer_api():\n  actual = build_phase97_5_data()\n\n  expected = {\n    "pi7_4": (\n      "65",\n      "Toda Proposition 5.6",\n      "pi7_4_group_relation",\n    ),\n    "pi9_5": (\n      "68",\n      "Toda Proposition 5.8",\n      "pi9_5_group_relation",\n    ),\n    "pi10_4": (\n      "73",\n      "Toda Proposition 5.11",\n      "pi10_4_group_relation",\n    ),\n    "pi11_5": (\n      "73",\n      "Toda Proposition 5.11",\n      (\n        "nu_squared_finite_dimensional."\n        "pi11_5_group_relation"\n      ),\n    ),\n    "pi9_2": (\n      "75",\n      "Toda Proposition 5.15",\n      "pi9_2_zero",\n    ),\n    "pi12_5": (\n      "75",\n      "Toda Proposition 5.15",\n      "pi12_5_group_relation",\n    ),\n  }\n\n  for (\n    key,\n    (\n      expected_phase,\n      expected_theorem,\n      expected_branch,\n    ),\n  ) in expected.items():\n    report_candidate = (\n      get_phase97_5_single_report_candidate(\n        actual[\n          "results"\n        ][\n          key\n        ]\n      )\n    )\n    source_candidate = (\n      report_candidate.source_candidate\n    )\n    goal_source = (\n      source_candidate.goal_source\n    )\n    presented_source = (\n      report_candidate\n      .presentation\n      .source\n      .goal_source\n    )\n\n    assert goal_source is not None\n    assert presented_source is not None\n    assert (\n      presented_source\n      .source_goal_source\n      is goal_source\n    )\n    assert (\n      presented_source\n      .repository_source\n      .source_entry\n      is goal_source.source_entry\n    )\n    assert (\n      presented_source\n      .repository_source\n      .phase\n      == expected_phase\n    )\n    assert (\n      presented_source\n      .repository_source\n      .theorem\n      == expected_theorem\n    )\n    assert (\n      presented_source.branch_name\n      == expected_branch\n    )\n',
}

REMOVE_FROM_MERGE = {
  "tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_public_reference_markers_cover_structured_entries",
  "tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py::test_phase153_r3_9_all_reference_entries_have_selected_statement",
  "tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_representative_goal_sources_preserve_theorem_phase_and_branch",
}

EXISTING_AUDIT_ONLY = {
  (
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::"
    "test_phase144_6_r5_43_11d_final_completion_invariants_pass"
  ),
  (
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::"
    "test_phase144_6_r5_43_11d_renderer_remains_generic"
  ),
  (
    "tests/test_phase153_r3_11_reference_body_ownership_repair.py::"
    "test_phase153_r3_11_all_112_groups_have_no_exact_selected_statement_body_duplicates"
  ),
}


def _read_nodeids(path):
  return {
    line.strip()
    for line in path.read_text(
      encoding="utf-8"
    ).splitlines()
    if line.strip()
  }


def _functions(source):
  tree = ast.parse(source)
  return {
    node.name: node
    for node in tree.body
    if isinstance(node, ast.FunctionDef)
  }


def _replace(source, old_name, replacement):
  lines = source.splitlines(
    keepends=True
  )
  functions = _functions(
    source
  )

  if old_name not in functions:
    raise RuntimeError(
      "Function not found for replacement: "
      + old_name
    )

  node = functions[
    old_name
  ]

  if node.end_lineno is None:
    raise RuntimeError(
      "AST end_lineno unavailable: "
      + old_name
    )

  start = sum(
    len(line)
    for line in lines[
      :node.lineno - 1
    ]
  )
  end = sum(
    len(line)
    for line in lines[
      :node.end_lineno
    ]
  )

  updated = (
    source[:start]
    + replacement.rstrip(
      "\n"
    )
    + "\n"
    + source[end:]
  )

  ast.parse(
    updated
  )
  return updated


def _remove_functions(source, names):
  lines = source.splitlines(
    keepends=True
  )
  functions = _functions(
    source
  )

  missing = set(
    names
  ) - set(
    functions
  )

  if missing:
    raise RuntimeError(
      "Functions not found for deletion: "
      + ", ".join(
        sorted(
          missing
        )
      )
    )

  spans = []

  for name in names:
    node = functions[
      name
    ]

    if node.end_lineno is None:
      raise RuntimeError(
        "AST end_lineno unavailable: "
        + name
      )

    spans.append(
      (
        node.lineno - 1,
        node.end_lineno,
      )
    )

  for start, end in sorted(
    spans,
    reverse=True,
  ):
    del lines[
      start:end
    ]

    while (
      start < len(
        lines
      )
      and lines[
        start
      ].strip()
      == ""
      and start > 0
      and lines[
        start - 1
      ].strip()
      == ""
    ):
      del lines[
        start
      ]

  updated = "".join(
    lines
  )
  ast.parse(
    updated
  )
  return updated


def _group(nodeids):
  grouped = {}

  for nodeid in nodeids:
    path, name = nodeid.split(
      "::",
      1,
    )
    grouped.setdefault(
      path,
      set(),
    ).add(
      name
    )

  return grouped


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()
  r4_dir = (
    repo_root
    / "phase155_closure_r2c_r4_output"
  )

  merge_path = (
    r4_dir
    / "merge_candidate.txt"
  )
  delete_path = (
    r4_dir
    / "delete_candidate.txt"
  )

  for path in (
    merge_path,
    delete_path,
  ):
    if not path.exists():
      raise SystemExit(
        "Required R2C-R4 output not found: "
        + str(
          path
        )
      )

  actual_merge = _read_nodeids(
    merge_path
  )
  actual_delete = _read_nodeids(
    delete_path
  )

  if actual_merge != EXPECTED_MERGE_FIVE:
    raise SystemExit(
      "R2C-R4 MERGE_CANDIDATE set differs from reviewed five. "
      + "actual="
      + repr(
        sorted(
          actual_merge
        )
      )
    )

  if actual_delete != EXPECTED_DELETE_SIX:
    raise SystemExit(
      "R2C-R4 DELETE_CANDIDATE set differs from reviewed six. "
      + "actual="
      + repr(
        sorted(
          actual_delete
        )
      )
    )

  changed = set()

  for (
    relative_path,
    old_name,
  ), replacement in REPLACE.items():
    path = (
      repo_root
      / relative_path
    )
    source = path.read_text(
      encoding="utf-8-sig"
    )
    updated = _replace(
      source,
      old_name,
      replacement,
    )
    path.write_text(
      updated,
      encoding="utf-8",
    )
    changed.add(
      relative_path
    )

  removal_nodeids = (
    EXPECTED_DELETE_SIX
    | REMOVE_FROM_MERGE
  )

  for relative_path, names in _group(
    removal_nodeids
  ).items():
    path = (
      repo_root
      / relative_path
    )
    source = path.read_text(
      encoding="utf-8-sig"
    )
    updated = _remove_functions(
      source,
      names,
    )
    path.write_text(
      updated,
      encoding="utf-8",
    )
    changed.add(
      relative_path
    )

  manifest_path = (
    repo_root
    / "tests"
    / "phase155_audit_only_nodeids.txt"
  )
  current_audits = _read_nodeids(
    manifest_path
  )

  if current_audits != EXISTING_AUDIT_ONLY:
    raise SystemExit(
      "Existing audit-only boundary differs from expected pre-R2C-R5 three."
    )

  final_audits = (
    EXISTING_AUDIT_ONLY
    | NEW_AUDIT_ONLY
  )

  manifest_path.write_text(
    "".join(
      nodeid + "\n"
      for nodeid in sorted(
        final_audits
      )
    ),
    encoding="utf-8",
  )
  changed.add(
    "tests/phase155_audit_only_nodeids.txt"
  )

  boundary_path = (
    repo_root
    / "tests"
    / "test_phase155_audit_boundary.py"
  )
  boundary_source = (
    boundary_path.read_text(
      encoding="utf-8-sig"
    )
  )

  exact_boundary = """def test_phase155_audit_boundary_has_5_exact_nodeids():
  nodeids = _phase155_audit_nodeids()

  assert set(
    nodeids
  ) == {
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
  }
  assert len(
    nodeids
  ) == 5
"""

  phase_boundary = """def test_phase155_audit_boundary_contains_only_reviewed_phase144_phase153_or_phase97_tests():
  nodeids = _phase155_audit_nodeids()

  assert all(
    (
      nodeid.startswith(
        "tests/test_phase144_"
      )
      or nodeid.startswith(
        "tests/test_phase153_"
      )
      or nodeid.startswith(
        "tests/test_phase97_"
      )
    )
    for nodeid in nodeids
  )
"""

  boundary_source = _replace(
    boundary_source,
    "test_phase155_audit_boundary_has_3_exact_nodeids",
    exact_boundary,
  )
  boundary_source = _replace(
    boundary_source,
    "test_phase155_audit_boundary_contains_only_reviewed_phase144_or_phase153_tests",
    phase_boundary,
  )
  boundary_path.write_text(
    boundary_source,
    encoding="utf-8",
  )
  changed.add(
    "tests/test_phase155_audit_boundary.py"
  )

  print(
    "Phase 155 Closure-R2C-R5 changes applied."
  )
  print(
    "MERGE_CANDIDATE input:",
    len(
      EXPECTED_MERGE_FIVE
    ),
  )
  print(
    "Merged replacement tests:",
    len(
      REPLACE
    ),
  )
  print(
    "Deleted redundant test functions:",
    len(
      EXPECTED_DELETE_SIX
    ),
  )
  print(
    "Removed merge-source test functions:",
    len(
      REMOVE_FROM_MERGE
    ),
  )
  print(
    "Audit-only manifest total:",
    len(
      final_audits
    ),
  )
  print(
    "Production changes: none"
  )
  print(
    "Top-level import changes: none"
  )
  print(
    "Changed repository files:",
    len(
      changed
    ),
  )

  for path in sorted(
    changed
  ):
    print(
      " -",
      path,
    )


if __name__ == "__main__":
  main()
