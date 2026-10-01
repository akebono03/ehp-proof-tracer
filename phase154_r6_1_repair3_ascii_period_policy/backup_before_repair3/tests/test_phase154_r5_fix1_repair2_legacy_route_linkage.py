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


def test_phase154_r5_fix1_repair2_pi11_4_links_reference_after_marker_generation():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    r"[R2]より、$\nu_{4}$ の分解写像は同型写像である。"
    in rendered
  )
  assert "まず、[R2]を用いる。" not in rendered
  assert (
    r"このことから、$\nu_{4}$ の分解写像は同型写像である。"
    not in rendered
  )


def test_phase154_r5_fix1_repair2_reference_filtering_renumbers_linked_marker():
  rendered = _render_group(
    4,
    7,
  )

  assert "**[R1] Proposition 5.8.**" in rendered
  assert "**[R2] Proposition 4.4.**" in rendered
  assert "**[R3]" not in rendered
  assert "[R3]より、" not in rendered


def test_phase154_r5_fix1_repair2_keeps_root_only_reference_neutral():
  rendered = _render_group(
    4,
    7,
  )

  assert "[R1]を用いる。" in rendered
  assert r"[R1]より、$\pi_{11}^{4} = 0" not in rendered


def test_phase154_r5_fix1_repair2_keeps_consumer_once_and_final_conclusion():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    rendered.count(
      r"$\nu_{4}$ の分解写像は同型写像である。"
    )
    == 1
  )
  assert r"\pi_{11}^{4} = 0" in rendered
