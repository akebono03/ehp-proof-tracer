from __future__ import annotations

import csv
from collections import Counter
from dataclasses import fields, is_dataclass
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


def _reference_name(
  entry,
) -> str:
  return (
    entry.reference.locator
    or entry.reference.label
  )


def _normalized_source_theorem(
  theorem: str | None,
) -> str:
  if theorem is None:
    return ""

  normalized = theorem.strip()

  if normalized.startswith(
    "Toda "
  ):
    normalized = normalized[
      len(
        "Toda "
      ):
    ]

  return normalized


def _selected_reference_steps(
  presentation,
  entry,
):
  candidate_steps = []

  for proof_step in entry.proof_steps:
    rendered_statement = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not (
      _is_toda_group_proof_narrative_reference_statement_candidate(
        proof_step,
        rendered_statement,
      )
    ):
      continue

    candidate_steps.append(
      proof_step
    )

  return (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      tuple(
        candidate_steps
      ),
      presentation.edges,
    )
  )


def _contains_equal_value(
  container,
  target,
  *,
  root_call: bool = True,
  visited: set[int] | None = None,
) -> bool:
  if visited is None:
    visited = set()

  if not root_call:
    try:
      if container == target:
        return True
    except Exception:
      pass

  container_id = id(
    container
  )

  if container_id in visited:
    return False

  visited.add(
    container_id
  )

  if is_dataclass(
    container
  ):
    for field in fields(
      container
    ):
      if _contains_equal_value(
        getattr(
          container,
          field.name,
        ),
        target,
        root_call=False,
        visited=visited,
      ):
        return True

    return False

  if isinstance(
    container,
    dict,
  ):
    for key, value in container.items():
      if _contains_equal_value(
        key,
        target,
        root_call=False,
        visited=visited,
      ):
        return True

      if _contains_equal_value(
        value,
        target,
        root_call=False,
        visited=visited,
      ):
        return True

    return False

  if isinstance(
    container,
    (
      tuple,
      list,
      set,
      frozenset,
    ),
  ):
    for item in container:
      if _contains_equal_value(
        item,
        target,
        root_call=False,
        visited=visited,
      ):
        return True

  return False


def _classification(
  selected_step,
  root_step,
  *,
  same_source_theorem: bool,
) -> str:
  if selected_step is root_step:
    return "selected_root_step_identity"

  try:
    if (
      selected_step.conclusion
      == root_step.conclusion
    ):
      return "selected_root_conclusion_equal"
  except Exception:
    pass

  if _contains_equal_value(
    selected_step.conclusion,
    root_step.conclusion,
  ):
    return "selected_aggregate_contains_root_conclusion"

  if same_source_theorem:
    return "same_source_theorem_only"

  return "not_self_reference"


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  selected_rows = []
  defect_rows = []
  group_rows = []
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

      group_selected = 0
      group_exact = 0
      group_aggregate = 0
      group_same_theorem_only = 0

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
        source_theorem = (
          presentation.source_entry.theorem
        )
        normalized_source_theorem = (
          _normalized_source_theorem(
            source_theorem
          )
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

        for entry in reference_entries:
          reference_name = (
            _reference_name(
              entry
            )
          )
          same_source_theorem = (
            bool(
              normalized_source_theorem
            )
            and reference_name
            == normalized_source_theorem
          )
          selected_steps = (
            _selected_reference_steps(
              presentation,
              entry,
            )
          )

          for selected_step in selected_steps:
            group_selected += 1
            totals[
              "selected_reference_steps"
            ] += 1

            classification = (
              _classification(
                selected_step,
                root_step,
                same_source_theorem=(
                  same_source_theorem
                ),
              )
            )
            rendered_statement = (
              _render_generic_narrative_step(
                selected_step
              )
            )
            root_rendered = (
              _render_generic_narrative_step(
                root_step
              )
            )

            row = {
              "n": n,
              "k": k,
              "source_theorem": (
                source_theorem
                or ""
              ),
              "reference_number": (
                entry.number
              ),
              "reference": (
                reference_name
              ),
              "classification": (
                classification
              ),
              "selected_statement_type": type(
                selected_step.conclusion
              ).__name__,
              "selected_statement": (
                rendered_statement
              ),
              "root_statement_type": type(
                root_step.conclusion
              ).__name__,
              "root_statement": (
                root_rendered
              ),
              "selected_is_root_identity": (
                selected_step is root_step
              ),
              "same_source_theorem": (
                same_source_theorem
              ),
            }
            selected_rows.append(
              row
            )

            if classification == (
              "selected_root_step_identity"
            ):
              totals[
                "selected_root_step_identity"
              ] += 1
              totals[
                "exact_self_reference"
              ] += 1
              group_exact += 1
              defect_rows.append(
                row
              )
              affected_groups.add(
                (
                  n,
                  k,
                )
              )
              continue

            if classification == (
              "selected_root_conclusion_equal"
            ):
              totals[
                "selected_root_conclusion_equal"
              ] += 1
              totals[
                "exact_self_reference"
              ] += 1
              group_exact += 1
              defect_rows.append(
                row
              )
              affected_groups.add(
                (
                  n,
                  k,
                )
              )
              continue

            if classification == (
              "selected_aggregate_contains_root_conclusion"
            ):
              totals[
                "aggregate_self_reference"
              ] += 1
              group_aggregate += 1
              defect_rows.append(
                row
              )
              affected_groups.add(
                (
                  n,
                  k,
                )
              )
              continue

            if classification == (
              "same_source_theorem_only"
            ):
              totals[
                "same_source_theorem_only"
              ] += 1
              group_same_theorem_only += 1

        group_rows.append(
          {
            "n": n,
            "k": k,
            "source_theorem": (
              source_theorem
              or ""
            ),
            "reference_entries": len(
              reference_entries
            ),
            "selected_reference_steps": (
              group_selected
            ),
            "exact_self_reference": (
              group_exact
            ),
            "aggregate_self_reference": (
              group_aggregate
            ),
            "same_source_theorem_only": (
              group_same_theorem_only
            ),
            "has_self_reference_defect": (
              group_exact > 0
              or group_aggregate > 0
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
  totals[
    "self_reference_selected_steps"
  ] = (
    totals[
      "exact_self_reference"
    ]
    + totals[
      "aggregate_self_reference"
    ]
  )

  classification_counts = Counter(
    row[
      "classification"
    ]
    for row in selected_rows
  )

  summary_lines = [
    "=" * 78,
    "Reference Self-Reference Audit - 112 Groups",
    "=" * 78,
    "scope: n=2..15, k=0..7, depth=2, semantic closure",
    "production changes: none",
    "tests changes: none",
    "",
    f"groups: {totals['groups']}",
    f"exceptions: {totals['exceptions']}",
    f"reference entries: {totals['reference_entries']}",
    f"selected reference steps: {totals['selected_reference_steps']}",
    "",
    "Self-reference defects:",
    (
      "  exact self-reference: "
      + str(
        totals[
          "exact_self_reference"
        ]
      )
    ),
    (
      "    selected root step identity: "
      + str(
        totals[
          "selected_root_step_identity"
        ]
      )
    ),
    (
      "    selected root conclusion equal: "
      + str(
        totals[
          "selected_root_conclusion_equal"
        ]
      )
    ),
    (
      "  aggregate contains root conclusion: "
      + str(
        totals[
          "aggregate_self_reference"
        ]
      )
    ),
    (
      "  total self-reference selected steps: "
      + str(
        totals[
          "self_reference_selected_steps"
        ]
      )
    ),
    (
      "  affected groups: "
      + str(
        totals[
          "affected_groups"
        ]
      )
    ),
    "",
    (
      "Same-source-theorem but not proven self-reference: "
      + str(
        totals[
          "same_source_theorem_only"
        ]
      )
    ),
    "",
    "All selected-step classifications:",
  ]

  for classification, count in sorted(
    classification_counts.items()
  ):
    summary_lines.append(
      "  "
      + classification
      + ": "
      + str(
        count
      )
    )

  summary_lines.extend(
    (
      "",
      "Interpretation:",
      (
        "  exact/aggregate categories are confirmed "
        "self-reference defects."
      ),
      (
        "  same_source_theorem_only is suspicious but "
        "is NOT counted as a confirmed defect."
      ),
      "",
      "Output files:",
      "  self_reference_summary.txt",
      "  self_reference_defects.csv",
      "  selected_reference_steps.csv",
      "  group_inventory.csv",
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

  (OUTPUT_DIR / "self_reference_summary.txt").write_text(
    summary + "\n",
    encoding="utf-8",
  )

  selected_fields = (
    "n",
    "k",
    "source_theorem",
    "reference_number",
    "reference",
    "classification",
    "selected_statement_type",
    "selected_statement",
    "root_statement_type",
    "root_statement",
    "selected_is_root_identity",
    "same_source_theorem",
  )

  _write_csv(
    OUTPUT_DIR / "self_reference_defects.csv",
    defect_rows,
    selected_fields,
  )
  _write_csv(
    OUTPUT_DIR / "selected_reference_steps.csv",
    selected_rows,
    selected_fields,
  )
  _write_csv(
    OUTPUT_DIR / "group_inventory.csv",
    group_rows,
    (
      "n",
      "k",
      "source_theorem",
      "reference_entries",
      "selected_reference_steps",
      "exact_self_reference",
      "aggregate_self_reference",
      "same_source_theorem_only",
      "has_self_reference_defect",
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
