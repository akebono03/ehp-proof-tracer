
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      ROOT
    ),
  )

import toda_group_proof_narrative_contribution_renderer as contribution

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


def _entry_summary(
  entries,
) -> tuple[str, ...]:
  return tuple(
    (
      f"R{entry.number}:"
      f"{entry.reference.locator}:"
      f"{len(entry.proof_steps)}steps"
    )
    for entry in entries
  )


def main() -> int:
  print(
    "=== Phase159 pi_4^3 repair2g fix8 "
    "reference render pipeline audit ==="
  )
  print(
    "Production code changes: NONE"
  )

  original_statement_lines = (
    contribution
    ._toda_group_proof_narrative_reference_statement_lines_by_number
  )
  original_step_usage = (
    contribution
    .filter_toda_group_proof_narrative_reference_entries_by_step_usage
  )
  original_body_usage = (
    contribution
    .filter_toda_group_proof_narrative_reference_entries_by_body_usage
  )
  original_reference_render = (
    contribution
    .render_toda_group_proof_narrative_reference_entries_markdown
  )

  def traced_statement_lines(
    presentation,
    reference_entries,
  ):
    result = original_statement_lines(
      presentation,
      reference_entries,
    )

    print()
    print(
      "--- statement-lines input entries ---"
    )
    for item in _entry_summary(
      reference_entries
    ):
      print(
        item
      )

    print(
      "--- statement-lines output ---"
    )
    if not result:
      print(
        "(empty)"
      )
    else:
      for number, lines in result.items():
        print(
          f"R{number}:"
        )
        for line in lines:
          print(
            "   ",
            line,
          )

    return result

  def traced_step_usage(
    entries,
    statement_lines_by_reference_number,
    used_step_ids,
    root_step,
  ):
    result = original_step_usage(
      entries,
      statement_lines_by_reference_number,
      used_step_ids,
      root_step,
    )

    print()
    print(
      "--- step-usage result ---"
    )
    print(
      "entries:",
      _entry_summary(
        result[0]
      ),
    )
    print(
      "statement keys:",
      tuple(
        result[1].keys()
      ),
    )

    return result

  body_usage_call_count = {
    "value": 0,
  }

  def traced_body_usage(
    entries,
    statement_lines_by_reference_number,
    body_markdown,
  ):
    body_usage_call_count[
      "value"
    ] += 1

    print()
    print(
      "--- body-usage input "
      f"call {body_usage_call_count['value']} ---"
    )
    print(
      "entries:",
      _entry_summary(
        entries
      ),
    )
    print(
      "statement keys:",
      tuple(
        statement_lines_by_reference_number.keys()
      ),
    )
    print(
      "body has marker:",
      "[R" in body_markdown,
    )

    result = original_body_usage(
      entries,
      statement_lines_by_reference_number,
      body_markdown,
    )

    print(
      "--- body-usage output "
      f"call {body_usage_call_count['value']} ---"
    )
    print(
      "entries:",
      _entry_summary(
        result[0]
      ),
    )
    print(
      "statement keys:",
      tuple(
        result[1].keys()
      ),
    )
    print(
      "body has marker:",
      "[R" in result[2],
    )

    return result

  def traced_reference_render(
    entries,
    statement_lines_by_reference_number=None,
  ):
    print()
    print(
      "--- final reference renderer input ---"
    )
    print(
      "entries:",
      _entry_summary(
        entries
      ),
    )
    print(
      "statement keys:",
      (
        None
        if statement_lines_by_reference_number is None
        else tuple(
          statement_lines_by_reference_number.keys()
        )
      ),
    )

    result = original_reference_render(
      entries,
      statement_lines_by_reference_number,
    )

    print(
      "--- final reference renderer output ---"
    )
    print(
      repr(
        result
      )
    )

    return result

  contribution._toda_group_proof_narrative_reference_statement_lines_by_number = (
    traced_statement_lines
  )
  contribution.filter_toda_group_proof_narrative_reference_entries_by_step_usage = (
    traced_step_usage
  )
  contribution.filter_toda_group_proof_narrative_reference_entries_by_body_usage = (
    traced_body_usage
  )
  contribution.render_toda_group_proof_narrative_reference_entries_markdown = (
    traced_reference_render
  )

  report = build_standard_toda_report(
    n=3,
    k=1,
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

  print()
  print(
    "=== final pi_4^3 public Narrative ==="
  )
  print(
    rendered
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
