import main as cli_main


def _render_phase134_3_pi6_3(
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


def test_phase134_3_pi6_3_has_reference_section(
  capsys,
):
  rendered = (
    _render_phase134_3_pi6_3(
      capsys
    )
  )

  assert "## 参照" in rendered

  assert (
    "**[R1] Toda Proposition 5.6.**"
    in rendered
  )

  assert (
    "本証明では, Proposition 5.6 "
    "のうち次の主張を示す."
    in rendered
  )

  assert (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}"
    in rendered
  )


def test_phase134_3_pi6_3_uses_numbered_facts(
  capsys,
):
  rendered = (
    _render_phase134_3_pi6_3(
      capsys
    )
  )

  assert r"\tag{" in rendered
  assert "## 証明" in rendered
  assert " より," in rendered
  assert "以上から," in rendered


def test_phase134_3_pi6_3_map_properties_use_japanese_prose(
  capsys,
):
  rendered = (
    _render_phase134_3_pi6_3(
      capsys
    )
  )

  assert "は単射である." in rendered
  assert "は全射である." in rendered
  assert "は完全である." in rendered

  assert (
    r"\text{ is injective}"
    not in rendered
  )

  assert (
    r"\text{ is surjective}"
    not in rendered
  )

  assert (
    r"\text{ is exact}"
    not in rendered
  )


def test_phase134_3_pi6_3_uses_ascii_punctuation(
  capsys,
):
  rendered = (
    _render_phase134_3_pi6_3(
      capsys
    )
  )

  assert "、" not in rendered
  assert "。" not in rendered


def test_phase134_3_pi6_3_preserves_phase133_readable_labels(
  capsys,
):
  rendered = (
    _render_phase134_3_pi6_3(
      capsys
    )
  )

  expected_labels = (
    "Toda (5.2) の η₂ 合成同型",
    "Δ 写像が零写像であること",
    (
      "ν′ に対する Lemma 5.2 "
      "の Toda bracket 特殊化"
    ),
    (
      "Toda Proposition 5.1 "
      "の有限次元結果"
    ),
  )

  for label in expected_labels:
    assert label in rendered


def test_phase134_3_pi6_3_does_not_expose_internal_rule_names(
  capsys,
):
  rendered = (
    _render_phase134_3_pi6_3(
      capsys
    )
  )

  internal_names = (
    "Toda 5.2 eta_2 composition isomorphism",
    (
      "Toda Proposition 5.6 "
      "pi_7^5 Delta zero"
    ),
    (
      "Toda 5.3 nu-prime "
      "Lemma 5.2 bracket specialization"
    ),
    (
      "Toda Proposition 5.1 "
      "finite-dimensional integration"
    ),
  )

  for internal_name in internal_names:
    assert internal_name not in rendered
