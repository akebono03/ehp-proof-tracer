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

Completed through Phase 33.

```text
Phase 28  map injectivity / isomorphism / equality reflection
Phase 29  actual H facts / typing / isomorphism
Phase 30  Toda Prop.2.2 right formula
Phase 31  SmashProduct minimum representation
Phase 32  Toda Prop.2.2 left formula
Phase 33  Barratt–Hilton prerequisite minimum representation
```

Current full regression:

```text
1585 passed in 23.09s
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

Phase 33 scalar-expression structures:

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
algebraic theorem equality
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

Phase 33 adds only the minimum representation and sign machinery needed before Toda Prop.3.1 itself.

## Symbolic scalar expressions

Lossless structural representation is available for:

```text
p+k
q+h
(p+k)h
ph
(-1)^((p+k)h)
(-1)^(ph)
```

For example:

```text
(-1)^((p+k)h)
```

is represented as a `ScalarPower` whose exponent is a `ScalarProduct` containing `ScalarSum(p,k)` and `h`.

No general-purpose CAS or automatic normalization is implemented.

## IteratedSuspension

The existing `IteratedSuspension` accepts symbolic scalar exponents needed for:

```text
E^q a
E^(p+k)b
E^p b
E^(q+h)a
```

Current boundary:

```text
symbolic exponent
→ source = None
→ target = None
```

Concrete integer exponent typing remains unchanged.

## Parity-driven sign evaluation

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

No automatic compound parity inference is implemented.

## Symbolic sign and Multiple

`Multiple` can use symbolic scalar coefficients, so:

```text
(-1)^n a
```

is structural syntax.

With an explicit sign evaluation:

```text
(-1)^n=1
↓
(-1)^n a=a
```

```text
(-1)^n=-1
↓
(-1)^n a=-a
```

The additive inverse remains:

```text
-a = Multiple(-1,a)
```

## Barratt–Hilton formula statement representation

Phase 33 can represent both Toda Prop.3.1 formula shapes as structural `RelationType.EQUALITY` objects:

```text
a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
```

and:

```text
a∧b
=
(-1)^(ph)
(E^p b∘E^(q+h)a)
```

Important:

```text
formula is representable
!=
formula is theorem-derived
```

Toda Prop.3.1 theorem inference is not yet implemented.

---

# Phase 33 representative capability demo

Run:

```powershell
python -m probes.probe_phase33_capabilities
```

Representative inference:

```text
((p+k)h) is even
↓
(-1)^((p+k)h)=1
↓
(-1)^((p+k)h)(E^q a∘E^(p+k)b)
=
E^q a∘E^(p+k)b
```

The probe also confirms:

```text
formula is Relation: True
formula is ProofStep: False
symbolic exponent source = None
symbolic exponent target = None
```

---

# Tests

Focused Phase 33 suite:

```powershell
python -m pytest tests/test_phase33_barratt_hilton.py -q
```

Verified:

```text
73 passed in 0.31s
```

Related scalar suite:

```powershell
python -m pytest tests/test_scalar_rules.py -q
```

Verified during Phase 33:

```text
18 passed
```

Full suite:

```powershell
python -m pytest -q
```

Verified at Phase 33 completion:

```text
1585 passed in 23.09s
```

No failures.

---

# Current non-goals

Not currently implemented:

- general symbolic scalar algebra,
- scalar commutativity / distributivity normalization,
- automatic compound parity inference,
- general smash-product typing,
- smash-product algebra / normalization,
- symbolic source / target arithmetic for iterated suspensions,
- Toda (2.1) composition formulas,
- Toda Prop.3.1 Barratt–Hilton theorem inference,
- automatic calculation of `H((2ι₂)η₂)`,
- `H((2ι₂)η₂)=H(4η₂)`,
- `(2ι₂)η₂=4η₂`,
- stable homotopy-group model,
- stable Toda brackets,
- higher / variable-arity Toda brackets.

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
Phase 34
Toda Prop.3.1 Barratt–Hilton theorem rule
```

Phase 34 should reuse the Phase 33 syntax and add explicit literature-backed theorem inference only. It should not generalize Barratt–Hilton into unrestricted smash-product algebra.

Longer dependency:

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
Toda Prop.3.1 Barratt–Hilton
↓
Phase 35+
actual H((2ι₂)η₂) calculation
↓
H((2ι₂)η₂)=H(4η₂)
↓
existing Injective(H) equality reflection
↓
(2ι₂)η₂=4η₂
```
