
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(ROOT),
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


def main() -> int:
  report = build_standard_toda_report(
    n=2,
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

  print(
    "=== pi_3^2 current public Narrative ==="
  )
  print(
    rendered
  )

  print()
  print(
    "=== wording contract probes ==="
  )

  probes = (
    "は単射.",
    "は単射である.",
    "は全射.",
    "は全射である.",
    "は同型.",
    "は同型写像である.",
    "は零写像.",
    "は零写像である.",
    r"\tag{1}",
    r"\tag{2}",
    r"\qquad (1)",
    r"\qquad (2)",
  )

  for probe in probes:
    print(
      repr(
        probe
      ),
      "=>",
      rendered.count(
        probe
      ),
    )

  print()
  print(
    "=== paragraphs containing map-property wording ==="
  )

  for paragraph in rendered.split(
    "\n\n"
  ):
    if any(
      token in paragraph
      for token in (
        "単射",
        "全射",
        "同型",
        "零写像",
      )
    ):
      print(
        "---"
      )
      print(
        paragraph
      )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
