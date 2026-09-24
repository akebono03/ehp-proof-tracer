import main as cli_main


def test_phase134_9_pi6_3_snapshot_structure_after_phase136_2_revision(
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

  rendered = captured.out

  assert rendered.startswith(
    "# Group proof narrative\n"
  )

  assert "**[R1]" in rendered
  assert "**[R2] Toda Proposition 5.1.**" in rendered
  assert "**[R3] Toda Proposition 5.3.**" in rendered
  assert "**[R4] Toda Lemma 5.2.**" in rendered
  assert (
    "**[R5] Toda Proposition 2.2 "
    "の右合成公式.**"
    in rendered
  )

  assert (
    "のある元を $\\nu'$ と定める."
    in rendered
  )

  assert (
    r"\nu'\in\pi_{6}^{3}.\tag{3}"
    in rendered
  )

  assert (
    r"0\longrightarrow\pi_{5}^{2}"
    r"\xrightarrow{E}\pi_{6}^{3}"
    r"\xrightarrow{H}\pi_{6}^{5}"
    r"\longrightarrow 0."
    r"\tag{19}"
    in rendered
  )

  assert (
    r"\nu'\text{ の位数は }4"
    r"\text{ である.}\tag{16}"
    in rendered
  )

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
