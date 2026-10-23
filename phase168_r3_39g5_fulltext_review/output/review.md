# Phase 168 R3-39G-5 — 全文差分精査

読み取り専用。自動判定は文章上の出現・順序・引用整合性に限り、数学的同等性を保証しません。

| 対象 | 説明項目 | 本文アンカー | Reference 条件 | 引用参照 | 残存差分ブロック |
|---|---:|---:|---:|---|---:|
| pi3_2 | 4/4 | 7/7 | 2/2 | OK | 4 |
| pi4_3 | 4/4 | 8/8 | 2/2 | OK | 6 |
| pi5_4 | 4/4 | 5/5 | 3/3 | OK | 3 |

## pi3_2

- 確認: circle specialization
- 確認: Hopf injective
- 確認: suspension of identity
- 確認: delta vanishes by exactness
- 確認: Hopf isomorphism by bijectivity
- 確認: Hopf generator image
- 確認: conclusion
- 確認: circle dimension restriction
- 確認: diagonal dimension restriction
- 確認: proof_starts_with_source_group
- 確認: no_unrestricted_circle_formula_in_proof
- 確認: final_conclusion_once

### unaligned_reference_blocks

**ブロック 1: replace**

固定基準:
```text
[R1] (5.1).
\pi_{i}^{1} = 0\quad(i > 1).
```
現行出力:
```text
**[R1] (5.1).**
$\pi_i^1=0\quad(i>1)$.
```

**ブロック 2: replace**

固定基準:
```text
[R2] Proposition 5.1.
```
現行出力:
```text
**[R2] Proposition 4.2 (4.4).**
Proposition 4.2 により, EHP の列 $\pi_i^n\xrightarrow{E}\pi_{i+1}^{n+1}\xrightarrow{H}\pi_{i+1}^{2n+1}\xrightarrow{\Delta}\pi_{i-1}^{n}\xrightarrow{E}\pi_i^{n+1}$ は完全である.
**[R3] Foundational: suspension identity.**
$E(\iota_{1})=\iota_{2}$.
**[R4] Proposition 5.1.**
```


### unaligned_proof_blocks

**ブロック 1: replace**

固定基準:
```text
\pi_{3}^{2} の群構造を決定するために, 次の完全列を考える.
```
現行出力:
```text
群構造を決定するために, 次の完全列を考える.
```

**ブロック 2: replace**

固定基準:
```text
[R1]より, \pi_{2}^{1} = 0.
完全性より, H: \pi_{3}^{2} \to \pi_{3}^{3} は単射.
[R1]より, \pi_{1}^{1} = \mathbb{Z}\{\iota_{1}\}.
[R1]より, \pi_{2}^{2} = \mathbb{Z}\{\iota_{2}\}.
E(\iota_{1}) = \iota_{2}.
これより, E: \pi_{1}^{1} \to \pi_{2}^{2} は同型.
完全性より, \operatorname{Im}Δ=\ker E=0 なので, \Delta: \pi_{3}^{3} \to \pi_{1}^{1} は零写像.
完全性より, H: \pi_{3}^{2} \to \pi_{3}^{3} は全射.
単射性と全射性より, H: \pi_{3}^{2} \to \pi_{3}^{3} は同型.
[R1]より, \pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}.
[R2]より, H(\eta_{2}) = \iota_{3}.
以上より, \pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}.
```
現行出力:
```text
導出により, $\pi_{2}^{1} = 0$ を得る.
完全性より, $H: \pi_{3}^{2}\to \pi_{3}^{3}$ は単射である.
[R1]より, $\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}$ を得る.
導出により, $\pi_{1}^{1} = \mathbb{Z}\{\iota_{1}\}$ を得る.
導出により, $\pi_{2}^{2} = \mathbb{Z}\{\iota_{2}\}$ を得る.
[R3]より, $E(\iota_{1})=\iota_{2}$.
$E: \pi_{1}^{1}\to \pi_{2}^{2}$ は同型.
完全性より, $\operatorname{Im}\Delta=\ker E=0$ なので, $\Delta: \pi_{3}^{3}\to \pi_{1}^{1}$ は零写像である.
完全性より, $H: \pi_{3}^{2}\to \pi_{3}^{3}$ は全射である.
単射性と全射性より, $H: \pi_{3}^{2}\to \pi_{3}^{3}$ は同型である.
導出により, $\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}$ を得る.
[R4]より, $H(\eta_{2})=\iota_{3}$.
以上より, $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$ を得る.
```


## pi4_3

- 確認: suspended eta
- 確認: delta generator
- 確認: delta image
- 確認: kernel
- 確認: vanishing target
- 確認: E surjective by exactness
- 確認: quotient
- 確認: conclusion
- 確認: diagonal dimension restriction
- 確認: below diagonal restriction
- 確認: proof_starts_with_source_group
- 確認: no_unrestricted_circle_formula_in_proof
- 確認: final_conclusion_once

### unaligned_reference_blocks

**ブロック 1: replace**

固定基準:
```text
[R1] (5.1).
\pi_{i}^{n} = 0\quad(i < n).
```
現行出力:
```text
**[R1] Chapter V, i) The Groups pi^(n)_(n+1), eta-family notation.**
$n\ge 2$ に対し, $\eta_n=E^{n-2}\eta_2$ と定義する.
**[R2] (5.1).**
```

**ブロック 2: replace**

固定基準:
```text
[R2] Proposition 5.1.
```
現行出力:
```text
$\pi_i^n=0\quad(i<n)$.
**[R3] Proposition 5.1.**
$\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$.
```

**ブロック 3: replace**

固定基準:
```text
\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}.
```
現行出力:
```text
**[R4] Proposition 4.2 (4.4).**
Proposition 4.2 により, EHP の列 $\pi_i^n\xrightarrow{E}\pi_{i+1}^{n+1}\xrightarrow{H}\pi_{i+1}^{2n+1}\xrightarrow{\Delta}\pi_{i-1}^{n}\xrightarrow{E}\pi_i^{n+1}$ は完全である.
```


### unaligned_proof_blocks

**ブロック 1: replace**

固定基準:
```text
\pi_{4}^{3} の群構造を決定するために, 次の完全列を考える.
```
現行出力:
```text
群構造を決定するために, 次の完全列を考える.
```

**ブロック 2: replace**

固定基準:
```text
[R1]より, \pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}.
これより, \pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}.
[R2]より, \Delta(\iota_{5}) = \pm 2\eta_{2}.
```
現行出力:
```text
[R2]より, $\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}$ を得る.
導出により, $\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}$ を得る.
[R3]より, $\Delta\left(\iota_{5}\right) = \pm 2\eta_{2}$ を得る.
```

**ブロック 3: replace**

固定基準:
```text
完全性より, \ker E=\mathbb{Z}\{2η_{2}\}.
\pi_{4}^{5} = 0.
完全性より, E: \pi_{3}^{2} \to \pi_{4}^{3} は全射.
[R2]より, \pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}.
全射性と核の決定から, 準同型定理より \pi_{4}^{3}\cong \pi_{3}^{2}/\mathbb{Z}\{2η_{2}\}.
以上より, \pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}.
```
現行出力:
```text
完全性より, $\operatorname{Im}\Delta=\ker E$ が成り立つ.
完全性より, $\ker E=\mathbb{Z}\{2\eta_{2}\}$.
導出により, $\pi_{4}^{5} = 0$ を得る.
完全性より, $E: \pi_{3}^{2}\to \pi_{4}^{3}$ は全射である.
[R3]より, $\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}$ を得る.
全射性と核の決定から, 準同型定理より $\pi_{4}^{3}\cong \pi_{3}^{2}/\mathbb{Z}\{2\eta_{2}\}$.
以上より, $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ を得る.
```


## pi5_4

- 確認: source group
- 確認: Toda 4.5 substitution
- 確認: specific isomorphism
- 確認: generator image
- 確認: conclusion
- 確認: Toda stable-range restriction
- 確認: Toda suspension-domain restriction
- 確認: Toda nonnegative stem restriction
- 確認: proof_starts_with_source_group
- 確認: no_unrestricted_circle_formula_in_proof
- 確認: final_conclusion_once
- 確認: toda45_argument_order
- 確認: toda45_citation_on_substitution_line

### unaligned_reference_blocks

**ブロック 1: replace**

固定基準:
```text
[R1] (4.5).
n \ge k + 2 のとき, E^{m-n}: \pi_{n+k}^{n} \to \pi_{m+k}^{m} は同型.
[R2] Proposition 5.1.
```
現行出力:
```text
**[R1] Chapter V, i) The Groups pi^(n)_(n+1), eta-family notation.**
$n\ge 2$ に対し, $\eta_n=E^{n-2}\eta_2$ と定義する.
**[R2] Proposition 5.1.**
```

**ブロック 2: insert**

固定基準:
```text
(なし)
```
現行出力:
```text
**[R3] (4.5).**
$n\ge k+2$, $m\ge n$, $k\ge0$ に対し, $E^{m-n}:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{m+k}^{m}$ が成り立つ.
```


### unaligned_proof_blocks

**ブロック 1: replace**

固定基準:
```text
\pi_{5}^{4} の群構造を決定する.
[R2]より, \pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}.
[R1]を (n,m,k)=(3,4,1) に適用すると, E: \pi_{4}^{3} \to \pi_{5}^{4} は同型.
E\eta_{3} = \eta_{4}.
以上より, \pi_{5}^{4} = \mathbb{Z}/2\{\eta_{4}\}.
```
現行出力:
```text
[R2]より, $\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$ を得る.
[R3]を $(n,m,k)=(3,4,1)$ に適用すると, $E: \pi_{4}^{3}\to \pi_{5}^{4}$ は同型である.
$E(\eta_{3})=\eta_{4}$.
導出により, $\pi_{5}^{4} = \mathbb{Z}/2\{E\eta_{3}\}$ を得る.
以上より, $\pi_{5}^{4} = \mathbb{Z}/2\{\eta_{4}\}$ を得る.
```


## 判定上の注意

- Reference の番号・一覧は固定基準に含まれないため、番号の違い自体は不合格としない。
- 数式の `$` や空白の差は数式の同等性を保証しない。
- 残存差分は上の各ブロックを原文と照合し、論証内容・順序・詳しさを人手で確認する。
- 旧 Renderer・群専用固定文章は使用しない。
- プロジェクトの実装ファイルおよび固定基準は変更しない。
- Phase 終了まで全体 pytest は実行しない。
