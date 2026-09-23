import main as cli_main


def test_phase133_6_pi8_5_uses_readable_nu_family_labels(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "5",
      "3",
      "--depth",
      "1",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""

  assert (
    "E²: π₆³ → π₈⁵ の単射性"
    in captured.out
  )
  assert (
    "π₈⁵ / E²π₆³ が位数 2 であること"
    in captured.out
  )

  assert (
    "Toda Proposition 5.6 "
    "E^2 pi_6^3 injective"
    not in captured.out
  )
  assert (
    "Toda Proposition 5.6 "
    "pi_8^5 quotient by E^2 pi_6^3"
    not in captured.out
  )


def test_phase133_6_pi10_4_uses_readable_nu4_decomposition_label(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "4",
      "6",
      "--depth",
      "1",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""

  assert (
    "Toda (5.6) の ν₄ 分解"
    in captured.out
  )
  assert (
    "Toda (5.6) nu_4 decomposition integration"
    not in captured.out
  )


def test_phase133_6_pi12_5_uses_readable_sigma_triple_prime_labels(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "5",
      "7",
      "--depth",
      "1",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""

  assert (
    "π₁₂⁵ の位数 2 の Hopf 像への同型"
    in captured.out
  )
  assert (
    "Toda Lemma 5.13 の σ‴ に関する結果"
    in captured.out
  )

  assert (
    "Toda Proposition 5.15 "
    "pi_12^5 Hopf isomorphism"
    not in captured.out
  )
  assert (
    "Toda Lemma 5.13 "
    "sigma triple-prime definition"
    not in captured.out
  )


def test_phase133_6_sigma9_depth_two_reuses_new_labels(
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

  assert (
    "π₁₂⁵ の位数 2 の Hopf 像への同型"
    in captured.out
  )
  assert (
    "Toda Lemma 5.13 の σ‴ に関する結果"
    in captured.out
  )
  assert (
    "π₁₆⁹ の位数 16 と E⁴ の単射性"
    in captured.out
  )
  assert (
    "σ-family の定義"
    in captured.out
  )
