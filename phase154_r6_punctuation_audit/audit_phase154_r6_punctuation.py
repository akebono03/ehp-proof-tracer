from __future__ import annotations

from pathlib import Path
import re
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
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


REPRESENTATIVES = (
  ("pi6_3", 3, 3),
  ("pi10_4", 4, 6),
  ("pi11_4", 4, 7),
  ("pi12_5", 5, 7),
  ("pi16_9", 9, 7),
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


def _strip_inline_math(
  line: str,
) -> str:
  result = []
  in_math = False
  escaped = False

  for character in line:
    if escaped:
      if not in_math:
        result.append(
          character
        )
      escaped = False
      continue

    if character == "\\":
      escaped = True

      if not in_math:
        result.append(
          character
        )
      continue

    if character == "$":
      in_math = not in_math

      if not in_math:
        result.append(
          "MATH"
        )
      continue

    if not in_math:
      result.append(
        character
      )

  return "".join(
    result
  )


def _is_reference_title_line(
  line: str,
) -> bool:
  return bool(
    re.fullmatch(
      r"\*\*\[R[0-9]+\] .+\.\*\*",
      line.strip(),
    )
  )


def _is_markdown_or_math_only_line(
  line: str,
) -> bool:
  stripped = line.strip()

  if not stripped:
    return True

  if stripped.startswith(
    "#"
  ):
    return True

  if _is_reference_title_line(
    stripped
  ):
    return True

  if stripped in {
    r"\[",
    r"\]",
    r"\qquad",
  }:
    return True

  prose = _strip_inline_math(
    stripped
  ).strip()

  return prose in {
    "",
    "MATH",
  }


def _contains_japanese(
  text: str,
) -> bool:
  return bool(
    re.search(
      r"[ぁ-んァ-ヶ一-龠々]",
      text,
    )
  )


def classify_line(
  line: str,
) -> dict:
  if _is_markdown_or_math_only_line(
    line
  ):
    return {
      "ascii_period_end": False,
      "japanese_period_end": False,
      "ascii_comma": False,
      "japanese_comma": False,
      "normalized_prose": "",
    }

  prose = _strip_inline_math(
    line
  ).strip()

  if not _contains_japanese(
    prose
  ):
    return {
      "ascii_period_end": False,
      "japanese_period_end": False,
      "ascii_comma": False,
      "japanese_comma": False,
      "normalized_prose": prose,
    }

  return {
    "ascii_period_end": prose.endswith(
      "."
    ),
    "japanese_period_end": prose.endswith(
      "。"
    ),
    "ascii_comma": bool(
      re.search(
        r",(?:\s|$)",
        prose,
      )
    ),
    "japanese_comma": "、" in prose,
    "normalized_prose": prose,
  }


def audit_group(
  name: str,
  n: int,
  k: int,
):
  rendered = render_group(
    n,
    k,
  )
  ascii_period_lines = []
  japanese_period_lines = []
  ascii_comma_lines = []
  japanese_comma_lines = []

  for line_number, line in enumerate(
    rendered.splitlines(),
    start=1,
  ):
    classification = classify_line(
      line
    )

    if classification[
      "ascii_period_end"
    ]:
      ascii_period_lines.append(
        (
          line_number,
          line,
        )
      )

    if classification[
      "japanese_period_end"
    ]:
      japanese_period_lines.append(
        (
          line_number,
          line,
        )
      )

    if classification[
      "ascii_comma"
    ]:
      ascii_comma_lines.append(
        (
          line_number,
          line,
        )
      )

    if classification[
      "japanese_comma"
    ]:
      japanese_comma_lines.append(
        (
          line_number,
          line,
        )
      )

  return {
    "name": name,
    "rendered": rendered,
    "ascii_period_lines": tuple(
      ascii_period_lines
    ),
    "japanese_period_lines": tuple(
      japanese_period_lines
    ),
    "ascii_comma_lines": tuple(
      ascii_comma_lines
    ),
    "japanese_comma_lines": tuple(
      japanese_comma_lines
    ),
  }


def main() -> int:
  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  results = tuple(
    audit_group(
      name,
      n,
      k,
    )
    for name, n, k in REPRESENTATIVES
  )

  total_ascii_period = sum(
    len(
      result[
        "ascii_period_lines"
      ]
    )
    for result in results
  )
  total_japanese_period = sum(
    len(
      result[
        "japanese_period_lines"
      ]
    )
    for result in results
  )
  total_ascii_comma = sum(
    len(
      result[
        "ascii_comma_lines"
      ]
    )
    for result in results
  )
  total_japanese_comma = sum(
    len(
      result[
        "japanese_comma_lines"
      ]
    )
    for result in results
  )

  lines = [
    "# Phase 154-R6 Punctuation Audit",
    "",
    "Production changes: none.",
    "",
    "Scope:",
    "- Narrative",
    "- depth 2",
    "- pi6_3, pi10_4, pi11_4, pi12_5, pi16_9",
    "- Japanese prose only",
    "- inline/display mathematics excluded from punctuation classification",
    "- Reference title punctuation excluded",
    "",
    "## Summary",
    "",
    f"ascii_period_sentence_endings: {total_ascii_period}",
    f"japanese_period_sentence_endings: {total_japanese_period}",
    f"ascii_comma_prose_lines: {total_ascii_comma}",
    f"japanese_comma_prose_lines: {total_japanese_comma}",
    "",
  ]

  for result in results:
    lines.extend(
      (
        "## "
        + result[
          "name"
        ],
        "",
        (
          "ascii_period_sentence_endings: "
          + str(
            len(
              result[
                "ascii_period_lines"
              ]
            )
          )
        ),
        (
          "japanese_period_sentence_endings: "
          + str(
            len(
              result[
                "japanese_period_lines"
              ]
            )
          )
        ),
        (
          "ascii_comma_prose_lines: "
          + str(
            len(
              result[
                "ascii_comma_lines"
              ]
            )
          )
        ),
        (
          "japanese_comma_prose_lines: "
          + str(
            len(
              result[
                "japanese_comma_lines"
              ]
            )
          )
        ),
        "",
      )
    )

    if result[
      "ascii_period_lines"
    ]:
      lines.append(
        "ASCII period sentence endings:"
      )
      lines.append("")

      for line_number, line in result[
        "ascii_period_lines"
      ]:
        lines.append(
          "- L"
          + str(
            line_number
          )
          + ": `"
          + line.replace(
            "`",
            r"\`",
          )
          + "`"
        )

      lines.append("")

    if result[
      "ascii_comma_lines"
    ]:
      lines.append(
        "ASCII comma prose lines:"
      )
      lines.append("")

      for line_number, line in result[
        "ascii_comma_lines"
      ]:
        lines.append(
          "- L"
          + str(
            line_number
          )
          + ": `"
          + line.replace(
            "`",
            r"\`",
          )
          + "`"
        )

      lines.append("")

    narrative_path = (
      output_dir
      / (
        result[
          "name"
        ]
        + "_narrative.txt"
      )
    )
    narrative_path.write_text(
      result[
        "rendered"
      ],
      encoding="utf-8",
    )

  lines.extend(
    (
      "## R6 normalization target",
      "",
      "- Japanese Narrative prose sentence endings: `。`",
      "- Japanese Narrative prose clause separators: `、`",
      "- Do not alter punctuation inside TeX / mathematical notation.",
      "- Do not alter literature-reference labels such as `Proposition 5.8.`.",
      "- Apply changes at renderer sources, not by blind post-render replacement.",
      "",
      "## Next step",
      "",
      (
        "Use this inventory to choose the smallest shared renderer-level "
        "normalization change for R6 implementation."
      ),
      "",
    )
  )

  report = "\n".join(
    lines
  )
  report_path = (
    output_dir
    / "phase154_r6_punctuation_audit.md"
  )
  report_path.write_text(
    report,
    encoding="utf-8",
  )

  print(
    report
  )
  print(
    "Report:",
    report_path,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
