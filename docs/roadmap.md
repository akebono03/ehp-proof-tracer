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
