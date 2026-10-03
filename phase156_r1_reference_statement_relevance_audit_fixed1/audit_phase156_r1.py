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
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
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

CLASS_UNNECESSARY = "unnecessary_duplicate"
CLASS_BODY_REQUIRED = "body_restatement_required"
CLASS_REFERENCE_OVERFULL = "reference_side_overfull"

DERIVATION_TOKENS = (
  "これより",
  "したがって",
  "従って",
  "よって",
  "ゆえに",
  "以上より",
  "この結果",
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
  "exactness",
  "完全性",
)

REFERENCE_USE_PATTERNS = (
  "を用いる",
  "により",
  "から",
)


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

    stripped = line.strip()
    normalized_line = _normalize(
      stripped
    )
    standalone = (
      normalized_line
      == normalized_statement
    )
    result.append(
      {
        "line_number": line_number,
        "line": line,
        "standalone": standalone,
      }
    )

  return tuple(
    result
  )


def classify_duplicate(
  *,
  reference_number: int,
  statement_line: str,
  reference_statement_count: int,
  body_occurrences: tuple[dict[str, object], ...],
) -> tuple[str, str]:
  if not body_occurrences:
    raise ValueError(
      "body_occurrences must not be empty"
    )

  marker = (
    "[R"
    + str(
      reference_number
    )
    + "]"
  )
  context = "\n".join(
    str(
      occurrence[
        "line"
      ]
    )
    for occurrence in body_occurrences
  )

  if reference_statement_count > 1:
    return (
      CLASS_REFERENCE_OVERFULL,
      (
        "the Reference currently exposes multiple selected statements; "
        "R2 must decide from consumer usage whether this duplicated "
        "component is actually required"
      ),
    )

  if any(
    bool(
      occurrence[
        "standalone"
      ]
    )
    for occurrence in body_occurrences
  ):
    return (
      CLASS_UNNECESSARY,
      (
        "the selected Reference statement is repeated as a standalone "
        "body line and carries no additional derivation context"
      ),
    )

  has_marker = marker in context
  has_reference_use_prose = any(
    token in context
    for token in REFERENCE_USE_PATTERNS
  )
  has_derivation_context = any(
    token in context
    for token in DERIVATION_TOKENS
  )

  if (
    has_marker
    and has_reference_use_prose
    and not has_derivation_context
  ):
    return (
      CLASS_UNNECESSARY,
      (
        "the body occurrence already attributes the fact to the same "
        "Reference and adds no detected derivation context"
      ),
    )

  if has_derivation_context:
    return (
      CLASS_BODY_REQUIRED,
      (
        "the exact statement occurs inside a body sentence carrying "
        "calculation/derivation context; R1 preserves it as body-needed"
      ),
    )

  if has_marker:
    return (
      CLASS_UNNECESSARY,
      (
        "the body occurrence is already connected to the same Reference "
        "marker without detected calculation/derivation context"
      ),
    )

  return (
    CLASS_BODY_REQUIRED,
    (
      "the body occurrence is embedded in proof prose without a direct "
      "Reference-only form; R1 conservatively treats it as body-needed"
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

  duplicate_rows = []
  group_rows = []
  exceptions = []
  classification_counts = Counter()
  classification_groups = {
    CLASS_UNNECESSARY: set(),
    CLASS_BODY_REQUIRED: set(),
    CLASS_REFERENCE_OVERFULL: set(),
  }

  groups_seen = 0

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
      body = (
        _public_body(
          rendered,
          canonical_reference_section,
        )
      )

      duplicates_in_group = 0

      for entry in entries:
        statement_lines = (
          selected_by_number.get(
            entry.number,
            (),
          )
        )
        reference_statement_count = len(
          statement_lines
        )

        for statement_index, statement_line in enumerate(
          statement_lines,
          start=1,
        ):
          occurrences = (
            _body_occurrences(
              body,
              statement_line,
            )
          )

          if not occurrences:
            continue

          duplicates_in_group += 1
          classification, reason = classify_duplicate(
            reference_number=entry.number,
            statement_line=statement_line,
            reference_statement_count=reference_statement_count,
            body_occurrences=occurrences,
          )
          classification_counts[
            classification
          ] += 1
          classification_groups[
            classification
          ].add(
            group
          )

          title = (
            entry.reference.locator
            or entry.reference.label
          )
          body_line_numbers = ";".join(
            str(
              occurrence[
                "line_number"
              ]
            )
            for occurrence in occurrences
          )
          body_lines = " || ".join(
            str(
              occurrence[
                "line"
              ]
            )
            for occurrence in occurrences
          )

          duplicate_rows.append(
            {
              "n": n,
              "k": k,
              "group": group,
              "reference_number": entry.number,
              "reference_title": title,
              "statement_index": statement_index,
              "reference_statement_count": (
                reference_statement_count
              ),
              "classification": classification,
              "reason": reason,
              "statement": statement_line,
              "body_occurrence_count": len(
                occurrences
              ),
              "body_line_numbers": body_line_numbers,
              "body_lines": body_lines,
            }
          )

      group_rows.append(
        {
          "n": n,
          "k": k,
          "group": group,
          "reference_entry_count": len(
            entries
          ),
          "selected_statement_count": sum(
            len(
              lines
            )
            for lines in selected_by_number.values()
          ),
          "duplicate_count": duplicates_in_group,
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

  duplicate_count = len(
    duplicate_rows
  )

  if sum(
    classification_counts.values()
  ) != duplicate_count:
    raise AssertionError(
      "classification does not partition duplicates"
    )

  _write_csv(
    output_dir
    / "phase156_r1_duplicate_classification.csv",
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
      "body_occurrence_count",
      "body_line_numbers",
      "body_lines",
    ),
    duplicate_rows,
  )

  _write_csv(
    output_dir
    / "phase156_r1_group_summary.csv",
    (
      "n",
      "k",
      "group",
      "reference_entry_count",
      "selected_statement_count",
      "duplicate_count",
    ),
    group_rows,
  )

  _write_csv(
    output_dir
    / "phase156_r1_exceptions.csv",
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
      "classification": classification,
      "occurrences": classification_counts[
        classification
      ],
      "affected_groups": len(
        classification_groups[
          classification
        ]
      ),
    }
    for classification in (
      CLASS_UNNECESSARY,
      CLASS_BODY_REQUIRED,
      CLASS_REFERENCE_OVERFULL,
    )
  ]

  _write_csv(
    output_dir
    / "phase156_r1_classification_summary.csv",
    (
      "classification",
      "occurrences",
      "affected_groups",
    ),
    summary_rows,
  )

  payload = {
    "phase": "Phase156-R1",
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
    "duplicate_population": duplicate_count,
    "expected_duplicate_population": EXPECTED_DUPLICATES,
    "classification_counts": dict(
      classification_counts
    ),
    "classification_affected_groups": {
      key: len(
        value
      )
      for key, value in classification_groups.items()
    },
    "classification_partition_complete": (
      sum(
        classification_counts.values()
      )
      == duplicate_count
    ),
    "phase156_r2_boundary": (
      "R2 must inspect consumer usage and turn the R1 evidence "
      "classes into a minimal Reference statement selection rule."
    ),
  }

  (
    output_dir
    / "phase156_r1_result.json"
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
    "Phase156-R1 — Reference statement relevance / minimal display audit",
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
    "exact selected-statement/body duplicates: "
    + str(
      duplicate_count
    ),
    "",
    "Classification:",
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
        "  unnecessary_duplicate: Reference attribution is sufficient "
        "under the R1 structural evidence."
      ),
      (
        "  body_restatement_required: the duplicate carries surrounding "
        "calculation/derivation prose, so R1 preserves it."
      ),
      (
        "  reference_side_overfull: the Reference exposes multiple "
        "selected statements; R2 must inspect actual consumer usage."
      ),
      "",
      "R1 boundary:",
      (
        "  This audit classifies all 117 observations but does not change "
        "Reference selection, rendering, suppression, or proof data."
      ),
      (
        "  R2 is responsible for consumer-usage semantics and may refine "
        "the conservative R1 class for a statement."
      ),
      "",
      "Output files:",
      "  phase156_r1_duplicate_classification.csv",
      "  phase156_r1_group_summary.csv",
      "  phase156_r1_classification_summary.csv",
      "  phase156_r1_exceptions.csv",
      "  phase156_r1_result.json",
      "  phase156_r1_summary.txt",
      "=" * 78,
    ]
  )

  summary_text = "\n".join(
    summary
  ) + "\n"
  (
    output_dir
    / "phase156_r1_summary.txt"
  ).write_text(
    summary_text,
    encoding="utf-8",
  )
  print(
    summary_text
  )

  if groups_seen != EXPECTED_GROUPS:
    print(
      "FAIL: 112-group population was not reproduced."
    )
    return payload

  if exceptions:
    print(
      "FAIL: audit exceptions were observed."
    )
    return payload

  if duplicate_count != EXPECTED_DUPLICATES:
    print(
      "FAIL: expected 117 duplicates, observed "
      + str(
        duplicate_count
      )
      + "."
    )
    return payload

  print(
    "PASS: all 117 duplicates were reproduced and classified."
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
      / "phase156_r1_audit_output"
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
