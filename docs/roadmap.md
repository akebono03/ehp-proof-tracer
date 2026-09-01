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

# 2. Phase 28 完了時点の実装基盤

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
Actual displayed-entry type compatibility
Explicit primitive zero-composition facts
ZeroCompositionFactRepository
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
Human-readable Phase 28 capability probe
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
map-property knowledge
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
Human-readable proof trace
```

---

# 5. Phase 27 completion

Phase 27 で actual ε₃ Toda proof chain は corrected end-to-end まで到達した。

primitive knowledge:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
```

corrected indexed definedness:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
↓
{η₃,Eν′,ν₇}_1 is defined
```

theorem connection:

```text
Toda theorem fact
+
derived definedness
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

---

# 6. Phase 28 completion

Phase 28 では次の一般形を proof graph 上で扱えるようになった。

```text
f(a)=f(b)
+
f is injective / isomorphism
↓
a=b
```

実装済み:

```text
InjectiveMapStatement
IsomorphismStatement
isomorphism_implies_injective_inference_rule()
injective_map_reflects_equality_inference_rule()
```

representation:

```text
f(a)=f(b)
```

は既存:

```text
MapApplication
RelationType.EQUALITY
```

で表す。

end-to-end:

```text
GIVEN
Isomorphism(f)

GIVEN
f(a)=f(b)

Round 1
Injective(f)

Round 2
a=b

↓
FIXED_POINT
```

invalid boundary:

```text
Injective(f) + g(a)=g(b)
↛ a=b
```

```text
Injective(f) + f(a)=g(b)
↛ a=b
```

scope regression:

```text
unrelated fact
↛ provenance
```

```text
derived Injective(f)
→ 1 step
```

```text
derived a=b
→ 1 step
```

```text
terminal re-run
→ new_steps == ()
```

representative probe:

```powershell
python -m probes.probe_phase28_capabilities
```

表示例:

```text
H is an isomorphism
↓
H is injective
+
H(a)=H(b)
↓
a=b
```

重要:

```text
H
=
Phase 28 では representative MapSymbol
```

actual Hopf map fact はまだ未導入。

最終確認:

```text
tests/test_map_property_rules.py
26 passed in 1.42s
```

```text
full suite
1358 passed in 102.90s
```

---

# 7. 実装状況

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
| `MapApplication` equality representation | IMPLEMENTED | existing + Phase 28 validation |
| injective equality reflection | IMPLEMENTED | Phase 28 |
| map-property provenance chain | IMPLEMENTED | Phase 28 |
| mismatched-map regression | IMPLEMENTED | Phase 28 |
| map-property fixed-point regression | IMPLEMENTED | Phase 28 |
| Phase 28 capability probe | IMPLEMENTED | Phase 28 |
| typed `MapSymbol` domain / codomain | PLANNED | Phase 29 candidate |
| actual Hopf map `H` facts | PLANNED | Phase 29 |
| actual `H` isomorphism fact | PLANNED | Phase 29 |
| map-property literature provenance | PLANNED | concrete need |
| `SurjectiveMapStatement` | PLANNED | concrete need |
| preimage `f⁻¹(a)` | PLANNED | set-valued inverse image |
| `f(a)=f(b) ⇒ a≡b mod Ker(f)` | PLANNED | reuse Phase 13–15 |
| generator-fact literature provenance | PLANNED | concrete provenance need |
| composition-fact literature provenance | PLANNED | concrete provenance need |
| name / generator validation | PLANNED | explicit validation layer |
| dimension / generator validation | PLANNED | explicit validation layer |
| symbolic scalar `(-1)^n` | PLANNED | preserve symbolic sign |
| parity reduction of `(-1)^n` | PLANNED | even→1, odd→-1 |
| smash product `γ∧δ` | PLANNED | Hopf formulas |
| `{a,b,c}_0={a,b,c}` canonicalization | PLANNED | unstable Toda notation |
| general theorem representation | PLANNED | quantified theorem need |
| stable homotopy group `π_k^S` | PLANNED | stable context |
| stable Toda bracket `<a,b,c>` | PLANNED | stable layer |
| higher Toda bracket | DEFERRED | concrete need required |

---

# 8. 次 Phase：Phase 29 actual H map facts / typing

Phase 28 の representative example:

```text
H is an isomorphism
H(a)=H(b)
↓
a=b
```

では、`H is an isomorphism` を GIVEN として直接与えている。

Phase 29 の目的は、この `H` を actual mathematical knowledge に接続すること。

候補 dependency:

```text
actual H identity
↓
H map typing
↓
H property fact
↓
IsomorphismStatement(H)
↓
existing Phase 28 rule
↓
Injective(H)
```

最初から Hopf formula 全体を入れず、次の actual proof に必要な最小 facts だけ追加する。

---

# 9. Representative map-theoretic scenario 1

長期目標:

```text
(2ι₂)η₂=4η₂
```

想定 proof structure:

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

よって:

```text
H((2ι₂)η₂)=H(4η₂)
```

Phase 28 の既存 machinery:

```text
Isomorphism(H)
↓
Injective(H)
```

を使って:

```text
(2ι₂)η₂=4η₂
```

へ反射する。

---

# 10. Representative map-theoretic scenario 2

長期目標:

```text
P(ι₅)=±2η₂
```

theorem input 候補:

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

さらに Phase 28:

```text
Isomorphism(H)
↓
Injective(H)
↓
P(ι₅)=±2η₂
```

---

# 11. Preimage / inverse-image reasoning

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

基本 semantics:

```text
x ∈ f⁻¹(a)
↔
f(x)=a
```

必要になるまで実装しない。

---

# 12. Kernel-modulo equality reasoning

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

# 13. Map property facts / provenance

Phase 28 では:

```text
IsomorphismStatement(H)
```

を representative GIVEN として使用した。

Phase 29 以降、actual proof で必要になれば:

```text
known map fact
+
LiteratureReference
↓
fact entry
↓
repository
↓
ProofStep.GIVEN
```

のような supply layer を検討する。

theorem repository と対称にしたいだけの理由では追加しない。

---

# 14. Additional generator / composition facts

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

# 15. Nested expression typing

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

# 16. Symbolic scalar expressions

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

# 17. Smash product

Toda 型 Hopf-invariant calculation のため:

```text
γ ∧ δ
```

を structural に保持する候補:

```text
SmashProduct(
  left=γ,
  right=δ,
)
```

theorem example:

```text
H(γα)
=
(γ∧γ)H(α)
```

無条件 generic rewrite にはせず、typed conditions / literature source を持つ theorem として扱う。

---

# 18. Stable homotopy groups

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

# 19. Stable Toda brackets

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

# 20. Higher Toda brackets

higher / variable-arity brackets は concrete literature example が必要になるまで deferred。

---

# 21. 長期 dependency

Phase 28 完了後の有力順序:

```text
generic equality reflection
↓
actual H map facts / typing
↓
Hopf invariant formulas
↓
smash product
↓
actual H calculation
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

# 22. テスト / representative demonstration 原則

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

# 23. 文書運用方針

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

# 24. 長期目標

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
