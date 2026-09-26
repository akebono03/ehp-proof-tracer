from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_proof_block,
)
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


def test_phase143_51a_pi6_3_renders_structured_map_properties():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert (
    r"$\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である."
    in rendered
  )
  assert (
    "Toda Proposition 5.6 pi_7^5 Delta zero"
    not in rendered
  )
  assert (
    "Toda Proposition 5.3 n=3 suspension isomorphism"
    not in rendered
  )


def test_phase143_51a_pi8_5_renders_iterated_suspension_injective():
  rendered = _render_multi_argument(
    5,
    3,
  )

  assert (
    r"$E^{2}: \pi_{6}^{3} \to \pi_{8}^{5}$ は単射である."
    in rendered
  )
  assert (
    "Toda Proposition 5.6 E^2 pi_6^3 injective"
    not in rendered
  )


def test_phase143_51a_pi16_9_renders_sigma_family_definition():
  rendered = _render_multi_argument(
    9,
    7,
  )

  assert (
    r"$\sigma_{9}$ を \(\sigma\)-family の元として定める."
    in rendered
  )
  assert (
    "`TodaSigmaFamilyDefinitionStatement`"
    not in rendered
  )


def test_phase143_51a_argument_narrative_suppresses_reference_fallbacks():
  rendered = _render_multi_argument(
    5,
    3,
  )

  for internal_name in (
    "Toda Lemma 5.4 integration",
    "Toda 5.5 nu-family finite-dimensional integration",
    "Toda 5.3 nu-prime Lemma 5.2 bracket specialization",
    "Toda Proposition 5.1 finite-dimensional integration",
    "Toda 5.2 eta_2 composition isomorphism",
    "Toda (5.6) nu_4 decomposition integration",
  ):
    assert internal_name not in rendered


def test_phase143_51a_argument_narrative_suppresses_internal_decomposition_map():
  rendered = _render_multi_argument(
    8,
    7,
  )

  assert (
    "`TodaProp44DecompositionMap`"
    not in rendered
  )


def test_phase143_51a_keeps_unhandled_aggregate_fallback_for_phase143_51b():
  rendered = _render_multi_argument(
    5,
    3,
  )

  assert (
    "Toda Proposition 5.6 "
    "pi_8^5 quotient by E^2 pi_6^3"
    in rendered
  )


def test_phase143_51a_generic_block_keeps_provenance_by_default():
  (
    presentation,
    blocks,
    _sidecar,
    _arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  rendered = "\n".join(
    "\n".join(
      _render_generic_narrative_proof_block(
        presentation,
        blocks,
        block_index,
      )
    )
    for block_index in range(
      len(
        blocks
      )
    )
  )

  assert (
    "Toda Proposition 5.1 finite-dimensional integration"
    in rendered
  )
