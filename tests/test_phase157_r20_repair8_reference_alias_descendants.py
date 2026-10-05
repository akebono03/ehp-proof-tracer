from pathlib import Path

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


def _render_pi6_3_r20_repair8() -> str:
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


def test_phase157_r20_repair8_equivalent_step_usage_keeps_required_references():
  rendered = _render_pi6_3_r20_repair8()

  for locator in (
    "Proposition 5.6",
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.1",
    "Proposition 2.2",
  ):
    assert locator in rendered


def test_phase157_r20_repair8_keeps_target_specific_reference_logic_absent():
  reference_source = Path(
    "toda_group_proof_narrative_references.py"
  ).read_text(
    encoding="utf-8"
  )
  renderer_source = Path(
    "toda_group_proof_narrative_contribution_renderer.py"
  ).read_text(
    encoding="utf-8"
  )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
    "filter_phase157_r3_pi6_3_reference_entries",
    "_phase157_r3_is_pi6_3_root",
    "restore_phase157_r3_pi6_3_required_reference_entries_after_body_usage",
  )

  for token in forbidden:
    assert token not in reference_source
    assert token not in renderer_source
