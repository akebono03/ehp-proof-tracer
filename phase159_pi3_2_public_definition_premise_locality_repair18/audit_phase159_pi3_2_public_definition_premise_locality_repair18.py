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


from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


def main() -> int:
  (
    presentation,
    _,
    _,
    _,
  ) = _method_evidence_data(
    2,
    1,
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]
  paragraphs = tuple(
    paragraph.strip()
    for paragraph in body.split(
      "\n\n"
    )
    if paragraph.strip()
  )

  targets = {
    "zero_group": (
      "[R1]より, "
      r"$\pi_{2}^{1} = 0$."
    ),
    "h_injective": (
      "完全性より, "
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
      "は単射."
    ),
    "e_isomorphism": (
      "[R1]より, "
      r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
      "は同型."
    ),
    "e_injective": (
      r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
      "は単射."
    ),
    "delta_zero": (
      "完全性より, "
      r"$\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ "
      "は零写像."
    ),
    "h_surjective": (
      "完全性より, "
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
      "は全射."
    ),
    "h_isomorphism": (
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
      "は同型."
    ),
    "pi3_target": (
      "[R1]より, "
      r"$\pi_{3}^{3} = "
      r"\mathbb{Z}\{\iota_{3}\}$."
    ),
    "eta2_definition": (
      "この同型写像により, "
      r"$H(\eta_{2}) = \iota_{3}$ となる "
      r"$\eta_{2} \in \pi_{3}^{2}$ "
      "が一意に存在する."
    ),
    "final_group": (
      "以上より, "
      r"$\pi_{3}^{2} = "
      r"\mathbb{Z}\{\eta_{2}\}$."
    ),
  }

  positions = {
    label: paragraphs.index(
      value
    )
    for label, value in targets.items()
  }

  print(
    "=== Phase 159 pi3_2 public definition-premise locality repair18 ==="
  )

  for label, index in positions.items():
    print(
      f"{index:3d} {label}"
    )

  checks = (
    (
      "zero_group -> H injective adjacent",
      positions["h_injective"]
      == positions["zero_group"] + 1,
    ),
    (
      "E branch dependency order",
      positions["e_isomorphism"]
      < positions["e_injective"]
      < positions["delta_zero"]
      < positions["h_surjective"],
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
    (
      "H isomorphism -> pi3 target adjacent",
      positions["pi3_target"]
      == positions["h_isomorphism"] + 1,
    ),
    (
      "pi3 target -> eta2 definition adjacent",
      positions["eta2_definition"]
      == positions["pi3_target"] + 1,
    ),
    (
      "eta2 definition < final group",
      positions["eta2_definition"]
      < positions["final_group"],
    ),
    (
      "QED last",
      paragraphs[-1] == "□",
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

  return 1 if failed else 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
