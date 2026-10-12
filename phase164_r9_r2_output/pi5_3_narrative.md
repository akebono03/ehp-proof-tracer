# Group proof narrative

## 証明対象

\[
\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}.
\]

## 使用する結果

**[R1] (5.3).**
$H\left(\nu'\right) = \eta_{5}$.

---

## 証明

$\pi_{5}^{3}$ の群構造を決定するために, 次の完全列を考える.

\[
\pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2}.
\]

$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$.

$\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$.

$\Delta: \pi_{5}^{5} \to \pi_{3}^{2}$ は単射.

完全性より, $H: \pi_{5}^{3} \to \pi_{5}^{5}$ は零写像.

完全性より,

\[
E: \pi_{4}^{2} \to \pi_{5}^{3}\quad\text{は全射}. \qquad (2)
\]


[R1]より, $H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射.

完全性より, $\ker \Delta=\operatorname{Im}H=\pi_{6}^{5}$ である.

$\Delta: \pi_{6}^{5} \to \pi_{4}^{2}$ は零写像.

完全性より,

\[
E: \pi_{4}^{2} \to \pi_{5}^{3}\quad\text{は単射}. \qquad (1)
\]

(1), (2) より, $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型.

$\eta_{4}=E\eta_{3}$.

$\eta_{3}\eta_{3} = \eta_{3}^{2}$.

以上より, $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}$.

□