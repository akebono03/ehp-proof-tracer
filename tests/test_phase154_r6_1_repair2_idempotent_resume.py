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


def test_phase154_r6_1_repair2_pi6_3_remaining_reason_periods_are_normalized():
  rendered = _render_group(
    3,
    3,
  )

  assert (
    r"$4\nu'=0$ かつ $2\nu'\neq0$ である。"
    in rendered
  )
  assert (
    r"$4\nu'=0$ かつ $2\nu'\neq0$ である."
    not in rendered
  )
  assert (
    r"中央の群の位数は $2\cdot2=4$ である。"
    in rendered
  )
  assert (
    r"中央の群の位数は $2\cdot2=4$ である."
    not in rendered
  )


def test_phase154_r6_1_repair2_pi11_4_current_public_punctuation_and_r5_linkage():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    r"まず、$H: \pi_{10}^{3} \to \pi_{10}^{5}$ "
    r"は単射である。"
    in rendered
  )
  assert (
    r"さらに、$\pi_{10}^{3} \xrightarrow{H} "
    r"\pi_{10}^{5} \xrightarrow{Δ} \pi_{8}^{2}$ "
    r"は完全である。"
    in rendered
  )
  assert (
    r"[R2]より、$\nu_{4}$ の分解写像は同型写像である。"
    in rendered
  )
