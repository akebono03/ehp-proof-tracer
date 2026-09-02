# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to explain how homotopy groups of spheres are determined from mathematical input such as EHP exact sequences, element orders, additive relations, Suspension, Freudenthal theory, composition, generalized Hopf invariants, homomorphisms, subgroup / modulo information, symbolic scalar constraints, indeterminacy, Toda brackets, typed homotopy elements, structured generator notation, literature-backed theorem repositories, explicit generator / composition / map facts, map properties, and later stable-homotopy information.

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
- Phase 29: actual H map facts / typing / production-fact connection
- Phase 30: Toda Prop.2.2 right suspended-composition formula / actual-H proof closure

Current architecture:

```text
literature-backed theorem facts / repository
explicit generator facts / repository
explicit composition facts / repository
explicit map facts / repository
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

Phase 21 adds minimal source / target context and compatibility queries. Phase 22 adds structured generator identity while keeping generator notation separate from typing rules. Phase 23 connects indexed Toda theorem facts to membership under explicit guards. Phase 24 adds a narrow literature-backed theorem repository. Phase 25 adds a separate explicit generator-fact repository and typed-element materialization. Phase 26 expands this knowledge to the actual generators appearing in the ε₃ Toda bracket. Phase 27 adds explicit corrected composition knowledge and connects it to actual indexed Toda definedness and theorem-backed membership. Phase 28 adds proof-level injectivity / isomorphism statements and equality reflection through an injective map. Phase 29 connects an actual Hopf map identity, typing context, and isomorphism fact to the Phase 28 proof-level machinery. Phase 30 connects the existing generalized Hopf-invariant composition machinery to the actual EHP `H` map representation and generic equality rules, yielding the Toda Prop.2.2 right suspended-composition formula as a proof-level equality with full provenance.

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

has type-compatible displayed adjacent compositions.

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

the corrected actual indexed condition is:

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

The rule captures:

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

Phase 28 introduced the minimal general mechanism:

```text
f(a)=f(b)
+
f is injective / an isomorphism
↓
a=b
```

Added:

```text
InjectiveMapStatement
IsomorphismStatement
isomorphism_implies_injective_inference_rule()
injective_map_reflects_equality_inference_rule()
```

Existing `MapApplication` represents:

```text
f(a)
```

and `RelationType.EQUALITY` represents:

```text
f(a)=f(b)
```

The fixed-point chain is:

```text
GIVEN
Isomorphism(f)

GIVEN
f(a)=f(b)

Round 1
Injective(f)

Round 2
a=b
```

Invalid mismatched-map cases are rejected and full proof-level provenance is retained.

Important Phase 28 boundary:

```text
H
=
representative MapSymbol only
```

No actual Hopf-map fact was yet supplied.

---

# Phase 29: actual H map facts / typing

Phase 29 replaces the representative Phase 28 `H is an isomorphism` assumption with explicit production mathematical knowledge for the required Hopf-map context.

## 29-1: actual H map identity

Production map identity:

```text
HOPF_MAP = MapSymbol(name="H")
```

Critical boundary:

```text
HOPF_MAP
!=
map typing
!=
map property
```

`MapSymbol` remains a structural map identity only.

## 29-2: map typing representation

Added:

```text
MapTypingFact
```

with fields:

```text
map
source_group_dimension
source_sphere_dimension
target_group_dimension
target_sphere_dimension
```

This represents maps between unstable homotopy groups without embedding typing in `MapSymbol`.

Representative structure:

```text
H : π₃(S²) → π₃(S³)
```

Critical:

```text
MapSymbol
!=
MapTypingFact
```

## 29-3: actual H typing fact

Production knowledge:

```text
HOPF_MAP_TYPING_FACT
```

represents:

```text
H : π₃(S²) → π₃(S³)
```

The map identity remains:

```text
HOPF_MAP == MapSymbol(name="H")
```

and does not acquire typing fields.

## 29-4: isomorphism fact representation

Added:

```text
MapIsomorphismFact
```

with:

```text
typing: MapTypingFact
```

Thus the property is explicitly tied to one typing context.

Critical:

```text
MapIsomorphismFact
!=
IsomorphismStatement
```

The former is knowledge-layer data; the latter is a proof-level statement.

## 29-5: production isomorphism fact / repository

Production fact:

```text
HOPF_MAP_ISOMORPHISM_FACT
```

Production repository:

```text
MAP_ISOMORPHISM_FACT_REPOSITORY
```

Repository API:

```text
lookup(typing)
```

The registered fact is:

```text
H : π₃(S²) → π₃(S³)
is an isomorphism
```

Lookup is exact on `MapTypingFact` structural equality.

Therefore:

```text
same MapSymbol("H")
+
different typing context
↛
registered isomorphism fact
```

Duplicate isomorphism facts in the same typing context are rejected.

## 29-6: fact materialization to proof level

`MapIsomorphismFact.to_proof_step()` materializes:

```text
HOPF_MAP_ISOMORPHISM_FACT
↓
ProofStep.GIVEN
↓
IsomorphismStatement(HOPF_MAP)
```

This is knowledge materialization, not mathematical inference.

Therefore:

```text
rule = ProofRule.GIVEN
premises = ()
inference_rule = None
```

The current proof-level `IsomorphismStatement` retains map identity only; typing context remains in the knowledge-layer fact used to create it.

## 29-7: actual H fact to injectivity

The existing Phase 28 rule is reused unchanged:

```text
MAP_ISOMORPHISM_FACT_REPOSITORY
↓ lookup
HOPF_MAP_ISOMORPHISM_FACT
↓ to_proof_step()
GIVEN Isomorphism(H)
↓
isomorphism_implies_injective_inference_rule()
↓
Injective(H)
```

No new inference rule and no generic-engine change are required.

## 29-8: representative actual-H end-to-end example

Representative probe:

```powershell
python -m probes.probe_phase29_capabilities
```

Visible proof trace:

```text
PRODUCTION FACT
H : π₃(S²) → π₃(S³) is an isomorphism

↓ materialize

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

The inference engine reports:

```text
rounds = 2
termination = InferenceTerminationReason.FIXED_POINT
```

The key improvement over Phase 28 is that `Isomorphism(H)` is now supplied from actual production knowledge rather than directly assumed in the probe.

Important boundary:

```text
H(a)=H(b)
```

is still a representative GIVEN equality in Phase 29.

Phase 29 does not yet calculate:

```text
H((2ι₂)η₂)=H(4η₂)
```

## 29-9: provenance / invalid / scope regression

The actual-H chain now verifies:

```text
full proof-level provenance
```

```text
Injective(H) + g(a)=g(b)
↛ a=b
```

```text
unknown H typing context
↛ isomorphism fact lookup
```

```text
unrelated fact
↛ Injective(H) provenance
↛ a=b provenance
```

Derived conclusions remain unique:

```text
Injective(H)
→ exactly one derived step
```

```text
a=b
→ exactly one derived step
```

A terminal re-run gives:

```text
new_steps == ()
```

so the two-round result is a genuine fixed point.

---

# Phase 29 completion boundary

Implemented:

1. production `HOPF_MAP` identity.
2. `MapTypingFact` for maps between unstable homotopy groups.
3. production `HOPF_MAP_TYPING_FACT`.
4. structural `MapIsomorphismFact` tied to a typing context.
5. production `HOPF_MAP_ISOMORPHISM_FACT`.
6. `MapIsomorphismFactRepository`.
7. exact typing-context lookup.
8. duplicate fact rejection.
9. `MapIsomorphismFact.to_proof_step()`.
10. actual fact → `ProofStep.GIVEN` → `IsomorphismStatement(H)`.
11. existing Phase 28 isomorphism → injectivity connection.
12. actual-H fact-driven equality-reflection example.
13. full proof-level provenance regression.
14. different-map rejection.
15. unknown-typing-context rejection.
16. unrelated-fact exclusion.
17. derived-conclusion deduplication.
18. genuine fixed-point regression.
19. human-readable Phase 29 capability probe.
20. generic inference engine unchanged.
21. full regression passes.

Current verified status:

```text
full suite
1408 passed in 96.81s
```

No failures.


---

# Phase 30: Toda Prop.2.2 right suspended-composition formula

Phase 30 establishes the right-hand formula from [Toda] Prop.2.2:

```text
H(a ∘ Eb)=H(a) ∘ Eb
```

without introducing smash products or the left-hand Prop.2.2 formula.

## Existing machinery reused

Phase 30 deliberately reuses the Phase 11 generalized Hopf-invariant layer:

```text
HopfInvariantStatement
HopfCompositionLawStatement
hopf_composition_law_inference_rule()
hopf_composition_formula_inference_rule()
```

and connects it to the production H identity through:

```text
hopf_invariant_statement_to_ehp_h_equality_inference_rule()
```

The bridge materializes:

```text
HopfInvariantStatement(
  expression=x,
  value=y,
)
```

as the proof-level equality:

```text
H(x)=y
```

using the actual production map:

```text
EHP_H_MAP
```

No implicit equality exists between `HopfInvariantStatement` and `Relation(MapApplication(...))`; the connection is an explicit inference rule.

## Right-formula proof chain

Starting from:

```text
GIVEN
H(a)=β
```

Phase 11 machinery gives:

```text
H(a)=β
↓
generalized Hopf composition law
↓
H(a ∘ Eb)=β ∘ Eb
```

The actual-H bridge gives this as:

```text
H(a ∘ Eb)=β ∘ Eb
```

A second branch starts again from:

```text
H(a)=β
```

and uses generic equality rules:

```text
H(a)=β
↓ equality symmetry
β=H(a)
↓ equality preserved under right composition by Eb
β ∘ Eb=H(a) ∘ Eb
```

Finally:

```text
H(a ∘ Eb)=β ∘ Eb
β ∘ Eb=H(a) ∘ Eb
↓ equality transitivity
H(a ∘ Eb)=H(a) ∘ Eb
```

Thus the Toda Prop.2.2 right formula is available as an actual proof-level `RelationType.EQUALITY` over the production H map.

## Provenance

The final equality retains both proof branches.

Left branch:

```text
final transitivity premise
↓
actual-H bridge
↓
Hopf composition formula
↓
Hopf composition law
↓
GIVEN H(a)=β
```

Right branch:

```text
final transitivity premise
↓
staged right composition
↓
equality symmetry
↓
actual-H bridge
↓
GIVEN H(a)=β
```

Unrelated equalities and unrelated valid Hopf facts are excluded from the final closure.

## Scope / termination boundary

The generic rule:

```text
equality_preserved_under_right_composition_inference_rule(Eb)
```

is structurally productive and can be applied repeatedly:

```text
x=y
↓
x∘Eb=y∘Eb
↓
(x∘Eb)∘Eb=(y∘Eb)∘Eb
↓
...
```

Therefore Phase 30 does not place this rule into an unrestricted global fixed-point rule set. It is used as one explicit staged application in the Prop.2.2 proof.

The terminal transitivity step itself is stable:

```text
terminal derive_inference_round_result()
→ new_steps == ()
```

Invalid / scope regressions verify:

```text
unsuspended right factor
↛ right suspended-composition formula
```

```text
mismatched middle expression
↛ transitivity closure
```

```text
different suspended right factor
↛ Prop.2.2 closure
```

```text
unrelated equality
↛ final provenance
```

```text
unrelated valid Hopf fact H(c)=γ
↛ closure of the a / β branch
```

The final formula is deduplicated within the tested inference round.

## Representative capability probe

Run:

```powershell
python -m probes.probe_phase30_capabilities
```

The probe visibly demonstrates:

```text
GIVEN H(a)=β
↓
Hopf composition law
↓
H(a∘Eb)=β∘Eb
```

and:

```text
GIVEN H(a)=β
↓
β=H(a)
↓
β∘Eb=H(a)∘Eb
```

followed by:

```text
equality transitivity
↓
H(a∘Eb)=H(a)∘Eb
```

The probe also displays the full provenance chain and explicitly states that right composition is a staged step.

---

# Phase 30 completion boundary

Implemented:

1. structural representation of `H(a∘Eb)=H(a)∘Eb` using existing `MapApplication`, `Composition`, and `Suspension`.
2. explicit distinction between Phase 11 `HopfInvariantStatement` and actual-H map-application equality.
3. explicit Phase 11 Hopf statement → production EHP `H` equality bridge.
4. reuse of the existing generalized Hopf composition law.
5. reuse of the existing generalized Hopf composition formula.
6. actual-H equality for `H(a∘Eb)=β∘Eb`.
7. actual-H equality for `H(a)=β`.
8. equality symmetry to obtain `β=H(a)`.
9. staged right-composition equality to obtain `β∘Eb=H(a)∘Eb`.
10. equality transitivity closure to obtain `H(a∘Eb)=H(a)∘Eb`.
11. full proof-level provenance across both branches.
12. mismatched-middle rejection.
13. different-right-factor rejection.
14. unrelated-equality provenance exclusion.
15. final-formula deduplication in the tested round.
16. explicit staged-rule scope for structurally productive right composition.
17. genuine terminal transitivity regression with `new_steps == ()`.
18. unrelated valid Hopf-branch rejection.
19. human-readable Phase 30 capability probe.
20. production map identity `EHP_H_MAP` / `HOPF_MAP` reused unchanged.
21. generic inference engine unchanged.
22. full regression passes.

Current verified status:

```text
tests/test_phase30_prop22.py
21 passed in 0.19s
```

```text
tests/test_relation_rules.py
47 passed in 0.20s
```

```text
tests/test_hopf_rules.py
31 passed in 0.12s
```

```text
tests/test_map_facts.py
54 passed in 0.17s
```

```text
full suite
1439 passed in 23.44s
```

No failures.

# Current limitations

Not yet implemented as general systems:

- typed `MapSymbol` domain / codomain; typing remains external knowledge,
- typing-aware proof-level `IsomorphismStatement`,
- literature provenance for map-property facts,
- `SurjectiveMapStatement`,
- preimage reasoning,
- general kernel-modulo equality shortcut,
- literature provenance on generator typing / ambient-group facts,
- literature provenance on composition facts,
- `ProofStep` representation for generator facts,
- external generator-table loading,
- external composition-fact-table loading,
- external map-fact-table loading,
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
- Toda Prop.2.2 left formula `H((Ec)∘a)=E(c∧c)∘H(a)`,
- actual mapped equality `H((2ι₂)η₂)=H(4η₂)`,
- stable homotopy-group model,
- stable Toda bracket `<a,b,c>`,
- higher / variable-arity Toda brackets.

---

# Tests

Phase 30 focused suite:

```powershell
python -m pytest tests/test_phase30_prop22.py -q
```

Verified:

```text
21 passed in 0.19s
```

Related focused suites:

```powershell
python -m pytest tests/test_relation_rules.py -q
python -m pytest tests/test_hopf_rules.py -q
python -m pytest tests/test_map_facts.py -q
```

Verified:

```text
47 passed in 0.20s
31 passed in 0.12s
54 passed in 0.17s
```

Full suite:

```powershell
python -m pytest -q
```

Verified at Phase 30 completion:

```text
1439 passed in 23.44s
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

Phase 29:

```powershell
python -m probes.probe_phase29_capabilities
```

Phase 30:

```powershell
python -m probes.probe_phase30_capabilities
```

The Phase 30 probe visibly demonstrates:

```text
GIVEN H(a)=β
↓
Hopf composition law
↓
H(a∘Eb)=β∘Eb
```

and:

```text
H(a)=β
↓ equality symmetry
β=H(a)
↓ staged right composition
β∘Eb=H(a)∘Eb
```

then:

```text
equality transitivity
↓
H(a∘Eb)=H(a)∘Eb
```

The probe also displays full proof provenance and the staged-rule scope boundary.

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capabilities and dependency order

Historical statements in the development log describe the state at that time. Current behavior is defined by the latest README and design documents.

---

# Next development boundary

Phase 30 completes the right-hand Toda Prop.2.2 chain:

```text
H(a)=β
↓
H(a∘Eb)=β∘Eb

H(a)=β
↓
β=H(a)
↓
β∘Eb=H(a)∘Eb

↓ equality transitivity

H(a∘Eb)=H(a)∘Eb
```

The next natural phase is:

```text
Phase 31
SmashProduct minimum representation
```

The immediate structural target is:

```text
a ∧ b
```

represented without prematurely implementing general smash-product algebra.

This is required before the second Toda Prop.2.2 formula can be represented faithfully:

```text
H((Ec) ∘ a)=E(c ∧ c) ∘ H(a)
```

Phase 31 should preserve:

```text
SmashProduct(a,b)
!=
Barratt-Hilton theorem knowledge
```

and should not yet implement the full Barratt-Hilton formula, symbolic sign algebra, or the actual calculation of `H((2ι₂)η₂)`.

The longer dependency is:

```text
Phase 30
Toda Prop.2.2 right formula complete
↓
Phase 31
SmashProduct minimum representation
↓
left Prop.2.2 formula support
↓
IteratedSuspension / symbolic sign support as required
↓
Toda Prop.3.1 Barratt-Hilton
↓
actual H((2ι₂)η₂) calculation
↓
H((2ι₂)η₂)=H(4η₂)
↓
existing Phase 28/29 equality reflection
↓
(2ι₂)η₂=4η₂
```
