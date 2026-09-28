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


def test_phase143_51b_pi8_5_renders_quotient_mathematically():
  rendered = _render_multi_argument(
    5,
    3,
  )

  assert (
    r"$\pi_{8}^{5}/E^{2}\left(\pi_{6}^{3}\right)"
    r" \cong \mathbb{Z}/2$"
    in rendered
  )
  assert (
    "Toda Proposition 5.6 "
    "pi_8^5 quotient by E^2 pi_6^3"
    not in rendered
  )


def test_phase143_51b_pi15_8_renders_short_exact_sequence():
  rendered = _render_multi_argument(
    8,
    7,
  )

  assert (
    "次の短完全列を得る."
    in rendered
  )
  assert (
    r"$0\longrightarrow \pi_{13}^{6}"
    r"\xrightarrow{E} \pi_{14}^{7}"
    r"\xrightarrow{H} \pi_{14}^{13}"
    r"\longrightarrow 0$"
    in rendered
  )
  assert (
    "Toda (5.14) second short exact sequence"
    not in rendered
  )


def test_phase143_51b_pi15_8_renders_transported_decomposition():
  rendered = _render_multi_argument(
    8,
    7,
  )

  assert (
    r"$\pi_{15}^{8} \cong "
    in rendered
  )
  assert (
    r"\mathbb{Z}/8\{E\sigma'\}"
    in rendered
  )
  assert (
    r"\mathbb{Z}\{\sigma_{8}\}"
    in rendered
  )
  assert (
    "Toda Proposition 5.15 "
    "sigma_8 transported decomposition"
    not in rendered
  )


def test_phase143_51b_pi16_9_renders_order_and_e4_injective():
  rendered = _render_multi_argument(
    9,
    7,
  )

  assert (
    r"$|\pi_{16}^{9}| = 16$"
    in rendered
  )
  assert (
    r"$E^{4}: \pi_{12}^{5} \to \pi_{16}^{9}$ は単射である."
    in rendered
  )
  assert (
    "Toda (4.8) pi_16^9 order sixteen and E4 injective"
    not in rendered
  )


def test_phase143_51b_keeps_final_group_conclusions():
  expected = (
    (
      5,
      3,
      r"\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}",
    ),
    (
      8,
      7,
      (
        r"\pi_{15}^{8} = "
        r"\mathbb{Z}\{\sigma_{8}\} "
        r"\oplus \mathbb{Z}/8\{E\sigma'\}"
      ),
    ),
    (
      9,
      7,
      r"\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}",
    ),
  )

  for n, k, conclusion in expected:
    rendered = _render_multi_argument(
      n,
      k,
    )

    assert conclusion in rendered
