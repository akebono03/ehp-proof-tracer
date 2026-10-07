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

  body = after.lstrip()

  labels = (
    (
      "pi2_zero",
      r"$\pi_{2}^{1} = 0$.",
    ),
    (
      "pi3_target",
      r"$\pi_{3}^{3} = "
      r"\mathbb{Z}\{\iota_{3}\}$.",
    ),
    (
      "e_isomorphism",
      r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ は同型.",
    ),
    (
      "e_injective",
      r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ は単射.",
    ),
    (
      "delta_zero",
      "完全性より, "
      r"$\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ は零写像.",
    ),
    (
      "h_surjective",
      "完全性より, "
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は全射.",
    ),
    (
      "h_injective",
      "完全性より, "
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射.",
    ),
    (
      "h_isomorphism",
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型.",
    ),
    (
      "eta2_definition",
      "この同型写像により, "
      r"$H(\eta_{2}) = \iota_{3}$ となる "
      r"$\eta_{2} \in \pi_{3}^{2}$ が一意に存在する.",
    ),
    (
      "final_result",
      r"以上より, $\pi_{3}^{2} = "
      r"\mathbb{Z}\{\eta_{2}\}$.",
    ),
  )

  positions = {}

  print(
    "=== Phase 159 pi3_2 repair5 stable-order audit ==="
  )

  for label, sentence in labels:
    index = body.find(
      sentence
    )

    if index < 0:
      raise RuntimeError(
        "missing statement: "
        + label
      )

    positions[
      label
    ] = index

    print(
      f"{index:6d}  {label}: {sentence}"
    )

  checks = (
    (
      "pi2_zero < h_injective",
      positions["pi2_zero"]
      < positions["h_injective"],
    ),
    (
      "e_isomorphism < e_injective",
      positions["e_isomorphism"]
      < positions["e_injective"],
    ),
    (
      "e_injective < delta_zero",
      positions["e_injective"]
      < positions["delta_zero"],
    ),
    (
      "delta_zero < h_surjective",
      positions["delta_zero"]
      < positions["h_surjective"],
    ),
    (
      "h_injective < h_isomorphism",
      positions["h_injective"]
      < positions["h_isomorphism"],
    ),
    (
      "h_surjective < h_isomorphism",
      positions["h_surjective"]
      < positions["h_isomorphism"],
    ),
    (
      "pi3_target < eta2_definition",
      positions["pi3_target"]
      < positions["eta2_definition"],
    ),
    (
      "h_isomorphism < eta2_definition",
      positions["h_isomorphism"]
      < positions["eta2_definition"],
    ),
    (
      "eta2_definition < final_result",
      positions["eta2_definition"]
      < positions["final_result"],
    ),
  )

  print()
  print(
    "=== checks ==="
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
