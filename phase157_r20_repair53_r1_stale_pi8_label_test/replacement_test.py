def test_phase134_9_pi8_5_keeps_phase133_labels(
  capsys,
):
  rendered = _render_pi8_5(
    capsys
  )

  assert (
    "Toda Proposition 5.6 のうち,"
    in rendered
  )
  assert "## 使用する結果" in rendered
  assert "## 証明" in rendered
  assert (
    r"\pi_{8}^{5} = "
    r"\mathbb{Z}/8\{\nu_{5}\}"
    in rendered
  )
