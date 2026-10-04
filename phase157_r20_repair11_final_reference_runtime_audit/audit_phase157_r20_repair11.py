from __future__ import annotations

import sys
from pathlib import Path


REPOSITORY_ROOT = Path(
  __file__
).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )


import toda_group_proof_narrative_contribution_renderer as contribution_renderer
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


TARGETS = {
  "Proposition 5.6",
  "(5.3)",
  "Proposition 5.3",
  "Proposition 5.1",
  "Proposition 2.2",
}


def dump_state(
  label,
  entries,
  statement_lines,
  body=None,
) -> None:
  print("")
  print("=" * 88)
  print(label)
  print("=" * 88)

  for entry in entries:
    locator = entry.reference.locator

    if locator not in TARGETS:
      continue

    print(
      f"[R{entry.number}] {locator}"
    )

    lines = statement_lines.get(
      entry.number,
      (),
    )

    for line in lines:
      print(
        "  ",
        line,
      )

    if body is not None:
      marker = (
        "[R"
        + str(
          entry.number
        )
        + "]"
      )
      print(
        "  marker_in_body=",
        marker in body,
      )

  if body is not None:
    print("")
    print(
      "body markers:",
      [
        token
        for token in (
          "[R1]",
          "[R2]",
          "[R3]",
          "[R4]",
          "[R5]",
          "[R6]",
          "[R7]",
          "[R8]",
        )
        if token in body
      ],
    )


original_statement_lines = (
  contribution_renderer
  ._toda_group_proof_narrative_reference_statement_lines_by_number
)
original_body_filter = (
  contribution_renderer
  .filter_toda_group_proof_narrative_reference_entries_by_body_usage
)
original_restore = (
  contribution_renderer
  .restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage
)
original_reference_render = (
  contribution_renderer
  .render_toda_group_proof_narrative_reference_entries_markdown
)


statement_call_count = 0
body_filter_call_count = 0
restore_call_count = 0
reference_render_call_count = 0


def traced_statement_lines(
  presentation,
  reference_entries,
):
  global statement_call_count
  statement_call_count += 1

  result = original_statement_lines(
    presentation,
    reference_entries,
  )

  dump_state(
    "STATEMENT-LINES CALL "
    + str(
      statement_call_count
    ),
    reference_entries,
    result,
  )

  return result


def traced_body_filter(
  entries,
  statement_lines,
  body,
):
  global body_filter_call_count
  body_filter_call_count += 1

  dump_state(
    "BODY-FILTER "
    + str(
      body_filter_call_count
    )
    + " INPUT",
    entries,
    statement_lines,
    body,
  )

  result = original_body_filter(
    entries,
    statement_lines,
    body,
  )

  dump_state(
    "BODY-FILTER "
    + str(
      body_filter_call_count
    )
    + " OUTPUT",
    result[0],
    result[1],
    result[2],
  )

  return result


def traced_restore(
  original_entries,
  original_statement_lines,
  filtered_entries,
  filtered_statement_lines,
  body,
  root_step,
  used_step_ids,
  presentation=None,
):
  global restore_call_count
  restore_call_count += 1

  dump_state(
    "RESTORE "
    + str(
      restore_call_count
    )
    + " ORIGINAL",
    original_entries,
    original_statement_lines,
    body,
  )
  dump_state(
    "RESTORE "
    + str(
      restore_call_count
    )
    + " FILTERED INPUT",
    filtered_entries,
    filtered_statement_lines,
    body,
  )

  result = original_restore(
    original_entries,
    original_statement_lines,
    filtered_entries,
    filtered_statement_lines,
    body,
    root_step,
    used_step_ids,
    presentation=presentation,
  )

  dump_state(
    "RESTORE "
    + str(
      restore_call_count
    )
    + " OUTPUT",
    result[0],
    result[1],
    result[2],
  )

  return result


def traced_reference_render(
  entries,
  statement_lines,
):
  global reference_render_call_count
  reference_render_call_count += 1

  dump_state(
    "FINAL REFERENCE RENDER INPUT "
    + str(
      reference_render_call_count
    ),
    entries,
    statement_lines,
  )

  return original_reference_render(
    entries,
    statement_lines,
  )


def main() -> int:
  print(
    "Repository root:",
    REPOSITORY_ROOT,
  )

  contribution_renderer._toda_group_proof_narrative_reference_statement_lines_by_number = (
    traced_statement_lines
  )
  contribution_renderer.filter_toda_group_proof_narrative_reference_entries_by_body_usage = (
    traced_body_filter
  )
  contribution_renderer.restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage = (
    traced_restore
  )
  contribution_renderer.render_toda_group_proof_narrative_reference_entries_markdown = (
    traced_reference_render
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

  print("")
  print("=" * 88)
  print("FINAL PUBLIC NARRATIVE")
  print("=" * 88)
  print(
    rendered
  )

  print("")
  print("=" * 88)
  print("CALL COUNTS")
  print("=" * 88)
  print(
    "statement_lines:",
    statement_call_count,
  )
  print(
    "body_filter:",
    body_filter_call_count,
  )
  print(
    "restore:",
    restore_call_count,
  )
  print(
    "reference_render:",
    reference_render_call_count,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
