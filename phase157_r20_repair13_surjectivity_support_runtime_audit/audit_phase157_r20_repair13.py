from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(0, str(REPOSITORY_ROOT))

import toda_group_proof_narrative_contribution_renderer as renderer

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


original_order = (
  renderer
  .order_toda_group_proof_narrative_surjectivity_support
)
original_filter = (
  renderer
  .filter_toda_group_proof_narrative_reference_entries_by_body_usage
)

order_count = 0
filter_count = 0


def print_excerpt(
  label,
  markdown,
):
  print("")
  print("=" * 88)
  print(label)
  print("=" * 88)

  paragraphs = markdown.split(
    "\n\n"
  )

  for index, paragraph in enumerate(
    paragraphs
  ):
    if (
      "pi_{7}^{5}" in paragraph
      or r"\pi_{7}^{5}" in paragraph
      or "は全射である" in paragraph
      or "[R3]" in paragraph
      or "[R4]" in paragraph
      or "[R5]" in paragraph
      or "[R6]" in paragraph
    ):
      print(
        f"[{index}] {paragraph}"
      )


def traced_order(
  presentation,
  markdown,
  reference_entries=(),
  statement_lines_by_reference_number=None,
):
  global order_count
  order_count += 1

  print_excerpt(
    "SURJECTIVITY SUPPORT INPUT "
    + str(
      order_count
    ),
    markdown,
  )

  print("")
  print("REFERENCE STATEMENTS AT ORDER CALL")

  for entry in reference_entries:
    if entry.reference.locator in (
      "Proposition 5.3",
      "Proposition 5.1",
      "Proposition 2.2",
    ):
      print(
        "[R"
        + str(
          entry.number
        )
        + "] ",
        entry.reference.locator,
        sep="",
      )

      if statement_lines_by_reference_number is not None:
        for line in (
          statement_lines_by_reference_number.get(
            entry.number,
            (),
          )
        ):
          print(
            "   ",
            line,
          )

  result = original_order(
    presentation,
    markdown,
    reference_entries,
    statement_lines_by_reference_number,
  )

  print_excerpt(
    "SURJECTIVITY SUPPORT OUTPUT "
    + str(
      order_count
    ),
    result,
  )

  return result


def traced_filter(
  entries,
  statement_lines,
  body,
):
  global filter_count
  filter_count += 1

  print_excerpt(
    "BODY FILTER "
    + str(
      filter_count
    )
    + " INPUT BODY",
    body,
  )

  print("")
  print(
    "BODY FILTER ",
    filter_count,
    " REFERENCES",
    sep="",
  )

  for entry in entries:
    if entry.reference.locator in (
      "Proposition 5.3",
      "Proposition 5.1",
      "Proposition 2.2",
    ):
      print(
        "[R"
        + str(
          entry.number
        )
        + "] ",
        entry.reference.locator,
        " marker=",
        (
          "[R"
          + str(
            entry.number
          )
          + "]"
        )
        in body,
        sep="",
      )

  return original_filter(
    entries,
    statement_lines,
    body,
  )


def main() -> int:
  renderer.order_toda_group_proof_narrative_surjectivity_support = (
    traced_order
  )
  renderer.filter_toda_group_proof_narrative_reference_entries_by_body_usage = (
    traced_filter
  )

  report = build_standard_toda_report(
    n=3,
    k=3,
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

  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  print("")
  print("=" * 88)
  print("FINAL REFERENCE HEADERS")
  print("=" * 88)

  reference_section = rendered.split(
    "---",
    1,
  )[0]

  for line in reference_section.splitlines():
    if line.startswith(
      "**[R"
    ):
      print(
        line
      )

  print("")
  print("=" * 88)
  print("COUNTS")
  print("=" * 88)
  print(
    "order calls:",
    order_count,
  )
  print(
    "body filter calls:",
    filter_count,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
