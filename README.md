# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The project separates mathematical theorem knowledge, explicit facts, the generic inference engine, and algebraic calculation.

Development follows:

```text
actual mathematical need
↓
minimum representation
↓
explicit fact / domain rule when needed
↓
existing generic inference engine
```

Important boundaries:

```text
representation
!=
typing
!=
theorem knowledge
```

```text
structural equality
!=
mathematical equality
```

---

# Current status

Completed through Phase 38.

```text
Phase 28  map injectivity / isomorphism / equality reflection
Phase 29  actual H facts / typing / isomorphism
Phase 30  Toda Prop.2.2 right formula
Phase 31  SmashProduct minimum representation
Phase 32  Toda Prop.2.2 left formula
Phase 33  Barratt-Hilton prerequisite minimum representation
Phase 34  Toda Prop.3.1 Barratt-Hilton theorem rules
Phase 35  actual H((2ι₂)η₂) calculation
Phase 36  actual H(4η₂) calculation
Phase 37  actual H-side equality closure
Phase 38  Injective(H) reflection
```

Current full regression:

```text
1711 passed in 60.38s
```

Focused Phase 38 suite:

```text
13 passed
```

Representative Phase 38 probe:

```powershell
python -m probes.probe_phase38_capabilities
```

The probe reaches:

```text
(2ι₂)η₂=4η₂
```

as an actual inference-generated `ProofStep`.

---

# Expression model

Current expression classes include:

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Sum
├── SmashProduct
├── Composition
├── MapApplication
├── Suspension
└── IteratedSuspension
```

Scalar-expression structures include:

```text
ScalarExpression
├── ScalarSymbol
├── ScalarSum
├── ScalarProduct
└── ScalarPower
```

The expression layer remains structural syntax. Constructors do not perform theorem-aware normalization.

---

# Toda Prop.2.2

Phase 30 and Phase 32 provide direct theorem rules for:

```text
H(a∘Eb)=H(a)∘Eb
```

and:

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

Both use the canonical production `EHP_H_MAP`.

---

# Phase 33: Barratt-Hilton prerequisites

Phase 33 added the minimum symbolic structures required before Toda Prop.3.1:

```text
p+k
q+h
(p+k)h
ph
(-1)^((p+k)h)
(-1)^(ph)
```

and:

```text
E^q a
E^(p+k)b
E^p b
E^(q+h)a
```

Explicit parity facts can derive:

```text
n even
↓
(-1)^n=1
```

and:

```text
n odd
↓
(-1)^n=-1
```

The evaluated sign can then reduce a symbolic `Multiple`.

No general scalar CAS was introduced.

---

# Phase 34: Toda Prop.3.1 Barratt-Hilton theorem rules

Phase 34 introduced:

```text
HomotopyGroupMembershipStatement
```

and direct literature-backed first / second Barratt-Hilton theorem rules.

From:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
```

the first rule derives:

```text
a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
```

and the second rule derives:

```text
a∧b
=
(-1)^(ph)
(E^p b∘E^(q+h)a)
```

Both preserve structured provenance for:

```text
Toda Prop.3.1
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Proposition 3.1
```

Important:

```text
Barratt-Hilton theorem inference
!=
general smash-product rewrite system
```

---

# Phase 35: actual H((2ι₂)η₂) calculation

Phase 35 connects the Phase 30–34 theorem infrastructure to one concrete calculation.

## Actual Hopf-invariant fact

Phase 35 adds the literature-backed fact:

```text
H(η₂)=ι₃
```

with provenance:

```text
Toda Prop.5.1
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Proposition 5.1
```

The fact is represented as a `HopfInvariantStatement` and bridged to the canonical actual `EHP_H_MAP`.

---

## Concrete Toda Prop.2.2 left application

Using:

```text
c=2ι₁
a=η₂
```

the existing left formula gives:

```text
H((E(2ι₁))∘η₂)
=
E((2ι₁)∧(2ι₁))∘H(η₂)
```

---

## Concrete Barratt-Hilton instantiation

Phase 35 extends the membership statement only enough to accept actual expressions such as:

```text
2ι₁ ∈ π₁(S¹)
```

For the concrete parameters:

```text
a=2ι₁
b=2ι₁
p=1
q=1
k=0
h=0
```

Toda Prop.3.1 derives:

```text
2ι₁∧2ι₁
=
(-1)^(1·0)
(E^1(2ι₁)∘E^1(2ι₁))
```

Concrete integer additions inside the theorem parameter construction are folded only where needed for applicability. This is not general scalar simplification.

---

## Concrete parity and sign reduction

With the explicit fact:

```text
1·0 is even
```

the existing Phase 33 machinery derives:

```text
(-1)^(1·0)=1
```

and then:

```text
2ι₁∧2ι₁
=
E^1(2ι₁)∘E^1(2ι₁)
```

No automatic parity solver is introduced.

---

## Suspension and multiple calculation

Phase 35 adds the minimum bridges required for the concrete calculation.

Actual suspension facts:

```text
Eι₁=ι₂
Eι₂=ι₃
```

combined with Suspension homomorphism reasoning give:

```text
E(2ι₁)=2ι₂
E(2ι₂)=2ι₃
```

A proof-level bridge connects:

```text
E^1x=Ex
```

without changing structural equality.

Therefore:

```text
E(2ι₁∧2ι₁)
=
2ι₃∘2ι₃
```

---

## Directed Toda (2.1) calculation

Phase 35 adds only the concrete direction required by the calculation:

```text
a∘(kb)=k(a∘b)
```

together with an explicit right-identity premise and nested integer-multiple reduction.

This gives:

```text
2ι₃∘2ι₃
=
2((2ι₃)∘ι₃)
=
2(2ι₃)
=
4ι₃
```

Hence:

```text
E(2ι₁∧2ι₁)=4ι₃
```

Important:

```text
directed Toda (2.1) support
!=
general composition bilinearity
```

---

## Actual H equality transport

Phase 35 adds a narrow equality-preservation rule for the canonical actual `EHP_H_MAP`:

```text
x=y
↓
H(x)=H(y)
```

This is deliberately not a universal arbitrary-map congruence rule.

Using:

```text
E(2ι₁)=2ι₂
```

the left input becomes:

```text
(E(2ι₁))∘η₂
=
(2ι₂)∘η₂
```

and therefore:

```text
H((E(2ι₁))∘η₂)
=
H((2ι₂)∘η₂)
```

---

# Phase 35 final chain

The representative proof is:

```text
E(2ι₁)=2ι₂
↓
(E(2ι₁))∘η₂=(2ι₂)∘η₂
↓
H((E(2ι₁))∘η₂)=H((2ι₂)∘η₂)

Toda Prop.2.2 left
↓
H((E(2ι₁))∘η₂)
=
E(2ι₁∧2ι₁)∘H(η₂)

Toda Prop.3.1
+
explicit parity / sign reduction
↓
2ι₁∧2ι₁
=
E^1(2ι₁)∘E^1(2ι₁)

Suspension / multiple calculation
+
Toda (2.1)
↓
E(2ι₁∧2ι₁)=4ι₃

Toda Prop.5.1
↓
H(η₂)=ι₃

right-identity composition
↓
E(2ι₁∧2ι₁)∘H(η₂)=4ι₃

equality transitivity
↓
H((2ι₂)∘η₂)=4ι₃
```

This is the completed Phase 35 mathematical capability.

---

# Phase 35 provenance

The representative proof retains dependencies on:

```text
Toda Prop.2.2 left
Toda Prop.3.1
Toda Prop.5.1
Toda (2.1)
```

as well as explicit Suspension / identity / parity facts and generic equality transport.

The generic inference engine remains unchanged.

---


# Phase 36: actual H(4η₂) calculation

Phase 36 computes the parallel actual Hopf-invariant value:

```text
H(4η₂)=4ι₃
```

The existing generic homomorphism machinery already provides:

```text
Homomorphism(f)
↓
f(kx)=k f(x)
```

Phase 36 adds only the narrow actual-H materialization:

```text
ehp_h_homomorphism_proof_step()
↓
Homomorphism(EHP_H_MAP)
```

This is an explicit actual-map fact. It does not add a general rule:

```text
Isomorphism(f)
↛
Homomorphism(f)
```

and does not infer homomorphism properties from arbitrary `MapSymbol` values.

Using the existing generic rule gives:

```text
H(4η₂)=4H(η₂)
```

The existing Toda Prop.5.1 fact:

```text
H(η₂)=ι₃
```

is transported under `Multiple`:

```text
4H(η₂)=4ι₃
```

Equality transitivity then yields:

```text
H(4η₂)=4ι₃
```

The generic inference engine remains unchanged.

---

# Phase 36 scope boundaries

Now implemented:

```text
actual Homomorphism(H) materialization
H(4η₂)=4H(η₂)
4H(η₂)=4ι₃
H(4η₂)=4ι₃
```

Still not implemented:

```text
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
```

Important boundaries remain:

```text
actual Homomorphism(H)
!=
automatic arbitrary-map homomorphism inference
```

```text
Isomorphism(H)
↛
Homomorphism(H) automatically
```

```text
H((2ι₂)η₂)=4ι₃
+
H(4η₂)=4ι₃
↛
direct transitivity
```

Phase 37 must first reverse the second equality and derive:

```text
H((2ι₂)η₂)=H(4η₂)
```

before Phase 38 can reuse existing `Injective(H)` reflection.

---

# Phase 37: actual H-side equality closure

Phase 37 combines the two completed actual calculations:

```text
H((2ι₂)η₂)=4ι₃
H(4η₂)=4ι₃
```

using only existing generic equality rules.

First, equality symmetry reverses the Phase 36 result:

```text
H(4η₂)=4ι₃
↓ symmetry
4ι₃=H(4η₂)
```

Then equality transitivity closes the H-side equality:

```text
H((2ι₂)η₂)=4ι₃
4ι₃=H(4η₂)
↓ transitivity
H((2ι₂)η₂)=H(4η₂)
```

No new theorem rule, production algebra, or generic inference-engine feature was added.

The representative proof graph preserves the actual Phase 35 and Phase 36 branches:

```text
Phase 37 final
├── Phase 35 final: H((2ι₂)η₂)=4ι₃
└── symmetry
    └── Phase 36 final: H(4η₂)=4ι₃
```

Important boundary:

```text
H((2ι₂)η₂)=H(4η₂)
!=
(2ι₂)η₂=4η₂
```

The latter requires the existing actual `Injective(H)` machinery and belongs to Phase 38.

---

# Phase 38: Injective(H) reflection

Phase 38 reuses the existing Phase 28/29 map-property machinery without adding a new production theorem rule.

The actual `H` isomorphism fact materializes:

```text
Isomorphism(H)
```

and the existing generic rule derives:

```text
Isomorphism(H)
↓
Injective(H)
```

Phase 37 already provides:

```text
H((2ι₂)η₂)=H(4η₂)
```

Both sides are `MapApplication` values using the same canonical `EHP_H_MAP`. The existing injective-map equality-reflection rule therefore applies:

```text
Injective(H)
+
H((2ι₂)η₂)=H(4η₂)
↓
(2ι₂)η₂=4η₂
```

The final proof graph preserves both branches:

```text
(2ι₂)η₂=4η₂
├── Injective(H)
│   └── Isomorphism(H)
└── H((2ι₂)η₂)=H(4η₂)
    ├── Phase 35 final
    └── symmetry
        └── Phase 36 final
```

No new H-specific reflection theorem, direct `Isomorphism(H)` reflection, or unrestricted arbitrary-map reflection was introduced.

Phase 38 scope regressions confirm:

```text
Isomorphism(H) + H(a)=H(b)
↛ direct reflection

Injective(H) + H(a)=c
↛ reflection

Injective(H) + a=b
↛ reflection
```

Focused Phase 38 suite:

```text
13 passed
```

Full regression at Phase 38 completion:

```text
1711 passed in 60.38s
```

Representative probe:

```powershell
python -m probes.probe_phase38_capabilities
```

---

# Phase 35 historical scope boundaries

Still not implemented:

```text
H(4η₂)=4ι₃
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
```

Also intentionally not implemented as general systems:

```text
general symbolic scalar algebra
scalar commutativity / distributivity normalization
automatic compound parity inference
general SmashProduct typing
general SmashProduct algebra / normalization
symbolic source / target arithmetic for iterated suspensions
general composition bilinearity
unrestricted bidirectional Toda (2.1) rewriting
universal arbitrary-map equality congruence
automatic identity-map inference from ι notation
stable homotopy-group model
stable Toda brackets
higher / variable-arity Toda brackets
```

Important:

```text
H((2ι₂)η₂)=4ι₃
+
Injective(H)
↛
(2ι₂)η₂=4η₂
```

because injective-map reflection requires an equality of the form:

```text
H(a)=H(b)
```

The next branch must first derive:

```text
H(4η₂)=4ι₃
```

and then:

```text
H((2ι₂)η₂)=H(4η₂)
```

before reusing the existing `Injective(H)` equality reflection.

---

# Tests

Focused Phase 38 suite:

```powershell
python -m pytest tests/test_phase38_injective_reflection.py -q
```

Verified:

```text
13 passed
```

Related regressions:

```powershell
python -m pytest tests/test_phase35_actual_h_calculation.py -q
python -m pytest tests/test_phase36_actual_h_multiple.py -q
python -m pytest tests/test_relation_rules.py -q
python -m pytest tests/test_map_property_rules.py -q
```

Verified at Phase 37 completion:

```text
53 passed
14 passed
50 passed
26 passed
```

Full suite:

```powershell
python -m pytest -q
```

Verified at Phase 38 completion:

```text
1711 passed in 60.38s
```

No failures.

---

# Representative capability demos

```powershell
python -m probes.probe_phase25_capabilities
python -m probes.probe_phase26_capabilities
python -m probes.probe_phase27_capabilities
python -m probes.probe_phase28_capabilities
python -m probes.probe_phase29_capabilities
python -m probes.probe_phase30_capabilities
python -m probes.probe_phase31_capabilities
python -m probes.probe_phase32_capabilities
python -m probes.probe_phase33_capabilities
python -m probes.probe_phase34_capabilities
python -m probes.probe_phase35_capabilities
python -m probes.probe_phase36_capabilities
python -m probes.probe_phase37_capabilities
python -m probes.probe_phase38_capabilities
```

The Phase 35 and Phase 36 probes demonstrate the two parallel actual calculations:

```text
H((2ι₂)∘η₂)=4ι₃
H(4η₂)=4ι₃
```

The Phase 37 probe combines them by symmetry and transitivity:

```text
H((2ι₂)η₂)=H(4η₂)
```

The Phase 38 probe applies the existing injectivity reflection:

```text
(2ι₂)η₂=4η₂
```

---

# Documentation

- `README.md` — current capabilities and status
- `docs/design.md` — current architecture, semantics, and boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capability dependency

Historical limitations in the development log describe the state at that time. Current behavior is defined by the latest README and design documents.

---

# Next development boundary

Phase 38 is complete.

The actual equality branch now reaches:

```text
H((2ι₂)η₂)=4ι₃
H(4η₂)=4ι₃
↓
H((2ι₂)η₂)=H(4η₂)
↓
Injective(H)
↓
(2ι₂)η₂=4η₂
```

The next major planned branch is the Toda Chapter 4 2-primary calculation infrastructure described in `docs/roadmap.md`. The first implementation step should be chosen only after current code inspection and should preserve the existing principle of adding the minimum representation required by an actual mathematical need.
