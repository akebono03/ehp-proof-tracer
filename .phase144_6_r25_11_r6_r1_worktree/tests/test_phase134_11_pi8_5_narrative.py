import main as cli_main


def _render_pi8_5(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "5",
      "3",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""

  return captured.out


def test_phase134_11_pi8_5_has_two_references_in_use_order(
  capsys,
):
  rendered = _render_pi8_5(
    capsys
  )

  r1 = (
    "**[R1] Toda (5.5) "
    "の ν-family 有限次元結果.**"
  )

  r2 = (
    "**[R2] Toda (5.6) の ν₄ 分解.**"
  )

  assert r1 in rendered
  assert r2 in rendered
  assert rendered.index(
    r1
  ) < rendered.index(
    r2
  )


def test_phase134_11_pi8_5_definition_is_natural_japanese(
  capsys,
):
  rendered = _render_pi8_5(
    capsys
  )

  assert (
    "$\\nu_{5}$ を $\\nu$-family "
    "の定義により取る."
    in rendered
  )

  assert (
    r"\text{ is the defined }"
    not in rendered
  )


def test_phase134_11_pi8_5_stops_at_pi6_3_boundary(
  capsys,
):
  rendered = _render_pi8_5(
    capsys
  )

  assert (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}"
    in rendered
  )

  assert (
    r"\pi_{5}^{2} = "
    r"\mathbb{Z}/2"
    not in rendered
  )

  assert (
    r"\pi_{5}^{2} "
    r"\xrightarrow{E} "
    r"\pi_{6}^{3}"
    not in rendered
  )

  assert (
    r"\pi_{6}^{5} = "
    r"\mathbb{Z}/2"
    not in rendered
  )


def test_phase134_11_pi8_5_uses_hidden_toda55_as_reference(
  capsys,
):
  rendered = _render_pi8_5(
    capsys
  )

  assert (
    "[R1], (1) より,"
    in rendered
  )

  assert (
    r"2\nu_{5} = E^{2}\nu'"
    in rendered
  )


def test_phase134_11_pi8_5_uses_pi6_boundary_for_e2_order(
  capsys,
):
  rendered = _render_pi8_5(
    capsys
  )

  assert "既に," in rendered

  assert (
    "$E^{2}\\nu'$ の位数は $4$ である."
    in rendered
  )

  assert (
    "$\\nu_{5}$ の位数は $8$ である."
    in rendered
  )


def test_phase134_11_pi8_5_keeps_ascii_punctuation(
  capsys,
):
  rendered = _render_pi8_5(
    capsys
  )

  assert "、" not in rendered
  assert "。" not in rendered
