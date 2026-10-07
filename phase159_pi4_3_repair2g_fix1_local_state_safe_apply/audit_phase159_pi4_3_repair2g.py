from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      ROOT
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


def render(
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
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def section(
  rendered: str,
  heading: str,
  next_marker: str,
) -> str:
  start = rendered.index(
    heading
  )
  end = rendered.index(
    next_marker,
    start,
  )
  return rendered[
    start:end
  ]


def main() -> int:
  pi3 = render(
    2,
    1,
  )
  pi4 = render(
    3,
    1,
  )

  print(
    "=" * 80
  )
  print(
    "Phase 159 pi_4^3 repair2g verification"
  )
  print(
    "=" * 80
  )

  print()
  print(
    "[pi_3^2 Reference]"
  )
  print(
    section(
      pi3,
      "## 使用する結果",
      "---",
    )
  )

  print()
  print(
    "[pi_4^3 Reference]"
  )
  print(
    section(
      pi4,
      "## 使用する結果",
      "---",
    )
  )

  print()
  print(
    "[pi_4^3 Proof]"
  )
  proof_start = pi4.index(
    "## 証明"
  )
  print(
    pi4[
      proof_start:
    ]
  )

  print()
  print(
    "CHECK pi3 has R1 (5.1):",
    "**[R1] (5.1).**"
    in pi3,
  )
  print(
    "CHECK pi4 has R1 (5.1):",
    "**[R1] (5.1).**"
    in pi4,
  )
  print(
    "CHECK pi4 has R2 Proposition 5.1:",
    "**[R2] Proposition 5.1.**"
    in pi4,
  )

  pi4_ref = section(
    pi4,
    "## 使用する結果",
    "---",
  )

  print(
    "CHECK no Proposition 4.2 Reference:",
    "Proposition 4.2"
    not in pi4_ref,
  )
  print(
    "CHECK no exactness arrow in Reference:",
    r"\xrightarrow"
    not in pi4_ref,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
