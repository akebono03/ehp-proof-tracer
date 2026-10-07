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

  print(
    rendered
  )
  print()

  injective = (
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は単射}. \qquad (1)"
    "\n\\]"
  )
  surjective = (
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は全射}. \qquad (2)"
    "\n\\]"
  )
  isomorphism = (
    r"(1), (2) より, "
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
  )

  assert injective in rendered
  assert surjective in rendered
  assert isomorphism in rendered
  assert (
    rendered.index(
      injective
    )
    < rendered.index(
      surjective
    )
    < rendered.index(
      isomorphism
    )
  )

  assert (
    r"[R1] より, $\pi_{2}^{1} = 0$."
    in rendered
  )
  assert (
    r"[R1] より, $\pi_{3}^{3} = "
    r"\mathbb{Z}\{\iota_{3}\}$."
    in rendered
  )
  assert (
    r"$E(\iota_{1}) = \iota_{2}$ であるから, "
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ は同型."
    in rendered
  )

  print(
    "PASS: numbered exactness reasoning and Reference linkage coexist."
  )


if __name__ == "__main__":
  main()
