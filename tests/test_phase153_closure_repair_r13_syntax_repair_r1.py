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


def _render(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase153_r13_syntax_repair_pi8_5_renders():
  rendered = _render(
    5,
    3,
  )

  assert "## 証明" in rendered
  assert r"\pi_{8}^{5}" in rendered


def test_phase153_r13_syntax_repair_pi15_8_renders():
  rendered = _render(
    8,
    7,
  )

  assert "## 証明" in rendered
  assert r"\pi_{15}^{8}" in rendered
