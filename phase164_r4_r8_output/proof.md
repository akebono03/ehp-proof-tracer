# Backward proof narrative

## 使用する結果

**[R1] (5.3).**
$\nu'\in\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}$.
$\nu'\in\pi_{6}^{3}$.
$2\nu'=\eta_{3}\eta_{4}\eta_{5}$.
$H(\nu')=\eta_{5}$.
**[R2] (4.5).**
$n\ge k+2,\quad m\ge n\quad \Longrightarrow\quad E^{m-n}:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{m+k}^{m}$.
**[R3] Proposition 5.1.**
$\pi_{3}^{2}=\mathbb{Z}\{\eta_{2}\}$.
$H(\eta_{2})=\iota_{3}$.
$\Delta(\iota_{5})=\pm2\eta_{2}$.
$\pi_{n+1}^{n}=\mathbb{Z}/2\{\eta_{n}\}\quad(n\ge3)$.

---

## 証明

### 準備

[R1]より、$H\left(\nu'\right) = \eta_{5}$

### 単射性

[R3]より、Proposition 5.1 の $n=5$ への適用から $\pi_{6}^{5}=\mathbb{Z}/2\{\eta_{5}\}$ を得る。準備で使用した (5.3) の $H(\nu')=\eta_{5}$ と合わせると、$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射である.

$\Delta: \pi_{6}^{5} \to \pi_{4}^{2}$ は零写像である.

完全性より、$E: \pi_{4}^{2} \to \pi_{5}^{3}$ は単射である.

### 全射性

[R3]より、Proposition 5.1 の $\Delta(\iota_{5})=\pm2\eta_{2}$ と $\pi_{3}^{2}=\mathbb{Z}\{\eta_{2}\}$ を用いる。$\pi_{5}^{5}$ が $\iota_{5}$ で生成される無限巡回群であることから、$\Delta: \pi_{5}^{5} \to \pi_{3}^{2}$ は単射である.

$H: \pi_{5}^{3} \to \pi_{5}^{5}$ は零写像である.

完全性より、$E: \pi_{4}^{2} \to \pi_{5}^{3}$ は全射である.

### 結論

$E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型写像である.

□
