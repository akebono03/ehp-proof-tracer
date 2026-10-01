from __future__ import annotations

import csv
import re
from pathlib import Path

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


N_RANGE = range(
  2,
  16,
)
K_RANGE = range(
  0,
  8,
)
MAX_DEPTH = 2
EXPECTED_GROUP_COUNT = 112

OUTPUT_DIR = (
  Path(__file__).resolve().parent
  / "audit_output"
)


def _label(
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


def _render_group(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  if not report.candidates:
    raise AssertionError(
      "no report candidate for "
      + "n="
      + str(
        n
      )
      + ", k="
      + str(
        k
      )
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

  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _strip_inline_math(
  line: str,
) -> str:
  result = []
  inside_math = False
  escaped = False

  for character in line:
    if escaped:
      if not inside_math:
        result.append(
          character
        )
      escaped = False
      continue

    if character == "\\":
      escaped = True
      if not inside_math:
        result.append(
          character
        )
      continue

    if character == "$":
      inside_math = not inside_math
      if not inside_math:
        result.append(
          "MATH"
        )
      continue

    if not inside_math:
      result.append(
        character
      )

  return "".join(
    result
  )


def _prose_lines(
  rendered: str,
):
  in_display_math = False

  for line_number, line in enumerate(
    rendered.splitlines(),
    start=1,
  ):
    stripped = line.strip()

    if stripped in (
      r"\[",
      "$$",
    ):
      in_display_math = True
      continue

    if stripped in (
      r"\]",
      "$$",
    ):
      in_display_math = False
      continue

    if in_display_math:
      continue

    if not stripped:
      continue

    prose = _strip_inline_math(
      stripped
    )

    if not re.search(
      r"[ぁ-んァ-ヶ一-龠々]",
      prose,
    ):
      continue

    yield (
      line_number,
      stripped,
      prose,
    )


def _section_for_line(
  rendered: str,
  target_line_number: int,
) -> str:
  section = "header"

  for line_number, line in enumerate(
    rendered.splitlines(),
    start=1,
  ):
    if line_number > target_line_number:
      break

    if line.strip() == "## 使用する結果":
      section = "references"
      continue

    if line.strip() == "## 証明":
      section = "proof"
      continue

  return section


def _write_csv(
  path: Path,
  rows,
) -> None:
  fieldnames = (
    "n",
    "k",
    "group",
    "section",
    "line_number",
    "kind",
    "line",
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
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  scanned_groups = 0
  rendered_groups = 0
  exceptions = []
  violations = []
  ascii_comma_lines = 0
  ascii_period_endings = 0
  groups_with_ascii_comma = set()
  groups_with_ascii_period = set()

  for n in N_RANGE:
    for k in K_RANGE:
      scanned_groups += 1
      label = _label(
        n,
        k,
      )

      try:
        rendered = _render_group(
          n,
          k,
        )
      except Exception as exc:
        exceptions.append(
          (
            n,
            k,
            label,
            type(
              exc
            ).__name__,
            str(
              exc
            ),
          )
        )
        continue

      rendered_groups += 1

      for line_number, line, prose in _prose_lines(
        rendered
      ):
        section = _section_for_line(
          rendered,
          line_number,
        )

        if "、" in prose:
          violations.append(
            {
              "n": n,
              "k": k,
              "group": label,
              "section": section,
              "line_number": line_number,
              "kind": "japanese_comma",
              "line": line,
            }
          )

        if "。" in prose:
          violations.append(
            {
              "n": n,
              "k": k,
              "group": label,
              "section": section,
              "line_number": line_number,
              "kind": "japanese_period",
              "line": line,
            }
          )

        if re.search(
          r",(?:\s|$)",
          prose,
        ):
          ascii_comma_lines += 1
          groups_with_ascii_comma.add(
            label
          )

        if prose.endswith(
          "."
        ):
          ascii_period_endings += 1
          groups_with_ascii_period.add(
            label
          )

  _write_csv(
    OUTPUT_DIR
    / "violations.csv",
    violations,
  )

  exception_lines = [
    "n,k,group,exception_type,exception_message",
  ]

  for (
    n,
    k,
    label,
    exception_type,
    message,
  ) in exceptions:
    exception_lines.append(
      ",".join(
        (
          str(
            n
          ),
          str(
            k
          ),
          label,
          exception_type,
          message.replace(
            "\n",
            " ",
          ),
        )
      )
    )

  (
    OUTPUT_DIR
    / "exceptions.csv"
  ).write_text(
    "\n".join(
      exception_lines
    )
    + "\n",
    encoding="utf-8-sig",
  )

  japanese_comma_count = sum(
    row["kind"]
    == "japanese_comma"
    for row in violations
  )
  japanese_period_count = sum(
    row["kind"]
    == "japanese_period"
    for row in violations
  )
  affected_groups = sorted(
    {
      row["group"]
      for row in violations
    }
  )

  summary_lines = [
    "=" * 78,
    "Phase 154 — Punctuation Closure Audit",
    "=" * 78,
    "Production changes: none",
    "Existing test changes: none",
    (
      "Range: n=2..15, k=0..7 "
      + "("
      + str(
        EXPECTED_GROUP_COUNT
      )
      + " groups)"
    ),
    "Replay depth: 2",
    "Route: public Narrative renderer",
    "Policy: prose comma=', ' / prose period='.'",
    "TeX display and inline math: excluded from punctuation violations",
    "",
    "Summary",
    "-" * 78,
    "scanned groups: "
    + str(
      scanned_groups
    ),
    "rendered groups: "
    + str(
      rendered_groups
    ),
    "exceptions: "
    + str(
      len(
        exceptions
      )
    ),
    "japanese comma violations: "
    + str(
      japanese_comma_count
    ),
    "japanese period violations: "
    + str(
      japanese_period_count
    ),
    "affected groups: "
    + str(
      len(
        affected_groups
      )
    ),
    "ascii comma prose lines: "
    + str(
      ascii_comma_lines
    ),
    "groups with ascii comma prose: "
    + str(
      len(
        groups_with_ascii_comma
      )
    ),
    "ascii period prose endings: "
    + str(
      ascii_period_endings
    ),
    "groups with ascii period prose: "
    + str(
      len(
        groups_with_ascii_period
      )
    ),
  ]

  if affected_groups:
    summary_lines.extend(
      (
        "",
        "Affected groups",
        "-" * 78,
      )
    )
    summary_lines.extend(
      affected_groups
    )

  if violations:
    summary_lines.extend(
      (
        "",
        "Violation preview",
        "-" * 78,
      )
    )

    for row in violations[
      :40
    ]:
      summary_lines.append(
        (
          row["group"]
          + " "
          + row["section"]
          + " L"
          + str(
            row["line_number"]
          )
          + " "
          + row["kind"]
          + ": "
          + row["line"]
        )
      )

  if exceptions:
    summary_lines.extend(
      (
        "",
        "Exceptions",
        "-" * 78,
      )
    )

    for (
      _n,
      _k,
      label,
      exception_type,
      message,
    ) in exceptions:
      summary_lines.append(
        label
        + ": "
        + exception_type
        + ": "
        + message
      )

  summary_lines.extend(
    (
      "",
      "Output files",
      "-" * 78,
      "audit_output/summary.txt",
      "audit_output/violations.csv",
      "audit_output/exceptions.csv",
      "=" * 78,
    )
  )

  summary = (
    "\n".join(
      summary_lines
    )
    + "\n"
  )

  (
    OUTPUT_DIR
    / "summary.txt"
  ).write_text(
    summary,
    encoding="utf-8",
  )

  print(
    summary
  )

  passed = (
    scanned_groups
    == EXPECTED_GROUP_COUNT
    and rendered_groups
    == EXPECTED_GROUP_COUNT
    and not exceptions
    and japanese_comma_count
    == 0
    and japanese_period_count
    == 0
    and ascii_comma_lines
    > 0
    and ascii_period_endings
    > 0
  )

  if passed:
    print(
      "PASS: all 112 public Narrative outputs satisfy "
      "the ASCII punctuation policy outside TeX."
    )
    return 0

  print(
    "FAIL: punctuation closure is not complete. "
    "Inspect violations.csv and exceptions.csv before "
    "changing production code."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
