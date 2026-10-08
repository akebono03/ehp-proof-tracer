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


def _render_phase161_r4_r5_repair3_pi4_2() -> str:
  report = build_standard_toda_report(
    n=2,
    k=2,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase161_r4_r5_repair3_moves_prop51_marker_to_concrete_pi4_3():
  rendered = (
    _render_phase161_r4_r5_repair3_pi4_2()
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  prop51_number = next(
    number
    for number in range(
      1,
      5,
    )
    if (
      f"**[R{number}] Proposition 5.1.**"
      in reference
    )
  )
  marker = (
    "[R"
    + str(
      prop51_number
    )
    + "]"
  )

  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    in reference
  )
  assert (
    r"\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}"
    not in reference
  )

  body_paragraphs = body.split(
    "\n\n"
  )
  pi4_3_paragraph = next(
    paragraph
    for paragraph in body_paragraphs
    if (
      r"\pi_{4}^{3} = "
      r"\mathbb{Z}/2\{\eta_{3}\}"
      in paragraph
    )
  )

  assert marker in pi4_3_paragraph
  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    not in body
  )


def test_phase161_r4_r5_repair3_keeps_52_specialization_and_target():
  rendered = (
    _render_phase161_r4_r5_repair3_pi4_2()
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  assert "(5.2)" in reference
  assert (
    r"\eta_{2}\circ -: "
    r"\pi_{i}^{3} \to \pi_{i}^{2}"
    in reference
  )

  assert "$i=4$" in body
  assert (
    r"\pi_{4}^{3} \to \pi_{4}^{2}"
    in body
  )
  assert (
    r"\eta_{3} \mapsto "
    r"\eta_{2}\eta_{3}"
    in body
  )
  assert (
    r"\pi_{4}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}^{2}\}"
    in body
  )
  assert "□" in body
