import main as cli_main


def test_phase133_10_sigma9_depth_two_uses_final_japanese_wording(
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
  assert "Theorem 3.6" in captured.out
  assert "Lemma 5.14" in captured.out
  assert (
    r"$\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}$"
    in captured.out
  )

  assert (
    "Theorem 3.6 から Lemma 5.14 への σ″ bridge"
    not in captured.out
  )
  assert (
    "Toda Lemma 5.14 の σ′ branch"
    not in captured.out
  )
