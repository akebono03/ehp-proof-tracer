from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
import re
import traceback

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
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


def _is_fallback(
  proof_step,
  rendered: str,
) -> bool:
  inference_rule = proof_step.inference_rule

  return (
    not rendered
    or (
      inference_rule is not None
      and rendered == inference_rule.name
    )
    or rendered
    == (
      "`"
      + type(
        proof_step.conclusion
      ).__name__
      + "`"
    )
    or rendered == repr(
      proof_step.conclusion
    )
    or rendered == str(
      proof_step.conclusion
    )
  )


def _public_sections(
  rendered: str,
) -> tuple[
  str,
  str,
]:
  marker = "## 証明"

  if marker not in rendered:
    return (
      rendered,
      "",
    )

  reference_part, proof_part = rendered.split(
    marker,
    1,
  )

  return (
    reference_part,
    proof_part,
  )


def _statement_in_text(
  statement: str,
  text: str,
) -> bool:
  return (
    statement in text
  )


def _reference_marker(
  number: int,
) -> str:
  return (
    "[R"
    + str(
      number
    )
    + "]"
  )


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


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  group_rows = []
  entry_rows = []
  selected_rows = []
  unresolved_rows = []
  public_missing_rows = []
  body_duplicate_rows = []
  fallback_rows = []
  exception_rows = []

  totals = Counter()
  public_route_totals = Counter()

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
        reference_entries = (
          build_toda_group_proof_narrative_reference_entries(
            presentation
          )
        )
        statement_lines_by_number = (
          _toda_group_proof_narrative_reference_statement_lines_by_number(
            presentation,
            reference_entries,
          )
        )
        public_rendered = (
          render_toda_group_proof_narrative_markdown(
            raw_presentation
          )
        )
        reference_part, proof_part = (
          _public_sections(
            public_rendered
          )
        )

        if "## 証明" in public_rendered:
          public_route_totals[
            "has_proof_section"
          ] += 1
        else:
          public_route_totals[
            "no_proof_section"
          ] += 1

        totals[
          "presentation_nodes"
        ] += len(
          presentation.nodes
        )
        totals[
          "reference_entries"
        ] += len(
          reference_entries
        )

        selected_statement_count = sum(
          len(
            statement_lines
          )
          for statement_lines in (
            statement_lines_by_number.values()
          )
        )
        totals[
          "selected_statements"
        ] += selected_statement_count

        group_public_missing = 0
        group_body_duplicates = 0
        group_unresolved = 0
        group_fallbacks = 0

        for entry in reference_entries:
          selected_lines = (
            statement_lines_by_number.get(
              entry.number,
              (),
            )
          )

          if selected_lines:
            totals[
              "entries_with_selected_statement"
            ] += 1
          else:
            totals[
              "entries_without_selected_statement"
            ] += 1

          renderable_step_count = 0
          unresolved_step_count = 0

          for proof_step in entry.proof_steps:
            rendered_step = (
              _render_generic_narrative_step(
                proof_step
              )
            )

            if _is_fallback(
              proof_step,
              rendered_step,
            ):
              unresolved_step_count += 1
              totals[
                "unresolved_steps"
              ] += 1
              group_unresolved += 1

              unresolved_rows.append(
                {
                  "n": n,
                  "k": k,
                  "reference_number": entry.number,
                  "reference": (
                    entry.reference.locator
                    or entry.reference.label
                  ),
                  "statement_type": type(
                    proof_step.conclusion
                  ).__name__,
                  "rendered": rendered_step,
                  "rule_name": (
                    ""
                    if proof_step.inference_rule
                    is None
                    else proof_step.inference_rule.name
                  ),
                }
              )
            else:
              renderable_step_count += 1

          entry_rows.append(
            {
              "n": n,
              "k": k,
              "reference_number": entry.number,
              "reference": (
                entry.reference.locator
                or entry.reference.label
              ),
              "proof_steps": len(
                entry.proof_steps
              ),
              "renderable_steps": renderable_step_count,
              "unresolved_steps": unresolved_step_count,
              "selected_statements": len(
                selected_lines
              ),
            }
          )

          for statement_index, statement_line in enumerate(
            selected_lines,
            start=1,
          ):
            marker = _reference_marker(
              entry.number
            )
            statement_in_reference = (
              _statement_in_text(
                statement_line,
                reference_part,
              )
            )
            statement_in_proof = (
              _statement_in_text(
                statement_line,
                proof_part,
              )
            )

            selected_rows.append(
              {
                "n": n,
                "k": k,
                "reference_number": entry.number,
                "reference": (
                  entry.reference.locator
                  or entry.reference.label
                ),
                "statement_index": statement_index,
                "statement": statement_line,
                "marker_in_public": (
                  marker in public_rendered
                ),
                "statement_in_reference": statement_in_reference,
                "statement_in_proof": statement_in_proof,
              }
            )

            if not statement_in_reference:
              totals[
                "public_reference_statement_missing"
              ] += 1
              group_public_missing += 1

              public_missing_rows.append(
                {
                  "n": n,
                  "k": k,
                  "reference_number": entry.number,
                  "reference": (
                    entry.reference.locator
                    or entry.reference.label
                  ),
                  "statement": statement_line,
                  "marker_present": (
                    marker in public_rendered
                  ),
                }
              )

            if statement_in_proof:
              totals[
                "body_exact_duplicates"
              ] += 1
              group_body_duplicates += 1

              body_duplicate_rows.append(
                {
                  "n": n,
                  "k": k,
                  "reference_number": entry.number,
                  "reference": (
                    entry.reference.locator
                    or entry.reference.label
                  ),
                  "statement": statement_line,
                }
              )

            inference_rule_names = tuple(
              step.inference_rule.name
              for step in entry.proof_steps
              if step.inference_rule is not None
            )

            exposed_fallbacks = tuple(
              fallback
              for fallback in (
                *inference_rule_names,
                *(
                  "`"
                  + type(
                    step.conclusion
                  ).__name__
                  + "`"
                  for step in entry.proof_steps
                ),
              )
              if (
                fallback
                and fallback in reference_part
              )
            )

            for exposed_fallback in exposed_fallbacks:
              totals[
                "public_reference_fallback_exposures"
              ] += 1
              group_fallbacks += 1

              fallback_rows.append(
                {
                  "n": n,
                  "k": k,
                  "reference_number": entry.number,
                  "reference": (
                    entry.reference.locator
                    or entry.reference.label
                  ),
                  "fallback": exposed_fallback,
                }
              )

        group_rows.append(
          {
            "n": n,
            "k": k,
            "presentation_nodes": len(
              presentation.nodes
            ),
            "reference_entries": len(
              reference_entries
            ),
            "selected_statements": selected_statement_count,
            "unresolved_steps": group_unresolved,
            "public_missing_statements": group_public_missing,
            "body_exact_duplicates": group_body_duplicates,
            "public_fallback_exposures": group_fallbacks,
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
    "Phase 153-R3-7 - 112-group Reference Regression Audit",
    "=" * 78,
    "scope: n=2..15, k=0..7, depth=2, semantic closure",
    "production changes: none",
    "",
    f"groups: {totals['groups']}",
    f"exceptions: {totals['exceptions']}",
    f"presentation nodes: {totals['presentation_nodes']}",
    f"reference entries: {totals['reference_entries']}",
    f"entries with selected statement: {totals['entries_with_selected_statement']}",
    f"entries without selected statement: {totals['entries_without_selected_statement']}",
    f"selected statements: {totals['selected_statements']}",
    f"unresolved steps: {totals['unresolved_steps']}",
    "",
    "Public Reference rendering:",
    (
      "  selected statement missing from Reference section: "
      + str(
        totals[
          "public_reference_statement_missing"
        ]
      )
    ),
    (
      "  exact selected statement duplicated in proof body: "
      + str(
        totals[
          "body_exact_duplicates"
        ]
      )
    ),
    (
      "  rule-name/type-name fallback exposures in Reference section: "
      + str(
        totals[
          "public_reference_fallback_exposures"
        ]
      )
    ),
    "",
    "Public route shape:",
    (
      "  narratives with ## 証明: "
      + str(
        public_route_totals[
          "has_proof_section"
        ]
      )
    ),
    (
      "  narratives without ## 証明: "
      + str(
        public_route_totals[
          "no_proof_section"
        ]
      )
    ),
    "",
    "Audit interpretation:",
    (
      "  entries_without_selected_statement / unresolved_steps measure "
      "structured Reference pipeline coverage."
    ),
    (
      "  public_reference_statement_missing measures whether the selected "
      "statement is actually visible before ## 証明 in the public Narrative."
    ),
    (
      "  body_exact_duplicates measures only exact rendered-string duplicates "
      "after R3-5; semantic-equivalent paraphrases are not counted."
    ),
    (
      "  fallback exposures measure internal inference-rule/type labels that "
      "leak into the public Reference section."
    ),
    "",
    "Output files:",
    "  group_reference_regression.csv",
    "  reference_entry_regression.csv",
    "  selected_reference_statements.csv",
    "  unresolved_reference_steps.csv",
    "  public_reference_missing.csv",
    "  body_exact_duplicates.csv",
    "  public_reference_fallback_exposures.csv",
    "  exception_inventory.csv",
    "  reference_regression_summary.txt",
    "=" * 78,
  ]

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
    OUTPUT_DIR / "group_reference_regression.csv",
    group_rows,
    (
      "n",
      "k",
      "presentation_nodes",
      "reference_entries",
      "selected_statements",
      "unresolved_steps",
      "public_missing_statements",
      "body_exact_duplicates",
      "public_fallback_exposures",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "reference_entry_regression.csv",
    entry_rows,
    (
      "n",
      "k",
      "reference_number",
      "reference",
      "proof_steps",
      "renderable_steps",
      "unresolved_steps",
      "selected_statements",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "selected_reference_statements.csv",
    selected_rows,
    (
      "n",
      "k",
      "reference_number",
      "reference",
      "statement_index",
      "statement",
      "marker_in_public",
      "statement_in_reference",
      "statement_in_proof",
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
      "rendered",
      "rule_name",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "public_reference_missing.csv",
    public_missing_rows,
    (
      "n",
      "k",
      "reference_number",
      "reference",
      "statement",
      "marker_present",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "body_exact_duplicates.csv",
    body_duplicate_rows,
    (
      "n",
      "k",
      "reference_number",
      "reference",
      "statement",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "public_reference_fallback_exposures.csv",
    fallback_rows,
    (
      "n",
      "k",
      "reference_number",
      "reference",
      "fallback",
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

  if totals[
    "exceptions"
  ]:
    print()
    print(
      "AUDIT COMPLETE WITH EXCEPTIONS: inspect exception_inventory.csv."
    )
  elif (
    totals[
      "entries_without_selected_statement"
    ]
    == 0
    and totals[
      "unresolved_steps"
    ]
    == 0
    and totals[
      "public_reference_statement_missing"
    ]
    == 0
    and totals[
      "body_exact_duplicates"
    ]
    == 0
    and totals[
      "public_reference_fallback_exposures"
    ]
    == 0
  ):
    print()
    print(
      "PASS: all 112 groups satisfy the R3 Reference regression criteria."
    )
  else:
    print()
    print(
      "AUDIT COMPLETE: remaining Reference regression defects were detected."
    )
    print(
      "This is an audit result, not an audit-script failure."
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
