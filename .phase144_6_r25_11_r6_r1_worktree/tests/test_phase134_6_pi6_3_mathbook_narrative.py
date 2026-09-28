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


def test_phase134_6_delta_zero_remains_proof_fact(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert (
    r"\Delta:\pi_{7}^{5}\to\pi_{5}^{2}"
    r"\quad\text{は零写像である.}"
    r"\tag{13}"
    in rendered
  )

  assert (
    "Δ 写像が零写像であることを用いる."
    not in rendered
  )

def test_phase134_6_nu_prime_bracket_specialization_remains_fact(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert (
    r"\nu' \in "
    r"\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}."
    r"\tag{2}"
    in rendered
  )

  assert (
    "この bracket のある元を "
    "$\\nu'$ と定める."
    in rendered
  )

def test_phase134_6_zero_relation_has_no_mechanical_suffix(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  zero_formula = (
    r"2\eta_{3}=0.\tag{1}"
  )

  assert zero_formula in rendered

  zero_start = rendered.index(
    zero_formula
  )

  zero_tail = rendered[
    zero_start:
    zero_start + 120
  ]

  assert (
    "が成り立つ."
    not in zero_tail
  )

def test_phase134_6_membership_has_no_mechanical_suffix(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  membership = (
    r"\nu'\in\pi_{6}^{3}.\tag{3}"
  )

  assert membership in rendered

  membership_start = rendered.index(
    membership
  )

  membership_tail = rendered[
    membership_start:
    membership_start + 120
  ]

  assert (
    "が成り立つ."
    not in membership_tail
  )

def test_phase134_6_reference_order_follows_first_use(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  r1 = rendered.index(
    "[R1]"
  )

  r2 = rendered.index(
    "[R2]"
  )

  r3 = rendered.index(
    "[R3]"
  )

  proof = rendered.index(
    "## 証明\n"
  )

  assert r1 < r2 < r3 < proof

  assert (
    "(6), [R1] より,"
    in rendered
  )

  assert (
    "[R2] の $n=5$ の場合より,"
    in rendered
  )

def test_phase134_6_does_not_promote_derived_boundary_facts_to_references(
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
    "Δ 写像が零写像"
    not in reference_section
  )

  assert (
    "Toda bracket 特殊化"
    not in reference_section
  )


def test_phase134_6_keeps_target_and_final_conclusion(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  target = (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}"
  )
  final_target = (
    r"\pi_{6}^{3}="
    r"\mathbb{Z}/4\{\nu'\}"
    r"\tag{20}"
  )

  assert target in rendered
  assert final_target in rendered
  assert "以上により," in rendered
  assert "を得る." in rendered

def test_phase134_6_keeps_ascii_punctuation(
  capsys,
):
  rendered = _render_pi6_3(
    capsys
  )

  assert "、" not in rendered
  assert "。" not in rendered
