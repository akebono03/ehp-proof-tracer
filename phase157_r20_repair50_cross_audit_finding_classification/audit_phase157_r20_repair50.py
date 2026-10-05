from __future__ import annotations

import csv
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

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
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


REPAIR49_OUTPUT = (
  REPOSITORY_ROOT
  / "phase157_r20_repair49_112_group_post_repair_cross_audit"
  / "audit_output"
)

OUTPUT_DIR = (
  Path(__file__).resolve().parent
  / "audit_output"
)


def render_group(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def first_nonempty_lines(
  text: str,
  limit: int = 12,
) -> tuple[
  str,
  ...,
]:
  lines = tuple(
    line
    for line in text.splitlines()
    if line.strip()
  )

  return lines[
    :limit
  ]


def last_nonempty_lines(
  text: str,
  limit: int = 12,
) -> tuple[
  str,
  ...,
]:
  lines = tuple(
    line
    for line in text.splitlines()
    if line.strip()
  )

  return lines[
    -limit:
  ]


def classify_missing_proof_section(
  rendered: str,
) -> str:
  if "\n## 証明\n" in rendered:
    return "HAS_PROOF_SECTION"

  if "# Group proof narrative" not in rendered:
    return "NOT_GROUP_PROOF_NARRATIVE"

  if "## 使用する結果" not in rendered:
    return "NO_REFERENCE_SECTION_EITHER"

  stripped = rendered.strip()

  if stripped.endswith(
    r"$\square$"
  ):
    return "NO_PROOF_HEADING_BUT_QED_PRESENT"

  return "REFERENCE_ONLY_OR_DIRECT_RESULT"


def main() -> int:
  findings_path = (
    REPAIR49_OUTPUT
    / "findings.csv"
  )

  if not findings_path.is_file():
    raise RuntimeError(
      "repair49 findings.csv was not found. "
      "Run repair49 first."
    )

  with findings_path.open(
    "r",
    encoding="utf-8",
    newline="",
  ) as handle:
    findings = tuple(
      csv.DictReader(
        handle
      )
    )

  relevant = tuple(
    row
    for row in findings
    if row[
      "kind"
    ]
    in (
      "missing_proof_section",
      "exact_duplicate_paragraph",
    )
  )

  group_keys = sorted(
    {
      (
        int(
          row[
            "n"
          ]
        ),
        int(
          row[
            "k"
          ]
        ),
      )
      for row in relevant
    }
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  rows = []
  report_lines = [
    "=" * 96,
    "Phase157-R20 repair50 - cross-audit finding classification",
    "=" * 96,
    "Production code changes: none",
    "pytest: not run",
    "",
  ]

  for n, k in group_keys:
    group_findings = tuple(
      row
      for row in relevant
      if (
        int(
          row[
            "n"
          ]
        )
        == n
        and int(
          row[
            "k"
          ]
        )
        == k
      )
    )
    rendered = render_group(
      n,
      k,
    )
    classification = (
      classify_missing_proof_section(
        rendered
      )
    )
    label = f"pi_{n + k}^{n}"

    report_lines.extend(
      (
        "-" * 96,
        f"{label}  (n={n}, k={k})",
        "findings:",
      )
    )

    for finding in group_findings:
      report_lines.append(
        "  - "
        + finding[
          "kind"
        ]
        + ": "
        + finding[
          "detail"
        ]
      )

    report_lines.extend(
      (
        "classification: "
        + classification,
        "first non-empty lines:",
      )
    )

    for line in first_nonempty_lines(
      rendered
    ):
      report_lines.append(
        "  "
        + line
      )

    report_lines.append(
      "last non-empty lines:"
    )

    for line in last_nonempty_lines(
      rendered
    ):
      report_lines.append(
        "  "
        + line
      )

    report_lines.append(
      ""
    )

    rows.append(
      {
        "n": n,
        "k": k,
        "group": label,
        "finding_kinds": ";".join(
          row[
            "kind"
          ]
          for row in group_findings
        ),
        "classification": classification,
        "has_proof_heading": (
          "\n## 証明\n"
          in rendered
        ),
        "has_reference_heading": (
          "## 使用する結果"
          in rendered
        ),
        "has_qed": rendered.strip().endswith(
          r"$\square$"
        ),
      }
    )

  duplicate_rows = tuple(
    row
    for row in relevant
    if row[
      "kind"
    ]
    == "exact_duplicate_paragraph"
  )

  report_lines.extend(
    (
      "=" * 96,
      "EXACT DUPLICATE SUMMARY",
      "=" * 96,
      f"count: {len(duplicate_rows)}",
    )
  )

  for row in duplicate_rows:
    report_lines.append(
      f"{row['group']}: {row['detail']}"
    )

  with (
    OUTPUT_DIR
    / "classification.csv"
  ).open(
    "w",
    encoding="utf-8",
    newline="",
  ) as handle:
    writer = csv.DictWriter(
      handle,
      fieldnames=(
        "n",
        "k",
        "group",
        "finding_kinds",
        "classification",
        "has_proof_heading",
        "has_reference_heading",
        "has_qed",
      ),
    )
    writer.writeheader()
    writer.writerows(
      rows
    )

  report = "\n".join(
    report_lines
  )

  (
    OUTPUT_DIR
    / "report.txt"
  ).write_text(
    report
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    report
  )
  print("")
  print(
    "Output:"
  )
  print(
    "  audit_output/classification.csv"
  )
  print(
    "  audit_output/report.txt"
  )
  print("")
  print(
    "AUDIT COMPLETE"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
