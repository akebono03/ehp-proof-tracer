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


def _phase159_pi3_2_proof_body() -> str:
  rendered = (
    _phase159_dependency_order_pi3_2()
  )
  before, marker, after = rendered.partition(
    "## 証明"
  )

  assert marker == "## 証明"
  assert before

  return after.lstrip()


def test_phase159_pi3_2_visible_dependency_order_follows_proof_graph():
  body = (
    _phase159_pi3_2_proof_body()
  )

  pi2_zero = (
    r"$\pi_{2}^{1} = 0$."
  )
  pi3_target = (
    r"$\pi_{3}^{3} = "
    r"\mathbb{Z}\{\iota_{3}\}$."
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
  h_injective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は単射."
  )
  h_isomorphism = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は同型."
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
    pi3_target,
    e_isomorphism,
    e_injective,
    delta_zero,
    h_surjective,
    h_injective,
    h_isomorphism,
    eta2_definition,
    final_result,
  ):
    assert sentence in body

  assert body.index(
    pi2_zero
  ) < body.index(
    h_injective
  )

  assert body.index(
    e_isomorphism
  ) < body.index(
    e_injective
  )
  assert body.index(
    e_injective
  ) < body.index(
    delta_zero
  )
  assert body.index(
    delta_zero
  ) < body.index(
    h_surjective
  )

  assert body.index(
    h_injective
  ) < body.index(
    h_isomorphism
  )
  assert body.index(
    h_surjective
  ) < body.index(
    h_isomorphism
  )

  assert body.index(
    pi3_target
  ) < body.index(
    eta2_definition
  )
  assert body.index(
    h_isomorphism
  ) < body.index(
    eta2_definition
  )
  assert body.index(
    eta2_definition
  ) < body.index(
    final_result
  )


def test_phase159_pi3_2_exactness_reason_is_attached():
  body = (
    _phase159_pi3_2_proof_body()
  )

  expected = (
    "完全性より, "
    r"$\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ "
    "は零写像."
  )

  assert expected in body


def test_phase159_pi3_2_stable_order_does_not_pull_definition_forward():
  body = (
    _phase159_pi3_2_proof_body()
  )

  h_isomorphism = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は同型."
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

  assert body.index(
    h_isomorphism
  ) < body.index(
    eta2_definition
  )
  assert body.index(
    eta2_definition
  ) < body.index(
    final_result
  )


def test_phase159_pi3_2_stable_order_preserves_unconstrained_root_order():
  body = (
    _phase159_pi3_2_proof_body()
  )

  pi3_target = (
    r"$\pi_{3}^{3} = "
    r"\mathbb{Z}\{\iota_{3}\}$."
  )
  e_isomorphism = (
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
    "は同型."
  )

  assert body.index(
    pi3_target
  ) < body.index(
    e_isomorphism
  )
