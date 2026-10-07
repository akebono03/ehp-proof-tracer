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


def _render_pi6_3_repair26() -> str:
  report = build_standard_toda_report(
    n=3,
    k=3,
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


def test_phase157_r20_repair26_hides_both_rendered_reflexive_equalities():
  rendered = _render_pi6_3_repair26()
  body = rendered.split(
    "---",
    1,
  )[1]

  assert (
    r"$\eta_{3}^{3} = \eta_{3}^{3}"
    not in body
  )
  assert (
    r"$\eta_{5} = \eta_{5}"
    not in body
  )


def test_phase157_r20_repair26_keeps_required_nonreflexive_support():
  rendered = _render_pi6_3_repair26()
  body = rendered.split(
    "---",
    1,
  )[1]

  required = (
    r"$2\nu' = \eta_{3}^{3}",
    r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2",
    r"$H\left(\nu'\right) = \eta_{5}",
    r"$\eta_{6}=E\eta_{5}$.",
    r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}",
  )

  for text in required:
    assert text in body
