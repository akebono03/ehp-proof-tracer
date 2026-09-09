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
```

現在の repository-wide regression:

```text
4102 passed in 32.75s
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
H(ν′)=η₅
2ν′=η₃η₄η₅
↓
π_{n+2}^n=Z/2{η_n²}
↓
ν₄
H(ν₄)=ι₇
2Eν₄=E²ν′
↓
ν_n
2ν_n=E^(n-3)ν′
4ν_n=η_n³
↓
π_(i-1)^3 ⊕ π_i^7 ≅ π_i^4
↓
Toda Proposition 5.6
π_5^2=Z/2{η₂³}
π_6^3=Z/4{ν′}
π_7^4=Z{ν₄}⊕Z/4{Eν′}
π_(n+3)^n=Z/8{ν_n}
↓
Toda (5.8)
Δ(ι₉)=±(2ν₄-Eν′)=±[ι₄,ι₄]
↓
Toda Lemma 5.7
E²α∈2ι₅∘π_(i+2)(S⁵)
→ E(η₂∘α)=0
↓
E(η₂∘ν′)=0
π_6^2=Z/4{η₂∘ν′}
Δ(ν₅)=±(η₂∘ν′)
```

---

# 5. 次の数学 Phase

Phase 67 は COMPLETE。

次は **Toda Lemma 5.7 後の次の concrete source statement / consequence** を確認して開始する。

Phase number:

```text
Phase 68
```

開始内容は source を確認してから確定する。

最初に行うこと:

```text
Phase 68-1
source statement / proof dependency /
current representation compatibility analysis
```

確認順序:

```text
A.
Toda source の Lemma 5.7 後の
statement / proposition / lemma / equation

B.
その proof が Phase 60–67 の
ν′ / ν₄ / ν-family / Δ / exactness result を
どのように利用するか

C.
current Expression / TodaPrimaryGroup / map / statement で
必要対象を structural に保持できるか

D.
不足が theorem-specific statement / bridge で済むか

E.
generic framework が本当に複数 independent branch で
繰り返し必要になったか
```

exact mathematical target は source analysis 前に固定しない。

---

# 6. Proof Records の運用

現在の正式 record:

```text
Toda Equation (5.8)
Δ(ι₉)=±(2ν₄-Eν′)=±[ι₄,ι₄]

Toda Lemma 5.7
E²α∈2ι₅∘π_(i+2)(S⁵) → E(η₂∘α)=0
E(η₂∘ν′)=0
Δ(ν₅)=±(η₂∘ν′)
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

必要になったとき separate documentation task として行う。

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

現在 formal proof record が2件蓄積した。

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

Phase 67 completion:

```text
4102 passed in 32.75s
```

test 数は増えているが full regression は約30秒台を維持している。

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
| next concrete Toda calculation | NEXT | 68 |
| automatic proof narrative generation | PLANNED / DEFERRED | later |
| persistent Proof Repository | PLANNED / DEFERRED | later |
| stable homotopy branch | DEFERRED | later |
| higher Toda brackets | DEFERRED | concrete need |

---

# 13. Current next step

```text
Phase 68-1
Toda Lemma 5.7 後の next source statement /
proof dependency /
current representation compatibility analysis
```

開始前に:

```text
current Toda source
Phase 67 implementation / tests
probes/probe_phase67_capabilities.py
docs/code_reference.md
docs/proof_records.md
```

を確認する。

原則:

```text
source statement
↓
dependency analysis
↓
current compatibility
↓
minimum change
```
