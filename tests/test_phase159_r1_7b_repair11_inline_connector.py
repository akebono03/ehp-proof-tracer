from toda_group_proof_narrative_renderer import (
  _phase159_r1_7b_map_property_signature,
)


def test_phase159_r1_7b_repair11_inline_connector_property_signature():
  line = (
    r"$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$"
    " は全射."
  )

  assert (
    _phase159_r1_7b_map_property_signature(
      line
    )
    == (
      r"\Delta",
      r"\pi_{10}^{5}",
      r"\pi_{8}^{2}",
    )
  )
