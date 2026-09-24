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


def test_phase134_7_has_three_deterministic_block_leads(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  first = (
    "まず, $\\nu'$ の位数を求める."
  )

  second = (
    "次に, $\\nu' \\in \\pi_{6}^{3}$ "
    "であることを確認する."
  )

  third = (
    "最後に, EHP 完全列を用いて "
    "$\\pi_{6}^{3}$ の群構造を決定する."
  )

  assert first in rendered
  assert second in rendered
  assert third in rendered

  assert (
    rendered.index(
      first
    )
    < rendered.index(
      second
    )
    < rendered.index(
      third
    )
  )


def test_phase134_7_boundary_facts_remain_numbered_facts(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert (
    r"\pi_{5}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\eta_{4}\}\tag{1}"
    in rendered
  )

  assert (
    r"2\nu' = "
    r"\eta_{3}\eta_{4}\eta_{5}\tag{7}"
    in rendered
  )

  assert (
    r"H\left(\nu'\right) = "
    r"\eta_{5}\tag{13}"
    in rendered
  )


def test_phase134_7_boundary_facts_are_not_references(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  reference_section = rendered[
    rendered.index(
      "## 使用する結果"
    ):
    rendered.index(
      "## 証明\n"
    )
  ]

  assert (
    r"\pi_{5}^{3}"
    not in reference_section
  )

  assert (
    r"2\nu'"
    not in reference_section
  )

  assert (
    r"H\left(\nu'\right)"
    not in reference_section
  )


def test_phase134_7_uses_therefore_for_final_conclusion(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert "したがって," in rendered
  assert "以上から," not in rendered

  final_target = (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}\tag{16}"
  )

  assert final_target in rendered

  assert (
    rendered.index(
      "したがって,"
    )
    < rendered.index(
      final_target
    )
  )


def test_phase134_7_keeps_reference_order(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert (
    rendered.index(
      "[R1]"
    )
    < rendered.index(
      "[R2]"
    )
  )

  assert "(1), [R1] より," in rendered
  assert "(13), [R2] より," in rendered


def test_phase134_7_keeps_ascii_punctuation(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert "、" not in rendered
  assert "。" not in rendered
