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


def main() -> None:
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

  body = rendered.split(
    "## 証明\\n\\n",
    1,
  )[1]

  labels = (
    (
      "pi2_zero",
      r"$\\pi_{2}^{1} = 0$.",
    ),
    (
      "h_injective",
      "完全性より, "
      r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "
      "は単射.",
    ),
    (
      "pi3_target",
      r"$\\pi_{3}^{3} = "
      r"\\mathbb{Z}\\{\\iota_{3}\\}$.",
    ),
    (
      "e_isomorphism",
      r"$E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$ "
      "は同型.",
    ),
    (
      "e_injective",
      r"$E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$ "
      "は単射.",
    ),
    (
      "delta_zero",
      "完全性より, "
      r"$\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ "
      "は零写像.",
    ),
    (
      "h_surjective",
      "完全性より, "
      r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "
      "は全射.",
    ),
    (
      "h_isomorphism",
      r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "
      "は同型.",
    ),
  )

  print(
    "=== Phase 159 pi3_2 public dependency order ==="
  )

  rows = []

  for label, sentence in labels:
    index = body.find(
      sentence
    )
    rows.append(
      (
        index,
        label,
        sentence,
      )
    )

  for index, label, sentence in sorted(
    rows
  ):
    print(
      f"{index:6d}  {label}: {sentence}"
    )

  print()
  print(
    "Expected branch-continuity constraints:"
  )
  print(
    "pi2_zero < h_injective < pi3_target"
  )
  print(
    "e_isomorphism < e_injective < delta_zero < h_surjective"
  )


if __name__ == "__main__":
  main()
