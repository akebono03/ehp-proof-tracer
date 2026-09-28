from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _render_multi_argument(
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


def test_phase143_50_pi6_3_renders_map_properties_in_japanese():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である."
    in rendered
  )
  assert (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である."
    in rendered
  )
  assert r"\text{ is injective}" not in rendered
  assert r"\text{ is surjective}" not in rendered


def test_phase143_50_pi8_5_renders_exactness_and_definition_in_japanese():
  rendered = _render_multi_argument(
    5,
    3,
  )

  assert (
    r"$\nu_{5}$ を \(\nu\)-family の元として定める."
    in rendered
  )
  assert (
    r"$\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}$ は完全である."
    in rendered
  )
  assert (
    r"$\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}$ は完全である."
    in rendered
  )
  assert r"\text{ is exact}" not in rendered
  assert r"\text{ is the defined }" not in rendered


def test_phase143_50_pi16_9_renders_exactness_in_japanese():
  rendered = _render_multi_argument(
    9,
    7,
  )

  assert (
    r"$\pi_{12}^{5} \xrightarrow{H} "
    r"\pi_{12}^{9} \xrightarrow{\Delta} "
    r"\pi_{10}^{4}$ は完全である."
    in rendered
  )
  assert r"\text{ is exact}" not in rendered
  assert (
    r"\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}"
    in rendered
  )


def test_phase143_50_pi15_8_group_conclusion_is_preserved():
  rendered = _render_multi_argument(
    8,
    7,
  )

  assert (
    r"\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}"
    in rendered
  )


def test_phase143_50_structured_prose_remains_after_aggregate_rendering():
  rendered = _render_multi_argument(
    5,
    3,
  )

  assert (
    r"$E^{2}: \pi_{6}^{3} \to \pi_{8}^{5}$ は単射である."
    in rendered
  )
  assert (
    r"$\pi_{8}^{5}/E^{2}\left(\pi_{6}^{3}\right)"
    r" \cong \mathbb{Z}/2$"
    in rendered
  )
