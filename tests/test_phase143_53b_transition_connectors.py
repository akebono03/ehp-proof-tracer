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


def test_phase143_53b_pi6_3_derivation_connects_order_and_target():
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
    "以上より、\n\n"
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in rendered
  )


def test_phase143_53b_pi6_3_support_definition_has_no_connector():
  rendered = _render(
    3,
    3,
  )

  assert (
    "以上より、\n\n"
    r"$\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$"
    not in rendered
  )


def test_phase143_53b_pi15_8_aggregate_derivation_connects_target():
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


def test_phase143_53b_pi16_9_definition_support_has_no_connector():
  rendered = _render(
    9,
    7,
  )

  assert (
    "以上より、\n\n"
    r"$\sigma_{9}$ を \(\sigma\)-family の元として定める."
    not in rendered
  )


def test_phase143_53b_pi16_9_derivation_connects_target():
  rendered = _render(
    9,
    7,
  )

  assert (
    "以上より、\n\n"
    r"$\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}$"
    in rendered
  )
