from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(
  REPO_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
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
    n=2,
    k=1,
  )
  group_result = (
    report.candidates[0]
    .source_candidate.group_result
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

  marker = "## 証明"
  marker_index = rendered.find(
    marker
  )

  if marker_index < 0:
    raise RuntimeError(
      "proof marker not found"
    )

  proof = rendered[
    marker_index:
  ]

  required_fragments = (
    "完全性より,",
    (
      r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
      r"\quad\text{は単射}. \qquad (1)"
    ),
    (
      r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
      r"\quad\text{は全射}. \qquad (2)"
    ),
    (
      r"(1), (2) より, "
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
    ),
  )

  missing = tuple(
    fragment
    for fragment in required_fragments
    if fragment not in proof
  )

  if missing:
    raise AssertionError(
      "expected pi_3^2 public narrative fragments are missing: "
      + repr(
        missing
      )
    )

  print(
    proof
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
