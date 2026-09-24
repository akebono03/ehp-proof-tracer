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
    "まず, Lemma 5.2 を "
    "$\\alpha=\\eta_{3}$, $i=4$, "
    "$\\beta=\\nu'$ として適用するための仮定を確認する."
  )

  second = (
    "$\\nu'$ の位数を決定するために, "
    "次の EHP 完全列を考える."
  )

  third = (
    "最後に, $\\pi_{6}^{3}$ の群構造を決定する."
  )

  assert first in rendered
  assert second in rendered
  assert third in rendered

  assert (
    rendered.index(first)
    < rendered.index(second)
    < rendered.index(third)
  )

def test_phase134_7_boundary_facts_remain_numbered_facts(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert (
    r"\pi_{5}^{3}="
    r"\mathbb{Z}/2\{\eta_{3}^{2}\}."
    r"\tag{6}"
    in rendered
  )

  assert (
    r"2\nu'="
    r"\eta_{3}\circ E\eta_{3}\circ\eta_{5}"
    r"=\eta_{3}^{3}."
    r"\tag{5}"
    in rendered
  )

  assert (
    r"H(\nu')=\eta_{5}."
    r"\tag{4}"
    in rendered
  )

def test_phase134_7_reference_section_matches_phase136_structure(
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
    r"\pi_{5}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}^{2}\}"
    in reference_section
  )

  assert (
    r"\nu' \in "
    r"\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}."
    in reference_section
  )

  assert (
    r"H(\nu')=E^{2}\eta_{3}"
    in reference_section
  )

def test_phase134_7_uses_final_conclusion_lead(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert "以上により," in rendered

  final_target = (
    r"\pi_{6}^{3}="
    r"\mathbb{Z}/4\{\nu'\}"
    r"\tag{20}"
  )

  assert final_target in rendered

  assert (
    rendered.index(
      "以上により,"
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
    rendered.index("[R1]")
    < rendered.index("[R2]")
    < rendered.index("[R3]")
    < rendered.index("[R4]")
    < rendered.index("[R5]")
  )

  assert "(6), [R1] より," in rendered
  assert "[R2] の $n=5$ の場合より," in rendered

def test_phase134_7_keeps_ascii_punctuation(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert "、" not in rendered
  assert "。" not in rendered
