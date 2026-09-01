# EHP Proof Tracer Roadmap

## 1. この文書の目的

この文書は EHP Proof Tracer の将来拡張に関する長期的な設計方針を記録する。

```text
README.md
=
current capabilities / current status

 docs/design.md
=
current architecture / semantics / boundaries

 docs/development_log.md
=
chronological implementation history

 docs/roadmap.md
=
future capability dependency
```

各機能は actual mathematical need に基づいて個別に仕様化し、既存 API と generic inference engine を不必要に壊さない最小変更で導入する。

---

# 2. Phase 26 完了時点の実装基盤

Implemented foundations:

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
Typed-element materialization from explicit facts
η₃ / ν′ / ν₇ production generator facts
Explicit Eν′ typing connection via Suspension
Actual typed {η₃,Eν′,ν₇}_1 representative
Actual Toda defining-composition type compatibility
Typing / ambient-group consistency query
Representative human-readable capability probes
```

---

# 3. 基本設計原則

```text
actual mathematical need
↓
minimal representation
↓
explicit fact / domain rule
↓
existing machinery
```

Important:

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
type-compatible
≠
zero composition
≠
Toda definedness
```

Avoid notation-derived hidden knowledge.

---

# 4. Current main dependency chain

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
Actual Toda type compatibility
```

---

# 5. Phase 26 completion

Production generator coverage:

```text
η₃ : S⁴ → S³
η₃ ∈ π₄(S³)

ν′ : S⁶ → S³
ν′ ∈ π₆(S³)

ν₇ : S¹⁰ → S⁷
ν₇ ∈ π₁₀(S⁷)
```

Production repository:

```text
GENERATOR_FACT_REPOSITORY
```

Actual typing chain:

```text
ν′ : S⁶ → S³
↓
Suspension
↓
Eν′ : S⁷ → S⁴
```

Actual Toda entries:

```text
η₃  : S⁴  → S³
Eν′ : S⁷  → S⁴
ν₇  : S¹⁰ → S⁷
```

Actual indexed bracket:

```text
{η₃,Eν′,ν₇}_1
```

Verified compatibility:

```text
η₃ ∘ Eν′
→ type-compatible
```

```text
Eν′ ∘ ν₇
→ type-compatible
```

Therefore:

```text
{η₃,Eν′,ν₇}_1
→ defining compositions are type-compatible
```

Consistency API:

```text
is_typing_ambient_group_consistent()
```

Production results:

```text
η₃ → True
ν′ → True
ν₇ → True
```

Verified:

```text
tests/test_generator_facts.py
100 passed in 0.39s
```

```text
full suite
1290 passed in 23.16s
```

Representative capability demo:

```powershell
python -m probes.probe_phase26_capabilities
```

---

# 6. 実装状況

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
| η₃ generator facts | IMPLEMENTED | Phase 25 |
| ν′ generator facts | IMPLEMENTED | Phase 26 |
| ν₇ generator facts | IMPLEMENTED | Phase 26 |
| production η₃ / ν′ / ν₇ repository coverage | IMPLEMENTED | Phase 26 |
| explicit Eν′ typing connection | IMPLEMENTED | Phase 26 |
| actual typed `{η₃,Eν′,ν₇}_1` | IMPLEMENTED | Phase 26 |
| actual Toda type compatibility | IMPLEMENTED | Phase 26 |
| typing ↔ ambient consistency query | IMPLEMENTED | Phase 26 |
| representative capability demo convention | IMPLEMENTED | Phase 25+ |
| generator-fact literature provenance | PLANNED | concrete provenance need |
| actual zero-composition facts for ε₃ entries | NEXT CANDIDATE | deepen same proof chain |
| actual Toda definedness from explicit zero premises | PLANNED | after zero-composition facts |
| name / generator validation | PLANNED | explicit validation layer |
| dimension / generator validation | PLANNED | explicit validation layer |
| external generator-table loader | PLANNED | actual file-loading need |
| general theorem representation | PLANNED | quantified theorem need |
| stable homotopy group `π_k^S` | PLANNED | stable context |
| stable Toda bracket `<a,b,c>` | PLANNED | stable layer |
| higher Toda bracket | DEFERRED | concrete need required |

---

# 7. Recommended next Phase direction

The strongest next direction is to deepen the same actual ε₃ bracket chain.

Current state:

```text
explicit generator facts
↓
typed η₃ / Eν′ / ν₇
↓
type-compatible defining compositions
```

Natural next requirement:

```text
η₃ ∘ Eν′ = 0
Eν′ ∘ ν₇ = 0
```

as explicit mathematical facts or consequences of already supported rules.

Then:

```text
zero compositions
↓
Toda definedness
↓
existing theorem fact
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

This would connect the Phase 24 theorem fact and Phase 26 typed actual bracket into a deeper end-to-end proof trace.

---

# 8. Candidate Phase 27

Natural candidate:

```text
Phase 27
actual ε₃ Toda-definedness bridge
```

A possible split:

```text
27-1  η₃ ∘ Eν′ zero-composition fact requirement
27-2  Eν′ ∘ ν₇ zero-composition fact requirement
27-3  zero-composition fact representation / repository choice
27-4  production registration
27-5  typed actual compositions ↔ zero facts connection
27-6  actual {η₃,Eν′,ν₇}_1 definedness derivation
27-7  theorem fact applicability with actual definedness
27-8  ε₃ membership end-to-end representative
27-9  provenance / regression / scope
27-10 Phase 27 completion整理
```

This is only a roadmap suggestion. Exact Phase 27 scope should be fixed from current code and the actual mathematical sources before implementation.

---

# 9. Generator-fact provenance

Current generator provenance is:

```text
registered explicit fact
↓
repository lookup
↓
materialized typed element
```

Potential future extension:

```text
known generator typing statement
+
LiteratureReference
↓
generator fact entry
↓
repository
↓
typed element
```

Do not add `LiteratureReference` solely for symmetry with theorem facts. Add it when an actual generator fact requires source attribution in the proof trace.

---

# 10. Additional production generator facts

Current production coverage:

```text
η₃
ν′
ν₇
```

Potential future needs:

```text
μ₃
ι₇
other η_n / ν_n
```

Add only facts required by concrete theorem / proof scenarios.

Do not create a family formula solely because notation has an index.

---

# 11. Nested expression typing

Current explicit pattern:

```text
GeneratorSymbol
↓
materialized typed HomotopyElement
↓
Suspension
↓
shifted source / target
```

No general recursive repository traversal exists.

Future recursive typing should be introduced only if multiple nested expression forms create a real need.

---

# 12. Typing / ambient-group consistency

Current API:

```text
is_typing_ambient_group_consistent(generator)
```

Current semantics:

```text
True / False / None
```

No auto-conversion and no repository-construction rejection for cross-family mismatch.

A stronger validation layer should only be added when an actual workflow needs strict rejection.

---

# 13. Stable homotopy groups

Future stable context:

```text
α ∈ π_k^S
```

must remain distinct from unstable:

```text
α ∈ π_m(S^n)
```

Bridges should use stabilization mathematics, not notation-only conversion.

---

# 14. Stable Toda brackets

Stable notation:

```text
<a,b,c>
```

must remain distinct from unstable:

```text
{a,b,c}
```

---

# 15. Higher Toda brackets

Higher / variable-arity brackets remain deferred until concrete literature examples require them.

---

# 16. Long-term dependency suggestion

```text
Phase 26
actual typed Toda entries / compatibility
↓
actual zero-composition knowledge
↓
actual Toda definedness
↓
actual theorem applicability
↓
actual ε₃ membership proof trace
↓
generator / theorem provenance expansion when needed
↓
stable homotopy representation
↓
stable Toda bracket
```

At each suitable Phase boundary, grow a representative executable proof / validation scenario so that the visible mathematical chain becomes deeper rather than only increasing internal API coverage.

Target direction:

```text
generator facts
↓
typing
↓
composition validity
↓
zero compositions
↓
Toda definedness
↓
theorem applicability
↓
membership
↓
human-readable proof trace
```

---

# 17. Testing and representative-demonstration principle

For each new layer:

1. representation
2. structural distinction
3. validity / applicability
4. invalid-case behavior
5. integration
6. provenance if inference exists
7. representative scenario
8. termination / scope boundary
9. full regression
10. representative executable demonstration when mathematically meaningful

Tests and probes have different purposes:

```text
pytest
=
correctness / regression
```

```text
representative probe
=
visible mathematical progress
```

The probe must reuse production APIs and existing inference rules. It must not introduce a second implementation of the mathematical rule merely for demonstration.

Prefer module execution:

```powershell
python -m probes.<probe_module>
```

when the probe imports project-root modules.

---

# 18. Documentation policy

```text
README.md
=
current capabilities / current status

 docs/design.md
=
current architecture / semantics / boundaries

 docs/development_log.md
=
chronological implementation history

 docs/roadmap.md
=
future capability dependency
```

---

# 19. 長期目標

最終的には:

```text
known unstable homotopy groups
+
known stable homotopy groups
+
generator / map tables
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
additive reasoning
+
subgroup / modulo reasoning
+
symbolic scalar constraints
+
indeterminacy
+
unstable Toda brackets
+
stable Toda brackets
↓
new homotopy-theoretic conclusions
```

を同一の proof graph 上で扱えることを目標とする。

---

# 20. Map typing / injectivity / isomorphism

Current `MapSymbol` / `MapApplication` / homomorphism reasoning は実装済みだが、
complete source / target / ambient-group typing と map-property reasoning は今後の拡張候補とする。

将来的に、

```text
f : A → B
```

のような map typing を proof-level に保持できるようにする。

候補となる statement:

```text
InjectiveMapStatement(f)
IsomorphismStatement(f)
SurjectiveMapStatement(f)
```

基本的な theorem bridge:

```text
Isomorphism(f)
↓
Injective(f)
```

```text
Isomorphism(f)
↓
Surjective(f)
```

単射による equality reflection:

```text
Injective(f)
f(a)=f(b)
↓
a=b
```

この rule は、Toda 型の計算で
「写像した先で等しいことを示し、単射または同型を使って元に戻す」
証明を trace するために重要となる。

Map property は notation から暗黙に推測せず、
explicit theorem fact / literature-backed fact として扱う。

---

# 21. Preimage / inverse-image reasoning

一般の写像について、

```text
f⁻¹(a)
```

を inverse map の値ではなく preimage set として扱う。

概念的な representation 候補:

```text
PreimageSet(
  map=f,
  value=a,
)
```

基本 semantics:

```text
x ∈ f⁻¹(a)
↔
f(x)=a
```

を explicit theorem rule として扱えるようにする。

Important:

```text
f⁻¹(a)
```

自体を単一 element として扱わない。

文献で「`f⁻¹(a)` の元を取る」と書かれる場合には、

```text
preimage set
+
chosen element / witness
```

を区別する。

存在命題との将来接続:

```text
f⁻¹(a) ≠ ∅
↔
∃x, f(x)=a
```

symbolic witness の導入は、
general theorem representation / existential statement が実際に必要になった時点で検討する。

---

# 22. Kernel-modulo equality reasoning

群準同型 `f` に対する重要な一般則:

```text
f(a)=f(b)
↓
a-b ∈ Ker(f)
↓
a≡b mod Ker(f)
```

すなわち、

```text
f(a)=f(b)
→
a=b mod Ker(f)
```

という reasoning を将来的に扱えるようにする。

Current layers との接続候補:

```text
Homomorphism(f)
+
f(a)=f(b)
↓
f(a-b)=0
↓
a-b∈Ker(f)
↓
a≡b mod Ker(f)
```

これは Phase 13〜15 で実装済みの、

```text
homomorphism
ZERO
kernel membership
modulo ↔ difference membership
```

を再利用できる可能性が高い。

可能であれば専用 shortcut rule を増やすより、
既存 rule family の composition で proof trace を構築することを優先する。

Injective specialization:

```text
Injective(f)
↓
Ker(f)=0
```

に相当する theorem knowledge が利用できる場合、

```text
a≡b mod Ker(f)
↓
a=b
```

へ接続できる。

---

# 23. Symbolic scalar expressions beyond Phase 16

Phase 16 では、

```text
ScalarSymbol
OddScalarStatement
EvenScalarStatement
ScalarCongruenceStatement
```

まで実装済みである。

一般の symbolic scalar arithmetic expression は未実装。

Toda の計算では、

```text
(-1)^n
```

のような scalar expression を concrete sign に決めずに保持する必要がある。

将来的な representation 候補:

```text
ScalarPower(
  base=-1,
  exponent=n,
)
```

したがって、

```text
(-1)^n α
```

を、

```text
Multiple(
  coefficient=ScalarPower(-1,n),
  expression=α,
)
```

のように構造的に保持できるようにする。

必要最小限の scalar expression tree 候補:

```text
ScalarExpression
├── ScalarInteger
├── ScalarSymbol
├── ScalarNegation
├── ScalarSum
├── ScalarProduct
└── ScalarPower
```

ただし general-purpose CAS は目標としない。

Actual theorem need に応じて必要な node だけ追加する。

---

# 24. Parity reduction of `(-1)^n`

`(-1)^n` は `±1` の単なる indeterminacy ではなく、
`n` の parity によって値が決まる symbolic expression として扱う。

将来的な rules:

```text
n even
↓
(-1)^n=1
```

```text
n odd
↓
(-1)^n=-1
```

したがって、

```text
n even
↓
(-1)^n α=α
```

```text
n odd
↓
(-1)^n α=-α
```

へ接続できる。

Important distinction:

```text
±α
```

は sign indeterminacy。

```text
(-1)^n α
```

は symbolic scalar expression。

Parity が未知の場合でも式をそのまま保持し、
premature に `±α` へ collapse しない。

---

# 25. Smash product support for Hopf formulas

Toda 型の Hopf-invariant calculation では、

```text
γ ∧ γ
```

のような smash product が現れる。

将来的な structural expression 候補:

```text
SmashProduct(
  left=γ,
  right=δ,
)
```

Actual theorem example:

```text
H(γα)
=
(γ∧γ)H(α)
```

このような公式は無条件の generic rewrite とせず、

```text
typed variables
dimension conditions
map compatibility
literature source
```

を持つ theorem / inference rule として登録する。

将来の representative calculation:

```text
H((2ι₂)η₂)
=
E(2ι₁∧2ι₁)H(η₂)
=
2ι₃∘2ι₃∘ι₃
=
4ι₃
```

smash product 一般論は先取りせず、
実際の Hopf formula に必要な最小 representation から追加する。

---

# 26. Unstable Toda index-zero notation

Unstable Toda bracket について、

```text
{a,b,c}_0
=
{a,b,c}
```

を notation-level equivalence として扱う。

Internal canonical form の第一候補:

```text
TodaBracket(
  entries=(a,b,c),
  index=0,
)
```

つまり unindexed notation:

```text
{a,b,c}
```

を内部的には index `0` として解釈する。

一方、

```text
{a,b,c}_1
{a,b,c}_2
```

等は別の bracket として保持する。

---

# 27. Representative future map-theoretic proof scenarios

## 27.1 `(2ι₂)η₂=4η₂`

Goal:

```text
(2ι₂)η₂=4η₂
```

Target proof structure:

```text
H((2ι₂)η₂)
↓ Hopf theorem
E(2ι₁∧2ι₁)H(η₂)
↓ known facts / map calculation
2ι₃∘2ι₃∘ι₃
↓ additive / composition reasoning
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

したがって:

```text
H((2ι₂)η₂)=H(4η₂)
```

さらに:

```text
Isomorphism(H)
↓
Injective(H)
↓
(2ι₂)η₂=4η₂
```

この scenario は、

```text
map typing
smash product
Hopf theorem
homomorphism
injectivity / isomorphism
equality reflection
provenance
```

の統合テスト候補となる。

## 27.2 `P(ι₅)=±2η₂`

Goal:

```text
P(ι₅)=±2η₂
```

Target theorem input:

```text
n even
↓
HP(ι_{2n+1})=±2ι_{2n-1}
```

`n=2` への specialization:

```text
HP(ι₅)=±2ι₃
```

Known:

```text
H(η₂)=ι₃
```

Homomorphism reasoning:

```text
H(±2η₂)=±2ι₃
```

したがって:

```text
HP(ι₅)=H(±2η₂)
```

さらに:

```text
Isomorphism(H)
↓
Injective(H)
↓
P(ι₅)=±2η₂
```

この scenario は、

```text
theorem instantiation
parity side condition
sign indeterminacy
homomorphism
injectivity
provenance
```

の統合テスト候補となる。

---

# 28. Recommended long-term dependency extension

Current main direction:

```text
Phase 26
actual typed Toda entries / compatibility
↓
actual zero-composition knowledge
↓
actual Toda definedness
↓
actual theorem applicability
↓
actual ε₃ membership proof trace
```

この current chain は維持する。

その後または actual need に応じて、

```text
map typing
↓
injectivity / isomorphism
↓
preimage reasoning
↓
kernel-modulo equality
↓
symbolic scalar expressions
↓
(-1)^n parity reduction
↓
smash product / Hopf formulas
↓
general theorem representation
↓
stable homotopy representation
↓
stable Toda bracket
```

へ進む。

Important:

```text
Phase 27 candidate
=
actual ε₃ Toda-definedness bridge
```

は今回の追記によって置き換えない。

---

# 29. Updated implementation-status additions

以下を current implementation-status table の将来項目として扱う。

| 項目 | 状態 | 備考 |
|---|---|---|
| typed `MapSymbol` domain / codomain | PLANNED | actual map-typing need |
| `InjectiveMapStatement` | PLANNED | equality reflection |
| `IsomorphismStatement` | PLANNED | injective / surjective bridge |
| preimage `f⁻¹(a)` | PLANNED | set-valued inverse image |
| preimage membership `x∈f⁻¹(a) ↔ f(x)=a` | PLANNED | theorem bridge |
| `f(a)=f(b) ⇒ a≡b mod Ker(f)` | PLANNED | reuse Phase 13–15 |
| symbolic scalar `(-1)^n` | PLANNED | preserve symbolic sign |
| parity reduction of `(-1)^n` | PLANNED | even→1, odd→-1 |
| smash product `γ∧δ` | PLANNED | Hopf formulas |
| `{a,b,c}_0={a,b,c}` canonicalization | PLANNED | unstable Toda notation |
| representative map-theoretic proof probes | PLANNED | after supporting APIs exist |

---

# 30. Long-term target extension

Long-term target に以下を追加する。

```text
known unstable homotopy groups
+
known stable homotopy groups
+
generator / map tables
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

その際、

```text
exact value
partial information
sign uncertainty
coefficient uncertainty
symbolic sign (-1)^n
coset uncertainty
preimage membership
kernel-modulo equality
Toda-bracket membership
stable Toda-bracket membership
```

を provenance 付き knowledge として保持する。

