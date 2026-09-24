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


def test_phase136_2_promotes_prop53_and_lemma52_to_references(
  capsys,
):
  rendered = _render_pi6_3_narrative(
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
    "[R3] Toda Proposition 5.3"
    in reference_section
  )
  assert (
    "[R4] Toda Lemma 5.2"
    in reference_section
  )


def test_phase136_2_explains_twice_nu_prime_source(
  capsys,
):
  rendered = _render_pi6_3_narrative(
    capsys
  )

  reason = (
    "[R4] の倍元公式と η-family の "
    "suspension relation より,"
  )
  formula = (
    r"2\nu' = \eta_{3}^{3}.\tag{7}"
  )

  assert reason in rendered
  assert formula in rendered
  assert (
    rendered.index(reason)
    < rendered.index(formula)
  )


def test_phase136_2_explains_two_eta3_as_lemma52_premise(
  capsys,
):
  rendered = _render_pi6_3_narrative(
    capsys
  )

  zero_formula = (
    r"2\eta_{3} = 0.\tag{10}"
  )
  premise_sentence = (
    "この関係は [R4] を ν′ に特殊化して "
    "membership, 倍元, Hopf 像を得るための "
    "premise である."
  )

  assert zero_formula in rendered
  assert premise_sentence in rendered
  assert (
    rendered.index(zero_formula)
    < rendered.index(premise_sentence)
  )


def test_phase136_2_orders_target_group_before_hopf_surjectivity(
  capsys,
):
  rendered = _render_pi6_3_narrative(
    capsys
  )

  hopf_image = (
    r"H\left(\nu'\right) = "
    r"\eta_{5}.\tag{13}"
  )
  target_group = (
    r"\pi_{6}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}\}.\tag{14}"
  )
  surjectivity = (
    r"H: \pi_{6}^{3} \to \pi_{6}^{5}"
    r"\quad\text{は全射である.}"
    r"\tag{15}"
  )

  assert hopf_image in rendered
  assert target_group in rendered
  assert surjectivity in rendered
  assert (
    rendered.index(hopf_image)
    < rendered.index(target_group)
    < rendered.index(surjectivity)
  )


def test_phase136_2_uses_above_for_final_conclusion(
  capsys,
):
  rendered = _render_pi6_3_narrative(
    capsys
  )

  final_target = (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}\tag{16}"
  )

  assert "以上により," in rendered
  assert "したがって," not in rendered
  assert final_target in rendered
  assert (
    rendered.index(
      "以上により,"
    )
    < rendered.index(
      final_target
    )
  )
