from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
import traceback

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _is_toda_group_proof_narrative_reference_statement_candidate,
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def _write_csv(
  path: Path,
  rows: list[dict],
  fieldnames: tuple[str, ...],
) -> None:
  with path.open(
    "w",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=fieldnames,
    )
    writer.writeheader()

    for row in rows:
      writer.writerow(
        {
          field: row.get(
            field,
            "",
          )
          for field in fieldnames
        }
      )


def _reference_name(
  entry,
) -> str:
  return (
    entry.reference.locator
    or entry.reference.label
  )


def _fallback_kind(
  proof_step,
  rendered: str,
) -> str | None:
  if not rendered:
    return "empty"

  if (
    proof_step.inference_rule is not None
    and rendered
    == proof_step.inference_rule.name
  ):
    return "rule_name"

  if rendered == (
    "`"
    + type(
      proof_step.conclusion
    ).__name__
    + "`"
  ):
    return "type_name"

  if rendered == repr(
    proof_step.conclusion
  ):
    return "repr"

  if rendered == str(
    proof_step.conclusion
  ):
    return "str"

  return None


def _public_reference_and_body(
  rendered: str,
  canonical_reference_section: str,
) -> tuple[
  str,
  str,
  str,
]:
  lines = rendered.splitlines()

  if "## 証明" in lines:
    proof_index = lines.index(
      "## 証明"
    )
    reference_part = "\n".join(
      lines[
        :proof_index
      ]
    )
    body_part = "\n".join(
      lines[
        proof_index + 1:
      ]
    )

    return (
      reference_part,
      body_part,
      "explicit_proof_heading",
    )

  if (
    canonical_reference_section
    and rendered.startswith(
      canonical_reference_section
    )
  ):
    body_part = rendered[
      len(
        canonical_reference_section
      ):
    ].lstrip()

    return (
      canonical_reference_section,
      body_part,
      "canonical_prefix_without_proof_heading",
    )

  if canonical_reference_section:
    return (
      "",
      rendered,
      "reference_boundary_unresolved",
    )

  return (
    "",
    rendered,
    "no_reference_entries",
  )


def _public_reference_fallback_exposures(
  reference_part: str,
  reference_entries,
) -> list[dict]:
  exposures = []
  seen = set()

  for entry in reference_entries:
    marker = (
      "[R"
      + str(
        entry.number
      )
      + "]"
    )

    for proof_step in entry.proof_steps:
      candidates = []

      if proof_step.inference_rule is not None:
        candidates.append(
          (
            "rule_name",
            proof_step.inference_rule.name,
          )
        )

      candidates.append(
        (
          "type_name",
          "`"
          + type(
            proof_step.conclusion
          ).__name__
          + "`",
        )
      )

      for fallback_kind, fallback_text in candidates:
        if not fallback_text:
          continue

        key = (
          entry.number,
          fallback_kind,
          fallback_text,
        )

        if key in seen:
          continue

        if fallback_text not in reference_part:
          continue

        seen.add(
          key
        )
        exposures.append(
          {
            "reference_number": entry.number,
            "reference": _reference_name(
              entry
            ),
            "marker": marker,
            "fallback_kind": fallback_kind,
            "fallback_text": fallback_text,
          }
        )

  return exposures


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  unresolved_rows = []
  missing_selected_entry_rows = []
  public_missing_statement_rows = []
  public_missing_marker_rows = []
  duplicate_rows = []
  fallback_exposure_rows = []
  route_rows = []
  exception_rows = []

  totals = Counter()

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      totals[
        "groups"
      ] += 1

      try:
        report = build_standard_toda_report(
          n=n,
          k=k,
        )

        if not report.candidates:
          raise RuntimeError(
            "standard report has no candidates"
          )

        group_result = (
          report.candidates[
            0
          ].source_candidate.group_result
        )
        replay = build_toda_group_result_proof_replay(
          group_result,
          max_depth=2,
        )
        raw_presentation = (
          build_toda_group_proof_presentation(
            replay
          )
        )
        presentation = (
          build_toda_group_proof_narrative_semantic_closure_presentation(
            raw_presentation
          )
        )

        totals[
          "presentation_nodes"
        ] += len(
          presentation.nodes
        )

        reference_entries = (
          build_toda_group_proof_narrative_reference_entries(
            presentation
          )
        )
        totals[
          "reference_entries"
        ] += len(
          reference_entries
        )

        selected_by_number = (
          _toda_group_proof_narrative_reference_statement_lines_by_number(
            presentation,
            reference_entries,
          )
        )

        totals[
          "selected_statements"
        ] += sum(
          len(
            statement_lines
          )
          for statement_lines in (
            selected_by_number.values()
          )
        )

        for entry in reference_entries:
          selected_lines = (
            selected_by_number.get(
              entry.number,
              (),
            )
          )

          if not selected_lines:
            totals[
              "entries_without_selected_statement"
            ] += 1
            missing_selected_entry_rows.append(
              {
                "n": n,
                "k": k,
                "reference_number": entry.number,
                "reference": _reference_name(
                  entry
                ),
                "proof_steps": len(
                  entry.proof_steps
                ),
              }
            )

          for proof_step in entry.proof_steps:
            rendered_step = (
              _render_generic_narrative_step(
                proof_step
              )
            )
            fallback_kind = (
              _fallback_kind(
                proof_step,
                rendered_step,
              )
            )

            if fallback_kind is None:
              continue

            totals[
              "unresolved_reference_steps"
            ] += 1
            unresolved_rows.append(
              {
                "n": n,
                "k": k,
                "reference_number": entry.number,
                "reference": _reference_name(
                  entry
                ),
                "statement_type": type(
                  proof_step.conclusion
                ).__name__,
                "fallback_kind": fallback_kind,
                "rendered": rendered_step,
                "rule_name": (
                  ""
                  if proof_step.inference_rule
                  is None
                  else proof_step.inference_rule.name
                ),
              }
            )

        canonical_reference_section = (
          render_toda_group_proof_narrative_reference_entries_markdown(
            reference_entries,
            selected_by_number,
          )
        )

        rendered = (
          render_toda_group_proof_narrative_markdown(
            raw_presentation
          )
        )

        (
          reference_part,
          body_part,
          route_shape,
        ) = _public_reference_and_body(
          rendered,
          canonical_reference_section,
        )

        route_rows.append(
          {
            "n": n,
            "k": k,
            "route_shape": route_shape,
            "reference_entries": len(
              reference_entries
            ),
            "selected_statements": sum(
              len(
                statement_lines
              )
              for statement_lines in (
                selected_by_number.values()
              )
            ),
            "has_proof_heading": (
              "## 証明"
              in rendered.splitlines()
            ),
            "canonical_reference_is_prefix": (
              bool(
                canonical_reference_section
              )
              and rendered.startswith(
                canonical_reference_section
              )
            ),
          }
        )

        for entry in reference_entries:
          marker = (
            "[R"
            + str(
              entry.number
            )
            + "]"
          )

          if marker not in reference_part:
            totals[
              "public_reference_marker_missing"
            ] += 1
            public_missing_marker_rows.append(
              {
                "n": n,
                "k": k,
                "route_shape": route_shape,
                "reference_number": entry.number,
                "reference": _reference_name(
                  entry
                ),
                "marker": marker,
              }
            )

          for statement_line in (
            selected_by_number.get(
              entry.number,
              (),
            )
          ):
            if statement_line not in reference_part:
              totals[
                "public_selected_statement_missing"
              ] += 1
              public_missing_statement_rows.append(
                {
                  "n": n,
                  "k": k,
                  "route_shape": route_shape,
                  "reference_number": entry.number,
                  "reference": _reference_name(
                    entry
                  ),
                  "statement": statement_line,
                }
              )

            if statement_line in body_part:
              totals[
                "exact_body_duplicates"
              ] += 1
              duplicate_rows.append(
                {
                  "n": n,
                  "k": k,
                  "route_shape": route_shape,
                  "reference_number": entry.number,
                  "reference": _reference_name(
                    entry
                  ),
                  "statement": statement_line,
                }
              )

        exposures = (
          _public_reference_fallback_exposures(
            reference_part,
            reference_entries,
          )
        )

        for exposure in exposures:
          totals[
            "reference_fallback_exposures"
          ] += 1
          fallback_exposure_rows.append(
            {
              "n": n,
              "k": k,
              "route_shape": route_shape,
              **exposure,
            }
          )

      except Exception as exc:
        totals[
          "exceptions"
        ] += 1
        exception_rows.append(
          {
            "n": n,
            "k": k,
            "exception_type": type(
              exc
            ).__name__,
            "message": str(
              exc
            ),
            "traceback": traceback.format_exc(),
          }
        )

  closure_metrics = (
    (
      "exceptions",
      totals[
        "exceptions"
      ],
    ),
    (
      "entries without selected statement",
      totals[
        "entries_without_selected_statement"
      ],
    ),
    (
      "unresolved reference steps",
      totals[
        "unresolved_reference_steps"
      ],
    ),
    (
      "public selected statement missing",
      totals[
        "public_selected_statement_missing"
      ],
    ),
    (
      "public Reference marker missing",
      totals[
        "public_reference_marker_missing"
      ],
    ),
    (
      "exact selected statement duplicated in proof body",
      totals[
        "exact_body_duplicates"
      ],
    ),
    (
      "rule-name/type-name fallback exposure in Reference",
      totals[
        "reference_fallback_exposures"
      ],
    ),
  )

  closure_passed = all(
    value == 0
    for _, value in closure_metrics
  )

  route_counts = Counter(
    row[
      "route_shape"
    ]
    for row in route_rows
  )

  summary_lines = [
    "=" * 78,
    "Phase 153-R3-12 - 112-group Reference Regression Re-Audit",
    "=" * 78,
    "scope: n=2..15, k=0..7, depth=2, semantic closure",
    "production changes: none",
    "tests changes: none",
    "",
    f"groups: {totals['groups']}",
    f"exceptions: {totals['exceptions']}",
    f"presentation nodes: {totals['presentation_nodes']}",
    f"reference entries: {totals['reference_entries']}",
    f"selected statements: {totals['selected_statements']}",
    "",
    "Closure metrics:",
  ]

  for label, value in closure_metrics:
    summary_lines.append(
      "  "
      + label
      + ": "
      + str(
        value
      )
    )

  summary_lines.extend(
    (
      "",
      "Public route shapes:",
    )
  )

  for route_shape, count in sorted(
    route_counts.items()
  ):
    summary_lines.append(
      "  "
      + route_shape
      + ": "
      + str(
        count
      )
    )

  summary_lines.extend(
    (
      "",
      (
        "R3 CLOSURE: PASS"
        if closure_passed
        else "R3 CLOSURE: FAIL"
      ),
      "",
      "Output files:",
      "  reference_regression_summary.txt",
      "  route_inventory.csv",
      "  entries_without_selected_statement.csv",
      "  unresolved_reference_steps.csv",
      "  public_selected_statement_missing.csv",
      "  public_reference_marker_missing.csv",
      "  exact_body_duplicates.csv",
      "  reference_fallback_exposures.csv",
      "  exception_inventory.csv",
      "=" * 78,
    )
  )

  summary = "\n".join(
    summary_lines
  )

  print(
    summary
  )

  (OUTPUT_DIR / "reference_regression_summary.txt").write_text(
    summary + "\n",
    encoding="utf-8",
  )

  _write_csv(
    OUTPUT_DIR / "route_inventory.csv",
    route_rows,
    (
      "n",
      "k",
      "route_shape",
      "reference_entries",
      "selected_statements",
      "has_proof_heading",
      "canonical_reference_is_prefix",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "entries_without_selected_statement.csv",
    missing_selected_entry_rows,
    (
      "n",
      "k",
      "reference_number",
      "reference",
      "proof_steps",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "unresolved_reference_steps.csv",
    unresolved_rows,
    (
      "n",
      "k",
      "reference_number",
      "reference",
      "statement_type",
      "fallback_kind",
      "rendered",
      "rule_name",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "public_selected_statement_missing.csv",
    public_missing_statement_rows,
    (
      "n",
      "k",
      "route_shape",
      "reference_number",
      "reference",
      "statement",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "public_reference_marker_missing.csv",
    public_missing_marker_rows,
    (
      "n",
      "k",
      "route_shape",
      "reference_number",
      "reference",
      "marker",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "exact_body_duplicates.csv",
    duplicate_rows,
    (
      "n",
      "k",
      "route_shape",
      "reference_number",
      "reference",
      "statement",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "reference_fallback_exposures.csv",
    fallback_exposure_rows,
    (
      "n",
      "k",
      "route_shape",
      "reference_number",
      "reference",
      "marker",
      "fallback_kind",
      "fallback_text",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "exception_inventory.csv",
    exception_rows,
    (
      "n",
      "k",
      "exception_type",
      "message",
      "traceback",
    ),
  )

  print()
  print(
    (
      "AUDIT COMPLETE: R3 closure conditions are satisfied."
      if closure_passed
      else "AUDIT COMPLETE: remaining R3 defects were detected."
    )
  )
  print(
    "Production files were NOT changed."
  )
  print(
    "Tests were NOT changed."
  )
  print(
    "Full pytest was NOT run."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
