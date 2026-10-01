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


def test_phase154_r2_fix2_pi11_4_semantic_sentences_are_not_double_wrapped():
  rendered = _render_group(
    4,
    7,
  )

  assert "である.を用いる。" not in rendered
  assert (
    r"まず、$H: \pi_{10}^{3} \to \pi_{10}^{5}$ "
    r"は単射である."
    in rendered
  )
  assert (
    r"また、$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$ "
    r"は単射である."
    in rendered
  )
  assert (
    r"さらに、$\pi_{10}^{3} \xrightarrow{H} "
    r"\pi_{10}^{5} \xrightarrow{Δ} \pi_{8}^{2}$ "
    r"は完全である."
    in rendered
  )


def test_phase154_r2_fix2_pi11_4_does_not_expose_root_source_metadata():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    "Toda Proposition 5.15を用いる。"
    not in rendered
  )
  assert "# Group proof narrative" in rendered
  assert "## 使用する結果" in rendered
  assert "## 証明" in rendered


def test_phase154_r2_fix2_pi11_4_renders_nu4_decomposition_isomorphism_semantically():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    "Toda (5.6) の ν₄ 分解同型"
    not in rendered
  )
  assert (
    r"$\nu_{4}$ の分解写像は同型写像である。"
    in rendered
  )
  assert r"\pi_{11}^{4} = 0" in rendered


def test_phase154_r2_fix2_keeps_pi10_4_fixed1_result():
  rendered = _render_group(
    4,
    6,
  )

  assert (
    "Toda (5.6) nu_4 decomposition integration"
    not in rendered
  )
  assert (
    r"$\nu_{4}$ の分解を用いる。"
    in rendered
  )
  assert (
    r"\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}"
    in rendered
  )
