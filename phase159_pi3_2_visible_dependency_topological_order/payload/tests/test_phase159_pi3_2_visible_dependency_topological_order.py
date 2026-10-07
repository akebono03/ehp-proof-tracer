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


def _phase159_dependency_order_pi3_2() -> str:
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

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase159_pi3_2_visible_dependency_order_follows_proof_graph():
  rendered = (
    _phase159_dependency_order_pi3_2()
  )

  pi2_zero = (
    r"$\pi_{2}^{1} = 0$."
  )
  h_injective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は単射."
  )
  e_isomorphism = (
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
    "は同型."
  )
  e_injective = (
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
    "は単射."
  )
  delta_zero = (
    r"$\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ "
    "は零写像."
  )
  h_surjective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は全射."
  )
  h_isomorphism = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は同型."
  )
  pi3_target = (
    r"$\pi_{3}^{3} = "
    r"\mathbb{Z}\{\iota_{3}\}$."
  )
  eta2_definition = (
    "この同型写像により, "
    r"$H(\eta_{2}) = \iota_{3}$ となる "
    r"$\eta_{2} \in \pi_{3}^{2}$ が一意に存在する."
  )
  final_result = (
    r"以上より, $\pi_{3}^{2} = "
    r"\mathbb{Z}\{\eta_{2}\}$."
  )

  for sentence in (
    pi2_zero,
    h_injective,
    e_isomorphism,
    e_injective,
    delta_zero,
    h_surjective,
    h_isomorphism,
    pi3_target,
    eta2_definition,
    final_result,
  ):
    assert sentence in rendered

  assert rendered.index(
    pi2_zero
  ) < rendered.index(
    h_injective
  )

  assert rendered.index(
    e_isomorphism
  ) < rendered.index(
    e_injective
  )
  assert rendered.index(
    e_injective
  ) < rendered.index(
    delta_zero
  )
  assert rendered.index(
    delta_zero
  ) < rendered.index(
    h_surjective
  )

  assert rendered.index(
    h_injective
  ) < rendered.index(
    h_isomorphism
  )
  assert rendered.index(
    h_surjective
  ) < rendered.index(
    h_isomorphism
  )

  assert rendered.index(
    pi3_target
  ) < rendered.index(
    eta2_definition
  )
  assert rendered.index(
    h_isomorphism
  ) < rendered.index(
    eta2_definition
  )
  assert rendered.index(
    eta2_definition
  ) < rendered.index(
    final_result
  )


def test_phase159_pi3_2_visible_dependency_order_keeps_exactness_reason_attached():
  rendered = (
    _phase159_dependency_order_pi3_2()
  )

  assert (
    "完全性より, "
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は単射."
    in rendered
  )
  assert (
    "完全性より, "
    r"$\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ "
    "は零写像."
    in rendered
  )
  assert (
    "完全性より, "
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は全射."
    in rendered
  )
