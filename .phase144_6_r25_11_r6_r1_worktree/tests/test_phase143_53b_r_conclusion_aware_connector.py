from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _render(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  return (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )


def test_phase143_53b_r_pi6_3_connector_precedes_order_conclusion():
  rendered = _render(
    3,
    3,
  )

  assert (
    "以上より、\n\n"
    r"$\operatorname{ord}\left(\nu'\right) = 4$"
    in rendered
  )
  assert (
    r"$\operatorname{ord}\left(\nu'\right) = 4$"
    "\n\n以上より、\n\n"
    r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$"
    not in rendered
  )


def test_phase143_53b_r_pi8_5_connector_precedes_order_conclusion():
  rendered = _render(
    5,
    3,
  )

  assert (
    "以上より、\n\n"
    r"$\operatorname{ord}\left(\nu_{5}\right) = 8$"
    in rendered
  )
  assert (
    r"$\operatorname{ord}\left(\nu_{5}\right) = 8$"
    "\n\n以上より、\n\n"
    r"$\operatorname{ord}\left(E^{2}\nu'\right) = 4$"
    not in rendered
  )


def test_phase143_53b_r_pi15_8_connector_still_precedes_target():
  rendered = _render(
    8,
    7,
  )

  assert (
    "以上より、\n\n"
    r"$\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}$"
    in rendered
  )


def test_phase143_53b_r_pi16_9_support_definition_stays_unconnected():
  rendered = _render(
    9,
    7,
  )

  assert (
    "以上より、\n\n"
    r"$\sigma_{9}$ を \(\sigma\)-family の元として定める."
    not in rendered
  )


def test_phase143_53b_r_pi16_9_connector_still_precedes_target():
  rendered = _render(
    9,
    7,
  )

  assert (
    "以上より、\n\n"
    r"$\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}$"
    in rendered
  )
