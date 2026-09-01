# EHP Proof Tracer Roadmap

## 1. この文書の目的

この文書は EHP Proof Tracer の将来拡張に関する長期的な設計方針を記録する。

```text
README.md
=
現在できること / 現在の状態

docs/design.md
=
現在の architecture / semantics / boundaries

docs/development_log.md
=
時系列の実装履歴

docs/roadmap.md
=
将来機能と依存関係
```

各機能は actual mathematical need に基づいて個別に仕様化し、既存 API と generic inference engine を不必要に壊さない最小変更で導入する。

---

# 2. Phase 29 完了時点の実装基盤

実装済みの主な基盤:

```text
Abelian group calculation
EHP reasoning
ORDER
Suspension
Freudenthal
Composition
Generalized Hopf invariant
Additive expressions
Homomorphism reasoning
Set / subgroup reasoning
Coset / modulo reasoning
Symbolic scalar constraints
Indeterminacy
Toda bracket minimum representation
Toda bracket membership
Toda bracket definedness
Toda membership theorem bridge
Indexed unstable Toda notation
Typed HomotopyElement source / target context
Structured GeneratorSymbol
Indexed Toda theorem validity
Literature-backed theorem fact repository
Explicit generator typing facts
Explicit generator ambient-group facts
Generator fact repository
Typed-element materialization
η₃ / ν′ / ν₇ production generator facts
Explicit Eν′ typing via Suspension
Actual typed {η₃,Eν′,ν₇}_1
Explicit primitive zero-composition facts
Corrected index-1 Toda definedness rule
Actual corrected {η₃,Eν′,ν₇}_1 definedness
Actual theorem-backed ε₃ membership
Corrected single-run end-to-end Toda proof trace
InjectiveMapStatement
IsomorphismStatement
Isomorphism → Injective inference
MapApplication equality representation
Injective-map equality reflection
Map-property provenance chain
Mismatched-map rejection
Map-property fixed-point regression
HOPF_MAP actual identity
MapTypingFact
HOPF_MAP_TYPING_FACT
MapIsomorphismFact
HOPF_MAP_ISOMORPHISM_FACT
MapIsomorphismFactRepository
MAP_ISOMORPHISM_FACT_REPOSITORY
Exact typing-context map-property lookup
MapIsomorphismFact → ProofStep.GIVEN materialization
Actual H fact → Isomorphism(H)
Actual H Isomorphism → Injective(H)
Actual-H fact-driven equality reflection
Actual-H provenance / invalid / scope regression
Human-readable Phase 29 capability probe
```

Current full regression:

```text
1408 passed in 96.81s
```

---

# 3. 基本設計原則

```text
実際の数学的必要
↓
必要最小限の表現
↓
explicit fact / domain rule
↓
既存 machinery
```

重要:

```text
representable
≠
valid
```

```text
GeneratorSymbol
≠
typing knowledge
```

```text
MapSymbol
≠
map typing knowledge
```

```text
MapTypingFact
≠
map property knowledge
```

```text
MapIsomorphismFact
≠
IsomorphismStatement
```

```text
type-compatible
≠
zero composition
≠
Toda definedness
```

```text
IsomorphismStatement(f)
≠
InjectiveMapStatement(f)
```

notation から hidden knowledge を自動生成しない。

---

# 4. 現在の主要 dependency chain

```text
Abelian group expression
↓
Homomorphism reasoning
↓
Set / subgroup reasoning
↓
Coset / modulo reasoning
↓
Symbolic scalar constraints
↓
Indeterminacy
↓
Toda bracket
↓
Indexed unstable Toda notation
↓
Typed homotopy elements
↓
Structured generators
↓
Indexed theorem validity
↓
Theorem fact repository
↓
Generator typing / ambient-group facts
↓
Actual Toda-generator typing
↓
Explicit corrected composition knowledge
↓
Corrected index-1 Toda definedness
↓
Actual theorem applicability
↓
ε₃ membership
↓
Map property statements
↓
Isomorphism → injectivity
↓
Equality reflection
↓
Actual H identity / typing context
↓
Actual H isomorphism fact repository
↓
Actual fact materialization
↓
Actual Isomorphism(H)
↓
Actual Injective(H)
↓
Actual-H fact-driven equality reflection
↓
Human-readable proof trace
```

---

# 5. Phase 27 completion

Phase 27 actual ε₃ Toda proof chain:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
↓
{η₃,Eν′,ν₇}_1 is defined
```

```text
Toda theorem fact
+
derived definedness
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

---

# 6. Phase 28 completion

Phase 28 general form:

```text
f(a)=f(b)
+
f is injective / isomorphism
↓
a=b
```

Implemented:

```text
InjectiveMapStatement
IsomorphismStatement
isomorphism_implies_injective_inference_rule()
injective_map_reflects_equality_inference_rule()
```

Representative `H` was still only a local `MapSymbol` assumption.

---

# 7. Phase 29 completion

Phase 29 connects actual `H` knowledge to the Phase 28 generic machinery.

## Actual identity

```text
HOPF_MAP
=
MapSymbol(name="H")
```

## Actual typing

```text
HOPF_MAP_TYPING_FACT

H : π₃(S²) → π₃(S³)
```

## Actual property

```text
HOPF_MAP_ISOMORPHISM_FACT

H : π₃(S²) → π₃(S³)
is an isomorphism
```

## Repository

```text
MAP_ISOMORPHISM_FACT_REPOSITORY
```

exact typing-context lookup:

```text
lookup(HOPF_MAP_TYPING_FACT)
↓
HOPF_MAP_ISOMORPHISM_FACT
```

## Materialization

```text
HOPF_MAP_ISOMORPHISM_FACT
↓
to_proof_step()
↓
GIVEN Isomorphism(H)
```

## Existing generic rule connection

```text
GIVEN Isomorphism(H)
↓
Injective(H)
```

## Representative actual-H end-to-end chain

```text
PRODUCTION FACT
H : π₃(S²) → π₃(S³) is an isomorphism

↓ materialize

GIVEN
H is an isomorphism

↓
H is injective

+

GIVEN
H(a)=H(b)

↓
a=b
```

The actual property comes from production knowledge. The mapped equality remains representative.

Regression coverage:

```text
full provenance
different-map rejection
unknown-typing-context rejection
unrelated-fact exclusion
deduplication
genuine fixed point
```

Final status:

```text
1408 passed in 96.81s
```

---

# 8. 実装状況

| 項目 | 状態 | 備考 |
|---|---|---|
| Additive expression | IMPLEMENTED | Phase 12 |
| homomorphism reasoning | IMPLEMENTED | Phase 13 |
| set / subgroup reasoning | IMPLEMENTED | Phase 14 |
| coset / modulo | IMPLEMENTED | Phase 15 |
| symbolic scalar constraints | IMPLEMENTED | Phase 16 |
| indeterminacy | IMPLEMENTED | Phase 17 |
| unstable Toda bracket | IMPLEMENTED | Phase 18 |
| Toda theorem bridge | IMPLEMENTED | Phase 19 |
| indexed Toda notation | IMPLEMENTED | Phase 20 |
| typed source / target | IMPLEMENTED | Phase 21 |
| structured `GeneratorSymbol` | IMPLEMENTED | Phase 22 |
| indexed Toda theorem validity | IMPLEMENTED | Phase 23 |
| theorem fact repository | IMPLEMENTED | Phase 24 |
| `GeneratorTypingFact` | IMPLEMENTED | Phase 25 |
| `GeneratorAmbientGroupFact` | IMPLEMENTED | Phase 25 |
| generator fact repository | IMPLEMENTED | Phase 25 |
| η₃ / ν′ / ν₇ production facts | IMPLEMENTED | Phase 25–26 |
| actual typed `{η₃,Eν′,ν₇}_1` | IMPLEMENTED | Phase 26 |
| corrected ε₃ Toda definedness | IMPLEMENTED | Phase 27 |
| corrected ε₃ end-to-end membership | IMPLEMENTED | Phase 27 |
| `InjectiveMapStatement` | IMPLEMENTED | Phase 28 |
| `IsomorphismStatement` | IMPLEMENTED | Phase 28 |
| isomorphism → injective | IMPLEMENTED | Phase 28 |
| injective equality reflection | IMPLEMENTED | Phase 28 |
| map-property provenance / fixed point | IMPLEMENTED | Phase 28 |
| `HOPF_MAP` actual identity | IMPLEMENTED | Phase 29 |
| `MapTypingFact` | IMPLEMENTED | Phase 29 |
| actual `HOPF_MAP_TYPING_FACT` | IMPLEMENTED | Phase 29 |
| `MapIsomorphismFact` | IMPLEMENTED | Phase 29 |
| actual `HOPF_MAP_ISOMORPHISM_FACT` | IMPLEMENTED | Phase 29 |
| `MapIsomorphismFactRepository` | IMPLEMENTED | Phase 29 |
| actual H fact materialization | IMPLEMENTED | Phase 29 |
| actual H → `IsomorphismStatement(H)` | IMPLEMENTED | Phase 29 |
| actual `Isomorphism(H)` → `Injective(H)` | IMPLEMENTED | Phase 29 |
| actual-H fact-driven equality reflection | IMPLEMENTED | Phase 29 |
| Phase 29 capability probe | IMPLEMENTED | Phase 29 |
| Hopf formula minimum representation | PLANNED | Phase 30 |
| smash product `γ∧δ` | PLANNED | Phase 31 candidate |
| actual H calculation | PLANNED | Phase 32+ |
| `H((2ι₂)η₂)=H(4η₂)` | PLANNED | after Hopf formula / smash product |
| `(2ι₂)η₂=4η₂` | PLANNED | use existing equality reflection |
| map-property literature provenance | PLANNED | concrete need |
| typing-aware proof-level map property | PLANNED | multiple contexts need |
| `SurjectiveMapStatement` | PLANNED | concrete need |
| preimage `f⁻¹(a)` | PLANNED | set-valued inverse image |
| `f(a)=f(b) ⇒ a≡b mod Ker(f)` | PLANNED | reuse Phase 13–15 |
| generator-fact literature provenance | PLANNED | concrete provenance need |
| composition-fact literature provenance | PLANNED | concrete provenance need |
| name / generator validation | PLANNED | explicit validation layer |
| dimension / generator validation | PLANNED | explicit validation layer |
| symbolic scalar `(-1)^n` | PLANNED | preserve symbolic sign |
| parity reduction of `(-1)^n` | PLANNED | even→1, odd→-1 |
| `{a,b,c}_0={a,b,c}` canonicalization | PLANNED | unstable Toda notation |
| general theorem representation | PLANNED | quantified theorem need |
| stable homotopy group `π_k^S` | PLANNED | stable context |
| stable Toda bracket `<a,b,c>` | PLANNED | stable layer |
| higher Toda bracket | DEFERRED | concrete need required |

---

# 9. 次 Phase：Phase 30 Hopf formula minimum representation

Phase 29 により actual H property side は準備できた。

現在:

```text
actual H isomorphism
↓
Injective(H)
```

が production knowledge 由来で利用可能。

次に必要なのは mapped equality を actual calculation から作るための formula layer。

代表 theorem/formula:

```text
H(γ α)=(γ∧γ)H(α)
```

Phase 30 の目的は、この formula を future actual proof に利用できる最小 structural / theorem representation として導入すること。

Phase 30 ではまだ:

```text
general smash-product algebra
actual (2ι₂)η₂ calculation
```

を先取りしない。

---

# 10. Representative map-theoretic scenario 1

長期目標:

```text
(2ι₂)η₂=4η₂
```

想定 proof structure:

```text
H((2ι₂)η₂)
↓ Hopf formula
(2ι₁∧2ι₁)H(η₂)
↓ known facts / smash-product calculation
4ι₃
```

一方:

```text
H(4η₂)
↓ homomorphism
4H(η₂)
↓ H(η₂)=ι₃
4ι₃
```

よって:

```text
H((2ι₂)η₂)=H(4η₂)
```

Phase 29 machinery:

```text
actual Isomorphism(H)
↓
Injective(H)
```

を用いて:

```text
(2ι₂)η₂=4η₂
```

へ反射する。

---

# 11. Representative map-theoretic scenario 2

長期目標:

```text
P(ι₅)=±2η₂
```

候補 theorem input:

```text
n even
↓
HP(ι_{2n+1})=±2ι_{2n-1}
```

`n=2`:

```text
HP(ι₅)=±2ι₃
```

known:

```text
H(η₂)=ι₃
```

homomorphism:

```text
H(±2η₂)=±2ι₃
```

よって:

```text
HP(ι₅)=H(±2η₂)
```

さらに Phase 29:

```text
actual Isomorphism(H)
↓
Injective(H)
↓
P(ι₅)=±2η₂
```

---

# 12. Hopf formula layer

Phase 30 candidate:

```text
Hopf formula theorem / statement
```

representative:

```text
H(γ α)=(γ∧γ)H(α)
```

重要:

```text
formula representation
≠
unconditional generic rewrite
```

actual theorem applicability / typing condition / source provenance は concrete implementation need に応じて追加する。

---

# 13. Smash product

Phase 31 candidate:

```text
γ ∧ δ
```

structural representation 候補:

```text
SmashProduct(
  left=γ,
  right=δ,
)
```

Phase 30 formula representation で smash-product expression が実際に必要になった時点で追加する。

---

# 14. Actual H calculation

Phase 32+ candidate:

```text
H((2ι₂)η₂)
```

の actual evaluation を行う。

必要候補:

```text
Hopf formula
smash product
H(η₂)=ι₃
scalar / additive reasoning
composition simplification
```

目標:

```text
H((2ι₂)η₂)=4ι₃
```

and:

```text
H(4η₂)=4ι₃
```

から:

```text
H((2ι₂)η₂)=H(4η₂)
```

を構築する。

---

# 15. Preimage / inverse-image reasoning

一般の写像:

```text
f⁻¹(a)
```

は inverse map の値ではなく preimage set として扱う。

候補:

```text
PreimageSet(
  map=f,
  value=a,
)
```

必要になるまで実装しない。

---

# 16. Kernel-modulo equality reasoning

一般則:

```text
f(a)=f(b)
↓
a-b ∈ Ker(f)
↓
a≡b mod Ker(f)
```

Phase 13〜15 の既存 machinery を再利用できる可能性が高い。

専用 shortcut rule を増やす前に existing rule composition を優先する。

---

# 17. Map property facts / provenance

Phase 29 で actual map fact repository は導入済み。

現在:

```text
MapIsomorphismFact
↓
to_proof_step()
↓
ProofStep.GIVEN
```

ただし literature provenance はまだない。

将来 concrete need があれば:

```text
map fact
+
LiteratureReference
↓
repository
↓
ProofStep.GIVEN
```

を検討する。

また current proof-level `IsomorphismStatement` は typing context を保持しない。

複数 H typing context を同じ proof graph で同時に扱う必要が生じた場合に typing-aware statement を検討する。

---

# 18. Additional generator / composition facts

現在の generator coverage:

```text
η₃
ν′
ν₇
```

現在の primitive zero-composition coverage:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
```

必要な theorem / proof scenario が出たときだけ追加する。

family formula や general composition table を先取りしない。

---

# 19. Nested expression typing

現在:

```text
GeneratorSymbol
↓
materialized typed HomotopyElement
↓
Suspension
↓
shifted source / target
```

general recursive repository traversal は未実装。

複数 nested expression form で本当に必要になったときに検討する。

---

# 20. Symbolic scalar expressions

Phase 16 では:

```text
ScalarSymbol
OddScalarStatement
EvenScalarStatement
ScalarCongruenceStatement
```

まで実装済み。

将来候補:

```text
(-1)^n
```

を structural に保持する最小 expression。

general-purpose CAS は目標としない。

---

# 21. Stable homotopy groups

stable context:

```text
α ∈ π_k^S
```

は unstable:

```text
α ∈ π_m(S^n)
```

と明確に区別する。

bridge は stabilization theorem に基づく。

notation-only conversion は行わない。

---

# 22. Stable Toda brackets

stable notation:

```text
<a,b,c>
```

は unstable:

```text
{a,b,c}
```

と別 representation にする。

---

# 23. Higher Toda brackets

higher / variable-arity brackets は concrete literature example が必要になるまで deferred。

---

# 24. 長期 dependency

Phase 29 完了後の有力順序:

```text
actual H equality-reflection foundation
↓
Hopf formula minimum representation
↓
smash product
↓
actual H calculation
↓
H((2ι₂)η₂)=H(4η₂)
↓
(2ι₂)η₂ = 4η₂
↓
preimage / kernel-modulo reasoning
↓
symbolic scalar expressions
↓
general theorem representation
↓
stable homotopy representation
↓
stable Toda bracket
```

actual theorem scenario に応じて順番は調整してよい。

---

# 25. テスト / representative demonstration 原則

各 layer で:

1. representation
2. structural distinction
3. validity / applicability
4. invalid-case behavior
5. integration
6. provenance
7. representative scenario
8. termination / scope
9. full regression
10. representative executable demonstration

を確認する。

```text
pytest
=
correctness / regression
```

```text
probe
=
人間が目で追える数学的 capability
```

probe は production APIs と existing inference rules を再利用し、別実装を作らない。

---

# 26. 文書運用方針

```text
README.md
=
現在の capabilities / status

docs/design.md
=
現在の architecture / semantics / boundaries

docs/development_log.md
=
chronological implementation history

docs/roadmap.md
=
future capability dependency
```

Phase completion ごとに historical statement と current specification を区別する。

---

# 27. 長期目標

最終的には:

```text
known unstable homotopy groups
+
known stable homotopy groups
+
generator / composition / map tables
+
map-property facts
+
quantified theorems
+
EHP exactness
+
ORDER
+
Suspension / stabilization
+
composition
+
Hopf invariant
+
smash-product formulas
+
additive reasoning
+
subgroup / modulo reasoning
+
kernel-modulo equality
+
preimage reasoning
+
injectivity / isomorphism reasoning
+
symbolic scalar constraints
+
symbolic scalar expressions
+
indeterminacy
+
unstable Toda brackets
+
stable Toda brackets
↓
new homotopy-theoretic conclusions
```

を同一 proof graph 上で扱う。
