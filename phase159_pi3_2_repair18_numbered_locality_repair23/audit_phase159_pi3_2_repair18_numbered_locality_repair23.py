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
    report.candidates[
      0
    ].source_candidate.group_result
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

  proof = rendered.split(
    "## 証明\n\n",
    1,
  )[1]
  paragraphs = tuple(
    proof.rstrip(
      "\n"
    ).split(
      "\n\n"
    )
  )

  zero_group = (
    r"[R1] より, $\pi_{2}^{1} = 0$."
  )
  h_injective = (
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は単射}. \qquad (1)"
    "\n\\]"
  )
  e_isomorphism = (
    r"$E(\iota_{1}) = \iota_{2}$ であるから, "
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ は同型."
  )
  e_injective = (
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ は単射."
  )
  delta_zero = (
    r"完全性より, $\Delta: \pi_{3}^{3} "
    r"\to \pi_{1}^{1}$ は零写像."
  )
  h_surjective = (
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は全射}. \qquad (2)"
    "\n\\]"
  )
  h_isomorphism = (
    r"(1), (2) より, "
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
  )
  pi3_target = (
    r"[R1] より, $\pi_{3}^{3} = "
    r"\mathbb{Z}\{\iota_{3}\}$."
  )
  eta2_definition = (
    r"この同型写像により, "
    r"$H(\eta_{2}) = \iota_{3}$ となる "
    r"$\eta_{2} \in \pi_{3}^{2}$ が一意に存在する."
  )
  final_group = (
    r"以上より, $\pi_{3}^{2} = "
    r"\mathbb{Z}\{\eta_{2}\}$."
  )

  print(
    "=== pi3_2 proof after repair23 ==="
  )

  for index, paragraph in enumerate(
    paragraphs
  ):
    print(
      str(
        index
      ).rjust(
        2
      )
      + ": "
      + repr(
        paragraph
      )
    )

  assert (
    paragraphs.index(
      h_injective
    )
    == paragraphs.index(
      zero_group
    ) + 1
  )
  assert (
    paragraphs.index(
      h_isomorphism
    )
    + 1
    == paragraphs.index(
      pi3_target
    )
  )
  assert (
    paragraphs.index(
      pi3_target
    )
    + 1
    == paragraphs.index(
      eta2_definition
    )
  )
  assert (
    paragraphs.index(
      e_isomorphism
    )
    < paragraphs.index(
      e_injective
    )
    < paragraphs.index(
      delta_zero
    )
    < paragraphs.index(
      h_surjective
    )
    < paragraphs.index(
      h_isomorphism
    )
    < paragraphs.index(
      pi3_target
    )
    < paragraphs.index(
      eta2_definition
    )
    < paragraphs.index(
      final_group
    )
  )

  print()
  print(
    "PASS: repair18 locality is compatible with "
    "the current numbered display contract."
  )


if __name__ == "__main__":
  main()
