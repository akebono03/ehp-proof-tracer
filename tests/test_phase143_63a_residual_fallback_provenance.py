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


def test_phase143_63a_pi6_3_exactness_fallback_is_japanese():
  rendered = _render(
    3,
    3,
  )

  assert r"\text{ is exact}" not in rendered
  assert (
    r"$\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}$ は完全である."
    in rendered
  )


def test_phase143_63a_pi16_9_provenance_only_sigma8_does_not_leak():
  rendered = _render(
    9,
    7,
  )

  assert (
    "Toda Lemma 5.14 sigma_8 branch"
    not in rendered
  )
  assert (
    "Toda Lemma 5.14 の σ₈ に関する結果"
    not in rendered
  )
  assert (
    "TodaLemma514Sigma8Statement"
    not in rendered
  )


def test_phase143_63a_pi8_5_direct_premise_placement_remains():
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


def test_phase143_63a_four_case_narratives_have_no_known_residual_leakage():
  for n, k in (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ):
    rendered = _render(
      n,
      k,
    )

    assert r"\text{ is exact}" not in rendered
    assert (
      "Toda Lemma 5.14 sigma_8 branch"
      not in rendered
    )
    assert (
      "TodaLemma514Sigma8Statement"
      not in rendered
    )
