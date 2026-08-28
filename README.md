# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in
EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to explain how homotopy groups of spheres are determined
from mathematical input such as EHP exact sequences, element orders,
Suspension, Freudenthal theorems, composition relations, generalized Hopf
invariants, Toda relations, Toda brackets, Steenrod operations, and
literature-backed facts.

The project separates:

```text
mathematical rule / theorem
generic inference mechanism
abelian-group calculation
```

---

# Current status

Completed foundations and theorem families:

1. finitely generated abelian-group calculation,
2. EHP exact-sequence calculation,
3. proof / relation representation,
4. generic fixed-point inference,
5. EHP-domain inference,
6. ORDER reasoning,
7. Suspension reasoning,
8. Freudenthal stable-range reasoning,
9. composition reasoning,
10. Suspension-composition functoriality,
11. generalized Hopf-invariant reasoning,
12. provenance and explicit inference-scope / termination boundaries.

Current architecture:

```text
homotopy / EHP domain rules
        ↓
generic proof / inference engine
        ↓
homotopy / EHP data layer
        ↓
finitely generated abelian-group algebra
        ↓
integer linear algebra
```

Phase 5-65 is the completion point of the generic inference-engine foundation.
Later Phases add mathematical rule families without adding domain-specific
branches to the engine unless an actual theorem demonstrates a missing generic
capability.

---

# Development status

- Phase 1: finite abelian-group calculations — completed
- Phase 2: structured subgroup calculations — completed
- Phase 3: quotient groups, exact sequences, extensions, EHP inference — completed
- Phase 4: presentation-based calculations with free components — completed
- Phase 5: generic proof / inference engine foundation — completed
- Phase 6: EHP domain-inference foundation — completed
- Phase 7: element-order reasoning — completed
- Phase 8: Suspension reasoning foundation — completed
- Phase 9: Freudenthal / stable-range reasoning — completed
- Phase 10: composition reasoning / Suspension-composition functoriality — completed
- Phase 11: generalized Hopf-invariant reasoning — completed

---

# Algebra layer

The algebra layer handles finitely generated abelian groups of the form:

```text
Z^r ⊕ finite torsion
```

The presentation-based path uses relation matrices, integer lattices,
Hermite normal form, and Smith normal form to calculate kernel, image, and
cokernel. Finite-group enumeration remains as an independent reference path.

For:

```text
A --f--> B --g--> C
```

exactness is represented by:

```text
Im(f)=Ker(g)
```

and is kept distinct from:

```text
B / Im(f) ≅ Im(g)
```

---

# Proof / relation model

`Relation` stores:

```text
lhs
rhs
relation_type
source
note
```

Current relation types:

```text
EQUALITY
ZERO
ORDER
```

A `ProofStep` preserves:

```text
conclusion
premises
rule
note
inference_rule
```

This is the basis for end-to-end provenance.

`LiteratureReference` stores structured literature metadata.

---

# Expression model

Current structured expressions include:

```text
Zero
HomotopyElement
Multiple
Composition
Suspension
```

Generator helpers include:

```text
eta(n)
nu(n)
sigma(n)
```

The expression layer represents syntax and structure. It does not itself
perform theorem application, normalization, stable-range checks, dimension
validation, or equality / zero proof.

---

# Generic inference engine

The generic pipeline is:

```text
known ProofSteps
+
InferenceRules
↓
premise search
↓
structured matching
↓
bindings / shared-binding consistency
↓
match guard
↓
conclusion construction
↓
duplicate classification
↓
new ProofSteps
↓
next round
```

Termination reasons:

```text
FIXED_POINT
MAX_ROUNDS
```

`max_rounds` is a safety bound, not semantic cycle detection.

One round does not recursively consume conclusions created earlier in that
same round as new premises for later rules.

---

# Generic relation rules

Equality symmetry:

```text
x=y
→ y=x
```

Equality transitivity:

```text
x=y
y=z
→ x=z
```

Generic ZERO propagation:

```text
x=0
y=x
→ y=0
```

EHP-, ORDER-, Suspension-, Freudenthal-, Toda-, and Hopf-derived facts reconnect
through the same generic relation machinery where their semantics permit it.

---

# Phase 6: EHP reasoning

Representative chain:

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
generic ZERO
↓
equality closure / ZERO propagation
↓
FIXED_POINT
```

---

# Phase 7: ORDER reasoning

```text
ord(α)=n
↓
nα=0
↓
generic equality / ZERO reasoning
```

---

# Phase 8: Suspension reasoning

```text
x=y  → E(x)=E(y)
x=0  → E(x)=0
nα=0 → nE(α)=0
```

Repeated Suspension may generate:

```text
E(x), E²(x), E³(x), ...
```

so unrestricted fixed-point termination is not assumed.

---

# Phase 9: Freudenthal reasoning

Stable range:

```text
stem <= sphere_dimension - 2
→ suspension isomorphism
→ injectivity
→ equality / ZERO reflection
```

Boundary:

```text
stem == sphere_dimension - 1
→ epimorphism only
```

Outside current range:

```text
stem >= sphere_dimension
→ no Freudenthal-derived conclusion
```

---

# Phase 10: Composition reasoning

Known composition facts are ordinary structured equality relations:

```text
α∘β = γ
```

Known zero composition can be bridged to generic ZERO.

Suspension preservation gives:

```text
α∘β=γ
→ E(α∘β)=Eγ
```

Suspension-composition functoriality gives:

```text
α∘β=γ
→ E(α∘β)=Eα∘Eβ
```

Generic equality reasoning can then derive:

```text
Eα∘Eβ=Eγ
```

Because functoriality combined with symmetry can increase structural depth,
Phase 10 uses bounded / staged execution where needed.

---

# Phase 11: Generalized Hopf-invariant reasoning

## Representation

Generalized Hopf-invariant facts are represented by:

```text
HopfInvariantStatement(
  expression,
  value,
  source,
  note,
)
```

Semantics:

```text
H(expression)=value
```

`value` is an `Expression`, not an integer-only field.

Therefore the model can represent values such as:

```text
0
β
nβ
β∘Eγ
```

## Known fact / provenance

A known Hopf fact may carry a `LiteratureReference`.

Provenance is preserved through:

```text
derived ProofStep
↓
premises
↓
known Hopf fact
↓
LiteratureReference
```

rather than by blindly copying source metadata to every derived conclusion.

## Hopf composition-law applicability

```text
H(α)=β
↓
HopfCompositionLawStatement(α,β)
```

The intermediate statement records theorem applicability.

## Generalized Hopf composition formula

```text
HopfCompositionLawStatement(α,β)
+
γ
↓
H(α∘Eγ)=β∘Eγ
```

Existing `Composition` and `Suspension` expressions are reused.

## Hopf value ZERO bridge

```text
H(x)=y
+
y=0
↓
H(x)=0
```

The ZERO fact must concern exactly the same value `y`.

An unrelated ZERO fact is rejected.

Most importantly:

```text
H(x)=0
↛
x=0
```

Phase 11 does not confuse vanishing Hopf invariant with vanishing element.

## Suspension / composition integration

For `β=Eδ`:

```text
H(α∘Eγ)=Eδ∘Eγ
```

If:

```text
δ∘γ=0
```

existing Suspension, functoriality, equality, and ZERO rules can derive:

```text
Eδ∘Eγ=0
```

and therefore:

```text
H(α∘Eγ)=0
```

No separate Hopf-specific equality engine is added.

## EHP bridge

For the EHP map pair specifically `E` followed by `H`:

```text
EHPZeroCompositionStatement(E,H)
+
α
↓
H(Eα)=0
```

Thus:

```text
Exactness(E,H)
↓
EHPZeroCompositionStatement(E,H)
↓
H(Eα)=0
```

The bridge rejects other consecutive EHP pairs such as `H` followed by `P`.

## Representative scenario

The representative Phase 11 scenario keeps both branches in one knowledge
state:

```text
Hopf branch:
H(α)=Eδ
→ H(α∘Eγ)=Eδ∘Eγ
→ Eδ∘Eγ=0
→ H(α∘Eγ)=0
```

```text
EHP branch:
Exactness(E,H)
→ EHPZeroCompositionStatement(E,H)
→ H(Eγ)=0
```

The final finite stage reaches a genuine `FIXED_POINT`.

## Provenance regression

The final Hopf conclusion can be traced back through:

```text
H(α∘Eγ)=0
↓
H(α∘Eγ)=Eδ∘Eγ
↓
HopfCompositionLawStatement(α,Eδ)
↓
H(α)=Eδ
↓
LiteratureReference
```

The EHP branch can be traced through:

```text
H(Eγ)=0
↓
EHPZeroCompositionStatement(E,H)
↓
Exactness(E,H)
```

## Theorem scope

Implemented:

```text
H(α)=β
→ HopfCompositionLawStatement(α,β)
```

```text
HopfCompositionLawStatement(α,β)
+
γ
→ H(α∘Eγ)=β∘Eγ
```

```text
H(x)=y
+
y=0
→ H(x)=0
```

```text
EHPZeroCompositionStatement(E,H)
+
α
→ H(Eα)=0
```

Not inferred:

```text
H(x)=0 → x=0
H(x)=0 → x ∈ Im(E)
H(x)=0 → x=E(y) for some y
P∘H=0 → H(Eα)=0
```

## Phase 11 termination boundary

The Hopf law / formula pair is recursively applicable:

```text
H(α)=β
↓
Law(α,β)
↓
H(α∘Eγ)=β∘Eγ
↓
Law(α∘Eγ,β∘Eγ)
↓
H((α∘Eγ)∘Eγ)=(β∘Eγ)∘Eγ
↓
...
```

Therefore:

```text
hopf_composition_law_inference_rule
+
hopf_composition_formula_inference_rule
```

is not treated as unrestricted fixed-point-safe.

The bounded regression reaches `MAX_ROUNDS` while demonstrating actual
increasing composition depth.

Finite tasks use staged execution:

```text
explicit Hopf structural stage
↓
explicit formula stage
↓
finite ZERO / generic stage
↓
FIXED_POINT
```

The principle remains:

```text
mathematical applicability
≠
execution scope
```

---

# Current limitations

- Duplicate identity uses ordinary Python equality.
- The knowledge state keeps the first accepted `ProofStep` for an equal
  conclusion; alternative applications remain in execution traces.
- Pattern matching is structured but not fully general recursive unification.
- Exhaustive premise assignment can grow combinatorially.
- Arbitrary symbolic rule families are not guaranteed to terminate.
- `max_rounds` is a safety bound, not semantic cycle detection.
- Repeated Suspension, functoriality, and recursive Hopf formula application
  can generate unbounded structural depth.
- Automatic rule scheduling / theorem-depth planning is not implemented.
- Canonical `E^n` and composition normalization are not implemented.
- Composition associativity, identity, and bilinearity are not implemented.
- There is no first-class `NONZERO` relation type.
- General inverse-map construction / unrestricted desuspension are not
  implemented.
- Element-level set / subgroup / image / kernel membership is not first-class.
- `H(x)=0` cannot yet produce an explicit `x ∈ Ker(H)=Im(E)` fact or witness.
- Hopf additivity is not implemented.
- Toda brackets, Steenrod operations, double EHP, and odd-primary-specific
  theorem families remain future work.

---

# Tests

Full suite:

```powershell
python -m pytest -v
```

Phase 11 completion:

```text
791 passed in 23.41s
```

Phase 11 suite:

```powershell
python -m pytest tests/test_hopf_rules.py -v
```

Result:

```text
28 passed
```

Focused theorem-scope / termination tests:

```powershell
python -m pytest tests/test_hopf_rules.py::test_phase11_theorem_scope_boundary tests/test_hopf_rules.py::test_phase11_inference_scope_and_termination_boundary -v
```

Result:

```text
2 passed
```

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history

Historical statements in the development log describe the state at that time.
Current behavior is defined by the latest README and design documents.

---

# Phase 11 completion boundary

Phase 11 is complete because the project now supports a traceable vertical
slice:

```text
generalized Hopf fact
↓
composition-law applicability
↓
Hopf composition formula
↓
existing Suspension / composition reasoning
↓
generic ZERO reasoning
↓
Hopf-invariant-zero conclusion
```

together with:

```text
EHP exactness
↓
E-H zero composition
↓
H(Eα)=0
```

without modifying the generic inference engine.

---

# Next development boundary

The next Phase should start from an actual mathematical representation need,
not speculative generic-engine refactoring.

Natural candidates include:

```text
α+β
-α
±α
```

```text
α ∈ A
A ⊆ B
α ∈ Ker(H)
α ∈ Im(E)
```

```text
mod A
Toda-bracket indeterminacy
```

```text
α=kβ+γ
k odd
```

as well as further Toda relations, Toda brackets, Steenrod operations, double
EHP, odd-primary-specific theorem families, and preimage reasoning.

The governing rule remains:

```text
new mathematical knowledge
=
new domain InferenceRule
```

and the generic engine should change only when an actual mathematical rule
cannot be represented correctly with the current infrastructure.
