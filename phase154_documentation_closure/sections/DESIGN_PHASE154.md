<!-- PHASE154_DOCUMENTATION_CLOSURE -->
# Phase 154 設計完了記録 — Proof prose generation refinement

Phase 154 は proof provenance（証明の由来）や theorem fact（定理事実）を増やす Phase ではなく、
既存 proof graph から生成される public Narrative prose（公開証明本文）の品質を一般規則で
改善する Phase とした。

## 設計境界

ground truth は引き続き次である。

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
LiteratureReference
```

Phase 154 の prose layer はこれらを表示へ変換する presentation rule であり、

```text
proof-prose refinement
!= new theorem fact

proof-prose refinement
!= proof edge creation

proof-prose refinement
!= proof search

Reference-to-body linkage
!= Reference selection rewrite

sentence deduplication
!= provenance deletion
```

とする。

## internal fallback leakage

public Narrative に inference-rule name や statement type-name がそのまま露出する場合は、
stored semantic information から generic prose を生成する。

特に、

```text
Toda (5.6) nu_4 decomposition integration
\text{ is injective}
\text{ is exact}
```

のような internal / English representation を public prose へ残さない。

## semantic duplication

同じ semantic reason が複数の typed reason instance から同一文へ写る場合でも、
public Narrative で同じ `FINAL_RESULT_DERIVATION` 文を反復表示しない。

```text
multiple typed final reasons
→ one shared final-result prose sentence
```

これは reason sidecar の情報を削除することではない。

```text
reason provenance
→ preserved

visible duplicate sentence
→ suppressed
```

## Reference-to-proof-body linkage

Reference marker は単に独立行で

```text
[Rk]を用いる.
```

と置くのではなく、Proof graph 上で一意に対応する visible non-root consumer が存在する場合、
その consumer sentence へ接続する。

例:

```text
[R2]より, $\nu_4$ の分解写像は同型写像である.
```

root-only Reference のように一意 consumer へ結び付けられない場合は neutral use sentence を
維持する。

```text
unique graph-backed consumer
→ [Rk]より, consumer fact.

no unique safe consumer
→ [Rk]を用いる.
```

Reference selection / granularity 自体は Phase 153 の責務を維持する。

## transition / sentence composition

Argument purpose と exactness method introduction、semantic fact、Reference reuse を結合する際は、
生成元同士の punctuation contract を一致させる。

Phase 154-R6 で、

```text
そのために, 次の完全列を考える.
以上より, ...
(1) と (2) より, ...
```

へ統一した。

これにより、異なる renderer source が旧 `、` と新 `, ` を混在させたために発生する
sentence fusion failure を防ぐ。

## punctuation policy

public Narrative prose の punctuation は次で統一する。

```text
comma  = ", "
period = "."
```

ただし以下は対象外である。

```text
TeX / inline math
display math
literature title punctuation
mathematical list punctuation
```

したがって `Proposition 5.8.` の period や TeX 内部の comma を prose normalization で
変更しない。

## 112-group closure invariant

対象:

$$
n=2,\ldots,15,
\qquad
k=0,\ldots,7,
$$

depth 2 の public Narrative 112群。

Phase 154 closure invariant:

```text
render exception = 0
transition repetition = 0
semantic duplication = 0
internal fallback leakage = 0
English prose = 0
Reference linkage violation = 0
ordering violation = 0
Japanese prose punctuation violation = 0
```

最終監査:

```text
scanned groups: 112
rendered groups: 112
exceptions: 0
violations: 0

transition_repetition: 0
semantic_duplication: 0
internal_fallback_leakage: 0
english_prose: 0
reference_linkage: 0
ordering: 0
punctuation: 0
```

全112群で ASCII comma prose / ASCII period prose の双方が存在することも確認した。

## dedicated route heading audit

$\pi_8^5$ と $\pi_{15}^8$ の専用 renderer について、closure audit の substring count が

```text
## 証明対象
```

を

```text
## 証明
```

として誤検出した。

production defect ではなく audit defect であり、exact line match に変更して、

```text
## 証明対象
<
## 使用する結果
<
## 証明
```

を確認した。

この修正は audit code のみで、production renderer は変更していない。

## test-contract maintenance boundary

Phase 154 の current contract と矛盾した historical tests は test-only で更新した。

```text
Phase 149:
(1) と (2) より、 → (1) と (2) より,

Phase 150:
同一 FINAL_RESULT_DERIVATION prose の重複表示
→ public Narrative では1回

Phase 150 reason vocabulary:
、 → ,
```

production semantics を historical expectation に戻さない。

## Phase 154 完了境界

documentation closure 時点で次は完了している。

```text
focused Phase 154 regression: PASS
ordering / reason boundary regression: PASS
112-group closure audit: PASS
punctuation closure audit: PASS
```

ただし repository-wide final full regression はまだ実行していない。

したがって、

```text
documentation closure complete
!= Phase 154 final regression complete
```

とする。

Phase 154 の正式 completion は次の Phase-final full regression 後に確定する。
