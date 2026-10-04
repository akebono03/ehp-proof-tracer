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


def _body_pi6_3_repair33() -> str:
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
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  return rendered.split(
    "\n## 証明\n",
    1,
  )[1]


def test_phase157_r20_repair33_eta_bridge_precedes_visible_prop22_support():
  body = _body_pi6_3_repair33()

  eta6_definition = (
    r"$\eta_{6}=E\eta_{5}$ である."
  )
  prop22 = (
    "[R5]より, "
    r"$H(\alpha\circ E\beta) = "
    r"H(\alpha)\circ E\beta$."
  )
  hopf_value = (
    r"$H\left(\nu'\eta_{6}\right) = "
    r"\eta_{5}^{2}\tag{8}$."
  )

  assert eta6_definition in body
  assert prop22 in body
  assert hopf_value in body

  assert body.index(
    eta6_definition
  ) < body.index(
    prop22
  )
  assert body.index(
    prop22
  ) < body.index(
    hopf_value
  )


def test_phase157_r20_repair33_full_exactness_still_precedes_eta_bridge():
  body = _body_pi6_3_repair33()

  full_exactness = (
    r"$\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}$ は完全である."
  )
  eta6_definition = (
    r"$\eta_{6}=E\eta_{5}$ である."
  )

  assert full_exactness in body
  assert eta6_definition in body
  assert body.index(
    full_exactness
  ) < body.index(
    eta6_definition
  )
