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


def _render_pi12_5(
  depth: int = 3,
) -> str:
  report = build_standard_toda_report(
    n=5,
    k=7,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _reference_section(
  rendered: str,
) -> str:
  if "## 使用する結果" in rendered:
    start = rendered.index(
      "## 使用する結果"
    )
    proof = rendered.index(
      "## 証明",
      start,
    )
    return rendered[
      start:
      proof
    ]

  marker = "使用する結果を先にまとめる."
  start = rendered.index(
    marker
  )
  next_body = rendered.find(
    "\n\n次に,",
    start,
  )

  if next_body < 0:
    next_body = rendered.find(
      "\n\nまず,",
      start,
    )

  assert next_body >= 0

  return rendered[
    start:
    next_body
  ]


def test_phase157_r4_r3_repair1_pi12_5_restores_used_lemma513_fixed_reference():
  reference = _reference_section(
    _render_pi12_5()
  )

  assert "Lemma 5.13" in reference
  assert "\\sigma'''" in reference


def test_phase157_r4_r3_repair1_pi12_5_does_not_restore_prop511_internal_map_facts():
  reference = _reference_section(
    _render_pi12_5()
  )

  assert (
    r"H: \pi_{12}^{5} \to \pi_{12}^{9} は単射"
    not in reference
  )
  assert "は全射である." not in reference
  assert "is exact" not in reference
