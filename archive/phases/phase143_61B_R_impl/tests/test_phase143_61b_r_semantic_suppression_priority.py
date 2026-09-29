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


def test_phase143_61b_r_semantic_duplicate_suppression_precedes_relocation():
  rendered = _render(
    8,
    7,
  )

  assert (
    r"$\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus \mathbb{Z}\{\sigma_{8}\}$"
    not in rendered
  )


def test_phase143_61b_r_keeps_pi15_8_final_conclusion():
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


def test_phase143_61b_r_keeps_pi8_5_relocated_direct_premise():
  rendered = _render(
    5,
    3,
  )

  assert (
    r"$2\nu_{5} = E^{2}\nu'$"
    "\n\n"
    r"$\operatorname{ord}\left(E^{2}\nu'\right) = 4$"
    "\n\n"
    "以上より、"
    "\n\n"
    r"$\operatorname{ord}\left(\nu_{5}\right) = 8$"
    in rendered
  )


def test_phase143_61b_r_keeps_pi6_3_local_connector():
  rendered = _render(
    3,
    3,
  )

  assert "これらより、" in rendered
  assert (
    "以上より、\n\n"
    r"$\operatorname{ord}\left(\nu'\right) = 4$"
    in rendered
  )
