# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to explain how homotopy groups of spheres are determined from mathematical input such as EHP exact sequences, element orders, additive relations, Suspension, Freudenthal theory, composition, generalized Hopf invariants, homomorphisms, subgroup / modulo information, symbolic scalar constraints, indeterminacy, Toda brackets, typed homotopy elements, structured generator notation, literature-backed theorem repositories, explicit generator and composition facts, map properties, and later stable-homotopy information.

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
- Phase 28: map-property equality-reflection foundation

Current architecture:

```text
literature-backed theorem facts / repository
explicit generator facts / repository
explicit composition facts / repository
explicit map-property statements / future map facts
        ↓
homotopy / EHP / map-property domain rules
        ↓
generic proof / inference engine
        ↓
proof-level expression / scalar / set / subgroup / modulo /
indeterminacy / Toda / map-property statements
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

Phase 21 adds minimal source / target context and compatibility queries. Phase 22 adds structured generator identity while keeping generator notation separate from typing rules. Phase 23 connects indexed Toda theorem facts to membership under explicit guards. Phase 24 adds a narrow literature-backed theorem repository. Phase 25 adds a separate explicit generator-fact repository and typed-element materialization. Phase 26 expands this knowledge to the actual generators appearing in the ε₃ Toda bracket. Phase 27 adds explicit corrected composition knowledge and connects it to actual indexed Toda definedness and theorem-backed membership. Phase 28 adds proof-level injectivity / isomorphism statements and equality reflection through an injective map.

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

Critical boundary retained in later phases:

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

## Corrected indexed condition

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

with:

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

and terminates at a genuine fixed point.

---

# Phase 28: map-property equality-reflection foundation

Phase 28 introduces the minimal general mechanism needed for proofs of the form:

```text
f(a) = f(b)
+
f is injective / an isomorphism
↓
a = b
```

The phase intentionally stops before adding actual Hopf-map facts.

## 28-1: InjectiveMapStatement

Added:

```text
InjectiveMapStatement(
  map=f,
)
```

This represents:

```text
f is injective
```

Critical boundary:

```text
MapSymbol(f)
↛
InjectiveMapStatement(f)
```

Injectivity is explicit proof-level knowledge and is not inferred from notation.

## 28-2: IsomorphismStatement

Added:

```text
IsomorphismStatement(
  map=f,
)
```

Critical structural distinction:

```text
IsomorphismStatement(f)
!=
InjectiveMapStatement(f)
```

Mathematical implication is represented by an explicit inference rule rather than by structural equality.

## 28-3: isomorphism implies injectivity

Added:

```text
isomorphism_implies_injective_inference_rule()
```

Rule:

```text
Isomorphism(f)
↓
Injective(f)
```

The derived `ProofStep` preserves the isomorphism premise as provenance.

No reverse implication is added.

## 28-4: MapApplication equality representation

Existing structures are sufficient to represent:

```text
f(a)=f(b)
```

as:

```text
Relation(
  lhs=MapApplication(
    map=f,
    expression=a,
  ),
  rhs=MapApplication(
    map=f,
    expression=b,
  ),
  relation_type=RelationType.EQUALITY,
)
```

No new map-equality statement class is needed.

Structural distinctions remain visible:

```text
f(a)=f(b)
!=
f(a)=g(b)
```

## 28-5: equality reflection under injectivity

Added:

```text
injective_map_reflects_equality_inference_rule()
```

Rule:

```text
Injective(f)
+
f(a)=f(b)
↓
a=b
```

The guard requires:

```text
lhs is MapApplication
rhs is MapApplication
lhs.map == rhs.map
injective_statement.map == lhs.map
```

The conclusion reuses the original mapped expressions:

```text
lhs = mapped_equality.lhs.expression
rhs = mapped_equality.rhs.expression
relation_type = EQUALITY
```

## 28-6: provenance chain

The existing rules compose in one fixed-point run:

```text
GIVEN
Isomorphism(f)

GIVEN
f(a)=f(b)

Round 1
Isomorphism(f)
→ Injective(f)

Round 2
Injective(f) + f(a)=f(b)
→ a=b
```

The final equality step preserves direct premises:

```text
derived Injective(f)
mapped equality f(a)=f(b)
```

and the derived injectivity step preserves:

```text
Isomorphism(f)
```

Thus the complete proof chain is traceable.

## 28-7: invalid / mismatched map regression

The following are rejected:

```text
Injective(f) + g(a)=g(b)
↛ a=b
```

```text
Injective(f) + f(a)=g(b)
↛ a=b
```

```text
Isomorphism(f) + g(a)=g(b)
↛ a=b
```

```text
Injective(f) + plain a=b
↛ equality-reflection rule
```

Equality reflection requires the same map on both applications and the injectivity statement for that same map.

## 28-8: representative end-to-end probe

Representative executable probe:

```powershell
python -m probes.probe_phase28_capabilities
```

Visible chain:

```text
GIVEN
H is an isomorphism

INFERENCE
isomorphism implies injectivity
↓
H is injective

GIVEN
H(a)=H(b)

INFERENCE
injective map reflects equality
↓
a=b
```

The probe reports:

```text
rounds = 2
termination = InferenceTerminationReason.FIXED_POINT
```

Important boundary:

```text
H
=
representative MapSymbol only
```

Phase 28 does not yet claim any actual Hopf-map typing or theorem fact.

## 28-9: scope / fixed-point regression

Phase 28 fixes:

```text
unrelated fact
↛ injectivity provenance
```

```text
unrelated fact
↛ equality provenance
```

Derived conclusions are unique:

```text
Injective(f)
→ exactly one derived step
```

```text
a=b
→ exactly one derived step
```

A terminal re-run using:

```text
derive_inference_round_result()
```

produces:

```text
new_steps == ()
```

Therefore the two-round result is a genuine fixed point rather than a round-limit artifact.

Generic inference engine remains unchanged.

---

# Phase 28 completion boundary

Implemented:

1. `InjectiveMapStatement`.
2. `IsomorphismStatement`.
3. structural distinction between injectivity and isomorphism.
4. `isomorphism_implies_injective_inference_rule()`.
5. existing `MapApplication` representation of `f(a)=f(b)`.
6. no new map-equality statement class.
7. `injective_map_reflects_equality_inference_rule()`.
8. same-map guard for equality reflection.
9. `Isomorphism(f) → Injective(f) → a=b` fixed-point composition.
10. full two-level `ProofStep` provenance.
11. mismatched-map rejection.
12. plain-equality rejection.
13. unrelated-fact provenance exclusion.
14. derived-conclusion deduplication.
15. genuine terminal fixed-point regression.
16. human-readable Phase 28 capability probe.
17. generic inference engine unchanged.
18. full regression passes.

Current verified status:

```text
tests/test_map_property_rules.py
26 passed in 1.42s
```

```text
full suite
1358 passed in 102.90s
```

No failures.

---

# Current limitations

Not yet implemented as general systems:

- typed `MapSymbol` domain / codomain,
- actual Hopf map `H` typing facts,
- actual `H` isomorphism facts,
- literature provenance for map-property facts,
- map-property fact repository,
- `SurjectiveMapStatement`,
- preimage reasoning,
- general kernel-modulo equality shortcut,
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
- symbolic scalar expression trees such as `(-1)^n`,
- smash-product expressions,
- actual Hopf-invariant formulas needed for `(2ι₂)η₂=4η₂`,
- stable homotopy-group model,
- stable Toda bracket `<a,b,c>`,
- higher / variable-arity Toda brackets.

---

# Tests

Focused Phase 28 suite:

```powershell
python -m pytest tests/test_map_property_rules.py -q
```

Verified:

```text
26 passed in 1.42s
```

Full suite:

```powershell
python -m pytest -q
```

Verified at Phase 28 completion:

```text
1358 passed in 102.90s
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

Phase 28:

```powershell
python -m probes.probe_phase28_capabilities
```

The Phase 28 probe visibly demonstrates:

```text
H is an isomorphism
↓
H is injective

H(a)=H(b)
↓
a=b
```

It explicitly states that `H` is only a representative `MapSymbol` in Phase 28.

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capabilities and dependency order

Historical statements in the development log describe the state at that time. Current behavior is defined by the latest README and design documents.

---

# Next development boundary

Phase 28 completes the generic map-property equality-reflection foundation.

The natural next phase is:

```text
Phase 29
actual H map facts / typing
```

The target is to replace the representative `MapSymbol("H")` assumption with explicit mathematical knowledge appropriate for the concrete Hopf-map situation.

Likely Phase 29 responsibilities include only the facts needed by the next representative proof, for example:

```text
actual H identity
actual H domain / codomain context
actual H isomorphism property in the required case
explicit fact / provenance supply
connection to the existing Phase 28 map-property rules
```

Phase 29 should not yet implement the full calculation

```text
H((2ι₂)η₂)=4ι₃
```

or smash-product / Hopf-formula machinery unless the concrete next subphase requires it.

The longer dependency remains:

```text
Phase 28
generic injectivity / isomorphism / equality reflection

↓
Phase 29
actual H map facts / typing

↓
Phase 30+
Hopf formulas / smash product / actual calculation

↓
(2ι₂)η₂ = 4η₂
```
