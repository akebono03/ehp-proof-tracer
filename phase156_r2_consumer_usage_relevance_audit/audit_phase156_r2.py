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
  _phase153_r6_reference_aggregate_component,
  _phase153_r6_render_reference_statement,
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  render_toda_group_proof_narrative_reference_entries_markdown,
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
EXPECTED_DUPLICATES = 117
EXPECTED_R1_OVERFULL = 103

CLASS_BOUNDARY_DIRECT = "boundary_direct_consumer"
CLASS_INTERNAL_ONLY = "internal_consumer_only"
CLASS_UNUSED = "no_consumer"
CLASS_AGGREGATE_PARTIAL = "aggregate_component_only"


def _group_label(n: int, k: int) -> str:
  return "pi_" + str(n + k) + "^" + str(n)


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
          + str(n)
          + ", k="
          + str(k)
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


def _public_body(
  rendered: str,
  canonical_reference_section: str,
) -> str:
  lines = rendered.splitlines()

  if "## 証明" in lines:
    proof_index = lines.index(
      "## 証明"
    )
    return "\n".join(
      lines[
        proof_index + 1:
      ]
    )

  if rendered.startswith(
    canonical_reference_section
  ):
    return rendered[
      len(
        canonical_reference_section
      ):
    ].lstrip()

  return rendered


def _normalize(text: str) -> str:
  normalized = text
  normalized = normalized.replace("\\[", "$")
  normalized = normalized.replace("\\]", "$")
  normalized = normalized.replace("$$", "$")
  normalized = normalized.replace("**", "")
  normalized = normalized.replace("`", "")
  normalized = re.sub(
    r"\s+",
    "",
    normalized,
  )
  return normalized


def _body_occurrences(
  body: str,
  statement_line: str,
) -> tuple[dict[str, object], ...]:
  result = []
  normalized_statement = _normalize(
    statement_line
  )

  for line_number, line in enumerate(
    body.splitlines(),
    start=1,
  ):
    if not normalized_statement:
      continue

    if normalized_statement not in _normalize(
      line
    ):
      continue

    result.append(
      {
        "line_number": line_number,
        "line": line,
      }
    )

  return tuple(
    result
  )


def classify_consumer_usage(
  *,
  has_external_consumer: bool,
  has_internal_consumer: bool,
  aggregate_component_used: bool,
) -> tuple[str, str]:
  if aggregate_component_used:
    return (
      CLASS_AGGREGATE_PARTIAL,
      (
        "the selected Reference source is an aggregate statement, "
        "but the current proof consumes exactly one rendered component"
      ),
    )

  if has_external_consumer:
    return (
      CLASS_BOUNDARY_DIRECT,
      (
        "the selected statement is a direct premise of a proof step "
        "outside the same Reference"
      ),
    )

  if has_internal_consumer:
    return (
      CLASS_INTERNAL_ONLY,
      (
        "the selected statement is consumed only inside the same "
        "Reference ancestry and has no direct boundary consumer"
      ),
    )

  return (
    CLASS_UNUSED,
    (
      "the selected statement has no outgoing proof edge and is retained "
      "only by the current fallback selection"
    ),
  )


def _selected_statement_records(
  presentation,
  entry,
) -> tuple[dict[str, object], ...]:
  candidate_steps = []
  rendered_by_step_id = {}
  seen_rendered_statements = set()

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

    if rendered_statement in seen_rendered_statements:
      continue

    seen_rendered_statements.add(
      rendered_statement
    )
    candidate_steps.append(
      proof_step
    )
    rendered_by_step_id[
      id(
        proof_step
      )
    ] = rendered_statement

  selected_steps = (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      tuple(
        candidate_steps
      ),
      presentation.edges,
      root_step=presentation.root_step,
    )
  )

  records = []

  for proof_step in selected_steps:
    raw_statement = rendered_by_step_id[
      id(
        proof_step
      )
    ]
    rendered_statement = (
      _phase153_r6_render_reference_statement(
        presentation,
        entry,
        proof_step,
        raw_statement,
      )
    )
    aggregate_component = (
      _phase153_r6_reference_aggregate_component(
        presentation,
        entry,
        proof_step,
      )
    )

    records.append(
      {
        "proof_step": proof_step,
        "raw_statement": raw_statement,
        "statement": rendered_statement,
        "aggregate_component_used": (
          aggregate_component is not None
        ),
      }
    )

  return tuple(
    records
  )


def _reference_title(reference) -> str:
  return (
    reference.locator
    or reference.label
  )


def _consumer_records(
  presentation,
  entry,
  proof_step,
) -> tuple[
  tuple[dict[str, str], ...],
  tuple[dict[str, str], ...],
]:
  external = []
  internal = []

  for edge in presentation.edges:
    if edge.premise_step is not proof_step:
      continue

    parent_step = edge.parent_step
    parent_reference = (
      extract_toda_group_proof_step_literature_reference(
        parent_step
      )
    )
    rendered_parent = (
      _render_generic_narrative_step(
        parent_step
      )
    )
    row = {
      "statement": rendered_parent,
      "reference": (
        ""
        if parent_reference is None
        else _reference_title(
          parent_reference
        )
      ),
    }

    if parent_reference == entry.reference:
      internal.append(
        row
      )
    else:
      external.append(
        row
      )

  return (
    tuple(
      external
    ),
    tuple(
      internal
    ),
  )


def _write_csv(
  path: Path,
  fieldnames: tuple[str, ...],
  rows: list[dict[str, object]],
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
) -> dict[str, object]:
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  usage_rows = []
  group_rows = []
  exceptions = []
  class_counts = Counter()
  class_groups = {
    CLASS_BOUNDARY_DIRECT: set(),
    CLASS_INTERNAL_ONLY: set(),
    CLASS_UNUSED: set(),
    CLASS_AGGREGATE_PARTIAL: set(),
  }

  groups_seen = 0
  duplicate_population = 0
  r1_overfull_population = 0

  for (
    n,
    k,
    raw_presentation,
    presentation,
  ) in _presentations():
    group = _group_label(
      n,
      k,
    )
    groups_seen += 1
    group_overfull = 0

    try:
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
      canonical_reference_section = (
        render_toda_group_proof_narrative_reference_entries_markdown(
          entries,
          selected_by_number,
        )
      )
      rendered = (
        render_toda_group_proof_narrative_markdown(
          raw_presentation
        )
      )
      body = _public_body(
        rendered,
        canonical_reference_section,
      )

      for entry in entries:
        selected_records = (
          _selected_statement_records(
            presentation,
            entry,
          )
        )
        statement_lines = (
          selected_by_number.get(
            entry.number,
            (),
          )
        )

        reconstructed_lines = tuple(
          str(
            record[
              "statement"
            ]
          )
          for record in selected_records
        )

        if reconstructed_lines != statement_lines:
          raise AssertionError(
            "selected statement/source-step reconstruction mismatch "
            "for "
            + group
            + " R"
            + str(
              entry.number
            )
          )

        reference_statement_count = len(
          statement_lines
        )

        for statement_index, record in enumerate(
          selected_records,
          start=1,
        ):
          statement_line = str(
            record[
              "statement"
            ]
          )
          occurrences = _body_occurrences(
            body,
            statement_line,
          )

          if not occurrences:
            continue

          duplicate_population += 1

          if reference_statement_count <= 1:
            continue

          r1_overfull_population += 1
          group_overfull += 1
          proof_step = record[
            "proof_step"
          ]
          external_consumers, internal_consumers = (
            _consumer_records(
              presentation,
              entry,
              proof_step,
            )
          )
          aggregate_component_used = bool(
            record[
              "aggregate_component_used"
            ]
          )
          classification, reason = (
            classify_consumer_usage(
              has_external_consumer=bool(
                external_consumers
              ),
              has_internal_consumer=bool(
                internal_consumers
              ),
              aggregate_component_used=(
                aggregate_component_used
              ),
            )
          )
          class_counts[
            classification
          ] += 1
          class_groups[
            classification
          ].add(
            group
          )

          usage_rows.append(
            {
              "n": n,
              "k": k,
              "group": group,
              "reference_number": entry.number,
              "reference_title": _reference_title(
                entry.reference
              ),
              "statement_index": statement_index,
              "reference_statement_count": (
                reference_statement_count
              ),
              "classification": classification,
              "reason": reason,
              "statement": statement_line,
              "raw_source_statement": str(
                record[
                  "raw_statement"
                ]
              ),
              "aggregate_component_used": (
                aggregate_component_used
              ),
              "external_consumer_count": len(
                external_consumers
              ),
              "internal_consumer_count": len(
                internal_consumers
              ),
              "external_consumers": " || ".join(
                consumer[
                  "statement"
                ]
                + (
                  ""
                  if not consumer[
                    "reference"
                  ]
                  else (
                    " ["
                    + consumer[
                      "reference"
                    ]
                    + "]"
                  )
                )
                for consumer in external_consumers
              ),
              "internal_consumers": " || ".join(
                consumer[
                  "statement"
                ]
                for consumer in internal_consumers
              ),
              "body_occurrence_count": len(
                occurrences
              ),
              "body_line_numbers": ";".join(
                str(
                  occurrence[
                    "line_number"
                  ]
                )
                for occurrence in occurrences
              ),
              "body_lines": " || ".join(
                str(
                  occurrence[
                    "line"
                  ]
                )
                for occurrence in occurrences
              ),
            }
          )

      group_rows.append(
        {
          "n": n,
          "k": k,
          "group": group,
          "r1_overfull_duplicate_count": (
            group_overfull
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

  partition_count = sum(
    class_counts.values()
  )

  _write_csv(
    output_dir
    / "phase156_r2_consumer_usage_classification.csv",
    (
      "n",
      "k",
      "group",
      "reference_number",
      "reference_title",
      "statement_index",
      "reference_statement_count",
      "classification",
      "reason",
      "statement",
      "raw_source_statement",
      "aggregate_component_used",
      "external_consumer_count",
      "internal_consumer_count",
      "external_consumers",
      "internal_consumers",
      "body_occurrence_count",
      "body_line_numbers",
      "body_lines",
    ),
    usage_rows,
  )

  _write_csv(
    output_dir
    / "phase156_r2_group_summary.csv",
    (
      "n",
      "k",
      "group",
      "r1_overfull_duplicate_count",
    ),
    group_rows,
  )

  summary_rows = [
    {
      "classification": classification,
      "occurrences": class_counts[
        classification
      ],
      "affected_groups": len(
        class_groups[
          classification
        ]
      ),
    }
    for classification in (
      CLASS_BOUNDARY_DIRECT,
      CLASS_INTERNAL_ONLY,
      CLASS_UNUSED,
      CLASS_AGGREGATE_PARTIAL,
    )
  ]

  _write_csv(
    output_dir
    / "phase156_r2_classification_summary.csv",
    (
      "classification",
      "occurrences",
      "affected_groups",
    ),
    summary_rows,
  )

  _write_csv(
    output_dir
    / "phase156_r2_exceptions.csv",
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
    "phase": "Phase156-R2",
    "scope": {
      "n": "2..15",
      "k": "0..7",
      "depth": MAX_DEPTH,
      "expected_groups": EXPECTED_GROUPS,
    },
    "production_changes": False,
    "groups_seen": groups_seen,
    "exceptions": len(
      exceptions
    ),
    "duplicate_population": duplicate_population,
    "expected_duplicate_population": EXPECTED_DUPLICATES,
    "r1_overfull_population": r1_overfull_population,
    "expected_r1_overfull_population": EXPECTED_R1_OVERFULL,
    "classification_counts": dict(
      class_counts
    ),
    "classification_affected_groups": {
      key: len(
        value
      )
      for key, value in class_groups.items()
    },
    "classification_partition_complete": (
      partition_count
      == r1_overfull_population
    ),
    "r2_boundary": (
      "R2 audits consumer usage only. It does not change Reference "
      "statement selection, rendering, body suppression, or proof data."
    ),
    "phase156_r3_boundary": (
      "R3 may convert the observed consumer classes into the minimal "
      "Reference statement selection rule."
    ),
  }

  (
    output_dir
    / "phase156_r2_result.json"
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
    "Phase156-R2 — consumer usage relevance audit",
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
    "R1 duplicate population reproduced: "
    + str(
      duplicate_population
    ),
    "R1 reference_side_overfull population: "
    + str(
      r1_overfull_population
    ),
    "",
    "Consumer usage classification:",
  ]

  for row in summary_rows:
    summary.append(
      "  "
      + str(
        row[
          "classification"
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
      "Interpretation:",
      (
        "  boundary_direct_consumer: the statement directly crosses the "
        "Reference boundary and is structurally relevant."
      ),
      (
        "  internal_consumer_only: the statement is used only inside the "
        "same Reference ancestry; R3 must decide whether it belongs in "
        "the public Reference summary."
      ),
      (
        "  no_consumer: the statement has no outgoing proof edge and is "
        "a strong candidate for Reference-side suppression."
      ),
      (
        "  aggregate_component_only: only one component of an aggregate "
        "Reference source is consumed; keep the component rather than "
        "the whole aggregate statement."
      ),
      "",
      "R2 boundary:",
      (
        "  No Reference selection/rendering/suppression behavior is "
        "changed in R2."
      ),
      (
        "  R3 is the first step allowed to turn these observations into "
        "a minimal-display rule."
      ),
      "",
      "Output files:",
      "  phase156_r2_consumer_usage_classification.csv",
      "  phase156_r2_group_summary.csv",
      "  phase156_r2_classification_summary.csv",
      "  phase156_r2_exceptions.csv",
      "  phase156_r2_result.json",
      "  phase156_r2_summary.txt",
      "=" * 78,
    ]
  )

  summary_text = "\n".join(
    summary
  ) + "\n"
  (
    output_dir
    / "phase156_r2_summary.txt"
  ).write_text(
    summary_text,
    encoding="utf-8",
  )
  print(
    summary_text
  )

  passed = (
    groups_seen
    == EXPECTED_GROUPS
    and not exceptions
    and duplicate_population
    == EXPECTED_DUPLICATES
    and r1_overfull_population
    == EXPECTED_R1_OVERFULL
    and partition_count
    == r1_overfull_population
  )

  if passed:
    print(
      "PASS: all 103 R1 overfull duplicates were classified by "
      "consumer usage."
    )
  else:
    print(
      "FAIL: Phase156-R2 population or classification invariant failed."
    )

  return payload


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--repo-root",
    type=Path,
    default=Path.cwd(),
  )
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=None,
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()
  output_dir = (
    args.output_dir.resolve()
    if args.output_dir is not None
    else (
      repo_root
      / "phase156_r2_audit_output"
    )
  )

  result = run_audit(
    output_dir
  )

  passed = (
    result[
      "groups_seen"
    ]
    == EXPECTED_GROUPS
    and result[
      "exceptions"
    ]
    == 0
    and result[
      "duplicate_population"
    ]
    == EXPECTED_DUPLICATES
    and result[
      "r1_overfull_population"
    ]
    == EXPECTED_R1_OVERFULL
    and result[
      "classification_partition_complete"
    ]
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
