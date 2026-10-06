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


def _pi3_2_public_narrative() -> str:
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
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase159_r1_7c_r4_pi3_2_keeps_only_longer_exact_sequence():
  rendered = _pi3_2_public_narrative()
  paragraphs = tuple(
    paragraph.strip()
    for paragraph in rendered.split(
      "\n\n"
    )
  )

  longer = (
    r"$\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1} \xrightarrow{E} "
    r"\pi_{2}^{2}$."
  )
  shorter = (
    r"$\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1}$."
  )

  assert longer in paragraphs
  assert shorter not in paragraphs


def test_phase159_r1_7c_r4_pi3_2_keeps_injective_surjective_structure():
  rendered = _pi3_2_public_narrative()

  assert (
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    in rendered
  )
  assert "は単射" in rendered
  assert "は全射" in rendered
  assert "(1), (2) より" in rendered
  assert "は同型" in rendered


def test_phase159_r1_7c_r4_pi3_2_eta2_wording_is_unchanged():
  rendered = _pi3_2_public_narrative()

  assert (
    "この同型写像により"
    in rendered
  )
  assert (
    r"H(\eta_{2})=\iota_{3}"
    in rendered
    or r"H\left(\eta_{2}\right)=\iota_{3}"
    in rendered
    or r"H\left(\eta_{2}\right) = \iota_{3}"
    in rendered
  )
  assert (
    r"\eta_{2}"
    in rendered
  )
