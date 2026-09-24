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


def test_phase136_2_checks_two_eta3_before_toda_bracket(
  capsys,
):
  rendered = _render_pi6_3_narrative(capsys)

  zero_formula = r"2\eta_{3}=0.\tag{1}"
  bracket_formula = (
    r"\nu' \in "
    r"\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}."
    r"\tag{2}"
  )

  assert zero_formula in rendered
  assert bracket_formula in rendered
  assert rendered.index(zero_formula) < rendered.index(bracket_formula)


def test_phase136_2_ehp_sequence_intro_states_its_purpose(
  capsys,
):
  rendered = _render_pi6_3_narrative(capsys)

  intro = (
    "$\\nu'$ の位数を決定するために, "
    "次の EHP 完全列を考える."
  )
  exact_sequence = (
    r"\pi_{7}^{3}"
    r"\xrightarrow{H}"
    r"\pi_{7}^{5}"
    r"\xrightarrow{\Delta}"
    r"\pi_{5}^{2}"
    r"\xrightarrow{E}"
    r"\pi_{6}^{3}"
    r"\xrightarrow{H}"
    r"\pi_{6}^{5}"
    r"\quad\text{は完全である.}"
    r"\tag{8}"
  )

  assert intro in rendered
  assert exact_sequence in rendered
  assert rendered.index(intro) < rendered.index(exact_sequence)
  assert "次に, $\\nu'$ の位数を決定するために" not in rendered
  assert "ここで EHP 完全列は," not in rendered
  assert "つなげて" not in rendered


def test_phase136_2_uses_short_exact_sequence_around_pi6_3(
  capsys,
):
  rendered = _render_pi6_3_narrative(capsys)

  assert (
    r"0\longrightarrow\pi_{5}^{2}"
    r"\xrightarrow{E}\pi_{6}^{3}"
    r"\xrightarrow{H}\pi_{6}^{5}"
    r"\longrightarrow 0."
    r"\tag{19}"
    in rendered
  )


def test_phase136_2_final_formula_has_no_period_before_closing_sentence(
  capsys,
):
  rendered = _render_pi6_3_narrative(capsys)

  assert (
    r"\pi_{6}^{3}="
    r"\mathbb{Z}/4\{\nu'\}"
    r"\tag{20}"
    in rendered
  )
  assert (
    r"\mathbb{Z}/4\{\nu'\}.\tag{20}"
    not in rendered
  )
