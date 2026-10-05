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
  build_complete_toda_group_result_proof_replay,
)


def _render_group(n: int, k: int) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_complete_toda_group_result_proof_replay(
    group_result
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase150_rc4_7a_pi10_4_numbers_normalized_references(
):
  rendered = _render_group(
    4,
    6,
  )

  assert "## 使用する結果" in rendered
  assert "[R1]" in rendered
  assert r"\pi_{10}^{4}" in rendered
  assert r"\mathbb{Z}/8" in rendered


def test_phase150_rc4_7a_pi12_5_numbers_normalized_references(
):
  rendered = _render_group(
    5,
    7,
  )

  assert "## 使用する結果" in rendered
  assert "[R1]" in rendered
  assert r"\pi_{12}^{5}" in rendered
  assert r"\mathbb{Z}/2" in rendered


def test_phase150_rc4_7a_pi16_9_numbers_normalized_references(
):
  rendered = _render_group(9, 7)

  assert "## 使用する結果" in rendered
  assert "**[R1] " in rendered
  assert "[R1]" in rendered


def test_phase150_rc4_7a_pi15_8_uses_generic_order_contract(
):
  rendered = _render_group(
    8,
    7,
  )

  transported = (
    r"$\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus \mathbb{Z}\{\sigma_{8}\}$"
  )
  final = (
    r"$\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}$"
  )

  assert "Proposition 4.4" in rendered
  assert transported in rendered
  assert final in rendered
  assert rendered.index(
    transported
  ) < rendered.index(
    final
  )

def test_phase150_rc4_7a_depth1_keeps_legacy_reference_free_fallback(
):
  report = build_standard_toda_report(
    n=8,
    k=7,
  )
  group_result = report.candidates[0].source_candidate.group_result

  from toda_group_result_proof_replay import (
    build_toda_group_result_proof_replay,
  )

  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=1,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert "## 使用する結果" not in rendered
  assert "[R1]" not in rendered
