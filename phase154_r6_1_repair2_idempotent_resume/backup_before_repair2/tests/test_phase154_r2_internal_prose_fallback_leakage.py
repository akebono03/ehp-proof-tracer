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


def test_phase154_r2_pi10_4_suppresses_raw_contribution_rule_name():
  rendered = _render_group(
    4,
    6,
  )

  assert (
    "Toda (5.6) nu_4 decomposition integration"
    not in rendered
  )
  assert (
    r"\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}"
    in rendered
  )


def test_phase154_r2_pi11_4_renders_injective_fact_in_japanese():
  rendered = _render_group(
    4,
    7,
  )

  assert r"\text{ is injective}" not in rendered
  assert "は単射である。"in rendered
  assert (
    r"\pi_{11}^{4} = 0"
    in rendered
  )


def test_phase154_r2_pi11_4_renders_exactness_fact_in_japanese():
  rendered = _render_group(
    4,
    7,
  )

  assert r"\text{ is exact}" not in rendered
  assert "は完全である。"in rendered
  assert (
    r"\pi_{11}^{4} = 0"
    in rendered
  )


def test_phase154_r2_representative_public_narratives_have_no_known_raw_fallbacks():
  forbidden = (
    "Toda (5.6) nu_4 decomposition integration",
    r"\text{ is injective}",
    r"\text{ is exact}",
  )

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

    for fragment in forbidden:
      assert fragment not in rendered
