# Group proof narrative

## 証明対象

\[
\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}.
\]

## 使用する結果

**[R1] (5.1).**
$\pi_{i}^{1} = 0\ (i > 1)$.
$\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}\qquad (n \ge 1)$.
**[R2] Proposition 5.1.**
$H(\eta_{2}) = \iota_{3}$.
$\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$.

---

## 証明

$\pi_{4}^{3}$ の群構造を決定するために, 次の完全列を考える.

\[
\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}.
\]

infinite cyclic quotient structure

$\eta_{3}=E\eta_{2}$.

$E(\eta_{2}) = \eta_{3}$.

$\pi_{4}^{5} = 0$.

完全性より, $E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射.

[R1]より, $\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}$.

これより, $\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$.

[R2]より, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$.

これより, $\operatorname{Im}\Delta = \mathbb{Z}\{2\eta_{2}\}$.

[R1]より, $\pi_{2}^{1} = 0$.

完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射.

[R1]より, $\pi_{1}^{1} = \mathbb{Z}\{\iota_{1}\}$.

[R1]より, $\pi_{2}^{2} = \mathbb{Z}\{\iota_{2}\}$.

$E(\iota_{1}) = \iota_{2}$.

これより, $E: \pi_{1}^{1} \to \pi_{2}^{2}$ は同型.

完全性より, $\operatorname{Im}Δ=\ker E=0$ なので, $\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ は零写像.

\[
\pi_{3}^{3} \xrightarrow{\Delta} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}.
\]

完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は全射.

単射性と全射性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型.

[R1]より, $\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}$.

[R2]より, $H(\eta_{2}) = \iota_{3}$.

これより, $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$.

以上より, $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$.

□