# Group proof narrative

## 証明対象

\[
\pi_{15}^{8} = \mathbb{Z}\{\sigma_{8}\} \oplus \mathbb{Z}/8\{E\sigma'\}
\]

を示す.

## 使用する結果

**[R1] Proposition 5.15.**
$\pi_{14}^{7} = \mathbb{Z}/8\{\sigma'\}$.
$\pi_{13}^{6} = \mathbb{Z}/4\{\sigma''\}$.
$\pi_{12}^{5} = \mathbb{Z}/2\{\sigma'''\}$.
$\pi_{11}^{4} = 0$.
$\pi_{9}^{2} = 0$.
**[R2] Proposition 5.11.**
$\pi_{8}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}^{2}\}$, $\pi_{9}^{3} = 0$, $\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$, $\pi_{11}^{5} = \mathbb{Z}/2\{\nu_{5}\nu_{8}\}$, $\pi_{12}^{6} = \mathbb{Z}/2\{\nu_{6}\nu_{9}\}$, $\pi_{13}^{7} = \mathbb{Z}/2\{\nu_{7}\nu_{10}\}$, $\pi_{14}^{8} = \mathbb{Z}/2\{\nu_{8}\nu_{11}\}$, $\pi_{n + 6}^{n} = \mathbb{Z}/2\{\nu_{n}\nu_{n + 3}\}$, $n \ge 9$ が成り立つ.
$\pi_{9}^{3} = 0$.
$\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$.
$\pi_{8}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}^{2}\}$.
$\pi_{14}^{8} = \mathbb{Z}/2\{\nu_{8}\nu_{11}\}$.
**[R3] Equation 5.13.**
$\Delta\left(\eta_{13}\right) = 0$.
$\Delta\left(\nu_{9}\right) = \pm 2\nu_{4}\nu_{7}$.
$\Delta\left(\eta_{11}^{2}\right) = 0$.
**[R4] Proposition 5.3.**
$\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$, $\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}$, $\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}^{2}\}$, $\pi_{n + 2}^{n} = \mathbb{Z}/2\{\eta_{n}\eta_{n + 1}\}$, $n \ge 5$ が成り立つ.
$\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}$.
$\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}^{2}\}$.
**[R5] (5.5).**
$\nu_{n} = E^{n - 4}\nu_{4}$, $n \ge 5$, $2\nu_{n} = E^{n - 3}\nu'$, $4\nu_{n} = \eta_{n}\eta_{n + 1}\eta_{n + 2}$ が成り立つ.
**[R6] Proposition 5.6.**
$\pi_{12}^{9} = \mathbb{Z}/8\{\nu_{9}\}$.
**[R7] Proposition 5.9.**
$\pi_{8}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}^{2}\}$.
**[R8] (5.3).**
$\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ とすると,
$\nu' \in \pi_{6}^{3}$.
$2\nu' = \eta_{3}^{3}$.
$H\left(\nu'\right) = \eta_{5}$.

---

## 証明

まず, $\sigma'''$ を定める.

次の短完全列を得る.

$0\longrightarrow \pi_{13}^{6}\xrightarrow{E} \pi_{14}^{7}\xrightarrow{H} \pi_{14}^{13}\longrightarrow 0$.

[R3]より, $\Delta\left(\eta_{13}\right) = 0\tag{1}$.

(1) より,

$\Delta\left(\eta_{13}^{2}\right) = 0$.

[R2]より, $\pi_{9}^{3} = 0$.

[R2]より, $\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}$.

[R3]より, $\Delta\left(\nu_{9}\right) = \pm 2\nu_{4}\nu_{7}$.

$\Delta\left(\iota_{11}\right) = \nu_{5}\eta_{8}\tag{2}$.

$\eta_{n}\nu_{n + 1} = 0$.

[R5]を用いて, $\Delta\left(\nu_{11}\right) = 0$.

(2) より,

$\eta_{5}\nu_{6} = 0$.

$\eta_{5}\nu_{6} = E^{2}\nu'\eta_{8}$.

$2\nu_{5} = E^{2}\nu'$.

[R8]より, $H\left(\nu'\right) = \eta_{5}$.

$H\left(\nu'\eta_{6}\right) = H\left(\nu'\right)\eta_{6}$.

$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

これより,

$\eta_{3}\nu_{4} = \nu'\eta_{6}$.

これより,

$\eta_{6}\nu_{7} = 0$.

$\eta_{2} \wedge \nu_{4} = {-1}^{3\,3}\eta_{6}E^{3}\nu_{4}$.

$\eta_{2} \wedge \nu_{4} = {-1}^{2\,3}E^{2}\nu_{4}\eta_{9}$.

$\nu_{6}\eta_{9} = 0$.

$H\left(\eta_{3}\nu_{4}\right) = \eta_{5}^{2}$.

(2) より,

$\Delta\left(\eta_{11}\right) = \nu_{5}\eta_{8}^{2}$.

$4\nu_{n} = 2E^{n - 3}\nu'$.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

$2\nu_{n} = E^{n - 3}\nu'$.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

[R1]を用いて, $H: \pi_{12}^{5} \to \pi_{12}^{9}$ は単射である.

[R6]より, $\pi_{12}^{9} = \mathbb{Z}/8\{\nu_{9}\}$.

$\eta_{6}\nu_{7} = 0$.

$\eta_{2} \wedge \nu_{4} = {-1}^{3\,3}\eta_{6}E^{3}\nu_{4}$.

$\eta_{2} \wedge \nu_{4} = {-1}^{2\,3}E^{2}\nu_{4}\eta_{9}$.

$\nu_{6}\eta_{9} = 0\tag{3}$.

$\eta_{n}\nu_{n + 1} = 0$.

(3) より,

$E\nu_{5}\eta_{8}^{2} = 0$.

$\eta_{5}\nu_{6} = 0$.

$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

これより,

$H\left(\nu'\eta_{6}^{2}\right) = 4\nu_{5}$.

$\eta_{5}\nu_{6} = E^{2}\nu'\eta_{8}$.

$2\nu_{5} = E^{2}\nu'$.

$\eta_{3}\nu_{4} = \nu'\eta_{6}$.

$H\left(\eta_{3}\nu_{4}\right) = \eta_{5}^{2}$.

これより, $\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}$, この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.

[R4]を用いる.

$H\left([\iota_{4}, \iota_{4}]\right) = 2\iota_{7},\quad E[\iota_{4}, \iota_{4}] = 0,\quad u\text{ is the sign parameter}$.

$E^{n - 3}\nu' \in \{\eta_{n}, 2\iota_{n + 1}, \eta_{n + 1}\}_{t}$.

$\operatorname{Ind}\left(\{\eta_{n}, 2\iota_{n + 1}, \eta_{n + 1}\}_{t}\right) = \left\langle \eta_{n}\eta_{n + 1}\eta_{n + 2} \right\rangle$.

これより, $\operatorname{Ind}\left(\{\eta_{n}, 2\iota_{n + 1}, \eta_{n + 1}\}_{t}\right) = \left\langle 2E^{n - 3}\nu' \right\rangle$.

これより, $\{\eta_{n}, 2\iota_{n + 1}, \eta_{n + 1}\}_{t} = \{\pm E^{n - 3}\nu'\}$.

これより, $\{\eta_{5}, 2\iota_{6}, \eta_{6}\}_{3} = \{\pm E^{2}\nu'\}$.

これより, $2Eα* = \pm E^{2}\nu'$.

これより, $\begin{cases} \nu_{4} = α* - (-1)^{u}s[\iota_{4}, \iota_{4}] & \text{if } 2Eα* = E^{2}\nu' \\ \nu_{4} = -α* + (-1)^{u}\left(s + 1\right)[\iota_{4}, \iota_{4}] & \text{if } 2Eα* = -E^{2}\nu' \end{cases}$.

したがって, この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.

したがって, $\operatorname{ord}(\eta_{3}^{3})=2$ かつ $2\nu'=\eta_{3}^{3}$ より, $4\nu'=0$ かつ $2\nu'\neq0$ である.

この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.

$\operatorname{ord}(\eta_{3}^{3})=2$ かつ $2\nu'=\eta_{3}^{3}$ より, $4\nu'=0$ かつ $2\nu'\neq0$ である.

この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.

したがって, $\operatorname{ord}(\eta_{3}^{3})=2$ かつ $2\nu'=\eta_{3}^{3}$ より, $4\nu'=0$ かつ $2\nu'\neq0$ である.

この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.

したがって, $\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$ は単射である.

これより, これらより, 

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

$2\nu_{n} = E^{n - 3}\nu'$.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

群構造に関する結果と写像による移送の結果を合わせると, 対象の群の位数と写像の単射性が決まる.

$\pi_{8}^{5}/E^{2}\left(\pi_{6}^{3}\right) \cong \mathbb{Z}/2$.

$\Delta\left(\eta_{9}\right) = E\nu'\eta_{7}\tag{4}$.

(4) より,

$\Delta\left(\eta_{9}^{2}\right) = E\nu'\eta_{7}^{2}$.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

$2\nu_{n} = E^{n - 3}\nu'$.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

$E\nu_{4}\eta_{7} = \nu_{5}\eta_{8}\tag{5}$.

(5) より,

[R7]を用いて, $E\nu_{4}\eta_{7}^{2} = \nu_{5}\eta_{8}^{2}$.

次の完全列を考える.

$$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.$ は完全である.

$\eta_{4}\nu' = 0$.

これより,

$\eta_{3}\nu' = 0\tag{6}$.

$\eta_{4}\nu' = \eta_{4}E^{2}\nu'$.

$2\eta_{4} = 0$.

(6) より,

$\eta_{3}\nu'\eta_{6} = 0$.

次の完全列を考える.

$$\pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5}$ は完全である.$ は完全である.

この完全性と, 左の写像が単射, 右の写像が全射であることより, 次の短完全列を得る.

$0\longrightarrow \pi_{5}^{2}\xrightarrow{E} \pi_{6}^{3}\xrightarrow{H} \pi_{6}^{5}\longrightarrow 0$.

$\pi_{8}^{5}/E^{2}\left(\pi_{6}^{3}\right) \cong \mathbb{Z}/2$.

$\eta_{4}\nu' = 0$.

$\eta_{3}\nu' = 0$.

$\eta_{4}\nu' = \eta_{4}E^{2}\nu'$.

$2\eta_{4} = 0$.

次の完全列を考える.

$$\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5}$ は完全である.$ は完全である.

この完全性と, 左の写像が単射, 右の写像が全射であることより, 次の短完全列を得る.

$0\longrightarrow \pi_{5}^{2}\xrightarrow{E} \pi_{6}^{3}\xrightarrow{H} \pi_{6}^{5}\longrightarrow 0$.

$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

$\eta_{6}\nu_{7} = 0$.

$\eta_{2} \wedge \nu_{4} = {-1}^{3\,3}\eta_{6}E^{3}\nu_{4}$.

$\eta_{2} \wedge \nu_{4} = {-1}^{2\,3}E^{2}\nu_{4}\eta_{9}$.

$\nu_{6}\eta_{9} = 0$.

$\eta_{n}\nu_{n + 1} = 0$.

$\eta_{5}\nu_{6} = 0$.

$\eta_{5}\nu_{6} = E^{2}\nu'\eta_{8}$.

$2\nu_{5} = E^{2}\nu'$.

$\eta_{3}\nu_{4} = \nu'\eta_{6}$.

$H\left(\eta_{3}\nu_{4}\right) = \eta_{5}^{2}$.

$\pi_{8}^{5}/E^{2}\left(\pi_{6}^{3}\right) \cong \mathbb{Z}/2$.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

$2\nu_{n} = E^{n - 3}\nu'$.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

次の完全列を考える.

$$\pi_{7}^{5} \xrightarrow{Δ} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}$ は完全である.$ は完全である.

$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

$2\nu_{n} = E^{n - 3}\nu'$.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

次の完全列を考える.

$$\pi_{7}^{5} \xrightarrow{Δ} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}$ は完全である.$ は完全である.

$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

次の完全列を考える.

$$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \xrightarrow{Δ} \pi_{5}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{3} \xrightarrow{E} \pi_{6}^{4} \xrightarrow{H} \pi_{6}^{7}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{3} \xrightarrow{E} \pi_{6}^{4} \xrightarrow{H} \pi_{6}^{7}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \xrightarrow{Δ} \pi_{5}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5}$ は完全である.$ は完全である.

この完全性と, 左の写像が単射, 右の写像が全射であることより, 次の短完全列を得る.

$0\longrightarrow \pi_{5}^{2}\xrightarrow{E} \pi_{6}^{3}\xrightarrow{H} \pi_{6}^{5}\longrightarrow 0$.

$\pi_{8}^{5}/E^{2}\left(\pi_{6}^{3}\right) \cong \mathbb{Z}/2$.

$\eta_{4}\nu' = 0$.

$\eta_{3}\nu' = 0$.

$\eta_{4}\nu' = \eta_{4}E^{2}\nu'$.

$2\eta_{4} = 0$.

次の完全列を考える.

$$\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2}$ は完全である.$ は完全である.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

$2\nu_{n} = E^{n - 3}\nu'$.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

次の完全列を考える.

$$\pi_{7}^{5} \xrightarrow{Δ} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}$ は完全である.$ は完全である.

$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

次の完全列を考える.

$$\pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \xrightarrow{Δ} \pi_{5}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{3} \xrightarrow{E} \pi_{6}^{4} \xrightarrow{H} \pi_{6}^{7}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.$ は完全である.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

$2\nu_{n} = E^{n - 3}\nu'$.

$2E^{n - 3}\nu' = \eta_{n}\eta_{n + 1}\eta_{n + 2}$.

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

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{4}^{2} \xrightarrow{E} \pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.$ は完全である.

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

$$\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{Δ} \pi_{4}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{3} \xrightarrow{H} \pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{3} \xrightarrow{E} \pi_{6}^{4} \xrightarrow{H} \pi_{6}^{7}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{3} \xrightarrow{E} \pi_{6}^{4} \xrightarrow{H} \pi_{6}^{7}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{H} \pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{3} \xrightarrow{Δ} \pi_{1}^{1} \xrightarrow{E} \pi_{2}^{2}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{3} \xrightarrow{E} \pi_{6}^{4} \xrightarrow{H} \pi_{6}^{7}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{5}^{5} \xrightarrow{Δ} \pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3}$ は完全である.$ は完全である.

次の完全列を考える.

$$\pi_{3}^{2} \xrightarrow{E} \pi_{4}^{3} \xrightarrow{H} \pi_{4}^{5}$ は完全である.$ は完全である.

次に, $\nu_{7}$ を定める.

$\nu_{7}$ を \(\nu\)-family の元として定める.

次に, $\nu_{6}$ を定める.

$\nu_{6}$ を \(\nu\)-family の元として定める.

次に, $\nu_{7}$ を定める.

$\nu_{7}$ を \(\nu\)-family の元として定める.

次に, $\nu_{6}$ を定める.

$\nu_{6}$ を \(\nu\)-family の元として定める.

次に, $\nu_{7}$ を定める.

$\nu_{7}$ を \(\nu\)-family の元として定める.

次に, $\nu_{6}$ を定める.

$\nu_{6}$ を \(\nu\)-family の元として定める.

最後に, $\pi_{15}^{8}$ の群構造を決定する.

以上より, $\pi_{15}^{8} = \mathbb{Z}\{\sigma_{8}\} \oplus \mathbb{Z}/8\{E\sigma'\}$.

この完全性, 既知の群構造, および写像の像に関する結果を合わせると, 対象となる写像の像と核が決まる.

$\pi_{15}^{8} \cong \mathbb{Z}/8\{E\sigma'\} \oplus \mathbb{Z}\{\sigma_{8}\}$.

□
