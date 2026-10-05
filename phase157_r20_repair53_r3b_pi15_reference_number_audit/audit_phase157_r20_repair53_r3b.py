from __future__ import annotations

import re
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _phase134_24_render_pi15_8_narrative,
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
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


def _data():
  report = build_standard_toda_report(
    n=8,
    k=7,
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
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )

  return (
    raw,
    presentation,
  )


def _print_entries(
  title,
  entries,
) -> None:
  print("")
  print(title)
  print("-" * 96)

  for entry in entries:
    print(
      {
        "number": entry.number,
        "locator": entry.reference.locator,
        "label": entry.reference.label,
        "proof_steps": tuple(
          (
            type(
              step.conclusion
            ).__name__,
            (
              None
              if step.inference_rule is None
              else step.inference_rule.name
            ),
          )
          for step in entry.proof_steps
        ),
      }
    )


def main() -> int:
  raw, presentation = _data()

  dedicated = (
    _phase134_24_render_pi15_8_narrative(
      presentation
    )
  )

  if dedicated is None:
    raise RuntimeError(
      "dedicated pi15 renderer returned None"
    )

  lines = dedicated.splitlines()
  proof_index = lines.index(
    "## 証明"
  )
  proof_body = "\n".join(
    lines[
      proof_index + 1:
    ]
  ).lstrip()

  print("=" * 96)
  print(
    "Phase157-R20 repair53-r3b - pi15 Reference number audit"
  )
  print("=" * 96)
  print(
    "Production code changes: none"
  )
  print(
    "pytest: not run"
  )

  print("")
  print(
    "DEDICATED BODY MARKERS"
  )
  print("-" * 96)
  print(
    tuple(
      int(
        match.group(
          1
        )
      )
      for match in re.finditer(
        r"\[R([0-9]+)\]",
        proof_body,
      )
    )
  )
  print("")
  print(
    "marker lines:"
  )

  for line in proof_body.splitlines():
    if "[R" in line:
      print(
        repr(
          line
        )
      )

  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  _print_entries(
    "GRAPH ENTRIES",
    entries,
  )

  fixed_entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      entries,
      presentation.root_step,
    )
  )
  _print_entries(
    "AFTER FIXED BOUNDARY",
    fixed_entries,
  )

  statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      fixed_entries,
    )
  )

  print("")
  print(
    "STATEMENT LINES BY NUMBER"
  )
  print("-" * 96)

  for number, lines_for_number in sorted(
    statement_lines.items()
  ):
    print(
      number,
      tuple(
        lines_for_number
      ),
    )

  (
    used_entries,
    used_lines,
    filtered_body,
  ) = (
    filter_toda_group_proof_narrative_reference_entries_by_body_usage(
      fixed_entries,
      statement_lines,
      proof_body,
    )
  )

  _print_entries(
    "AFTER BODY-USAGE FILTER",
    used_entries,
  )

  print("")
  print(
    "FILTERED BODY MARKER LINES"
  )
  print("-" * 96)

  for line in filtered_body.splitlines():
    if "[R" in line:
      print(
        repr(
          line
        )
      )

  print("")
  print(
    "AUDIT COMPLETE"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
