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


def test_phase159_r1_6a_foundational_reference_is_superseded_by_toda_51():
  report = build_standard_toda_report(n=2, k=1)
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(replay)
  rendered = render_toda_group_proof_narrative_markdown(presentation)

  assert "[F1]" not in rendered
  assert "[F2]" not in rendered
  assert "[F3]" not in rendered
  assert "**[R1] (5.1).**" in rendered
