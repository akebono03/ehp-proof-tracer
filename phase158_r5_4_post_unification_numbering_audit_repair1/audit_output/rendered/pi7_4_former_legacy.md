# Group proof narrative

## 証明対象

\[
\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}
\]

を示す.

## 使用する結果

**[R1] Proposition 5.6.**
$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$.
$\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}^{3}\}$.
**[R2] Lemma 5.4.**
$H\left(\nu_{4}\right) = \iota_{7}$.
**[R3] (5.3).**
$\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ とすると,
$\nu' \in \pi_{6}^{3}$.
$2\nu' = \eta_{3}^{3}$.
$H\left(\nu'\right) = \eta_{5}$.
**[R4] Proposition 5.3.**
$\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}$.
**[R5] Proposition 2.2.**
$H(\alpha\circ E\beta) = H(\alpha)\circ E\beta$.

---

## 証明

最後に, $\pi_{7}^{4}$ の群構造を決定する.

$\operatorname{ord}(\eta_{3}^{3})=2$ かつ $2\nu'=\eta_{3}^{3}$ より, $4\nu'=0$ かつ $2\nu'\neq0$ である.

[R1] と $E$ の単射性より, $E(\eta_{2}^{3})=\eta_{3}^{3}\neq0$ であり, 単射写像は元の位数を保つ.

[R3]より, $2\nu' = \eta_{3}^{3}$.

$\operatorname{ord}\left(\nu'\right) = 4$.

[R1]より, $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$.

$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$.

これより, $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$.

Proposition 5.3 を順次適用し, suspension による安定化を用いると, 

これより, $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である.

これより, $\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である.

[R3]より, $H\left(\nu'\right) = \eta_{5}$.

$\eta_{6}=E\eta_{5}$ である.

[R5]より, $H(\alpha\circ E\beta) = H(\alpha)\circ E\beta$.

$H\left(\nu'\eta_{6}\right) = H\left(\nu'\right)\eta_{6}$.

$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

[R4]より, $\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}$.

$\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}$ は完全である.

完全性より, $\ker \Delta=\operatorname{Im}H=\pi_{7}^{5}$ である.

これより, この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.

$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である.

$\pi_{7}^{7} = \mathbb{Z}\{\iota_{7}\}$.

以上より, これより, 

$\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$, この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.

$\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}$, $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}^{2}\}$, $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$, $n \ge 5$ が成り立つ.

$\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}$.

[R2]を用いて, $\nu_{4}$ の分解を用いる.

これより,

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

これより,

$E^{n - 3}\eta_{3} = \eta_{n}$.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

□
