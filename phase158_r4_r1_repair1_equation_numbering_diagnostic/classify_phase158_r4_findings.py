from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
SOURCE_AUDIT_DIR = (
  REPO_ROOT
  / "phase158_r4_prose_formatting_continuity_audit"
  / "audit_output"
)

FINDINGS_CSV = SOURCE_AUDIT_DIR / "findings.csv"
GROUP_OUTPUT_DIR = SOURCE_AUDIT_DIR / "group_outputs"

CONNECTOR_REFERENCE_RE = re.compile(
  r"^\((\d+)\)"
  r"(?: と \((\d+)\))?"
  r" より,"
)
TAG_RE = re.compile(
  r"\\tag\{(\d+)\}"
)


def _read_findings() -> list[dict]:
  if not FINDINGS_CSV.exists():
    raise FileNotFoundError(
      "Phase 158-R4 findings.csv was not found: "
      + str(FINDINGS_CSV)
    )

  with FINDINGS_CSV.open(
    "r",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    return list(
      csv.DictReader(
        handle
      )
    )


def _group_output(
  group: str,
) -> str:
  path = (
    GROUP_OUTPUT_DIR
    / f"{group}.md"
  )

  if not path.exists():
    raise FileNotFoundError(
      "Rendered group output was not found: "
      + str(path)
    )

  return path.read_text(
    encoding="utf-8"
  )


def _connector_references(
  text: str,
) -> Counter[int]:
  result: Counter[int] = Counter()

  for line in text.splitlines():
    match = CONNECTOR_REFERENCE_RE.match(
      line.strip()
    )

    if match is None:
      continue

    result[
      int(
        match.group(1)
      )
    ] += 1

    second = match.group(2)

    if second is not None:
      result[
        int(
          second
        )
      ] += 1

  return result


def _tag_numbers(
  text: str,
) -> Counter[int]:
  return Counter(
    int(
      match.group(1)
    )
    for match in TAG_RE.finditer(
      text
    )
  )


def _classify(
  row: dict,
  rendered: str,
) -> tuple[
  str,
  str,
]:
  category = row[
    "category"
  ]

  if (
    category
    == "ambiguous_anaphora"
  ):
    return (
      "confirmed_prose_review",
      (
        "Generated prose contains an ambiguous "
        "anaphoric phrase."
      ),
    )

  if (
    category
    == "standalone_period"
  ):
    return (
      "confirmed_formatting_defect",
      "Standalone period is a formatting defect.",
    )

  if (
    category
    == "split_calculation_sequence"
  ):
    return (
      "confirmed_continuity_review",
      (
        "Adjacent calculation paragraphs require "
        "semantic review."
      ),
    )

  number_match = re.search(
    r"\((\d+)\)",
    row[
      "detail"
    ],
  )

  if (
    number_match is None
    and category
    == "unreferenced_equation_tag"
  ):
    number_match = re.search(
      r"\\tag\{(\d+)\}",
      row[
        "excerpt"
      ],
    )

  if number_match is None:
    return (
      "needs_review",
      "Could not recover equation number.",
    )

  number = int(
    number_match.group(1)
  )
  tags = _tag_numbers(
    rendered
  )
  connector_refs = (
    _connector_references(
      rendered
    )
  )

  if (
    category
    == "missing_equation_tag"
  ):
    if (
      connector_refs[number] > 0
      and tags[number] == 0
    ):
      return (
        "confirmed_linkage_defect",
        (
          f"({number}) is used by a canonical "
          "equation connector but has no matching tag."
        ),
      )

    return (
      "audit_false_positive",
      (
        f"({number}) is not an equation reference in "
        "the canonical connector form."
      ),
    )

  if (
    category
    == "unreferenced_equation_tag"
  ):
    if (
      tags[number] > 0
      and connector_refs[number] == 0
    ):
      return (
        "confirmed_unused_number_candidate",
        (
          f"\\tag{{{number}}} is visible but unused "
          "by canonical equation connectors."
        ),
      )

    return (
      "audit_false_positive",
      (
        f"\\tag{{{number}}} is consumed by an "
        "equation connector."
      ),
    )

  return (
    "needs_review",
    "Unknown category.",
  )


def main() -> int:
  rows = _read_findings()
  classified = []
  group_counts = defaultdict(
    Counter
  )

  for row in rows:
    rendered = _group_output(
      row[
        "group"
      ]
    )
    classification, rationale = (
      _classify(
        row,
        rendered,
      )
    )
    item = {
      **row,
      "classification": classification,
      "rationale": rationale,
    }
    classified.append(
      item
    )
    group_counts[
      row["group"]
    ][
      classification
    ] += 1

  counts = Counter(
    item[
      "classification"
    ]
    for item in classified
  )

  output_dir = (
    PACKAGE_DIR
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  fieldnames = (
    "n",
    "k",
    "group",
    "category",
    "severity",
    "line_number",
    "detail",
    "excerpt",
    "classification",
    "rationale",
  )

  with (
    output_dir
    / "classified_findings.csv"
  ).open(
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
      classified
    )

  lines = [
    "=" * 78,
    "Phase 158-R4-R1 - 11 finding classification",
    "=" * 78,
    "Production code changes: none",
    "Existing test changes: none",
    "",
    f"Input findings: {len(classified)}",
    "",
    "Classification counts",
    "-" * 78,
  ]

  for classification in sorted(
    counts
  ):
    lines.append(
      f"{classification}: {counts[classification]}"
    )

  lines.extend(
    [
      "",
      "Per group",
      "-" * 78,
    ]
  )

  for group in sorted(
    group_counts
  ):
    lines.append(
      group
      + ": "
      + repr(
        dict(
          group_counts[
            group
          ]
        )
      )
    )

  lines.extend(
    [
      "",
      "Detailed findings",
      "-" * 78,
    ]
  )

  for index, item in enumerate(
    classified,
    start=1,
  ):
    lines.extend(
      [
        "",
        (
          f"{index}. {item['group']} / "
          f"{item['category']} => "
          f"{item['classification']}"
        ),
        "detail: "
        + item["detail"],
        "rationale: "
        + item["rationale"],
        "excerpt: "
        + item["excerpt"],
      ]
    )

  summary = "\n".join(
    lines
  ) + "\n"

  (
    output_dir
    / "classification_summary.txt"
  ).write_text(
    summary,
    encoding="utf-8",
  )

  print(
    summary,
    end="",
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
