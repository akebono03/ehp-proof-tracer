from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys
import traceback

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
OUTPUT_DIR = Path(
  "phase157_r5_r1_audit_output"
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


def _rule_name(
  proof_step,
) -> str:
  if proof_step.inference_rule is None:
    return str(
      proof_step.rule
    )

  return proof_step.inference_rule.name


def _boundary_status(
  proof_step,
  root_step,
) -> tuple[
  str,
  str,
  bool | None,
]:
  boundary = (
    classify_toda_literature_statement_step(
      proof_step
    )
  )

  if boundary is None:
    return (
      "UNTRACKED",
      "",
      None,
    )

  if (
    boundary.classification
    == TodaLiteratureStatementClassification.PROOF_INTERNAL
  ):
    return (
      "PROOF_INTERNAL",
      "",
      False,
    )

  component_key = (
    boundary.component_key
    or ""
  )

  if not component_key:
    return (
      "FIXED_STATEMENT_WITHOUT_COMPONENT",
      "",
      False,
    )

  component = (
    get_toda_fixed_statement_component(
      boundary.reference_locator,
      component_key,
    )
  )

  if component is None:
    return (
      "FIXED_STATEMENT_MISSING_COMPONENT",
      component_key,
      False,
    )

  root_boundary = (
    classify_toda_literature_statement_step(
      root_step
    )
  )

  if (
    root_boundary is None
    or root_boundary.component_key is None
  ):
    return (
      "FIXED_STATEMENT",
      component_key,
      True,
    )

  eligible = (
    is_toda_fixed_statement_component_reference_eligible(
      component,
      root_boundary.reference_locator,
      root_boundary.component_key,
    )
  )

  return (
    (
      "FIXED_STATEMENT"
      if eligible
      else "FIXED_STATEMENT_INELIGIBLE"
    ),
    component_key,
    eligible,
  )


def _write_csv(
  path: Path,
  rows: list[dict],
  fieldnames: tuple[
    str,
    ...,
  ],
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
    writer.writerows(
      rows
    )


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  totals = Counter()
  status_groups = defaultdict(
    set
  )
  locator_counts = Counter()
  locator_groups = defaultdict(
    set
  )
  selected_rows = []
  defect_rows = []
  group_rows = []
  exception_rows = []

  for n in N_RANGE:
    for k in K_RANGE:
      totals[
        "groups"
      ] += 1
      group = _group_label(
        n,
        k,
      )
      group_status_counts = Counter()

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
          ]
          .source_candidate
          .group_result
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

        root_step = presentation.root_step
        root_boundary = (
          classify_toda_literature_statement_step(
            root_step
          )
        )
        root_status = (
          "UNTRACKED"
          if root_boundary is None
          else root_boundary.classification.value
        )
        root_component_key = (
          ""
          if root_boundary is None
          else (
            root_boundary.component_key
            or ""
          )
        )

        entries = (
          build_toda_group_proof_narrative_reference_entries(
            presentation
          )
        )

        totals[
          "reference_entries"
        ] += len(
          entries
        )

        for entry in entries:
          candidates = (
            _candidate_steps(
              entry
            )
          )

          selected_steps = (
            select_toda_group_proof_narrative_reference_statement_steps(
              entry,
              candidates,
              presentation.edges,
              root_step=root_step,
            )
          )

          for selected_step in selected_steps:
            totals[
              "selected_steps"
            ] += 1

            (
              status,
              component_key,
              eligible,
            ) = _boundary_status(
              selected_step,
              root_step,
            )

            reference = (
              _reference_title(
                entry
              )
            )
            rendered = (
              _render_generic_narrative_step(
                selected_step
              )
            )

            group_status_counts[
              status
            ] += 1
            status_groups[
              status
            ].add(
              group
            )
            locator_counts[
              reference
            ] += 1
            locator_groups[
              reference
            ].add(
              group
            )

            row = {
              "n": n,
              "k": k,
              "group": group,
              "root_rule": _rule_name(
                root_step
              ),
              "root_boundary": (
                root_status
              ),
              "root_component_key": (
                root_component_key
              ),
              "reference": reference,
              "selected_rule": _rule_name(
                selected_step
              ),
              "selected_statement_type": type(
                selected_step.conclusion
              ).__name__,
              "selected_statement": rendered,
              "boundary_status": status,
              "component_key": (
                component_key
              ),
              "eligible": (
                ""
                if eligible is None
                else eligible
              ),
            }
            selected_rows.append(
              row
            )

            if status in (
              "PROOF_INTERNAL",
              "FIXED_STATEMENT_INELIGIBLE",
              "FIXED_STATEMENT_WITHOUT_COMPONENT",
              "FIXED_STATEMENT_MISSING_COMPONENT",
            ):
              defect_rows.append(
                row
              )

        group_rows.append(
          {
            "n": n,
            "k": k,
            "group": group,
            "root_boundary": (
              root_status
            ),
            "root_component_key": (
              root_component_key
            ),
            "reference_entries": len(
              entries
            ),
            "selected_steps": sum(
              group_status_counts.values()
            ),
            "fixed_statement": group_status_counts[
              "FIXED_STATEMENT"
            ],
            "proof_internal": group_status_counts[
              "PROOF_INTERNAL"
            ],
            "untracked": group_status_counts[
              "UNTRACKED"
            ],
            "fixed_ineligible": group_status_counts[
              "FIXED_STATEMENT_INELIGIBLE"
            ],
            "fixed_without_component": group_status_counts[
              "FIXED_STATEMENT_WITHOUT_COMPONENT"
            ],
            "fixed_missing_component": group_status_counts[
              "FIXED_STATEMENT_MISSING_COMPONENT"
            ],
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

  status_summary = []
  for status in (
    "FIXED_STATEMENT",
    "PROOF_INTERNAL",
    "UNTRACKED",
    "FIXED_STATEMENT_INELIGIBLE",
    "FIXED_STATEMENT_WITHOUT_COMPONENT",
    "FIXED_STATEMENT_MISSING_COMPONENT",
  ):
    count = sum(
      1
      for row in selected_rows
      if row[
        "boundary_status"
      ] == status
    )
    status_summary.append(
      {
        "status": status,
        "occurrences": count,
        "affected_groups": len(
          status_groups[
            status
          ]
        ),
      }
    )

  locator_rows = [
    {
      "reference": locator,
      "selected_occurrences": (
        locator_counts[
          locator
        ]
      ),
      "affected_groups": len(
        locator_groups[
          locator
        ]
      ),
      "fixed_occurrences": sum(
        1
        for row in selected_rows
        if (
          row[
            "reference"
          ] == locator
          and row[
            "boundary_status"
          ] == "FIXED_STATEMENT"
        )
      ),
      "proof_internal_occurrences": sum(
        1
        for row in selected_rows
        if (
          row[
            "reference"
          ] == locator
          and row[
            "boundary_status"
          ] == "PROOF_INTERNAL"
        )
      ),
      "untracked_occurrences": sum(
        1
        for row in selected_rows
        if (
          row[
            "reference"
          ] == locator
          and row[
            "boundary_status"
          ] == "UNTRACKED"
        )
      ),
      "ineligible_occurrences": sum(
        1
        for row in selected_rows
        if (
          row[
            "reference"
          ] == locator
          and row[
            "boundary_status"
          ] == "FIXED_STATEMENT_INELIGIBLE"
        )
      ),
    }
    for locator in sorted(
      locator_counts
    )
  ]

  confirmed_defects = len(
    defect_rows
  )
  untracked_count = sum(
    1
    for row in selected_rows
    if row[
      "boundary_status"
    ] == "UNTRACKED"
  )

  summary_lines = [
    "=" * 78,
    "Phase157-R5-R1 — 112-group Literature Statement Boundary cross-audit",
    "=" * 78,
    "scope: n=2..15, k=0..7, depth=2, semantic closure",
    "production changes: none",
    "existing test changes: none",
    "pytest: not run",
    "full Narrative rendering: not used",
    "",
    "groups: "
    + str(
      totals[
        "groups"
      ]
    ),
    "exceptions: "
    + str(
      totals[
        "exceptions"
      ]
    ),
    "reference entries: "
    + str(
      totals[
        "reference_entries"
      ]
    ),
    "selected Reference steps: "
    + str(
      totals[
        "selected_steps"
      ]
    ),
    "",
    "Boundary classification:",
  ]

  for row in status_summary:
    summary_lines.append(
      "  "
      + row[
        "status"
      ]
      + ": occurrences="
      + str(
        row[
          "occurrences"
        ]
      )
      + ", affected_groups="
      + str(
        row[
          "affected_groups"
        ]
      )
    )

  summary_lines.extend(
    (
      "",
      "Confirmed boundary defects:",
      (
        "  PROOF_INTERNAL selected as Reference: "
        + str(
          sum(
            1
            for row in defect_rows
            if row[
              "boundary_status"
            ] == "PROOF_INTERNAL"
          )
        )
      ),
      (
        "  same-theorem fixed component but ineligible: "
        + str(
          sum(
            1
            for row in defect_rows
            if row[
              "boundary_status"
            ] == "FIXED_STATEMENT_INELIGIBLE"
          )
        )
      ),
      (
        "  fixed statement without component key: "
        + str(
          sum(
            1
            for row in defect_rows
            if row[
              "boundary_status"
            ] == "FIXED_STATEMENT_WITHOUT_COMPONENT"
          )
        )
      ),
      (
        "  fixed statement missing registered component: "
        + str(
          sum(
            1
            for row in defect_rows
            if row[
              "boundary_status"
            ] == "FIXED_STATEMENT_MISSING_COMPONENT"
          )
        )
      ),
      (
        "  total confirmed defects: "
        + str(
          confirmed_defects
        )
      ),
      "",
      (
        "UNTRACKED selected steps requiring catalog review: "
        + str(
          untracked_count
        )
      ),
      "",
      "Interpretation:",
      (
        "  FIXED_STATEMENT is eligible under the currently registered "
        "Literature Statement Boundary."
      ),
      (
        "  PROOF_INTERNAL and FIXED_STATEMENT_INELIGIBLE are confirmed "
        "Reference-boundary defects."
      ),
      (
        "  UNTRACKED is not automatically a defect; it means the locator/rule "
        "has not yet been classified in the Phase157 boundary catalog."
      ),
      (
        "  R5-R1 does not alter production code. Its purpose is to measure "
        "the remaining population before deciding R5-R2 catalog expansion "
        "and selection integration."
      ),
      "",
      "Output files:",
      "  phase157_r5_r1_summary.txt",
      "  phase157_r5_r1_result.json",
      "  phase157_r5_r1_selected_steps.csv",
      "  phase157_r5_r1_confirmed_defects.csv",
      "  phase157_r5_r1_group_inventory.csv",
      "  phase157_r5_r1_locator_summary.csv",
      "  phase157_r5_r1_exceptions.csv",
      "=" * 78,
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
    / "phase157_r5_r1_summary.txt"
  ).write_text(
    summary,
    encoding="utf-8",
  )

  payload = {
    "phase": "157-R5-R1",
    "scope": {
      "n": "2..15",
      "k": "0..7",
      "depth": MAX_DEPTH,
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
    "reference_entries": totals[
      "reference_entries"
    ],
    "selected_steps": totals[
      "selected_steps"
    ],
    "status_summary": (
      status_summary
    ),
    "confirmed_defects": (
      confirmed_defects
    ),
    "untracked_selected_steps": (
      untracked_count
    ),
  }

  (
    OUTPUT_DIR
    / "phase157_r5_r1_result.json"
  ).write_text(
    json.dumps(
      payload,
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
    "root_rule",
    "root_boundary",
    "root_component_key",
    "reference",
    "selected_rule",
    "selected_statement_type",
    "selected_statement",
    "boundary_status",
    "component_key",
    "eligible",
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r1_selected_steps.csv",
    selected_rows,
    selected_fields,
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r1_confirmed_defects.csv",
    defect_rows,
    selected_fields,
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r1_group_inventory.csv",
    group_rows,
    (
      "n",
      "k",
      "group",
      "root_boundary",
      "root_component_key",
      "reference_entries",
      "selected_steps",
      "fixed_statement",
      "proof_internal",
      "untracked",
      "fixed_ineligible",
      "fixed_without_component",
      "fixed_missing_component",
    ),
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r1_locator_summary.csv",
    locator_rows,
    (
      "reference",
      "selected_occurrences",
      "affected_groups",
      "fixed_occurrences",
      "proof_internal_occurrences",
      "untracked_occurrences",
      "ineligible_occurrences",
    ),
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r1_exceptions.csv",
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

  if totals[
    "groups"
  ] != EXPECTED_GROUPS:
    print(
      "WARNING: expected 112 groups but saw "
      + str(
        totals[
          "groups"
        ]
      )
    )

  print(
    "AUDIT COMPLETE."
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

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
