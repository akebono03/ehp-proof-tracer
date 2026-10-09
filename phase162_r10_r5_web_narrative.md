# Group proof narrative

## 証明対象

\[
\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}.
\]

## 使用する結果

**[R1] (5.3).**
$H\left(\nu'\right) = \eta_{5}$.
**[R2] (4.5).**
$E^{n - 3}: \pi_{3 + 1}^{3} \to \pi_{n + 1}^{n}$ は同型.

---

## 証明

$\pi_{5}^{3}$ の群構造を決定するために, 次の完全列を考える.

\[
\pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}.
\]

[R1]より, $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射.

完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は単射.

完全性より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は全射.

完全性より, $E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射.

$\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$.

$\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$.

$\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$.

$\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$.

$[\iota_{2}, \iota_{2}]$.

これより, $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ.

$\operatorname{Im}\Delta = \mathbb{Z}\{2\eta_{2}\}$.

完全性より, $\ker E=\operatorname{Im}Δ=\mathbb{Z}\{2\eta_{2}\}$.

$\pi_{4}^{5} = 0$.

$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$.

これより, $\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$.

$\Delta\left(\iota_{5}\right) = \pm [\iota_{2}, \iota_{2}]$.

$[\iota_{2}, \iota_{2}]$.

これより, $H([\iota_{2}, \iota_{2}]) = \pm 2\iota_{3}$ が成り立つ.

[R2]より, $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$.

$\pi_{4}^{5} = 0$.

これより, $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$.

$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$.

完全性より, $\ker \Delta=\operatorname{Im}H=\pi_{6}^{5}$ である.

これより, $\Delta: \pi_{6}^{5} \to \pi_{4}^{2}$ は零写像.

完全性より,

\[
E: \pi_{4}^{2} \to \pi_{5}^{3}\quad\text{は単射}. \qquad (1)
\]

\[
\pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}.
\]

$\Delta: \pi_{5}^{5} \to \pi_{3}^{2}$ は単射.

完全性より, これより, $H: \pi_{5}^{3} \to \pi_{5}^{5}$ は零写像.

完全性より,

\[
E: \pi_{4}^{2} \to \pi_{5}^{3}\quad\text{は全射}. \qquad (2)
\]

(1), (2) より, $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型.

$\eta_{4}=E\eta_{3}$.

$\eta_{3}\eta_{3} = \eta_{3}^{2}$.

これより, 以上より, 

$\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}$.

証明木に記録された群構造の移送について、$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ と $E^{n - 3}: \pi_{3 + 1}^{3} \xrightarrow{\cong} \pi_{n + 1}^{n}$ から $\pi_{n + 1}^{n} = \mathbb{Z}/2\{E^{n - 3}\eta_{3}\}$ を得る。生成元の対応は $E^{n - 3}\eta_{3} = \eta_{n}$ である。

□