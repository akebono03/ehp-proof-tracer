import main as cli_main


def test_phase133_9_pi10_4_depth_two_uses_final_readable_labels(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "4",
      "6",
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
    "Toda Proposition 5.6 の有限次元結果",
    "Toda (5.6) の ν₄ 分解同型",
    "Toda Lemma 5.4 の結果",
    "Toda (5.6) の ν₄ 分解",
  )

  for label in expected_labels:
    assert label in captured.out

  internal_names = (
    "Toda Proposition 5.6 finite-dimensional integration",
    "Toda (5.6) nu_4 decomposition isomorphism semantics",
    "Toda Lemma 5.4 integration",
  )

  for internal_name in internal_names:
    assert internal_name not in captured.out


def test_phase133_9_pi16_9_depth_two_uses_final_sigma_labels(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
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
    "Theorem 3.6 から Lemma 5.14 への σ″ bridge",
    "Toda Lemma 5.14 の σ′ branch",
    "Toda Lemma 5.14 の σ₈ に関する結果",
    "σ-family の定義",
  )

  for label in expected_labels:
    assert label in captured.out

  internal_names = (
    "Toda Theorem 3.6 Lemma 5.14 sigma double-prime bridge",
    "Toda Lemma 5.14 sigma-prime branch",
  )

  for internal_name in internal_names:
    assert internal_name not in captured.out


def test_phase133_9_previous_labels_remain_available(
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
