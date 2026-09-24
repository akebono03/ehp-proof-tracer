import main as cli_main


def _render_pi6_3(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "3",
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


def test_phase134_5_separates_target_and_references(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert "## 証明対象" in rendered
  assert "## 使用する結果" in rendered
  assert "## 証明" in rendered
  assert "Toda (5.2) の η₂ 合成同型" in rendered
  assert "Toda Proposition 5.1 の有限次元結果" in rendered

  assert (
    "**[R1] Toda Proposition 5.6.**"
    not in rendered
  )


def test_phase134_5_reference_statements_are_visible(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert r"\eta_{2}\circ -" in rendered
  assert r"\pi_{n + 1}^{n}" in rendered
  assert r"\mathbb{Z}/2\{\eta_{n}\}" in rendered


def test_phase134_5_references_are_not_numbered_facts(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert "**(2)** Toda (5.2)" not in rendered
  assert "[R1]" in rendered
  assert "[R2]" in rendered


def test_phase134_5_order_relations_use_natural_sentences(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert "の位数は $2$ である." in rendered
  assert "の位数は $4$ である." in rendered
  assert r"\operatorname{ord}" not in rendered


def test_phase134_5_keeps_final_group_conclusion(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert "以上から," in rendered

  assert (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}"
    in rendered
  )

  assert "を得る." in rendered


def test_phase134_5_keeps_ascii_punctuation(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert "、" not in rendered
  assert "。" not in rendered
