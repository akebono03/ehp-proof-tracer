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

将来の Phase の generic framework を先取りしない。

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
ordinary / Toda-(4.3) separation
ordinary Toda (2.11)
ordinary image bridge
composition-level primary reduction
Prop.2.6 indexed bracket + Toda (1.15)
corrected provenance / retirement audit
seventh formal proof record revised canonically

Phase 72R-A1
Toda (4.3) semantic audit

Phase 73
Toda Proposition 5.11 finite-dimensional
π_8^2=Z/2{η₂ν′η₆²}
π_9^3=0
π_10^4=Z/8{ν₄²}
π_(n+6)^n=Z/2{ν_n²}, n≥5
eighth formal proof record
```

現在の repository-wide regression:

```text
5386 passed in 124.02s
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

# 6. 証明記録 の運用

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

# 7. 自動証明 narrative 生成

現在の state:

```text
proof inference        = automatic
proof provenance       = automatic
literature metadata    = structured
proof records          = human curated
proof-style narrative  = hand-authored probe presentation
```

現在 formal mathematical proof record は Phase 78 までに13件蓄積し、Phase 79/80 は infrastructure capability records として分離している。

将来の target:

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

automatic proof narrative generation は Phase 80 完了後も未実装であり、rule selection / proof search とは別 capability として deferred のままとする。

---

# 8. 永続 Proof Repository

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

# 9. 安定群 branch

Phase 78 で low stable stems の concrete branch を実装済み:

```text
G_0=Z{ι}

(G_1;2)=Z/2{η}
(G_2;2)=Z/2{η²}
(G_3;2)=Z/8{ν}
(G_4;2)=0
(G_5;2)=0
(G_6;2)=Z/2{ν²}
(G_7;2)=Z/16{σ}
```

現在の representation:

```text
G_0
  StableHomotopyGroup(stem=0)

(G_k;2), k>=1
  StablePrimaryComponent(
    StableHomotopyGroup(stem=k),
    prime=2
  )
```

still deferred:

```text
generic E^∞ map object
generic stable homotopy-group database
generic stable theorem engine
stable ring / product machinery
generic stable composition typing
```

状態:

```text
LOW-STEM CONCRETE BRANCH COMPLETE THROUGH G_7
```

---

# 10. 性能 / 推論アーキテクチャ

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

# 12. 現在の完了表

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
| Toda (4.3) semantic audit | COMPLETE | 72R-A1 |
| seventh formal proof record canonical revision | COMPLETE | 72R |
| Toda Proposition 5.11 finite-dimensional / π_(n+6)^n | COMPLETE | 73 |
| stable homotopy branch through G_7 | COMPLETE | 78 |
| minimal in-memory Proof Repository | COMPLETE | 79 |
| repository-assisted automatic inference | COMPLETE | 80 |
| automatic rule selection / proof-search foundation | COMPLETE | 81 |
| multi-step / goal-directed proof-search foundation | IMPLEMENTED / FINAL PROBE REGRESSION PENDING | 82 |
| automatic proof narrative generation | PLANNED / DEFERRED | later |
| persistent Proof Repository | PLANNED / DEFERRED | later |
| higher Toda brackets | DEFERRED | concrete need |

---

# 13. 現在の次ステップ

Phase 73 は COMPLETE。

```text
π_8^2=Z/2{η₂ν′η₆²}
π_9^3=0
π_10^4=Z/8{ν₄²}
π_(n+6)^n=Z/2{ν_n²}, n≥5
```

supporting Toda (5.13):

```text
Δ(ν₉)=±2ν₄²
Δ(η₁₁²)=0
Δ(η₁₃)=0
```

次は:

```text
Phase 74-1
Toda 原典の次 statement
原典 / 証明依存 / 現在表現との互換性解析
```

Phase 74 の具体的 target は、Toda 原典の次 statement と proof dependency を確認してから確定する。

stable:

```text
(G_6;2)=Z/2{ν²}
```

は Phase 74 へ自動的に持ち越さず、stable branch 全体の concrete need が生じた時点で再評価する。

---

# 14. Phase 73 完了境界

完成:

```text
ν_n² := ν_n∘ν_(n+3)

π_8^2=Z/2{η₂ν′η₆²}
π_9^3=0
π_10^4=Z/8{ν₄²}

Δ(ν₉)=±2ν₄²
Δ(η₁₁²)=0
Δ(η₁₃)=0

π_11^5=Z/2{ν₅²}
π_12^6=Z/2{ν₆²}
π_13^7=Z/2{ν₇²}
π_14^8=Z/2{ν₈²}
π_(n+6)^n=Z/2{ν_n²}, n≥9

π_(n+6)^n=Z/2{ν_n²}, n≥5
TodaProp511FiniteDimensionalStatement
representative probe
formal proof record 8
```

provenance:

```text
all four direct Proposition 5.11 branches are INFERENCE
final aggregate is INFERENCE
final aggregate is not GIVEN
final graph acyclic
stable fields absent
```

代表 probe:

```powershell
python -m probes.probe_phase73_capabilities
```

final regression:

```text
5386 passed in 124.02s
```

### stable branch

```text
(G_6;2)=Z/2{ν²}
```

は deferred。

これまでの:

```text
(G_1;2)=Z/2{η}
(G_2;2)=Z/2{η²}
ν:=E^∞ν₄
4ν=η³
(G_3;2)=Z/8{ν}
(G_4;2)=0
```

と同じ stable branch に残す。

---

# 15. Phase 74 開始時の原則

```text
Toda source
↓
proof dependency
↓
ordinary / Toda-(4.3) semantics
↓
finite-dimensional / stable branch separation
↓
current representation compatibility
↓
minimum theorem-specific implementation
```

先取りしない:

```text
stable homotopy-group model
automatic proof narrative generation
persistent Proof Repository
generic symbolic solver
generic suspension-of-composition normalizer
```



---

# 16. Phase 74 completion / Phase 75 boundary

Phase 74 completed:

```text
Toda Lemma 5.12
{η_n,ν_(n+1),η_(n+4)}={ν_n²}, n≥6
```

completion spine:

```text
bracket definedness
first indeterminacy zero
second indeterminacy zero
singleton mod two
coefficient stability
n=8 nonzero anchor
final integration
applicability / provenance regression
representative probe
formal proof record 9
```

final regression:

```text
5609 passed in 31.59s
```

next:

```text
Phase 75-1
Toda 原典の次 statement
source / proof dependency / representation compatibility analysis
```

Phase 75 の具体的 target は原典と proof dependency を確認してから確定する。

引き続き先取りしない:

```text
stable homotopy-group model
generic Toda-bracket coset algebra
generic coefficient solver
generic induction engine
automatic proof narrative generation
persistent Proof Repository
```

---

# 17. Phase 75 completion / next boundary

Phase 75 は COMPLETE。

完了済み finite-dimensional Proposition 5.15:

```text
π_9^2=0
π_10^3=0
π_11^4=0
π_12^5=Z/2{σ'''}
π_13^6=Z/4{σ''}
π_14^7=Z/8{σ'}
π_15^8=Z{σ₈}⊕Z/8{Eσ'}
π_(n+7)^n=Z/16{σ_n}, n≥9
```

completion spine:

```text
low zero branches
Lemma 5.13 σ'''
Lemma 5.14 σ'' / σ' / σ₈
sigma-family definition
π_16^9=Z/16{σ₉}
n≥9 Toda (4.5) transport
n=8 Proposition 4.4 / Toda (5.15)
finite-dimensional aggregate
representative probe
formal proof record 10
```

pre-probe full regression:

```text
5991 passed in 114.31s
```

The stable clause:

```text
(G_7;2)=Z/16{σ}
```

remains in the deferred stable branch.

## 次の数学 Phase

Start with source/dependency/representation compatibility analysis of Toda (5.16).

Primary targets:

```text
ker(E:π_15^8→π_16^9)
=
<2σ₈-Eσ'>

Δ(ι₁₇)
=
±(2σ₈-Eσ').
```

First dependencies to inspect:

```text
Phase 75:
π_15^8=Z{σ₈}⊕Z/8{Eσ'}
π_16^9=Z/16{σ₉}
σ₉=Eσ₈
2Eσ₈=E²σ'

Toda EHP exactness around:
π_17^17 --Δ--> π_15^8 --E--> π_16^9

critical Toda-(4.3) semantics for π_15^8
ordinary / Toda group distinction
```

Do not preemptively add:

```text
generic mixed free/torsion kernel solver
generic homomorphism matrix framework
generic sign algebra
stable homotopy-group model
automatic proof narrative generation
persistent Proof Repository
```


---

# 18. Phase 76 completion / Phase 77 boundary

Phase 76 は COMPLETE。

完了済み Toda Equation (5.16):

```text
Ker(E:π_15^8→π_16^9)
=
Z{2σ₈-Eσ'}

Im(Δ:π_17^17→π_15^8)
=
Z{2σ₈-Eσ'}

π_17^17=Z{ι₁₇}

Δ(ι₁₇)
=
±(2σ₈-Eσ')
```

completion spine:

```text
source / dependency / representation audit
concrete mixed kernel calculation
concrete Proposition 4.2 Delta-E exactness
Ker E -> Im Delta bridge
π_17^17 diagonal free-cyclic fact
Delta generator up-to-sign consequence
applicability / provenance / non-circularity regression
representative probe
formal proof record 11
```

pre-probe full regression:

```text
6117 passed in 109.84s
```

## Phase 77 completion milestone

```text
Toda Lemma 5.16
```

完了済み capability:

```text
t>0
β∈π_(t+4)(S^m)
β∘ν_(t+4)=0
↓
E^4β∘σ_(t+8)
∈
(-1)^m x {ν_(m+4),E^7β,ν_(t+11)}_7
+
(-1)^t x {E^4β,ν_(t+8),2ν_(t+11)}_(t+3)
```

completion spine:

```text
source / typing audit
E^nβ -> E^7β correction
typed bracket setup
first / second Theorem 3.6 branches
Theorem 3.6 bracket-sum consequence
Phase 75 odd x provenance reuse
E^tσ₈=xE^tα*
σ_(t+8)=E^tσ₈
scaled composition
final scaled bracket-sum consequence
applicability / provenance / non-circularity
representative probe
formal proof record 12
```

pre-probe repository-wide regression:

```text
6262 passed in 114.35s
```

## Phase 78 completion milestone

Phase 78 は COMPLETE。

Machine-derived stable results:

```text
G_0=Z{ι}

(G_1;2)=Z/2{η}
(G_2;2)=Z/2{η²}
(G_3;2)=Z/8{ν}
(G_4;2)=0
(G_5;2)=0
(G_6;2)=Z/2{ν²}
(G_7;2)=Z/16{σ}
```

代表 probe:

```powershell
python -m probes.probe_phase78_capabilities
```

final repository-wide regression:

```text
6472 passed in 35.18s
```

formal proof record:

```text
record 13
Phase 78 stable G_0 through G_7 integration
```

## 次の数学 Phase

Begin with:

```text
source audit after the current Toda Lemma 5.16 segment
dependency analysis
representation compatibility
minimum missing theorem edge
```

Only after that audit should the next implementation Phase be named.

Do not preemptively add:

```text
generic stable homotopy-group database
generic E^∞ theorem engine
generic limit / colimit machinery
generic stable composition algebra
automatic proof narrative generation
persistent Proof Repository
```


---

# 19. Phase 79 completion / repository milestone

Phase 79 は COMPLETE。

The planned post-7-stem minimum repository milestone has now been reached.

実装済み:

```text
ProofRepositoryEntry
ProofRepository
in-memory registration
exact key lookup
conclusion lookup
statement-type lookup
phase lookup
theorem lookup
direct dependency access
cross-phase Phase 76 / 77 / 78 integration
duplicate-conclusion separation
applicability isolation
non-circularity regression
representative repository probe
```

現在の流れ:

```text
existing concrete proof builder
↓
ProofStep graph
↓
in-memory ProofRepository
↓
search / reuse within the same Python process
```

The milestone is intentionally narrower than the older `DerivedFact` candidate. Concrete implementation showed that the existing `ProofStep` already owns proof semantics and dependency edges, so the minimum repository only needs a thin catalog layer rather than duplicated group / generator / dependency fields.

現在のリポジトリ全体回帰:

```text
6520 passed in 35.07s
```

## 永続化は後続 milestone のまま

未実装:

```text
persistent backing store
serialization schema
persistent node IDs
schema migration
replay / validation
reverse dependency index
```

Persistence should be added only when cross-process reuse becomes a concrete requirement.

## 次の開発境界

Two paths remain independent:

```text
mathematical continuation
→ source / dependency audit after the current Toda / stable G_0...G_7 boundary

repository persistence
→ concrete cross-process reuse requirement
→ serialization / identity audit
→ minimum durable schema
```

Do not merge these into a generic theorem-prover / database framework prematurely.


---

# 20. Phase 80 completion / proof-search 境界

Phase 80 implements the first repository-assisted automatic inference path.

完了済み implementation:

```text
ProofRepository.entries()
repository_available_steps()
find_goal_step()
RepositoryInferenceResult
derive_goal_from_repository()
actual Phase 77 / Toda Lemma 5.16 integration
applicability / non-circularity regression
representative Phase 80 probe
```

現在の流れ:

```text
registered existing ProofStep premises
↓
identity-safe repository seed bridge
↓
explicitly supplied InferenceRule set
↓
existing fixed-point inference
↓
structural goal detection
↓
new final ProofStep
```

代表 actual proof guarantees:

```text
goal not initially registered
goal absent from initial ancestry
new final not original builder final_step
new final = INFERENCE
exact repository premises retained
exact existing Phase 77 rule retained
fixed point reached
graph acyclic
repository not mutated
```

Pre-probe repository-wide regression:

```text
6565 passed in 36.33s
```

## 以前の将来境界の訂正

Earlier Phase 79 roadmap text correctly treated automatic inference as not part of Phase 79. After Phase 80, the 現在の state must be distinguished as:

```text
repository lookup alone
→ does not auto-infer

repository-assisted runner with explicit rules
→ can infer automatically
```

Therefore `automatic theorem search` は引き続き保留, but repository-assisted inference is no longer deferred.

Similarly, the older roadmap entry describing the stable branch as deferred is superseded by Phase 78:

```text
low-stem stable branch G_0...G_7
= COMPLETE
```

The remaining stable deferrals concern generic stable machinery, not the concrete G_0...G_7 branch.

## 次の capability 依存

自然な次 milestone:

```text
Phase 81+
rule selection / proof-search audit
```

実装前に確認する事項:

```text
which existing InferenceRule families are safe for unrestricted fixed-point use?
which rules are one-shot / scope-sensitive?
how should goal shape restrict candidate rules?
how should repository facts be indexed without moving theorem knowledge into ProofRepository?
how should search avoid cycles and repeated equivalent states?
how should multiple derivations be ranked or retained?
```

Do not jump directly to:

```text
general theorem prover
global backward-chaining engine
generic mathematical normalization
persistent database
automatic theorem generation
```

The next Phase should first audit 現在の rule families and define the minimum safe search policy.


---

# 21. Phase 81 completion / Phase 82 boundary

Phase 81 implements the first automatic rule-selection layer above the Phase 80 repository-assisted runner.

Completed:

```text
InferenceRule safety audit
minimal InferenceRuleCatalog
goal-compatible exact-type filtering
fixed-point-safe opt-in metadata
rule identity deduplication
catalog-aware repository inference wrapper
actual Toda Lemma 5.16 integration
wrong-rule / ambiguity regression
non-circularity / acyclicity regression
representative probe
```

現在の流れ:

```text
actual goal
↓
InferenceRuleCatalog
↓
exact conclusion-type + fixed-point-safe filtering
↓
execution-rule identity deduplication
↓
existing premise matching / match_guard
↓
repository-assisted forward fixed-point inference
↓
new proof
```

代表 actual theorem:

```text
Toda Lemma 5.16
```

Phase 81 により、caller は final rule を直接指定する必要がなくなった。

Pre-probe repository-wide regression:

```text
6631 passed in 34.70s
```

## Phase 82 next capability dependency

Phase 81 では、自動選択された rule が必要とする premise はすべて repository / forward closure に既に存在する必要がある。

Phase 82 では次の不足 capability を扱う:

```text
selected goal-producing rule
↓
required premise missing
↓
identify rule(s) that could produce that premise
↓
limited multi-step goal-directed search
```

狭い範囲から開始する。

Recommended Phase 82-1:

```text
existing rule-producer / premise-demand audit
```

Questions:

```text
how to represent a missing premise target without generic theorem unification?
how to locate producer rules safely?
how to prevent recursive cycles?
how to bound depth / breadth?
how to preserve current fixed-point-safe boundaries?
how to distinguish structural producer compatibility from actual applicability?
```

次を直ちに導入しない:

```text
full backward chaining
general DFS / BFS theorem prover
A* proof search
proof ranking
persistent theorem database
mathematical-equivalence normalization
generic theorem synthesis
```

Phase 82 ではまず、final rule が初期状態に存在しない premise を要求し、その premise を既知の safe rule で生成できる concrete two-stage search path を1つ証明する。

---

# 22. Phase 82 completion / 次境界

Phase 82 で実装した capability:

```text
goal
↓
automatic final-rule selection
↓
missing-premise detection
↓
one-level producer lookup
↓
unique safe producer
↓
intermediate ProofStep
↓
final-rule retry
↓
goal ProofStep
```

主要 infrastructure:

```text
PremiseAvailability
detect_missing_premises()
detect_goal_rule_missing_premises()

find_premise_producer_rule_entries()
find_premise_producer_rules()

derive_goal_from_repository_with_one_level_producers()
```

actual representative:

```text
Toda Lemma 5.16
```

search safety:

```text
0 producer
→ stop

1 producer
→ execute one level

2+ distinct producers
→ ambiguity, stop

same-rule aliases
→ identity dedup

producer premise missing
→ do not recurse

multiple final premises missing
→ do not search

cycle-shaped catalog
→ do not traverse
```

Phase 82-6 repository-wide regression:

```text
6716 passed in 35.78s
```

Phase 82-7:

```text
representative probe
completion documentation
```

まで実装済み。final probe regression pending。

## Phase 82 後も保留するもの

```text
arbitrary-depth backward chaining
recursive theorem graph traversal
DFS / BFS / A*
multiple-missing-premise planning
producer ranking
proof-cost model
best-proof selection
persistent search cache
automatic proof narrative generation
generic theorem prover
```

## 次 Phase の決め方

Phase 83 の具体的 target はここでは先取りしない。

次の作業開始時に:

```text
現在の capability
↓
具体的な次の必要
↓
current code / tests audit
↓
最小 Phase target
```

で決定する。

Phase 82 の成功を理由に unrestricted recursive theorem search へ自動的に進まない。

---

# Phase 83 完了：multiple one-level producers

完了した拡張:

```text
one missing premise
→ multiple missing premises

one unique producer
→ one unique producer per missing premise

one producer execution
→ multiple producers in one shared round
```

維持した制約:

```text
producer depth = 1
recursive lookup = なし
ranking = なし
repository mutation = なし
```

代表actual theorem:

```text
Toda Lemma 5.16内部の
Theorem 3.6 bracket-sum containment
```

次候補:

```text
Phase 84
producer itself has a missing premise
→ depth=2 compatibility audit
```

Phase 84でも、最初から一般DFS/BFSへ進まず、bounded depth=2の表現・停止条件・cycle safetyを先に監査する。
