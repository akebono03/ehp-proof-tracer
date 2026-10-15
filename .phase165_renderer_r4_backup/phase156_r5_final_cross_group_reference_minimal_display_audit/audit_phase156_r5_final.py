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


EXPECTED_GROUPS = 112


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


def _public_headers(
  rendered: str,
) -> tuple[
  tuple[
    int,
    int,
    str,
  ],
  ...,
]:
  result = []

  for line_index, line in enumerate(
    rendered.splitlines()
  ):
    match = re.match(
      r"^\*\*\[R([0-9]+)\]\s+(.+?)\.\*\*$",
      line.strip(),
    )

    if match is None:
      continue

    result.append(
      (
        line_index,
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


def _body_markers(
  rendered: str,
) -> tuple[
  int,
  ...,
]:
  header_indices = {
    line_index
    for line_index, _number, _title
    in _public_headers(
      rendered
    )
  }

  return tuple(
    int(
      number
    )
    for line_index, line in enumerate(
      rendered.splitlines()
    )
    if line_index not in header_indices
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
    )
    not in entry_step_ids
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


def _public_reference_prefix_end(
  rendered: str,
) -> int:
  lines = rendered.splitlines()
  headers = _public_headers(
    rendered
  )

  if not headers:
    return 0

  if "## 証明" in lines:
    return lines.index(
      "## 証明"
    )

  if "# Group proof narrative" in lines:
    group_index = lines.index(
      "# Group proof narrative"
    )

    if all(
      line_index < group_index
      for line_index, _number, _title in headers
    ):
      return group_index

  last_header_index = headers[
    -1
  ][
    0
  ]
  next_heading_index = len(
    lines
  )

  for index in range(
    last_header_index + 1,
    len(
      lines
    ),
  ):
    stripped = lines[
      index
    ].strip()

    if (
      stripped.startswith(
        "# "
      )
      or stripped.startswith(
        "## "
      )
    ):
      next_heading_index = index
      break

  return next_heading_index


def _proof_body_lines(
  rendered: str,
) -> tuple[
  str,
  ...,
]:
  lines = rendered.splitlines()

  if "## 証明" in lines:
    proof_index = lines.index(
      "## 証明"
    )
    return tuple(
      lines[
        proof_index + 1:
      ]
    )

  if "# Group proof narrative" in lines:
    group_index = lines.index(
      "# Group proof narrative"
    )
    headers = _public_headers(
      rendered
    )

    if (
      headers
      and all(
        line_index < group_index
        for line_index, _number, _title in headers
      )
    ):
      return tuple(
        lines[
          group_index + 1:
        ]
      )

  prefix_end = _public_reference_prefix_end(
    rendered
  )

  return tuple(
    lines[
      prefix_end:
    ]
  )


def _displayed_canonical_statements(
  presentation,
  rendered: str,
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

  prefix_end = _public_reference_prefix_end(
    rendered
  )
  reference_lines = rendered.splitlines()[
    :prefix_end
  ]

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


def _suppressible_restatements(
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
  result = []

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

      result.append(
        {
          "statement": statement,
          "line_number": (
            line_number
          ),
          "line": line,
        }
      )

  return tuple(
    result
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

  groups = 0
  exceptions = []
  violations = []
  group_rows = []
  violation_counts = Counter()
  violation_groups = defaultdict(
    set
  )

  public_reference_groups = 0
  public_headers = 0
  body_markers = 0
  header_without_marker_occurrences = 0
  header_without_marker_groups = set()
  selected_statements = 0
  displayed_canonical_statements = 0
  multi_statement_entries = 0
  max_selected_per_entry = 0

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      groups += 1
      group = _group_label(
        n,
        k,
      )

      try:
        report = build_standard_toda_report(
          n=n,
          k=k,
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
        raw = (
          build_toda_group_proof_presentation(
            replay
          )
        )
        presentation = (
          build_toda_group_proof_narrative_semantic_closure_presentation(
            raw
          )
        )
        rendered = (
          render_toda_group_proof_narrative_markdown(
            raw
          )
        )

        headers = _public_headers(
          rendered
        )
        header_numbers = tuple(
          number
          for _line_index, number, _title
          in headers
        )
        markers = _body_markers(
          rendered
        )
        marker_set = set(
          markers
        )
        header_set = set(
          header_numbers
        )

        if headers:
          public_reference_groups += 1

        public_headers += len(
          headers
        )
        body_markers += len(
          markers
        )

        missing_body_use = (
          header_set
          - marker_set
        )
        header_without_marker_occurrences += len(
          missing_body_use
        )

        if missing_body_use:
          header_without_marker_groups.add(
            group
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
          violation_groups[
            kind
          ].add(
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

        expected_headers = tuple(
          range(
            1,
            len(
              header_numbers
            )
            + 1,
          )
        )

        if header_numbers != expected_headers:
          add_violation(
            "non_contiguous_reference_headers",
            repr(
              header_numbers
            ),
          )

        missing_headers = (
          marker_set
          - header_set
        )

        if missing_headers:
          add_violation(
            "body_marker_without_header",
            repr(
              tuple(
                sorted(
                  missing_headers
                )
              )
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
        selected_statements += sum(
          len(
            lines
          )
          for lines in selected_by_number.values()
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
          external = (
            _entry_external_candidates(
              presentation,
              entry,
              candidates,
            )
          )

          max_selected_per_entry = max(
            max_selected_per_entry,
            len(
              selected
            ),
          )

          if len(
            selected
          ) > 1:
            multi_statement_entries += 1

          if boundary:
            if selected != boundary:
              add_violation(
                "boundary_selection_mismatch",
                (
                  "entry="
                  + str(
                    entry.number
                  )
                ),
              )
            continue

          if external:
            if selected != external:
              add_violation(
                "entry_external_selection_mismatch",
                (
                  "entry="
                  + str(
                    entry.number
                  )
                ),
              )
            continue

          if len(
            selected
          ) > 1:
            add_violation(
              "same_entry_internal_public_expansion",
              (
                "entry="
                + str(
                  entry.number
                )
              ),
            )

        displayed = (
          _displayed_canonical_statements(
            presentation,
            rendered,
          )
        )
        displayed_canonical_statements += len(
          displayed
        )
        body_lines = _proof_body_lines(
          rendered
        )
        restatements = (
          _suppressible_restatements(
            displayed,
            body_lines,
          )
        )

        for restatement in restatements:
          add_violation(
            "exact_reference_body_restatement",
            (
              "line="
              + str(
                restatement[
                  "line_number"
                ]
              )
              + ", statement="
              + str(
                restatement[
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
              markers
            ),
            "header_without_marker": len(
              missing_body_use
            ),
            "canonical_selected_statements": sum(
              len(
                lines
              )
              for lines in selected_by_number.values()
            ),
            "displayed_canonical_statements": len(
              displayed
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

  required_kinds = (
    "non_contiguous_reference_headers",
    "body_marker_without_header",
    "boundary_selection_mismatch",
    "entry_external_selection_mismatch",
    "same_entry_internal_public_expansion",
    "exact_reference_body_restatement",
  )

  summary_rows = [
    {
      "kind": kind,
      "occurrences": violation_counts.get(
        kind,
        0,
      ),
      "affected_groups": len(
        violation_groups.get(
          kind,
          set(),
        )
      ),
    }
    for kind in required_kinds
  ]

  _write_csv(
    output_dir
    / "phase156_r5_final_group_summary.csv",
    (
      "n",
      "k",
      "group",
      "public_reference_headers",
      "body_reference_markers",
      "header_without_marker",
      "canonical_selected_statements",
      "displayed_canonical_statements",
      "violations",
    ),
    group_rows,
  )

  _write_csv(
    output_dir
    / "phase156_r5_final_violations.csv",
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
    / "phase156_r5_final_violation_summary.csv",
    (
      "kind",
      "occurrences",
      "affected_groups",
    ),
    summary_rows,
  )

  _write_csv(
    output_dir
    / "phase156_r5_final_exceptions.csv",
    (
      "n",
      "k",
      "group",
      "exception_type",
      "exception_message",
    ),
    exceptions,
  )

  payload = {
    "phase": "Phase156-R5-final",
    "production_changes": False,
    "scope": {
      "n": "2..15",
      "k": "0..7",
      "depth": 2,
    },
    "groups": groups,
    "exceptions": len(
      exceptions
    ),
    "public_reference_groups": (
      public_reference_groups
    ),
    "public_reference_headers": (
      public_headers
    ),
    "body_reference_markers": (
      body_markers
    ),
    "header_without_marker_occurrences_informational": (
      header_without_marker_occurrences
    ),
    "header_without_marker_groups_informational": len(
      header_without_marker_groups
    ),
    "canonical_selected_statements": (
      selected_statements
    ),
    "displayed_canonical_statements": (
      displayed_canonical_statements
    ),
    "multi_statement_entries": (
      multi_statement_entries
    ),
    "max_selected_statements_in_one_entry": (
      max_selected_per_entry
    ),
    "required_violations": len(
      violations
    ),
    "violation_counts": {
      kind: violation_counts.get(
        kind,
        0,
      )
      for kind in required_kinds
    },
    "pass": (
      groups
      == EXPECTED_GROUPS
      and not exceptions
      and not violations
    ),
  }

  (
    output_dir
    / "phase156_r5_final_result.json"
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
    "Phase156-R5 — final 112-group cross-group Reference minimal-display audit",
    "=" * 78,
    "production changes: none",
    "scope: n=2..15, k=0..7, depth=2",
    "",
    "groups: "
    + str(
      groups
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
      public_headers
    ),
    "body Reference markers: "
    + str(
      body_markers
    ),
    (
      "header without marker (informational): occurrences="
      + str(
        header_without_marker_occurrences
      )
      + ", affected_groups="
      + str(
        len(
          header_without_marker_groups
        )
      )
    ),
    "canonical selected statements: "
    + str(
      selected_statements
    ),
    "displayed canonical statements: "
    + str(
      displayed_canonical_statements
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
    "Required cross-group violations:",
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
      "Total required violations: "
      + str(
        len(
          violations
        )
      ),
      "",
      "Contract:",
      (
        "  body marker -> matching Reference header is required."
      ),
      (
        "  Reference header -> explicit body marker is not required; "
        "generic rendering may retain a Reference by proof-graph usage."
      ),
      (
        "  Phase156-R3 statement-selection invariants and exact "
        "Reference/body non-duplication remain required."
      ),
      "=" * 78,
    ]
  )

  summary_text = "\n".join(
    summary
  ) + "\n"

  (
    output_dir
    / "phase156_r5_final_summary.txt"
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
      "phase156_r5_final_audit_output"
    ),
  )
  args = parser.parse_args()

  result = run_audit(
    args.output_dir
  )

  if result[
    "pass"
  ]:
    print(
      "PASS: all required Phase156-R5 Reference minimal-display "
      "invariants hold across 112 groups."
    )
    return 0

  print(
    "FAIL: required Phase156-R5 Reference minimal-display "
    "violations remain."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
