# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to explain how homotopy groups of spheres are determined from mathematical input such as EHP exact sequences, element orders, additive relations, Suspension, Freudenthal theory, composition, generalized Hopf invariants, homomorphisms, subgroup / modulo information, symbolic scalar constraints, indeterminacy, Toda brackets, typed homotopy elements, structured generator notation, literature-backed theorem repositories, explicit generator facts, and later stable-homotopy information.

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

Current architecture:

```text
literature-backed theorem facts / repository
explicit generator facts / repository
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

Phase 21 adds minimal source / target context and compatibility queries. Phase 22 adds structured generator identity while keeping generator notation separate from typing rules. Phase 23 connects indexed Toda theorem facts to membership under explicit guards. Phase 24 adds a narrow literature-backed theorem repository. Phase 25 adds a separate explicit generator-fact repository and typed-element materialization without changing `GeneratorSymbol` semantics or the generic inference engine.

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

# Phase 24: Theorem fact / knowledge-table integration

Phase 24 introduces:

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

# Phase 25: Generator typing / ambient-group facts

Phase 25 introduces an explicit knowledge layer connecting structured generator identity to typing and ambient unstable homotopy-group context.

Core principle:

```text
GeneratorSymbol
+
explicit registered fact
↓
exact structural lookup
↓
explicit materialization
↓
typed HomotopyElement
```

not:

```text
GeneratorSymbol.index
↓
automatic formula
↓
typing
```

## Generator typing fact

```text
GeneratorTypingFact
├── generator: GeneratorSymbol
├── source: int
└── target: int
```

Representative:

```text
η₃ : S⁴ → S³
```

stored as `ETA_3_TYPING_FACT`.

## Ambient-group fact

```text
GeneratorAmbientGroupFact
├── generator: GeneratorSymbol
├── group_dimension: int
└── sphere_dimension: int
```

Representative:

```text
η₃ ∈ π₄(S³)
```

stored as `ETA_3_AMBIENT_GROUP_FACT`.

Typing facts and ambient-group facts are distinct knowledge families.

```text
typing fact
!=
ambient-group fact
```

No automatic conversion between them is introduced.

## Representative generator identity

```text
ETA_3_GENERATOR
=
GeneratorSymbol(family="η", index=3)
```

Both representative facts share this identity.

## Generator fact repository

Phase 25 adds `GeneratorFactRepository` with:

```text
typing_facts
ambient_group_facts
```

and explicit lookup:

```text
lookup_typing(generator)
lookup_ambient_group(generator)
```

Production repository:

```text
GENERATOR_FACT_REPOSITORY
```

contains the representative η₃ facts.

Lookup is exact structural lookup:

```text
η₃ → match
η₄ → no match
η → no match
μ₃ → no match
```

`index=None` is not a wildcard.

## Typed-element materialization

Phase 25 adds:

```text
GeneratorFactRepository.materialize_typed_element()
```

Representative chain:

```text
untyped HomotopyElement
+
GENERATOR_FACT_REPOSITORY
↓
lookup_typing(η₃)
↓
ETA_3_TYPING_FACT
↓
new typed HomotopyElement
```

The original element is not mutated. Existing or partial typing is not overwritten or implicitly completed. Unknown generators return `None`. Ambient-group facts alone do not materialize source / target typing.

## Toda entry integration

```text
explicit GeneratorTypingFact
↓
GeneratorFactRepository
↓
typed HomotopyElement entries
↓
TodaBracket
↓
are_defining_compositions_type_compatible()
```

No repository lookup is embedded into `TodaBracket`. No recursive automatic expression typing is introduced.

## Repository uniqueness

Within each fact family, a generator may appear at most once.

```text
same generator + two typing facts
→ ValueError
```

```text
same generator + two ambient-group facts
→ ValueError
```

However:

```text
same generator
+
one typing fact
+
one ambient-group fact
→ allowed
```

## Scope / provenance boundary

Current generator-fact provenance is explicit data provenance:

```text
typed HomotopyElement
← materialize_typed_element()
← registered GeneratorTypingFact
← GeneratorFactRepository
```

The generator fact layer does not yet attach `LiteratureReference`, create `ProofStep`, or invoke inference.

Important:

```text
HomotopyElement.name
↛
generator lookup
```

```text
materialization
↛
repository mutation
↛
new fact generation
↛
inference-engine execution
```

```text
generator fact repository
!=
theorem fact repository
```

---

# Phase 25 completion boundary

Implemented:

1. `GeneratorTypingFact`.
2. exact generator matching for typing facts.
3. `GeneratorAmbientGroupFact`.
4. η₃ representative generator identity.
5. η₃ typing representative.
6. η₃ ambient-group representative.
7. `GeneratorFactRepository`.
8. production `GENERATOR_FACT_REPOSITORY`.
9. exact structural typing lookup.
10. exact structural ambient-group lookup.
11. unknown lookup returns `None`.
12. explicit typed-element materialization.
13. non-mutating materialization.
14. already typed element is not overwritten.
15. partially typed element is not implicitly completed.
16. typing facts and ambient-group facts remain distinct.
17. duplicate generator facts are rejected within each fact family.
18. same generator may occur once in each fact family.
19. fact-derived typed entries participate in existing Toda type compatibility.
20. lookup preserves registered fact identity.
21. unrelated facts do not affect η₃ materialization.
22. `HomotopyElement.name` is not a lookup key.
23. ambient-group fact alone does not create typing.
24. materialization does not mutate repository state.
25. generator materialization does not modify theorem repository state.
26. no generator-specific inference rule is added.
27. no recursive expression typing is added.
28. no automatic η_n / ν_n typing formula is added.
29. no typing / ambient cross-family consistency rule is added.
30. generic inference engine remains unchanged.
31. full regression passes.

---

# Current limitations

Not yet implemented as general systems:

- literature provenance on generator typing / ambient-group facts,
- `ProofStep` representation for generator facts,
- external generator-table loading,
- stable fact key / fact ID system for generator facts,
- name / generator consistency validation,
- generator / `HomotopyElement.dimension` consistency validation,
- typing / ambient-group cross-family consistency validation,
- automatic source / target derivation from generator notation,
- general η_n / ν_n / μ_n / ι_n typing formulas,
- recursive typing of arbitrary nested expressions,
- automatic typing of `Suspension(ν′)` from a base-generator repository entry,
- full production typing facts for `ν′`, `ν₇`, and the complete ε₃ Toda bracket,
- ambient homotopy-group validation of expressions,
- stem / stable-context classification,
- general theorem quantification,
- stable homotopy-group model,
- stable Toda bracket `<a,b,c>`,
- higher / variable-arity Toda brackets.

---

# Tests

Focused Phase 25 generator-fact suite:

```powershell
python -m pytest tests/test_generator_facts.py -q
```

Verified Phase 25 completion:

```text
55 passed in 2.25s
```

Full suite:

```powershell
python -m pytest -q
```

Verified Phase 25 completion:

```text
1245 passed in 65.71s
```

No failures.

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capabilities and dependency order

Historical statements in the development log describe the state at that time. Current behavior is defined by the latest README and design documents.

---

# Next development boundary

Natural next candidate:

```text
Phase 26
Generator fact provenance / actual Toda-generator typing expansion
```

Strong candidates:

```text
A. attach LiteratureReference to generator facts
B. register actual ν′ / ν₇ typing facts needed by ε₃ Toda notation
C. validate typing fact ↔ ambient-group fact consistency
D. type Suspension / nested Toda entries from explicit generator facts
```

These should not all be implemented at once. Stable homotopy groups and stable Toda brackets remain later layers.
