from __future__ import annotations

import csv
import json
import traceback
from collections import Counter, defaultdict
from pathlib import Path
import sys


REPOSITORY_ROOT = Path.cwd()
if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )


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
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
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
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
  get_toda_fixed_statement_component,
  is_toda_fixed_statement_component_reference_eligible,
)


OUTPUT_DIR = Path(
  "phase157_r5_r5_audit_output"
)

N_RANGE = range(
  2,
  16,
)
K_RANGE = range(
  0,
  8,
)
MAX_DEPTH = 2
EXPECTED_GROUPS = 112

BASELINE_R5_R1 = {
  "groups": 112,
  "exceptions": 0,
  "reference_entries": 225,
  "selected_reference_steps": 234,
  "fixed_statement": 34,
  "proof_internal": 46,
  "untracked": 128,
  "fixed_statement_ineligible": 2,
  "fixed_statement_without_component": 24,
  "fixed_statement_missing_component": 0,
  "confirmed_defects": 72,
}


def _write_csv(
  path: Path,
  rows: list[dict[str, object]],
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


def _group_label(
  n: int,
  k: int,
) -> str:
  return (
    "pi_"
    + str(
      n + k
    )
    + "^"
    + str(
      n
    )
  )


def _reference_title(
  entry,
) -> str:
  return (
    entry.reference.locator
    or entry.reference.label
  )


def _candidate_steps(
  entry,
) -> tuple:
  candidates = []
  seen_rendered = set()

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

    if rendered_statement in seen_rendered:
      continue

    seen_rendered.add(
      rendered_statement
    )
    candidates.append(
      proof_step
    )

  return tuple(
    candidates
  )


def _selected_steps(
  presentation,
  entry,
) -> tuple:
  candidates = _candidate_steps(
    entry
  )

  return (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      candidates,
      presentation.edges,
      root_step=presentation.root_step,
    )
  )


def _boundary_status(
  selected_step,
  root_step,
) -> tuple[
  str,
  str,
  str,
  str,
]:
  boundary = (
    classify_toda_literature_statement_step(
      selected_step
    )
  )

  if boundary is None:
    return (
      "UNTRACKED",
      "",
      "",
      "",
    )

  locator = (
    boundary.reference_locator
    or ""
  )
  component_key = (
    boundary.component_key
    or ""
  )

  if (
    boundary.classification
    == TodaLiteratureStatementClassification.PROOF_INTERNAL
  ):
    return (
      "PROOF_INTERNAL",
      locator,
      component_key,
      "",
    )

  if (
    boundary.classification
    != TodaLiteratureStatementClassification.FIXED_STATEMENT
  ):
    return (
      "UNTRACKED",
      locator,
      component_key,
      "",
    )

  if boundary.component_key is None:
    return (
      "FIXED_STATEMENT_WITHOUT_COMPONENT",
      locator,
      "",
      "",
    )

  component = (
    get_toda_fixed_statement_component(
      boundary.reference_locator,
      boundary.component_key,
    )
  )

  if component is None:
    return (
      "FIXED_STATEMENT_MISSING_COMPONENT",
      locator,
      boundary.component_key,
      "",
    )

  root_boundary = (
    classify_toda_literature_statement_step(
      root_step
    )
  )

  if (
    root_boundary is not None
    and root_boundary.reference_locator is not None
    and root_boundary.component_key is not None
  ):
    eligible = (
      is_toda_fixed_statement_component_reference_eligible(
        component,
        root_boundary.reference_locator,
        root_boundary.component_key,
      )
    )

    if not eligible:
      return (
        "FIXED_STATEMENT_INELIGIBLE",
        locator,
        boundary.component_key,
        (
          root_boundary.reference_locator
          + "::"
          + root_boundary.component_key
        ),
      )

  return (
    "FIXED_STATEMENT",
    locator,
    boundary.component_key,
    "",
  )


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  totals = Counter()
  status_counts = Counter()
  status_groups = defaultdict(
    set
  )

  selected_rows = []
  defect_rows = []
  group_rows = []
  exception_rows = []
  locator_rows = defaultdict(
    lambda: {
      "occurrences": 0,
      "groups": set(),
      "statuses": Counter(),
    }
  )

  for n in N_RANGE:
    for k in K_RANGE:
      totals[
        "groups"
      ] += 1
      group = _group_label(
        n,
        k,
      )

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

        replay = (
          build_toda_group_result_proof_replay(
            group_result,
            max_depth=MAX_DEPTH,
          )
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
        root_step = (
          presentation.root_step
        )

        raw_entries = (
          build_toda_group_proof_narrative_reference_entries(
            presentation
          )
        )
        totals[
          "raw_reference_entries"
        ] += len(
          raw_entries
        )

        raw_selected_count = 0

        for raw_entry in raw_entries:
          raw_selected_count += len(
            _selected_steps(
              presentation,
              raw_entry,
            )
          )

        totals[
          "raw_selected_reference_steps"
        ] += raw_selected_count

        filtered_entries = (
          filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
            raw_entries,
            root_step,
          )
        )

        totals[
          "filtered_reference_entries"
        ] += len(
          filtered_entries
        )

        group_selected = 0
        group_defects = 0
        group_untracked = 0

        for entry in filtered_entries:
          selected_steps = (
            _selected_steps(
              presentation,
              entry,
            )
          )

          for selected_step in selected_steps:
            totals[
              "selected_reference_steps"
            ] += 1
            group_selected += 1

            (
              boundary_status,
              boundary_locator,
              component_key,
              ineligible_against,
            ) = _boundary_status(
              selected_step,
              root_step,
            )

            status_counts[
              boundary_status
            ] += 1
            status_groups[
              boundary_status
            ].add(
              group
            )

            rendered_statement = (
              _render_generic_narrative_step(
                selected_step
              )
            )
            inference_rule = (
              selected_step.inference_rule
            )
            selected_rule = (
              ""
              if inference_rule is None
              else inference_rule.name
            )

            row = {
              "n": n,
              "k": k,
              "group": group,
              "reference_number": (
                entry.number
              ),
              "reference": (
                _reference_title(
                  entry
                )
              ),
              "boundary_status": (
                boundary_status
              ),
              "boundary_locator": (
                boundary_locator
              ),
              "component_key": (
                component_key
              ),
              "ineligible_against": (
                ineligible_against
              ),
              "selected_rule": (
                selected_rule
              ),
              "selected_statement_type": (
                type(
                  selected_step.conclusion
                ).__name__
              ),
              "selected_statement": (
                rendered_statement
              ),
            }
            selected_rows.append(
              row
            )

            locator_key = (
              boundary_locator
              or _reference_title(
                entry
              )
            )
            locator_rows[
              locator_key
            ][
              "occurrences"
            ] += 1
            locator_rows[
              locator_key
            ][
              "groups"
            ].add(
              group
            )
            locator_rows[
              locator_key
            ][
              "statuses"
            ][
              boundary_status
            ] += 1

            if boundary_status in (
              "PROOF_INTERNAL",
              "FIXED_STATEMENT_INELIGIBLE",
              "FIXED_STATEMENT_WITHOUT_COMPONENT",
              "FIXED_STATEMENT_MISSING_COMPONENT",
            ):
              defect_rows.append(
                row
              )
              group_defects += 1

            if boundary_status == "UNTRACKED":
              group_untracked += 1

        group_rows.append(
          {
            "n": n,
            "k": k,
            "group": group,
            "raw_reference_entries": len(
              raw_entries
            ),
            "filtered_reference_entries": len(
              filtered_entries
            ),
            "removed_reference_entries": (
              len(
                raw_entries
              )
              - len(
                filtered_entries
              )
            ),
            "raw_selected_reference_steps": (
              raw_selected_count
            ),
            "selected_reference_steps": (
              group_selected
            ),
            "confirmed_defects": (
              group_defects
            ),
            "untracked": (
              group_untracked
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
            "group": group,
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
    "removed_reference_entries"
  ] = (
    totals[
      "raw_reference_entries"
    ]
    - totals[
      "filtered_reference_entries"
    ]
  )
  totals[
    "removed_selected_reference_steps"
  ] = (
    totals[
      "raw_selected_reference_steps"
    ]
    - totals[
      "selected_reference_steps"
    ]
  )

  confirmed_defect_statuses = (
    "PROOF_INTERNAL",
    "FIXED_STATEMENT_INELIGIBLE",
    "FIXED_STATEMENT_WITHOUT_COMPONENT",
    "FIXED_STATEMENT_MISSING_COMPONENT",
  )

  confirmed_defects = sum(
    status_counts[
      status
    ]
    for status in confirmed_defect_statuses
  )

  untracked = status_counts[
    "UNTRACKED"
  ]

  locator_inventory = []

  for locator in sorted(
    locator_rows
  ):
    payload = locator_rows[
      locator
    ]
    statuses = payload[
      "statuses"
    ]

    locator_inventory.append(
      {
        "reference": locator,
        "occurrences": payload[
          "occurrences"
        ],
        "affected_groups": len(
          payload[
            "groups"
          ]
        ),
        "fixed_statement": statuses[
          "FIXED_STATEMENT"
        ],
        "proof_internal": statuses[
          "PROOF_INTERNAL"
        ],
        "untracked": statuses[
          "UNTRACKED"
        ],
        "fixed_statement_ineligible": statuses[
          "FIXED_STATEMENT_INELIGIBLE"
        ],
        "fixed_statement_without_component": statuses[
          "FIXED_STATEMENT_WITHOUT_COMPONENT"
        ],
        "fixed_statement_missing_component": statuses[
          "FIXED_STATEMENT_MISSING_COMPONENT"
        ],
      }
    )

  status_order = (
    "FIXED_STATEMENT",
    "PROOF_INTERNAL",
    "UNTRACKED",
    "FIXED_STATEMENT_INELIGIBLE",
    "FIXED_STATEMENT_WITHOUT_COMPONENT",
    "FIXED_STATEMENT_MISSING_COMPONENT",
  )

  summary_lines = [
    "=" * 78,
    "Phase157-R5-R5 — 112-group Literature Statement Boundary re-audit",
    "=" * 78,
    (
      "scope: n=2..15, k=0..7, depth=2, "
      "semantic closure + generic R5-R4 boundary filter"
    ),
    "production changes: none",
    "existing test changes: none",
    "pytest: not run",
    "full Narrative rendering: not used",
    "",
    "Population:",
    (
      "  groups: "
      + str(
        totals[
          "groups"
        ]
      )
    ),
    (
      "  exceptions: "
      + str(
        totals[
          "exceptions"
        ]
      )
    ),
    "",
    "Before generic boundary filter:",
    (
      "  reference entries: "
      + str(
        totals[
          "raw_reference_entries"
        ]
      )
    ),
    (
      "  selected Reference steps: "
      + str(
        totals[
          "raw_selected_reference_steps"
        ]
      )
    ),
    "",
    "After generic boundary filter:",
    (
      "  reference entries: "
      + str(
        totals[
          "filtered_reference_entries"
        ]
      )
    ),
    (
      "  selected Reference steps: "
      + str(
        totals[
          "selected_reference_steps"
        ]
      )
    ),
    (
      "  removed reference entries: "
      + str(
        totals[
          "removed_reference_entries"
        ]
      )
    ),
    (
      "  removed selected-step population: "
      + str(
        totals[
          "removed_selected_reference_steps"
        ]
      )
    ),
    "",
    "Boundary classification after filter:",
  ]

  for status in status_order:
    summary_lines.append(
      "  "
      + status
      + ": occurrences="
      + str(
        status_counts[
          status
        ]
      )
      + ", affected_groups="
      + str(
        len(
          status_groups[
            status
          ]
        )
      )
    )

  summary_lines.extend(
    (
      "",
      "Confirmed boundary defects after filter:",
      (
        "  PROOF_INTERNAL selected as Reference: "
        + str(
          status_counts[
            "PROOF_INTERNAL"
          ]
        )
      ),
      (
        "  same-theorem fixed component but ineligible: "
        + str(
          status_counts[
            "FIXED_STATEMENT_INELIGIBLE"
          ]
        )
      ),
      (
        "  fixed statement without component key: "
        + str(
          status_counts[
            "FIXED_STATEMENT_WITHOUT_COMPONENT"
          ]
        )
      ),
      (
        "  fixed statement missing registered component: "
        + str(
          status_counts[
            "FIXED_STATEMENT_MISSING_COMPONENT"
          ]
        )
      ),
      (
        "  total confirmed defects: "
        + str(
          confirmed_defects
        )
      ),
      (
        "  UNTRACKED selected steps: "
        + str(
          untracked
        )
      ),
      "",
      "R5-R1 baseline comparison:",
      (
        "  confirmed defects: "
        + str(
          BASELINE_R5_R1[
            "confirmed_defects"
          ]
        )
        + " -> "
        + str(
          confirmed_defects
        )
      ),
      (
        "  UNTRACKED: "
        + str(
          BASELINE_R5_R1[
            "untracked"
          ]
        )
        + " -> "
        + str(
          untracked
        )
      ),
      (
        "  selected Reference steps: "
        + str(
          BASELINE_R5_R1[
            "selected_reference_steps"
          ]
        )
        + " -> "
        + str(
          totals[
            "selected_reference_steps"
          ]
        )
      ),
      "",
      "Completion criterion:",
      (
        "  groups == 112"
      ),
      (
        "  exceptions == 0"
      ),
      (
        "  confirmed boundary defects == 0"
      ),
      (
        "  UNTRACKED selected steps == 0"
      ),
      "",
      "Output files:",
      "  phase157_r5_r5_summary.txt",
      "  phase157_r5_r5_result.json",
      "  phase157_r5_r5_selected_steps.csv",
      "  phase157_r5_r5_confirmed_defects.csv",
      "  phase157_r5_r5_group_inventory.csv",
      "  phase157_r5_r5_locator_summary.csv",
      "  phase157_r5_r5_exceptions.csv",
      "=" * 78,
    )
  )

  passed = (
    totals[
      "groups"
    ] == EXPECTED_GROUPS
    and totals[
      "exceptions"
    ] == 0
    and confirmed_defects == 0
    and untracked == 0
  )

  summary_lines.extend(
    (
      "",
      (
        "AUDIT RESULT: PASS"
        if passed
        else "AUDIT RESULT: NEEDS REVIEW"
      ),
    )
  )

  summary = "\n".join(
    summary_lines
  ) + "\n"

  print(
    summary
  )

  (
    OUTPUT_DIR
    / "phase157_r5_r5_summary.txt"
  ).write_text(
    summary,
    encoding="utf-8",
  )

  result = {
    "phase": "157-R5-R5",
    "pass": passed,
    "scope": {
      "n_min": 2,
      "n_max": 15,
      "k_min": 0,
      "k_max": 7,
      "max_depth": MAX_DEPTH,
      "expected_groups": EXPECTED_GROUPS,
    },
    "production_changes": False,
    "existing_test_changes": False,
    "pytest_run": False,
    "full_narrative_rendering": False,
    "groups": totals[
      "groups"
    ],
    "exceptions": totals[
      "exceptions"
    ],
    "before_filter": {
      "reference_entries": totals[
        "raw_reference_entries"
      ],
      "selected_reference_steps": totals[
        "raw_selected_reference_steps"
      ],
    },
    "after_filter": {
      "reference_entries": totals[
        "filtered_reference_entries"
      ],
      "selected_reference_steps": totals[
        "selected_reference_steps"
      ],
      "removed_reference_entries": totals[
        "removed_reference_entries"
      ],
      "removed_selected_reference_steps": totals[
        "removed_selected_reference_steps"
      ],
    },
    "boundary_classification": {
      status: {
        "occurrences": status_counts[
          status
        ],
        "affected_groups": len(
          status_groups[
            status
          ]
        ),
      }
      for status in status_order
    },
    "confirmed_defects": confirmed_defects,
    "untracked": untracked,
    "r5_r1_baseline": BASELINE_R5_R1,
  }

  (
    OUTPUT_DIR
    / "phase157_r5_r5_result.json"
  ).write_text(
    json.dumps(
      result,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  selected_fields = (
    "n",
    "k",
    "group",
    "reference_number",
    "reference",
    "boundary_status",
    "boundary_locator",
    "component_key",
    "ineligible_against",
    "selected_rule",
    "selected_statement_type",
    "selected_statement",
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r5_selected_steps.csv",
    selected_rows,
    selected_fields,
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r5_confirmed_defects.csv",
    defect_rows,
    selected_fields,
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r5_group_inventory.csv",
    group_rows,
    (
      "n",
      "k",
      "group",
      "raw_reference_entries",
      "filtered_reference_entries",
      "removed_reference_entries",
      "raw_selected_reference_steps",
      "selected_reference_steps",
      "confirmed_defects",
      "untracked",
    ),
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r5_locator_summary.csv",
    locator_inventory,
    (
      "reference",
      "occurrences",
      "affected_groups",
      "fixed_statement",
      "proof_internal",
      "untracked",
      "fixed_statement_ineligible",
      "fixed_statement_without_component",
      "fixed_statement_missing_component",
    ),
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r5_exceptions.csv",
    exception_rows,
    (
      "n",
      "k",
      "group",
      "exception_type",
      "message",
      "traceback",
    ),
  )

  print(
    "Production files were NOT changed."
  )
  print(
    "Existing tests were NOT changed."
  )
  print(
    "Pytest was NOT run."
  )
  print(
    "Full Narrative rendering was NOT used."
  )

  return (
    0
    if passed
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
