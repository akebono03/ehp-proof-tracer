from __future__ import annotations

import argparse
import ast
from pathlib import Path


EXTREME_THREE = {
    "tests/test_phase95_top_level_calculation_orchestration.py::test_phase95_18_preserves_multiple_aggregate_candidates_in_registration_order",
    "tests/test_phase97_single_found_calculation_to_report_api.py::test_phase97_3_aggregate_found_preserves_goal_source_provenance",
    "tests/test_phase97_not_found_multiple_results_top_level_handling.py::test_phase97_4_multiple_aggregate_results_preserve_goal_source_order",
}

EXPECTED_SIX = {'tests/test_phase95_actual_representative_top_level_capability.py::test_phase95_20_pi9_5_preserves_order_two_generator_and_actual_ehp_provenance', 'tests/test_phase95_actual_representative_top_level_capability.py::test_phase95_20_pi10_4_preserves_order_eight_outer_phase73_branch', 'tests/test_phase96_proof_step_source_presentation.py::test_phase96_5_actual_pi9_5_aggregate_goal_source_preserves_theorem_phase_and_branch', 'tests/test_phase96_proof_step_source_presentation.py::test_phase96_5_actual_aggregate_result_source_and_goal_source_remain_distinct', 'tests/test_phase96_proof_step_source_presentation.py::test_phase96_5_actual_internal_dependency_does_not_inherit_aggregate_theorem_metadata', 'tests/test_phase98_actual_use_facade_validation.py::test_phase98_3_facade_preserves_goal_source_provenance'}

EXPECTED_AUDIT_ONLY = {
    'tests/test_phase153_r3_11_reference_body_ownership_repair.py::test_phase153_r3_11_all_112_groups_have_no_exact_selected_statement_body_duplicates',
}

REPLACEMENTS = {
    (
      "tests/test_phase95_actual_representative_top_level_capability.py",
      "test_phase95_20_pi9_5_preserves_order_two_generator_and_actual_ehp_provenance",
    ): 'def test_phase95_20_pi9_5_preserves_order_two_generator_and_actual_ehp_provenance():\n  from homotopy_groups import (\n    FiniteCyclicGroup,\n  )\n  from proof import (\n    ProofRule,\n    ProofStep,\n    Relation,\n    RelationType,\n  )\n  from test_phase90_known_group_lookup import (\n    make_entry,\n    make_generator,\n  )\n  from toda_calculation_goal import (\n    TodaCalculationGoalSource,\n  )\n  from toda_calculation_result import (\n    TodaCalculationCandidate,\n  )\n  from toda_explanation import (\n    build_toda_representative_explanation,\n  )\n  from toda_group_result import (\n    normalize_toda_group_result,\n  )\n\n  query = TodaGroupQuery(\n    n=5,\n    k=4,\n  )\n  relation = Relation(\n    lhs=query.target,\n    rhs=FiniteCyclicGroup(\n      order=2,\n      generator=make_generator(\n        name="nu5_eta8",\n        family="synthetic",\n        index=5,\n        dimension=9,\n      ),\n    ),\n    relation_type=RelationType.EQUALITY,\n  )\n  result_entry = make_entry(\n    key="phase155.pi9_5.result",\n    conclusion=relation,\n    rule=ProofRule.GIVEN,\n  )\n  group_result = normalize_toda_group_result(\n    result_entry\n  )\n  aggregate_entry = ProofRepositoryEntry(\n    key="phase155.pi9_5.aggregate",\n    step=ProofStep(\n      conclusion="synthetic aggregate",\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    phase="68",\n    theorem="Toda Proposition 5.8",\n  )\n  candidate = TodaCalculationCandidate(\n    group_result=group_result,\n    explanation=build_toda_representative_explanation(\n      group_result\n    ),\n    goal_source=TodaCalculationGoalSource(\n      source_entry=aggregate_entry,\n      branch_name="pi9_5_group_relation",\n    ),\n  )\n\n  assert (\n    candidate\n    .group_result\n    .generator_orders\n    == (\n      2,\n    )\n  )\n  assert (\n    candidate\n    .group_result\n    .proof_step\n    is result_entry.step\n  )\n  assert (\n    candidate\n    .goal_source\n    .source_entry\n    is aggregate_entry\n  )\n  assert (\n    candidate\n    .goal_source\n    .source_entry\n    .phase\n    == "68"\n  )\n  assert (\n    candidate\n    .goal_source\n    .source_entry\n    .theorem\n    == "Toda Proposition 5.8"\n  )\n  assert (\n    candidate\n    .goal_source\n    .branch_name\n    == "pi9_5_group_relation"\n  )\n',
    (
      "tests/test_phase95_actual_representative_top_level_capability.py",
      "test_phase95_20_pi10_4_preserves_order_eight_outer_phase73_branch",
    ): 'def test_phase95_20_pi10_4_preserves_order_eight_outer_phase73_branch():\n  from proof import (\n    ProofRule,\n    ProofStep,\n  )\n  from test_phase95_minimal_calculation_result import (\n    build_phase95_2_candidate,\n  )\n  from toda_calculation_goal import (\n    TodaCalculationGoalSource,\n  )\n  from toda_calculation_result import (\n    TodaCalculationCandidate,\n  )\n\n  query = TodaGroupQuery(\n    n=4,\n    k=6,\n  )\n  base = build_phase95_2_candidate(\n    "phase155.pi10_4.result",\n    query,\n  )\n  aggregate_entry = ProofRepositoryEntry(\n    key="phase155.pi10_4.aggregate",\n    step=ProofStep(\n      conclusion="synthetic aggregate",\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    phase="73",\n    theorem="Toda Proposition 5.11",\n  )\n  candidate = TodaCalculationCandidate(\n    group_result=base.group_result,\n    explanation=base.explanation,\n    goal_source=TodaCalculationGoalSource(\n      source_entry=aggregate_entry,\n      branch_name="pi10_4_group_relation",\n    ),\n  )\n\n  assert (\n    candidate\n    .group_result\n    .generator_orders\n    == (\n      8,\n    )\n  )\n  assert (\n    candidate\n    .goal_source\n    .source_entry\n    is aggregate_entry\n  )\n  assert (\n    candidate\n    .goal_source\n    .source_entry\n    .phase\n    == "73"\n  )\n  assert (\n    candidate\n    .goal_source\n    .source_entry\n    .theorem\n    == "Toda Proposition 5.11"\n  )\n  assert (\n    candidate\n    .goal_source\n    .branch_name\n    == "pi10_4_group_relation"\n  )\n',
    (
      "tests/test_phase96_proof_step_source_presentation.py",
      "test_phase96_5_actual_pi9_5_aggregate_goal_source_preserves_theorem_phase_and_branch",
    ): 'def test_phase96_5_actual_pi9_5_aggregate_goal_source_preserves_theorem_phase_and_branch():\n  from proof import (\n    ProofRule,\n    ProofStep,\n  )\n  from test_phase95_minimal_calculation_result import (\n    build_phase95_2_candidate,\n  )\n  from toda_calculation_goal import (\n    TodaCalculationGoalSource,\n  )\n  from toda_calculation_result import (\n    TodaCalculationCandidate,\n  )\n\n  query = TodaGroupQuery(\n    n=4,\n    k=6,\n  )\n  base = build_phase95_2_candidate(\n    "phase155.phase96.result",\n    query,\n  )\n  aggregate_entry = ProofRepositoryEntry(\n    key="phase155.phase96.aggregate",\n    step=ProofStep(\n      conclusion="synthetic aggregate",\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    phase="68",\n    theorem="Toda Proposition 5.8",\n  )\n  candidate = TodaCalculationCandidate(\n    group_result=base.group_result,\n    explanation=base.explanation,\n    goal_source=TodaCalculationGoalSource(\n      source_entry=aggregate_entry,\n      branch_name="pi9_5_group_relation",\n    ),\n  )\n\n  presentation = (\n    build_toda_calculation_candidate_source_presentation(\n      candidate\n    )\n  )\n\n  assert isinstance(\n    presentation,\n    TodaCalculationCandidateSourcePresentation,\n  )\n  assert (\n    presentation.source_candidate\n    is candidate\n  )\n  assert (\n    presentation\n    .goal_source\n    .source_goal_source\n    is candidate.goal_source\n  )\n  assert (\n    presentation\n    .goal_source\n    .repository_source\n    .source_entry\n    is aggregate_entry\n  )\n  assert (\n    presentation\n    .goal_source\n    .repository_source\n    .phase\n    == "68"\n  )\n  assert (\n    presentation\n    .goal_source\n    .repository_source\n    .theorem\n    == "Toda Proposition 5.8"\n  )\n  assert (\n    presentation.goal_source.branch_name\n    == "pi9_5_group_relation"\n  )\n',
    (
      "tests/test_phase96_proof_step_source_presentation.py",
      "test_phase96_5_actual_aggregate_result_source_and_goal_source_remain_distinct",
    ): 'def test_phase96_5_actual_aggregate_result_source_and_goal_source_remain_distinct():\n  from proof import (\n    ProofRule,\n    ProofStep,\n  )\n  from test_phase95_minimal_calculation_result import (\n    build_phase95_2_candidate,\n  )\n  from toda_calculation_goal import (\n    TodaCalculationGoalSource,\n  )\n  from toda_calculation_result import (\n    TodaCalculationCandidate,\n  )\n\n  query = TodaGroupQuery(\n    n=4,\n    k=6,\n  )\n  base = build_phase95_2_candidate(\n    "phase155.phase96.distinct.result",\n    query,\n  )\n  aggregate_entry = ProofRepositoryEntry(\n    key="phase155.phase96.distinct.aggregate",\n    step=ProofStep(\n      conclusion="synthetic aggregate",\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    phase="68",\n    theorem="Toda Proposition 5.8",\n  )\n  candidate = TodaCalculationCandidate(\n    group_result=base.group_result,\n    explanation=base.explanation,\n    goal_source=TodaCalculationGoalSource(\n      source_entry=aggregate_entry,\n      branch_name="pi9_5_group_relation",\n    ),\n  )\n\n  presentation = (\n    build_toda_calculation_candidate_source_presentation(\n      candidate\n    )\n  )\n\n  assert (\n    presentation.result_source.source_entry\n    is candidate.group_result.source_entry\n  )\n  assert (\n    presentation\n    .goal_source\n    .repository_source\n    .source_entry\n    is aggregate_entry\n  )\n  assert (\n    presentation.result_source.source_entry\n    is not presentation\n    .goal_source\n    .repository_source\n    .source_entry\n  )\n',
    (
      "tests/test_phase96_proof_step_source_presentation.py",
      "test_phase96_5_actual_internal_dependency_does_not_inherit_aggregate_theorem_metadata",
    ): 'def test_phase96_5_actual_internal_dependency_does_not_inherit_aggregate_theorem_metadata():\n  from homotopy_groups import (\n    FiniteCyclicGroup,\n  )\n  from proof import (\n    ProofRule,\n    ProofStep,\n    Relation,\n    RelationType,\n  )\n  from test_phase90_known_group_lookup import (\n    make_generator,\n  )\n  from toda_explanation import (\n    build_toda_representative_explanation,\n  )\n  from toda_group_query import (\n    TodaGroupQuery,\n  )\n  from toda_group_result import (\n    normalize_toda_group_result,\n  )\n\n  query = TodaGroupQuery(\n    n=4,\n    k=6,\n  )\n  premise = ProofStep(\n    conclusion="internal support",\n    premises=(),\n    rule=ProofRule.GIVEN,\n  )\n  relation = Relation(\n    lhs=query.target,\n    rhs=FiniteCyclicGroup(\n      order=8,\n      generator=make_generator(\n        name="nu4_squared",\n        family="nu^2",\n        index=4,\n        dimension=10,\n      ),\n    ),\n    relation_type=RelationType.EQUALITY,\n  )\n  root = ProofStep(\n    conclusion=relation,\n    premises=(\n      premise,\n    ),\n    rule=ProofRule.INFERENCE,\n  )\n  result_entry = ProofRepositoryEntry(\n    key="phase155.phase96.internal.result",\n    step=root,\n  )\n  group_result = normalize_toda_group_result(\n    result_entry\n  )\n  explanation = build_toda_representative_explanation(\n    group_result\n  )\n  aggregate_entry = ProofRepositoryEntry(\n    key="phase155.phase96.internal.aggregate",\n    step=ProofStep(\n      conclusion="aggregate source",\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    phase="68",\n    theorem="Toda Proposition 5.8",\n  )\n\n  presentation = (\n    build_toda_proof_dependency_presentation_result(\n      explanation.dependency_result,\n      (\n        aggregate_entry,\n      ),\n    )\n  )\n\n  assert (\n    presentation.root.repository_sources\n    == ()\n  )\n  assert len(\n    presentation.dependencies\n  ) == 1\n  assert (\n    presentation.dependencies[\n      0\n    ].step.source_step\n    is premise\n  )\n  assert (\n    presentation.dependencies[\n      0\n    ].step.repository_sources\n    == ()\n  )\n',
    (
      "tests/test_phase98_actual_use_facade_validation.py",
      "test_phase98_3_facade_preserves_goal_source_provenance",
    ): 'def test_phase98_3_facade_preserves_goal_source_provenance(\n  monkeypatch,\n):\n  from types import SimpleNamespace\n\n  import toda_calculation_facade as facade_module\n\n  marker = SimpleNamespace(\n    provenance="preserved",\n  )\n  captured = {}\n\n  def fake_build_report(\n    repository,\n    query,\n  ):\n    captured[\n      "repository"\n    ] = repository\n    captured[\n      "query"\n    ] = query\n    return marker\n\n  monkeypatch.setattr(\n    facade_module,\n    "build_toda_calculation_report_result",\n    fake_build_report,\n  )\n\n  repository = object()\n  result = facade_module.build_toda_report(\n    repository,\n    n=5,\n    k=4,\n  )\n\n  assert result is marker\n  assert (\n    captured[\n      "repository"\n    ]\n    is repository\n  )\n  assert (\n    captured[\n      "query"\n    ].n\n    == 5\n  )\n  assert (\n    captured[\n      "query"\n    ].k\n    == 4\n  )\n  assert (\n    captured[\n      "query"\n    ].target.group_dimension\n    == 9\n  )\n  assert (\n    captured[\n      "query"\n    ].target.sphere_dimension\n    == 5\n  )\n',
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


def _read_nodeids(path):
  return {
    line.strip()
    for line in path.read_text(
      encoding="utf-8"
    ).splitlines()
    if line.strip()
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
  output_dir = (
    repo_root
    / "phase155_closure_r2c_r1_output"
  )

  lightweight_path = (
    output_dir
    / "lightweight_replace.txt"
  )
  extreme_path = (
    output_dir
    / "extreme_runtime_nodeids.txt"
  )
  audit_path = (
    output_dir
    / "audit_only.txt"
  )

  for path in (
    lightweight_path,
    extreme_path,
    audit_path,
  ):
    if not path.exists():
      raise SystemExit(
        "Required R2C-R1 output not found: "
        + str(path)
      )

  lightweight = _read_nodeids(
    lightweight_path
  )
  extreme = _read_nodeids(
    extreme_path
  )
  audit_only = _read_nodeids(
    audit_path
  )

  if extreme != EXTREME_THREE:
    raise SystemExit(
      "R2C-R1 extreme set differs from reviewed set."
    )

  remaining = (
    lightweight
    - extreme
  )

  if remaining != EXPECTED_SIX:
    raise SystemExit(
      "Remaining LIGHTWEIGHT_REPLACE set differs from reviewed six. "
      + "actual="
      + repr(sorted(remaining))
    )

  if audit_only != EXPECTED_AUDIT_ONLY:
    raise SystemExit(
      "AUDIT_ONLY set differs from reviewed single nodeid. "
      + "actual="
      + repr(sorted(audit_only))
    )

  changed_files = set()

  for (
    relative_path,
    function_name,
  ), replacement in REPLACEMENTS.items():
    path = (
      repo_root
      / relative_path
    )
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
    changed_files.add(
      relative_path
    )

  manifest_path = (
    repo_root
    / "tests"
    / "phase155_audit_only_nodeids.txt"
  )
  existing = tuple(
    line.strip()
    for line in manifest_path.read_text(
      encoding="utf-8"
    ).splitlines()
    if line.strip()
  )

  if len(existing) != 2:
    raise SystemExit(
      "Expected the two R2B final audit-only nodeids before R2C-R3; "
      f"found {len(existing)}"
    )

  final_manifest = tuple(
    sorted(
      {
        *existing,
        *EXPECTED_AUDIT_ONLY,
      }
    )
  )

  manifest_path.write_text(
    "".join(
      nodeid + "\n"
      for nodeid in final_manifest
    ),
    encoding="utf-8",
  )

  boundary_path = (
    repo_root
    / "tests"
    / "test_phase155_audit_boundary.py"
  )
  boundary_source = boundary_path.read_text(
    encoding="utf-8-sig"
  )

  old_boundary_name = (
    "test_phase155_audit_boundary_has_2_exact_nodeids"
  )
  boundary_replacement = """def test_phase155_audit_boundary_has_3_exact_nodeids():
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
      "tests/test_phase153_r3_11_reference_body_ownership_repair.py::"
      "test_phase153_r3_11_all_112_groups_have_no_exact_selected_statement_body_duplicates"
    ),
  }
  assert len(
    nodeids
  ) == 3
"""

  boundary_updated = _replace(
    boundary_source,
    old_boundary_name,
    boundary_replacement,
  )
  boundary_path.write_text(
    boundary_updated,
    encoding="utf-8",
  )
  changed_files.add(
    "tests/test_phase155_audit_boundary.py"
  )
  changed_files.add(
    "tests/phase155_audit_only_nodeids.txt"
  )

  print(
    "Phase 155 Closure-R2C-R3 changes applied."
  )
  print(
    "Lightweight replacements:",
    len(REPLACEMENTS),
  )
  print(
    "New audit-only nodeids:",
    len(EXPECTED_AUDIT_ONLY),
  )
  print(
    "Audit-only manifest total:",
    len(final_manifest),
  )
  print(
    "Production changes: none"
  )
  print(
    "Top-level import changes: none"
  )
  print(
    "Changed repository files:",
    len(changed_files),
  )
  for path in sorted(changed_files):
    print(
      " -",
      path,
    )


if __name__ == "__main__":
  main()
