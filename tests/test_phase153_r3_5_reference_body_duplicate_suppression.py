from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  suppress_toda_group_proof_narrative_reference_body_duplicates,
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


def _phase153_r3_5_pi10_6_narrative() -> str:
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


def test_phase153_r3_5_suppresses_exact_standalone_statement_line():
  body = (
    "まず、群構造を確認する。\n\n"
    "$E: A \\xrightarrow{\\cong} B$\n\n"
    "したがって結論を得る。"
  )

  suppressed = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          "$E: A \\xrightarrow{\\cong} B$",
        ),
      },
    )
  )

  assert "$E: A \\xrightarrow{\\cong} B$" not in suppressed
  assert "まず、群構造を確認する。" in suppressed
  assert "したがって結論を得る。" in suppressed


def test_phase153_r3_5_compacts_reference_marker_sentence():
  statement = "$E: A \\xrightarrow{\\cong} B$"
  body = (
    "また、[R2] により、"
    + statement
    + "を得る。"
  )

  suppressed = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          statement,
        ),
      },
    )
  )

  assert suppressed == "また、[R2]を用いる。"


def test_phase153_r3_5_does_not_suppress_similar_but_nonidentical_statement():
  selected = "$E: A \\xrightarrow{\\cong} B$"
  different = "$E^2: A \\xrightarrow{\\cong} B$"
  body = (
    "また、[R2] により、"
    + different
    + "を得る。"
  )

  suppressed = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          selected,
        ),
      },
    )
  )

  assert suppressed == body


def test_phase153_r3_5_public_pi10_6_keeps_current_reference_baseline_without_obsolete_45():
  rendered = (
    _phase153_r3_5_pi10_6_narrative()
  )

  parts = rendered.split(
    "## 証明",
    1,
  )
  reference_section = parts[0]
  proof_body = (
    parts[1]
    if len(parts) == 2
    else rendered
  )

  assert "**[R1] Proposition 5.8.**" in reference_section
  assert "(4.5)" not in reference_section
  assert "$\pi_{10}^{6} = 0$" in proof_body

