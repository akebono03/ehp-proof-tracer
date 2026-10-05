from pathlib import Path
import csv
import re

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
  build_complete_toda_group_result_proof_replay,
)


AUDIT_TARGETS = (
  ("pi6_3_reference", 3, 3),
  ("pi8_5_former_dedicated", 5, 3),
  ("pi15_8_former_dedicated", 8, 7),
  ("pi7_4_former_legacy", 4, 3),
  ("pi10_4_existing_generic", 4, 6),
  ("pi12_5_existing_generic", 5, 7),
  ("pi16_9_existing_generic", 9, 7),
)

LEFT_PROOF_ITEM_RE = re.compile(
  r"^\s*(?:\*\*)?\((\d+)\)(?:\*\*)?\s+"
)
TAG_RE = re.compile(
  r"\\tag\{(\d+)\}"
)
PAREN_NUMBER_RE = re.compile(
  r"\((\d+)\)"
)

OLD_ROUTE_MARKERS = (
  "Toda Proposition 5.6 のうち,",
  "直和因子の順序を入れ替えると,",
)


def _presentation(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )
  return build_toda_group_proof_presentation(
    replay
  )


def _line_numbered_findings(
  markdown: str,
):
  lines = markdown.splitlines()
  left_items = []
  tagged_equations = []
  parenthesized_uses = []

  for line_number, line in enumerate(
    lines,
    start=1,
  ):
    left_match = LEFT_PROOF_ITEM_RE.match(
      line
    )
    if left_match is not None:
      left_items.append(
        (
          line_number,
          int(
            left_match.group(
              1
            )
          ),
          line,
        )
      )

    for tag_match in TAG_RE.finditer(
      line
    ):
      tagged_equations.append(
        (
          line_number,
          int(
            tag_match.group(
              1
            )
          ),
          line,
        )
      )

    line_without_tags = TAG_RE.sub(
      "",
      line,
    )
    for paren_match in PAREN_NUMBER_RE.finditer(
      line_without_tags
    ):
      parenthesized_uses.append(
        (
          line_number,
          int(
            paren_match.group(
              1
            )
          ),
          line,
        )
      )

  return (
    tuple(
      left_items
    ),
    tuple(
      tagged_equations
    ),
    tuple(
      parenthesized_uses
    ),
  )


def _equation_reference_findings(
  tagged_equations,
  parenthesized_uses,
):
  tag_lines_by_number = {}

  for line_number, number, line in tagged_equations:
    tag_lines_by_number.setdefault(
      number,
      [],
    ).append(
      (
        line_number,
        line,
      )
    )

  uses_by_number = {}

  for line_number, number, line in parenthesized_uses:
    uses_by_number.setdefault(
      number,
      [],
    ).append(
      (
        line_number,
        line,
      )
    )

  tag_without_later_use = []
  duplicate_tags = []
  use_without_tag = []

  for number, tag_lines in tag_lines_by_number.items():
    if len(
      tag_lines
    ) > 1:
      duplicate_tags.append(
        (
          number,
          tuple(
            tag_lines
          ),
        )
      )

    first_tag_line = min(
      line_number
      for line_number, _line in tag_lines
    )
    later_uses = tuple(
      (
        line_number,
        line,
      )
      for line_number, line in uses_by_number.get(
        number,
        (),
      )
      if line_number > first_tag_line
    )

    if not later_uses:
      tag_without_later_use.append(
        (
          number,
          tuple(
            tag_lines
          ),
        )
      )

  for number, uses in uses_by_number.items():
    if number not in tag_lines_by_number:
      use_without_tag.append(
        (
          number,
          tuple(
            uses
          ),
        )
      )

  return (
    tuple(
      tag_without_later_use
    ),
    tuple(
      duplicate_tags
    ),
    tuple(
      use_without_tag
    ),
  )


def _shell_findings(
  markdown: str,
):
  return {
    "has_title": (
      "# Group proof narrative"
      in markdown
    ),
    "has_target_section": (
      "## 証明対象"
      in markdown
    ),
    "has_reference_section": (
      "## 使用する結果"
      in markdown
    ),
    "has_proof_section": (
      "## 証明"
      in markdown
    ),
    "has_separator": (
      "\n---\n"
      in markdown
    ),
    "has_qed": (
      markdown.rstrip().endswith(
        (
          "□",
          r"\square",
          r"$\square$",
        )
      )
    ),
  }


def main() -> int:
  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  rendered_dir = (
    output_dir
    / "rendered"
  )
  rendered_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  rows = []
  detail_lines = [
    "=" * 88,
    "Phase 158-R5-4 — post-unification public Narrative numbering audit",
    "=" * 88,
    "",
    "Production code changes: none",
    "Test code changes: none",
    "pytest: not run",
    "",
  ]

  total_left_items = 0
  total_tags = 0
  total_tag_without_later_use = 0
  total_duplicate_tags = 0
  total_use_without_tag = 0
  total_old_route_markers = 0
  exceptions = []

  for label, n, k in AUDIT_TARGETS:
    try:
      presentation = _presentation(
        n,
        k,
      )
      markdown = (
        render_toda_group_proof_narrative_markdown(
          presentation
        )
      )
    except Exception as exc:
      exceptions.append(
        (
          label,
          n,
          k,
          type(exc).__name__,
          str(exc),
        )
      )
      continue

    (
      left_items,
      tagged_equations,
      parenthesized_uses,
    ) = _line_numbered_findings(
      markdown
    )
    (
      tag_without_later_use,
      duplicate_tags,
      use_without_tag,
    ) = _equation_reference_findings(
      tagged_equations,
      parenthesized_uses,
    )
    shell = _shell_findings(
      markdown
    )

    old_route_markers = tuple(
      marker
      for marker in OLD_ROUTE_MARKERS
      if marker in markdown
    )

    total_left_items += len(
      left_items
    )
    total_tags += len(
      tagged_equations
    )
    total_tag_without_later_use += len(
      tag_without_later_use
    )
    total_duplicate_tags += len(
      duplicate_tags
    )
    total_use_without_tag += len(
      use_without_tag
    )
    total_old_route_markers += len(
      old_route_markers
    )

    rendered_path = (
      rendered_dir
      / f"{label}.md"
    )
    rendered_path.write_text(
      markdown,
      encoding="utf-8",
    )

    rows.append(
      {
        "label": label,
        "n": n,
        "k": k,
        "group": (
          f"pi_{n + k}^{n}"
        ),
        "left_proof_items": len(
          left_items
        ),
        "equation_tags": len(
          tagged_equations
        ),
        "tags_without_later_use": len(
          tag_without_later_use
        ),
        "duplicate_tags": len(
          duplicate_tags
        ),
        "paren_uses_without_tag": len(
          use_without_tag
        ),
        "old_route_markers": len(
          old_route_markers
        ),
        **shell,
      }
    )

    detail_lines.extend(
      (
        "-" * 88,
        (
          f"{label}: "
          f"pi_{n + k}^{n}"
        ),
        "-" * 88,
        (
          "left proof-item numbering: "
          f"{len(left_items)}"
        ),
        (
          "equation tags: "
          f"{len(tagged_equations)}"
        ),
        (
          "tags without later reference: "
          f"{len(tag_without_later_use)}"
        ),
        (
          "duplicate tags: "
          f"{len(duplicate_tags)}"
        ),
        (
          "parenthesized number uses without tag: "
          f"{len(use_without_tag)}"
        ),
        (
          "old dedicated-route markers: "
          + (
            ", ".join(
              old_route_markers
            )
            if old_route_markers
            else "none"
          )
        ),
        (
          "shell: "
          + ", ".join(
            f"{key}={value}"
            for key, value in shell.items()
          )
        ),
      )
    )

    if left_items:
      detail_lines.append(
        "left proof-item lines:"
      )
      detail_lines.extend(
        (
          f"  L{line_number}: {line}"
        )
        for line_number, _number, line in left_items
      )

    if tagged_equations:
      detail_lines.append(
        "tagged equation lines:"
      )
      detail_lines.extend(
        (
          f"  L{line_number}: tag({number}) {line}"
        )
        for line_number, number, line in tagged_equations
      )

    if tag_without_later_use:
      detail_lines.append(
        "tags without later reference:"
      )
      for number, tag_lines in tag_without_later_use:
        detail_lines.append(
          f"  tag({number})"
        )
        detail_lines.extend(
          f"    L{line_number}: {line}"
          for line_number, line in tag_lines
        )

    if duplicate_tags:
      detail_lines.append(
        "duplicate tags:"
      )
      for number, tag_lines in duplicate_tags:
        detail_lines.append(
          f"  tag({number})"
        )
        detail_lines.extend(
          f"    L{line_number}: {line}"
          for line_number, line in tag_lines
        )

    if use_without_tag:
      detail_lines.append(
        "parenthesized number uses without matching tag:"
      )
      for number, uses in use_without_tag:
        detail_lines.append(
          f"  ({number})"
        )
        detail_lines.extend(
          f"    L{line_number}: {line}"
          for line_number, line in uses
        )

    detail_lines.append(
      ""
    )

  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  csv_path = (
    output_dir
    / "summary.csv"
  )
  fieldnames = (
    list(
      rows[
        0
      ].keys()
    )
    if rows
    else [
      "label",
      "n",
      "k",
      "group",
    ]
  )

  with csv_path.open(
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

  exceptions_path = (
    output_dir
    / "exceptions.csv"
  )

  with exceptions_path.open(
    "w",
    encoding="utf-8-sig",
    newline="",
  ) as handle:
    writer = csv.writer(
      handle
    )
    writer.writerow(
      (
        "label",
        "n",
        "k",
        "exception_type",
        "message",
      )
    )
    writer.writerows(
      exceptions
    )

  summary_lines = [
    "=" * 88,
    "Phase 158-R5-4 — post-unification public Narrative numbering audit",
    "=" * 88,
    f"targets: {len(AUDIT_TARGETS)}",
    f"rendered: {len(rows)}",
    f"exceptions: {len(exceptions)}",
    f"left proof-item numbering findings: {total_left_items}",
    f"equation tags: {total_tags}",
    (
      "equation tags without later reference: "
      f"{total_tag_without_later_use}"
    ),
    f"duplicate equation tags: {total_duplicate_tags}",
    (
      "parenthesized number uses without matching tag: "
      f"{total_use_without_tag}"
    ),
    (
      "old dedicated-route marker findings: "
      f"{total_old_route_markers}"
    ),
    "",
    "Interpretation boundary:",
    (
      "  This audit records post-unification display facts only."
    ),
    (
      "  It does not modify numbering, prose, proof data, "
      "semantic structure, or route selection."
    ),
    "",
    "Output:",
    "  audit_output/summary.txt",
    "  audit_output/details.txt",
    "  audit_output/summary.csv",
    "  audit_output/exceptions.csv",
    "  audit_output/rendered/*.md",
    "=" * 88,
  ]

  (
    output_dir
    / "summary.txt"
  ).write_text(
    "\n".join(
      summary_lines
    )
    + "\n",
    encoding="utf-8",
  )

  (
    output_dir
    / "details.txt"
  ).write_text(
    "\n".join(
      detail_lines
    )
    + "\n",
    encoding="utf-8",
  )

  print(
    "\n".join(
      summary_lines
    )
  )

  if exceptions:
    return 1

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
