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

  before, marker, after = rendered.partition(
    "## 証明"
  )

  if marker != "## 証明":
    raise RuntimeError(
      "proof section marker not found"
    )

  if not before:
    raise RuntimeError(
      "unexpected empty prefix before proof section"
    )

  paragraphs = tuple(
    paragraph.strip()
    for paragraph in after.split(
      "\n\n"
    )
    if paragraph.strip()
  )

  zero_group = (
    "[R1]より, "
    r"$\pi_{2}^{1} = 0$."
  )
  h_injective = (
    "完全性より, "
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は単射."
  )
  delta_zero = (
    "完全性より, "
    r"$\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ "
    "は零写像."
  )
  h_surjective = (
    "完全性より, "
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は全射."
  )
  h_isomorphism = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は同型."
  )

  positions = {
    "zero_group": paragraphs.index(
      zero_group
    ),
    "h_injective": paragraphs.index(
      h_injective
    ),
    "delta_zero": paragraphs.index(
      delta_zero
    ),
    "h_surjective": paragraphs.index(
      h_surjective
    ),
    "h_isomorphism": paragraphs.index(
      h_isomorphism
    ),
  }

  print(
    "=== Phase 159 pi3_2 exactness locality repair7 audit ==="
  )

  for name, index in positions.items():
    print(
      f"{index:3d} {name}"
    )

  checks = (
    (
      "zero_group -> H injective adjacent",
      positions["h_injective"]
      == positions["zero_group"] + 1,
    ),
    (
      "Delta zero -> H surjective adjacent",
      positions["h_surjective"]
      == positions["delta_zero"] + 1,
    ),
    (
      "H injective < H isomorphism",
      positions["h_injective"]
      < positions["h_isomorphism"],
    ),
    (
      "H surjective < H isomorphism",
      positions["h_surjective"]
      < positions["h_isomorphism"],
    ),
  )

  failed = False

  for label, passed in checks:
    print(
      ("PASS" if passed else "FAIL")
      + " "
      + label
    )

    if not passed:
      failed = True

  if failed:
    raise SystemExit(
      1
    )


if __name__ == "__main__":
  main()
