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

# 2. Phase 25 完了時点の実装基盤

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
Indexed Toda theorem / validity connection
Literature-backed theorem fact repository
Explicit generator typing facts
Explicit generator ambient-group facts
Generator fact repository
Typed-element materialization from explicit facts
Toda entry typing integration
Representative human-readable capability probe
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
```

---

# 5. Phase 25 completion

Implemented:

```text
GeneratorTypingFact
GeneratorAmbientGroupFact
GeneratorFactRepository
```

Representative:

```text
η₃ : S⁴ → S³
η₃ ∈ π₄(S³)
```

Production data:

```text
ETA_3_GENERATOR
ETA_3_TYPING_FACT
ETA_3_AMBIENT_GROUP_FACT
GENERATOR_FACT_REPOSITORY
```

Main chain:

```text
GeneratorSymbol
+
explicit typing fact
↓
repository lookup
↓
new typed HomotopyElement
↓
existing Toda compatibility
```

Boundary:

```text
GeneratorSymbol.index
↛
automatic typing
```

```text
GeneratorAmbientGroupFact
↛
source / target typing
```

```text
generator repository
!=
theorem repository
```

Verified:

```text
tests/test_generator_facts.py
55 passed
```

```text
full suite
1245 passed
```

Representative capability demo:

```powershell
python -m probes.probe_phase25_capabilities
```

Visible current results:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
η₃ : S⁴ → S³
η₃ ∈ π₄(S³)
```

Current visible boundary:

```text
ν′ / ν₇ production typing
repository-derived Eν′ typing
complete ε₃ Toda entry typing
```

remain future work.

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
| η₃ generator facts | IMPLEMENTED | Phase 25 |
| generator fact repository | IMPLEMENTED | Phase 25 |
| exact generator lookup | IMPLEMENTED | Phase 25 |
| typed-element materialization | IMPLEMENTED | Phase 25 |
| duplicate generator-fact rejection | IMPLEMENTED | Phase 25 |
| Toda entry typing connection | IMPLEMENTED | Phase 25 |
| representative capability demo convention | IMPLEMENTED | post-Phase 25 documentation / probe |
| generator-fact literature provenance | NEXT CANDIDATE | Phase 26 candidate |
| ν′ / ν₇ production typing facts | PLANNED | actual Toda requirement |
| typing ↔ ambient consistency validation | PLANNED | actual validation need |
| nested Suspension typing from repository | PLANNED | actual expression need |
| name / generator validation | PLANNED | explicit validation layer |
| external generator-table loader | PLANNED | actual file-loading need |
| general theorem representation | PLANNED | quantified theorem need |
| stable homotopy group `π_k^S` | PLANNED | stable context |
| stable Toda bracket `<a,b,c>` | PLANNED | stable layer |
| higher Toda bracket | DEFERRED | concrete need required |

---

# 7. Phase 26 candidate

Natural candidate:

```text
Phase 26
Generator fact provenance / actual Toda-generator typing expansion
```

Possible first actual requirement:

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

Alternative:

```text
ν′ / ν₇ typing facts
↓
explicit materialization
↓
actual ε₃ Toda entry typing
```

Do not implement both automatically unless the actual requirement needs both.

---

# 8. Additional production generator facts

Current production fact coverage:

```text
η₃
```

Potential needs:

```text
ν′
ν₇
μ₃
ι₇
```

Add only facts required by concrete theorem / proof scenarios.

Do not create a family formula solely because notation has an index.

---

# 9. Nested expression typing

Potential future requirement:

```text
GeneratorSymbol
↓
typed HomotopyElement
↓
Suspension
↓
shifted source / target
```

Reuse existing Suspension semantics after explicit base-element materialization.

Do not introduce recursive global expression inference prematurely.

---

# 10. Typing / ambient-group consistency

Current separate facts:

```text
GeneratorTypingFact(source,target)
GeneratorAmbientGroupFact(group_dimension,sphere_dimension)
```

No rule currently asserts:

```text
source == group_dimension
target == sphere_dimension
```

A future explicit consistency predicate may be introduced when required.

---

# 11. Stable homotopy groups

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

# 12. Stable Toda brackets

Stable notation:

```text
<a,b,c>
```

must remain distinct from unstable:

```text
{a,b,c}
```

---

# 13. Higher Toda brackets

Higher / variable-arity brackets remain deferred until concrete literature examples require them.

---

# 14. Long-term dependency suggestion

```text
Phase 25
explicit generator facts
↓
Phase 26 candidate
generator fact provenance / additional actual typing facts
↓
explicit nested generator-expression typing
↓
actual Toda theorem typing expansion
↓
ambient / stem validation when needed
↓
stable homotopy representation
↓
stable Toda bracket
```

At each suitable Phase boundary, also grow a representative executable proof / validation scenario so that the visible mathematical chain becomes deeper rather than only increasing internal API coverage.

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

# 15. Testing and representative-demonstration principle

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

In addition, when the Phase has a meaningful human-visible mathematical result:

10. provide or extend a representative probe,
11. run it from the project root,
12. show the premises / registered facts,
13. show the applied inference or validation,
14. show the mathematical conclusion,
15. show the previous-Phase difference,
16. show the remaining Phase boundary.

Tests and probes have different purposes:

```text
pytest
=
correctness / regression

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

# 16. Documentation policy

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

# 17. 長期目標

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
