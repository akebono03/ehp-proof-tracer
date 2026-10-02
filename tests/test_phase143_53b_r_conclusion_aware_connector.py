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
    "以上より, \n\n"
    r"$\operatorname{ord}\left(\nu'\right) = 4$"
    in rendered
  )
  assert (
    r"$\operatorname{ord}\left(\nu'\right) = 4$"
    "\n\n以上より, \n\n"
    r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$"
    not in rendered
  )


def test_phase143_53b_r_pi8_5_connector_precedes_order_conclusion():
  rendered = _render(
    5,
    3,
  )

  assert (
    "以上より, \n\n"
    r"$\operatorname{ord}\left(\nu_{5}\right) = 8$"
    in rendered
  )
  assert (
    r"$\operatorname{ord}\left(\nu_{5}\right) = 8$"
    "\n\n以上より, \n\n"
    r"$\operatorname{ord}\left(E^{2}\nu'\right) = 4$"
    not in rendered
  )


