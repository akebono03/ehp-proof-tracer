import main as cli_main


def _render_pi6_3_narrative(
  capsys,
) -> str:
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


def test_phase136_1_pi6_3_reference_has_eta_range(
  capsys,
):
  rendered = _render_pi6_3_narrative(capsys)

  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    r"\qquad (n \ge 3)."
    in rendered
  )


def test_phase136_1_pi6_3_uses_eta_power_notation(
  capsys,
):
  rendered = _render_pi6_3_narrative(capsys)

  assert r"\mathbb{Z}/2\{\eta_{3}^{2}\}" in rendered
  assert r"\mathbb{Z}/2\{\eta_{2}^{3}\}" in rendered
  assert r"\eta_{3}^{3}" in rendered
  assert r"\eta_{3}\eta_{4}\eta_{5}" not in rendered


def test_phase136_1_pi6_3_order_facts_use_right_hand_tags(
  capsys,
):
  rendered = _render_pi6_3_narrative(capsys)

  assert (
    r"\eta_{3}^{3}\text{ の位数は }2"
    r"\text{ である.}\tag{15}"
    in rendered
  )
  assert (
    r"\nu'\text{ の位数は }4"
    r"\text{ である.}\tag{16}"
    in rendered
  )


def test_phase136_1_pi6_3_map_properties_are_numbered_sentences(
  capsys,
):
  rendered = _render_pi6_3_narrative(capsys)

  assert (
    r"\Delta:\pi_{7}^{5}\to\pi_{5}^{2}"
    r"\quad\text{は零写像である.}\tag{13}"
    in rendered
  )
  assert (
    r"E:\pi_{5}^{2}\to\pi_{6}^{3}"
    r"\quad\text{は単射である.}\tag{14}"
    in rendered
  )
  assert (
    r"H:\pi_{6}^{3}\to\pi_{6}^{5}"
    r"\quad\text{は全射である.}\tag{18}"
    in rendered
  )


def test_phase136_1_pi6_3_leaf_facts_show_reasons(
  capsys,
):
  rendered = _render_pi6_3_narrative(capsys)

  assert "[R2] の $n=3$ の場合より," in rendered
  assert "[R2] の $n=5$ の場合より," in rendered
  assert "[R3] の $n=3$ の場合より," in rendered
  assert "[R3] の $n=5$ の場合より," in rendered


def test_phase136_1_pi6_3_formula_only_facts_end_with_period(
  capsys,
):
  rendered = _render_pi6_3_narrative(capsys)

  assert r"\nu'\in\pi_{6}^{3}.\tag{3}" in rendered
  assert r"H(\nu')=\eta_{5}.\tag{4}" in rendered
  assert (
    r"2\nu'=\eta_{3}\circ E\eta_{3}\circ\eta_{5}"
    r"=\eta_{3}^{3}.\tag{5}"
    in rendered
  )
  assert (
    r"\pi_{6}^{5}=\mathbb{Z}/2\{\eta_{5}\}."
    r"\tag{17}"
    in rendered
  )
