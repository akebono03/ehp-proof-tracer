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

Completed through Phase 45.

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
Phase 45  Toda Proposition 4.2 2-primary EHP exact sequence
```

Current full regression:

```text
2060 passed in 70.48s
```

Focused Phase 45 suites:

```text
tests/test_phase45_toda_prop42_compatibility.py
17 passed

tests/test_phase45_toda_prop42_sequence.py
19 passed

tests/test_phase45_toda_prop42_exactness_compatibility.py
17 passed

tests/test_phase45_toda_prop42_exactness_instance.py
18 passed

tests/test_phase45_toda_prop42_theorem_semantics.py
16 passed

tests/test_phase45_toda_prop42_bridge.py
16 passed
```

Representative Phase 45 probe:

```powershell
python -m probes.probe_phase45_capabilities
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

TodaEHPSequence(terms,maps)
→ structural Toda EHP sequence

TodaEHPExactnessWindow(
  source_term,
  middle_term,
  target_term,
  first_map,
  second_map,
)
→ one instance-aware three-term EHP window
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

TodaEHPSequence
!= EHPSegment

TodaEHPExactnessWindow
!= ExactnessStatement
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

# Toda Lemma 4.1 case semantics

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

and:

```text
H(α)=ι_{2n-1}
Eα ∈ π_{2n}(S^{n+1};2)
```

The group decomposition, Hopf condition, and suspension-primary condition use the same structural `α`.

---

# Phase 45: Toda Proposition 4.2

Phase 45 introduces a symbolic representation and theorem semantics for the three exact sequences in Toda Proposition 4.2.

Canonical symbolic maps:

```text
EHP_E_MAP     → E
EHP_H_MAP     → H
EHP_DELTA_MAP → Δ
```

The structural sequence is:

```text
π_i^n
--E→
π_{i+1}^{n+1}
--H→
π_{i+1}^{2n+1}
--Δ→
π_{i-1}^n
--E→
π_i^{n+1}
```

This long sequence is represented by:

```text
TodaEHPSequence
```

It does not itself assert exactness.

---

# Toda Proposition 4.2 exactness windows

The proposition is represented as three exactness windows.

## E-H window

```text
π_i^n
--E→
π_{i+1}^{n+1}
--H→
π_{i+1}^{2n+1}
```

## H-Δ window

```text
π_{i+1}^{n+1}
--H→
π_{i+1}^{2n+1}
--Δ→
π_{i-1}^n
```

## Δ-E window

```text
π_{i+1}^{2n+1}
--Δ→
π_{i-1}^n
--E→
π_i^{n+1}
```

Each window is represented by:

```text
TodaEHPExactnessWindow
```

which stores:

```text
source_term
middle_term
target_term
first_map
second_map
```

The window object is representation only and does not contain an `is_exact` field.

---

# Toda Proposition 4.2 theorem statements

Phase 45 introduces:

```text
TodaProp42ExactnessStatement(window)
```

This is the instance-aware theorem result that the supplied `TodaEHPExactnessWindow` is exact.

The three domain rules are:

```text
toda_prop42_e_h_exactness_inference_rule()

toda_prop42_h_delta_exactness_inference_rule()

toda_prop42_delta_e_exactness_inference_rule()
```

Each rule checks both:

```text
map order
symbolic group-dimension structure
```

before deriving the theorem statement.

The generic inference engine is unchanged.

---

# Instance-aware exactness

A key Phase 45 distinction is:

```text
TodaProp42ExactnessStatement
=
instance-aware theorem knowledge
```

For example:

```text
(i,n) E-H exactness
!=
(j,m) E-H exactness
```

when the group terms differ.

By contrast:

```text
ExactnessStatement(
  first_map=E,
  second_map=H,
  is_exact=True,
)
```

does not retain the group terms and therefore does not identify the symbolic `(i,n)` instance.

The instance-aware Toda statement is the authoritative theorem result.

---

# Generic exactness bridge

Phase 45 adds:

```text
toda_prop42_exactness_to_generic_inference_rule()
```

which derives:

```text
TodaProp42ExactnessStatement(window)
↓
ExactnessStatement(
  first_map=window.first_map,
  second_map=window.second_map,
  is_exact=True,
)
```

The generic projection is intentionally instance-lossy.

This permits existing generic EHP exactness infrastructure to be reused without changing `ExactnessStatement`.

---

# Existing generic EHP consequences

The Phase 45 representative run connects Toda Proposition 4.2 to the existing zero-composition rule.

```text
E-H exact
→ H∘E = 0

H-Δ exact
→ Δ∘H = 0

Δ-E exact
→ E∘Δ = 0
```

The end-to-end inference path is:

```text
TodaEHPExactnessWindow
↓
TodaProp42ExactnessStatement
↓
ExactnessStatement
↓
EHPZeroCompositionStatement
```

Representative inference reaches fixed point in three derived rounds:

```text
round 1
3 Toda theorem exactness statements

round 2
3 generic exactness statements

round 3
3 zero-composition statements

fixed point
```

---

# Applicability and provenance

The three Toda Proposition 4.2 rules use the same premise type:

```text
TodaEHPExactnessWindow
```

so pattern-level candidate search may return all three rules.

Actual theorem applicability is determined by guard-aware matching:

```text
find_inference_match()
```

which evaluates the rule `match_guard`.

Therefore:

```text
pattern-level candidate
!=
guard-aware inference match
```

For a valid E-H, H-Δ, or Δ-E window, exactly one of the three theorem rules produces an inference match.

Every derived theorem step preserves:

```text
ProofStep.premises
ProofStep.inference_rule
ProofRule.INFERENCE
```

The generic bridge also preserves the Toda theorem step as its premise.

---

# Phase 45 representative probe

Run:

```powershell
python -m probes.probe_phase45_capabilities
```

Representative output includes:

```text
π_i^n -E→ π_{i+1}^{n+1} -H→ π_{i+1}^{2n+1}
π_{i+1}^{n+1} -H→ π_{i+1}^{2n+1} -Δ→ π_{i-1}^n
π_{i+1}^{2n+1} -Δ→ π_{i-1}^n -E→ π_i^{n+1}
```

then:

```text
E-H exact
H-Δ exact
Δ-E exact
```

and existing generic consequences:

```text
H∘E = 0
Δ∘H = 0
E∘Δ = 0
```

The representative run reports:

```text
theorem exactness count = 3
generic exactness count = 3
zero composition count = 3
derived round count = 3
fixed point = True
```

---

# Phase 45 scope boundaries

Still not implemented:

```text
symbolic map typing solver
general symbolic dimension solver
automatic symbolic kernel/image groups for TodaEHPExactnessWindow
instance-aware generic ExactnessStatement
Toda (4.5) stable-range suspension isomorphism
Toda Proposition 4.4 decomposition theorem
Toda Proposition 4.4 consequence: E injective
stable homotopy group model
general Whitehead-product algebra
automatic Whitehead-product zero / nonzero solver
general existential witness machinery
higher Toda brackets
```

Important:

```text
TodaEHPExactnessWindow
!=
exactness theorem
```

and:

```text
TodaProp42ExactnessStatement
!=
generic ExactnessStatement
```

and:

```text
instance-aware theorem result
!=
instance-lossy generic projection
```

---

# Tests

Focused Phase 45:

```powershell
python -m pytest tests/test_phase45_toda_prop42_compatibility.py -q
python -m pytest tests/test_phase45_toda_prop42_sequence.py -q
python -m pytest tests/test_phase45_toda_prop42_exactness_compatibility.py -q
python -m pytest tests/test_phase45_toda_prop42_exactness_instance.py -q
python -m pytest tests/test_phase45_toda_prop42_theorem_semantics.py -q
python -m pytest tests/test_phase45_toda_prop42_bridge.py -q
```

Verified:

```text
17 passed
19 passed
17 passed
18 passed
16 passed
16 passed
```

Related regressions:

```powershell
python -m pytest tests/test_toda_rules.py -q
python -m pytest tests/test_ehp_rules.py -q
python -m pytest tests/test_inference_rule_pattern.py -q
```

Verified:

```text
66 passed
26 passed
438 passed
```

Full suite:

```powershell
python -m pytest -q
```

Verified:

```text
2060 passed in 70.48s
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

Phase 45 is complete.

The Toda Chapter 4 branch now contains theorem-level, instance-aware exactness semantics for Toda Proposition 4.2 and a bridge into the existing generic exactness infrastructure.

The next planned branch is:

```text
Toda (4.5)
stable-range E^(m-n) isomorphism
```

Before implementation, the current iterated-suspension representation, map isomorphism statements, symbolic dimension handling, and exact formulation of Toda (4.5) should be checked.

Toda Proposition 4.4 remains later and must not be introduced as part of the Toda (4.5) compatibility phase.
