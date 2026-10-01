from __future__ import annotations

import csv
from collections import Counter, defaultdict
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


def _public_route_shape(
  rendered: str,
) -> str:
  if "## 証明" in rendered:
    if "使用する結果を先にまとめる." in rendered:
      return "standard_reference_plus_proof"

    if "## 使用する結果" in rendered:
      return "legacy_custom_reference_plus_proof"

    return "proof_section_without_standard_reference"

  if "## 使用する結果" in rendered:
    return "custom_without_proof_header"

  if "使用する結果を先にまとめる." in rendered:
    return "standard_reference_without_proof_header"

  return "no_reference_or_proof_header"


def _public_reference_and_body(
  rendered: str,
) -> tuple[
  str,
  str,
]:
  if "## 証明" in rendered:
    return tuple(
      rendered.split(
        "## 証明",
        1,
      )
    )

  return (
    rendered,
    "",
  )


def _duplicate_shape(
  statement_line: str,
  reference_number: int,
  body: str,
) -> str:
  marker = (
    "[R"
    + str(
      reference_number
    )
    + "]"
  )

  for line in body.splitlines():
    if statement_line not in line:
      continue

    if line.strip() == statement_line:
      return "standalone_line"

    if marker in line:
      return "reference_marker_sentence"

    return "embedded_without_reference_marker"

  return "not_found"


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  unresolved_rows = []
  missing_entry_rows = []
  public_missing_rows = []
  duplicate_rows = []
  route_rows = []
  exception_rows = []

  unresolved_type_counts = Counter()
  unresolved_type_groups = defaultdict(set)
  unresolved_reference_counts = Counter()

  missing_reason_counts = Counter()
  missing_reason_groups = defaultdict(set)

  public_missing_route_counts = Counter()
  public_missing_marker_counts = Counter()

  duplicate_shape_counts = Counter()
  duplicate_route_counts = Counter()
  duplicate_group_counts = Counter()

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
        entries = (
          build_toda_group_proof_narrative_reference_entries(
            presentation
          )
        )
        selected_by_number = (
          _toda_group_proof_narrative_reference_statement_lines_by_number(
            presentation,
            entries,
          )
        )
        public_rendered = (
          render_toda_group_proof_narrative_markdown(
            raw_presentation
          )
        )

        route_shape = (
          _public_route_shape(
            public_rendered
          )
        )
        reference_part, body_part = (
          _public_reference_and_body(
            public_rendered
          )
        )

        route_rows.append(
          {
            "n": n,
            "k": k,
            "route_shape": route_shape,
            "has_proof_header": (
              "## 証明" in public_rendered
            ),
            "has_standard_reference_header": (
              "使用する結果を先にまとめる."
              in public_rendered
            ),
            "has_legacy_reference_header": (
              "## 使用する結果"
              in public_rendered
            ),
            "reference_entries": len(
              entries
            ),
            "selected_statements": sum(
              len(
                lines
              )
              for lines in (
                selected_by_number.values()
              )
            ),
          }
        )

        for entry in entries:
          selected_lines = (
            selected_by_number.get(
              entry.number,
              (),
            )
          )

          candidate_count = 0
          unresolved_count = 0
          unresolved_types = []

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
              if (
                _is_toda_group_proof_narrative_reference_statement_candidate(
                  proof_step,
                  rendered_step,
                )
              ):
                candidate_count += 1
              continue

            unresolved_count += 1
            statement_type = type(
              proof_step.conclusion
            ).__name__
            unresolved_types.append(
              statement_type
            )
            unresolved_type_counts[
              statement_type
            ] += 1
            unresolved_type_groups[
              statement_type
            ].add(
              (
                n,
                k,
              )
            )
            unresolved_reference_counts[
              _reference_name(
                entry
              )
            ] += 1

            unresolved_rows.append(
              {
                "n": n,
                "k": k,
                "reference_number": entry.number,
                "reference": _reference_name(
                  entry
                ),
                "statement_type": statement_type,
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

          if not selected_lines:
            if candidate_count == 0:
              if unresolved_count:
                reason = "unresolved_only_or_unrenderable"
              else:
                reason = "no_renderable_candidate"
            else:
              reason = "selection_returned_empty"

            missing_reason_counts[
              reason
            ] += 1
            missing_reason_groups[
              reason
            ].add(
              (
                n,
                k,
              )
            )

            missing_entry_rows.append(
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
                "renderable_candidates": candidate_count,
                "unresolved_steps": unresolved_count,
                "unresolved_types": ";".join(
                  unresolved_types
                ),
                "reason": reason,
              }
            )

          for statement_line in selected_lines:
            marker = (
              "[R"
              + str(
                entry.number
              )
              + "]"
            )
            statement_in_reference = (
              statement_line
              in reference_part
            )
            marker_in_public = (
              marker
              in public_rendered
            )

            if not statement_in_reference:
              public_missing_route_counts[
                route_shape
              ] += 1
              public_missing_marker_counts[
                (
                  "marker_present"
                  if marker_in_public
                  else "marker_missing"
                )
              ] += 1

              public_missing_rows.append(
                {
                  "n": n,
                  "k": k,
                  "route_shape": route_shape,
                  "reference_number": entry.number,
                  "reference": _reference_name(
                    entry
                  ),
                  "marker_present": marker_in_public,
                  "has_proof_header": (
                    "## 証明"
                    in public_rendered
                  ),
                  "statement": statement_line,
                }
              )

            if statement_line in body_part:
              shape = (
                _duplicate_shape(
                  statement_line,
                  entry.number,
                  body_part,
                )
              )
              duplicate_shape_counts[
                shape
              ] += 1
              duplicate_route_counts[
                route_shape
              ] += 1
              duplicate_group_counts[
                (
                  n,
                  k,
                )
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
                  "duplicate_shape": shape,
                  "statement": statement_line,
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

  summary_lines = [
    "=" * 78,
    "Phase 153-R3-8 - Remaining Reference Defect Classification",
    "=" * 78,
    "scope: n=2..15, k=0..7, depth=2, semantic closure",
    "production changes: none",
    "",
    f"groups: {totals['groups']}",
    f"exceptions: {totals['exceptions']}",
    "",
    "A. Unresolved reference steps by statement type",
  ]

  if unresolved_type_counts:
    for statement_type, count in (
      unresolved_type_counts.most_common()
    ):
      summary_lines.append(
        (
          "  "
          + statement_type
          + ": occurrences="
          + str(
            count
          )
          + ", groups="
          + str(
            len(
              unresolved_type_groups[
                statement_type
              ]
            )
          )
        )
      )
  else:
    summary_lines.append(
      "  none"
    )

  summary_lines.extend(
    (
      "",
      "B. Reference entries without selected statement",
    )
  )

  if missing_reason_counts:
    for reason, count in (
      missing_reason_counts.most_common()
    ):
      summary_lines.append(
        (
          "  "
          + reason
          + ": entries="
          + str(
            count
          )
          + ", groups="
          + str(
            len(
              missing_reason_groups[
                reason
              ]
            )
          )
        )
      )
  else:
    summary_lines.append(
      "  none"
    )

  summary_lines.extend(
    (
      "",
      "C. Public Reference statement missing by route shape",
    )
  )

  if public_missing_route_counts:
    for route_shape, count in (
      public_missing_route_counts.most_common()
    ):
      summary_lines.append(
        (
          "  "
          + route_shape
          + ": "
          + str(
            count
          )
        )
      )
  else:
    summary_lines.append(
      "  none"
    )

  summary_lines.append(
    "  marker status:"
  )

  if public_missing_marker_counts:
    for marker_status, count in (
      public_missing_marker_counts.most_common()
    ):
      summary_lines.append(
        (
          "    "
          + marker_status
          + ": "
          + str(
            count
          )
        )
      )
  else:
    summary_lines.append(
      "    none"
    )

  summary_lines.extend(
    (
      "",
      "D. Exact body duplicates by duplicate shape",
    )
  )

  if duplicate_shape_counts:
    for shape, count in (
      duplicate_shape_counts.most_common()
    ):
      summary_lines.append(
        (
          "  "
          + shape
          + ": "
          + str(
            count
          )
        )
      )
  else:
    summary_lines.append(
      "  none"
    )

  summary_lines.append(
    "  by route shape:"
  )

  if duplicate_route_counts:
    for route_shape, count in (
      duplicate_route_counts.most_common()
    ):
      summary_lines.append(
        (
          "    "
          + route_shape
          + ": "
          + str(
            count
          )
        )
      )
  else:
    summary_lines.append(
      "    none"
    )

  summary_lines.extend(
    (
      "",
      "E. Top affected groups by exact duplicate count",
    )
  )

  if duplicate_group_counts:
    for (
      n,
      k,
    ), count in (
      duplicate_group_counts.most_common(
        20
      )
    ):
      summary_lines.append(
        (
          "  (n="
          + str(
            n
          )
          + ", k="
          + str(
            k
          )
          + "): "
          + str(
            count
          )
        )
      )
  else:
    summary_lines.append(
      "  none"
    )

  summary_lines.extend(
    (
      "",
      "Classification guide:",
      (
        "  unresolved_only_or_unrenderable -> renderer coverage defect"
      ),
      (
        "  selection_returned_empty -> representative-selection defect"
      ),
      (
        "  public missing concentrated in custom/no-proof routes -> "
        "public route connection defect"
      ),
      (
        "  standalone/reference-marker duplicates in standard route -> "
        "suppression timing/coverage defect"
      ),
      (
        "  embedded_without_reference_marker -> body-generation ownership defect"
      ),
      "",
      "Output files:",
      "  unresolved_by_occurrence.csv",
      "  entries_without_selected_statement.csv",
      "  public_missing_classification.csv",
      "  body_duplicate_classification.csv",
      "  route_inventory.csv",
      "  exception_inventory.csv",
      "  remaining_reference_defect_summary.txt",
      "=" * 78,
    )
  )

  summary = "\n".join(
    summary_lines
  )

  print(
    summary
  )

  (OUTPUT_DIR / "remaining_reference_defect_summary.txt").write_text(
    summary + "\n",
    encoding="utf-8",
  )

  _write_csv(
    OUTPUT_DIR / "unresolved_by_occurrence.csv",
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
    OUTPUT_DIR / "entries_without_selected_statement.csv",
    missing_entry_rows,
    (
      "n",
      "k",
      "reference_number",
      "reference",
      "proof_steps",
      "renderable_candidates",
      "unresolved_steps",
      "unresolved_types",
      "reason",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "public_missing_classification.csv",
    public_missing_rows,
    (
      "n",
      "k",
      "route_shape",
      "reference_number",
      "reference",
      "marker_present",
      "has_proof_header",
      "statement",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "body_duplicate_classification.csv",
    duplicate_rows,
    (
      "n",
      "k",
      "route_shape",
      "reference_number",
      "reference",
      "duplicate_shape",
      "statement",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "route_inventory.csv",
    route_rows,
    (
      "n",
      "k",
      "route_shape",
      "has_proof_header",
      "has_standard_reference_header",
      "has_legacy_reference_header",
      "reference_entries",
      "selected_statements",
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
    "AUDIT COMPLETE: remaining defects classified."
  )
  print(
    "This package intentionally makes no production or test changes."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
