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


def _phase153_r2_public_pi10_6_narrative() -> str:
  report = build_standard_toda_report(
    n=6,
    k=4,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def test_phase153_r2_public_pi10_6_keeps_reference_and_shows_toda45_fact():
  rendered = (
    _phase153_r2_public_pi10_6_narrative()
  )

  assert "**[R2] (4.5).**" in rendered
  assert "[R2] により、" in rendered
  assert "は同型写像である." in rendered
  assert (
    "Toda 4.5 stable-range iterated suspension isomorphism"
    not in rendered
  )
  assert "[R2]を用いる。" not in rendered


def test_phase153_r2_public_pi10_6_keeps_provenance_only_reference_compact():
  rendered = (
    _phase153_r2_public_pi10_6_narrative()
  )

  assert "**[R1] Proposition 5.8.**" in rendered
  assert "Toda Proposition 5.8を用いる。" in rendered
  assert (
    "Toda Proposition 5.8 finite-dimensional integration"
    not in rendered
  )
