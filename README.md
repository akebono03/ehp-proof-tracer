# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to explain how homotopy groups of spheres are determined from mathematical input such as EHP exact sequences, element orders, additive relations, Suspension, Freudenthal theory, composition, generalized Hopf invariants, homomorphisms, subgroup / modulo information, symbolic scalar constraints, indeterminacy, Toda brackets, typed homotopy elements, structured generator notation, literature-backed theorem repositories, explicit generator and composition facts, and later stable-homotopy information.

The project separates:

```text
mathematical rule / theorem
knowledge / fact supply
generic inference mechanism
abelian-group calculation
```

Development principle:

```text
actual mathematical need
↓
minimal representation
↓
explicit fact / domain rule when needed
↓
existing generic engine
```

---

# Current status

Completed:

- Phase 1: finite abelian-group calculations
- Phase 2: structured subgroup calculations
- Phase 3: quotient / exact sequence / extension
- Phase 4: presentation-based finitely generated abelian groups
- Phase 5: generic proof / inference engine
- Phase 6: EHP domain inference
- Phase 7: ORDER reasoning
- Phase 8: Suspension reasoning
- Phase 9: Freudenthal / stable-range reasoning
- Phase 10: composition / Suspension-composition functoriality
- Phase 11: generalized Hopf-invariant reasoning
- Phase 12: additive expressions
- Phase 13: homomorphism reasoning
- Phase 14: set / subgroup reasoning
- Phase 15: coset / modulo reasoning
- Phase 16: symbolic scalar constraints
- Phase 17: indeterminacy
- Phase 18: Toda bracket minimum representation
- Phase 19: Toda membership / first theorem bridge
- Phase 20: indexed unstable Toda notation
- Phase 21: typed homotopy elements / source-target context
- Phase 22: structured generator representation
- Phase 23: indexed Toda theorem / validity connection
- Phase 24: theorem fact / knowledge-table integration
- Phase 25: generator typing / ambient-group facts
- Phase 26: actual Toda-generator typing expansion
- Phase 27: corrected actual ε₃ Toda-definedness / end-to-end inference

Current architecture:

```text
literature-backed theorem facts / repository
explicit generator facts / repository
explicit composition facts / repository
        ↓
homotopy / EHP domain rules
        ↓
generic proof / inference engine
        ↓
proof-level expression / scalar / set / subgroup / modulo /
indeterminacy / Toda statements
        ↓
homotopy / EHP data layer
        ↓
finitely generated abelian-group algebra
        ↓
integer linear algebra
```

---

# Expression model

Current expression classes include:

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Sum
├── Composition
├── MapApplication
├── Suspension
└── IteratedSuspension
```

Separate structural objects include:

```text
MapSymbol
ScalarSymbol
GeneratorSymbol
TodaBracket
IndexedTodaBracketData
```

Phase 21 adds minimal source / target context and compatibility queries. Phase 22 adds structured generator identity while keeping generator notation separate from typing rules. Phase 23 connects indexed Toda theorem facts to membership under explicit guards. Phase 24 adds a narrow literature-backed theorem repository. Phase 25 adds a separate explicit generator-fact repository and typed-element materialization. Phase 26 expands this knowledge to the actual generators appearing in the ε₃ Toda bracket. Phase 27 adds explicit corrected composition knowledge and connects it to actual indexed Toda definedness and theorem-backed membership.

---

# Structured generator representation

`GeneratorSymbol` stores:

```text
family: str
index: int | None
decoration: str | None
```

Examples:

```text
ν
ν′
barν
η₃
μ₃
ι₇
```

Critical boundary:

```text
GeneratorSymbol.index
↛
automatic source / target typing
```

Typing is supplied only through explicit registered facts.

---

# Phase 24: theorem fact / knowledge-table integration

Phase 24 introduced:

```text
TheoremFactEntry
TheoremFactRepository
```

Representative:

```text
EPSILON_3_TODA_MEMBERSHIP_FACT
THEOREM_FACT_REPOSITORY
```

Main chain:

```text
literature-backed theorem data
↓
TheoremFactRepository
↓
lookup
↓
TheoremFactEntry
↓
materialize_statement()
↓
ProofStep.GIVEN
+
matching TodaBracketDefinedStatement
↓
existing Toda theorem rule
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Boundary:

```text
repository fact
!=
membership
```

```text
lookup success
!=
theorem applicability
```

---

# Phase 25: generator typing / ambient-group facts

Phase 25 introduced an explicit knowledge layer connecting structured generator identity to typing and ambient unstable homotopy-group context.

Core structures:

```text
GeneratorTypingFact
GeneratorAmbientGroupFact
GeneratorFactRepository
GENERATOR_FACT_REPOSITORY
```

Representative:

```text
η₃ : S⁴ → S³
η₃ ∈ π₄(S³)
```

Critical:

```text
typing fact
!=
ambient-group fact
```

No automatic conversion is performed between them.

---

# Phase 26: actual Toda-generator typing expansion

Production generator coverage:

```text
η₃ : S⁴ → S³
η₃ ∈ π₄(S³)

ν′ : S⁶ → S³
ν′ ∈ π₆(S³)

ν₇ : S¹⁰ → S⁷
ν₇ ∈ π₁₀(S⁷)
```

Existing Suspension semantics connects:

```text
ν′ : S⁶ → S³
↓
Suspension
↓
Eν′ : S⁷ → S⁴
```

The actual typed entries can therefore be assembled as:

```text
η₃  : S⁴  → S³
Eν′ : S⁷  → S⁴
ν₇  : S¹⁰ → S⁷
```

and:

```text
{η₃,Eν′,ν₇}_1
```

has type-compatible displayed adjacent compositions:

```text
η₃ ∘ Eν′
Eν′ ∘ ν₇
```

Critical boundary retained in Phase 27:

```text
type-compatible
!=
composition is zero
!=
Toda bracket is defined
```

---

# Phase 27: corrected actual ε₃ Toda-definedness bridge

Phase 27 deepens the same actual ε₃ proof chain using explicit mathematical knowledge.

## Corrected primitive facts

The production primitive zero-composition facts are:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
```

The production Suspension identification is:

```text
Eν₆ = ν₇
```

These are represented by:

```text
ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
E_NU_6_EQUALS_NU_7_FACT
```

The zero-composition repository is:

```text
ZERO_COMPOSITION_FACT_REPOSITORY
```

and stores only the primitive zero-composition facts.

`E_NU_6_EQUALS_NU_7_FACT` is an equality fact and is intentionally not stored as a zero-composition fact.

## Important corrected indexed condition

For the indexed bracket:

```text
{η₃,Eν′,ν₇}_1
```

the second defining condition is not treated as a primitive displayed-adjacent fact

```text
Eν′ ∘ ν₇ = 0
```

Instead, the corrected actual indexed condition is:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
```

which derives:

```text
{η₃,Eν′,ν₇}_1 is defined
```

through:

```text
indexed_toda_bracket_index1_defined_inference_rule()
```

The rule captures the structural pattern:

```text
a ∘ Eb = 0
b ∘ c = 0
Ec = d
↓
{a,Eb,d}_1 is defined
```

## Zero-composition fact lookup

`ZeroCompositionFactRepository` supports:

```text
lookup()
```

for exact structural lookup and:

```text
lookup_by_untyped_structure()
```

for the narrow typed/untyped bridge needed by Phase 27.

The structure lookup ignores source / target typing annotations only. It still preserves:

```text
name
dimension
generator identity
Suspension structure
composition structure
```

Therefore typed actual expressions can be matched against stored untyped mathematical facts without making `None` a wildcard in general structural equality.

## Actual definedness derivation

Production proof inputs:

```text
GIVEN
η₃ ∘ Eν′ = 0

GIVEN
ν′ ∘ ν₆ = 0

GIVEN
Eν₆ = ν₇
```

derive:

```text
INFERENCE
{η₃,Eν′,ν₇}_1 is defined
```

The derived `ProofStep` preserves all three corrected premises.

## Corrected end-to-end theorem connection

The theorem repository supplies:

```text
GIVEN
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

as a literature-backed theorem statement.

A single fixed-point run over:

```text
indexed_toda_bracket_index1_defined_inference_rule()
toda_bracket_membership_from_theorem_inference_rule()
```

with the four production inputs:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
Toda theorem fact
```

derives:

```text
Round 1
{η₃,Eν′,ν₇}_1 is defined

Round 2
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

and terminates at:

```text
InferenceTerminationReason.FIXED_POINT
```

with:

```text
round_count = 2
```

## Provenance

The final membership step has direct premises:

```text
theorem_step
derived_definedness_step
```

The derived definedness step has direct premises:

```text
ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
E_NU_6_EQUALS_NU_7_FACT
```

Therefore the visible proof graph is:

```text
η₃ ∘ Eν′ = 0 ───────────────┐
                              │
ν′ ∘ ν₆ = 0 ─────────────────┼──→ {η₃,Eν′,ν₇}_1 defined
                              │              │
Eν₆ = ν₇ ────────────────────┘              │
                                             ├──→ ε₃ ∈ {η₃,Eν′,ν₇}_1
Toda theorem fact ────────────────────────────┘
```

Unrelated facts are excluded from the provenance chain.

## Regression / scope boundaries

Phase 27 fixes the following boundaries:

```text
displayed adjacent entries
↛
indexed defining conditions automatically
```

```text
Eν′ ∘ ν₇ = 0
↛
accepted as a substitute primitive condition
```

```text
typed structure lookup
↛
general wildcard structural equality
```

```text
inference execution
↛
ZERO_COMPOSITION_FACT_REPOSITORY mutation
```

```text
inference execution
↛
THEOREM_FACT_REPOSITORY mutation
```

```text
unrelated fact
↛
definedness provenance
```

```text
unrelated fact
↛
membership provenance
```

Derived actual definedness and membership are deduplicated, and the terminal inference round has no new steps.

Generic inference engine remains unchanged.

---

# Phase 27 completion boundary

Implemented:

1. explicit primitive fact `η₃ ∘ Eν′ = 0`.
2. explicit primitive fact `ν′ ∘ ν₆ = 0`.
3. explicit equality fact `Eν₆ = ν₇`.
4. `ZeroCompositionFactRepository`.
5. production registration of the two primitive zero-composition facts.
6. exact zero-composition lookup.
7. narrow typed/untyped structural lookup.
8. structure lookup that ignores only typing annotations.
9. rejection of mismatched generator / name / Suspension structure.
10. corrected indexed Toda definedness rule.
11. actual derivation of `{η₃,Eν′,ν₇}_1` definedness.
12. three-premise definedness provenance.
13. rejection of primitive `Eν′ ∘ ν₇ = 0` as the indexed defining substitute.
14. connection to `THEOREM_FACT_REPOSITORY`.
15. actual theorem-backed membership derivation.
16. corrected single-run end-to-end inference.
17. two-round fixed-point chain.
18. final membership provenance through theorem fact + derived definedness.
19. unrelated-fact provenance exclusion.
20. repository non-mutation regression.
21. derived-conclusion deduplication.
22. genuine terminal fixed-point regression.
23. human-readable Phase 27 capability probe.
24. generic inference engine unchanged.
25. full regression passes.

---

# Current limitations

Not yet implemented as general systems:

- literature provenance on generator typing / ambient-group facts,
- literature provenance on composition facts,
- `ProofStep` representation for generator facts,
- external generator-table loading,
- external composition-fact-table loading,
- stable fact key / fact ID system,
- name / generator consistency validation,
- generator / `HomotopyElement.dimension` consistency validation,
- automatic source / target derivation from generator notation,
- general η_n / ν_n / μ_n / ι_n typing formulas,
- recursive typing of arbitrary nested expressions,
- ambient homotopy-group validation of arbitrary expressions,
- automatic zero-composition facts from type compatibility,
- general indexed Toda definedness for arbitrary index,
- general theorem quantification,
- automatic theorem instantiation,
- proof-level map injectivity / isomorphism statements,
- preimage reasoning,
- general kernel-modulo equality shortcut,
- symbolic scalar expression trees such as `(-1)^n`,
- smash-product expressions,
- stable homotopy-group model,
- stable Toda bracket `<a,b,c>`,
- higher / variable-arity Toda brackets.

---

# Tests

Focused Phase 27 theorem connection suite:

```powershell
python -m pytest tests/test_phase27_theorem_connection.py -q
```

Verified:

```text
11 passed in 0.69s
```

Related suites:

```powershell
python -m pytest tests/test_phase27_toda_definedness.py -q
python -m pytest tests/test_composition_facts.py -q
python -m pytest tests/test_toda_rules.py -q
```

Latest verified counts during Phase 27:

```text
tests/test_phase27_toda_definedness.py
4 passed

tests/test_composition_facts.py
27 passed

tests/test_toda_rules.py
66 passed
```

Full suite:

```powershell
python -m pytest -q
```

Verified at Phase 27 completion:

```text
1332 passed in 86.87s
```

No failures.

---

# Representative capability demos

Phase 25:

```powershell
python -m probes.probe_phase25_capabilities
```

Phase 26:

```powershell
python -m probes.probe_phase26_capabilities
```

Phase 27:

```powershell
python -m probes.probe_phase27_capabilities
```

The Phase 27 probe visibly demonstrates:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
↓
{η₃,Eν′,ν₇}_1 is defined
+
Toda theorem fact
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

It also explicitly shows:

```text
Eν′ ∘ ν₇ = 0
```

is not used as primitive defining knowledge.

The probe reuses production facts, repositories, inference rules, and the generic fixed-point engine. It does not contain a second implementation of the mathematics.

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capabilities and dependency order

Historical statements in the development log describe the state at that time. Current behavior is defined by the latest README and design documents.

---

# Next development boundary

Phase 27 completes the first corrected end-to-end actual ε₃ Toda proof chain.

A natural next direction is to begin one of the map-theoretic proof capabilities already identified in the roadmap, while still following actual mathematical need.

Strong candidates include:

```text
A. map typing / injectivity / isomorphism
B. equality reflection through an injective map
C. generator / expression validation
D. literature provenance for generator / composition facts
```

The map-theoretic direction is especially useful for future proofs of the form:

```text
H(a) = H(b)
+
H injective / isomorphism
↓
a = b
```

and for representative Toda-style calculations such as:

```text
(2ι₂)η₂ = 4η₂
P(ι₅) = ±2η₂
```

Stable homotopy groups and stable Toda brackets remain later layers.
