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
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  select_toda_group_proof_narrative_reference_statement_steps,
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


def _reference_name_from_step(
  proof_step,
) -> str:
  reference = (
    extract_toda_group_proof_step_literature_reference(
      proof_step
    )
  )

  if reference is None:
    return ""

  return (
    reference.locator
    or reference.label
  )


def _reference_name(
  entry,
) -> str:
  return (
    entry.reference.locator
    or entry.reference.label
  )


def _candidate_steps(
  entry,
):
  candidates = []

  for proof_step in entry.proof_steps:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not (
      _is_toda_group_proof_narrative_reference_statement_candidate(
        proof_step,
        rendered,
      )
    ):
      continue

    candidates.append(
      proof_step
    )

  return tuple(
    candidates
  )


def _is_confirmed_self_reference(
  proof_step,
  root_step,
) -> bool:
  if proof_step is root_step:
    return True

  try:
    return (
      proof_step.conclusion
      == root_step.conclusion
    )
  except Exception:
    return False


def _depth_by_step_id(
  presentation,
) -> dict[int, int]:
  return {
    id(
      node.proof_step
    ): node.depth
    for node in presentation.nodes
  }


def _direct_root_premises(
  presentation,
):
  return tuple(
    edge.premise_step
    for edge in sorted(
      (
        edge
        for edge in presentation.edges
        if edge.parent_step
        is presentation.root_step
      ),
      key=lambda edge: edge.premise_index,
    )
  )


def _selected_after_exclusion(
  entry,
  candidates,
  presentation,
):
  filtered = tuple(
    proof_step
    for proof_step in candidates
    if not _is_confirmed_self_reference(
      proof_step,
      presentation.root_step,
    )
  )

  if not filtered:
    return (
      (),
      (),
    )

  selected = (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      filtered,
      presentation.edges,
    )
  )

  return (
    filtered,
    selected,
  )


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  defect_group_rows = []
  defect_reference_rows = []
  alternative_candidate_rows = []
  direct_premise_rows = []
  exception_rows = []

  totals = Counter()
  affected_groups = set()

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
        root_step = presentation.root_step
        depth_by_id = (
          _depth_by_step_id(
            presentation
          )
        )
        reference_entries = (
          build_toda_group_proof_narrative_reference_entries(
            presentation
          )
        )

        group_defect_count = 0
        group_alternative_entry_count = 0
        group_empty_after_exclusion = 0

        for entry in reference_entries:
          candidates = (
            _candidate_steps(
              entry
            )
          )
          selected = (
            select_toda_group_proof_narrative_reference_statement_steps(
              entry,
              candidates,
              presentation.edges,
            )
            if candidates
            else ()
          )
          self_selected = tuple(
            proof_step
            for proof_step in selected
            if _is_confirmed_self_reference(
              proof_step,
              root_step,
            )
          )

          if not self_selected:
            continue

          affected_groups.add(
            (
              n,
              k,
            )
          )
          group_defect_count += len(
            self_selected
          )
          totals[
            "confirmed_self_reference_steps"
          ] += len(
            self_selected
          )

          (
            filtered_candidates,
            alternative_selected,
          ) = _selected_after_exclusion(
            entry,
            candidates,
            presentation,
          )

          if alternative_selected:
            group_alternative_entry_count += 1
            totals[
              "defect_entries_with_alternative_selected"
            ] += 1
          else:
            group_empty_after_exclusion += 1
            totals[
              "defect_entries_without_alternative_selected"
            ] += 1

          defect_reference_rows.append(
            {
              "n": n,
              "k": k,
              "source_theorem": (
                presentation.source_entry.theorem
                or ""
              ),
              "reference_number": entry.number,
              "reference": _reference_name(
                entry
              ),
              "selected_self_reference_count": len(
                self_selected
              ),
              "candidate_count_before_exclusion": len(
                candidates
              ),
              "candidate_count_after_exclusion": len(
                filtered_candidates
              ),
              "alternative_selected_count": len(
                alternative_selected
              ),
              "root_statement_type": type(
                root_step.conclusion
              ).__name__,
              "root_statement": (
                _render_generic_narrative_step(
                  root_step
                )
              ),
            }
          )

          for proof_step in candidates:
            alternative_candidate_rows.append(
              {
                "n": n,
                "k": k,
                "source_theorem": (
                  presentation.source_entry.theorem
                  or ""
                ),
                "reference_number": entry.number,
                "reference": _reference_name(
                  entry
                ),
                "candidate_statement_type": type(
                  proof_step.conclusion
                ).__name__,
                "candidate_statement": (
                  _render_generic_narrative_step(
                    proof_step
                  )
                ),
                "candidate_depth": (
                  depth_by_id.get(
                    id(
                      proof_step
                    ),
                    "",
                  )
                ),
                "is_self_reference": (
                  _is_confirmed_self_reference(
                    proof_step,
                    root_step,
                  )
                ),
                "selected_before_exclusion": (
                  proof_step in selected
                ),
                "selected_after_exclusion": (
                  proof_step
                  in alternative_selected
                ),
                "is_direct_root_premise": (
                  any(
                    proof_step is premise
                    for premise in (
                      _direct_root_premises(
                        presentation
                      )
                    )
                  )
                ),
              }
            )

        if group_defect_count:
          defect_group_rows.append(
            {
              "n": n,
              "k": k,
              "source_theorem": (
                presentation.source_entry.theorem
                or ""
              ),
              "root_statement_type": type(
                root_step.conclusion
              ).__name__,
              "root_statement": (
                _render_generic_narrative_step(
                  root_step
                )
              ),
              "self_reference_steps": (
                group_defect_count
              ),
              "defect_entries_with_alternative_selected": (
                group_alternative_entry_count
              ),
              "defect_entries_without_alternative_selected": (
                group_empty_after_exclusion
              ),
            }
          )

          for premise_index, premise in enumerate(
            _direct_root_premises(
              presentation
            ),
            start=1,
          ):
            direct_premise_rows.append(
              {
                "n": n,
                "k": k,
                "source_theorem": (
                  presentation.source_entry.theorem
                  or ""
                ),
                "premise_index": premise_index,
                "premise_statement_type": type(
                  premise.conclusion
                ).__name__,
                "premise_statement": (
                  _render_generic_narrative_step(
                    premise
                  )
                ),
                "premise_reference": (
                  _reference_name_from_step(
                    premise
                  )
                ),
                "premise_depth": (
                  depth_by_id.get(
                    id(
                      premise
                    ),
                    "",
                  )
                ),
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

  totals[
    "affected_groups"
  ] = len(
    affected_groups
  )

  summary_lines = [
    "=" * 78,
    "Reference Self-Reference Alternative Candidate Audit",
    "=" * 78,
    "scope: n=2..15, k=0..7, depth=2, semantic closure",
    "production changes: none",
    "tests changes: none",
    "",
    f"groups: {totals['groups']}",
    f"exceptions: {totals['exceptions']}",
    f"affected groups: {totals['affected_groups']}",
    (
      "confirmed self-reference selected steps: "
      + str(
        totals[
          "confirmed_self_reference_steps"
        ]
      )
    ),
    (
      "defect entries with alternative selected candidate: "
      + str(
        totals[
          "defect_entries_with_alternative_selected"
        ]
      )
    ),
    (
      "defect entries without alternative selected candidate: "
      + str(
        totals[
          "defect_entries_without_alternative_selected"
        ]
      )
    ),
    "",
    "Affected groups:",
  ]

  for row in defect_group_rows:
    summary_lines.append(
      "  "
      + "pi_"
      + str(
        row[
          "n"
        ]
        + row[
          "k"
        ]
      )
      + "^"
      + str(
        row[
          "n"
        ]
      )
      + "  "
      + str(
        row[
          "source_theorem"
        ]
      )
      + "  self="
      + str(
        row[
          "self_reference_steps"
        ]
      )
      + "  alternative-entry="
      + str(
        row[
          "defect_entries_with_alternative_selected"
        ]
      )
      + "  empty-entry="
      + str(
        row[
          "defect_entries_without_alternative_selected"
        ]
      )
    )

  summary_lines.extend(
    (
      "",
      "Output files:",
      "  alternative_candidate_summary.txt",
      "  affected_groups.csv",
      "  defect_reference_entries.csv",
      "  candidate_inventory.csv",
      "  direct_root_premises.csv",
      "  exception_inventory.csv",
      "",
      "Interpretation:",
      (
        "  candidate_inventory.csv shows what remains in the same "
        "Reference entry after self-reference exclusion."
      ),
      (
        "  direct_root_premises.csv shows the actual immediate proof "
        "dependencies of each affected target."
      ),
      (
        "  This audit does not decide whether same-theorem alternatives "
        "are mathematically appropriate."
      ),
      "=" * 78,
    )
  )

  summary = "\n".join(
    summary_lines
  )

  print(
    summary
  )

  (OUTPUT_DIR / "alternative_candidate_summary.txt").write_text(
    summary + "\n",
    encoding="utf-8",
  )

  _write_csv(
    OUTPUT_DIR / "affected_groups.csv",
    defect_group_rows,
    (
      "n",
      "k",
      "source_theorem",
      "root_statement_type",
      "root_statement",
      "self_reference_steps",
      "defect_entries_with_alternative_selected",
      "defect_entries_without_alternative_selected",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "defect_reference_entries.csv",
    defect_reference_rows,
    (
      "n",
      "k",
      "source_theorem",
      "reference_number",
      "reference",
      "selected_self_reference_count",
      "candidate_count_before_exclusion",
      "candidate_count_after_exclusion",
      "alternative_selected_count",
      "root_statement_type",
      "root_statement",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "candidate_inventory.csv",
    alternative_candidate_rows,
    (
      "n",
      "k",
      "source_theorem",
      "reference_number",
      "reference",
      "candidate_statement_type",
      "candidate_statement",
      "candidate_depth",
      "is_self_reference",
      "selected_before_exclusion",
      "selected_after_exclusion",
      "is_direct_root_premise",
    ),
  )
  _write_csv(
    OUTPUT_DIR / "direct_root_premises.csv",
    direct_premise_rows,
    (
      "n",
      "k",
      "source_theorem",
      "premise_index",
      "premise_statement_type",
      "premise_statement",
      "premise_reference",
      "premise_depth",
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
    "AUDIT COMPLETE."
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
