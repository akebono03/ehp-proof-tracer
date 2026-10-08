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


def _render_phase161_r4_r5_repair9a_pi4_2() -> str:
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


def test_phase161_r4_r5_repair9a_final_public_relink_uses_prop51_on_pi4_3():
  rendered = (
    _render_phase161_r4_r5_repair9a_pi4_2()
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  assert "**[R1] (5.2).**" in reference
  assert "**[R2] Proposition 5.1.**" in reference

  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    in reference
  )
  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    not in body
  )

  pi4_3_paragraph = next(
    paragraph
    for paragraph in body.split(
      "\n\n"
    )
    if (
      r"\pi_{4}^{3} = "
      r"\mathbb{Z}/2\{\eta_{3}\}"
      in paragraph
    )
  )

  assert "[R2]" in pi4_3_paragraph
  assert (
    pi4_3_paragraph.count(
      "[R2]"
    )
    == 1
  )


def test_phase161_r4_r5_repair9a_final_public_relink_keeps_pi4_2_contract():
  rendered = (
    _render_phase161_r4_r5_repair9a_pi4_2()
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  assert "Proposition 4.4" not in reference
  assert "[R2]より, [R1]より" not in body

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
