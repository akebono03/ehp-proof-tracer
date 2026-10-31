使用する結果

**[R1] Proposition 5.6.**

$\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}^{3}\}$.

**[R2] DB prior: sphere.csv (n=5, k=2) [参考: Proposition 5.3].**

**[R3] Chapter V, i).**

$n\ge 2$ に対し, $\eta_n=E^{n-2}\eta_2$ と定義する.

**[R4] Proposition 2.2.**

**[R5] (5.3).**

$H\left(\nu'\right) = \eta_{5}$.

$2\nu' = \eta_{3}^{3}$.

**[R6] Proposition 4.2 (4.4).**

$\pi_i^n\xrightarrow{E}\pi_{i+1}^{n+1}\xrightarrow{H}\pi_{i+1}^{2n+1}\xrightarrow{\Delta}\pi_{i-1}^{n}\xrightarrow{E}\pi_i^{n+1}$ は完全.

**[R7] Proposition 5.1.**

$\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$.

$H\left(\eta_{2}\right) = \iota_{3}$.

$\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$.

$\pi_{n+1}^{n}=\mathbb{Z}/2\{\eta_{n}\}\quad(n\ge4)$.

**[R8] DB prior: sphere.csv (n=5, k=1) [参考: Proposition 5.1].**

証明

$\pi_{6}^{3}$の群構造を決定するために, [R6]を用いて次の完全列を考える.

$\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5} \xrightarrow{\Delta} \pi_{4}^{2}$.

[R1]より, $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}^{3}\}$.

[R2]より, $\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}$.

[R3]より, $E(\eta_{5})=\eta_{6}$.

$E\eta_{5} = \eta_{6}$.

$\eta_{6} = E\eta_{5}$.

$\nu'\eta_{6} = \nu'E\eta_{5}$.

$H\left(\nu'\eta_{6}\right) = H\left(\nu'E\eta_{5}\right)$.

$H\left(\nu'E\eta_{5}\right) = H\left(\nu'\right)E\eta_{5}$.

[R5]より, $H\left(\nu'\right) = \eta_{5}$.

$H\left(\nu'E\eta_{5}\right) = \eta_{5}E\eta_{5}$.

$H\left(\nu'\eta_{6}\right) = \eta_{5}E\eta_{5}$.

$\eta_{5}E\eta_{5} = \eta_{5}^{2}$.

$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

$H: \pi_{7}^{3}\to \pi_{7}^{5}$ は全射.

$\Delta: \pi_{7}^{5}\to \pi_{5}^{2}$ は零写像.

完全性より, $\ker E=\operatorname{Im}\Delta=0$ なので, $E: \pi_{5}^{2}\to \pi_{6}^{3}$ は単射.

[R7]より, $\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$.

$H: \pi_{6}^{3}\to \pi_{6}^{5}$ は全射.

$H$ の全射性と完全性より, $\ker\Delta=\operatorname{Im}H=\pi_{6}^{5}$ なので, $\Delta: \pi_{6}^{5}\to \pi_{4}^{2}$ は零写像.

完全性より, $H: \pi_{6}^{3}\to \pi_{6}^{5}$ は全射.

[R5]より, $2\nu' = \eta_{3}^{3}$.

[R3]より, $E(\eta_{2})=\eta_{3},\quad E(\eta_{3}^{2})=\eta_{4}^{2},\quad E(\eta_{2}^{3})=\eta_{3}^{3}$.

$2\nu' = E\left(\eta_{2}^{3}\right)$.

証明済みの単射性・全射性と完全性から, $0\longrightarrow \pi_{5}^{2}\xrightarrow{E}\pi_{6}^{3}\xrightarrow{H}\pi_{6}^{5}\longrightarrow 0$ は短完全列となる.

両端の群の位数はそれぞれ $2$, $2$ なので, $|\pi_{6}^{3}|=2\cdot2=4$.

また, 単射性によって $E\left(\eta_{2}^{3}\right)\neq0$ であり, 証明済みの $2\nu'=E\left(\eta_{2}^{3}\right)$ より $2\nu'\neq0$.

よって $\operatorname{ord}(\nu')=4$.

以上より, $\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$.

□
