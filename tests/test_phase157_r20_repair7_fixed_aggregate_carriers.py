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


def _render_pi6_3_r20_repair7() -> str:
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


def test_phase157_r20_repair7_fixed_aggregate_carriers_reach_reference_selection():
  rendered = _render_pi6_3_r20_repair7()

  for locator in (
    "Proposition 5.6",
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.1",
    "Proposition 2.2",
  ):
    assert locator in rendered


def test_phase157_r20_repair7_aggregate_component_selection_stays_minimal():
  rendered = _render_pi6_3_r20_repair7()

  assert (
    r"$\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}^{2}\}$."
    in rendered
  )
  assert (
    r"$\pi_{6}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}\}$."
    in rendered
  )

  assert (
    r"$\pi_{4}^{2}"
    not in rendered.split(
      "**[R3] Proposition 5.3.**",
      1,
    )[1].split(
      "**[R4]",
      1,
    )[0]
  )


def test_phase157_r20_repair7_has_no_target_specific_reference_logic():
  source = Path(
    "toda_group_proof_narrative_references.py"
  ).read_text(
    encoding="utf-8"
  )

  forbidden = (
    "is_pi6_3",
    "filter_phase157_r3_pi6_3_reference_entries",
    "_phase157_r3_is_pi6_3_root",
    "restore_phase157_r3_pi6_3_required_reference_entries_after_body_usage",
  )

  for token in forbidden:
    assert token not in source
