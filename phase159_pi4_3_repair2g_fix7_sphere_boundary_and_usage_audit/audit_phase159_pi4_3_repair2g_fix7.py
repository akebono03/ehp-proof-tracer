
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
import toda_group_proof_narrative_references as references

from low_dimensional_facts import (
  pi_4_5_zero_fact,
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
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
)
from toda_upstream_bootstrap import (
  _build_phase50_result,
)


def _entry_text(
  entry,
) -> str:
  parts = []

  for step in entry.proof_steps:
    boundary = (
      classify_toda_literature_statement_step(
        step
      )
    )
    parts.append(
      (
        type(
          step.conclusion
        ).__name__
        + ":"
        + (
          "NONE"
          if boundary is None
          else (
            boundary.classification.value
            + "/"
            + boundary.reference_locator
            + "/"
            + str(
              boundary.component_key
            )
          )
        )
      )
    )

  return (
    f"R{entry.number} "
    f"{entry.reference.locator} "
    + " | ".join(
      parts
    )
  )


def main() -> int:
  print(
    "=== Phase159 pi_4^3 repair2g fix7 audit ==="
  )

  phase50 = _build_phase50_result()
  pi4_zero_step = next(
    step
    for step in phase50[
      "result"
    ].steps
    if (
      step.conclusion
      == pi_4_5_zero_fact()
    )
  )
  pi4_zero_boundary = (
    classify_toda_literature_statement_step(
      pi4_zero_step
    )
  )

  print(
    "pi_4^5=0 boundary:",
    pi4_zero_boundary,
  )

  if (
    pi4_zero_boundary is None
    or pi4_zero_boundary.component_key
    != "sphere_connectivity_zero"
  ):
    raise RuntimeError(
      "sphere_connectivity_zero fixed mapping is not active"
    )

  original_fixed_filter = (
    contribution
    .filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary
  )
  original_usage_filter = (
    contribution
    .filter_toda_group_proof_narrative_reference_entries_by_step_usage
  )

  def traced_fixed_filter(
    entries,
    root_step,
  ):
    print()
    print(
      "--- fixed-boundary filter input ---"
    )
    for entry in entries:
      print(
        _entry_text(
          entry
        )
      )

    result = original_fixed_filter(
      entries,
      root_step,
    )

    print(
      "--- fixed-boundary filter output ---"
    )
    for entry in result:
      print(
        _entry_text(
          entry
        )
      )

    return result

  def traced_usage_filter(
    entries,
    statement_lines_by_reference_number,
    used_step_ids,
    root_step,
  ):
    print()
    print(
      "--- step-usage filter input ---"
    )
    print(
      "used_step_ids count:",
      len(
        used_step_ids
      ),
    )

    for entry in entries:
      flags = tuple(
        id(
          step
        )
        in used_step_ids
        for step in entry.proof_steps
      )
      print(
        _entry_text(
          entry
        ),
        "used_flags=",
        flags,
      )

    result = original_usage_filter(
      entries,
      statement_lines_by_reference_number,
      used_step_ids,
      root_step,
    )

    print(
      "--- step-usage filter output ---"
    )
    for entry in result[0]:
      print(
        _entry_text(
          entry
        )
      )

    if not result[0]:
      print(
        "(empty)"
      )

    return result

  contribution.filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary = (
    traced_fixed_filter
  )
  contribution.filter_toda_group_proof_narrative_reference_entries_by_step_usage = (
    traced_usage_filter
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

  print()
  print(
    "=== render pi_4^3 ==="
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  print()
  print(
    "=== public Narrative ==="
  )
  print(
    rendered
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
