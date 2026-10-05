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


def test_phase134_9_pi8_5_uses_structured_narrative(
  capsys,
):
  rendered = _render_pi8_5(
    capsys
  )

  assert "## 証明対象" in rendered
  assert "## 使用する結果" in rendered
  assert "## 証明" in rendered

  assert (
    r"\pi_{8}^{5} = "
    r"\mathbb{Z}/8\{\nu_{5}\}"
    in rendered
  )


def test_phase134_9_pi8_5_uses_order_block_lead(
  capsys,
):
  rendered = _render_pi8_5(
    capsys
  )

  assert (
    "まず, $\\nu_{5}$ の位数を求める."
    in rendered
  )

  assert (
    "最後に, これらの結果から "
    "$\\pi_{8}^{5}$ の群構造を決定する."
    in rendered
  )


def test_phase134_9_pi8_5_keeps_phase133_labels(
  capsys,
):
  rendered = _render_pi8_5(
    capsys
  )

  assert "Toda (5.6) の ν₄ 分解" in rendered
  assert "E²: π₆³ → π₈⁵ の単射性" in rendered
  assert (
    "π₈⁵ / E²π₆³ が位数 2 であること"
    in rendered
  )


def test_phase134_9_pi8_5_does_not_change_other_group_dispatch(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "5",
      "7",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "## 証明対象" not in captured.out
