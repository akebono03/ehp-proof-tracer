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

Completed through Phase 44.

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
Phase 39  PrimaryComponent minimum representation
Phase 40  TodaPrimaryGroup minimum representation
Phase 41  PreimageSubgroup minimum representation
Phase 42  WhiteheadProduct minimum representation
Phase 43  Toda Lemma 4.1 premise minimum representation
Phase 44  Toda Lemma 4.1 case semantics
```

Current full regression:

```text
1957 passed in 75.54s
```

Focused Phase 44 suite:

```text
tests/test_phase44_toda_lemma41_case_semantics.py
94 passed
```

Representative Phase 44 probe:

```powershell
python -m probes.probe_phase44_capabilities
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
├── WhiteheadProduct
├── Composition
├── MapApplication
├── Suspension
└── IteratedSuspension
```

`GeneratorSymbol.index` and `HomotopyElement.dimension` accept symbolic `ScalarValue` values when needed.

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

# Toda Chapter 4 structural group terms

The current structural layer contains:

```text
PrimaryComponent(i,n,p)
→ π_i(S^n;p)

TodaPrimaryGroup(i,n)
→ π_i^n

PreimageSubgroup(f,A)
→ f^-1(A)

FreeCyclicGroup(generator)
→ Z{generator}

DirectSumGroup(summands)
→ structural direct sum

PrimaryComponentMembershipStatement(element,component)
→ element ∈ π_i(S^n;p)
```

These remain distinct from the concrete finitely generated abelian-group calculation layer.

In particular:

```text
PrimaryComponent
!= AbelianGroup

FreeCyclicGroup
!= GroupComponent

DirectSumGroup
!= AbelianGroup
```

---

# Whitehead-product representation

Phase 42 introduced:

```text
WhiteheadProduct(a,b)
→ [a,b]
```

with the structural distinctions:

```text
WhiteheadProduct
!= Composition
!= SmashProduct
```

Phase 43 introduced the minimum relation vocabulary required for Toda Lemma 4.1:

```text
[ι_{n-1},ι_{n-1}] = 0
→ RelationType.ZERO

[ι_{n-1},ι_{n-1}] != 0
→ RelationType.INEQUALITY
```

The Whitehead product itself does not decide either relation.

---

# Phase 44: Toda Lemma 4.1 case semantics

Phase 44 implements the three case branches of Toda Lemma 4.1.

## Odd case

From:

```text
n odd
```

derive:

```text
π_{2n-1}^n
=
π_{2n-1}(S^n;2)
```

The result is represented as an equality between `TodaPrimaryGroup` and `PrimaryComponent`.

## Even / Whitehead nonzero case

From:

```text
n even
[ι_{n-1},ι_{n-1}] != 0
```

derive:

```text
π_{2n-1}^n
=
Z{P(ι_{2n+1})}
⊕
π_{2n-1}(S^n;2)
```

The free summand is represented structurally as `FreeCyclicGroup`, and the full right-hand side as `DirectSumGroup`.

## Even / Whitehead zero case

From:

```text
n even
[ι_{n-1},ι_{n-1}] = 0
```

derive:

```text
π_{2n-1}^n
=
Z{α}
⊕
π_{2n-1}(S^n;2)
```

The same theorem premise also derives:

```text
H(α)=ι_{2n-1}
```

and:

```text
Eα ∈ π_{2n}(S^{n+1};2)
```

The latter is represented by `PrimaryComponentMembershipStatement`.

The group decomposition, Hopf condition, and suspension-primary condition use the same structural `α`.

---

# Phase 44 rule structure

The generic inference engine still assumes one conclusion per `InferenceRule`.

Therefore the zero case uses three domain rules sharing the same premises:

```text
n even
+
[ι_{n-1},ι_{n-1}] = 0
```

to derive independently:

```text
π_{2n-1}^n = Z{α} ⊕ π_{2n-1}(S^n;2)
H(α)=ι_{2n-1}
Eα ∈ π_{2n}(S^{n+1};2)
```

No generic multi-conclusion theorem mechanism was introduced.

---

# Applicability and provenance

Representative applicability:

```text
odd premise
→ odd rule only

even + Whitehead nonzero
→ nonzero rule only

even + Whitehead zero
→ zero group rule only
```

For the zero-case theorem bundle:

```text
group structure rule
Hopf condition rule
suspension-primary condition rule
```

all three are applicable to the same two premises.

Every derived step preserves:

```text
ProofStep.premises
ProofStep.inference_rule
ProofRule.INFERENCE
```

as theorem provenance.

---

# Phase 44 representative probe

Run:

```powershell
python -m probes.probe_phase44_capabilities
```

Representative output includes:

```text
Toda Lemma 4.1: n odd
π_{2n-1}^{n} = π_{2n-1}(S^{n};2)
```

```text
Toda Lemma 4.1: n even + Whitehead nonzero
π_{2n-1}^{n} = Z{P(ι_{2n+1})} ⊕ π_{2n-1}(S^{n};2)
```

```text
Toda Lemma 4.1: n even + Whitehead zero
π_{2n-1}^{n} = Z{α} ⊕ π_{2n-1}(S^{n};2)

H(α)=ι_{2n-1}
Eα ∈ π_{2n}(S^{n+1};2)
```

The zero-case theorem bundle derives three results in one inference round and then reaches a fixed point.

---

# Phase 44 scope boundaries

Still not implemented:

```text
automatic Whitehead-product zero inference
automatic Whitehead-product nonzero inference
ZERO / INEQUALITY contradiction detection
Whitehead-product bilinearity
Whitehead-product antisymmetry
automatic α existence machinery
automatic α uniqueness machinery
general existential witness representation
PrimaryComponent membership → ordinary membership bridge
Toda Prop.4.2 semantics
Toda (4.5) stable-range E^(m-n) isomorphism
Toda Prop.4.4 decomposition theorem
stable homotopy group model
higher / variable-arity Toda brackets
```

Important:

```text
Toda Lemma 4.1 theorem semantics
!=
general Whitehead-product algebra
```

and:

```text
structural α shared across theorem conclusions
!=
general existential witness engine
```

---

# Tests

Focused Phase 44:

```powershell
python -m pytest tests/test_phase44_toda_lemma41_case_semantics.py -q
```

Verified:

```text
94 passed
```

Related regressions:

```powershell
python -m pytest tests/test_toda_rules.py -q
python -m pytest tests/test_phase43_toda_lemma41_premise.py -q
python -m pytest tests/test_phase39_primary_component.py -q
python -m pytest tests/test_hopf_rules.py -q
python -m pytest tests/test_expression.py -q
```

Verified:

```text
66 passed
32 passed
24 passed
31 passed
145 passed
```

Full suite:

```powershell
python -m pytest -q
```

Verified:

```text
1957 passed in 75.54s
```

No failures.

---

# Documentation

- `README.md` — current capabilities and status
- `docs/design.md` — current architecture, semantics, and boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capability dependency

Historical limitations in the development log describe the state at that time. Current behavior is defined by the latest README and design documents.

---

# Next development boundary

Phase 44 is complete.

The Toda Chapter 4 branch now has a theorem-level structural description of `π_{2n-1}^n` in all three Toda Lemma 4.1 cases.

The next planned branch is:

```text
Toda Prop.4.2
2-primary EHP exact sequence
```

Before implementation, the current EHP exactness representation, `PrimaryComponent`, `TodaPrimaryGroup`, and the exact statement of Toda Proposition 4.2 should be checked.

The next phase should add only the minimum representation and theorem semantics required by Proposition 4.2, without introducing general Whitehead-product algebra, existential-witness machinery, or stable-range theorems prematurely.
