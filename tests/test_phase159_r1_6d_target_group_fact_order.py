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


def _phase159_r1_6d_repair2_pi3_2_presentation():
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

  return build_toda_group_proof_presentation(
    replay
  )


def test_phase159_r1_6d_target_group_fact_follows_surjectivity():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6d_repair2_pi3_2_presentation()
    )
  )

  surjective = (
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は全射}. \qquad (2)"
  )
  target_group = (
    r"[R1] より, $\pi_{3}^{3} = "
    r"\mathbb{Z}\{\iota_{3}\}$."
  )
  isomorphism = (
    r"(1), (2) より, "
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
  )
  eta_definition = (
    r"$H(\eta_{2}) = \iota_{3}$ となる "
    r"$\eta_{2} \in \pi_{3}^{2}$ が一意に存在する."
  )

  assert surjective in rendered
  assert target_group in rendered
  assert isomorphism in rendered
  assert eta_definition in rendered

  assert (
    rendered.index(
      surjective
    )
    < rendered.index(
      target_group
    )
    < rendered.index(
      isomorphism
    )
    < rendered.index(
      eta_definition
    )
  )


def test_phase159_r1_6d_target_group_fact_is_not_before_surjectivity():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6d_repair2_pi3_2_presentation()
    )
  )

  zero_map = (
    r"完全性より, $\Delta: \pi_{3}^{3} "
    r"\to \pi_{1}^{1}$ は零写像."
  )
  target_group = (
    r"[R1] より, $\pi_{3}^{3} = "
    r"\mathbb{Z}\{\iota_{3}\}$."
  )
  surjective = (
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は全射}. \qquad (2)"
  )

  assert (
    rendered.index(
      zero_map
    )
    < rendered.index(
      surjective
    )
    < rendered.index(
      target_group
    )
  )
