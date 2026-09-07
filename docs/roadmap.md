# EHP Proof Tracer ロードマップ

この文書は今後の capability dependency と Phase 順序を記録する。

現在の仕様は `README.md` / `docs/design.md` を優先する。

---

# 1. 開発原則

```text
実際の数学的必要
↓
現在のコード / テスト互換性確認
↓
不足している最小表現
↓
最小限の定理 / fact 意味論
↓
integration
↓
applicability / provenance
↓
representative probe
↓
full regression
```

future Phase の generic framework を先取りしない。

---

# 2. 完了済み基盤

```text
Phase 1–27   generic proof / algebra / Toda bracket foundation COMPLETE
Phase 28–38  actual H / Prop.2.2 / Prop.3.1 equality branch COMPLETE
Phase 39     PrimaryComponent COMPLETE
Phase 40     TodaPrimaryGroup COMPLETE
Phase 41     PreimageSubgroup COMPLETE
Phase 42     WhiteheadProduct COMPLETE
Phase 43     Toda Lemma 4.1 premise representation COMPLETE
Phase 44     Toda Lemma 4.1 case semantics COMPLETE
Phase 45     Toda Proposition 4.2 EHP exactness COMPLETE
Phase 46     Toda (4.5) stable-range isomorphism COMPLETE
Phase 47     Toda Proposition 4.4 decomposition COMPLETE
Phase 48     Toda Proposition 4.4 E injectivity COMPLETE
```

---

# 3. 具体的低次元 branch

```text
Phase 49  π_3^2=Z{η₂}                                      COMPLETE
Phase 50  π_4^3=Z/2{η₃}                                    COMPLETE
Phase 51  Toda Proposition 5.1 dependency analysis         COMPLETE
Phase 52  Δ(ι₅)=±2η₂ direct bridge                         COMPLETE
Phase 53  Toda (4.5) finite-cyclic transport               COMPLETE
Phase 54  E^(n-3)η₃=η_n / π_{n+1}^n=Z/2{η_n}             COMPLETE
Phase 55  Toda Proposition 5.1 finite-dimensional result   COMPLETE
Phase 56  Toda (5.2) composition isomorphism               COMPLETE
Phase 57  Toda Lemma 5.2 proof integration                 COMPLETE
```

Phase 57 final regression:

```text
2997 passed in 38.45s
```

---

# 4. 現在の capability dependency

```text
Phase 49
π_3^2=Z{η₂}
↓
Phase 50
π_4^3=Z/2{η₃}
↓
Phase 52
Δ(ι₅)=±2η₂
↓
Phase 53
finite-cyclic transport
↓
Phase 54
higher η-family
↓
Phase 55
Proposition 5.1 finite-dimensional result
↓
Phase 56
Toda (5.2)
↓
Phase 57
Toda Lemma 5.2
↓
Phase 58
Toda (5.3) ν' consequence
```

---

# 5. Phase 57 完了結果

入力:

```text
α∈π_i(S^3)
2α=0
β∈{η₃,2ι₄,Eα}_1
```

導出:

```text
H(β)=E²α
2β=η₃∘Eα∘η_{i+1}
β∈π_{i+2}^3
Δ(E²α)=0
```

実装した dependency:

```text
Lemma 4.5 minimum consequence
Proposition 2.6 minimum consequence
Δ^-1(2η₂)=±ι₅ connection
Proposition 1.4 minimum consequence
Proposition 1.3 minimum consequence
Corollary 3.7 minimum consequence
Toda (2.1) minimum consequence
indeterminacy vanishing
end-to-end integration
```

---

# 6. Phase 58：Toda (5.3) ν' consequence

Phase 57 の Lemma 5.2 を再利用する concrete specialization。

入力:

```text
α=η₃∈π_4(S^3)
ν'∈{η₃,2ι₄,η₄}_1
```

Lemma 5.2 specialization から:

```text
ν'∈π_6^3
H(ν')=η₅
2ν'=η₃∘η₄∘η₅
```

を target とする。

候補分割:

```text
Phase 58-1
current η-family / bracket specialization compatibility check

Phase 58-2
ν' minimum definition / membership representation

Phase 58-3
Lemma 5.2 specialization α=η₃

Phase 58-4
H(ν')=η₅ bridge

Phase 58-5
2ν'=η₃∘η₄∘η₅ bridge

Phase 58-6
provenance / representative probe

Phase 58-7
completion
```

実装原則:

```text
Phase 57 proof を再実装しない
Lemma 5.2 result を specialization する
existing η-family facts を再利用する
generic normalization を先取りしない
```

状態:

```text
NEXT
```

---

# 7. Phase 59 以降

Phase 58 完了後は Toda 本の次の concrete consequence を優先する。

Phase 番号と対象は Phase 58 completion 時点で source dependency を再確認して確定する。

```text
source statement
↓
dependency analysis
↓
current representation compatibility
↓
minimum implementation
```

---

# 8. stable branch

Toda Proposition 5.1 の stable conclusion:

```text
(G_1;2)=Z/2{η}
```

状態:

```text
DEFERRED
```

stable homotopy group model が concrete proof branch に必要になるまで保留する。

---

# 9. 保留中の一般化

```text
general existential quantification
general witness / uniqueness framework
general inverse-map machinery
general cyclic-generator transport
generic typed map-property framework
general symbolic dimension solver
general symbolic map typing solver
general Whitehead-product algebra
general up-to-sign equality algebra
general sign variable / sign solver
general quotient simplification
general first-isomorphism theorem engine
general suspension normalization
general finite-cyclic direct-sum algebra
full Toda Proposition 1.3 formalization
full Toda Proposition 1.4 formalization
full Toda Proposition 2.6 formalization
full Corollary 3.7 formalization
generic Toda-bracket coset algebra
generic inverse-image algebra
generic Δ-H rewrite framework
stable homotopy group model
higher Toda brackets
general-purpose CAS normalization
```

方針:

```text
DEFERRED UNTIL CONCRETE NEED
```

---

# 10. 具体的結果の保存・照合・検証方針

今後、具体的ホモトピー群結果を蓄積する。

```text
concrete derived facts accumulate
↓
必要な fact schema が明確になる
↓
HomotopyFactRepository candidate
↓
既存 homotopy-group table との照合
↓
derived result verification
↓
persistent database if needed
```

repository / database を先に作って現在の proof development を妨げない。

---

# 11. 文書・コード探索方針

```text
README.md
= current capability

docs/design.md
= current architecture

docs/development_log.md
= historical Phase log

docs/roadmap.md
= future plan

docs/code_reference.md
= current code navigation
```

新規 Phase の実装前には:

```text
docs/code_reference.md
↓
関連 module を特定
↓
current code / related tests を確認
↓
最小変更
```

とする。

---

# 12. Completion table

| Capability | State | Phase |
|---|---|---:|
| generic proof / algebra foundation | COMPLETE | 1–27 |
| actual H / Prop.2.2 / Prop.3.1 equality branch | COMPLETE | 28–38 |
| PrimaryComponent | COMPLETE | 39 |
| TodaPrimaryGroup | COMPLETE | 40 |
| PreimageSubgroup | COMPLETE | 41 |
| WhiteheadProduct | COMPLETE | 42 |
| Toda Lemma 4.1 premise semantics | COMPLETE | 43 |
| Toda Lemma 4.1 case semantics | COMPLETE | 44 |
| Toda Prop.4.2 EHP exactness | COMPLETE | 45 |
| Toda (4.5) stable-range isomorphism | COMPLETE | 46 |
| Toda Prop.4.4 decomposition | COMPLETE | 47 |
| Toda Prop.4.4 E injectivity | COMPLETE | 48 |
| π_3^2=Z{η₂} | COMPLETE | 49 |
| minimum Prop.2.7 consequence | COMPLETE | 50 |
| π_4^3=Z/2{η₃} | COMPLETE | 50 |
| Prop.5.1 dependency analysis | COMPLETE | 51 |
| Δ(ι₅)=±2η₂ direct bridge | COMPLETE | 52 |
| Toda (4.5) finite-cyclic transport | COMPLETE | 53 |
| higher η-family bridge | COMPLETE | 54 |
| Prop.5.1 finite-dimensional integration | COMPLETE | 55 |
| Toda (5.2) composition isomorphism | COMPLETE | 56 |
| Toda Lemma 5.2 integration | COMPLETE | 57 |
| Toda (5.3) ν' consequence | NEXT | 58 |
| stable `(G_1;2)=Z/2{η}` | DEFERRED | later |
| stable homotopy | DEFERRED | later |
| higher Toda brackets | DEFERRED | concrete need |

---

# 13. 現在の直近ステップ

```text
Phase 58
Toda (5.3) ν' consequence
```

まず:

```text
58-1
current η-family / bracket specialization compatibility check
```

から開始する。
