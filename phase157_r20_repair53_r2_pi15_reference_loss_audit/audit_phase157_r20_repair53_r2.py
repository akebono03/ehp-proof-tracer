from __future__ import annotations

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
  _phase153_r3_10_connect_public_reference_section,
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
  render_toda_group_proof_narrative_markdown,
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


def _presentation():
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

  return (
    raw,
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    ),
  )


def _entry_text(
  entry,
) -> str:
  reference = getattr(
    entry,
    "literature_reference",
    None,
  )

  if reference is None:
    return repr(
      entry
    )

  return repr(
    (
      getattr(
        reference,
        "source",
        None,
      ),
      getattr(
        reference,
        "locator",
        None,
      ),
      getattr(
        reference,
        "label",
        None,
      ),
      getattr(
        entry,
        "number",
        None,
      ),
      tuple(
        (
          type(
            proof_step.conclusion
          ).__name__,
          (
            None
            if proof_step.inference_rule
            is None
            else proof_step.inference_rule.name
          ),
        )
        for proof_step in entry.proof_steps
      ),
    )
  )


def _print_entries(
  title: str,
  entries,
) -> None:
  print("")
  print(title)
  print("-" * 96)
  print(
    "count:",
    len(
      entries
    ),
  )

  for entry in entries:
    print(
      _entry_text(
        entry
      )
    )


def main() -> int:
  raw, presentation = (
    _presentation()
  )

  dedicated = (
    _phase134_24_render_pi15_8_narrative(
      presentation
    )
  )

  print("=" * 96)
  print(
    "Phase157-R20 repair53-r2 - pi15 Proposition 4.4 reference loss audit"
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
    "DEDICATED RAW RENDERER"
  )
  print("-" * 96)
  print(
    "has Proposition 4.4 label:",
    (
      dedicated is not None
      and "Toda Proposition 4.4 の分解同型"
      in dedicated
    ),
  )

  entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  _print_entries(
    "GRAPH REFERENCE ENTRIES",
    entries,
  )

  fixed_entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      entries,
      presentation.root_step,
    )
  )
  _print_entries(
    "AFTER FIXED-STATEMENT BOUNDARY",
    fixed_entries,
  )

  statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      fixed_entries,
    )
    if fixed_entries
    else {}
  )

  print("")
  print(
    "STATEMENT LINES"
  )
  print("-" * 96)

  for number, lines in sorted(
    statement_lines.items()
  ):
    print(
      number,
      repr(
        lines
      ),
    )

  if dedicated is None:
    raise RuntimeError(
      "pi15 dedicated renderer unexpectedly returned None"
    )

  lines = dedicated.splitlines()
  proof_header = "## 証明"
  proof_index = lines.index(
    proof_header
  )
  proof_body = "\n".join(
    lines[
      proof_index + 1:
    ]
  ).lstrip()

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
    "BODY-USAGE FILTERED STATEMENT LINES"
  )
  print("-" * 96)

  for number, lines in sorted(
    used_lines.items()
  ):
    print(
      number,
      repr(
        lines
      ),
    )

  connected = (
    _phase153_r3_10_connect_public_reference_section(
      presentation,
      dedicated,
    )
  )

  print("")
  print(
    "CONNECTED PUBLIC OUTPUT"
  )
  print("-" * 96)
  print(
    "has Proposition 4.4 label:",
    (
      "Toda Proposition 4.4 の分解同型"
      in connected
    ),
  )

  final = (
    render_toda_group_proof_narrative_markdown(
      raw
    )
  )

  print("")
  print(
    "FINAL PUBLIC OUTPUT"
  )
  print("-" * 96)
  print(
    "has Proposition 4.4 label:",
    (
      "Toda Proposition 4.4 の分解同型"
      in final
    ),
  )
  print(
    "has [R1] consumer wording:",
    (
      "[R1] より"
      in final
      or "[R1]より"
      in final
    ),
  )

  print("")
  print(
    "FINAL REFERENCE SECTION"
  )
  print("-" * 96)

  if "## 使用する結果" in final:
    reference_part = final.split(
      "## 使用する結果",
      1,
    )[1]

    if "## 証明" in reference_part:
      reference_part = reference_part.split(
        "## 証明",
        1,
      )[0]

    print(
      reference_part.strip()
    )
  else:
    print(
      "(no reference section)"
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
