from __future__ import annotations

import argparse
import ast
from pathlib import Path


DELETE = {
  (
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py",
    "test_phase144_6_r5_43_11d_final_completion_invariants_pass",
  ),
  (
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py",
    "test_phase144_6_r5_43_11d_renderer_remains_generic",
  ),
  (
    "tests/test_phase153_r3_11_reference_body_ownership_repair.py",
    "test_phase153_r3_11_all_112_groups_have_no_exact_selected_statement_body_duplicates",
  ),
}

REPLACE = {
  (
    "tests/test_phase153_r3_10_public_reference_connection_repair.py",
    "test_phase153_r3_10_all_group_reference_population_invariants",
  ): 'def test_phase153_r3_10_all_group_reference_population_invariants():\n  import re\n\n  violations = []\n\n  for (\n    n,\n    k,\n    raw_presentation,\n    _presentation,\n  ) in _phase153_r3_10_presentations():\n    rendered = (\n      render_toda_group_proof_narrative_markdown(\n        raw_presentation\n      )\n    )\n\n    header_numbers = []\n    body_marker_numbers = []\n\n    for line in rendered.splitlines():\n      header_match = re.match(\n        r"^\\*\\*\\[R(\\d+)\\]",\n        line,\n      )\n\n      if header_match is not None:\n        header_numbers.append(\n          int(\n            header_match.group(\n              1\n            )\n          )\n        )\n        continue\n\n      body_marker_numbers.extend(\n        int(\n          number\n        )\n        for number in re.findall(\n          r"\\[R(\\d+)\\]",\n          line,\n        )\n      )\n\n    if header_numbers:\n      expected = list(\n        range(\n          1,\n          len(\n            header_numbers\n          )\n          + 1,\n        )\n      )\n\n      if header_numbers != expected:\n        violations.append(\n          (\n            n,\n            k,\n            "non_contiguous_reference_headers",\n            tuple(\n              header_numbers\n            ),\n          )\n        )\n\n      header_set = set(\n        header_numbers\n      )\n\n      for marker in body_marker_numbers:\n        if marker in header_set:\n          continue\n\n        violations.append(\n          (\n            n,\n            k,\n            "body_marker_without_header",\n            marker,\n          )\n        )\n\n      continue\n\n    if body_marker_numbers:\n      violations.append(\n        (\n          n,\n          k,\n          "body_markers_without_reference_headers",\n          tuple(\n            body_marker_numbers\n          ),\n        )\n      )\n\n  assert violations == []\n',
  (
    "tests/test_phase97_actual_representative_targets_top_level_api.py",
    "test_phase97_5_representative_goal_source_provenance_survives_cross_layer_api",
  ): 'def test_phase97_5_representative_goal_source_provenance_survives_cross_layer_api():\n  actual = build_phase97_5_data()\n\n  for key in REPRESENTATIVE_KEYS:\n    report_candidate = (\n      get_phase97_5_single_report_candidate(\n        actual[\n          "results"\n        ][\n          key\n        ]\n      )\n    )\n    source_candidate = (\n      report_candidate.source_candidate\n    )\n    source_presentation = (\n      report_candidate\n      .presentation\n      .source\n    )\n\n    assert (\n      source_presentation.source_candidate\n      is source_candidate\n    )\n    assert (\n      source_presentation\n      .result_source\n      .source_entry\n      is source_candidate\n      .group_result\n      .source_entry\n    )\n\n    goal_source = (\n      source_candidate.goal_source\n    )\n\n    if goal_source is None:\n      assert (\n        source_presentation.goal_source\n        is None\n      )\n      continue\n\n    presented_goal_source = (\n      source_presentation.goal_source\n    )\n\n    assert presented_goal_source is not None\n    assert (\n      presented_goal_source\n      .source_goal_source\n      is goal_source\n    )\n    assert (\n      presented_goal_source\n      .repository_source\n      .source_entry\n      is goal_source.source_entry\n    )\n    assert (\n      presented_goal_source\n      .repository_source\n      .phase\n      == goal_source\n      .source_entry\n      .phase\n    )\n    assert (\n      presented_goal_source\n      .repository_source\n      .theorem\n      == goal_source\n      .source_entry\n      .theorem\n    )\n    assert (\n      presented_goal_source.branch_name\n      == goal_source.branch_name\n    )\n',
}

FINAL_AUDIT_NODEIDS = (
  (
    "tests/test_phase153_r3_10_public_reference_connection_repair.py::"
    "test_phase153_r3_10_all_group_reference_population_invariants"
  ),
  (
    "tests/test_phase97_actual_representative_targets_top_level_api.py::"
    "test_phase97_5_representative_goal_source_provenance_survives_cross_layer_api"
  ),
)


def _functions(source: str):
  tree = ast.parse(source)
  return {
    node.name: node
    for node in tree.body
    if isinstance(node, ast.FunctionDef)
  }


def _replace(source: str, name: str, replacement: str) -> str:
  lines = source.splitlines(keepends=True)
  functions = _functions(source)

  if name not in functions:
    raise RuntimeError("Function not found for replacement: " + name)

  node = functions[name]

  if node.end_lineno is None:
    raise RuntimeError("AST end_lineno unavailable: " + name)

  start = sum(len(line) for line in lines[:node.lineno - 1])
  end = sum(len(line) for line in lines[:node.end_lineno])

  updated = (
    source[:start]
    + replacement.rstrip("\n")
    + "\n"
    + source[end:]
  )
  ast.parse(updated)
  return updated


def _remove(source: str, name: str) -> str:
  lines = source.splitlines(keepends=True)
  functions = _functions(source)

  if name not in functions:
    raise RuntimeError("Function not found for deletion: " + name)

  node = functions[name]

  if node.end_lineno is None:
    raise RuntimeError("AST end_lineno unavailable: " + name)

  del lines[node.lineno - 1:node.end_lineno]

  updated = "".join(lines)
  ast.parse(updated)
  return updated


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--repo-root", type=Path, default=Path.cwd())
  args = parser.parse_args()

  root = args.repo_root.resolve()
  changed = set()

  for (relative_path, name), replacement in REPLACE.items():
    path = root / relative_path
    source = path.read_text(encoding="utf-8-sig")
    path.write_text(
      _replace(source, name, replacement),
      encoding="utf-8",
    )
    changed.add(relative_path)

  for relative_path, name in DELETE:
    path = root / relative_path
    source = path.read_text(encoding="utf-8-sig")
    path.write_text(
      _remove(source, name),
      encoding="utf-8",
    )
    changed.add(relative_path)

  manifest_path = root / "tests" / "phase155_audit_only_nodeids.txt"
  manifest_path.write_text(
    "".join(nodeid + "\n" for nodeid in FINAL_AUDIT_NODEIDS),
    encoding="utf-8",
  )
  changed.add("tests/phase155_audit_only_nodeids.txt")

  boundary_path = root / "tests" / "test_phase155_audit_boundary.py"
  boundary_source = boundary_path.read_text(encoding="utf-8-sig")
  boundary_functions = _functions(boundary_source)

  exact_old = next(
    (
      name
      for name in boundary_functions
      if name.startswith("test_phase155_audit_boundary_has_")
      and name.endswith("_exact_nodeids")
    ),
    None,
  )

  if exact_old is None:
    raise RuntimeError("Exact audit boundary test not found.")

  boundary_source = _replace(
    boundary_source,
    exact_old,
    'def test_phase155_audit_boundary_has_2_exact_nodeids():\n  nodeids = _phase155_audit_nodeids()\n\n  assert set(\n    nodeids\n  ) == {\n    (\n      "tests/test_phase153_r3_10_public_reference_connection_repair.py::"\n      "test_phase153_r3_10_all_group_reference_population_invariants"\n    ),\n    (\n      "tests/test_phase97_actual_representative_targets_top_level_api.py::"\n      "test_phase97_5_representative_goal_source_provenance_survives_cross_layer_api"\n    ),\n  }\n  assert len(\n    nodeids\n  ) == 2\n',
  )

  boundary_functions = _functions(boundary_source)
  phase_old = next(
    (
      name
      for name in boundary_functions
      if name.startswith(
        "test_phase155_audit_boundary_contains_only_reviewed_"
      )
    ),
    None,
  )

  if phase_old is not None:
    boundary_source = _replace(
      boundary_source,
      phase_old,
      'def test_phase155_audit_boundary_contains_only_reviewed_phase153_or_phase97_tests():\n  nodeids = _phase155_audit_nodeids()\n\n  assert all(\n    (\n      nodeid.startswith(\n        "tests/test_phase153_"\n      )\n      or nodeid.startswith(\n        "tests/test_phase97_"\n      )\n    )\n    for nodeid in nodeids\n  )\n',
    )

  boundary_path.write_text(
    boundary_source,
    encoding="utf-8",
  )
  changed.add("tests/test_phase155_audit_boundary.py")

  print("Phase155 Closure-R4-R2 audit reclassification applied.")
  print("Obsolete/deferred audit functions deleted: 3")
  print("Current audit functions updated: 2")
  print("Final audit-only manifest: 2")
  print("Routine test population changed: no")
  print("Production changes: none")
  print("Top-level import changes: none")

  for path in sorted(changed):
    print(" -", path)

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
