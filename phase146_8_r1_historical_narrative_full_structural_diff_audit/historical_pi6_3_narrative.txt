# Group proof narrative

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

**[R2] Toda Proposition 5.1.**

\[
\pi_{n + 1}^{n} = \mathbb{Z}/2\{\eta_{n}\}\qquad (n \ge 3).
\]

**[R3] Toda Proposition 5.3.**

\[
\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}^{2}\}\qquad (n \ge 2).
\]

\[
\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\},\qquad\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}.
\]

**[R4] Toda Lemma 5.2.**

まず Lemma 5.2 の一般形を記す.

$\alpha\in\pi_i^3$, $2\alpha=0$ であり,

\[
\beta \in \{\eta_{3},2\iota_{4},E\alpha\}_{1}
\]

ならば,

\[
\beta\in\pi_{i+2}^{3},
\qquad
H(\beta)=E^{2}\alpha,
\qquad
2\beta=\eta_{3}\circ E\alpha\circ\eta_{i+1},
\qquad
\Delta(E^{2}\alpha)=0.
\]

この証明では $\alpha=\eta_{3}$, $i=4$ とする. まず $2\eta_{3}=0$ を確認すると, Toda bracket

\[
\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}
\]

が定義できる. この bracket のある元を $\nu'$ と定める. すなわち,

\[
\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}.
\]

すると Lemma 5.2 より,

\[
\nu'\in\pi_{6}^{3},
\qquad
H(\nu')=E^{2}\eta_{3},
\qquad
2\nu'=\eta_{3}\circ E\eta_{3}\circ\eta_{5},
\qquad
\Delta(E^{2}\eta_{3})=0
\]

を得る.

**[R5] Toda Proposition 2.2 の右合成公式.**

\[
H(\alpha\circ E\beta)=H(\alpha)\circ E\beta.
\]

## 証明

まず, Lemma 5.2 を $\alpha=\eta_{3}$, $i=4$, $\beta=\nu'$ として適用するための仮定を確認する.

[R2] の $n=3$ の場合より,

\[
2\eta_{3}=0.\tag{1}
\]

したがって Toda bracket $\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}$ が定義できる. [R4] でこの bracket のある元を $\nu'$ と定めたので,

\[
\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}.\tag{2}
\]

(1), (2) により Lemma 5.2 の仮定が満たされる. したがって Lemma 5.2 の結論から,

\[
\nu'\in\pi_{6}^{3}.\tag{3}
\]

さらに $H(\beta)=E^{2}\alpha$ と $E^{2}\eta_{3}=\eta_{5}$ から,

\[
H(\nu')=\eta_{5}.\tag{4}
\]

また $2\beta=\eta_{3}\circ E\alpha\circ\eta_{i+1}$ と $E\eta_{3}=\eta_{4}$ から,

\[
2\nu'=\eta_{3}\circ E\eta_{3}\circ\eta_{5}=\eta_{3}^{3}.\tag{5}
\]

[R3] の $n=3$ の場合より,

\[
\pi_{5}^{3}=\mathbb{Z}/2\{\eta_{3}^{2}\}.\tag{6}
\]

(6), [R1] より,

\[
\pi_{5}^{2}=\mathbb{Z}/2\{\eta_{2}^{3}\}.\tag{7}
\]

$\nu'$ の位数を決定するために, 次の EHP 完全列を考える.

\[
\pi_{7}^{3}\xrightarrow{H}\pi_{7}^{5}\xrightarrow{\Delta}\pi_{5}^{2}\xrightarrow{E}\pi_{6}^{3}\xrightarrow{H}\pi_{6}^{5}\quad\text{は完全である.}\tag{8}
\]

[R2] の $n=6$ の場合より $\eta_{6}\in\pi_{7}^{6}$ であり, (3) と合成して,

\[
\nu'\eta_{6}\in\pi_{7}^{3}.\tag{9}
\]

また η-family の suspension relation $\eta_{6}=E\eta_{5}$ を用いる. [R5] の Toda Proposition 2.2 に $\alpha=\nu'$, $\beta=\eta_{5}$ を代入すると,

\[
H(\nu'\eta_{6})=H(\nu'\circ E\eta_{5})=H(\nu')\circ E\eta_{5}=\eta_{5}\eta_{6}=\eta_{5}^{2}.\tag{10}
\]

[R3] の $n=5$ の場合より,

\[
\pi_{7}^{5}=\mathbb{Z}/2\{\eta_{5}^{2}\}.\tag{11}
\]

(9), (10), (11) より, $H:\pi_{7}^{3}\to\pi_{7}^{5}$ は生成元 $\eta_{5}^{2}$ を像に持つ. したがって,

\[
H:\pi_{7}^{3}\to\pi_{7}^{5}\quad\text{は全射である.}\tag{12}
\]

(8), (12) の完全性より $\operatorname{Im}H=\ker\Delta=\pi_{7}^{5}$ である. よって,

\[
\Delta:\pi_{7}^{5}\to\pi_{5}^{2}\quad\text{は零写像である.}\tag{13}
\]

さらに (8), (13) より $\operatorname{Im}\Delta=\ker E=0$ なので,

\[
E:\pi_{5}^{2}\to\pi_{6}^{3}\quad\text{は単射である.}\tag{14}
\]

(7), (14) と η-family の suspension relation $E(\eta_{2}^{3})=\eta_{3}^{3}$ より,

\[
\eta_{3}^{3}\text{ の位数は }2\text{ である.}\tag{15}
\]

(5), (15) より,

\[
\nu'\text{ の位数は }4\text{ である.}\tag{16}
\]

最後に, $\pi_{6}^{3}$ の群構造を決定する.

[R2] の $n=5$ の場合より,

\[
\pi_{6}^{5}=\mathbb{Z}/2\{\eta_{5}\}.\tag{17}
\]

(4), (17) より,

\[
H:\pi_{6}^{3}\to\pi_{6}^{5}\quad\text{は全射である.}\tag{18}
\]

(8), (14), (18) より, $E$ は単射, $H$ は全射なので, 次の短完全列を得る.

\[
0\longrightarrow\pi_{5}^{2}\xrightarrow{E}\pi_{6}^{3}\xrightarrow{H}\pi_{6}^{5}\longrightarrow 0.\tag{19}
\]

(7), (17), (19) より $\pi_{6}^{3}$ の位数は 4 である. 一方, (3), (16) より $\nu'\in\pi_{6}^{3}$ は位数 4 の元なので, $\nu'$ が群全体を生成する.

以上により,

\[
\pi_{6}^{3}=\mathbb{Z}/4\{\nu'\}\tag{20}
\]

を得る.

