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

# 2. Phase 27 完了時点の実装基盤

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
Corrected single-run end-to-end proof trace
Human-readable capability probes
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
type-compatible
≠
zero composition
≠
Toda definedness
```

```text
displayed adjacency
≠
indexed Toda defining conditions
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
Actual displayed-entry type compatibility
↓
Explicit corrected composition knowledge
↓
Corrected index-1 Toda definedness
↓
Actual theorem applicability
↓
ε₃ membership
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
ε₃ ∈ {η₃,Eν′,ν₇}_1

+
derived definedness

↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

single fixed-point run:

```text
Round 1
definedness

Round 2
membership

↓
FIXED_POINT
```

重要な correction:

```text
Eν′ ∘ ν₇ = 0
```

を primitive second defining condition として扱わない。

current second base zero condition:

```text
ν′ ∘ ν₆ = 0
```

third displayed entry は:

```text
Eν₆ = ν₇
```

で接続する。

代表 probe:

```powershell
python -m probes.probe_phase27_capabilities
```

最終確認:

```text
tests/test_phase27_theorem_connection.py
11 passed in 0.69s
```

```text
full suite
1332 passed in 86.87s
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
| actual displayed Toda type compatibility | IMPLEMENTED | Phase 26 |
| typing ↔ ambient consistency query | IMPLEMENTED | Phase 26 |
| `η₃∘Eν′=0` fact | IMPLEMENTED | Phase 27 |
| `ν′∘ν₆=0` fact | IMPLEMENTED | Phase 27 |
| `Eν₆=ν₇` fact | IMPLEMENTED | Phase 27 |
| `ZeroCompositionFactRepository` | IMPLEMENTED | Phase 27 |
| typed/untyped structure lookup | IMPLEMENTED | Phase 27 |
| corrected index-1 Toda definedness | IMPLEMENTED | Phase 27 |
| actual `{η₃,Eν′,ν₇}_1` definedness | IMPLEMENTED | Phase 27 |
| corrected ε₃ end-to-end membership | IMPLEMENTED | Phase 27 |
| full ProofStep provenance chain | IMPLEMENTED | Phase 27 |
| Phase 27 capability probe | IMPLEMENTED | Phase 27 |
| generator-fact literature provenance | PLANNED | concrete provenance need |
| composition-fact literature provenance | PLANNED | concrete provenance need |
| name / generator validation | PLANNED | explicit validation layer |
| dimension / generator validation | PLANNED | explicit validation layer |
| typed `MapSymbol` domain / codomain | PLANNED | map-theoretic proof need |
| `InjectiveMapStatement` | PLANNED | equality reflection |
| `IsomorphismStatement` | PLANNED | injective / surjective bridge |
| preimage `f⁻¹(a)` | PLANNED | set-valued inverse image |
| `f(a)=f(b) ⇒ a≡b mod Ker(f)` | PLANNED | reuse Phase 13–15 |
| symbolic scalar `(-1)^n` | PLANNED | preserve symbolic sign |
| parity reduction of `(-1)^n` | PLANNED | even→1, odd→-1 |
| smash product `γ∧δ` | PLANNED | Hopf formulas |
| `{a,b,c}_0={a,b,c}` canonicalization | PLANNED | unstable Toda notation |
| general theorem representation | PLANNED | quantified theorem need |
| stable homotopy group `π_k^S` | PLANNED | stable context |
| stable Toda bracket `<a,b,c>` | PLANNED | stable layer |
| higher Toda bracket | DEFERRED | concrete need required |

---

# 7. 次 Phase の推奨方向

Phase 27 までで:

```text
generator facts
↓
typing
↓
composition validity
↓
explicit zero-composition knowledge
↓
corrected Toda definedness
↓
theorem applicability
↓
membership
↓
proof trace
```

が actual ε₃ example で一通りつながった。

次の強い候補は map-theoretic reasoning。

候補 dependency:

```text
map typing
↓
injectivity / isomorphism
↓
equality reflection
↓
preimage reasoning
↓
kernel-modulo equality
```

最初からすべて実装せず、representative proof に必要な最小 layer から進む。

---

# 8. Map typing / injectivity / isomorphism

現在 `MapSymbol` / `MapApplication` / homomorphism reasoning は実装済み。

今後、proof-level に:

```text
f : A → B
```

という map typing を保持する候補がある。

statement 候補:

```text
InjectiveMapStatement(f)
IsomorphismStatement(f)
SurjectiveMapStatement(f)
```

基本 bridge:

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

equality reflection:

```text
Injective(f)
f(a)=f(b)
↓
a=b
```

Map property は notation から推測せず、explicit theorem fact / literature-backed fact として供給する。

---

# 9. Representative map-theoretic scenario 1

目標:

```text
(2ι₂)η₂=4η₂
```

将来の proof structure:

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

さらに:

```text
Isomorphism(H)
↓
Injective(H)
↓
(2ι₂)η₂=4η₂
```

必要候補:

```text
map typing
smash product
Hopf theorem
homomorphism
injectivity / isomorphism
equality reflection
provenance
```

---

# 10. Representative map-theoretic scenario 2

目標:

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

さらに:

```text
Isomorphism(H)
↓
Injective(H)
↓
P(ι₅)=±2η₂
```

必要候補:

```text
theorem instantiation
parity side condition
sign indeterminacy
homomorphism
injectivity
provenance
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

`f⁻¹(a)` 自体を単一 element としない。

必要なら:

```text
preimage set
+
chosen witness
```

を分ける。

---

# 12. Kernel-modulo equality reasoning

重要な一般則:

```text
f(a)=f(b)
↓
a-b ∈ Ker(f)
↓
a≡b mod Ker(f)
```

Phase 13〜15 の既存:

```text
homomorphism
ZERO
kernel membership
modulo ↔ difference membership
```

を再利用できる可能性が高い。

専用 shortcut rule を増やす前に既存 rule composition を優先する。

---

# 13. Generator / composition fact provenance

現在 generator typing provenance は data-path provenance。

Phase 27 composition facts も explicit production fact だが、composition fact 自体の literature source は未導入。

将来候補:

```text
known generator / composition fact
+
LiteratureReference
↓
fact entry
↓
repository
↓
ProofStep.GIVEN
```

ただし theorem repository と対称にしたいだけの理由では追加しない。

actual proof trace で source attribution が必要になった時点で導入する。

---

# 14. Additional production generator / composition facts

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

一般の symbolic scalar arithmetic expression は未実装。

将来候補:

```text
(-1)^n
```

を structural に保持するため:

```text
ScalarPower(
  base=-1,
  exponent=n,
)
```

などを必要最小限で追加する。

general-purpose CAS は目標としない。

---

# 17. `(-1)^n` の parity reduction

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

重要な区別:

```text
±α
```

は sign indeterminacy。

```text
(-1)^n α
```

は symbolic scalar expression。

parity 不明時に `±α` へ collapse しない。

---

# 18. Smash product

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

# 19. Unstable Toda index-zero notation

将来:

```text
{a,b,c}_0
=
{a,b,c}
```

という notation-level equivalence を扱う候補。

internal canonicalization は actual need に応じて決める。

index `1`, `2`, ... は別 bracket として保持する。

---

# 20. Stable homotopy groups

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

# 21. Stable Toda brackets

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

# 22. Higher Toda brackets

higher / variable-arity brackets は concrete literature example が必要になるまで deferred。

---

# 23. 長期 dependency

Phase 27 完了後の候補:

```text
corrected actual ε₃ proof chain
↓
map typing
↓
injectivity / isomorphism
↓
equality reflection
↓
preimage / kernel-modulo reasoning
↓
symbolic scalar expressions
↓
smash product / Hopf formulas
↓
general theorem representation
↓
stable homotopy representation
↓
stable Toda bracket
```

実際の theorem scenario に応じて順番は調整してよい。

---

# 24. テスト / representative demonstration 原則

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

# 25. 文書運用方針

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

# 26. 長期目標

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

knowledge として:

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

を provenance 付きで保持することを目標とする。
