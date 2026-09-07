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
Phase 49
π_3^2=Z{η₂}
COMPLETE

Phase 50
π_4^3=Z/2{η₃}
COMPLETE

Phase 51
Toda Proposition 5.1 dependency analysis
COMPLETE

Phase 52
Δ(ι₅)=±2η₂ direct bridge
COMPLETE

Phase 53
Toda (4.5) finite-cyclic transport
COMPLETE

Phase 54
E^(n-3)η₃=η_n
π_{n+1}^n=Z/2{η_n}
COMPLETE

Phase 55
Toda Proposition 5.1 finite-dimensional integration / provenance
COMPLETE

Phase 56
Toda (5.2) composition isomorphism
COMPLETE
```

---

# 4. Phase 49

結果:

```text
H isomorphism
↓
η₂ = ι₃ の一意な H-preimage
↓
H(η₂)=ι₃
↓
π_3^2=Z{η₂}
```

検証:

```text
2557 passed in 56.45s
```

---

# 5. Phase 50

結果:

```text
H([ι₂,ι₂])=±2ι₃
↓
[ι₂,ι₂]=±2η₂
↓
Δ(ι₅)=±2η₂
↓
Im(Δ)=Z{2η₂}
↓
Ker(E)=Z{2η₂}
```

および:

```text
E surjective
↓
π_4^3=Z/2{Eη₂}
↓
η₃=Eη₂
↓
π_4^3=Z/2{η₃}
```

検証:

```text
2703 passed in 65.69s
```

---

# 6. Phase 51–55：Proposition 5.1 finite-dimensional branch

Phase 51 で不足 edge を:

```text
1. Δ(ι₅)=±2η₂ direct bridge
2. Toda (4.5) finite-cyclic transport
3. E^(n-3)η₃=η_n bridge
4. finite-dimensional Proposition 5.1 integration
```

に限定。

Phase 52:

```text
Δ(ι₅)=±[ι₂,ι₂]
+
[ι₂,ι₂]=±2η₂
↓
Δ(ι₅)=±2η₂
```

Phase 53:

```text
π_4^3=Z/2{η₃}
+
E^(n-3): π_4^3 ≅ π_{n+1}^n
↓
π_{n+1}^n=Z/2{E^(n-3)η₃}
```

Phase 54:

```text
η_n=E^(n-2)η₂
+
η₃=Eη₂
↓
E^(n-3)η₃=η_n
```

したがって:

```text
π_{n+1}^n=Z/2{η_n}
```

Phase 55:

```text
π_3^2=Z{η₂}        INFERENCE
H(η₂)=ι₃           INFERENCE
Δ(ι₅)=±2η₂         INFERENCE
π_{n+1}^n=Z/2{η_n} INFERENCE
↓
Toda Proposition 5.1 finite-dimensional result
```

代表値:

```text
given = 17
derived = 23
rounds = 14
fixed point = True
```

検証:

```text
2844 passed in 31.12s
```

---

# 7. Phase 56：Toda (5.2) composition isomorphism

目標:

```text
α ↦ η₂∘α :
π_i^3
≅
π_i^2
    (i≥3)
```

完了経路:

```text
Phase 56-1
Prop.4.4 / Composition / zero-group compatibility
COMPLETE

Phase 56-2
i≥3
↓
π_{i-1}^1=0
COMPLETE

Phase 56-3
Prop.4.4 n=2, α=η₂ specialization
COMPLETE

Phase 56-4
second-summand restriction
γ ↦ η₂∘γ
COMPLETE

Phase 56-5
zero first summand
+
Prop.4.4 specialization
+
second-summand restriction
↓
Toda (5.2)
COMPLETE

Phase 56-6
applicability / provenance / representative probe
COMPLETE

Phase 56-7
completion
COMPLETE
```

最終推論:

```text
i≥3
↓
π_{i-1}^1=0

η₂ definition
H(η₂)=ι₃
↓
Φ:
π_{i-1}^1 ⊕ π_i^3
≅
π_i^2

Φ|_{π_i^3}(γ)=η₂∘γ
↓
η₂∘- :
π_i^3
≅
π_i^2
```

代表値:

```text
given = 8
derived = 12
rounds = 9
fixed point = True
```

最終 provenance:

```text
π_{i-1}^1=0 is GIVEN = False
Prop.4.4 specialization is GIVEN = False
second-summand restriction is GIVEN = False
Toda (5.2) is GIVEN = False
```

検証:

```text
2910 passed in 29.17s
```

境界:

```text
no generic scalar normalization
no generic direct-sum reduction
no generic composition-map framework
no generic isomorphism-restriction theorem
no stable homotopy model
```

---

# 8. Phase 57：Toda Lemma 5.2 proof integration

次の concrete target。

入力:

```text
α∈π_i(S^3)
2α=0
β∈{η₃,2ι₄,Eα}_1
```

目標 candidate:

```text
H(β)=E²α
2β=η₃∘Eα∘η_{i+1}
β∈π_{i+2}^3
Δ(E²α)=0
```

ただし source material では:

```text
Lemma statement:
η_{i+1}

proof ending:
η_{i+2}
```

という添字不整合がある。

Phase 57-1 で原典、型、次元を確認し、development target を確定する。

---

# 9. Phase 57 proof dependency

前半:

```text
2α=0
+
Lemma 4.5
↓
2ι₃∘α=0
```

Toda bracket:

```text
{η₃,2Eι₃,Eα}_1
```

Hopf branch:

```text
Proposition 2.6
↓
H(β) ∈ Δ^-1(η₂∘2ι₃) ∘ E²α

η₂∘2ι₃=2η₂
+
Δ(ι₅)=±2η₂
↓
Δ^-1(2η₂)=±ι₅
↓
H(β)=E²α
```

`2β` branch candidate:

```text
2β
∈ 2{η₃,2ι₄,Eα}_1
=
{η₃,2ι₄,Eα}_1∘2ι_{i+2}
↓ Proposition 1.4
η₃∘E{2ι₃,α,2ι_i}
↓ Proposition 1.3
η₃∘-{2ι₄,Eα,2ι_{i+1}}
↓ Corollary 3.7
η₃∘-(Eα∘η_{i+1})
```

indeterminacy vanishing candidate:

```text
γ∈π_{i+2}(S^4)
↓ (2.1)
E(η₃∘γ∘2ι_{i+2})
=η₄∘2Eγ
=2η₄∘Eγ
=0
↓ Lemma 4.5
η₃∘γ∘2ι_{i+2}=0
```

最後:

```text
H(β)=E²α
↓
Δ(E²α)=Δ(H(β))=0
```

---

# 10. Phase 57 candidate 分割

```text
Phase 57-1
Lemma 5.2 statement / proof index / typing compatibility check

Phase 57-2
Lemma 4.5 minimum consequence needed for 2ι₃∘α=0

Phase 57-3
Proposition 2.6 minimum Hopf-invariant Toda-bracket consequence

Phase 57-4
Δ^-1(2η₂)=±ι₅ connection using independently derived Δ relation

Phase 57-5
Proposition 1.4 / Proposition 1.3 / Corollary 3.7 minimum bracket transformation chain

Phase 57-6
(2.1) + Lemma 4.5 indeterminacy-vanishing bridge

Phase 57-7
Lemma 5.2 end-to-end integration / provenance / representative probe

Phase 57-8
completion
```

実装原則:

```text
use only minimum consequences actually appearing in this proof
no full Prop.1.3 / Prop.1.4 / Prop.2.6 / Cor.3.7 formalization unless required
no generic Toda-bracket CAS normalization
no generic coset algebra unless concrete need forces it
no stable homotopy model
```

状態:

```text
NEXT
```

---

# 11. Phase 58：Toda (5.3) ν' consequence

Phase 57 完了後。

入力:

```text
α=η₃∈π_4(S^3)
2ι₃∘η₃=0
ν'∈{η₃,2ι₄,η₄}_1
```

Lemma 5.2 specialization から:

```text
ν'∈π_6^3
H(ν')=η₅
2ν'=η₃∘η₄∘η₅
```

を target とする。

候補:

```text
58-1 current η-family / bracket specialization compatibility check
58-2 ν' minimum definition / membership representation
58-3 Lemma 5.2 specialization α=η₃
58-4 H(ν')=η₅ bridge
58-5 2ν'=η₃∘η₄∘η₅ bridge
58-6 provenance / representative probe
58-7 completion
```

Phase 58 では Lemma 5.2 proof を再実装しない。

---

# 12. 直近の capability dependency

```text
Phase 55
Prop.5.1 finite-dimensional integration
COMPLETE
↓
Phase 56
Toda (5.2) composition isomorphism
COMPLETE
↓
Phase 57
Toda Lemma 5.2 proof integration
NEXT
↓
Phase 58
Toda (5.3) ν' consequence
PLANNED
```

Phase 57 dependency:

```text
Lemma 4.5
Proposition 2.6
Proposition 1.4
Proposition 1.3
Corollary 3.7
(2.1)
```

---

# 13. 保留中の一般化

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
general iterated-suspension composition algebra
general scalar normalization
general finite-cyclic direct-sum algebra
generic direct-sum reduction
generic composition-map framework
generic isomorphism restriction
full Toda Proposition 2.7 formalization
stable homotopy group model
higher Toda brackets
general-purpose CAS normalization
```

---

# 14. Completion table

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
| π_{n+1}^n=Z/2{η_n} | COMPLETE | 54 |
| Prop.5.1 finite-dimensional integration / provenance | COMPLETE | 55 |
| Toda (5.2) composition isomorphism | COMPLETE | 56 |
| Toda Lemma 5.2 | NEXT | 57 |
| Toda (5.3) ν' consequence | PLANNED | 58 |
| Prop.5.1 stable `(G_1;2)` conclusion | DEFERRED | later |
| stable homotopy | PLANNED | later |
| higher Toda brackets | DEFERRED | concrete need |

---

# 15. 現在 independently derived できる結果

```text
π_3^2=Z{η₂}
H(η₂)=ι₃
π_4^3=Z/2{η₃}
Δ(ι₅)=±2η₂
π_{n+1}^n=Z/2{η_n}
Toda Proposition 5.1 finite-dimensional result
η₂∘- : π_i^3 ≅ π_i^2  (i≥3)
```

---

# 16. 具体的結果の保存・照合・検証方針

具体的結果を将来 repository / database 化し、既存 table と照合する方向は維持する。

基本:

```text
定理・推論ルール
↓
推論された concrete fact
↓
fact repository
↓
existing table lookup
↓
comparison
```

区別:

```text
推論エンジン
!=
fact repository
!=
既存 table
```

table に記載されていることと proof により導出されたことを区別する。

---

# 17. Fact source candidate

```text
LITERATURE_FACT
TABLE_FACT
USER_IMPORTED_FACT
DERIVED_FACT
```

保存候補:

```text
result
source / provenance
premises
used inference rules
proof trace
```

既存の `ProofStep` provenance を可能な限り再利用する。

---

# 18. Table verification candidate

比較状態候補:

```text
MATCH
PARTIAL_MATCH
CONFLICT
NO_ENTRY
NOT_DERIVED
```

将来の verification status 候補:

```text
VERIFIED
DERIVABLE
CONSISTENT_BUT_NOT_DERIVED
PARTIALLY_VERIFIED
CONFLICT
UNKNOWN
```

重要:

```text
UNKNOWN != FALSE
```

---

# 19. Repository / database 導入時期

database first にはしない。

```text
concrete calculations
↓
common fact schema
↓
repository interface
↓
persistent storage if needed
```

具体的結果をさらに蓄積し、必要 schema が明確になってから実装する。

---

# 20. 将来 backlog

具体的必要が出るまで保留:

```text
Lemma 1.1
Proposition 1.2
Proposition 1.3 の未使用部分
Proposition 1.5
Proposition 1.6
Proposition 2.3
Proposition 2.5 の 2-primary case
Lemma 4.3
```

Phase 57 で具体的必要が発生済み:

```text
Proposition 1.4
Proposition 1.3
(2.1)
Proposition 2.6
Corollary 3.7
Lemma 4.5
```

これらは full formalization ではなく Phase 57 proof に必要な minimum consequence から実装する。
