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


def _render_pi6_3_repair16() -> str:
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


def test_phase157_r20_repair16_eta_bridge_preserves_suspension_reason():
  rendered = _render_pi6_3_repair16()
  body = rendered.split(
    "---",
    1,
  )[1]

  assert r"$\eta_{6}=E\eta_{5}$ である." in body
  assert r"$\eta_{6}=\eta_{6}$ である." not in body


def test_phase157_r20_repair16_removes_reflexive_equalities():
  rendered = _render_pi6_3_repair16()
  body = rendered.split(
    "---",
    1,
  )[1]

  assert r"$\eta_{3}^{3} = \eta_{3}^{3}" not in body
  assert r"$\eta_{5} = \eta_{5}" not in body


def test_phase157_r20_repair16_kernel_reason_follows_surjectivity_and_exactness():
  rendered = _render_pi6_3_repair16()
  body = rendered.split(
    "---",
    1,
  )[1]

  surjective = (
    r"$H: \pi_{7}^{3} \to "
    r"\pi_{7}^{5}$ は全射である."
  )
  exactness = (
    r"$\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}$ は完全である."
  )
  kernel = (
    "完全性より, "
    r"$\ker \Delta=\operatorname{Im}H="
    r"\pi_{7}^{5}$ である."
  )
  delta_zero = (
    r"$\Delta: \pi_{7}^{5} \to "
    r"\pi_{5}^{2}$ は零写像である."
  )

  assert surjective in body
  assert exactness in body
  assert kernel in body
  assert delta_zero in body

  assert body.index(
    surjective
  ) < body.index(
    exactness
  )
  assert body.index(
    exactness
  ) < body.index(
    kernel
  )
  assert body.index(
    kernel
  ) < body.index(
    delta_zero
  )
