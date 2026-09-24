import main as cli_main


EXPECTED_PI6_3 = r"""# Group proof narrative

## 証明対象

Toda Proposition 5.6 のうち,

\[
\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}
\]

を示す.

## 使用する結果

**[R1] Toda (5.2) の η₂ 合成同型.**

次の合成写像は同型である.

\[
\eta_{2}\circ - : \pi_{i}^{3} \longrightarrow \pi_{i}^{2}.
\]

**[R2] Toda Proposition 5.1 の有限次元結果.**

次の群構造を用いる.

\[
\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}\qquad (n \ge 3).
\]

## 証明

まず, $\nu'$ の位数を求める.

Toda Proposition 5.3 より,

\[
\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}.\tag{1}
\]

(1), [R1] より,

\[
\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}^{3}\}.\tag{2}
\]

EHP 完全列と Toda Proposition 5.3 より,

\[
\Delta: \pi_{7}^{5} \to \pi_{5}^{2}\quad\text{は零写像である.}\tag{3}
\]

EHP 完全列より,

\[
\pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}\quad\text{は完全である.}\tag{4}
\]

(3), (4) より,

\[
E: \pi_{5}^{2} \to \pi_{6}^{3}\quad\text{は単射である.}\tag{5}
\]

(2), (5) より,

\[
\eta_{3}^{3}\text{ の位数は }2\text{ である.}\tag{6}
\]


\[
2\nu' = \eta_{3}^{3}.\tag{7}
\]

(6), (7) より,

\[
\nu'\text{ の位数は }4\text{ である.}\tag{8}
\]

次に, $\nu' \in \pi_{6}^{3}$ であることを確認する.

Toda Lemma 5.2 の ν′ に対する特殊化より,

\[
\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}.\tag{9}
\]

[R2] より,

\[
2\eta_{3} = 0.\tag{10}
\]

(9), (10) より,

\[
\nu' \in \pi_{6}^{3}.\tag{11}
\]

最後に, EHP 完全列を用いて $\pi_{6}^{3}$ の群構造を決定する.

EHP 完全列より,

\[
\pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5}\quad\text{は完全である.}\tag{12}
\]

Toda Proposition 5.3 より,

\[
H\left(\nu'\right) = \eta_{5}.\tag{13}
\]

(13), [R2] より,

\[
H: \pi_{6}^{3} \to \pi_{6}^{5}\quad\text{は全射である.}\tag{14}
\]

[R2] より,

\[
\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}.\tag{15}
\]

したがって,

\[
\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}\tag{16}
\]

を得る.

"""


def test_phase134_9_pi6_3_output_is_byte_for_byte_unchanged(
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
  assert captured.out == EXPECTED_PI6_3
