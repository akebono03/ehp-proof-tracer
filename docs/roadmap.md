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
Phase 58  Toda (5.3) ν′ consequence                        COMPLETE
```

Phase 59 final regression:

```text
3177 passed in 123.99s
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
Toda (5.3) ν′ consequence
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

# 6. Phase 58：Toda (5.3) ν′ consequence

Phase 57 の Lemma 5.2 を再利用する concrete specialization。

入力:

```text
ν′∈{η₃,2ι₄,η₄}_1
```

specialization:

```text
α=η₃
i=4
β=ν′
```

Phase 50 の:

```text
π_4^3=Z/2{η₃}
```

から:

```text
2η₃=0
```

を derived にし、Lemma 5.2 specialization から:

```text
ν′∈π_6^3
H(ν′)=E²η₃
2ν′=η₃∘Eη₃∘η₅
```

を得る。

concrete η bridge:

```text
E²η₃=η₅
Eη₃=η₄
```

と generic equality / composition propagation から:

```text
ν′∈π_6^3
H(ν′)=η₅
2ν′=η₃∘η₄∘η₅
```

を導出する。

Phase 58 の分割:

```text
Phase 58-1
current η-family / bracket specialization compatibility check
COMPLETE

Phase 58-2
ν′ minimum specialization representation
COMPLETE

Phase 58-3
Lemma 5.2 specialization α=η₃
COMPLETE

Phase 58-4
H(ν′)=η₅ bridge
COMPLETE

Phase 58-5
2ν′=η₃∘η₄∘η₅ bridge
COMPLETE

Phase 58-6
provenance / representative probe / staged same-run
COMPLETE

Phase 58-7
completion
COMPLETE
```

実装原則:

```text
Phase 57 proof を再実装しない
Lemma 5.2 result を specialization する
existing η-family facts を再利用する
generic normalization を先取りしない
repeatable composition rule は one-shot で使う
```

状態:

```text
COMPLETE
```

---

# 7. Phase 59：Toda Proposition 5.3 finite-dimensional branch

Phase 59 の theorem target は Toda Proposition 5.3 の finite-dimensional result とする。

記法:

```text
η_n^2 := η_n∘η_{n+1}
```

target:

```text
π_{n+2}^n=<η_n^2>≅Z/2
(n≥2)
```

stable result:

```text
(G_2;2)=<η^2>≅Z/2
```

は Phase 59 では扱わず deferred とする。

理由:

```text
finite-dimensional branch
↓
既存 Phase 49–58 と直接接続可能

stable branch
↓
stable homotopy group model を別途要求
```

---

## Phase 59 proof dependency

Toda Proposition 5.3 の finite-dimensional proof は次の4段階に分ける。

### n=2

Toda (5.2) と Phase 50 から:

```text
η₂∘- : π_4^3 ≅ π_4^2
π_4^3=Z/2{η₃}
↓
π_4^2=Z/2{η₂∘η₃}
↓
π_4^2=Z/2{η₂^2}
```

確認事項:

```text
Toda52CompositionIsomorphismStatement から
finite-cyclic generator transport が既存表現で可能か

η₂^2 := η₂∘η₃
を既存 Composition だけで表現できるか
```

---

### n=3

EHP exact sequence:

```text
π_6^3
  --H-->
π_6^5
  --Δ-->
π_4^2
  --E-->
π_5^3
  --H-->
π_5^5
  --Δ-->
π_3^2
```

Prop.5.1 から:

```text
Δ:π_5^5→π_3^2 injective
↓ exactness
H(π_5^3)=0
↓
E:π_4^2→π_5^3 surjective
```

Phase 58 から:

```text
ν′∈π_6^3
H(ν′)=η₅
```

Prop.5.1 の:

```text
π_6^5=Z/2{η₅}
```

と合わせて:

```text
H:π_6^3→π_6^5 surjective
↓ exactness
Δ:π_6^5→π_4^2 zero
↓
E:π_4^2→π_5^3 injective
```

したがって:

```text
E:π_4^2≅π_5^3
```

さらに:

```text
Eη₂^2=η₃^2
```

から:

```text
π_5^3=Z/2{η₃^2}
```

を得る。

Phase 58 の `H(ν′)=η₅` はここで直接利用する。

---

### n=4

EHP segment:

```text
π_5^3
  --E-->
π_6^4
  -->
π_6^7
```

Toda (5.1) から:

```text
π_6^7=0
```

よって exactness から:

```text
E:π_5^3→π_6^4 surjective
```

さらに Proposition 4.4 consequence から:

```text
E:π_5^3→π_6^4 injective
```

したがって:

```text
E:π_5^3≅π_6^4
```

および:

```text
Eη₃^2=η₄^2
```

より:

```text
π_6^4=Z/2{η₄^2}
```

を得る。

---

### n>4

Toda (4.5) stable-range suspension isomorphism から:

```text
E^(n-4):
π_6^4 ≅ π_{n+2}^n
```

および:

```text
Eη_k^2=η_{k+1}^2
```

を使って generator を transport し:

```text
π_{n+2}^n=Z/2{η_n^2}
```

を得る。

---

## Phase 59 で最初に確認する compatibility

```text
A.
Phase 56 + Phase 50 から
π_4^2=Z/2{η₂^2}
を既存 rule で導けるか

B.
Prop.5.1 から
Δ:π_5^5→π_3^2 injective
を current statement で導けるか

C.
H(ν′)=η₅
+
π_6^5=Z/2{η₅}
から
H:π_6^3→π_6^5 surjective
を導けるか

D.
EHP exactness
+
H surjective
から
Δ=0
さらに
E injective
まで existing rule で届くか

E.
Toda (5.1) の
π_6^7=0
をどう current representation に入れるか

F.
Phase 48 / Prop.4.4 から
E:π_5^3→π_6^4 injective
を current instance で再利用できるか

G.
η_n^2 := η_n∘η_{n+1}
Eη_n^2=η_{n+1}^2
を existing Composition / Suspension semantics で扱えるか
```

generic square-of-eta class は先に追加しない。

まず:

```text
η_n^2
=
Composition(
  η_n,
  η_{n+1},
)
```

で十分かを確認する。

---

## Phase 59 の分割

```text
Phase 59-1
Toda Proposition 5.3 proof dependency /
current compatibility check

Phase 59-2
π_4^2=Z/2{η₂^2} from Toda (5.2)

Phase 59-3
n=3 EHP surjectivity / injectivity chain

Phase 59-4
π_5^3=Z/2{η₃^2}

Phase 59-5
n=4 suspension isomorphism

Phase 59-6
π_6^4=Z/2{η₄^2}

Phase 59-7
n>4 stable-range finite-dimensional transport

Phase 59-8
π_{n+2}^n=Z/2{η_n^2}
integration / provenance / representative probe

Phase 59-9
Phase 59 completion
```

実装原則:

```text
Phase 58 の H(ν′)=η₅ を再利用する
Phase 56 の Toda (5.2) を再利用する
Phase 45 の EHP exactness を再利用する
Phase 48 の E injectivity を再利用する
Phase 46 の Toda (4.5) を再利用する

generic η^2 class を先取りしない
generic cyclic-generator transport を先取りしない
stable (G_2;2) を Phase 59 に入れない
```

状態:

```text
COMPLETE
```

Phase 59 final capability:

```text
π_{n+2}^n=Z/2{η_n²}
(n≥2)
```

Phase 59 final regression:

```text
3177 passed in 123.99s
```

---

# 8. stable branch

Toda Proposition 5.1 の stable conclusion:

```text
(G_1;2)=Z/2{η}
```

Toda Proposition 5.3 の stable conclusion:

```text
(G_2;2)=Z/2{η^2}
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
generic concrete η normalization
global η-name normalization
unrestricted fixed-point composition closure
generic Toda-bracket specialization framework
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
| Toda (5.3) ν′ consequence | COMPLETE | 58 |
| Toda Prop.5.3 finite-dimensional branch | COMPLETE | 59 |
| stable `(G_1;2)=Z/2{η}` | DEFERRED | later |
| stable `(G_2;2)=Z/2{η^2}` | DEFERRED | later |
| stable homotopy | DEFERRED | later |
| higher Toda brackets | DEFERRED | concrete need |

---

# 13. 現在の直近ステップ

Phase 59 は COMPLETE。

次の Phase 番号と theorem target は、次の Toda source statement と proof dependency を確認してから確定する。

```text
source statement
↓
dependency analysis
↓
current representation compatibility
↓
minimum implementation
```

優先確認:

```text
Toda Proposition 5.3 直後の concrete statement / proof
Phase 59 aggregate の再利用可能性
既存 EHP / η-family / Toda bracket rule family
```

stable branch は引き続き別系統:

```text
(G_1;2)=Z/2{η}    DEFERRED
(G_2;2)=Z/2{η²}   DEFERRED
```
