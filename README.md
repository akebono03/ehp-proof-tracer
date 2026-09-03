# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The project separates mathematical theorem knowledge, explicit facts, the generic inference engine, and algebraic calculation. Development follows:

```text
actual mathematical need
↓
minimum representation
↓
explicit fact / domain rule when needed
↓
existing generic engine
```

---

# Current status

Completed through Phase 34.

```text
Phase 28  map injectivity / isomorphism / equality reflection
Phase 29  actual H facts / typing / isomorphism
Phase 30  Toda Prop.2.2 right formula
Phase 31  SmashProduct minimum representation
Phase 32  Toda Prop.2.2 left formula
Phase 33  Barratt–Hilton prerequisite minimum representation
Phase 34  Toda Prop.3.1 Barratt–Hilton theorem rules
```

Current full regression:

```text
1620 passed in 23.32s
```

Focused Phase 34 suite:

```text
35 passed
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
├── SmashProduct
├── Composition
├── MapApplication
├── Suspension
└── IteratedSuspension
```

Scalar-expression structures:

```text
ScalarExpression
├── ScalarSymbol
├── ScalarSum
├── ScalarProduct
└── ScalarPower
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

# Toda Prop.2.2

Phase 30 / 32 provide direct theorem rules for:

```text
H(a∘Eb)=H(a)∘Eb
```

and:

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

Both preserve the canonical production `H` map identity.

---

# Phase 33: Barratt–Hilton prerequisites

Phase 33 added only the minimum representation and sign machinery required before Toda Prop.3.1 itself.

Representable:

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

```text
n odd
↓
(-1)^n=-1
```

With an explicit sign evaluation:

```text
(-1)^n a=a
```

or:

```text
(-1)^n a=-a
```

The additive inverse remains represented as:

```text
-a = Multiple(-1,a)
```

Phase 33 could represent the two Barratt–Hilton formulas structurally, but did not yet derive them as theorem-backed `ProofStep` objects.

---

# Phase 34: Toda Prop.3.1 Barratt–Hilton theorem rules

Phase 34 adds the minimum theorem-applicability representation and direct literature-backed theorem rules for Toda Prop.3.1.

## Symbolic homotopy-group membership

Phase 34 introduces:

```text
HomotopyGroupMembershipStatement
```

which can represent:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
```

without adding symbolic `HomotopyElement.source` / `target` arithmetic.

Important boundary:

```text
symbolic homotopy-group membership
!=
symbolic source / target solver
```

---

## First Barratt–Hilton theorem rule

From:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
```

the first direct theorem rule derives:

```text
a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
```

as an inference-generated `ProofStep`.

Applicability is strict:

```text
missing membership
wrong group dimension
wrong sphere dimension
wrong element
→ no match
```

Unrelated available knowledge does not block inference; the generic engine selects the two required premises.

---

## Second Barratt–Hilton theorem rule

The same typing premises also derive:

```text
a∧b
=
(-1)^(ph)
(E^p b∘E^(q+h)a)
```

The first and second formulas remain structurally distinct and are produced by separate theorem rules.

---

## Literature provenance

Both formulas preserve a structured reference to:

```text
Toda Prop.3.1
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Proposition 3.1
```

The proof trace therefore separates:

```text
proof premises
→ ProofStep.premises

inference identity
→ ProofStep.inference_rule

literature source
→ Relation.source

formula identity
→ Relation.note
```

No general theorem-repository refactor was introduced.

---

## Sign-evaluation connection

Phase 34 reuses the Phase 33 sign machinery directly.

Representative chain:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
↓ Toda Prop.3.1
a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)

+

((p+k)h) is even
↓
(-1)^((p+k)h)=1
↓
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
=
E^q a∘E^(p+k)b

↓ equality transitivity

a∧b
=
E^q a∘E^(p+k)b
```

Odd parity similarly reduces the signed term to its additive inverse.

No Barratt–Hilton-specific sign bridge was needed.

---

# Phase 34 representative capability demo

Run:

```powershell
python -m probes.probe_phase34_capabilities
```

The probe displays:

```text
typing premises
↓
Toda Prop.3.1
↓
Barratt–Hilton theorem equality
↓
explicit parity
↓
sign evaluation
↓
signed Multiple reduction
↓
equality transitivity
↓
reduced Barratt–Hilton equality
```

It also displays:

```text
source: Toda Prop.3.1
locator: Proposition 3.1
theorem result is ProofStep: True
final result is ProofStep: True
symbolic suspension source/target = None
```

and confirms that actual `H((2ι₂)η₂)` calculation is still outside Phase 34.

---

# Phase 34 scope boundaries

Still not implemented:

```text
automatic compound parity inference
general symbolic scalar algebra
general SmashProduct normalization
general SmashProduct typing
symbolic suspension source / target arithmetic
Toda (2.1) composition formulas
actual H((2ι₂)η₂) calculation
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
```

Important:

```text
Barratt–Hilton theorem inference
!=
general smash-product rewrite system
```

and:

```text
Toda Prop.3.1
!=
actual Hopf-invariant calculation
```

---

# Tests

Focused Phase 34 suite:

```powershell
python -m pytest tests/test_phase34_barratt_hilton.py -q
```

Verified:

```text
35 passed
```

Related regressions:

```powershell
python -m pytest tests/test_phase33_barratt_hilton.py -q
python -m pytest tests/test_scalar_rules.py -q
python -m pytest tests/test_relation_rules.py -q
```

Verified:

```text
73 passed
18 passed
50 passed
```

Full suite:

```powershell
python -m pytest -q
```

Verified at Phase 34 completion:

```text
1620 passed in 23.32s
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

Next:

```text
Phase 35+
actual H((2ι₂)η₂) calculation
```

The intended dependency is:

```text
Phase 29
actual H equality-reflection foundation
↓
Phase 30
Toda Prop.2.2 right COMPLETE
↓
Phase 31
SmashProduct minimum representation COMPLETE
↓
Phase 32
Toda Prop.2.2 left COMPLETE
↓
Phase 33
Barratt–Hilton prerequisites COMPLETE
↓
Phase 34
Toda Prop.3.1 Barratt–Hilton COMPLETE
↓
Phase 35+
actual H((2ι₂)η₂)
↓
H((2ι₂)η₂)=H(4η₂)
↓
existing Injective(H) equality reflection
↓
(2ι₂)η₂=4η₂
```

Phase 35+ should introduce only the concrete theorem/fact/algebraic machinery required by the actual `H((2ι₂)η₂)` calculation and should continue to avoid unrelated general symbolic algebra.
