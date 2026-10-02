from __future__ import annotations

import argparse
import ast
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


EXPECTED_KEEP_ROUTINE = {
  "tests/test_phase153_r2_public_reference_semantic_fact.py::test_phase153_r2_public_pi10_6_excludes_obsolete_45_reference",
  "tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_selected_statements_are_publicly_visible",
  "tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_public_reference_markers_cover_structured_entries",
  "tests/test_phase153_r3_4_reference_statement_rendering_connection.py::test_phase153_r3_4_public_pi10_6_reference_section_excludes_obsolete_45",
  "tests/test_phase153_r3_5_reference_body_duplicate_suppression.py::test_phase153_r3_5_public_pi10_6_keeps_current_reference_baseline_without_obsolete_45",
  "tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py::test_phase153_r3_9_all_reference_entries_have_selected_statement",
  "tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_integrates_calculation_source_metadata",
  "tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_result_source_and_goal_source_remain_distinct",
  "tests/test_phase96_full_proof_report_renderer.py::test_phase96_11_actual_pi9_5_full_report_contains_source_metadata",
  "tests/test_phase96_human_readable_renderer.py::test_phase96_9_actual_pi9_5_markdown_contains_result_source_and_ehp",
  "tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_representative_goal_sources_preserve_theorem_phase_and_branch",
  "tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_all_representative_results_keep_result_and_goal_sources_distinct",
  "tests/test_phase97_actual_representative_targets_top_level_api.py::test_phase97_5_representative_goal_source_provenance_survives_top_level_api",
  "tests/test_phase98_representative_convenience_validation.py::test_phase98_6_shortest_path_preserves_goal_source_provenance",
}


CLASSIFICATION = {
  "tests/test_phase153_r2_public_reference_semantic_fact.py::test_phase153_r2_public_pi10_6_excludes_obsolete_45_reference": (
    "DELETE_CANDIDATE",
    "The same pi10^6 public Reference baseline is checked again by Phase153 R3-4 and R3-5. R2 is an older integration checkpoint.",
    "phase153_pi10_6_reference_baseline",
  ),
  "tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_all_selected_statements_are_publicly_visible": (
    "MERGE_CANDIDATE",
    "This performs the same 112-group traversal as the marker-coverage and selected-statement audits. Keep the visibility invariant, but merge it into one population audit.",
    "phase153_all_group_reference_population",
  ),
  "tests/test_phase153_r3_10_public_reference_connection_repair.py::test_phase153_r3_10_public_reference_markers_cover_structured_entries": (
    "MERGE_CANDIDATE",
    "This shares the same 112-group build/replay/render traversal with the selected-statement visibility audit. The marker invariant is distinct but should share one audit pass.",
    "phase153_all_group_reference_population",
  ),
  "tests/test_phase153_r3_4_reference_statement_rendering_connection.py::test_phase153_r3_4_public_pi10_6_reference_section_excludes_obsolete_45": (
    "KEEP",
    "This is the focused current public-rendering contract for pi10^6 after structured Reference statement connection.",
    "phase153_pi10_6_reference_baseline",
  ),
  "tests/test_phase153_r3_5_reference_body_duplicate_suppression.py::test_phase153_r3_5_public_pi10_6_keeps_current_reference_baseline_without_obsolete_45": (
    "DELETE_CANDIDATE",
    "The file already has focused suppression-unit tests, while this integration assertion repeats the same pi10^6 Reference baseline retained in R3-4.",
    "phase153_pi10_6_reference_baseline",
  ),
  "tests/test_phase153_r3_9_remaining_reference_renderer_coverage.py::test_phase153_r3_9_all_reference_entries_have_selected_statement": (
    "MERGE_CANDIDATE",
    "The structured selected-statement invariant is useful, but it repeats the same 112-group traversal used by R3-10. Merge it into the single Reference population audit.",
    "phase153_all_group_reference_population",
  ),
  "tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_integrates_calculation_source_metadata": (
    "DELETE_CANDIDATE",
    "R2C-R3 now has a lightweight direct source-presentation metadata contract. Rebuilding the actual pi9^5 end-to-end fixture for the same metadata adds no layer-specific assertion.",
    "source_metadata_provenance",
  ),
  "tests/test_phase96_actual_pi9_5_end_to_end_presentation.py::test_phase96_7_actual_pi9_5_result_source_and_goal_source_remain_distinct": (
    "DELETE_CANDIDATE",
    "R2C-R3 now checks result-source/goal-source distinction directly with a lightweight source-presentation test.",
    "result_goal_source_distinction",
  ),
  "tests/test_phase96_full_proof_report_renderer.py::test_phase96_11_actual_pi9_5_full_report_contains_source_metadata": (
    "KEEP",
    "This protects the final full-report text surface. Lower-level provenance tests cannot replace a renderer-output contract.",
    "rendered_source_metadata",
  ),
  "tests/test_phase96_human_readable_renderer.py::test_phase96_9_actual_pi9_5_markdown_contains_result_source_and_ehp": (
    "KEEP",
    "This protects the human-readable Markdown surface, including source/EHP presentation. It is a distinct renderer boundary.",
    "rendered_source_metadata",
  ),
  "tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_representative_goal_sources_preserve_theorem_phase_and_branch": (
    "MERGE_CANDIDATE",
    "The six-target provenance matrix overlaps the Phase97 top-level provenance matrix. One representative cross-layer integration audit is sufficient after lightweight source contracts were added.",
    "representative_provenance_matrix",
  ),
  "tests/test_phase96_representative_targets_end_to_end_presentation.py::test_phase96_8_all_representative_results_keep_result_and_goal_sources_distinct": (
    "DELETE_CANDIDATE",
    "The result/goal-source distinction is now covered directly by the lightweight Phase96 contract; repeating it across six heavy representative fixtures is redundant.",
    "result_goal_source_distinction",
  ),
  "tests/test_phase97_actual_representative_targets_top_level_api.py::test_phase97_5_representative_goal_source_provenance_survives_top_level_api": (
    "MERGE_CANDIDATE",
    "This is valuable cross-layer coverage, but it overlaps the Phase96 six-target provenance matrix. Preserve one merged representative integration audit rather than both.",
    "representative_provenance_matrix",
  ),
  "tests/test_phase98_representative_convenience_validation.py::test_phase98_6_shortest_path_preserves_goal_source_provenance": (
    "DELETE_CANDIDATE",
    "R2C-R3 now verifies the facade delegates query construction/result identity, while Phase97 verifies report-layer provenance. Rechecking the same six-target provenance through the facade is redundant.",
    "representative_provenance_matrix",
  ),
}


@dataclass(frozen=True)
class Row:
  nodeid: str
  classification: str
  overlap_group: str
  assert_count: int
  calls_build_standard_toda_report: bool
  calls_build_phase95_20_data: bool
  calls_render_narrative: bool
  scans_group_grid: bool
  rationale: str


def _read_nodeids(
  path: Path,
) -> set[str]:
  return {
    line.strip()
    for line in path.read_text(
      encoding="utf-8"
    ).splitlines()
    if line.strip()
  }


def _function_source(
  path: Path,
  function_name: str,
) -> tuple[str, ast.FunctionDef]:
  source = path.read_text(
    encoding="utf-8-sig"
  )
  tree = ast.parse(
    source
  )

  for node in tree.body:
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name
      == function_name
    ):
      if node.end_lineno is None:
        raise RuntimeError(
          "AST end_lineno unavailable: "
          + function_name
        )

      lines = source.splitlines()
      return (
        "\n".join(
          lines[
            node.lineno - 1:
            node.end_lineno
          ]
        ),
        node,
      )

  raise RuntimeError(
    "Function not found: "
    + function_name
    + " in "
    + str(path)
  )


def _row(
  repo_root: Path,
  nodeid: str,
) -> Row:
  relative_path, function_name = (
    nodeid.split(
      "::",
      1,
    )
  )
  function_source, function_node = (
    _function_source(
      repo_root / relative_path,
      function_name,
    )
  )
  file_source = (
    repo_root
    / relative_path
  ).read_text(
    encoding="utf-8-sig"
  )

  (
    classification,
    rationale,
    overlap_group,
  ) = CLASSIFICATION[
    nodeid
  ]

  return Row(
    nodeid=nodeid,
    classification=classification,
    overlap_group=overlap_group,
    assert_count=sum(
      isinstance(
        node,
        ast.Assert,
      )
      for node in ast.walk(
        function_node
      )
    ),
    calls_build_standard_toda_report=(
      "build_standard_toda_report"
      in function_source
      or (
        "build_standard_toda_report"
        in file_source
        and "_phase153_"
        in function_source
      )
    ),
    calls_build_phase95_20_data=(
      "build_phase95_20_data"
      in function_source
      or (
        "build_phase95_20_data"
        in file_source
        and (
          "build_phase96_"
          in function_source
          or "build_phase97_"
          in function_source
          or "build_phase98_"
          in function_source
        )
      )
    ),
    calls_render_narrative=(
      "render_toda_group_proof_narrative_markdown"
      in function_source
      or "render_toda_full_proof_report_markdown"
      in function_source
      or "report" in function_name
      or "markdown" in function_name
    ),
    scans_group_grid=(
      "all_selected_statements"
      in function_name
      or "markers_cover_structured"
      in function_name
      or "all_reference_entries"
      in function_name
    ),
    rationale=rationale,
  )


def _markdown(
  rows: tuple[Row, ...],
) -> str:
  classes = Counter(
    row.classification
    for row in rows
  )
  groups = Counter(
    row.overlap_group
    for row in rows
  )

  lines = [
    "# Phase 155 Closure-R2C-R4 overlap / redundancy audit",
    "",
    "## Boundary",
    "",
    "- KEEP_ROUTINE_CANDIDATE reviewed: 14",
    "- Repository test bodies executed: 0",
    "- Repository files changed: 0",
    "- Production changes: none",
    "",
    "## Classification",
    "",
    "```text",
  ]

  for key in (
    "KEEP",
    "MERGE_CANDIDATE",
    "DELETE_CANDIDATE",
  ):
    lines.append(
      f"{key}: {classes.get(key, 0)}"
    )

  lines.extend(
    [
      "```",
      "",
      "## Overlap groups",
      "",
      "```text",
    ]
  )

  for key, count in sorted(
    groups.items()
  ):
    lines.append(
      f"{key}: {count}"
    )

  lines.extend(
    [
      "```",
      "",
      "## Review table",
      "",
      "| classification | overlap group | asserts | nodeid |",
      "| --- | --- | ---: | --- |",
    ]
  )

  for row in rows:
    lines.append(
      "| "
      + row.classification
      + " | "
      + row.overlap_group
      + " | "
      + str(
        row.assert_count
      )
      + " | `"
      + row.nodeid
      + "` |"
    )

  lines.extend(
    [
      "",
      "## Per-test rationale",
      "",
    ]
  )

  for row in rows:
    lines.append(
      "### `"
      + row.nodeid
      + "`"
    )
    lines.append("")
    lines.append(
      "- classification: `"
      + row.classification
      + "`"
    )
    lines.append(
      "- overlap group: `"
      + row.overlap_group
      + "`"
    )
    lines.append(
      "- source assert count: "
      + str(
        row.assert_count
      )
    )
    flags = []
    if row.calls_build_standard_toda_report:
      flags.append(
        "standard-report"
      )
    if row.calls_build_phase95_20_data:
      flags.append(
        "phase95-heavy-fixture"
      )
    if row.calls_render_narrative:
      flags.append(
        "render-surface"
      )
    if row.scans_group_grid:
      flags.append(
        "all-group-population"
      )
    lines.append(
      "- static signals: "
      + (
        ", ".join(
          flags
        )
        if flags
        else "none"
      )
    )
    lines.append(
      "- rationale: "
      + row.rationale
    )
    lines.append("")

  lines.extend(
    [
      "## Recommended R2C-R5 action",
      "",
      "1. Keep the three distinct public/rendering contracts unchanged.",
      "2. Merge the three Phase153 population scans into one opt-in population audit so the 112-group traversal is performed once.",
      "3. Merge the Phase96/97 representative provenance matrices into one representative cross-layer integration audit.",
      "4. Delete only the six tests marked DELETE_CANDIDATE after their covering contracts are revalidated.",
      "5. Do not run the repository-wide suite until the Phase155 closure shards are ready.",
      "",
    ]
  )

  return "\n".join(
    lines
  )


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  parser.add_argument(
    "--manifest",
    type=Path,
    default=Path(
      "phase155_closure_r2c_r1_output/"
      "keep_routine_candidate.txt"
    ),
  )
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase155_closure_r2c_r4_output"
    ),
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()
  manifest_path = (
    args.manifest
    if args.manifest.is_absolute()
    else repo_root
    / args.manifest
  )
  output_dir = (
    args.output_dir
    if args.output_dir.is_absolute()
    else repo_root
    / args.output_dir
  )

  if not manifest_path.exists():
    raise SystemExit(
      "KEEP_ROUTINE_CANDIDATE manifest not found: "
      + str(
        manifest_path
      )
    )

  actual = _read_nodeids(
    manifest_path
  )

  if actual != EXPECTED_KEEP_ROUTINE:
    raise SystemExit(
      "KEEP_ROUTINE_CANDIDATE set differs from reviewed 14. "
      + "missing="
      + repr(
        sorted(
          EXPECTED_KEEP_ROUTINE
          - actual
        )
      )
      + " extra="
      + repr(
        sorted(
          actual
          - EXPECTED_KEEP_ROUTINE
        )
      )
    )

  if set(
    CLASSIFICATION
  ) != EXPECTED_KEEP_ROUTINE:
    raise SystemExit(
      "Internal R2C-R4 classification table does not cover the exact 14."
    )

  rows = tuple(
    _row(
      repo_root,
      nodeid,
    )
    for nodeid in sorted(
      actual
    )
  )

  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  payload = {
    "reviewed_nodeids": 14,
    "repository_tests_executed": 0,
    "repository_files_changed": 0,
    "production_changes": False,
    "classification_counts": dict(
      Counter(
        row.classification
        for row in rows
      )
    ),
    "overlap_group_counts": dict(
      Counter(
        row.overlap_group
        for row in rows
      )
    ),
    "rows": [
      asdict(
        row
      )
      for row in rows
    ],
  }

  (
    output_dir
    / "phase155_closure_r2c_r4_audit.json"
  ).write_text(
    json.dumps(
      payload,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  (
    output_dir
    / "phase155_closure_r2c_r4_audit.md"
  ).write_text(
    _markdown(
      rows
    ),
    encoding="utf-8",
  )

  for classification in (
    "KEEP",
    "MERGE_CANDIDATE",
    "DELETE_CANDIDATE",
  ):
    (
      output_dir
      / (
        classification.lower()
        + ".txt"
      )
    ).write_text(
      "".join(
        row.nodeid
        + "\n"
        for row in rows
        if row.classification
        == classification
      ),
      encoding="utf-8",
    )

  counts = Counter(
    row.classification
    for row in rows
  )

  print(
    "Phase 155 Closure-R2C-R4 overlap / redundancy audit"
  )
  print(
    "Reviewed KEEP_ROUTINE_CANDIDATE:",
    len(
      rows
    ),
  )
  print(
    "Repository tests executed: 0"
  )
  print(
    "Repository files changed: 0"
  )
  print(
    "Production changes: none"
  )
  print("")
  print(
    "Classifications:"
  )
  for key in (
    "KEEP",
    "MERGE_CANDIDATE",
    "DELETE_CANDIDATE",
  ):
    print(
      f"  {key}: {counts.get(key, 0)}"
    )

  if counts != Counter({
    "KEEP": 3,
    "MERGE_CANDIDATE": 5,
    "DELETE_CANDIDATE": 6,
  }):
    raise SystemExit(
      "Unexpected R2C-R4 classification counts: "
      + repr(
        dict(
          counts
        )
      )
    )

  print("")
  print(
    "R2C-R4 validated: True"
  )
  print(
    "No KEEP_ROUTINE_CANDIDATE test body was executed."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
