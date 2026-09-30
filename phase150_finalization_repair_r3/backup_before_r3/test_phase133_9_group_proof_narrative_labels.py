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

  assert "## 使用する結果" in captured.out
  assert "Proposition 5.11" in captured.out
  assert "Proposition 5.6" in captured.out
  assert r"\pi_{10}^{4}" in captured.out

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

  assert "## 使用する結果" in captured.out
  assert "Proposition 5.15" in captured.out
  assert "Lemma 5.14" in captured.out
  assert "Theorem 3.6" in captured.out

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

  assert "## 使用する結果" in captured.out
  assert "Proposition 5.15" in captured.out
  assert "Lemma 5.13" in captured.out
  assert r"\pi_{12}^{5}" in captured.out
