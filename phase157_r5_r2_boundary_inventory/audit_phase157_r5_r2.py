from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys


INPUT_DIR = Path(
  "phase157_r5_r1_audit_output"
)
SELECTED_CSV = (
  INPUT_DIR
  / "phase157_r5_r1_selected_steps.csv"
)
OUTPUT_DIR = Path(
  "phase157_r5_r2_inventory_output"
)

STATUS_UNTRACKED = "UNTRACKED"
STATUS_FIXED_WITHOUT_COMPONENT = (
  "FIXED_STATEMENT_WITHOUT_COMPONENT"
)
STATUS_PROOF_INTERNAL = "PROOF_INTERNAL"
STATUS_FIXED_INELIGIBLE = (
  "FIXED_STATEMENT_INELIGIBLE"
)


def _read_rows(
  path: Path,
) -> list[dict[str, str]]:
  with path.open(
    "r",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    return list(
      csv.DictReader(
        handle
      )
    )


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


def _group_key(
  row: dict[str, str],
) -> str:
  return row[
    "group"
  ]


def _stable_unique(
  values,
) -> tuple[str, ...]:
  seen = set()
  result = []

  for value in values:
    if value in seen:
      continue

    seen.add(
      value
    )
    result.append(
      value
    )

  return tuple(
    result
  )


def _aggregate_by_locator(
  rows: list[dict[str, str]],
) -> list[dict[str, object]]:
  grouped = defaultdict(
    list
  )

  for row in rows:
    grouped[
      row[
        "reference"
      ]
    ].append(
      row
    )

  result = []

  for locator in sorted(
    grouped
  ):
    locator_rows = grouped[
      locator
    ]
    statuses = Counter(
      row[
        "boundary_status"
      ]
      for row in locator_rows
    )
    rules = _stable_unique(
      row[
        "selected_rule"
      ]
      for row in locator_rows
    )
    statement_types = _stable_unique(
      row[
        "selected_statement_type"
      ]
      for row in locator_rows
    )
    groups = _stable_unique(
      _group_key(
        row
      )
      for row in locator_rows
    )

    result.append(
      {
        "reference": locator,
        "occurrences": len(
          locator_rows
        ),
        "affected_groups": len(
          groups
        ),
        "distinct_rules": len(
          rules
        ),
        "distinct_statement_types": len(
          statement_types
        ),
        "untracked": statuses[
          STATUS_UNTRACKED
        ],
        "fixed_without_component": statuses[
          STATUS_FIXED_WITHOUT_COMPONENT
        ],
        "proof_internal": statuses[
          STATUS_PROOF_INTERNAL
        ],
        "fixed_ineligible": statuses[
          STATUS_FIXED_INELIGIBLE
        ],
        "rules": " | ".join(
          rules
        ),
        "statement_types": " | ".join(
          statement_types
        ),
        "groups": " ".join(
          groups
        ),
      }
    )

  return result


def _aggregate_by_rule(
  rows: list[dict[str, str]],
) -> list[dict[str, object]]:
  grouped = defaultdict(
    list
  )

  for row in rows:
    grouped[
      (
        row[
          "reference"
        ],
        row[
          "selected_rule"
        ],
        row[
          "boundary_status"
        ],
      )
    ].append(
      row
    )

  result = []

  for key in sorted(
    grouped
  ):
    (
      locator,
      rule,
      status,
    ) = key
    rule_rows = grouped[
      key
    ]
    statement_types = _stable_unique(
      row[
        "selected_statement_type"
      ]
      for row in rule_rows
    )
    statements = _stable_unique(
      row[
        "selected_statement"
      ]
      for row in rule_rows
    )
    groups = _stable_unique(
      _group_key(
        row
      )
      for row in rule_rows
    )
    root_rules = _stable_unique(
      row[
        "root_rule"
      ]
      for row in rule_rows
    )

    result.append(
      {
        "reference": locator,
        "boundary_status": status,
        "selected_rule": rule,
        "occurrences": len(
          rule_rows
        ),
        "affected_groups": len(
          groups
        ),
        "distinct_statement_types": len(
          statement_types
        ),
        "distinct_rendered_statements": len(
          statements
        ),
        "statement_types": " | ".join(
          statement_types
        ),
        "groups": " ".join(
          groups
        ),
        "root_rules": " | ".join(
          root_rules
        ),
        "sample_statement": (
          statements[
            0
          ]
          if statements
          else ""
        ),
      }
    )

  return result


def _aggregate_by_statement_type(
  rows: list[dict[str, str]],
) -> list[dict[str, object]]:
  grouped = defaultdict(
    list
  )

  for row in rows:
    grouped[
      (
        row[
          "boundary_status"
        ],
        row[
          "selected_statement_type"
        ],
      )
    ].append(
      row
    )

  result = []

  for key in sorted(
    grouped
  ):
    status, statement_type = key
    type_rows = grouped[
      key
    ]
    locators = _stable_unique(
      row[
        "reference"
      ]
      for row in type_rows
    )
    rules = _stable_unique(
      row[
        "selected_rule"
      ]
      for row in type_rows
    )
    groups = _stable_unique(
      _group_key(
        row
      )
      for row in type_rows
    )

    result.append(
      {
        "boundary_status": status,
        "statement_type": statement_type,
        "occurrences": len(
          type_rows
        ),
        "affected_groups": len(
          groups
        ),
        "distinct_locators": len(
          locators
        ),
        "distinct_rules": len(
          rules
        ),
        "locators": " | ".join(
          locators
        ),
        "groups": " ".join(
          groups
        ),
      }
    )

  return result


def _candidate_priority(
  row: dict[str, object],
) -> tuple:
  status = str(
    row[
      "boundary_status"
    ]
  )

  priority_by_status = {
    STATUS_FIXED_WITHOUT_COMPONENT: 0,
    STATUS_UNTRACKED: 1,
  }

  return (
    priority_by_status.get(
      status,
      9,
    ),
    -int(
      row[
        "affected_groups"
      ]
    ),
    -int(
      row[
        "occurrences"
      ]
    ),
    str(
      row[
        "reference"
      ]
    ),
    str(
      row[
        "selected_rule"
      ]
    ),
  )


def main() -> int:
  if not SELECTED_CSV.exists():
    print(
      "ERROR: R5-R1 selected-step CSV was not found:"
    )
    print(
      SELECTED_CSV.resolve()
    )
    print(
      "Run Phase157-R5-R1 first."
    )
    return 1

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  all_rows = _read_rows(
    SELECTED_CSV
  )

  untracked_rows = [
    row
    for row in all_rows
    if row[
      "boundary_status"
    ] == STATUS_UNTRACKED
  ]

  fixed_without_component_rows = [
    row
    for row in all_rows
    if row[
      "boundary_status"
    ] == STATUS_FIXED_WITHOUT_COMPONENT
  ]

  review_rows = [
    row
    for row in all_rows
    if row[
      "boundary_status"
    ]
    in (
      STATUS_UNTRACKED,
      STATUS_FIXED_WITHOUT_COMPONENT,
    )
  ]

  locator_rows = _aggregate_by_locator(
    review_rows
  )
  rule_rows = _aggregate_by_rule(
    review_rows
  )
  statement_type_rows = (
    _aggregate_by_statement_type(
      review_rows
    )
  )

  catalog_candidate_rows = sorted(
    (
      row
      for row in rule_rows
      if row[
        "boundary_status"
      ]
      in (
        STATUS_UNTRACKED,
        STATUS_FIXED_WITHOUT_COMPONENT,
      )
    ),
    key=_candidate_priority,
  )

  untracked_locators = sorted(
    {
      row[
        "reference"
      ]
      for row in untracked_rows
    }
  )
  fixed_without_component_locators = sorted(
    {
      row[
        "reference"
      ]
      for row in fixed_without_component_rows
    }
  )

  untracked_rules = {
    (
      row[
        "reference"
      ],
      row[
        "selected_rule"
      ],
    )
    for row in untracked_rows
  }

  fixed_without_component_rules = {
    (
      row[
        "reference"
      ],
      row[
        "selected_rule"
      ],
    )
    for row in fixed_without_component_rows
  }

  summary_lines = [
    "=" * 78,
    "Phase157-R5-R2 — Literature boundary inventory",
    "=" * 78,
    "source: Phase157-R5-R1 selected-step CSV",
    "production changes: none",
    "existing test changes: none",
    "pytest: not run",
    "proof replay: not rerun",
    "Narrative rendering: not run",
    "",
    "R5-R1 rows loaded: "
    + str(
      len(
        all_rows
      )
    ),
    "",
    "UNTRACKED:",
    "  occurrences: "
    + str(
      len(
        untracked_rows
      )
    ),
    "  distinct locators: "
    + str(
      len(
        untracked_locators
      )
    ),
    "  distinct locator/rule pairs: "
    + str(
      len(
        untracked_rules
      )
    ),
    "",
    "FIXED_STATEMENT_WITHOUT_COMPONENT:",
    "  occurrences: "
    + str(
      len(
        fixed_without_component_rows
      )
    ),
    "  distinct locators: "
    + str(
      len(
        fixed_without_component_locators
      )
    ),
    "  distinct locator/rule pairs: "
    + str(
      len(
        fixed_without_component_rules
      )
    ),
    "",
    "UNTRACKED locators:",
  ]

  if untracked_locators:
    summary_lines.extend(
      "  " + locator
      for locator in untracked_locators
    )
  else:
    summary_lines.append(
      "  (none)"
    )

  summary_lines.extend(
    (
      "",
      "FIXED_STATEMENT_WITHOUT_COMPONENT locators:",
    )
  )

  if fixed_without_component_locators:
    summary_lines.extend(
      "  " + locator
      for locator
      in fixed_without_component_locators
    )
  else:
    summary_lines.append(
      "  (none)"
    )

  summary_lines.extend(
    (
      "",
      "R5-R3 preparation:",
      (
        "  Review catalog_candidates.csv from top to bottom. "
        "Each row is one locator/rule unit that can be assigned "
        "a fixed-statement component or classified as proof-internal."
      ),
      (
        "  FIXED_STATEMENT_WITHOUT_COMPONENT rows come first because "
        "their fixed/proof-internal classification is already known; "
        "only component granularity is missing."
      ),
      (
        "  UNTRACKED rows still require literature/source review before "
        "production catalog changes."
      ),
      "",
      "Output files:",
      "  phase157_r5_r2_summary.txt",
      "  phase157_r5_r2_result.json",
      "  phase157_r5_r2_locator_inventory.csv",
      "  phase157_r5_r2_rule_inventory.csv",
      "  phase157_r5_r2_statement_type_inventory.csv",
      "  phase157_r5_r2_catalog_candidates.csv",
      "  phase157_r5_r2_untracked_rows.csv",
      "  phase157_r5_r2_fixed_without_component_rows.csv",
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
    / "phase157_r5_r2_summary.txt"
  ).write_text(
    summary,
    encoding="utf-8",
  )

  result = {
    "phase": "157-R5-R2",
    "source": str(
      SELECTED_CSV
    ),
    "production_changes": False,
    "existing_test_changes": False,
    "pytest_run": False,
    "proof_replay_rerun": False,
    "narrative_rendering": False,
    "rows_loaded": len(
      all_rows
    ),
    "untracked": {
      "occurrences": len(
        untracked_rows
      ),
      "distinct_locators": len(
        untracked_locators
      ),
      "distinct_locator_rule_pairs": len(
        untracked_rules
      ),
      "locators": (
        untracked_locators
      ),
    },
    "fixed_without_component": {
      "occurrences": len(
        fixed_without_component_rows
      ),
      "distinct_locators": len(
        fixed_without_component_locators
      ),
      "distinct_locator_rule_pairs": len(
        fixed_without_component_rules
      ),
      "locators": (
        fixed_without_component_locators
      ),
    },
    "catalog_candidate_rows": len(
      catalog_candidate_rows
    ),
  }

  (
    OUTPUT_DIR
    / "phase157_r5_r2_result.json"
  ).write_text(
    json.dumps(
      result,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r2_locator_inventory.csv",
    locator_rows,
    (
      "reference",
      "occurrences",
      "affected_groups",
      "distinct_rules",
      "distinct_statement_types",
      "untracked",
      "fixed_without_component",
      "proof_internal",
      "fixed_ineligible",
      "rules",
      "statement_types",
      "groups",
    ),
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r2_rule_inventory.csv",
    rule_rows,
    (
      "reference",
      "boundary_status",
      "selected_rule",
      "occurrences",
      "affected_groups",
      "distinct_statement_types",
      "distinct_rendered_statements",
      "statement_types",
      "groups",
      "root_rules",
      "sample_statement",
    ),
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r2_statement_type_inventory.csv",
    statement_type_rows,
    (
      "boundary_status",
      "statement_type",
      "occurrences",
      "affected_groups",
      "distinct_locators",
      "distinct_rules",
      "locators",
      "groups",
    ),
  )

  _write_csv(
    OUTPUT_DIR
    / "phase157_r5_r2_catalog_candidates.csv",
    catalog_candidate_rows,
    (
      "reference",
      "boundary_status",
      "selected_rule",
      "occurrences",
      "affected_groups",
      "distinct_statement_types",
      "distinct_rendered_statements",
      "statement_types",
      "groups",
      "root_rules",
      "sample_statement",
    ),
  )

  selected_fields = tuple(
    all_rows[
      0
    ].keys()
  ) if all_rows else ()

  if selected_fields:
    _write_csv(
      OUTPUT_DIR
      / "phase157_r5_r2_untracked_rows.csv",
      untracked_rows,
      selected_fields,
    )

    _write_csv(
      OUTPUT_DIR
      / "phase157_r5_r2_fixed_without_component_rows.csv",
      fixed_without_component_rows,
      selected_fields,
    )

  print(
    "INVENTORY COMPLETE."
  )
  print(
    "Production files were NOT changed."
  )
  print(
    "Existing tests were NOT changed."
  )
  print(
    "R5-R1 proof replay was NOT rerun."
  )
  print(
    "Pytest was NOT run."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
