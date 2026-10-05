def test_phase157_r20_repair53_r3_public_pi15_8_restores_prop44_reference():
  (
    raw,
    presentation,
    prop44_step,
  ) = _repair53_r3_data()

  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )

  assert "Proposition 4.4.**" in rendered
  assert "Proposition 5.15" in rendered
  assert (
    r"\pi_{14}^{7} = "
    r"\mathbb{Z}/8\{\sigma'\}"
    in rendered
  )
  assert (
    r"\left(α, \beta\right) \mapsto "
    r"Eα + \sigma_{8}\beta"
    in rendered
  )
