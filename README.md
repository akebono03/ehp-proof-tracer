# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in
EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to explain how homotopy groups of spheres are determined
from mathematical input such as EHP exact sequences, element orders, additive
relations, Suspension, Freudenthal theory, composition, generalized Hopf
invariants, homomorphisms, subgroup / modulo information, symbolic scalar
constraints, indeterminacy, Toda brackets, typed homotopy elements, structured
generator notation, indexed Toda theorem facts, literature-backed theorem
repositories, and later stable-homotopy information.

The project separates:

```text
mathematical rule / theorem
generic inference mechanism
abelian-group calculation
```

Development principle:

```text
actual mathematical need
↓
minimal representation
↓
domain rule when needed
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

Current architecture:

```text
literature-backed theorem facts / repository
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

The expression layer is primarily structural syntax.

Phase 21 adds minimal source / target context and pure compatibility queries.

Phase 22 adds structured generator identity while preserving the existing
`HomotopyElement` API and keeping generator notation separate from typing rules,
table lookup, and theorem applicability.

Phase 23 connects indexed Toda theorem facts to membership under explicit
matching / validity guards while preserving the narrow literature-backed bridge
for specific actual notation.

Phase 24 adds a minimal repository layer that stores literature-backed theorem
facts and supplies them to the existing proof / inference infrastructure without
introducing a universal theorem prover.

---

# Toda bracket model

`TodaBracket` represents a three-fold unstable bracket:

```text
{a,b,c}
```

and stores an optional index:

```text
index: int | ScalarSymbol | None
```

Therefore:

```text
{a,b,c}
{a,b,c}_1
{a,b,c}_2
{a,b,c}_t
```

remain structurally distinct.

Dedicated statements represent:

```text
{a,b,c} defined
x∈{a,b,c}
```

Important:

```text
definedness
↛
membership
```

```text
membership
↛
exact equality
```

---

# Indexed unstable Toda notation

The canonical indexed structural form is:

```text
{a,E^t b,E^t c}_t
```

with:

```text
TodaBracket.index
IteratedSuspension
IndexedTodaBracketData
```

`IndexedTodaBracketData.is_consistent()` checks:

```text
bracket.second
==
IteratedSuspension(second_base, suspension_exponent)

bracket.third
==
IteratedSuspension(third_base, suspension_exponent)

bracket.index
==
suspension_exponent
```

Important:

```text
constructible
≠
structurally consistent
```

```text
structurally consistent
≠
theorem applicable
```

```text
IteratedSuspension(α,1)
!=structural
Suspension(α)
```

No automatic normalization is performed.

---

# Typed homotopy elements

`HomotopyElement` stores:

```text
name
dimension
source
target
generator
```

with:

```text
source: int | None
target: int | None
generator: GeneratorSymbol | None
```

For typed input:

```text
α : S^m → S^n
```

Suspension exposes:

```text
Eα : S^(m+1) → S^(n+1)
```

For concrete non-negative `r`:

```text
E^r α : S^(m+r) → S^(n+r)
```

For symbolic exponents, no symbolic sphere-dimension algebra is introduced.

`Composition.is_type_compatible()` checks:

```text
left.source == right.target
```

and:

```text
TodaBracket.are_defining_compositions_type_compatible()
```

checks both displayed entry compositions.

Important:

```text
type-compatible
≠
composition is zero
≠
Toda bracket defined
```

Current boolean semantics are intentionally narrow:

```text
True
=
compatibility is confirmed

False
=
compatibility is not confirmed
```

Unknown typing is not treated as a wildcard.

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

`GeneratorSymbol` is not an `Expression`.

Structural distinctions include:

```text
ν != ν′
ν′ != barν
η₃ != η₄
η₃ != μ₃
ι₇ != ι₈
```

`HomotopyElement.generator` is optional, so legacy construction remains valid:

```text
HomotopyElement(name, dimension)
```

Important:

```text
generator notation
↛
automatic source / target typing
```

```text
generator identity
!=
Suspension operation
```

For example:

```text
Eν′
=
Suspension(ν′)
```

rather than a new generator family.

---

# Phase 23: Indexed Toda theorem / validity connection

Phase 23 connects indexed Toda theorem facts to Toda membership while preserving
the distinction between structural representation and theorem applicability.

## Indexed theorem fact

The existing narrow theorem statement is reused:

```text
TodaBracketMembershipTheoremStatement
```

It can losslessly store:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

including bracket index, generator family / index / decoration, source, and note.

No parallel indexed theorem-statement hierarchy is introduced.

## Bracket / generator matching

The theorem bridge uses whole-bracket structural equality.

Therefore:

```text
{a,b,c}_1 == {a,b,c}_1
{a,b,c}_1 != {a,b,c}_2
{a,b,c}_1 != {a,b,c}
```

and differences in:

```text
GeneratorSymbol.family
GeneratorSymbol.index
GeneratorSymbol.decoration
```

also prevent matching.

`index=None` is not a wildcard.

## Definedness dependency

```text
matching theorem fact
+
matching TodaBracketDefinedStatement
↓
TodaBracketMembershipStatement
```

while:

```text
theorem fact alone
↛
membership
```

```text
definedness alone
↛
membership
```

## Canonical indexed guarded bridge

For canonical:

```text
{a,E^t b,E^t c}_t
```

Phase 23 uses:

```text
indexed_toda_bracket_membership_from_theorem_inference_rule(
  indexed_data
)
```

and requires:

```text
indexed_data.is_consistent()
```

plus:

```text
indexed_data.bracket
.are_defining_compositions_type_compatible()
```

together with matching theorem / definedness.

Thus:

```text
matching indexed theorem
+
matching definedness
+
structural consistency
+
confirmed typing compatibility
↓
indexed membership
```

## Actual ε₃ literature form

The actual representative:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

is stored as:

```text
η₃
Eν′ = Suspension(ν′)
ν₇
index = 1
```

It is not forced into `IndexedTodaBracketData`, because:

```text
Suspension(ν′)
!=structural
IteratedSuspension(ν′,1)
```

and no inverse generator lookup such as:

```text
ν₇ → ν₆
```

is introduced.

The actual theorem therefore continues to use the narrow literature-backed
bridge.

## Provenance

Derived membership keeps direct provenance:

```text
membership
├── theorem step
└── definedness step
```

Unrelated facts are excluded.

The theorem `source` and `note` propagate to membership.

Indexed membership does not automatically collapse to an unindexed membership.

---

# Phase 24: Theorem fact / knowledge-table integration

Phase 24 introduces a minimal repository for literature-backed theorem facts.

The purpose is:

```text
literature-backed theorem fact
+
LiteratureReference
↓
repository
↓
structured theorem statement
↓
ProofStep.GIVEN
↓
existing inference rules
↓
proof graph
```

It deliberately does not introduce:

```text
universal theorem prover
general quantified theorem language
JSON / YAML loader
generator typing table
automatic theorem applicability
```

## Repository structures

Phase 24 adds:

```text
TheoremFactEntry
TheoremFactRepository
```

Current narrow entry shape:

```text
TheoremFactEntry
├── statement: TodaBracketMembershipTheoremStatement
└── reference: LiteratureReference
```

Current repository shape:

```text
TheoremFactRepository
└── entries: tuple[TheoremFactEntry, ...]
```

The repository is intentionally narrow and currently stores the actual theorem
family needed by the project:

```text
TodaBracketMembershipTheoremStatement
```

It is not yet a universal repository for every possible statement type.

## Literature provenance

`LiteratureReference` is reused rather than duplicated.

Repository storage preserves:

```text
statement
reference
```

as one fact entry.

The stored theorem statement may remain:

```text
source=None
```

while repository metadata keeps the canonical literature reference separately.

`TheoremFactEntry.materialize_statement()` creates a new statement with:

```text
source = entry.reference
```

without mutating the stored statement.

Therefore:

```text
stored statement
!=
materialized statement object
```

while element, bracket, note, index, and generator structure are preserved.

## Registered representative fact

Phase 24 registers the concrete representative:

```text
EPSILON_3_TODA_MEMBERSHIP_FACT
```

for:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

and stores it in:

```text
THEOREM_FACT_REPOSITORY
```

The representation preserves:

```text
ε₃ generator family/index
η₃ generator family/index
ν′ decoration
ν₇ generator family/index
Suspension(ν′)
Toda index = 1
LiteratureReference
```

No canonical indexed conversion is performed.

## Structural lookup

Current minimal API:

```text
TheoremFactRepository.lookup(statement)
```

returns:

```text
matching structural statement
→ TheoremFactEntry

unknown structural statement
→ None

empty repository
→ None
```

Lookup uses existing structural equality rather than introducing a new fact-key
identity system.

In particular:

```text
{η₃,Eν′,ν₇}_1
!=
{η₃,Eν′,ν₇}_2
```

so the wrong index does not match.

## Duplicate repository boundary

Repository construction rejects duplicate structural theorem statements.

Therefore:

```text
same statement
+
different LiteratureReference
→ duplicate
→ ValueError
```

while:

```text
different statements
+
same LiteratureReference
```

remain allowed.

This prevents lookup and provenance from depending on tuple order.

Current repository invariant:

```text
statement identity is unique
known lookup → one entry
unknown lookup → None
empty lookup → None
```

No string key / ID system is introduced.

## ProofStep.GIVEN connection

`TheoremFactEntry.to_proof_step()` reuses the existing Toda theorem helper.

The chain is:

```text
TheoremFactEntry
↓
materialize_statement()
↓
source-backed TodaBracketMembershipTheoremStatement
↓
existing toda_bracket_membership_theorem_proof_step()
↓
ProofStep.GIVEN
```

The resulting theorem step has:

```text
rule = ProofRule.GIVEN
premises = ()
inference_rule = None
```

This does not itself imply bracket membership.

## Repository representative end-to-end

The Phase 24 actual representative is:

```text
THEOREM_FACT_REPOSITORY
↓ lookup
EPSILON_3_TODA_MEMBERSHIP_FACT
↓ materialize
source-backed theorem statement
↓ ProofStep.GIVEN
+
matching TodaBracketDefinedStatement
↓ existing Toda theorem bridge
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

No repository-specific inference rule is introduced.

The existing Toda bridge remains responsible for theorem applicability.

## Provenance / scope

Repository integration preserves the existing direct provenance:

```text
membership.premises
=
(theorem_step, defined_step)
```

An unrelated repository-derived theorem step does not enter membership
provenance.

The representative inference produces the expected membership only once and
reaches:

```text
FIXED_POINT
```

The generic inference engine remains unchanged.

---

# Phase 24 completion boundary

Implemented:

1. `TheoremFactRepository`.
2. empty repository representation.
3. `TheoremFactEntry`.
4. `LiteratureReference` stored with a theorem fact.
5. repository entry preserves statement and literature metadata.
6. actual `ε₃ ∈ {η₃,Eν′,ν₇}_1` registered as a production fact.
7. actual ε₃ generator structure remains lossless.
8. actual `Eν′` remains ordinary `Suspension`.
9. actual bracket index `1` remains lossless.
10. `THEOREM_FACT_REPOSITORY` contains the representative fact.
11. structural statement lookup.
12. known lookup returns the matching entry.
13. wrong-index / unknown structural lookup returns `None`.
14. empty repository lookup returns `None`.
15. duplicate structural statements are rejected.
16. same statement with another reference is still a duplicate.
17. no fact-key / ID system is introduced.
18. `materialize_statement()` attaches the repository `LiteratureReference`.
19. materialization does not mutate the stored statement.
20. statement element / bracket / note / generator structure are preserved.
21. `to_proof_step()` creates an existing-style `ProofStep.GIVEN`.
22. the existing Toda theorem proof-step helper is reused.
23. repository fact alone still does not imply membership.
24. repository-derived theorem + matching definedness derives membership.
25. actual indexed ε₃ membership is preserved.
26. membership direct provenance is theorem step + definedness step.
27. unrelated repository-derived facts are excluded from provenance.
28. matching membership is not duplicated.
29. representative inference reaches `FIXED_POINT`.
30. no repository-specific inference rule is added.
31. no universal theorem representation is added.
32. no JSON / YAML loader is added.
33. no automatic generator typing is added.
34. generic inference engine remains unchanged.
35. full regression passes.

---

# Current limitations

Not yet implemented as general systems:

- generator table lookup,
- automatic source / target derivation from generator identity,
- name / generator consistency validation,
- generator / dimension / typing validation,
- ambient homotopy-group / stem / stable-context typing,
- repository support for theorem families beyond the current narrow Toda
  membership fact family,
- fact key / stable fact ID system,
- multiple literature references for one theorem statement,
- external JSON / YAML knowledge-table loading,
- general theorem quantification,
- general theorem-side condition language,
- canonicalization between `Suspension(α)` and `IteratedSuspension(α,1)`,
- automatic recovery of generator bases from suspended indexed generators,
- general indexed Toda definedness theorem system,
- stable homotopy-group model,
- stable Toda bracket `<a,b,c>`,
- higher / variable-arity Toda brackets,
- general candidate-set algebra.

---

# Tests

Focused Phase 24 repository test:

```powershell
python -m pytest tests/test_theorem_facts.py -q
```

Verified Phase 24 completion:

```text
15 passed
```

Focused Toda regression:

```powershell
python -m pytest tests/test_toda_rules.py -q
```

Verified during Phase 24:

```text
66 passed
```

Full suite:

```powershell
python -m pytest -q
```

Verified Phase 24 completion:

```text
1190 passed in 61.30s
```

No failures.

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capabilities and dependency order

Historical statements in the development log describe the state at that time.
Current behavior is defined by the latest README and design documents.

---

# Next development boundary

The completed dependency chain now includes:

```text
Additive expressions
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
Toda bracket minimum representation
↓
Toda membership theorem bridge
↓
Indexed unstable Toda notation
↓
Typed homotopy elements / source-target context
↓
Structured generator representation
↓
Indexed Toda theorem / validity connection
↓
Theorem fact / knowledge-table integration
```

Natural next candidate:

```text
Phase 25
Generator typing / ambient-group facts
```

The next layer should use the new explicit fact / repository approach to provide
generator typing or ambient-group knowledge as explicit facts rather than
silently deriving source / target information from `GeneratorSymbol.index`.

Potential later dependencies:

```text
generator typing / ambient-group facts
↓
theorem representation generalization
  only when actual quantified theorems require it
↓
stable homotopy representation
↓
stable Toda brackets
```

Phase numbering remains driven by actual mathematical need.
