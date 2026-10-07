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


def render_group(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def main() -> int:
  pi3 = render_group(
    2,
    1,
  )

  print(
    "=== pi_3^2 public Narrative after fix10i ==="
  )
  print(
    pi3
  )

  required_pi3 = (
    (
      r"\\["
      "\\n"
      r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"
      r"\\quad\\text{は単射}. \\qquad (1)"
      "\\n"
      r"\\]"
    ),
    (
      r"\\["
      "\\n"
      r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"
      r"\\quad\\text{は全射}. \\qquad (2)"
      "\\n"
      r"\\]"
    ),
    (
      r"$\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ "
      "は零写像."
    ),
    (
      r"$E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$ "
      "は同型."
    ),
    (
      r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "
      "は同型."
    ),
  )

  missing = tuple(
    fragment
    for fragment in required_pi3
    if fragment not in pi3
  )

  if missing:
    raise RuntimeError(
      "pi_3^2 contract missing:\\n"
      + "\\n".join(
        missing
      )
    )

  forbidden = (
    r"\\tag{1}",
    r"\\tag{2}",
    "は単射である.",
    "は全射である.",
    "は同型写像である.",
    "は零写像である.",
  )

  present = tuple(
    fragment
    for fragment in forbidden
    if fragment in pi3
  )

  if present:
    raise RuntimeError(
      "stale pi_3^2 wording/numbering remains:\\n"
      + "\\n".join(
        present
      )
    )

  pi4 = render_group(
    3,
    1,
  )

  print()
  print(
    "=== pi_4^3 public Narrative after fix10i ==="
  )
  print(
    pi4
  )

  required_pi4 = (
    "**[R1] (5.1).**",
    r"$\\pi_{4}^{5} = 0$",
    r"$\\pi_{5}^{5} = \\mathbb{Z}\\{\\iota_{5}\\}$",
    "**[R2] Proposition 5.1.**",
    r"$\\pi_{3}^{2} = \\mathbb{Z}\\{\\eta_{2}\\}$",
    r"$\\Delta\\left(\\iota_{5}\\right) = \\pm 2\\eta_{2}$",
  )

  missing_pi4 = tuple(
    fragment
    for fragment in required_pi4
    if fragment not in pi4
  )

  if missing_pi4:
    raise RuntimeError(
      "pi_4^3 Reference regression:\\n"
      + "\\n".join(
        missing_pi4
      )
    )

  print()
  print(
    "fix10i audit: PASS"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
