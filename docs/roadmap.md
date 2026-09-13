# EHP Proof Tracer ロードマップ

この文書は **今後の capability dependency と Phase 順序**を記録する。

現在の仕様は `README.md` / `docs/design.md` を優先し、過去の詳細な実装履歴は `docs/development_log.md` を参照する。

---

# 1. 文書運用方針

roadmap は future-oriented に保つ。

完了済み Phase の詳細な subphase / focused test / implementation history はこの文書に蓄積しない。

```text
README.md
= current status / current capability

docs/design.md
= current architecture / semantics / boundaries

docs/development_log.md
= chronological implementation history

docs/code_reference.md
= current code navigation

docs/proof_records.md
= representative proof records

docs/roadmap.md
= future plan / dependency / deferred boundary
```

roadmap では完了済み work は milestone summary のみに圧縮する。

---

# 2. 開発原則

```text
実際の数学的必要
↓
source statement / proof dependency
↓
current code / related tests compatibility
↓
不足している最小表現
↓
最小限の theorem / fact semantics
↓
integration
↓
applicability / provenance
↓
representative probe
↓
full regression
↓
completion documentation
```

future Phase の generic framework を先取りしない。

---

# 3. 完了済み milestone summary

```text
Phase 1–27
generic proof / algebra / Toda-bracket foundation

Phase 28–48
actual H branch
PrimaryComponent / TodaPrimaryGroup
WhiteheadProduct
Toda Lemma 4.1
Proposition 4.2
Toda (4.5)
Proposition 4.4

Phase 49–56
π_3^2=Z{η₂}
π_4^3=Z/2{η₃}
Proposition 5.1 finite-dimensional branch
Toda (5.2)

Phase 57–63
Toda Lemma 5.2
Toda (5.3)
Proposition 5.3
Lemma 5.4
Lemma 5.5
Toda (5.5)
Toda (5.6)

Phase 64
performance stabilization

Phase 65
Toda Proposition 5.6 finite-dimensional computation

Phase 66
Toda Equation (5.8)
Δ(ι₉)=±(2ν₄-Eν′)=±[ι₄,ι₄]
proof record foundation

Phase 67
Toda Lemma 5.7
E²α∈2ι₅∘π_(i+2)(S⁵) → E(η₂∘α)=0
E(η₂∘ν′)=0
π_6^2=Z/4{η₂∘ν′}
Δ(ν₅)=±(η₂∘ν′)
second formal proof record

Phase 68
Toda Proposition 5.8 finite-dimensional
π_6^2=Z/4{η₂ν′}
π_7^3=Z/2{ν′η₆}
π_8^4=Z/2{ν₄η₇}⊕Z/2{Eν′η₇}
π_9^5=Z/2{ν₅η₈}
π_(n+4)^n=0, n≥6
third formal proof record

Phase 69
Toda Equation (5.10)
Δ(ι₁₁)=ν₅η₈
fourth formal proof record

Phase 70
Toda Proposition 5.9 finite-dimensional
π_7^2=Z/2{η₂ν′η₆}
π_8^3=Z/2{ν′η₆²}
π_9^4=Z/2{ν₄η₇²}⊕Z/2{Eν′η₇²}
π_10^5=Z/2{ν₅η₈²}
π_11^6=Z{Δι₁₃}
π_(n+5)^n=0, n≥7
fifth formal proof record

Phase 71
Toda Equation (5.12)
Δ:π_11^9→π_9^4 injective
Δ:π_12^11→π_10^5 injective
Δ:π_13^13→π_11^6 injective
Toda512DeltaInjectivityStatement
sixth formal proof record

Phase 72
Toda Lemma 5.10 first implementation
Δ(ι₁₃)∈{ν₆,η₉,2ι₁₀} mod 2π₁₁(S⁶)

Phase 72R
Toda Lemma 5.10 semantic correction
ordinary / 2-primary separation
ordinary Toda (2.11)
ordinary image bridge
composition-level primary reduction
Prop.2.6 indexed bracket + Toda (1.15)
corrected provenance / retirement audit
seventh formal proof record revised canonically
```

現在の repository-wide regression:

```text
5117 passed in 113.34s
```

---

# 4. 現在の concrete capability spine

```text
π_3^2=Z{η₂}
↓
π_4^3=Z/2{η₃}
↓
π_{n+1}^n=Z/2{η_n}
↓
Toda Lemma 5.2
↓
ν′
↓
π_{n+2}^n=Z/2{η_n²}
↓
ν₄ / ν_n
↓
Toda Proposition 5.6
π_(n+3)^n
↓
Toda (5.8) / Lemma 5.7 / Proposition 5.8
π_(n+4)^n
↓
Toda Equation (5.10)
Δ(ι₁₁)=ν₅η₈
↓
Toda Proposition 5.9
π_7^2=Z/2{η₂ν′η₆}
π_8^3=Z/2{ν′η₆²}
π_9^4=Z/2{ν₄η₇²}⊕Z/2{Eν′η₇²}
π_10^5=Z/2{ν₅η₈²}
π_11^6=Z{Δι₁₃}
π_(n+5)^n=0, n≥7
```

---

# 5. 次の数学 Phase

Phase 71 は COMPLETE。

完成:

```text
Toda Equation (5.12)

Δ:π_11^9→π_9^4 injective
Δ:π_12^11→π_10^5 injective
Δ:π_13^13→π_11^6 injective

Toda512DeltaInjectivityStatement
```

次は **Phase 72**。

開始:

```text
Phase 72-1
Toda Lemma 5.10
source statement / proof dependency /
current representation compatibility analysis
```

source target:

```text
Δ(ι₁₃)
∈
{ν₆,η₉,2ι₁₀}
mod 2π₁₁(S⁶)
```

確認順序:

```text
A.
Toda Lemma 5.10 exact statement / locator / proof

B.
Phase 71 Toda (5.12) injectivity のどの case が prerequisite か

C.
existing TodaBracket / modulo / subgroup semantics で
concrete coset-level statement を表現できるか

D.
不足する場合だけ narrow theorem-specific representation を追加
```

generic Toda-bracket coset algebra を source verification 前に先取りしない。

automatic proof narrative generation / persistent Proof Repository / stable homotopy branch は deferred のままとする。

---

# 6. Proof Records の運用

現在の正式 record:

```text
1. Toda Equation (5.8)
   Δ(ι₉)=±(2ν₄-Eν′)=±[ι₄,ι₄]

2. Toda Lemma 5.7
   E²α∈2ι₅∘π_(i+2)(S⁵) → E(η₂∘α)=0
   E(η₂∘ν′)=0
   Δ(ν₅)=±(η₂∘ν′)

3. Toda Proposition 5.8
   π_6^2=Z/4{η₂ν′}
   π_7^3=Z/2{ν′η₆}
   π_8^4=Z/2{ν₄η₇}⊕Z/2{Eν′η₇}
   π_9^5=Z/2{ν₅η₈}
   π_(n+4)^n=0, n≥6

4. Toda Equation (5.10)
   Δ(ι₁₁)=ν₅η₈

5. Toda Proposition 5.9
   π_7^2=Z/2{η₂ν′η₆}
   π_8^3=Z/2{ν′η₆²}
   π_9^4=Z/2{ν₄η₇²}⊕Z/2{Eν′η₇²}
   π_10^5=Z/2{ν₅η₈²}
   π_11^6=Z{Δι₁₃}
   π_(n+5)^n=0, n≥7

6. Toda Equation (5.12)
   Δ:π_11^9→π_9^4 injective
   Δ:π_12^11→π_10^5 injective
   Δ:π_13^13→π_11^6 injective
```

今後 representative proof-style probe を完成させた Phase では、必要に応じて `docs/proof_records.md` に追記する。

記録対象:

```text
source / theorem
result
upstream results
derived ingredients
proof-style derivation
machine provenance
literature
GIVEN / INFERENCE boundary
representation boundary
representative probe
regression status
```

過去 Phase 60–65 の backfill は一括して行わない。

---

# 7. Automatic proof narrative generation

current state:

```text
proof inference        = automatic
proof provenance       = automatic
literature metadata    = structured
proof records          = human curated
proof-style narrative  = hand-authored probe presentation
```

現在 formal proof record が6件蓄積した。

future target:

```text
ProofStep graph
+ Expression tree
+ InferenceRule provenance
+ LiteratureStatement
↓
relevant path extraction
↓
step grouping / compression
↓
equation-chain generation
↓
citation insertion
↓
rule-specific narrative templates
↓
console / Markdown / LaTeX
```

導入条件:

```text
複数 representative proof records が蓄積
↓
display pattern が安定
↓
必要 metadata が明確になる
↓
generic generator を設計
```

状態:

```text
PLANNED / DEFERRED UNTIL DISPLAY SCHEMA STABILIZES
```

Phase 68 で先取りしない。

---

# 8. Persistent Proof Repository

concrete calculation をさらに蓄積した後、proof result の persistent storage を separate Phase として検討する。

目安:

```text
roughly through 7-stem
↓
minimal Proof Repository design

8–10 stem calculations
↓
schema validation / extension
```

first repository candidate は最低限:

```text
derived conclusion
scope
group / generator structure
ProofStep provenance
dependencies
literature metadata
version / compatibility information
```

を保持する。

初期版では:

```text
generic theorem database
automatic theorem search
cached-answer replacement of inference
```

へ拡張しない。

状態:

```text
PLANNED / DEFERRED UNTIL CONCRETE NEED
```

---

# 9. Stable branch

引き続き deferred:

```text
(G_1;2)=Z/2{η}
(G_2;2)=Z/2{η²}
stable ν:=E^∞ν₄
4ν=η³
(G_3;2)=Z/8{ν}
stable homotopy-group model
```

finite-dimensional calculations で具体的必要が生じた時点で再評価する。

---

# 10. Performance / inference architecture

Phase 64:

```text
3657 tests
259.11s
↓
29.97s
```

Phase 71 completion on the then-used machine:

```text
4886 passed in 29.25s
```

Phase 72 completion on the home laptop:

```text
4990 passed in 70.11s
```

開発は2台のPCで行っているため wall-clock time は machine ごとに比較する。test count / semantics / provenance coverage は cross-machine regression signal として扱う。

当面は現在の architecture を維持する。

次を先取りしない:

```text
agenda / worklist inference engine
premise-type indexing
global proof cache
global GroupMap cache
automatic memoization of all builders
coverage reduction
```

fixture builder が heavy な同一 object graph を繰り返し構築する場合は、現在の方針どおり必要に応じて:

```python
@lru_cache(maxsize=1)
```

を利用する。

再び regression time が顕著に悪化した場合のみ profiling を行う。

---

# 11. 保留中の一般化

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
generic theorem specialization engine
generic theorem repository expansion
generic ImageMembership / map-image algebra
generic existential image witness
generic Lemma 4.5 all-n zero reflection
generic cyclic-image solver
generic exactness solver
stable homotopy-group model
higher Toda brackets
general-purpose CAS normalization
```

方針:

```text
DEFERRED UNTIL CONCRETE NEED
```

---

# 12. Current completion table

| Capability | State | Phase |
|---|---|---:|
| generic proof / algebra / Toda foundation | COMPLETE | 1–27 |
| actual H / early Toda branch | COMPLETE | 28–38 |
| primary / Toda group / Whitehead infrastructure | COMPLETE | 39–44 |
| Prop.4.2 / (4.5) / Prop.4.4 | COMPLETE | 45–48 |
| η low-dimensional branch / Prop.5.1 / (5.2) | COMPLETE | 49–56 |
| Lemma 5.2 / ν′ / Prop.5.3 | COMPLETE | 57–59 |
| Lemma 5.4 / Lemma 5.5 / ν-family / (5.6) | COMPLETE | 60–63 |
| performance stabilization | COMPLETE | 64 |
| Proposition 5.6 finite-dimensional | COMPLETE | 65 |
| Equation (5.8) | COMPLETE | 66 |
| proof record foundation | COMPLETE | 66 |
| Toda Lemma 5.7 | COMPLETE | 67 |
| second formal proof record | COMPLETE | 67 |
| Toda Proposition 5.8 finite-dimensional | COMPLETE | 68 |
| third formal proof record | COMPLETE | 68 |
| Toda Equation (5.10) | COMPLETE | 69 |
| fourth formal proof record | COMPLETE | 69 |
| Toda Proposition 5.9 finite-dimensional | COMPLETE | 70 |
| fifth formal proof record | COMPLETE | 70 |
| Toda Equation (5.12) Δ-injectivity | COMPLETE | 71 |
| sixth formal proof record | COMPLETE | 71 |
| Toda Lemma 5.10 first implementation | HISTORICAL / REGRESSION | 72 |
| Toda Lemma 5.10 semantic correction | COMPLETE | 72R |
| seventh formal proof record canonical revision | COMPLETE | 72R |
| Toda Proposition 5.11 / π_(n+6)^n | NEXT | 73 |
| automatic proof narrative generation | PLANNED / DEFERRED | later |
| persistent Proof Repository | PLANNED / DEFERRED | later |
| stable homotopy branch | DEFERRED | later |
| higher Toda brackets | DEFERRED | concrete need |

---

# 13. Current next step

```text
Phase 73-1
Toda Proposition 5.11
source statement / proof dependency / representation compatibility analysis
```

source definitions / targets:

```text
ν_n² := ν_n∘ν_(n+3),  n≥4
ν² := ν∘ν

π_8^2  = Z/2{η₂∘ν′∘η₆²}
π_9^3  = 0
π_10^4 = Z/8{ν₄²}
π_(n+6)^n = Z/2{ν_n²}, n≥5
(G_6;2)=Z/2{ν²}
```

source proof also introduces:

```text
Toda (5.13)
Δ(ν₉)=±2ν₄²
Δ(η₁₁²)=0
Δ(η₁₃)=0
```

Phase 73-1 で最初に確認する dependency:

```text
Proposition 5.9
Toda (5.2)
Lemma 5.7
Proposition 5.8
Proposition 5.6
Toda (5.6)
Toda (5.12)
Proposition 2.5
Toda (5.8)
Toda (5.10)
Toda (5.5)
Lemma 5.10
Proposition 1.4
Toda (5.4)
Proposition 4.4
Toda (4.5)
```

特に current representation で確認する:

```text
ν_n² / ν₄² composition representation
Delta composition rule from Proposition 2.5
Phase 72R corrected Lemma 5.10 modulo-bracket result の再利用方法
Prop.1.4 bracket-composition transformation
Toda (5.13) three concrete Delta relations
n=4,5,6 EHP exactness branch
n=8 Proposition 4.4 transport
n≥9 stable transport via (4.5)
```

原則:

```text
source proof
↓
dependency analysis
↓
current compatibility
↓
minimum new representation
↓
minimum theorem-specific inference
```

Proposition 5.11 全体や stable `(G_6;2)` を最初から一括実装しない。finite-dimensional concrete branches を先に分解する。

automatic proof narrative generation / persistent Proof Repository / stable homotopy branch は引き続き deferred。

---

# 14. Phase 72R completion boundary

Phase 72R is COMPLETE.

canonical prerequisite for future phases:

```text
Toda Lemma 5.10
TodaLemma510BracketModuloStatement
ambient_group=HomotopyGroup(11,6)
```

Do not use the historical Phase 72 primary-group shortcut graph as a new Phase prerequisite.

verified final regression:

```text
5117 passed in 113.34s
```

Phase 73 remains NEXT:

```text
Phase 73-1
Toda Proposition 5.11
source statement / proof dependency / representation compatibility analysis
```

Phase 73 should reuse the corrected Phase 72R result only where the Toda source proof actually requires Lemma 5.10.

