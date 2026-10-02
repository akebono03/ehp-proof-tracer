from __future__ import annotations

import argparse
import ast
from pathlib import Path


REPLACEMENTS = {
    (
      "tests/test_phase96_proof_step_source_presentation.py",
      "test_phase96_5_actual_pi9_5_aggregate_goal_source_preserves_theorem_phase_and_branch",
    ): 'def test_phase96_5_actual_pi9_5_aggregate_goal_source_preserves_theorem_phase_and_branch():\n  from proof import (\n    ProofRule,\n    ProofStep,\n  )\n  from test_phase95_minimal_calculation_result import (\n    build_phase95_2_candidate,\n  )\n  from toda_calculation_goal import (\n    TodaCalculationGoalSource,\n  )\n  from toda_calculation_result import (\n    TodaCalculationCandidate,\n  )\n  from toda_group_query import (\n    TodaGroupQuery,\n  )\n\n  query = TodaGroupQuery(\n    n=4,\n    k=6,\n  )\n  base = build_phase95_2_candidate(\n    "phase155.phase96.result",\n    query,\n  )\n  aggregate_entry = ProofRepositoryEntry(\n    key="phase155.phase96.aggregate",\n    step=ProofStep(\n      conclusion="synthetic aggregate",\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    phase="68",\n    theorem="Toda Proposition 5.8",\n  )\n  candidate = TodaCalculationCandidate(\n    group_result=base.group_result,\n    explanation=base.explanation,\n    goal_source=TodaCalculationGoalSource(\n      source_entry=aggregate_entry,\n      branch_name="pi9_5_group_relation",\n    ),\n  )\n\n  presentation = (\n    build_toda_calculation_candidate_source_presentation(\n      candidate\n    )\n  )\n\n  assert isinstance(\n    presentation,\n    TodaCalculationCandidateSourcePresentation,\n  )\n  assert (\n    presentation.source_candidate\n    is candidate\n  )\n  assert (\n    presentation\n    .goal_source\n    .source_goal_source\n    is candidate.goal_source\n  )\n  assert (\n    presentation\n    .goal_source\n    .repository_source\n    .source_entry\n    is aggregate_entry\n  )\n  assert (\n    presentation\n    .goal_source\n    .repository_source\n    .phase\n    == "68"\n  )\n  assert (\n    presentation\n    .goal_source\n    .repository_source\n    .theorem\n    == "Toda Proposition 5.8"\n  )\n  assert (\n    presentation.goal_source.branch_name\n    == "pi9_5_group_relation"\n  )\n',
    (
      "tests/test_phase96_proof_step_source_presentation.py",
      "test_phase96_5_actual_aggregate_result_source_and_goal_source_remain_distinct",
    ): 'def test_phase96_5_actual_aggregate_result_source_and_goal_source_remain_distinct():\n  from proof import (\n    ProofRule,\n    ProofStep,\n  )\n  from test_phase95_minimal_calculation_result import (\n    build_phase95_2_candidate,\n  )\n  from toda_calculation_goal import (\n    TodaCalculationGoalSource,\n  )\n  from toda_calculation_result import (\n    TodaCalculationCandidate,\n  )\n  from toda_group_query import (\n    TodaGroupQuery,\n  )\n\n  query = TodaGroupQuery(\n    n=4,\n    k=6,\n  )\n  base = build_phase95_2_candidate(\n    "phase155.phase96.distinct.result",\n    query,\n  )\n  aggregate_entry = ProofRepositoryEntry(\n    key="phase155.phase96.distinct.aggregate",\n    step=ProofStep(\n      conclusion="synthetic aggregate",\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    phase="68",\n    theorem="Toda Proposition 5.8",\n  )\n  candidate = TodaCalculationCandidate(\n    group_result=base.group_result,\n    explanation=base.explanation,\n    goal_source=TodaCalculationGoalSource(\n      source_entry=aggregate_entry,\n      branch_name="pi9_5_group_relation",\n    ),\n  )\n\n  presentation = (\n    build_toda_calculation_candidate_source_presentation(\n      candidate\n    )\n  )\n\n  assert (\n    presentation.result_source.source_entry\n    is candidate.group_result.source_entry\n  )\n  assert (\n    presentation\n    .goal_source\n    .repository_source\n    .source_entry\n    is aggregate_entry\n  )\n  assert (\n    presentation.result_source.source_entry\n    is not presentation\n    .goal_source\n    .repository_source\n    .source_entry\n  )\n',
    (
      "tests/test_phase155_audit_boundary.py",
      "test_phase155_audit_boundary_contains_only_phase144_tests",
    ): 'def test_phase155_audit_boundary_contains_only_reviewed_phase144_or_phase153_tests():\n  nodeids = _phase155_audit_nodeids()\n\n  assert all(\n    (\n      nodeid.startswith(\n        "tests/test_phase144_"\n      )\n      or nodeid.startswith(\n        "tests/test_phase153_"\n      )\n    )\n    for nodeid in nodeids\n  )\n',
}


def _functions(source):
  tree = ast.parse(source)
  return {
    node.name: node
    for node in tree.body
    if isinstance(node, ast.FunctionDef)
  }


def _replace(source, name, replacement):
  lines = source.splitlines(keepends=True)
  functions = _functions(source)

  if name not in functions:
    raise RuntimeError(
      "Function not found: "
      + name
    )

  node = functions[name]

  if node.end_lineno is None:
    raise RuntimeError(
      "AST end_lineno unavailable: "
      + name
    )

  start = sum(
    len(line)
    for line in lines[:node.lineno - 1]
  )
  end = sum(
    len(line)
    for line in lines[:node.end_lineno]
  )

  updated = (
    source[:start]
    + replacement.rstrip("\n")
    + "\n"
    + source[end:]
  )

  ast.parse(updated)
  return updated


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()

  manifest_path = (
    repo_root
    / "tests"
    / "phase155_audit_only_nodeids.txt"
  )

  expected = {
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

  current = {
    line.strip()
    for line in manifest_path.read_text(
      encoding="utf-8"
    ).splitlines()
    if line.strip()
  }

  if current != expected:
    raise SystemExit(
      "Audit-only manifest differs from expected R2C-R3 three-nodeid boundary."
    )

  changed = set()

  for (
    relative_path,
    function_name,
  ), replacement in REPLACEMENTS.items():
    path = repo_root / relative_path
    source = path.read_text(
      encoding="utf-8-sig"
    )
    updated = _replace(
      source,
      function_name,
      replacement,
    )
    path.write_text(
      updated,
      encoding="utf-8",
    )
    changed.add(
      relative_path
    )

  print(
    "Phase 155 Closure-R2C-R3-R1 repair applied."
  )
  print(
    "Changed test functions:",
    len(REPLACEMENTS),
  )
  print(
    "Audit-only manifest changes: none"
  )
  print(
    "Production changes: none"
  )
  print(
    "Top-level import changes: none"
  )
  print(
    "Changed repository files:",
    len(changed),
  )
  for path in sorted(changed):
    print(
      " -",
      path,
    )


if __name__ == "__main__":
  main()
