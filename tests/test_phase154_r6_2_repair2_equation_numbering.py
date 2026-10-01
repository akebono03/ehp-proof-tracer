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


def test_phase154_r6_2_repair2_pi6_3_numbered_derivation_uses_ascii_comma():
  rendered = _render_group(
    3,
    3,
  )

  assert "(1) と (2) より, " in rendered
  assert "(1) と (2) より、" not in rendered


def test_phase154_r6_2_repair2_representatives_have_no_japanese_punctuation():
  for n, k in (
    (3, 3),
    (4, 6),
    (4, 7),
    (5, 7),
    (9, 7),
  ):
    rendered = _render_group(
      n,
      k,
    )

    assert "、" not in rendered
    assert "。" not in rendered
