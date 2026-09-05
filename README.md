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

Completed through Phase 47.

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
Phase 46  Toda (4.5) stable-range E^(m-n) isomorphism
Phase 47  Toda Proposition 4.4 decomposition isomorphism
```

Current full regression:

```text
2277 passed in 55.61s
```

Focused Phase 47 suites:

```text
tests/test_phase47_toda_prop44_compatibility.py
20 passed

tests/test_phase47_toda_prop44_decomposition_groups.py
17 passed

tests/test_phase47_toda_prop44_decomposition_map.py
27 passed

tests/test_phase47_toda_prop44_toda_membership.py
15 passed

tests/test_phase47_toda_prop44_theorem_semantics.py
22 passed

tests/test_phase47_toda_prop44_applicability_compatibility.py
21 passed

tests/test_phase47_toda_prop44_probe.py
12 passed
```

Representative Phase 47 probe:

```powershell
python -m probes.probe_phase47_capabilities
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
→ structural direct sum including FreeCyclicGroup / PrimaryComponent / TodaPrimaryGroup summands

PrimaryComponentMembershipStatement(element,component)
→ element ∈ π_i(S^n;p)

TodaPrimaryGroupMembershipStatement(element,group)
→ element ∈ π_i^n

TodaProp44DecompositionMap(source_group,target_group,alpha,beta,gamma,formula)
→ instance-aware Toda Proposition 4.4 decomposition map

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

# Phase 46: Toda (4.5) stable-range suspension isomorphism

Phase 46 represents and derives Toda (4.5):

```text
n ≥ k+2
m ≥ n
```

implies:

```text
E^(m-n):
π_{n+k}^n
→
π_{m+k}^m
```

is an isomorphism.

Phase 46 keeps four layers distinct:

```text
stable-range premise representation
!=
iterated-suspension map representation
!=
Toda theorem statement
!=
generic map-property statement
```

---

# Stable-range premise representation

Phase 46 introduces:

```text
ScalarGreaterEqualStatement(left,right)
```

with `left` and `right` both using `ScalarValue`.

Representative premises:

```text
ScalarGreaterEqualStatement(
  left=n,
  right=k+2,
)
→ n ≥ k+2
```

```text
ScalarGreaterEqualStatement(
  left=m,
  right=n,
)
→ m ≥ n
```

The statement is structural only.

It does not contain:

```text
evaluate()
is_true
solve()
```

and does not provide a general symbolic inequality solver.

---

# Toda iterated-suspension map

Phase 46 introduces:

```text
TodaIteratedSuspensionMap
├── exponent: ScalarValue
├── source_group: TodaPrimaryGroup
└── target_group: TodaPrimaryGroup
```

Representative:

```text
TodaIteratedSuspensionMap(
  exponent=m-n,
  source_group=π_{n+k}^n,
  target_group=π_{m+k}^m,
)
```

This represents the map-level object:

```text
E^(m-n):
π_{n+k}^n
→
π_{m+k}^m
```

Important:

```text
TodaIteratedSuspensionMap
!= IteratedSuspension
```

`IteratedSuspension` remains an element-level expression.

Also:

```text
TodaIteratedSuspensionMap
!= MapSymbol
```

The constructor stores structure only and does not solve dimension compatibility.

---

# Toda (4.5) theorem statement

Phase 46 introduces:

```text
Toda45IsomorphismStatement(map)
```

where `map` is the specific `TodaIteratedSuspensionMap`.

Meaning:

```text
the supplied iterated-suspension map
is an isomorphism by Toda (4.5)
```

This is an instance-aware theorem result.

For different symbolic source / target / exponent data:

```text
Toda45IsomorphismStatement(first_map)
!=
Toda45IsomorphismStatement(second_map)
```

when the underlying map instances differ.

---

# Toda (4.5) inference rule

The domain rule is:

```text
toda_45_isomorphism_inference_rule()
```

Premises:

```text
n ≥ k+2

m ≥ n

E^(m-n):
π_{n+k}^n
→
π_{m+k}^m
```

Conclusion:

```text
Toda45IsomorphismStatement(
  map=the supplied map instance
)
```

The rule uses `match_guard` to verify the shared symbolic structure:

```text
stable-range right side = k+2
second inequality = m ≥ n
source = π_{n+k}^n
target = π_{m+k}^m
exponent = m-n
```

It does not evaluate whether supplied inequality premises are numerically true.

Premise truth remains external theorem/fact knowledge.

---

# Phase 46 applicability and provenance

A valid representative instance derives exactly one theorem result.

Invalid or mismatched structures are rejected, including:

```text
missing n ≥ k+2
missing m ≥ n
missing iterated-suspension map
different n instance
different k instance
different m instance
wrong source-group shape
wrong target-group shape
wrong exponent
```

Every derived theorem step preserves:

```text
ProofStep.premises
ProofStep.inference_rule
ProofRule.INFERENCE
```

Representative inference reaches fixed point in one derived round:

```text
3 GIVEN premises
↓
1 Toda45IsomorphismStatement
↓
fixed point
```

---

# Generic isomorphism compatibility boundary

The existing generic map-property statements remain:

```text
IsomorphismStatement(map: MapSymbol)
InjectiveMapStatement(map: MapSymbol)
```

while:

```text
TodaIteratedSuspensionMap
!= MapSymbol
```

Therefore Phase 46 does not add:

```text
Toda45IsomorphismStatement
→
IsomorphismStatement
```

and does not derive a generic injectivity consequence.

Important:

```text
Toda45IsomorphismStatement
=
instance-aware authoritative Toda theorem result
```

but there is currently no lossless type-compatible generic projection.

The existing generic map-property API is not generalized merely for Phase 46.

---

# Phase 46 representative probe

Run:

```powershell
python -m probes.probe_phase46_capabilities
```

Representative output:

```text
n ≥ k+2
m ≥ n

E^(m-n): π_{n+k}^{n} → π_{m+k}^{m}

E^(m-n): π_{n+k}^{n} → π_{m+k}^{m} is isomorphism
```

The representative run reports:

```text
theorem isomorphism count = 1
premise count = 3
derived round count = 1
fixed point = True
```

---

# Phase 46 scope boundaries

Implemented:

```text
ScalarGreaterEqualStatement
symbolic n ≥ k+2
symbolic m ≥ n
TodaIteratedSuspensionMap
symbolic exponent m-n
source π_{n+k}^n
target π_{m+k}^m
Toda45IsomorphismStatement
Toda (4.5) applicability guard
invalid-case rejection
cross-instance rejection
theorem provenance
one-round fixed-point representative integration
executable Phase 46 probe
full regression
```

Still not implemented:

```text
general symbolic inequality solver
automatic numeric inequality verification
general symbolic dimension solver
symbolic map typing solver
generic map-property type generalization
Toda45IsomorphismStatement → IsomorphismStatement bridge
generic InjectiveMapStatement consequence
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
ScalarGreaterEqualStatement
!= inequality solver
```

and:

```text
TodaIteratedSuspensionMap
!= isomorphism theorem
```

and:

```text
Toda45IsomorphismStatement
!= generic IsomorphismStatement
```

---


# Phase 47: Toda Proposition 4.4 decomposition isomorphism

Phase 47 represents and derives Toda Proposition 4.4 in the form:

```text
α ∈ π_{2n-1}^n
H(α)=±ι_{2n-1}
```

implies that the decomposition map

```text
Φ:
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
→
π_i^n

Φ(β,γ)=Eβ+α∘γ
```

is an isomorphism.

Phase 47 keeps the following layers distinct:

```text
Toda group membership
!=
decomposition source / target representation
!=
decomposition map representation
!=
Toda Proposition 4.4 theorem statement
!=
generic map-property statement
```

---

# TodaPrimaryGroup membership

Phase 47 introduces:

```text
TodaPrimaryGroupMembershipStatement
├── element: Expression
└── group: TodaPrimaryGroup
```

Representative:

```text
α ∈ π_{2n-1}^n
```

This remains distinct from:

```text
PrimaryComponentMembershipStatement
→ element ∈ π_i(S^n;p)
```

The statement is structural only. Its constructor does not validate element dimensions or prove membership.

---

# Proposition 4.4 decomposition source / target

`DirectSumGroup` now accepts:

```text
FreeCyclicGroup
PrimaryComponent
TodaPrimaryGroup
```

as structural summands.

This permits the Proposition 4.4 source:

```text
π_{i-1}^{n-1}
⊕
π_i^{2n-1}
```

to be represented losslessly, while the target remains:

```text
π_i^n
```

as a `TodaPrimaryGroup`.

Important:

```text
DirectSumGroup
!= AbelianGroup
```

and source representation alone does not assert any isomorphism theorem.

---

# Toda Proposition 4.4 decomposition map

Phase 47 introduces:

```text
TodaProp44DecompositionMap
├── source_group: DirectSumGroup
├── target_group: TodaPrimaryGroup
├── alpha: Expression
├── beta: Expression
├── gamma: Expression
└── formula: Expression
```

Representative:

```text
Φ:
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
→
π_i^n

Φ(β,γ)=Eβ+α∘γ
```

The formula uses existing expression structures:

```text
Suspension(β)
Composition(α,γ)
Sum(Eβ, α∘γ)
```

The map constructor stores structure only. It does not validate source / target typing, formula validity, or theorem applicability.

Important:

```text
TodaProp44DecompositionMap
!= MapSymbol

TodaProp44DecompositionMap
!= TodaIteratedSuspensionMap
```

---

# Toda Proposition 4.4 theorem statement

Phase 47 introduces:

```text
TodaProp44IsomorphismStatement(map)
```

where `map` is a specific `TodaProp44DecompositionMap`.

Meaning:

```text
the supplied decomposition map instance
is an isomorphism by Toda Proposition 4.4
```

Different symbolic `(i,n,α)` instances remain structurally distinct.

Important:

```text
TodaProp44IsomorphismStatement
!= Toda45IsomorphismStatement

TodaProp44IsomorphismStatement
!= IsomorphismStatement
```

---

# Toda Proposition 4.4 inference rule

The domain rule is:

```text
toda_prop44_isomorphism_inference_rule()
```

Premises:

```text
α ∈ π_{2n-1}^n

H(α)=+ι_{2n-1}
or
H(α)=-ι_{2n-1}

TodaProp44DecompositionMap(
  π_{i-1}^{n-1} ⊕ π_i^{2n-1}
  →
  π_i^n,
  Φ(β,γ)=Eβ+α∘γ
)
```

Conclusion:

```text
TodaProp44IsomorphismStatement(map)
```

The rule uses `match_guard` to verify one shared symbolic instance:

```text
membership degree = 2n-1
same α in membership / Hopf relation / map
Hopf map = H
Hopf value = ±ι_{2n-1}
target = π_i^n
first source summand = π_{i-1}^{n-1}
second source summand = π_i^{2n-1}
formula = Eβ+α∘γ
```

The generic inference engine is unchanged.

---

# Phase 47 applicability and provenance

Valid positive- and negative-Hopf instances each derive exactly one theorem result.

Invalid or mixed structures are rejected, including:

```text
missing membership premise
missing Hopf premise
missing decomposition map
wrong membership degree
different α instance
different n instance
wrong Hopf map
wrong Hopf value
wrong target sphere dimension
reversed source summands
wrong formula
cross-instance premise mixing
```

Every derived theorem step preserves:

```text
ProofStep.premises
ProofStep.inference_rule
ProofRule.INFERENCE
```

Representative inference reaches fixed point in one derived round:

```text
3 GIVEN premises
↓
1 TodaProp44IsomorphismStatement
↓
fixed point
```

---

# Generic isomorphism compatibility boundary after Phase 47

The existing generic map-property API remains:

```text
IsomorphismStatement(map: MapSymbol)
InjectiveMapStatement(map: MapSymbol)
```

while:

```text
TodaProp44DecompositionMap
!= MapSymbol
```

Therefore Phase 47 does not add:

```text
TodaProp44IsomorphismStatement
→ IsomorphismStatement
```

and does not derive:

```text
InjectiveMapStatement
```

from the Proposition 4.4 theorem.

The Proposition 4.4 consequence that suspension `E` is injective is also intentionally outside Phase 47.

Important:

```text
decomposition map isomorphism
!=
E injectivity consequence
```

---

# Phase 47 representative probe

Run:

```powershell
python -m probes.probe_phase47_capabilities
```

Representative output:

```text
α ∈ π_{2n-1}^{n}
H(α) = ι_(2n-1)

Φ: π_{i-1}^{n-1} ⊕ π_{i}^{2n-1} → π_{i}^{n}
Φ(β,γ) = Eβ + α∘γ

Φ: π_{i-1}^{n-1} ⊕ π_{i}^{2n-1} → π_{i}^{n} is isomorphism
```

The representative run reports:

```text
theorem isomorphism count = 1
premise count = 3
derived round count = 1
fixed point = True
```

---

# Phase 47 scope boundaries

Implemented:

```text
TodaPrimaryGroupMembershipStatement
DirectSumGroup TodaPrimaryGroup summands
symbolic Proposition 4.4 source / target
TodaProp44DecompositionMap
structural formula Eβ+α∘γ
positive Hopf applicability
negative Hopf applicability
TodaProp44IsomorphismStatement
Toda Proposition 4.4 theorem rule
cross-instance rejection
invalid-case rejection
theorem provenance
one-round fixed-point integration
representative executable probe
full regression
```

Still not implemented:

```text
general symbolic dimension solver
symbolic map typing solver
generic map-property type generalization
Toda45IsomorphismStatement → IsomorphismStatement bridge
TodaProp44IsomorphismStatement → IsomorphismStatement bridge
generic injectivity consequence for Toda-specific maps
Toda Proposition 4.4 consequence: E injective
stable homotopy group model
general Whitehead-product algebra
automatic Whitehead-product zero / nonzero solver
general existential witness machinery
higher Toda brackets
```

Important:

```text
TodaPrimaryGroupMembershipStatement
!= membership solver
```

```text
TodaProp44DecompositionMap
!= isomorphism theorem
```

```text
TodaProp44IsomorphismStatement
!= generic IsomorphismStatement
```

---

# Phase 45 historical scope boundaries

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

Focused Phase 47:

```powershell
python -m pytest tests/test_phase47_toda_prop44_compatibility.py -q
python -m pytest tests/test_phase47_toda_prop44_decomposition_groups.py -q
python -m pytest tests/test_phase47_toda_prop44_decomposition_map.py -q
python -m pytest tests/test_phase47_toda_prop44_toda_membership.py -q
python -m pytest tests/test_phase47_toda_prop44_theorem_semantics.py -q
python -m pytest tests/test_phase47_toda_prop44_applicability_compatibility.py -q
python -m pytest tests/test_phase47_toda_prop44_probe.py -q
```

Verified:

```text
20 passed
17 passed
27 passed
15 passed
22 passed
21 passed
12 passed
```

Related regressions:

```powershell
python -m pytest tests/test_toda_rules.py -q
python -m pytest tests/test_map_property_rules.py -q
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
2277 passed in 55.61s
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

Phase 47 is complete.

The Toda Chapter 4 branch now contains:

```text
Toda Lemma 4.1 case semantics
Toda Proposition 4.2 instance-aware EHP exactness
Toda (4.5) stable-range E^(m-n) instance-aware isomorphism
Toda Proposition 4.4 instance-aware decomposition isomorphism
```

The next planned branch is:

```text
Phase 48 candidate
Toda Proposition 4.4 consequence
E injective
```

Phase 48 should derive the injectivity of the suspension map `E` as a consequence of the Proposition 4.4 decomposition isomorphism, without conflating the full decomposition map with `E`.

The compatibility check should determine the minimum instance-aware representation needed for this consequence and whether any existing generic injectivity machinery can be reused without generalizing unrelated APIs.

Important:

```text
TodaProp44IsomorphismStatement
!= generic IsomorphismStatement

decomposition-map injectivity
!= E injectivity
```
