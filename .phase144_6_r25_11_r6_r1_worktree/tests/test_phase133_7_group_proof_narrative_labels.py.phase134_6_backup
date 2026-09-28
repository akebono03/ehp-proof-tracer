import main as cli_main


def test_phase133_7_pi6_3_depth_two_uses_readable_labels(
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

  expected_labels = (
    "Toda (5.2) の η₂ 合成同型",
    "Δ 写像が零写像であること",
    "ν′ に対する Lemma 5.2 の Toda bracket 特殊化",
    "Toda Proposition 5.1 の有限次元結果",
  )

  for label in expected_labels:
    assert label in captured.out

  internal_names = (
    "Toda 5.2 eta_2 composition isomorphism",
    "Toda Proposition 5.6 pi_7^5 Delta zero",
    "Toda 5.3 nu-prime Lemma 5.2 bracket specialization",
    "Toda Proposition 5.1 finite-dimensional integration",
  )

  for internal_name in internal_names:
    assert internal_name not in captured.out


def test_phase133_7_pi12_5_depth_two_uses_readable_labels(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "5",
      "7",
      "--depth",
      "2",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""

  expected_labels = (
    "Hopf 写像の単射性",
    "Toda Proposition 5.11 の有限次元結果",
    "Toda (5.5) の ν-family 有限次元結果",
    "π₁₂⁵ の位数 2 の Hopf 像への同型",
    "Toda Lemma 5.13 の σ‴ に関する結果",
  )

  for label in expected_labels:
    assert label in captured.out

  internal_names = (
    "Toda EHP exactness zero-left Hopf injectivity",
    "Toda Proposition 5.11 finite-dimensional integration",
    "Toda 5.5 nu-family finite-dimensional integration",
  )

  for internal_name in internal_names:
    assert internal_name not in captured.out


def test_phase133_7_phase133_6_labels_remain_available(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "5",
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

  expected_labels = (
    "Toda (5.6) の ν₄ 分解",
    "E²: π₆³ → π₈⁵ の単射性",
    "π₈⁵ / E²π₆³ が位数 2 であること",
  )

  for label in expected_labels:
    assert label in captured.out
