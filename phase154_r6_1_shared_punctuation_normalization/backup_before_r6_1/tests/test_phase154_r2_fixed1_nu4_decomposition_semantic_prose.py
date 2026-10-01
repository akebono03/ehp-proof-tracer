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


def test_phase154_r2_fixed1_pi10_4_replaces_raw_nu4_rule_name_with_semantic_prose():
  rendered = _render_group(
    4,
    6,
  )

  assert (
    "Toda (5.6) nu_4 decomposition integration"
    not in rendered
  )
  assert (
    r"$\nu_{4}$ の分解を用いる."
    in rendered
  )
  assert (
    r"\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}"
    in rendered
  )


def test_phase154_r2_fixed1_pi11_4_keeps_previous_r2_semantic_repairs():
  rendered = _render_group(
    4,
    7,
  )

  assert r"\text{ is injective}" not in rendered
  assert r"\text{ is exact}" not in rendered
  assert "は単射である." in rendered
  assert "は完全である." in rendered
  assert r"\pi_{11}^{4} = 0" in rendered
