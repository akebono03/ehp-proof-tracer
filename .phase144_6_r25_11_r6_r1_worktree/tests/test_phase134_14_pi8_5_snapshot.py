import main as cli_main


PI8_5_EXPECTED = r"""# Group proof narrative

## 証明対象

Toda Proposition 5.6 のうち,

\[
\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}
\]

を示す.

## 使用する結果

**[R1] Toda (5.5) の ν-family 有限次元結果.**

**[R2] Toda (5.6) の ν₄ 分解.**

## 証明

まず, $\nu_{5}$ の位数を求める.

**(1)** $\nu_{5}$ を $\nu$-family の定義により取る.

[R1], (1) より,

\[
2\nu_{5} = E^{2}\nu'\tag{2}
\]

既に,

\[
\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}\tag{3}
\]

[R2] より,
**(4)** E²: π₆³ → π₈⁵ の単射性.

(3), (4) より,
**(5)** $E^{2}\nu'$ の位数は $4$ である.

(2), (5), (1) より,
**(6)** $\nu_{5}$ の位数は $8$ である.

[R2] より,
**(7)** π₈⁵ / E²π₆³ が位数 2 であること.

最後に, これらの結果から $\pi_{8}^{5}$ の群構造を決定する.

(3), (4), (7) より, $E^{2}\pi_{6}^{3}$ は位数 $4$ の部分群であり, その商が位数 $2$ なので, $\pi_{8}^{5}$ の位数は $8$ である.

(6) より $\nu_{5}$ も位数 $8$ であるから, $\nu_{5}$ は $\pi_{8}^{5}$ を生成する.

したがって,

\[
\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}\tag{8}
\]

を得る.

"""


def test_phase134_14_pi8_5_output_is_byte_for_byte_unchanged(
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
  assert captured.out == PI8_5_EXPECTED
