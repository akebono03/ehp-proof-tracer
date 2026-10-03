from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
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


def _normalize(
  text: str,
) -> str:
  normalized = text
  normalized = normalized.replace(
    "\\[",
    "$",
  )
  normalized = normalized.replace(
    "\\]",
    "$",
  )
  normalized = normalized.replace(
    "$$",
    "$",
  )
  normalized = normalized.replace(
    "**",
    "",
  )
  normalized = normalized.replace(
    "`",
    "",
  )
  normalized = re.sub(
    r"\s+",
    "",
    normalized,
  )
  return normalized


def _headers(
  rendered: str,
):
  result = []

  for line_index, line in enumerate(
    rendered.splitlines()
  ):
    match = re.match(
      r"^\*\*\[R([0-9]+)\]\s+(.+?)\.\*\*$",
      line.strip(),
    )

    if match is None:
      continue

    result.append(
      (
        line_index,
        int(
          match.group(
            1
          )
        ),
        match.group(
          2
        ),
      )
    )

  return tuple(
    result
  )


def _body_markers(
  rendered: str,
):
  header_indices = {
    line_index
    for line_index, _number, _title in _headers(
      rendered
    )
  }

  return tuple(
    int(
      number
    )
    for line_index, line in enumerate(
      rendered.splitlines()
    )
    if line_index not in header_indices
    for number in re.findall(
      r"\[R([0-9]+)\]",
      line,
    )
  )


def _body_lines(
  rendered: str,
):
  lines = rendered.splitlines()

  if "## 証明" in lines:
    proof_index = lines.index(
      "## 証明"
    )
    return tuple(
      lines[
        proof_index + 1:
      ]
    )

  return tuple(
    lines
  )


def _route(
  n: int,
  k: int,
) -> str:
  dimension = n + k

  if (
    dimension == 6
    and n == 3
  ):
    return "pi6_3_generic_multi_argument"

  if (
    dimension == 10
    and n == 4
  ):
    return "phase150_generic_public_wrapper"

  if (
    dimension == 12
    and n == 5
  ):
    return "phase150_generic_public_wrapper"

  if (
    dimension == 16
    and n == 9
  ):
    return "phase150_generic_public_wrapper"

  if (
    dimension == 8
    and n == 5
  ):
    return "pi8_5_special_public_connection"

  if (
    dimension == 15
    and n == 8
  ):
    return "pi15_8_special_public_connection"

  return "standard_public_reference_route"


def _selected_statements_by_number(
  presentation,
):
  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )

  return (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      entries,
    )
  )


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=Path(
      "phase156_r5_repair2_output"
    ),
  )
  args = parser.parse_args()

  args.output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  groups = 0
  exceptions = []
  cases = []

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
        rendered = (
          render_toda_group_proof_narrative_markdown(
            raw_presentation
          )
        )

        headers = _headers(
          rendered
        )
        marker_set = set(
          _body_markers(
            rendered
          )
        )
        unused_headers = tuple(
          (
            line_index,
            number,
            title,
          )
          for line_index, number, title in headers
          if number not in marker_set
        )

        if not unused_headers:
          continue

        body_lines = _body_lines(
          rendered
        )
        selected_by_number = (
          _selected_statements_by_number(
            presentation
          )
        )

        unused_rows = []

        for (
          line_index,
          number,
          title,
        ) in unused_headers:
          statements = selected_by_number.get(
            number,
            (),
          )
          direct_statement_body_lines = []

          for statement in statements:
            normalized_statement = _normalize(
              statement
            )

            for body_line_number, line in enumerate(
              body_lines,
              start=1,
            ):
              if (
                normalized_statement
                and normalized_statement
                in _normalize(
                  line
                )
              ):
                direct_statement_body_lines.append(
                  {
                    "statement": statement,
                    "body_line_number": body_line_number,
                    "body_line": line,
                  }
                )

          nearby_lines = tuple(
            rendered.splitlines()[
              max(
                0,
                line_index - 2,
              ):
              min(
                len(
                  rendered.splitlines()
                ),
                line_index + 8,
              )
            ]
          )

          unused_rows.append(
            {
              "number": number,
              "title": title,
              "selected_statements": statements,
              "direct_statement_body_lines": (
                direct_statement_body_lines
              ),
              "header_neighborhood": "\n".join(
                nearby_lines
              ),
            }
          )

        cases.append(
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
            "headers": tuple(
              number
              for _line_index, number, _title in headers
            ),
            "body_markers": tuple(
              _body_markers(
                rendered
              )
            ),
            "unused_references": unused_rows,
            "body": "\n".join(
              body_lines
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
    "phase": "Phase156-R5-repair2",
    "production_changes": False,
    "groups": groups,
    "exceptions": len(
      exceptions
    ),
    "groups_with_header_without_marker": len(
      cases
    ),
    "cases": [
      {
        key: value
        for key, value in case.items()
        if key not in (
          "full_rendered",
          "body",
        )
      }
      for case in cases
    ],
  }

  (
    args.output_dir
    / "phase156_r5_repair2_result.json"
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
    / "phase156_r5_repair2_full_cases.json"
  ).write_text(
    json.dumps(
      cases,
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
    encoding="utf-8",
  )

  (
    args.output_dir
    / "phase156_r5_repair2_exceptions.json"
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
    "Phase156-R5 repair2 — public header without body marker diagnostic"
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
      cases
    ),
  )
  print()

  for index, case in enumerate(
    cases,
    start=1,
  ):
    print(
      "["
      + str(
        index
      )
      + "] "
      + case[
        "group"
      ]
    )
    print(
      "  route: "
      + case[
        "route"
      ]
    )
    print(
      "  headers: "
      + repr(
        case[
          "headers"
        ]
      )
    )
    print(
      "  body markers: "
      + repr(
        case[
          "body_markers"
        ]
      )
    )

    for unused in case[
      "unused_references"
    ]:
      print(
        "  unused [R"
        + str(
          unused[
            "number"
          ]
        )
        + "] "
        + unused[
          "title"
        ]
      )
      print(
        "    selected statements: "
        + repr(
          unused[
            "selected_statements"
          ]
        )
      )
      print(
        "    direct statement occurrences in body: "
        + str(
          len(
            unused[
              "direct_statement_body_lines"
            ]
          )
        )
      )

      for occurrence in unused[
        "direct_statement_body_lines"
      ]:
        print(
          "      line "
          + str(
            occurrence[
              "body_line_number"
            ]
          )
          + ": "
          + occurrence[
            "body_line"
          ]
        )

    print()

  print(
    "=" * 78
  )

  if (
    groups == 112
    and not exceptions
    and len(
      cases
    )
    == 4
  ):
    print(
      "PASS: the four public-header-without-marker cases were "
      "reproduced and classified for direct statement use."
    )
    return 0

  print(
    "FAIL: diagnostic population differs from the R5 Fixed1 result."
  )
  return 1


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
