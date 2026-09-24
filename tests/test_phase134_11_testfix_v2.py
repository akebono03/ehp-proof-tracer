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


def test_phase134_11_testfix_has_no_duplicate_dependency_leads(
  capsys,
):
  rendered = _render_pi8_5(
    capsys
  )

  assert rendered.count(
    "[R1], (1) より,"
  ) == 1

  assert rendered.count(
    "(3), (4) より,"
  ) == 1

  assert rendered.count(
    "(2), (5), (1) より,"
  ) == 1


def test_phase134_11_testfix_has_single_final_therefore(
  capsys,
):
  rendered = _render_pi8_5(
    capsys
  )

  assert rendered.count(
    "したがって,"
  ) == 1


def test_phase134_11_testfix_keeps_boundary_and_references(
  capsys,
):
  rendered = _render_pi8_5(
    capsys
  )

  assert (
    "**[R1] Toda (5.5) "
    "の ν-family 有限次元結果.**"
    in rendered
  )

  assert (
    "**[R2] Toda (5.6) の ν₄ 分解.**"
    in rendered
  )

  assert (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}\tag{3}"
    in rendered
  )
