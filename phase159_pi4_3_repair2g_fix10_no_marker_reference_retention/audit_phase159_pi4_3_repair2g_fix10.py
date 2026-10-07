
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


def main() -> int:
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

  print(
    "=== pi_4^3 public Narrative after fix10 ==="
  )
  print(
    rendered
  )

  required_fragments = (
    "**[R1] (5.1).**",
    r"$\pi_{4}^{5} = 0$",
    r"$\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$",
    "**[R2] Proposition 5.1.**",
    r"$\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$",
    r"$\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$",
  )

  missing = tuple(
    fragment
    for fragment in required_fragments
    if fragment not in rendered
  )

  if missing:
    raise RuntimeError(
      "required public Reference fragments missing:\n"
      + "\n".join(
        missing
      )
    )

  reference_section = rendered.split(
    "---",
    1,
  )[0]

  forbidden_reference_fragments = (
    "Proposition 4.2",
    "EHP exact",
  )

  forbidden = tuple(
    fragment
    for fragment in forbidden_reference_fragments
    if fragment in reference_section
  )

  if forbidden:
    raise RuntimeError(
      "forbidden EHP exactness Reference content found:\n"
      + "\n".join(
        forbidden
      )
    )

  print()
  print(
    "fix10 public Reference audit: PASS"
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
