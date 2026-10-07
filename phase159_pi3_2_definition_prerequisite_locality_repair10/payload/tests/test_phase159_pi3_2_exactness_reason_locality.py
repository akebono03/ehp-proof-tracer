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


def _phase159_pi3_2_body() -> str:
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

  assert marker == "## 証明"
  assert before

  return after.lstrip()


def _paragraphs(
  body: str,
) -> tuple[
  str,
  ...,
]:
  return tuple(
    paragraph.strip()
    for paragraph in body.split(
      "\n\n"
    )
    if paragraph.strip()
  )


def test_phase159_pi3_2_zero_group_is_immediately_followed_by_h_injective():
  paragraphs = _paragraphs(
    _phase159_pi3_2_body()
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

  assert (
    paragraphs.index(
      h_injective
    )
    == paragraphs.index(
      zero_group
    ) + 1
  )


def test_phase159_pi3_2_delta_zero_is_immediately_followed_by_h_surjective():
  paragraphs = _paragraphs(
    _phase159_pi3_2_body()
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

  assert (
    paragraphs.index(
      h_surjective
    )
    == paragraphs.index(
      delta_zero
    ) + 1
  )


def test_phase159_pi3_2_pi3_target_is_immediately_before_eta2_definition():
  paragraphs = _paragraphs(
    _phase159_pi3_2_body()
  )

  pi3_target = (
    "[R1]より, "
    r"$\pi_{3}^{3} = "
    r"\mathbb{Z}\{\iota_{3}\}$."
  )
  eta2_definition = (
    "この同型写像により, "
    r"$H(\eta_{2}) = \iota_{3}$ となる "
    r"$\eta_{2} \in \pi_{3}^{2}$ が一意に存在する."
  )

  assert (
    paragraphs.index(
      eta2_definition
    )
    == paragraphs.index(
      pi3_target
    ) + 1
  )


def test_phase159_pi3_2_h_isomorphism_precedes_definition_prerequisite():
  body = (
    _phase159_pi3_2_body()
  )

  h_isomorphism = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は同型."
  )
  pi3_target = (
    "[R1]より, "
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

  assert body.index(
    h_isomorphism
  ) < body.index(
    pi3_target
  )
  assert body.index(
    pi3_target
  ) < body.index(
    eta2_definition
  )
  assert body.index(
    eta2_definition
  ) < body.index(
    final_result
  )


def test_phase159_pi3_2_exactness_locality_preserves_e_branch():
  body = (
    _phase159_pi3_2_body()
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
    h_surjective
  ) < body.index(
    h_isomorphism
  )
