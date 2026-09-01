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
- Phase 26: actual Toda-generator typing expansion

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

Phase 21 adds minimal source / target context and compatibility queries. Phase 22 adds structured generator identity while keeping generator notation separate from typing rules. Phase 23 connects indexed Toda theorem facts to membership under explicit guards. Phase 24 adds a narrow literature-backed theorem repository. Phase 25 adds a separate explicit generator-fact repository and typed-element materialization. Phase 26 expands this explicit knowledge to the actual generators appearing in the ε₃ Toda bracket and connects them to existing Suspension and Toda type-compatibility semantics.

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

# Phase 25: Generator typing / ambient-group facts

Phase 25 introduced an explicit knowledge layer connecting structured generator identity to typing and ambient unstable homotopy-group context.

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
automatic family formula
↓
typing
```

Core structures:

```text
GeneratorTypingFact
GeneratorAmbientGroupFact
GeneratorFactRepository
GENERATOR_FACT_REPOSITORY
```

Phase 25 representative data:

```text
η₃ : S⁴ → S³
η₃ ∈ π₄(S³)
```

Typing facts and ambient-group facts are distinct knowledge families.

```text
typing fact
!=
ambient-group fact
```

No automatic conversion is performed between them.

---

# Phase 26: actual Toda-generator typing expansion

Phase 26 connects the Phase 25 generator-fact layer to the actual bracket used by the ε₃ theorem fact:

```text
{η₃,Eν′,ν₇}_1
```

The Phase deliberately expands only the explicit generator knowledge needed by this concrete Toda bracket.

## ν′ generator facts

Production identity:

```text
NU_PRIME_GENERATOR
=
GeneratorSymbol(
  family="ν",
  decoration="′",
)
```

Explicit typing fact:

```text
ν′ : S⁶ → S³
```

Explicit ambient-group fact:

```text
ν′ ∈ π₆(S³)
```

Production constants:

```text
NU_PRIME_TYPING_FACT
NU_PRIME_AMBIENT_GROUP_FACT
```

## ν₇ generator facts

Production identity:

```text
NU_7_GENERATOR
=
GeneratorSymbol(
  family="ν",
  index=7,
)
```

Explicit typing fact:

```text
ν₇ : S¹⁰ → S⁷
```

Explicit ambient-group fact:

```text
ν₇ ∈ π₁₀(S⁷)
```

Production constants:

```text
NU_7_TYPING_FACT
NU_7_AMBIENT_GROUP_FACT
```

## Production repository coverage

`GENERATOR_FACT_REPOSITORY` now contains typing and ambient-group facts for:

```text
η₃
ν′
ν₇
```

Typing lookup:

```text
η₃ → η₃ : S⁴ → S³
ν′ → ν′ : S⁶ → S³
ν₇ → ν₇ : S¹⁰ → S⁷
```

Ambient lookup:

```text
η₃ → η₃ ∈ π₄(S³)
ν′ → ν′ ∈ π₆(S³)
ν₇ → ν₇ ∈ π₁₀(S⁷)
```

Lookup remains exact structural lookup. Registered `ν₇` does not imply a formula for `ν₈`, `ν₉`, or arbitrary `ν_n`.

## Explicit Eν′ typing connection

Phase 26 does not add recursive repository typing.

Instead it explicitly composes existing layers:

```text
NU_PRIME_TYPING_FACT
↓
GENERATOR_FACT_REPOSITORY
↓
materialize_typed_element()
↓
ν′ : S⁶ → S³
↓
existing Suspension semantics
↓
Eν′ : S⁷ → S⁴
```

An unmaterialized `ν′` remains untyped under Suspension.

```text
Suspension(untyped ν′)
→ source=None
→ target=None
```

Therefore the typing still depends on explicit registered knowledge.

## Actual typed ε₃ Toda entries

Phase 26 can build:

```text
η₃  : S⁴  → S³
Eν′ : S⁷  → S⁴
ν₇  : S¹⁰ → S⁷
```

from production generator facts and existing Suspension semantics.

These entries can then be assembled as:

```text
TodaBracket(
  first=typed η₃,
  second=typed Eν′,
  third=typed ν₇,
  index=1,
)
```

which represents the actual indexed Toda notation:

```text
{η₃,Eν′,ν₇}_1
```

The typed representation preserves the same generator identities and index as the theorem-side actual bracket notation, while source / target annotations make the typed bracket structurally different from the untyped theorem-side bracket.

## Actual Toda type compatibility

The existing compatibility query is used without modification:

```text
TodaBracket.are_defining_compositions_type_compatible()
```

For the actual ε₃ bracket:

```text
η₃.source = 4
Eν′.target = 4
```

and:

```text
Eν′.source = 7
ν₇.target = 7
```

Therefore both defining compositions are type-compatible:

```text
η₃ ∘ Eν′
Eν′ ∘ ν₇
```

and:

```text
{η₃,Eν′,ν₇}_1
→ defining compositions are type-compatible
```

Critical boundary:

```text
type-compatible
!=
composition is zero
!=
Toda bracket is defined
```

Phase 26 does not derive zero compositions from typing.

## Typing / ambient-group consistency query

Phase 26 adds:

```text
GeneratorFactRepository.is_typing_ambient_group_consistent(generator)
```

Result semantics:

```text
True
=
both facts exist and
source == group_dimension and
target == sphere_dimension
```

```text
False
=
both facts exist but disagree
```

```text
None
=
one or both facts are missing
```

For production facts:

```text
η₃ → True
ν′ → True
ν₇ → True
```

The consistency query does not generate facts, repair facts, or reject a repository merely because the two fact families disagree.

## Phase 26 provenance and scope

Current provenance remains explicit data-path provenance:

```text
typed η₃
← ETA_3_TYPING_FACT
← GENERATOR_FACT_REPOSITORY
```

```text
typed Eν′
← Suspension
← typed ν′
← NU_PRIME_TYPING_FACT
← GENERATOR_FACT_REPOSITORY
```

```text
typed ν₇
← NU_7_TYPING_FACT
← GENERATOR_FACT_REPOSITORY
```

This is not `ProofStep` provenance.

Phase 26 regression fixes the following boundaries:

```text
lookup / materialization / compatibility
↛
generator repository mutation
```

```text
generator typing chain
↛
theorem repository mutation
```

```text
consistency query
↛
new fact generation
```

```text
ν₇ registered
↛
general ν_n typing formula
```

```text
data-path provenance
!=
ProofStep provenance
```

---

# Phase 26 completion boundary

Implemented:

1. `NU_PRIME_GENERATOR`.
2. `NU_PRIME_TYPING_FACT`.
3. `NU_PRIME_AMBIENT_GROUP_FACT`.
4. `NU_7_GENERATOR`.
5. `NU_7_TYPING_FACT`.
6. `NU_7_AMBIENT_GROUP_FACT`.
7. production repository registration for `η₃`, `ν′`, and `ν₇`.
8. production typing lookup for `ν′` and `ν₇`.
9. production ambient-group lookup for `ν′` and `ν₇`.
10. production materialization of typed `ν′` and `ν₇`.
11. explicit repository-derived `ν′` → typed `Eν′` connection using existing Suspension semantics.
12. actual typed entries `η₃`, `Eν′`, `ν₇`.
13. actual indexed `TodaBracket(..., index=1)` representative.
14. theorem-side notation identity connection at generator / index level.
15. compatibility of `η₃ ∘ Eν′`.
16. compatibility of `Eν′ ∘ ν₇`.
17. compatibility of the actual `{η₃,Eν′,ν₇}_1` defining compositions.
18. index / typing responsibility separation.
19. `is_typing_ambient_group_consistent()`.
20. `True / False / None` consistency semantics.
21. production consistency for `η₃`, `ν′`, `ν₇`.
22. repository non-mutation regression.
23. theorem repository non-mutation regression.
24. consistency-query non-generation regression.
25. no automatic `ν_n` family typing.
26. explicit data-path provenance regression.
27. generic inference engine unchanged.
28. full regression passes.

---

# Current limitations

Not yet implemented as general systems:

- literature provenance on generator typing / ambient-group facts,
- `ProofStep` representation for generator facts,
- external generator-table loading,
- stable fact key / fact ID system for generator facts,
- name / generator consistency validation,
- generator / `HomotopyElement.dimension` consistency validation,
- automatic source / target derivation from generator notation,
- general η_n / ν_n / μ_n / ι_n typing formulas,
- recursive typing of arbitrary nested expressions,
- repository API that automatically traverses `Suspension` or nested expressions,
- ambient homotopy-group validation of arbitrary expressions,
- automatic zero-composition facts from type compatibility,
- automatic Toda definedness from typing,
- generator-fact `LiteratureReference`,
- generator-fact `ProofStep` provenance,
- automatic connection from typed bracket validation to theorem applicability,
- stem / stable-context classification,
- general theorem quantification,
- stable homotopy-group model,
- stable Toda bracket `<a,b,c>`,
- higher / variable-arity Toda brackets.

---

# Tests

Focused theorem-fact suite:

```powershell
python -m pytest tests/test_theorem_facts.py -q
```

Focused generator-fact suite at Phase 26 completion:

```powershell
python -m pytest tests/test_generator_facts.py -q
```

Verified:

```text
100 passed in 0.39s
```

Full suite:

```powershell
python -m pytest -q
```

Verified:

```text
1290 passed in 23.16s
```

No failures.

---

# Representative capability demo

Phase completion includes a human-readable representative capability demo in addition to regression tests.

Phase 25 command:

```powershell
python -m probes.probe_phase25_capabilities
```

Phase 26 command:

```powershell
python -m probes.probe_phase26_capabilities
```

The Phase 26 probe should make visible:

```text
η₃ : S⁴ → S³
ν′ : S⁶ → S³
Eν′ : S⁷ → S⁴
ν₇ : S¹⁰ → S⁷
```

and:

```text
{η₃,Eν′,ν₇}_1
→ defining compositions are type-compatible
```

It should also retain the actual theorem-side result:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

while explicitly showing that:

```text
type compatibility
!=
Toda definedness
```

The probe reuses production APIs and existing inference rules; it does not contain a second implementation of the mathematics.

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capabilities and dependency order

Historical statements in the development log describe the state at that time. Current behavior is defined by the latest README and design documents.

---

# Next development boundary

Natural next candidates after Phase 26:

```text
A. generator-fact LiteratureReference / provenance
B. explicit zero-composition facts for the actual ε₃ Toda entries
C. actual Toda definedness connection from explicit zero-composition premises
D. name / dimension / generator validation
```

A strong next direction is to deepen the same actual ε₃ proof chain rather than widen generator coverage prematurely:

```text
typed actual entries
↓
explicit zero-composition knowledge
↓
Toda definedness
↓
existing theorem fact
↓
ε₃ membership
↓
human-readable proof trace
```

Stable homotopy groups and stable Toda brackets remain later layers.
