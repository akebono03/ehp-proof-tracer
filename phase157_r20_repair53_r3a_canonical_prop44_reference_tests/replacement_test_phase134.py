def test_phase134_24_pi15_8_narrative_has_mathematical_structure(
):
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi15_8_presentation()
    )
  )

  assert "# Group proof narrative" in rendered
  assert "## 証明対象" in rendered
  assert "## 使用する結果" in rendered
  assert "## 証明" in rendered
  assert "Proposition 4.4.**" in rendered
  assert (
    r"\left(α, \beta\right) \mapsto "
    r"Eα + \sigma_{8}\beta"
    in rendered
  )
