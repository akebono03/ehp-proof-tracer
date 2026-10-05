# Group proof narrative

## 証明対象

\[
\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}
\]

を示す.

## 使用する結果

**[R1] Proposition 5.6.**
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

$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$.

$\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$.

Proposition 5.3 を順次適用し, suspension による安定化を用いると, 

これより, $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$, この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.

$\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}$, $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}^{2}\}$, $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$, $n \ge 5$ が成り立つ.

これより, $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である.

これより, $\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である.

[R2]より, $H\left(\nu'\right) = \eta_{5}$.

$\eta_{6}=E\eta_{5}$ である.

[R4]より, $H(\alpha\circ E\beta) = H(\alpha)\circ E\beta$.

$H\left(\nu'\eta_{6}\right) = H\left(\nu'\right)\eta_{6}$.

$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

[R3]より, $\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}$.

$\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}$ は完全である.

完全性より, $\ker \Delta=\operatorname{Im}H=\pi_{7}^{5}$ である.

この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.

$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である.

次に, $\nu'$ の位数を決定する.

[R2]より, $2\nu' = \eta_{3}^{3}$.

[R1] と $E$ の単射性より, $E(\eta_{2}^{3})=\eta_{3}^{3}\neq0$ であり, 単射写像は元の位数を保つ.

$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$.

以上より, $\operatorname{ord}(\eta_{3}^{3})=2$ かつ $2\nu'=\eta_{3}^{3}$ より, $4\nu'=0$ かつ $2\nu'\neq0$ である.

$\operatorname{ord}\left(\nu'\right) = 4$.

次の完全列を考える.

$$\pi_{7}^{5} \xrightarrow{Δ} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \xrightarrow{Δ} \pi_{5}^{2}$ は完全である.$ は完全である.

これより,

$E^{n - 3}\eta_{3} = \eta_{n}$.

次の完全列を考える.

$$\pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2}$ は完全である.$ は完全である.

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

最後に, $\pi_{6}^{3}$ の群構造を決定するために, 次の完全列を考える.

$\pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$.

この完全性と, 左の写像が単射, 右の写像が全射であることより, 次の短完全列を得る.

$0\longrightarrow \pi_{5}^{2}\xrightarrow{E} \pi_{6}^{3}\xrightarrow{H} \pi_{6}^{5}\longrightarrow 0$.

[R2]より, $\nu' \in \pi_{6}^{3}$.

$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$.

$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である.

以上より, この短完全列と両端の群の位数より, 中央の群の位数は $2\cdot2=4$ である.
また, $\nu'$ は中央の群に属し, $\operatorname{ord}(\nu')=4$ であるから, $\nu'$ は中央の群を生成する.

$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$.

□
