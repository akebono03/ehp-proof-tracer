from __future__ import annotations

import argparse
import ast
from pathlib import Path


REPLACEMENTS = {
    (
        "tests/test_phase95_top_level_calculation_orchestration.py",
        "test_phase95_18_preserves_multiple_aggregate_candidates_in_registration_order",
    ): 'def test_phase95_18_preserves_multiple_aggregate_candidates_in_registration_order(\n  monkeypatch,\n):\n  from types import SimpleNamespace\n\n  import toda_calculation as calculation_module\n  import toda_calculation_goal_discovery as discovery_module\n  from test_phase95_minimal_calculation_result import (\n    build_phase95_2_candidate,\n  )\n  from toda_calculation_goal import (\n    TodaCalculationGoalCandidate,\n    TodaCalculationGoalSource,\n  )\n  from toda_calculation_result import (\n    TodaCalculationResult,\n  )\n\n  query = TodaGroupQuery(\n    n=4,\n    k=6,\n  )\n\n  first_base = build_phase95_2_candidate(\n    "phase155.extreme.first",\n    query,\n  )\n  second_base = build_phase95_2_candidate(\n    "phase155.extreme.second",\n    query,\n  )\n\n  first_entry = (\n    first_base\n    .group_result\n    .source_entry\n  )\n  second_entry = (\n    second_base\n    .group_result\n    .source_entry\n  )\n\n  repository = ProofRepository()\n  repository.register(\n    first_entry\n  )\n  repository.register(\n    second_entry\n  )\n\n  first_source = TodaCalculationGoalSource(\n    source_entry=first_entry,\n    branch_name="synthetic_first",\n  )\n  second_source = TodaCalculationGoalSource(\n    source_entry=second_entry,\n    branch_name="synthetic_second",\n  )\n\n  goal_by_entry = {\n    id(\n      first_entry\n    ): TodaCalculationGoalCandidate(\n      target=query.target,\n      goal=(\n        first_base\n        .group_result\n        .proof_step\n        .conclusion\n      ),\n      source=first_source,\n    ),\n    id(\n      second_entry\n    ): TodaCalculationGoalCandidate(\n      target=query.target,\n      goal=(\n        second_base\n        .group_result\n        .proof_step\n        .conclusion\n      ),\n      source=second_source,\n    ),\n  }\n\n  def extract_one(\n    entry,\n    actual_query,\n  ):\n    assert actual_query is query\n    return (\n      goal_by_entry[\n        id(\n          entry\n        )\n      ],\n    )\n\n  monkeypatch.setattr(\n    discovery_module,\n    "extract_concrete_toda_calculation_goal_candidates",\n    extract_one,\n  )\n\n  discovery = (\n    discovery_module\n    .discover_concrete_toda_calculation_goal_candidates(\n      repository,\n      query,\n    )\n  )\n\n  assert tuple(\n    candidate.source.source_entry\n    for candidate in discovery.candidates\n  ) == (\n    first_entry,\n    second_entry,\n  )\n\n  monkeypatch.setattr(\n    calculation_module,\n    "build_known_toda_calculation_result",\n    lambda actual_repository, actual_query: (\n      TodaCalculationResult(\n        query=actual_query,\n        candidates=(),\n      )\n    ),\n  )\n  monkeypatch.setattr(\n    calculation_module,\n    "discover_concrete_toda_calculation_goal_candidates",\n    lambda actual_repository, actual_query: discovery,\n  )\n\n  result_by_source_entry_id = {\n    id(\n      first_entry\n    ): (\n      first_base\n      .group_result\n    ),\n    id(\n      second_entry\n    ): (\n      second_base\n      .group_result\n    ),\n  }\n\n  def normalize_one(\n    goal_candidate,\n  ):\n    return (\n      result_by_source_entry_id[\n        id(\n          goal_candidate\n          .source\n          .source_entry\n        )\n      ],\n    )\n\n  monkeypatch.setattr(\n    calculation_module,\n    "normalize_recovered_toda_calculation_goal_candidate",\n    normalize_one,\n  )\n\n  result = (\n    calculation_module\n    .build_toda_calculation_result(\n      repository,\n      query,\n    )\n  )\n\n  assert (\n    result.status\n    is TodaCalculationStatus.MULTIPLE_RESULTS\n  )\n  assert tuple(\n    candidate.goal_source.source_entry\n    for candidate in result.candidates\n  ) == (\n    first_entry,\n    second_entry,\n  )\n  assert tuple(\n    candidate.group_result\n    for candidate in result.candidates\n  ) == (\n    first_base.group_result,\n    second_base.group_result,\n  )\n',
    (
        "tests/test_phase97_single_found_calculation_to_report_api.py",
        "test_phase97_3_aggregate_found_preserves_goal_source_provenance",
    ): 'def test_phase97_3_aggregate_found_preserves_goal_source_provenance(\n  monkeypatch,\n):\n  import toda_calculation_report as report_module\n  from test_phase95_minimal_calculation_result import (\n    build_phase95_2_candidate,\n  )\n  from toda_calculation_goal import (\n    TodaCalculationGoalSource,\n  )\n  from toda_calculation_result import (\n    TodaCalculationCandidate,\n    TodaCalculationResult,\n  )\n\n  query = TodaGroupQuery(\n    n=4,\n    k=6,\n  )\n  base = build_phase95_2_candidate(\n    "phase155.report.provenance",\n    query,\n  )\n  source_entry = (\n    base\n    .group_result\n    .source_entry\n  )\n  goal_source = TodaCalculationGoalSource(\n    source_entry=source_entry,\n    branch_name="synthetic_branch",\n  )\n  candidate = TodaCalculationCandidate(\n    group_result=base.group_result,\n    explanation=base.explanation,\n    goal_source=goal_source,\n  )\n  calculation_result = TodaCalculationResult(\n    query=query,\n    candidates=(\n      candidate,\n    ),\n  )\n\n  monkeypatch.setattr(\n    report_module,\n    "build_toda_calculation_result",\n    lambda repository, actual_query: calculation_result,\n  )\n\n  result = (\n    report_module\n    .build_toda_found_calculation_report_result(\n      ProofRepository(),\n      query,\n    )\n  )\n\n  source_candidate = (\n    result.candidates[\n      0\n    ].source_candidate\n  )\n\n  assert (\n    source_candidate\n    is candidate\n  )\n  assert (\n    source_candidate.goal_source\n    is goal_source\n  )\n  assert (\n    source_candidate\n    .goal_source\n    .source_entry\n    is source_entry\n  )\n  assert (\n    source_candidate\n    .goal_source\n    .branch_name\n    == "synthetic_branch"\n  )\n\n  source_presentation = (\n    result.candidates[\n      0\n    ].presentation.source\n  )\n\n  assert (\n    source_presentation\n    .goal_source\n    .source_goal_source\n    is goal_source\n  )\n  assert (\n    source_presentation\n    .goal_source\n    .repository_source\n    .source_entry\n    is source_entry\n  )\n  assert (\n    source_presentation\n    .goal_source\n    .branch_name\n    == "synthetic_branch"\n  )\n',
    (
        "tests/test_phase97_not_found_multiple_results_top_level_handling.py",
        "test_phase97_4_multiple_aggregate_results_preserve_goal_source_order",
    ): 'def test_phase97_4_multiple_aggregate_results_preserve_goal_source_order(\n  monkeypatch,\n):\n  import toda_calculation_report as report_module\n  from test_phase95_minimal_calculation_result import (\n    build_phase95_2_candidate,\n  )\n  from toda_calculation_goal import (\n    TodaCalculationGoalSource,\n  )\n  from toda_calculation_result import (\n    TodaCalculationCandidate,\n    TodaCalculationResult,\n  )\n\n  query = TodaGroupQuery(\n    n=4,\n    k=6,\n  )\n\n  first_base = build_phase95_2_candidate(\n    "phase155.report.first",\n    query,\n  )\n  second_base = build_phase95_2_candidate(\n    "phase155.report.second",\n    query,\n  )\n\n  first_entry = (\n    first_base\n    .group_result\n    .source_entry\n  )\n  second_entry = (\n    second_base\n    .group_result\n    .source_entry\n  )\n\n  first_goal_source = (\n    TodaCalculationGoalSource(\n      source_entry=first_entry,\n      branch_name="synthetic_first",\n    )\n  )\n  second_goal_source = (\n    TodaCalculationGoalSource(\n      source_entry=second_entry,\n      branch_name="synthetic_second",\n    )\n  )\n\n  first = TodaCalculationCandidate(\n    group_result=first_base.group_result,\n    explanation=first_base.explanation,\n    goal_source=first_goal_source,\n  )\n  second = TodaCalculationCandidate(\n    group_result=second_base.group_result,\n    explanation=second_base.explanation,\n    goal_source=second_goal_source,\n  )\n\n  calculation_result = TodaCalculationResult(\n    query=query,\n    candidates=(\n      first,\n      second,\n    ),\n  )\n\n  monkeypatch.setattr(\n    report_module,\n    "build_toda_calculation_result",\n    lambda repository, actual_query: calculation_result,\n  )\n\n  result = (\n    report_module\n    .build_toda_calculation_report_result(\n      ProofRepository(),\n      query,\n    )\n  )\n\n  assert (\n    result.status\n    is TodaCalculationStatus.MULTIPLE_RESULTS\n  )\n  assert tuple(\n    report_candidate.source_candidate\n    for report_candidate in result.candidates\n  ) == (\n    first,\n    second,\n  )\n  assert tuple(\n    report_candidate\n    .source_candidate\n    .goal_source\n    .source_entry\n    for report_candidate in result.candidates\n  ) == (\n    first_entry,\n    second_entry,\n  )\n  assert tuple(\n    report_candidate\n    .presentation\n    .source\n    .goal_source\n    .repository_source\n    .source_entry\n    for report_candidate in result.candidates\n  ) == (\n    first_entry,\n    second_entry,\n  )\n',
}


def _functions(
    source: str,
) -> dict[str, ast.FunctionDef]:
    tree = ast.parse(
        source
    )

    return {
        node.name: node
        for node in tree.body
        if isinstance(
            node,
            ast.FunctionDef,
        )
    }


def _replace_function(
    source: str,
    function_name: str,
    replacement: str,
) -> str:
    lines = source.splitlines(
        keepends=True
    )
    functions = _functions(
        source
    )

    if function_name not in functions:
        raise RuntimeError(
            "Function not found: "
            + function_name
        )

    node = functions[
        function_name
    ]

    if node.end_lineno is None:
        raise RuntimeError(
            "AST end_lineno unavailable: "
            + function_name
        )

    start = sum(
        len(
            line
        )
        for line in lines[
            : node.lineno - 1
        ]
    )
    end = sum(
        len(
            line
        )
        for line in lines[
            : node.end_lineno
        ]
    )

    updated = (
        source[
            :start
        ]
        + replacement.rstrip(
            "\n"
        )
        + "\n"
        + source[
            end:
        ]
    )

    ast.parse(
        updated
    )

    return updated


def main() -> int:
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
        / "phase155_closure_r2c_r1_output"
        / "extreme_runtime_nodeids.txt"
    )

    if not manifest_path.exists():
        raise SystemExit(
            "R2C-R1 extreme manifest not found: "
            + str(
                manifest_path
            )
        )

    extreme_nodeids = {
        line.strip()
        for line in manifest_path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    }

    expected_nodeids = {
        (
            relative_path
            + "::"
            + function_name
        )
        for (
            relative_path,
            function_name,
        ) in REPLACEMENTS
    }

    if extreme_nodeids != expected_nodeids:
        raise SystemExit(
            "R2C-R1 extreme set differs from reviewed R2C-R2 set."
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
        updated = _replace_function(
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

    print(
        "Phase 155 Closure-R2C-R2 extreme replacements applied."
    )
    print(
        "Replaced extreme tests:",
        len(
            REPLACEMENTS
        ),
    )
    print(
        "Changed repository files:",
        len(
            changed_files
        ),
    )
    for relative_path in sorted(
        changed_files
    ):
        print(
            " -",
            relative_path,
        )
    print(
        "Production changes: none"
    )
    print(
        "Top-level import block changes: none"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
