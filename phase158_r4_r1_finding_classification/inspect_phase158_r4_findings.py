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


def _line_context(
  text: str,
  line_number: int | None,
  radius: int = 2,
) -> str:
  if line_number is None:
    return ""

  lines = text.splitlines()
  start = max(
    0,
    line_number - 1 - radius,
  )
  end = min(
    len(lines),
    line_number + radius,
  )

  result = []

  for index in range(
    start,
    end,
  ):
    marker = (
      ">>"
      if index == line_number - 1
      else "  "
    )
    result.append(
      f"{marker} {index + 1:03d}: {lines[index]}"
    )

  return "\n".join(
    result
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


def _classify_missing_equation_tag(
  row: dict,
  rendered: str,
) -> tuple[str, str]:
  detail = row["detail"]
  match = re.search(
    r"\((\d+)\)",
    detail,
  )

  if match is None:
    return (
      "needs_review",
      "Could not recover the referenced equation number.",
    )

  number = int(
    match.group(1)
  )
  connector_refs = (
    _connector_references(
      rendered
    )
  )
  tags = _tag_numbers(
    rendered
  )

  if connector_refs[number] > 0 and tags[number] == 0:
    return (
      "confirmed_linkage_defect",
      (
        f"({number}) is used by an equation-derivation connector "
        "but no matching tag is visible."
      ),
    )

  return (
    "audit_false_positive",
    (
      f"({number}) is not used by the canonical "
      "'(N) [と (M)] より,' connector pattern."
    ),
  )


def _classify_unreferenced_tag(
  row: dict,
  rendered: str,
) -> tuple[str, str]:
  excerpt = row["excerpt"]
  match = TAG_RE.search(
    excerpt
  )

  if match is None:
    return (
      "needs_review",
      "Could not recover tag number from excerpt.",
    )

  number = int(
    match.group(1)
  )
  connector_refs = (
    _connector_references(
      rendered
    )
  )

  if connector_refs[number] == 0:
    return (
      "confirmed_unused_number_candidate",
      (
        f"\\tag{{{number}}} is visible but is not cited by "
        "any canonical equation-derivation connector."
      ),
    )

  return (
    "audit_false_positive",
    (
      f"\\tag{{{number}}} is cited by a canonical connector."
    ),
  )


def _classify_row(
  row: dict,
  rendered: str,
) -> tuple[str, str]:
  category = row["category"]

  if category == "missing_equation_tag":
    return _classify_missing_equation_tag(
      row,
      rendered,
    )

  if category == "unreferenced_equation_tag":
    return _classify_unreferenced_tag(
      row,
      rendered,
    )

  if category == "ambiguous_anaphora":
    return (
      "confirmed_prose_review",
      (
        "The phrase is generated prose and should be checked "
        "against the immediately preceding mathematical subject."
      ),
    )

  if category == "standalone_period":
    return (
      "confirmed_formatting_defect",
      "Standalone period is always a formatting defect.",
    )

  if category == "split_calculation_sequence":
    return (
      "confirmed_continuity_review",
      "Adjacent calculation paragraphs need semantic review.",
    )

  return (
    "needs_review",
    "Unknown category.",
  )


def main() -> int:
  rows = _read_findings()
  classified = []
  groups = defaultdict(
    list
  )

  for row in rows:
    group = row["group"]
    rendered = _group_output(
      group
    )
    classification, rationale = (
      _classify_row(
        row,
        rendered,
      )
    )

    line_number_text = (
      row.get(
        "line_number",
        "",
      )
      or ""
    )
    line_number = (
      int(
        line_number_text
      )
      if line_number_text.isdigit()
      else None
    )

    item = {
      **row,
      "classification": classification,
      "rationale": rationale,
      "context": _line_context(
        rendered,
        line_number,
      ),
    }
    classified.append(
      item
    )
    groups[
      group
    ].append(
      item
    )

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
    "context",
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

  summary_lines = [
    "=" * 78,
    "Phase 158-R4-R1 - finding classification",
    "=" * 78,
    "Production code changes: none",
    "Existing test changes: none",
    "Full pytest: not run",
    "",
    f"Input findings: {len(classified)}",
    f"Affected groups: {len(groups)}",
    "",
    "Classification counts",
    "-" * 78,
  ]

  for key in sorted(
    counts
  ):
    summary_lines.append(
      f"{key}: {counts[key]}"
    )

  summary_lines.extend(
    [
      "",
      "Per-group findings",
      "=" * 78,
    ]
  )

  for group in sorted(
    groups
  ):
    summary_lines.extend(
      [
        "",
        f"[{group}]",
        "-" * 78,
      ]
    )

    rendered = _group_output(
      group
    )
    connector_refs = _connector_references(
      rendered
    )
    tags = _tag_numbers(
      rendered
    )

    summary_lines.append(
      "visible tags: "
      + repr(
        tuple(
          sorted(
            tags
          )
        )
      )
    )
    summary_lines.append(
      "canonical connector refs: "
      + repr(
        tuple(
          sorted(
            connector_refs.elements()
          )
        )
      )
    )

    for index, item in enumerate(
      groups[group],
      start=1,
    ):
      summary_lines.extend(
        [
          "",
          (
            f"{index}. {item['category']} "
            f"=> {item['classification']}"
          ),
          "detail: " + item["detail"],
          "rationale: " + item["rationale"],
          "excerpt: " + item["excerpt"],
        ]
      )

      if item["context"]:
        summary_lines.extend(
          [
            "context:",
            item["context"],
          ]
        )

  summary_lines.extend(
    [
      "",
      "=" * 78,
      "Next decision boundary",
      "=" * 78,
      (
        "Only confirmed linkage defects, confirmed unused-number "
        "candidates, and confirmed prose reviews should proceed "
        "to an R4 production/test repair."
      ),
      (
        "Audit false positives must be repaired in the audit logic, "
        "not in production code."
      ),
    ]
  )

  summary = "\n".join(
    summary_lines
  ) + "\n"

  (
    output_dir
    / "summary.txt"
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
