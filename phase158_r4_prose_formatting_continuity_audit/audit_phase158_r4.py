from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
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


N_RANGE = range(2, 16)
K_RANGE = range(0, 8)
MAX_DEPTH = 2
EXPECTED_GROUP_COUNT = 112

TAG_RE = re.compile(r"\\tag\{([0-9]+)\}")
PAREN_NUMBER_RE = re.compile(r"\(([0-9]+)\)")
AMBIGUOUS_PHRASES = (
  "この群構造と",
  "この群構造、",
  "この結果と",
  "これらの結果と",
)


def _group_label(
  n: int,
  k: int,
) -> str:
  return (
    "pi_"
    + str(n + k)
    + "^"
    + str(n)
  )


def _build_raw_presentation(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  if not report.candidates:
    raise AssertionError(
      "no report candidate for "
      + f"n={n}, k={k}"
    )

  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )

  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=MAX_DEPTH,
  )

  return build_toda_group_proof_presentation(
    replay
  )


def _add_finding(
  findings: list[dict],
  *,
  n: int,
  k: int,
  group: str,
  category: str,
  severity: str,
  line_number: int | None,
  detail: str,
  excerpt: str,
) -> None:
  findings.append(
    {
      "n": n,
      "k": k,
      "group": group,
      "category": category,
      "severity": severity,
      "line_number": (
        ""
        if line_number is None
        else line_number
      ),
      "detail": detail,
      "excerpt": excerpt,
    }
  )


def _strip_tags(
  text: str,
) -> str:
  return TAG_RE.sub(
    "",
    text,
  )


def _number_references(
  rendered: str,
) -> Counter[int]:
  without_tags = _strip_tags(
    rendered
  )
  return Counter(
    int(match.group(1))
    for match in PAREN_NUMBER_RE.finditer(
      without_tags
    )
  )


def _paragraphs_with_lines(
  rendered: str,
) -> list[tuple[int, str]]:
  lines = rendered.splitlines()
  paragraphs: list[tuple[int, str]] = []
  current: list[str] = []
  start_line: int | None = None

  for index, line in enumerate(
    lines,
    start=1,
  ):
    if line.strip():
      if start_line is None:
        start_line = index
      current.append(line)
      continue

    if current:
      paragraphs.append(
        (
          start_line if start_line is not None else index,
          "\n".join(current),
        )
      )
      current = []
      start_line = None

  if current:
    paragraphs.append(
      (
        start_line if start_line is not None else len(lines),
        "\n".join(current),
      )
    )

  return paragraphs


def _is_math_only_paragraph(
  paragraph: str,
) -> bool:
  stripped = paragraph.strip()

  if (
    stripped.startswith("$")
    and stripped.endswith("$")
    and stripped.count("$") >= 2
  ):
    outside = re.sub(
      r"\$[^$]*\$",
      "",
      stripped,
    ).strip()
    return outside == ""

  if (
    stripped.startswith(r"\[")
    and stripped.endswith(r"\]")
  ):
    return True

  return False


def _looks_like_calculation(
  paragraph: str,
) -> bool:
  if not _is_math_only_paragraph(
    paragraph
  ):
    return False

  return (
    "=" in paragraph
    or r"\neq" in paragraph
    or r"\cong" in paragraph
    or r"\simeq" in paragraph
  )


def _scan_group(
  *,
  n: int,
  k: int,
  group: str,
  rendered: str,
  findings: list[dict],
) -> None:
  lines = rendered.splitlines()

  for line_number, line in enumerate(
    lines,
    start=1,
  ):
    stripped = line.strip()

    if stripped == ".":
      _add_finding(
        findings,
        n=n,
        k=k,
        group=group,
        category="standalone_period",
        severity="defect",
        line_number=line_number,
        detail="ASCII period is emitted as a standalone line.",
        excerpt=line,
      )

    for phrase in AMBIGUOUS_PHRASES:
      if phrase in stripped:
        _add_finding(
          findings,
          n=n,
          k=k,
          group=group,
          category="ambiguous_anaphora",
          severity="review",
          line_number=line_number,
          detail=(
            "Potentially ambiguous anaphoric prose: "
            + phrase
          ),
          excerpt=line,
        )

  tag_occurrences: dict[int, list[tuple[int, str]]] = defaultdict(list)

  for line_number, line in enumerate(
    lines,
    start=1,
  ):
    for match in TAG_RE.finditer(
      line
    ):
      tag_occurrences[
        int(match.group(1))
      ].append(
        (
          line_number,
          line,
        )
      )

  references = _number_references(
    rendered
  )

  for number, occurrences in sorted(
    tag_occurrences.items()
  ):
    if references[number] != 0:
      continue

    for line_number, line in occurrences:
      _add_finding(
        findings,
        n=n,
        k=k,
        group=group,
        category="unreferenced_equation_tag",
        severity="candidate",
        line_number=line_number,
        detail=(
          f"Equation tag ({number}) is emitted "
          "but is never cited elsewhere in the public Narrative."
        ),
        excerpt=line,
      )

  for number, count in sorted(
    references.items()
  ):
    if number in tag_occurrences:
      continue

    _add_finding(
      findings,
      n=n,
      k=k,
      group=group,
      category="missing_equation_tag",
      severity="defect",
      line_number=None,
      detail=(
        f"Equation reference ({number}) appears {count} time(s), "
        "but no matching \\tag is present."
      ),
      excerpt=f"({number})",
    )

  paragraphs = _paragraphs_with_lines(
    rendered
  )

  index = 0
  while index < len(paragraphs):
    if not _looks_like_calculation(
      paragraphs[index][1]
    ):
      index += 1
      continue

    start = index
    end = index

    while (
      end + 1 < len(paragraphs)
      and _looks_like_calculation(
        paragraphs[end + 1][1]
      )
    ):
      end += 1

    if end > start:
      start_line = paragraphs[start][0]
      excerpts = [
        paragraphs[position][1]
        for position in range(
          start,
          end + 1,
        )
      ]
      _add_finding(
        findings,
        n=n,
        k=k,
        group=group,
        category="split_calculation_sequence",
        severity="candidate",
        line_number=start_line,
        detail=(
          "Two or more adjacent math-only calculation paragraphs "
          "may belong to one continuous derivation."
        ),
        excerpt="\n\n".join(excerpts),
      )

    index = end + 1


def _write_csv(
  path: Path,
  rows: list[dict],
) -> None:
  fieldnames = (
    "n",
    "k",
    "group",
    "category",
    "severity",
    "line_number",
    "detail",
    "excerpt",
  )

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
  output_dir = (
    PACKAGE_DIR
    / "audit_output"
  )
  group_output_dir = (
    output_dir
    / "group_outputs"
  )

  group_output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  findings: list[dict] = []
  exceptions: list[dict] = []
  rendered_count = 0

  for n in N_RANGE:
    for k in K_RANGE:
      group = _group_label(
        n,
        k,
      )

      try:
        presentation = (
          _build_raw_presentation(
            n,
            k,
          )
        )
        rendered = (
          render_toda_group_proof_narrative_markdown(
            presentation
          )
        )
      except Exception as exc:
        exceptions.append(
          {
            "n": n,
            "k": k,
            "group": group,
            "exception": (
              type(exc).__name__
              + ": "
              + str(exc)
            ),
          }
        )
        continue

      rendered_count += 1

      (
        group_output_dir
        / f"{group}.md"
      ).write_text(
        rendered,
        encoding="utf-8",
      )

      _scan_group(
        n=n,
        k=k,
        group=group,
        rendered=rendered,
        findings=findings,
      )

  _write_csv(
    output_dir
    / "findings.csv",
    findings,
  )

  with (
    output_dir
    / "exceptions.json"
  ).open(
    "w",
    encoding="utf-8",
  ) as handle:
    json.dump(
      exceptions,
      handle,
      ensure_ascii=False,
      indent=2,
    )

  category_counts = Counter(
    row["category"]
    for row in findings
  )
  affected_groups = {
    row["group"]
    for row in findings
  }

  summary = {
    "phase": "158-R4",
    "production_changes": False,
    "existing_test_changes": False,
    "population": "n=2..15, k=0..7",
    "expected_groups": EXPECTED_GROUP_COUNT,
    "replay_depth": MAX_DEPTH,
    "rendered_groups": rendered_count,
    "exceptions": len(
      exceptions
    ),
    "findings": len(
      findings
    ),
    "affected_groups": len(
      affected_groups
    ),
    "category_counts": dict(
      sorted(
        category_counts.items()
      )
    ),
  }

  with (
    output_dir
    / "summary.json"
  ).open(
    "w",
    encoding="utf-8",
  ) as handle:
    json.dump(
      summary,
      handle,
      ensure_ascii=False,
      indent=2,
    )

  summary_lines = [
    "=" * 78,
    "Phase 158-R4 - 112-group prose formatting / continuity audit",
    "=" * 78,
    "Production code changes: none",
    "Existing test changes: none",
    "Full pytest: not run",
    "",
    f"Expected groups: {EXPECTED_GROUP_COUNT}",
    f"Rendered groups: {rendered_count}",
    f"Exceptions: {len(exceptions)}",
    f"Findings: {len(findings)}",
    f"Affected groups: {len(affected_groups)}",
    "",
    "Category counts",
    "-" * 78,
  ]

  for category in (
    "standalone_period",
    "unreferenced_equation_tag",
    "missing_equation_tag",
    "ambiguous_anaphora",
    "split_calculation_sequence",
  ):
    summary_lines.append(
      f"{category}: {category_counts.get(category, 0)}"
    )

  summary_lines.extend(
    [
      "",
      "Interpretation",
      "-" * 78,
      "standalone_period: definite formatting defect",
      "missing_equation_tag: definite numbering/linkage defect",
      "unreferenced_equation_tag: candidate for unnecessary equation numbering",
      "ambiguous_anaphora: prose review candidate",
      "split_calculation_sequence: continuity review candidate",
      "",
      "R4 audit only. Do not modify production code from this package.",
    ]
  )

  summary_text = "\n".join(
    summary_lines
  ) + "\n"

  (
    output_dir
    / "summary.txt"
  ).write_text(
    summary_text,
    encoding="utf-8",
  )

  print(
    summary_text,
    end="",
  )

  if (
    rendered_count
    != EXPECTED_GROUP_COUNT
  ):
    return 2

  if exceptions:
    return 3

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
