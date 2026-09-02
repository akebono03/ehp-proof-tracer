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

# 2. Phase 32 完了時点の実装基盤

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
HOPF_MAP actual identity
MapTypingFact
HOPF_MAP_TYPING_FACT
MapIsomorphismFact
HOPF_MAP_ISOMORPHISM_FACT
MapIsomorphismFactRepository
MAP_ISOMORPHISM_FACT_REPOSITORY
Actual H fact materialization
Actual Isomorphism(H)
Actual Injective(H)
Actual-H equality reflection
Toda Prop.2.2 right direct theorem
SmashProduct minimum representation
Toda Prop.2.2 left direct theorem
Phase 32 human-readable capability probe
```

Current full regression:

```text
1512 passed in 63.58s
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
representation
≠
typing
≠
theorem knowledge
```

```text
type-compatible
≠
zero composition
≠
Toda definedness
```

notation から hidden knowledge を自動生成しない。

---

# 4. Completed Phase chain

```text
Phase 12  Additive expressions
Phase 13  Homomorphism reasoning
Phase 14  Set / subgroup reasoning
Phase 15  Coset / modulo reasoning
Phase 16  Symbolic scalar constraints
Phase 17  Indeterminacy
Phase 18  Toda bracket minimum representation
Phase 19  Toda bracket membership / first theorem bridge
Phase 20  Indexed unstable Toda notation
Phase 21  Typed homotopy elements
Phase 22  Structured generators
Phase 23  Indexed Toda theorem validity
Phase 24  Theorem fact repository
Phase 25  Generator typing / ambient-group facts
Phase 26  Actual Toda-generator typing
Phase 27  Actual ε₃ Toda-definedness / membership
Phase 28  Map injectivity / isomorphism / equality reflection
Phase 29  Actual H facts / typing / isomorphism
Phase 30  Toda Prop.2.2 right formula
Phase 31  SmashProduct minimum representation
Phase 32  Toda Prop.2.2 left formula
```

すべて完了。

---

# 5. Toda Prop.2.2 completion

Phase 30 / 32 で [Toda] Prop.2.2 の両式を direct theorem rule として扱える。

右側:

```text
H(a∘Eb)=H(a)∘Eb
```

左側:

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

重要:

```text
H(a)=β
```

は Prop.2.2 本体の premise ではない。

β-based reasoning は concrete Hopf value への specialization / integration test として保持する。

両 theorem conclusion は canonical production `HOPF_MAP / EHP_H_MAP` identity を使用する。

---

# 6. SmashProduct current boundary

Phase 31 で:

```text
a∧b
c∧c
E(c∧c)
```

を structural に表現可能。

しかし:

```text
SmashProduct typing
SmashProduct algebra
normalization
symmetry theorem
associativity theorem
Barratt-Hilton knowledge
```

は未実装。

current:

```text
SmashProduct has no source / target
E(c∧c).source = None
E(c∧c).target = None
```

---

# 7. 長期目標 1

代表目標:

```text
(2ι₂)η₂=4η₂
```

想定 proof structure:

```text
H((2ι₂)η₂)
↓ Toda Prop.2.2 left
E(2ι₁∧2ι₁)H(η₂)
↓ Toda Prop.3.1 / required smash-product reasoning
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

Phase 29:

```text
Isomorphism(H)
↓
Injective(H)
```

から:

```text
(2ι₂)η₂=4η₂
```

へ反射する。

---

# 8. 長期目標 2

代表目標:

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

Phase 29 equality reflection を使って:

```text
P(ι₅)=±2η₂
```

へ進む候補がある。

---

# 9. Phase 33 candidate：Barratt–Hilton prerequisite minimum representation

Phase 32 の次は、[Toda] Prop.3.1 Barratt–Hilton に必要な prerequisite を最小単位で導入する。

現時点の第一候補:

```text
symbolic scalar expression
(-1)^n
```

[Toda] Prop.3.1 に現れる:

```text
(-1)^((p+k)h)
(-1)^(ph)
```

などを lossless に保持する必要がある。

候補:

```text
ScalarExpression
├── ScalarInteger
├── ScalarSymbol
├── ScalarSum
├── ScalarProduct
└── ScalarPower
```

ただし general-purpose CAS は作らない。

Prop.3.1 の concrete formula に必要な最小 structure のみ導入する。

---

# 10. parity reduction candidate

`(-1)^n` は sign indeterminacy ではなく parity により値が決まる symbolic scalar expression とする。

候補 rule:

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

さらに必要なら:

```text
n even
↓
(-1)^n a=a
```

```text
n odd
↓
(-1)^n a=-a
```

へ接続する。

Phase 16 の既存 parity / congruence machinery を再利用できるかを先に確認する。

---

# 11. IteratedSuspension

`IteratedSuspension` は既に実装済み。

[Toda] Prop.3.1 では:

```text
E^q a
E^(p+k)b
E^p b
E^(q+h)a
```

が現れる。

したがって新しい representation を作る前に existing `IteratedSuspension` で formula を lossless に表現できるか確認する。

不足する場合のみ:

```text
typing
symbolic exponent interaction
nested expression compatibility
```

を最小拡張する。

---

# 12. Barratt–Hilton theorem candidate

prerequisite が揃った後に [Toda] Prop.3.1 を explicit theorem rule として導入する。

重要:

```text
SmashProduct
↛
Barratt-Hilton
```

theorem knowledge は explicit domain rule として追加する。

また Prop.3.1 を general-purpose smash algebra に一般化しない。

---

# 13. Toda (2.1) foundational composition laws

将来必要:

```text
a ∘ (b₁ ± b₂)
=
a ∘ b₁ ± a ∘ b₂
```

```text
(a₁ ± a₂) ∘ Eb
=
a₁ ∘ Eb ± a₂ ∘ Eb
```

特に:

```text
k(a∘b)=a∘(kb)
```

```text
k(a∘Eb)=(ka)∘Eb
```

ただし unrestricted bidirectional rewrite は expression growth / loop を起こし得る。

actual proof scenario が要求した時点で staged / directed rule として導入する。

---

# 14. Toda (5.1) foundational sphere-group facts

known facts candidate:

```text
π_i(S¹)=0  (i>1)

π_i(S^n)=0  (i<n)

π_n(S^n)=Z{ι_n}
```

これらは foundational known-fact layer として将来利用できる。

ただし Phase 33 で直接必要でなければ先取りしない。

---

# 15. actual H calculation

Toda Prop.3.1 と必要な additive / scalar / composition machinery が揃った後:

```text
H((2ι₂)η₂)
```

の actual evaluation を行う。

目標:

```text
H((2ι₂)η₂)=4ι₃
```

さらに:

```text
H(4η₂)=4ι₃
```

を導出し:

```text
H((2ι₂)η₂)=H(4η₂)
```

へ接続する。

---

# 16. equality reflection reuse

新しい injectivity mechanism は不要。

Phase 29 の:

```text
actual Isomorphism(H)
↓
Injective(H)
```

と Phase 28 の:

```text
Injective(H)
+
H(a)=H(b)
↓
a=b
```

を再利用する。

目標:

```text
H((2ι₂)η₂)=H(4η₂)
↓
(2ι₂)η₂=4η₂
```

---

# 17. preimage / kernel-modulo reasoning

将来候補:

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

また:

```text
f(a)=f(b)
↓
a-b ∈ Ker(f)
↓
a≡b mod Ker(f)
```

は Phase 13–15 の machinery を優先的に再利用する。

---

# 18. stable homotopy groups

stable context:

```text
α ∈ π_k^S
```

は unstable:

```text
α ∈ π_m(S^n)
```

と別 representation にする。

notation-only conversion は行わず stabilization theorem を explicit bridge とする。

---

# 19. stable Toda brackets

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

# 20. higher Toda brackets

higher / variable-arity brackets は concrete literature example が必要になるまで deferred。

---

# 21. 実装状況

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
| generator fact repository | IMPLEMENTED | Phase 25 |
| actual Toda-generator typing | IMPLEMENTED | Phase 26 |
| corrected ε₃ proof chain | IMPLEMENTED | Phase 27 |
| map injectivity / isomorphism | IMPLEMENTED | Phase 28 |
| actual H facts / typing | IMPLEMENTED | Phase 29 |
| Toda Prop.2.2 right direct theorem | IMPLEMENTED | Phase 30 |
| `SmashProduct` | IMPLEMENTED | Phase 31 |
| Toda Prop.2.2 left direct theorem | IMPLEMENTED | Phase 32 |
| symbolic scalar `(-1)^n` | NEXT CANDIDATE | Phase 33 |
| parity reduction of `(-1)^n` | PLANNED | Phase 33+ |
| Barratt–Hilton Prop.3.1 | PLANNED | prerequisites 後 |
| actual H calculation | PLANNED | Prop.3.1 後 |
| `H((2ι₂)η₂)=H(4η₂)` | PLANNED | actual H calculation 後 |
| `(2ι₂)η₂=4η₂` | PLANNED | existing equality reflection を再利用 |
| Toda (2.1) | PLANNED | concrete need 時 |
| Toda (5.1) | PLANNED | concrete need 時 |
| stable homotopy group | PLANNED | later |
| stable Toda bracket | PLANNED | later |
| higher Toda bracket | DEFERRED | concrete need required |

---

# 22. 長期 dependency

```text
Phase 29
actual H equality-reflection foundation
↓
Phase 30
Toda Prop.2.2 right COMPLETE
↓
Phase 31
SmashProduct minimum representation COMPLETE
↓
Phase 32
Toda Prop.2.2 left COMPLETE
↓
Phase 33+
Barratt-Hilton prerequisites
↓
Toda Prop.3.1
↓
actual H((2ι₂)η₂) calculation
↓
H((2ι₂)η₂)=H(4η₂)
↓
(2ι₂)η₂=4η₂
↓
preimage / kernel-modulo reasoning as needed
↓
general theorem representation as needed
↓
stable homotopy representation
↓
stable Toda bracket
```

actual theorem scenario に応じて後続 Phase の番号・順序は調整してよい。

---

# 23. テスト / representative demonstration 原則

各 layer で:

1. representation
2. structural distinction
3. validity / applicability
4. invalid-case behavior
5. typing compatibility
6. integration
7. provenance
8. representative scenario
9. termination / scope
10. full regression
11. representative executable demonstration

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

---

# 24. Phase 32 完了時点

focused:

```text
tests/test_phase30_prop22.py
25 passed

tests/test_phase32_prop22.py
39 passed

tests/test_hopf_rules.py
31 passed

tests/test_map_facts.py
54 passed
```

full suite:

```text
1512 passed in 63.58s
```

No failures.

---

# 25. 次の直接的候補

推奨:

```text
Phase 33
Barratt-Hilton prerequisite minimum representation
```

最初に [Toda] Prop.3.1 の concrete formula を structural に再確認し、次の順に不足を確認する。

```text
existing IteratedSuspension
existing additive expressions
existing symbolic scalar constraints
existing SmashProduct
↓
不足している最小 syntax / rule のみ追加
```

現時点の最有力不足:

```text
(-1)^n
```

の symbolic scalar-expression representation と parity reduction。
