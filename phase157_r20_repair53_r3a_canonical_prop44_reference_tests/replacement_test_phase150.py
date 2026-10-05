def test_phase150_rc4_7a_pi15_8_special_renderer_is_unchanged(
):
  rendered = _render_group(8, 7)

  assert "Proposition 4.4.**" in rendered
  assert (
    r"\left(α, \beta\right) \mapsto "
    r"Eα + \sigma_{8}\beta"
    in rendered
  )
  assert "直和因子の順序を入れ替えると," in rendered
