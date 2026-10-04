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


def _body_pi6_3_repair45() -> str:
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


def test_phase157_r20_repair45_prop22_specialization_precedes_equation57_value():
  body = _body_pi6_3_repair45()

  prop22_specialization = (
    r"$H\left(\nu'\eta_{6}\right) = "
    r"H\left(\nu'\right)\eta_{6}\tag{7}$."
  )
  equation57_value = (
    r"$H\left(\nu'\eta_{6}\right) = "
    r"\eta_{5}^{2}\tag{8}$."
  )

  assert prop22_specialization in body
  assert equation57_value in body
  assert body.index(
    prop22_specialization
  ) < body.index(
    equation57_value
  )


def test_phase157_r20_repair45_prop22_specialization_stays_after_fixed_reference():
  body = _body_pi6_3_repair45()

  fixed_reference = (
    "[R5]より, "
    r"$H(\alpha\circ E\beta) = "
    r"H(\alpha)\circ E\beta$."
  )
  prop22_specialization = (
    r"$H\left(\nu'\eta_{6}\right) = "
    r"H\left(\nu'\right)\eta_{6}\tag{7}$."
  )

  assert body.index(
    fixed_reference
  ) < body.index(
    prop22_specialization
  )


def test_phase157_r20_repair45_delta_zero_unique_step_is_rendered_once():
  body = _body_pi6_3_repair45()

  delta_zero = (
    r"\Delta: \pi_{7}^{5} \to "
    r"\pi_{5}^{2}$ は零写像である."
  )

  assert body.count(
    delta_zero
  ) == 1
  assert (
    "以上より, "
    + "$"
    + delta_zero
    not in body
  )


def test_phase157_r20_repair45_delta_zero_remains_before_injectivity():
  body = _body_pi6_3_repair45()

  delta_zero = (
    r"$\Delta: \pi_{7}^{5} \to "
    r"\pi_{5}^{2}$ は零写像である."
  )
  injectivity = (
    r"$E: \pi_{5}^{2} \to "
    r"\pi_{6}^{3}$ は単射である."
  )

  assert body.index(
    delta_zero
  ) < body.index(
    injectivity
  )


def test_phase157_r20_repair45_short_exact_order_remains_correct():
  body = _body_pi6_3_repair45()

  surjectivity = (
    r"$H: \pi_{6}^{3} \to "
    r"\pi_{6}^{5}$ は全射である."
  )
  reason = (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
  )
  short_exact = (
    r"$0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0$."
  )

  assert body.index(
    surjectivity
  ) < body.index(
    reason
  )
  assert body.index(
    reason
  ) < body.index(
    short_exact
  )
