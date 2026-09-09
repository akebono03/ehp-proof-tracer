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
Phase 59  Toda Proposition 5.3 finite-dimensional result   COMPLETE
Phase 60  Toda Lemma 5.4 / ν₄ construction                COMPLETE
Phase 61  Toda Lemma 5.5 bracket transport                 COMPLETE
Phase 62  Toda (5.5) finite-dimensional ν-family           COMPLETE
Phase 63  Toda (5.6) ν₄ decomposition                         COMPLETE
Phase 64  performance stabilization                           COMPLETE
Phase 65  Toda Proposition 5.6 finite-dimensional result      COMPLETE
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


# 8. Phase 60：Toda Lemma 5.4 / ν₄ construction

Toda Lemma 5.4 の target:

```text
ν₄∈π_7^4
H(ν₄)=ι₇
2Eν₄=E²ν′
```

Phase 58 の:

```text
ν′∈π_6^3
H(ν′)=η₅
2ν′=η₃∘η₄∘η₅
```

Phase 59 の:

```text
π_{n+2}^n=Z/2{η_n²}
(n≥2)
```

を主要 dependency として再利用する。

---

## Phase 60 proof dependency

Lemma 5.4 の証明は次の branch に分ける。

### A. Theorem 3.6 specialization

Theorem 3.6 を:

```text
α=η₂
β=2ι₃
t=1
```

に specialization する。

前提:

```text
2η₆=0
2ι₃∘Eη₂=2η₃=0
```

から、ある:

```text
α*∈π_7^4
```

が存在して:

```text
2Eα*
∈
-{η₅,2ι₆,η₆}_3
```

を得る。

---

### B. Toda (5.4)

新しい主要中間結果:

```text
{η_n,2ι_{n+1},η_{n+1}}_t
=
{E^(n-3)ν′,-E^(n-3)ν′}
```

scope:

```text
n≥3
t≤n-2
```

まず:

```text
t≥1
```

を扱う。

Toda bracket の indeterminacy は:

```text
η_n∘π_{n+3}^{n+1}
+
π_{n+2}^n∘η_{n+2}
```

である。

Toda (4.7)、Proposition 5.3、Toda (5.3) から:

```text
η_n∘π_{n+3}^{n+1}
+
π_{n+2}^n∘η_{n+2}
=
<η_n∘η_{n+1}∘η_{n+2}>
=
<2E^(n-3)ν′>
```

を得る。

さらに ν′ の bracket definition、Proposition 1.3、Toda (1.15) から:

```text
E^(n-3)ν′
∈
{η_n,2ι_{n+1},η_{n+1}}_t
```

を示し、Toda (5.4) を得る。

---

### C. t=0 bridge

Toda (3.2) の:

```text
π_{n+3}(S^{n+1})
=
Eπ_{n+2}(S^n)
```

を使う。

その結果:

```text
{η_n,2ι_{n+1},η_{n+1}}_1
```

と:

```text
{η_n,2ι_{n+1},η_{n+1}}
```

は同じ indeterminacy group の coset になる。

Toda (1.15) から両 bracket を一致させ、`t=0` の Toda (5.4) を得る。

---

### D. α* consequence

Toda (5.4) の:

```text
n=5
t=3
```

から:

```text
2Eα*=±E²ν′
```

を得る。

---

### E. Hopf invariant parity

Phase 58 の:

```text
H(ν′)=η₅
```

と:

```text
π_6^5=Z/2{η₅}
```

から、ν′ は 2 で割れない。

一方:

```text
2Eα*=±E²ν′
```

から `E²ν′` は 2 で割れる。

Toda (4.8) から:

```text
H(α*)=(2s+1)ι₇
```

を得る。

---

### F. Whitehead correction

Whitehead product に対して:

```text
H[ι₄,ι₄]=(-1)^u 2ι₇
```

を使う。

`2Eα*` の sign に応じて:

```text
ν₄
=
α* - (-1)^u s[ι₄,ι₄]
```

または:

```text
ν₄
=
-α* + (-1)^u(s+1)[ι₄,ι₄]
```

と定義する。

`E[ι₄,ι₄]=0` と Hopf invariant correction から:

```text
H(ν₄)=ι₇
2Eν₄=E²ν′
```

を得る。

---

## Phase 60 の分割

```text
Phase 60-1
Lemma 5.4 dependency / current compatibility analysis

Phase 60-2
Toda (5.4) bracket statement / minimum value-set semantics

Phase 60-3
Toda (5.4) t≥1 indeterminacy calculation
using Toda (4.7), Prop.5.3, Toda (5.3)

Phase 60-4
E^(n-3)ν′ bracket inclusion
using ν′ definition, Prop.1.3, Toda (1.15)

Phase 60-5
t=0 bridge
using Toda (3.2) and Toda (1.15)

Phase 60-6
Theorem 3.6 specialization
α=η₂, β=2ι₃, t=1
↓
2Eα*=±E²ν′

Phase 60-7
Hopf invariant / parity consequence
H(α*)=(2s+1)ι₇

Phase 60-8
Whitehead correction / ν₄ construction

Phase 60-9
Lemma 5.4 integration / provenance

Phase 60-10
representative probe / full regression

Phase 60-11
Phase 60 completion
```

実装原則:

```text
Phase 58 ν′ result を再利用する
Phase 59 Prop.5.3 result を再利用する
existing WhiteheadProduct representation を再利用する
generic Toda-bracket coset algebra を先取りしない
general witness framework を先取りしない
general sign solver を先取りしない
Lemma 5.5 を Phase 60 に入れない
```

状態:

```text
COMPLETE
```

---

## Phase 60 completion result

完成:

```text
Toda (5.4) t≥1 up-to-sign bracket value
Toda (5.4) t=0 bridge
Theorem 3.6 specialization
α*∈π_7^4
2Eα*=±E²ν′
H(α*)=(2s+1)ι₇
Whitehead correction branches
ν₄∈π_7^4
H(ν₄)=ι₇
2Eν₄=E²ν′
TodaLemma54Statement
LiteratureStatement
reference statement display
Used in display
Proof-style derivation display
representative probe
```

final regression:

```text
3334 passed in 132.72s
```

Phase 60 では generic Toda-bracket coset algebra、generic sign solver、generic divisibility framework、generic witness framework、generic Whitehead correction algebraを導入しなかった。


---

# 9. Phase 61：Toda Lemma 5.5 bracket transport

Lemma 5.5 target:

```text
β∈π_{t+2}(S^m)
β∘η_{t+2}=0
t>0
↓
{η_{m+2},E³β,η_{t+5}}_3
contains
±(E²β∘E^tν₄)
```

proof dependency:

```text
Phase 60 Lemma 5.4 α* / ν₄ provenance
+
Lemma 5.5 hypotheses
↓
±(E²β∘E^tα*) bracket inclusion
+
E[ι₄,ι₄]=0
↓
E^tν₄=±E^tα*
↓
±(E²β∘E^tν₄) bracket inclusion
```

Phase 61 では Lemma 5.4 provenance を再利用し、α* / ν₄ proof を再実装しない。

## Phase 61 分割

```text
Phase 61-1
statement / dependency / current compatibility analysis
COMPLETE

Phase 61-2
minimum contains-up-to-sign statement semantics
COMPLETE

Phase 61-3
α* bracket inclusion consequence
COMPLETE

Phase 61-4
ν₄ suspension correction bridge
COMPLETE

Phase 61-5
α* → ν₄ composition bridge
COMPLETE

Phase 61-6
Lemma 5.5 final aggregate / literature provenance
COMPLETE

Phase 61-7
applicability / acyclic provenance regression
COMPLETE

Phase 61-8
representative proof-style probe
COMPLETE

Phase 61-9
completion documentation / final full regression record
IMPLEMENTATION COMPLETE
```

## Phase 61 completion result

完成:

```text
TodaLemma55BracketContainsUpToSignStatement
TodaLemma55SuspensionUpToSignStatement
TodaLemma55Statement
α* bracket inclusion
E^tν₄=±E^tα*
α*→ν₄ composition bridge
final bracket inclusion
literature-aware final aggregate
Phase 60 inherited literature
wrong-instance rejection
GIVEN / INFERENCE boundary regression
acyclic provenance regression
proof-style representative probe
```

verified probe result:

```text
{η_(m+2), E³β, η_(t+5)}_3
contains
±(E²β∘E^tν₄)
```

focused Phase 61 tests:

```text
8 + 13 + 16 + 14 + 20 + 15 + 16 passed
```

final repository-wide regression count:

```text
TO RECORD AFTER: python -m pytest -q
```

Phase 61 では generic bracket containment algebra、generic sign solver、generic up-to-sign transitivity、generic Whitehead correction algebra、full Theorem 3.6 formalizationを導入しなかった。

状態:

```text
COMPLETE (implementation / focused regression)
```

---

# 10. Phase 62：ν-family / Toda (5.5)

定義:

```text
ν_n:=E^(n-4)ν₄
(n≥4)

ν:=E^∞ν₄
```

および:

```text
η_n³:=η_n∘η_{n+1}∘η_{n+2}
(n≥2)

η³:=η∘η∘η
```

Toda (5.5) target:

```text
n≥5:
2ν_n=E^(n-3)ν′

4ν_n=η_n³

4ν=η³
```

主要 dependency:

```text
Lemma 5.4
+
Proposition 5.3
+
Phase 58 Toda (5.3)
+
η-family transport
```

Phase 62 では finite-dimensional `ν_n` branch を優先し、stable `ν` / `η³` に stable homotopy model が必要なら separate deferred boundary とする。

completion result:

```text
ν_n:=E^(n-4)ν₄
(n≥4)

n≥5:
2ν_n=E^(n-3)ν′
4ν_n=η_n³
```

aggregate:

```text
Toda55NuFamilyFiniteDimensionalStatement
```

representative probe:

```powershell
python -m probes.probe_phase62_capabilities
```

final regression:

```text
3550 passed in 411.22s
```

stable `ν:=E^∞ν₄` / `4ν=η³` は deferred。

状態:

```text
COMPLETE
```

---

# 11. Phase 63：Toda (5.6) Proposition 4.4 decomposition with ν₄

Toda (5.6) target:

```text
(α,β)
↦
Eα+ν₄∘β
```

が:

```text
π_{i-1}^3 ⊕ π_i^7
≅
π_i^4
```

を与える。

主要 dependency:

```text
Proposition 4.4 decomposition semantics
+
Lemma 5.4
H(ν₄)=ι₇
```

Phase 47 の decomposition infrastructure を再利用する。

実装原則:

```text
generic direct-sum decomposition framework を拡張しない
ν₄ specialization に必要な minimum bridge のみ追加する
```

状態:

```text
COMPLETE
```

---

# 12. stable branch

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

# 14. 将来：proof narrative generation

Phase 60 で proof-style derivation を representative probe に追加した。

current state:

```text
proof inference        = automatic
proof provenance       = automatic
literature metadata    = structured
Used in display        = probe-local mapping
proof-style narrative  = hand-authored probe presentation
```

したがって、まだ「ProofStep graph から証明本文を自動生成」しているわけではない。

将来 target:

```text
ProofStep graph
+ Expression tree
+ InferenceRule provenance
+ LiteratureStatement
↓
relevant dependency path extraction
↓
proof-step grouping / compression
↓
equation-chain generation
↓
automatic citation insertion
↓
rule-specific narrative templates
↓
natural-language connectors
↓
console / Markdown / LaTeX proof output
```

具体例として Phase 60-4 の:

```text
E^(n-3)ν′
∈ E^(n-3){η₃,2ι₄,η₄}_1
⊂ (-1)^(n-3){η_n,2ι_(n+1),η_(n+1)}_(n-2)
⊂ (-1)^(n-3){η_n,2ι_(n+1),η_(n+1)}_t
```

を、将来は current proof objects と citation metadata から組み立てる。

必要になる可能性のある schema:

```text
ProofDisplayStep / equivalent presentation metadata
premise role
conclusion role
equation rendering hint
citation role
narrative template
compression / omission hint
```

ただし generic proof narrative framework は今すぐ実装しない。

導入条件:

```text
Phase 61 以降の concrete proofs を蓄積
↓
同じ presentation pattern が複数回現れる
↓
必要 metadata が安定
↓
manual probe derivation から generic generator へ抽象化
```

状態:

```text
PLANNED / DEFERRED UNTIL DISPLAY SCHEMA STABILIZES
```

---

# 15. 具体的結果の保存・照合・検証方針

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

# 16. 文書・コード探索方針

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

# 17. Completion table

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
| Toda Lemma 5.4 / ν₄ construction | COMPLETE | 60 |
| Toda Lemma 5.5 bracket transport | COMPLETE | 61 |
| ν-family / Toda (5.5) finite-dimensional | COMPLETE | 62 |
| Toda (5.6) ν₄ decomposition | COMPLETE | 63 |
| performance stabilization | COMPLETE | 64 |
| automatic proof narrative generation | PLANNED / DEFERRED | later |
| stable `(G_1;2)=Z/2{η}` | DEFERRED | later |
| stable `(G_2;2)=Z/2{η^2}` | DEFERRED | later |
| stable homotopy | DEFERRED | later |
| higher Toda brackets | DEFERRED | concrete need |

---

# 18. Phase 62 completion 時点の直近ステップ（履歴）

Phase 62 は COMPLETE。

現在の verified capability:

```text
ν_n:=E^(n-4)ν₄
(n≥4)

n≥5:
2ν_n=E^(n-3)ν′
4ν_n=η_n³
```

representative probe:

```powershell
python -m probes.probe_phase62_capabilities
```

final repository-wide regression:

```text
3550 passed in 411.22s
```

次は:

```text
Phase 63-1
Toda (5.6)
Prop.4.4 n=4 / ν₄
current representation / dependency compatibility analysis
```

最初に確認する dependency:

```text
A.
Phase 47 の Toda Proposition 4.4 decomposition statement / map が
n=4 specialization を structural に保持できるか

B.
Phase 60 の derived H(ν₄)=ι₇ を
Prop.4.4 の H(α)=±ι_(2n-1) premise に接続できるか

C.
n=4 の domain:
π_(i-1)^3 ⊕ π_i^7
を existing DirectSumGroup / TodaPrimaryGroup でそのまま表せるか

D.
map formula:
(α,β)↦Eα+ν₄∘β
を existing Sum / Suspension / Composition で表せるか

E.
Toda (5.6) 専用 specialization だけで十分か、
追加の generic decomposition machinery が本当に必要か
```

generic specialization engine、generic direct-sum simplifier、stable ν / η³、automatic proof narrative generation は引き続き deferred とする。



---

# 19. Phase 63：Toda (5.6) ν₄ decomposition 完了

target:

```text
(α,β)
↦
Eα+ν₄∘β
:
π_{i-1}^3 ⊕ π_i^7
≅
π_i^4
```

実装 dependency:

```text
Phase 47
Toda Proposition 4.4 decomposition
+
Phase 60
Toda Lemma 5.4
ν₄∈π_7^4
H(ν₄)=ι₇
↓
Phase 63-2
n=4 / α=ν₄ specialization bridge
↓
Phase 63-3
concrete Proposition 4.4 decomposition specialization
↓
Phase 63-4
Toda (5.6) isomorphism semantics
↓
Phase 63-5
applicability / provenance regression
↓
Phase 63-6
literature-aware aggregate
↓
Phase 63-7
representative proof-style probe
```

最終 capability:

```text
π_(i-1)^3 ⊕ π_i^7
≅
π_i^4

(α,β)↦Eα+ν₄∘β
```

provenance boundary:

```text
theorem dependency = INFERENCE
TodaProp44DecompositionMap = GIVEN
```

literature:

```text
direct:
Toda (5.6), Equation (5.6)

inherited:
Toda Lemma 5.4 / Phase 60 literature
```

representative probe:

```powershell
python -m probes.probe_phase63_capabilities
```

focused tests:

```text
test_phase63_nu4_prop44_specialization.py              15 passed
test_phase63_prop44_decomposition_specialization.py    19 passed
test_phase63_toda56_semantics.py                       17 passed
test_phase63_applicability_provenance.py               20 passed
test_phase63_toda56_integration.py                     19 passed
test_phase63_probe.py                                  17 passed
```

final repository-wide regression:

```text
3657 passed in 939.47s
```

状態:

```text
COMPLETE
```

---


# 20. Phase 64：performance stabilization 完了

Phase 64 は Phase 63 の数学 capability を変更せず、regression performance を安定化する maintenance Phase とした。

same-machine baseline:

```text
3657 passed in 259.11s
```

final:

```text
3657 passed in 29.97s
```

約 88.4% 短縮。

主要施策:

```text
deterministic no-arg builder caching
inference premise-binding rematch elimination
algebra exhaustive crosscheck local precomputation
```

coverage:

```text
3657 tests unchanged
algebra exhaustive case ranges unchanged
checked-count thresholds unchanged
```

未導入:

```text
agenda/worklist
premise-type indexing
global proof cache
global GroupMap cache
SNF/HNF replacement
coverage reduction
new Toda theorem semantics
```

状態:

```text
COMPLETE
```

---

---

# 21. Phase 65：Toda Proposition 5.6 finite-dimensional result 完了

Phase 65 final capability:

```text
π_5^2=Z/2{η₂³}
π_6^3=Z/4{ν′}
π_7^4=Z{ν₄}⊕Z/4{Eν′}
π_(n+3)^n=Z/8{ν_n}
(n≥5)
```

dependency:

```text
Phase 58 ν′
Phase 59 η²
Phase 60 ν₄
Phase 62 Toda (5.5)
Phase 63 Toda (5.6)
Phase 46 Toda (4.5)
↓
Phase 65 finite-dimensional Proposition 5.6
```

subphases:

```text
65-1 dependency / compatibility                 COMPLETE
65-2 π_5^2=Z/2{η₂³}                            COMPLETE
65-3 Equation (5.7) / E injectivity             COMPLETE
65-4 ord(ν′)=4 / π_6^3                         COMPLETE
65-5 π_7^4 decomposition                        COMPLETE
65-6 π_8^5 quotient / E² injectivity            COMPLETE
65-7 ord(ν₅)=8 / π_8^5                         COMPLETE
65-8 Toda (4.5) n≥6 transport                   COMPLETE
65-9 Proposition 5.6 aggregate                  COMPLETE
65-10 proof-style probe / provenance regression COMPLETE
65-11 completion documentation                  COMPLETE
```

final regression:

```text
3841 passed in 31.82s
```

---

# 22. 現在の推論能力と次の目標

current engine:

```text
facts / hypotheses
+
formalized inference rules
↓
automatic premise matching
↓
automatic rule application
↓
derived ProofStep graph
↓
final conclusion
```

現在は「Toda の証明順を表示するだけ」ではない。

ただし:

```text
goal
↓
必要 theorem を自動選択
↓
proof strategy を自動発見
```

まで一般化されてはいない。

当面は concrete Toda calculations を進め、証明戦略に必要な rule pattern を蓄積する。

---

# 23. Proof Repository / Derived Fact Database milestone

現在:

```text
ProofStep provenance
= 実行中に保持

@lru_cache
= 同一 Python process 内の deterministic builder 再利用

persistent proof storage
= 未実装
```

したがって別実行では原則:

```text
facts
+
rules
↓
inference replay
↓
ProofStep graph 再構築
```

となる。

repository を導入する目安:

```text
〜7-stem
concrete calculations を十分蓄積
↓
minimal repository の schema を決める

8–10 stem
↓
より複雑な concrete examples で schema を検証
↓
必要に応じて拡張
```

7-stem までで repository 開始に十分と考える理由:

```text
cyclic group
direct sum
exact sequence
suspension transport
Hopf invariant
Whitehead product
Toda bracket
quotient
generator order
family relation
stable-range transport
low-dimensional exception
```

の多くが実例として揃うため。

8–10 stem で確認したい追加ケース:

```text
multiple generators
extension issues
multiple derivation paths
primary decomposition
larger Toda-bracket indeterminacy
```

minimal schema candidate:

```text
DerivedFact
  conclusion
  scope
  group structure
  generator information
  proof provenance
  dependencies
  literature metadata
```

重要:

```text
Proof Repository
!=
answer-only cache

Proof Repository
=
derived result
+
derivation
+
dependency
+
literature provenance
```

状態:

```text
PLANNED AFTER SUFFICIENT CONCRETE STEM COVERAGE
```

---

# 24. proof narrative generation milestone

Phase 60 / 61 / 63 / 65 で手書き proof-style probe が蓄積している。

導入条件:

```text
複数 concrete proofs
↓
display pattern の反復
↓
presentation metadata schema が安定
↓
ProofStep graph から自動生成
```

Proof Repository と proof narrative generator は関連するが同一機能ではない。

```text
repository
= proof object の永続保存 / 再利用

narrative generator
= proof object の人間向け文章化
```

両者を同時に巨大 framework として先取りしない。

---

# 25. 次の数学 Phase

Phase 65 は COMPLETE。

次は Toda Proposition 5.6 後の concrete source statement / consequence を確認して開始する。

開始順序:

```text
source statement
↓
proof dependency
↓
current code / tests compatibility
↓
minimum missing representation
↓
minimum theorem rule
↓
integration / provenance
```

Equation (5.8):

```text
Δ(ι₉)=±(2ν₄-Eν′)=±[ι₄,ι₄]
```

は Phase 65 では deferred とした次候補である。

引き続き deferred:

```text
stable ν / η³
stable homotopy-group model
generic exact-order solver
generic quotient solver
generic theorem specialization engine
automatic proof narrative generation
persistent Proof Repository implementation
agenda/worklist inference architecture
```
