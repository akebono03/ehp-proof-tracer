from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

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
  extract_toda_group_proof_step_literature_reference,
  select_toda_group_proof_narrative_reference_statement_steps,
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


N_RANGE = range(2, 16)
K_RANGE = range(0, 8)
MAX_DEPTH = 2
EXPECTED_GROUPS = 112

DERIVATION_TOKENS = (
  "これらから",
  "このことから",
  "したがって",
  "従って",
  "よって",
  "ゆえに",
  "以上より",
  "ここから",
  "計算",
  "導く",
  "導か",
  "得る",
  "従う",
  "分かる",
  "わかる",
  "示す",
  "確認",
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


def _normalize(
  text: str,
) -> str:
  normalized = text
  normalized = normalized.replace(
    "\\[",
    "$",
  )
  normalized = normalized.replace(
    "\\]",
    "$",
  )
  normalized = normalized.replace(
    "$$",
    "$",
  )
  normalized = normalized.replace(
    "**",
    "",
  )
  normalized = normalized.replace(
    "`",
    "",
  )
  normalized = re.sub(
    r"\s+",
    "",
    normalized,
  )
  return normalized


def _presentations():
  for n in N_RANGE:
    for k in K_RANGE:
      report = build_standard_toda_report(
        n=n,
        k=k,
      )

      if not report.candidates:
        raise AssertionError(
          "no report candidate for n="
          + str(
            n
          )
          + ", k="
          + str(
            k
          )
        )

      group_result = (
        report.candidates[
          0
        ].source_candidate.group_result
      )
      replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=MAX_DEPTH,
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

      yield (
        n,
        k,
        raw_presentation,
        presentation,
      )


def _public_sections(
  rendered: str,
) -> tuple[
  tuple[
    str,
    ...,
  ],
  tuple[
    str,
    ...,
  ],
]:
  lines = rendered.splitlines()

  if (
    "## 使用する結果" not in lines
    or "## 証明" not in lines
  ):
    return (
      (),
      tuple(
        lines
      ),
    )

  reference_index = lines.index(
    "## 使用する結果"
  )
  proof_index = lines.index(
    "## 証明"
  )

  if reference_index >= proof_index:
    return (
      (),
      tuple(
        lines
      ),
    )

  return (
    tuple(
      lines[
        reference_index
        + 1:
        proof_index
      ]
    ),
    tuple(
      lines[
        proof_index
        + 1:
      ]
    ),
  )


def _public_reference_headers(
  reference_lines: tuple[
    str,
    ...,
  ],
) -> tuple[
  tuple[
    int,
    str,
  ],
  ...,
]:
  result = []

  for line in reference_lines:
    match = re.match(
      r"^\*\*\[R([0-9]+)\]\s+(.+?)\.\*\*$",
      line.strip(),
    )

    if match is None:
      continue

    result.append(
      (
        int(
          match.group(
            1
          )
        ),
        match.group(
          2
        ),
      )
    )

  return tuple(
    result
  )


def _body_reference_markers(
  body_lines: tuple[
    str,
    ...,
  ],
) -> tuple[
  int,
  ...,
]:
  return tuple(
    int(
      number
    )
    for line in body_lines
    for number in re.findall(
      r"\[R([0-9]+)\]",
      line,
    )
  )


def _candidate_steps(
  entry,
) -> tuple:
  candidates = []
  seen_rendered = set()

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

    if rendered in seen_rendered:
      continue

    seen_rendered.add(
      rendered
    )
    candidates.append(
      proof_step
    )

  return tuple(
    candidates
  )


def _boundary_candidates(
  presentation,
  entry,
  candidates,
) -> tuple:
  boundary_ids = {
    id(
      edge.premise_step
    )
    for edge in presentation.edges
    if (
      edge.premise_step
      is not presentation.root_step
      and extract_toda_group_proof_step_literature_reference(
        edge.premise_step
      )
      == entry.reference
      and extract_toda_group_proof_step_literature_reference(
        edge.parent_step
      )
      != entry.reference
    )
  }

  return tuple(
    proof_step
    for proof_step in candidates
    if (
      proof_step is not presentation.root_step
      and id(
        proof_step
      )
      in boundary_ids
    )
  )


def _entry_external_candidates(
  presentation,
  entry,
  candidates,
) -> tuple:
  entry_step_ids = {
    id(
      proof_step
    )
    for proof_step in entry.proof_steps
  }
  external_used_ids = {
    id(
      edge.premise_step
    )
    for edge in presentation.edges
    if id(
      edge.parent_step
    ) not in entry_step_ids
  }

  return tuple(
    proof_step
    for proof_step in candidates
    if (
      proof_step is not presentation.root_step
      and id(
        proof_step
      )
      in external_used_ids
    )
  )


def _displayed_canonical_statements(
  presentation,
  reference_lines: tuple[
    str,
    ...,
  ],
) -> tuple[
  str,
  ...,
]:
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
  canonical = tuple(
    statement
    for statements in selected_by_number.values()
    for statement in statements
  )
  canonical_by_normalized = {
    _normalize(
      statement
    ): statement
    for statement in canonical
    if _normalize(
      statement
    )
  }

  displayed = []
  seen = set()

  for line in reference_lines:
    normalized = _normalize(
      line
    )
    statement = (
      canonical_by_normalized.get(
        normalized
      )
    )

    if statement is None:
      continue

    if normalized in seen:
      continue

    seen.add(
      normalized
    )
    displayed.append(
      statement
    )

  return tuple(
    displayed
  )


def _suppressible_body_restatements(
  displayed_statements: tuple[
    str,
    ...,
  ],
  body_lines: tuple[
    str,
    ...,
  ],
) -> tuple[
  dict[
    str,
    object,
  ],
  ...,
]:
  violations = []

  for statement in displayed_statements:
    normalized_statement = _normalize(
      statement
    )

    if not normalized_statement:
      continue

    for line_number, line in enumerate(
      body_lines,
      start=1,
    ):
      if normalized_statement not in _normalize(
        line
      ):
        continue

      if any(
        token in line
        for token in DERIVATION_TOKENS
      ):
        continue

      violations.append(
        {
          "statement": statement,
          "body_line_number": (
            line_number
          ),
          "body_line": line,
        }
      )

  return tuple(
    violations
  )


def classify_public_reference_structure(
  *,
  header_numbers: tuple[
    int,
    ...,
  ],
  body_markers: tuple[
    int,
    ...,
  ],
) -> tuple[
  tuple[
    int,
    ...,
  ],
  tuple[
    int,
    ...,
  ],
  bool,
]:
  header_set = set(
    header_numbers
  )
  marker_set = set(
    body_markers
  )

  missing_headers = tuple(
    sorted(
      marker_set
      - header_set
    )
  )
  unused_headers = tuple(
    sorted(
      header_set
      - marker_set
    )
  )
  contiguous = (
    header_numbers
    == tuple(
      range(
        1,
        len(
          header_numbers
        )
        + 1,
      )
    )
  )

  return (
    missing_headers,
    unused_headers,
    contiguous,
  )


def _write_csv(
  path: Path,
  fieldnames: tuple[
    str,
    ...,
  ],
  rows: list[
    dict[
      str,
      object,
    ]
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


def run_audit(
  output_dir: Path,
) -> dict[
  str,
  object,
]:
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  groups_seen = 0
  exceptions = []
  violations = []
  group_rows = []

  public_reference_groups = 0
  total_public_headers = 0
  total_body_markers = 0
  total_canonical_selected = 0
  total_displayed_canonical = 0
  multi_statement_entries = 0
  max_selected_per_entry = 0

  violation_counts = Counter()
  violation_groups = {}

  for (
    n,
    k,
    raw_presentation,
    presentation,
  ) in _presentations():
    groups_seen += 1
    group = _group_label(
      n,
      k,
    )

    try:
      rendered = (
        render_toda_group_proof_narrative_markdown(
          raw_presentation
        )
      )
      reference_lines, body_lines = (
        _public_sections(
          rendered
        )
      )
      headers = (
        _public_reference_headers(
          reference_lines
        )
      )
      header_numbers = tuple(
        number
        for number, _title in headers
      )
      body_markers = (
        _body_reference_markers(
          body_lines
        )
      )

      if headers:
        public_reference_groups += 1

      total_public_headers += len(
        headers
      )
      total_body_markers += len(
        body_markers
      )

      (
        missing_headers,
        unused_headers,
        contiguous,
      ) = (
        classify_public_reference_structure(
          header_numbers=header_numbers,
          body_markers=body_markers,
        )
      )

      group_violation_count = 0

      def add_violation(
        kind: str,
        detail: str,
      ) -> None:
        nonlocal group_violation_count

        group_violation_count += 1
        violation_counts[
          kind
        ] += 1
        violation_groups.setdefault(
          kind,
          set(),
        ).add(
          group
        )
        violations.append(
          {
            "n": n,
            "k": k,
            "group": group,
            "kind": kind,
            "detail": detail,
          }
        )

      if not contiguous:
        add_violation(
          "non_contiguous_reference_headers",
          repr(
            header_numbers
          ),
        )

      if missing_headers:
        add_violation(
          "body_marker_without_header",
          repr(
            missing_headers
          ),
        )

      if unused_headers:
        add_violation(
          "public_header_without_body_use",
          repr(
            unused_headers
          ),
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
      selected_count = sum(
        len(
          lines
        )
        for lines in selected_by_number.values()
      )
      total_canonical_selected += (
        selected_count
      )

      displayed_statements = (
        _displayed_canonical_statements(
          presentation,
          reference_lines,
        )
      )
      total_displayed_canonical += len(
        displayed_statements
      )

      for entry in entries:
        candidates = _candidate_steps(
          entry
        )
        selected = (
          select_toda_group_proof_narrative_reference_statement_steps(
            entry,
            candidates,
            presentation.edges,
            root_step=presentation.root_step,
          )
        )
        boundary = (
          _boundary_candidates(
            presentation,
            entry,
            candidates,
          )
        )
        entry_external = (
          _entry_external_candidates(
            presentation,
            entry,
            candidates,
          )
        )

        selected_len = len(
          selected
        )
        max_selected_per_entry = max(
          max_selected_per_entry,
          selected_len,
        )

        if selected_len > 1:
          multi_statement_entries += 1

        if boundary:
          if selected != boundary:
            add_violation(
              "boundary_selection_mismatch",
              (
                "reference="
                + str(
                  entry.reference.locator
                  or entry.reference.label
                )
                + ", selected="
                + str(
                  selected_len
                )
                + ", boundary="
                + str(
                  len(
                    boundary
                  )
                )
              ),
            )
          continue

        if entry_external:
          if selected != entry_external:
            add_violation(
              "entry_external_selection_mismatch",
              (
                "reference="
                + str(
                  entry.reference.locator
                  or entry.reference.label
                )
                + ", selected="
                + str(
                  selected_len
                )
                + ", entry_external="
                + str(
                  len(
                    entry_external
                  )
                )
              ),
            )
          continue

        if selected_len > 1:
          add_violation(
            "same_entry_internal_public_expansion",
            (
              "reference="
              + str(
                entry.reference.locator
                or entry.reference.label
              )
              + ", selected="
              + str(
                selected_len
              )
            ),
          )

      suppressible = (
        _suppressible_body_restatements(
          displayed_statements,
          body_lines,
        )
      )

      for item in suppressible:
        add_violation(
          "suppressible_exact_body_restatement",
          (
            "line="
            + str(
              item[
                "body_line_number"
              ]
            )
            + ", statement="
            + str(
              item[
                "statement"
              ]
            )
          ),
        )

      group_rows.append(
        {
          "n": n,
          "k": k,
          "group": group,
          "public_reference_headers": len(
            headers
          ),
          "body_reference_markers": len(
            body_markers
          ),
          "canonical_selected_statements": (
            selected_count
          ),
          "displayed_canonical_statements": len(
            displayed_statements
          ),
          "violations": (
            group_violation_count
          ),
        }
      )

    except Exception as exc:
      exceptions.append(
        {
          "n": n,
          "k": k,
          "group": group,
          "exception_type": type(
            exc
          ).__name__,
          "exception_message": str(
            exc
          ),
        }
      )

  _write_csv(
    output_dir
    / "phase156_r5_group_summary.csv",
    (
      "n",
      "k",
      "group",
      "public_reference_headers",
      "body_reference_markers",
      "canonical_selected_statements",
      "displayed_canonical_statements",
      "violations",
    ),
    group_rows,
  )

  _write_csv(
    output_dir
    / "phase156_r5_violations.csv",
    (
      "n",
      "k",
      "group",
      "kind",
      "detail",
    ),
    violations,
  )

  _write_csv(
    output_dir
    / "phase156_r5_exceptions.csv",
    (
      "n",
      "k",
      "group",
      "exception_type",
      "exception_message",
    ),
    exceptions,
  )

  summary_rows = [
    {
      "kind": kind,
      "occurrences": violation_counts[
        kind
      ],
      "affected_groups": len(
        violation_groups.get(
          kind,
          set(),
        )
      ),
    }
    for kind in (
      "non_contiguous_reference_headers",
      "body_marker_without_header",
      "public_header_without_body_use",
      "boundary_selection_mismatch",
      "entry_external_selection_mismatch",
      "same_entry_internal_public_expansion",
      "suppressible_exact_body_restatement",
    )
  ]

  _write_csv(
    output_dir
    / "phase156_r5_violation_summary.csv",
    (
      "kind",
      "occurrences",
      "affected_groups",
    ),
    summary_rows,
  )

  payload = {
    "phase": "Phase156-R5",
    "scope": {
      "n": "2..15",
      "k": "0..7",
      "depth": MAX_DEPTH,
    },
    "production_changes": False,
    "groups_seen": groups_seen,
    "exceptions": len(
      exceptions
    ),
    "public_reference_groups": (
      public_reference_groups
    ),
    "public_reference_headers": (
      total_public_headers
    ),
    "body_reference_markers": (
      total_body_markers
    ),
    "canonical_selected_statements": (
      total_canonical_selected
    ),
    "displayed_canonical_statements": (
      total_displayed_canonical
    ),
    "multi_statement_entries": (
      multi_statement_entries
    ),
    "max_selected_per_entry": (
      max_selected_per_entry
    ),
    "violations": len(
      violations
    ),
    "violation_counts": dict(
      violation_counts
    ),
    "all_cross_group_invariants_pass": (
      groups_seen
      == EXPECTED_GROUPS
      and not exceptions
      and not violations
    ),
    "phase156_r6_boundary": (
      "R6 is focused/sharded regression. No Reference selection, "
      "rendering, or proof-body rule changes are allowed unless R5 "
      "identifies a concrete invariant violation."
    ),
  }

  (
    output_dir
    / "phase156_r5_result.json"
  ).write_text(
    json.dumps(
      payload,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  summary = [
    "=" * 78,
    "Phase156-R5 — 112-group cross-group Reference minimal-display audit",
    "=" * 78,
    "production changes: none",
    "scope: n=2..15, k=0..7, depth=2",
    "",
    "groups: "
    + str(
      groups_seen
    ),
    "exceptions: "
    + str(
      len(
        exceptions
      )
    ),
    "public Reference groups: "
    + str(
      public_reference_groups
    ),
    "public Reference headers: "
    + str(
      total_public_headers
    ),
    "body Reference markers: "
    + str(
      total_body_markers
    ),
    "canonical selected statements: "
    + str(
      total_canonical_selected
    ),
    "displayed canonical statements: "
    + str(
      total_displayed_canonical
    ),
    "multi-statement entries: "
    + str(
      multi_statement_entries
    ),
    "max selected statements in one entry: "
    + str(
      max_selected_per_entry
    ),
    "",
    "Cross-group violations:",
  ]

  for row in summary_rows:
    summary.append(
      "  "
      + str(
        row[
          "kind"
        ]
      )
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

  summary.extend(
    [
      "",
      "Total violations: "
      + str(
        len(
          violations
        )
      ),
      "",
      "R5 boundary:",
      (
        "  This step is audit-only. It does not change Reference "
        "selection, Reference rendering, proof-body suppression, "
        "or proof data."
      ),
      (
        "  If violations are zero, R6 may proceed to focused/sharded "
        "regression without new production behavior."
      ),
      "=" * 78,
    ]
  )

  summary_text = "\n".join(
    summary
  ) + "\n"

  (
    output_dir
    / "phase156_r5_summary.txt"
  ).write_text(
    summary_text,
    encoding="utf-8",
  )

  print(
    summary_text
  )

  return payload


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r5_audit_output"
    ),
  )
  args = parser.parse_args()

  result = run_audit(
    args.output_dir
  )

  passed = bool(
    result[
      "all_cross_group_invariants_pass"
    ]
  )

  if passed:
    print(
      "PASS: all Phase156-R5 cross-group Reference minimal-display "
      "invariants hold across 112 groups."
    )
    return 0

  print(
    "FAIL: Phase156-R5 found cross-group Reference minimal-display "
    "violations."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
