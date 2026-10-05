# Group proof narrative

## 証明対象

\[
\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}
\]

を示す.

## 使用する結果

**[R1] Proposition 5.6.**
$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$.
$\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}^{3}\}$.
**[R2] (5.3).**
$\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ とすると,
$\nu' \in \pi_{6}^{3}$.
$2\nu' = \eta_{3}^{3}$.
$H\left(\nu'\right) = \eta_{5}$.
**[R3] Proposition 5.3.**
$\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}$.
**[R4] Proposition 2.2.**
$H(\alpha\circ E\beta) = H(\alpha)\circ E\beta$.

---

## 証明

まず, $\nu_{n}$ を定める.

$\nu_{n}$ を \(\nu\)-family の元として定める.

次に, $\nu_{5}$ を定める.

$\nu_{5}$ を \(\nu\)-family の元として定める.

次に, $\nu_{5}$ の位数を決定する.

$2\nu_{5} = E^{2}\nu'$.

[R1]より, $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$.

$\operatorname{ord}\left(E^{2}\nu'\right) = 4$.

[R2]より, $2\nu' = \eta_{3}^{3}$.

$\operatorname{ord}\left(\nu'\right) = 4$.

$\operatorname{ord}\left(\nu_{5}\right) = 8$.

これより,

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

(1) より,

$22\nu_{n} = 4\nu_{n}\tag{1}$.

$4\nu_{n} = 22\nu_{n}$.

(2) より,

$2\nu_{n} = E^{n - 3}\nu'\tag{2}$.

$22\nu_{n} = 2E^{n - 3}\nu'$.

$4\nu_{n} = 2E^{n - 3}\nu'$.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

$4\nu_{n} = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

[R2]より, $H\left(\nu'\right) = \eta_{5}$.

$H\left(\nu'\eta_{6}\right) = H\left(\nu'\right)\eta_{6}$.

$\eta_{6}=E\eta_{5}$ である.

$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

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

最後に, $\pi_{8}^{5}$ の群構造を決定する.

これより, $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である.

これより, $\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である.

[R4]より, $H(\alpha\circ E\beta) = H(\alpha)\circ E\beta$.

[R3]より, $\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}$.

$\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}$ は完全である.

完全性より, $\ker \Delta=\operatorname{Im}H=\pi_{7}^{5}$ である.

これより, この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.

$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である.

$\operatorname{ord}(\eta_{3}^{3})=2$ かつ $2\nu'=\eta_{3}^{3}$ より, $4\nu'=0$ かつ $2\nu'\neq0$ である.

[R1] と $E$ の単射性より, $E(\eta_{2}^{3})=\eta_{3}^{3}\neq0$ であり, 単射写像は元の位数を保つ.

群構造に関する結果と写像による移送の結果を合わせると, 対象の群の位数と写像の単射性が決まる.

$\pi_{8}^{5}/E^{2}\left(\pi_{6}^{3}\right) \cong \mathbb{Z}/2$.

以上より, $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$.

これより, $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$.

Proposition 5.3 を順次適用し, suspension による安定化を用いると, 

これより, $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$, この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.

$\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}$, $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}^{2}\}$, $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$, $n \ge 5$ が成り立つ.

$\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}$.

□
