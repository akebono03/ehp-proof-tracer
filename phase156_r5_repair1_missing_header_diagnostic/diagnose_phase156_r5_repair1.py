from __future__ import annotations

import argparse
import json
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


def _sections(
  rendered: str,
):
  lines = rendered.splitlines()

  if (
    "## 使用する結果" not in lines
    or "## 証明" not in lines
  ):
    return (
      (),
      tuple(
        lines
      ),
    )

  reference_index = lines.index(
    "## 使用する結果"
  )
  proof_index = lines.index(
    "## 証明"
  )

  if reference_index >= proof_index:
    return (
      (),
      tuple(
        lines
      ),
    )

  return (
    tuple(
      lines[
        reference_index
        + 1:
        proof_index
      ]
    ),
    tuple(
      lines[
        proof_index
        + 1:
      ]
    ),
  )


def _header_numbers(
  reference_lines,
):
  result = []

  for line in reference_lines:
    match = re.match(
      r"^\*\*\[R([0-9]+)\]",
      line.strip(),
    )

    if match is None:
      continue

    result.append(
      int(
        match.group(
          1
        )
      )
    )

  return tuple(
    result
  )


def _body_markers(
  body_lines,
):
  return tuple(
    int(
      number
    )
    for line in body_lines
    for number in re.findall(
      r"\[R([0-9]+)\]",
      line,
    )
  )


def _route(
  n: int,
  k: int,
) -> str:
  group_dimension = n + k

  if (
    group_dimension == 6
    and n == 3
  ):
    return "pi6_3_generic_multi_argument"

  if (
    group_dimension == 10
    and n == 4
  ):
    return "phase150_generic_public_wrapper"

  if (
    group_dimension == 12
    and n == 5
  ):
    return "phase150_generic_public_wrapper"

  if (
    group_dimension == 16
    and n == 9
  ):
    return "phase150_generic_public_wrapper"

  if (
    group_dimension == 8
    and n == 5
  ):
    return "pi8_5_special_public_connection"

  if (
    group_dimension == 15
    and n == 8
  ):
    return "pi15_8_special_public_connection"

  return "standard_public_reference_route"


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r5_repair1_output"
    ),
  )
  args = parser.parse_args()

  args.output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  violations = []
  exceptions = []
  groups = 0

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      groups += 1

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
        presentation = (
          build_toda_group_proof_presentation(
            replay
          )
        )
        rendered = (
          render_toda_group_proof_narrative_markdown(
            presentation
          )
        )
        reference_lines, body_lines = (
          _sections(
            rendered
          )
        )
        headers = _header_numbers(
          reference_lines
        )
        markers = _body_markers(
          body_lines
        )
        missing = tuple(
          sorted(
            set(
              markers
            )
            - set(
              headers
            )
          )
        )

        if not missing:
          continue

        marker_lines = tuple(
          line
          for line in body_lines
          if any(
            (
              "[R"
              + str(
                number
              )
              + "]"
            )
            in line
            for number in missing
          )
        )

        violations.append(
          {
            "n": n,
            "k": k,
            "group": _group_label(
              n,
              k,
            ),
            "route": _route(
              n,
              k,
            ),
            "header_numbers": (
              headers
            ),
            "body_marker_numbers": (
              markers
            ),
            "missing_header_numbers": (
              missing
            ),
            "reference_section": "\n".join(
              reference_lines
            ),
            "missing_marker_body_lines": "\n".join(
              marker_lines
            ),
            "full_rendered": rendered,
          }
        )

      except Exception as exc:
        exceptions.append(
          {
            "n": n,
            "k": k,
            "group": _group_label(
              n,
              k,
            ),
            "exception_type": type(
              exc
            ).__name__,
            "exception_message": str(
              exc
            ),
          }
        )

  result = {
    "phase": "Phase156-R5-repair1",
    "production_changes": False,
    "groups": groups,
    "exceptions": len(
      exceptions
    ),
    "body_marker_without_header_occurrences": len(
      violations
    ),
    "violations": [
      {
        key: value
        for key, value in row.items()
        if key != "full_rendered"
      }
      for row in violations
    ],
  }

  (
    args.output_dir
    / "phase156_r5_repair1_result.json"
  ).write_text(
    json.dumps(
      result,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  (
    args.output_dir
    / "phase156_r5_repair1_full_cases.json"
  ).write_text(
    json.dumps(
      violations,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  (
    args.output_dir
    / "phase156_r5_repair1_exceptions.json"
  ).write_text(
    json.dumps(
      exceptions,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  print(
    "=" * 78
  )
  print(
    "Phase156-R5 repair1 — body marker without header diagnostic"
  )
  print(
    "=" * 78
  )
  print(
    "production changes: none"
  )
  print(
    "groups:",
    groups,
  )
  print(
    "exceptions:",
    len(
      exceptions
    ),
  )
  print(
    "violating groups:",
    len(
      violations
    ),
  )
  print()

  for index, row in enumerate(
    violations,
    start=1,
  ):
    print(
      "["
      + str(
        index
      )
      + "] "
      + row[
        "group"
      ]
    )
    print(
      "  n="
      + str(
        row[
          "n"
        ]
      )
      + ", k="
      + str(
        row[
          "k"
        ]
      )
    )
    print(
      "  route: "
      + row[
        "route"
      ]
    )
    print(
      "  headers: "
      + repr(
        row[
          "header_numbers"
        ]
      )
    )
    print(
      "  body markers: "
      + repr(
        row[
          "body_marker_numbers"
        ]
      )
    )
    print(
      "  missing headers: "
      + repr(
        row[
          "missing_header_numbers"
        ]
      )
    )
    print(
      "  offending body lines:"
    )

    for line in row[
      "missing_marker_body_lines"
    ].splitlines():
      print(
        "    "
        + line
      )

    print()

  print(
    "Output:"
  )
  print(
    "  "
    + str(
      args.output_dir
      / "phase156_r5_repair1_result.json"
    )
  )
  print(
    "  "
    + str(
      args.output_dir
      / "phase156_r5_repair1_full_cases.json"
    )
  )
  print(
    "=" * 78
  )

  if (
    groups == 112
    and not exceptions
    and len(
      violations
    )
    == 4
  ):
    print(
      "PASS: the four R5 body-marker/header violations were reproduced "
      "and isolated."
    )
    return 0

  print(
    "FAIL: diagnostic population differs from the R5 result."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
