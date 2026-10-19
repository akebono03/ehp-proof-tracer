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


def test_phase143_51a_r_pi8_5_suppresses_provenance_only_fallbacks():
  rendered = _render_multi_argument(
    5,
    3,
  )

  for internal_name in (
    "Toda Lemma 5.4 integration",
    "Toda (5.6) nu_4 decomposition isomorphism semantics",
    (
      "Toda Proposition 5.6 "
      "pi_8^5 quotient by E^2 pi_6^3"
    ),
  ):
    assert internal_name not in rendered

  assert (
    r"$\pi_{8}^{5}/E^{2}\left(\pi_{6}^{3}\right)"
    r" \cong \mathbb{Z}/2$"
    in rendered
  )


def test_phase143_51a_r_pi15_8_suppresses_provenance_only_fallbacks():
  rendered = _render_multi_argument(
    8,
    7,
  )

  for internal_name in (
    "Toda Proposition 5.15 sigma_8 "
    "Proposition 4.4 specialization premises",
    "Toda Lemma 5.14 sigma-prime branch",
    "Toda (5.14) second short exact sequence",
    (
      "Toda Proposition 5.15 "
      "sigma_8 transported decomposition"
    ),
  ):
    assert internal_name not in rendered

  assert (
    r"$0\longrightarrow \pi_{13}^{6}"
    r"\xrightarrow{E} \pi_{14}^{7}"
    r"\xrightarrow{H} \pi_{14}^{13}"
    r"\longrightarrow 0$"
    in rendered
  )
  assert (
    r"$\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus \mathbb{Z}\{\sigma_{8}\}$"
    in rendered
  )


def test_phase143_51a_r_pi16_9_suppresses_provenance_only_fallbacks():
  rendered = _render_multi_argument(
    9,
    7,
  )

  for internal_name in (
    "Toda Lemma 5.14 sigma_8 branch",
    "Toda Theorem 3.6 Lemma 5.14 "
    "sigma double-prime bridge",
    "Toda Lemma 5.14 sigma-prime branch",
    "Toda Proposition 5.15 pi_12^5 Hopf isomorphism",
    "Toda Lemma 5.13 sigma triple-prime definition",
    "Toda Lemma 5.4 integration",
    "Toda Proposition 5.11 finite-dimensional integration",
    "Toda Proposition 5.8 finite-dimensional integration",
    "Toda Lemma 5.14 sigma double-prime branch",
    "Toda (5.14) second short exact sequence",
    "Toda (4.8) pi_16^9 order sixteen and E4 injective",
  ):
    assert internal_name not in rendered

  assert (
    r"$0\longrightarrow \pi_{13}^{6}"
    r"\xrightarrow{E} \pi_{14}^{7}"
    r"\xrightarrow{H} \pi_{14}^{13}"
    r"\longrightarrow 0$"
    in rendered
  )
  assert (
    r"$|\pi_{16}^{9}| = 16$"
    in rendered
  )
  assert (
    r"$E^{4}: \pi_{12}^{5} \to \pi_{16}^{9}$ は単射である."
    in rendered
  )


def test_phase143_51a_r_preserves_four_final_group_conclusions():
  expected = (
    (
      3,
      3,
      r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}",
    ),
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
