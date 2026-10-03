# Group proof narrative

## 使用する結果

**[R1] (5.3).**
$\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ とすると,
$\nu' \in \pi_{6}^{3}$,
$2\nu' = \eta_{3}\eta_{4}\eta_{5}$.
**[R2] Proposition 5.3.**
$\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}\eta_{4}\}$
**[R3] Proposition 5.6.**
$\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$

---

## 証明

次に, $\nu'$ の位数を決定するために, 次の完全列を考える.

$\pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}$

$2\nu' = \eta_{3}\eta_{4}\eta_{5}\tag{1}$

$\eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}\tag{2}$

(1) と (2) より, 

$2\nu' = \eta_{3}^{3}\tag{3}$

$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$

以上より, 

この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.
したがって, 

$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である.

$\operatorname{ord}(\eta_{3}^{3})=2$ かつ $2\nu'=\eta_{3}^{3}$ より, $4\nu'=0$ かつ $2\nu'\neq0$ である.
したがって, 

$\operatorname{ord}\left(\nu'\right) = 4$

最後に, $\pi_{6}^{3}$ の群構造を決定するために, 次の完全列を考える.

$\pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5}$

この完全性と, 左の写像が単射, 右の写像が全射であることより, 次の短完全列を得る.

$0\longrightarrow \pi_{5}^{2}\xrightarrow{E} \pi_{6}^{3}\xrightarrow{H} \pi_{6}^{5}\longrightarrow 0$

$\nu' \in \pi_{6}^{3}$

$E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である.

$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である.

以上で得た群構造, 生成元, および写像に関する結果を合わせると, 

$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$

以上より, 

この短完全列と両端の群の位数より, 中央の群の位数は $2\cdot2=4$ である.
また, $\nu'$ は中央の群に属し, $\operatorname{ord}(\nu')=4=4$ であるから, $\nu'$ は中央の群を生成する.
したがって, 

$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$