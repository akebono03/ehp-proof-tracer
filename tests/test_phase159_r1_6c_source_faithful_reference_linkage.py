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


def _phase159_r1_6c_pi3_2_presentation():
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


def test_phase159_r1_6c_toda_51_reference_is_source_faithful():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6c_pi3_2_presentation()
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

  assert "**[R1] (5.1).**" in reference
  assert (
    r"$\pi_{i}^{1} = 0\ (i > 1)$."
    in reference
  )
  assert (
    r"$\pi_{n}^{n} = "
    r"\mathbb{Z}\{\iota_{n}\}$."
    in reference
  )

  assert (
    r"$\pi_{i}^{n} = 0\ (i < n)$."
    not in reference
  )
  assert r"\langle" not in reference
  assert r"\rangle" not in reference
  assert r"\pi_{2}^{1} = 0" not in reference
  assert r"\pi_{3}^{3}" not in reference
  assert (
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$"
    not in reference
  )

def test_phase159_r1_6c_exact_sequence_intro_does_not_repeat_exactness():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6c_pi3_2_presentation()
    )
  )

  assert (
    "$\\pi_{3}^{2}$ の群構造を決定するために, "
    "次の完全列を考える."
    in rendered
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
  assert "は完全である." not in rendered

def test_phase159_r1_6c_proof_body_links_reference_and_exactness():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6c_pi3_2_presentation()
    )
  )

  assert (
    r"[R1] より, $\pi_{2}^{1} = 0$."
    in rendered
  )
  assert (
    "完全性より,\n\n"
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は単射}. \qquad (1)"
    "\n\\]"
    in rendered
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
  assert (
    r"したがって, $E: \pi_{1}^{1} "
    r"\to \pi_{2}^{2}$ は単射."
    in rendered
  )
  assert (
    r"完全性より, $\Delta: \pi_{3}^{3} "
    r"\to \pi_{1}^{1}$ は零写像."
    in rendered
  )
  assert (
    r"[R1] より, $\pi_{3}^{3} = "
    r"\mathbb{Z}\{\iota_{3}\}$."
    in rendered
  )
  assert (
    "完全性より,\n\n"
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は全射}. \qquad (2)"
    "\n\\]"
    in rendered
  )

def test_phase159_r1_6c_statement_numbers_are_outside_math():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase159_r1_6c_pi3_2_presentation()
    )
  )

  assert r"\tag{1}" not in rendered
  assert r"\tag{2}" not in rendered

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
