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
  rendered = (
    _render_pi6_3_narrative(
      capsys
    )
  )

  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    r"\qquad (n \ge 3)."
    in rendered
  )


def test_phase136_1_pi6_3_uses_eta_power_notation(
  capsys,
):
  rendered = (
    _render_pi6_3_narrative(
      capsys
    )
  )

  assert (
    r"\mathbb{Z}/2\{\eta_{3}^{2}\}"
    in rendered
  )
  assert (
    r"\mathbb{Z}/2\{\eta_{2}^{3}\}"
    in rendered
  )
  assert (
    r"\eta_{3}^{3}"
    in rendered
  )

  assert (
    r"\eta_{3}\eta_{4}"
    not in rendered
  )
  assert (
    r"\eta_{3}\eta_{4}\eta_{5}"
    not in rendered
  )


def test_phase136_1_pi6_3_order_facts_use_right_hand_tags(
  capsys,
):
  rendered = (
    _render_pi6_3_narrative(
      capsys
    )
  )

  assert (
    r"\eta_{3}^{3}"
    r"\text{ の位数は }"
    r"2"
    r"\text{ である.}"
    r"\tag{6}"
    in rendered
  )

  assert (
    r"\nu'"
    r"\text{ の位数は }"
    r"4"
    r"\text{ である.}"
    r"\tag{8}"
    in rendered
  )

  assert "**(6)**" not in rendered
  assert "**(8)**" not in rendered


def test_phase136_1_pi6_3_map_properties_are_numbered_sentences(
  capsys,
):
  rendered = (
    _render_pi6_3_narrative(
      capsys
    )
  )

  assert (
    r"\Delta: \pi_{7}^{5} \to \pi_{5}^{2}"
    r"\quad\text{は零写像である.}"
    r"\tag{3}"
    in rendered
  )

  assert (
    r"E: \pi_{5}^{2} \to \pi_{6}^{3}"
    r"\quad\text{は単射である.}"
    r"\tag{5}"
    in rendered
  )

  assert (
    r"H: \pi_{6}^{3} \to \pi_{6}^{5}"
    r"\quad\text{は全射である.}"
    r"\tag{15}"
    in rendered
  )


def test_phase136_1_pi6_3_leaf_facts_show_reasons(
  capsys,
):
  rendered = (
    _render_pi6_3_narrative(
      capsys
    )
  )

  assert (
    "[R3] より,"
    in rendered
  )
  assert (
    "EHP 完全列より,"
    in rendered
  )
  assert (
    "[R4] の Toda bracket 特殊化より,"
    in rendered
  )
  assert (
    "[R2] より,"
    in rendered
  )


def test_phase136_1_pi6_3_formula_only_facts_end_with_period(
  capsys,
):
  rendered = (
    _render_pi6_3_narrative(
      capsys
    )
  )

  assert (
    r"2\nu' = \eta_{3}^{3}.\tag{7}"
    in rendered
  )
  assert (
    r"\nu' \in \pi_{6}^{3}.\tag{11}"
    in rendered
  )
  assert (
    r"H\left(\nu'\right) = \eta_{5}.\tag{13}"
    in rendered
  )
  assert (
    r"\pi_{6}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}\}.\tag{14}"
    in rendered
  )
