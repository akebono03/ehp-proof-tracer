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


def _phase159_r1_6d_pi3_2_presentation():
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


def test_phase159_r1_6d_diagonal_group_notation_uses_braces():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6d_pi3_2_presentation()
    )
  )
  reference = (
    rendered.split(
      "## 使用する結果\n\n",
      1,
    )[1].split(
      "\n---\n",
      1,
    )[0]
  )

  assert (
    r"$\pi_{n}^{n} = "
    r"\mathbb{Z}\{\iota_{n}\}$."
    in reference
  )
  assert r"\langle" not in reference
  assert r"\rangle" not in reference


def test_phase159_r1_6d_suspension_isomorphism_is_derived_in_body():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6d_pi3_2_presentation()
    )
  )

  assert (
    r"[R1] より, $\pi_{1}^{1} = "
    r"\mathbb{Z}\{\iota_{1}\}$, "
    r"$\pi_{2}^{2} = "
    r"\mathbb{Z}\{\iota_{2}\}$."
    in rendered
  )
  assert (
    r"$E(\iota_{1}) = \iota_{2}$ であるから, "
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ は同型."
    in rendered
  )


def test_phase159_r1_6d_reference_marker_spacing_is_normalized():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6d_pi3_2_presentation()
    )
  )

  assert "[R1]より," not in rendered
  assert "[R1] より," in rendered


def test_phase159_r1_6d_structural_formulas_are_centered():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6d_pi3_2_presentation()
    )
  )

  assert (
    "\\[\n"
    r"\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1} \xrightarrow{E} "
    r"\pi_{2}^{2}."
    "\n\\]"
    in rendered
  )
  assert (
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は単射}. \qquad (1)"
    "\n\\]"
    in rendered
  )
  assert (
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は全射}. \qquad (2)"
    "\n\\]"
    in rendered
  )
