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


def _render_group(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
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


def test_phase157_r20_repair53_r3c_pi15_8_keeps_prop44_after_body_usage_filter():
  rendered = _render_group(
    8,
    7,
  )

  assert "**[R1] Proposition 4.4.**" in rendered
  assert (
    r"$(α, \beta) \mapsto Eα + \sigma_{8}\beta: "
    r"\pi_{14}^{7} \oplus \pi_{15}^{15} "
    r"\to \pi_{15}^{8}$ は同型写像である."
    in rendered
  )


def test_phase157_r20_repair53_r3c_pi15_8_marker_points_to_filtered_prop44():
  rendered = _render_group(
    8,
    7,
  )

  assert (
    "[R1] より, これらの生成元はそれぞれ"
    in rendered
  )
  assert "**[R1] Proposition 5.15.**" not in rendered
  assert "**[R2] Proposition 4.4.**" not in rendered


def test_phase157_r20_repair53_r3c_pi15_8_does_not_leave_stale_reference_number():
  rendered = _render_group(
    8,
    7,
  )

  assert "[R2] より, これらの生成元はそれぞれ" not in rendered
  assert "**[R2]" not in rendered
