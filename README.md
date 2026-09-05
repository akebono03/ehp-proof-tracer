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

Completed through Phase 48.

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
Phase 48  Toda Proposition 4.4 suspension E injectivity consequence
```

Current full regression:

```text
2411 passed in 58.16s
```

Focused Phase 48 suites:

```text
tests/test_phase48_toda_prop44_e_injectivity_compatibility.py
21 passed

tests/test_phase48_toda_prop44_e_map.py
22 passed

tests/test_phase48_toda_prop44_first_summand_restriction.py
22 passed

tests/test_phase48_toda_prop44_e_injective_theorem.py
26 passed

tests/test_phase48_toda_prop44_e_injective_applicability.py
22 passed

tests/test_phase48_toda_prop44_probe.py
21 passed
```

Representative Phase 48 probe:

```powershell
python -m probes.probe_phase48_capabilities
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

TodaSuspensionMap(source_group,target_group)
→ instance-aware single suspension E map between TodaPrimaryGroup terms

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

# Phase 48: Toda Proposition 4.4 suspension E injectivity consequence

Phase 48 derives the Proposition 4.4 consequence that the suspension map

```text
E:
π_{i-1}^{n-1}
→
π_i^n
```

is injective, while preserving the symbolic `(i,n)` source / target instance.

Phase 48 keeps four layers distinct:

```text
generic E map symbol
!=
instance-aware Toda suspension map
!=
first-summand restriction semantics
!=
instance-aware injectivity theorem
```

## Instance-aware suspension map

Phase 48 introduces:

```text
TodaSuspensionMap
├── source_group: TodaPrimaryGroup
└── target_group: TodaPrimaryGroup
```

Representative:

```text
E:
π_{i-1}^{n-1}
→
π_i^n
```

Important:

```text
TodaSuspensionMap
!= MapSymbol
!= EHP_E_MAP
!= Suspension
!= TodaIteratedSuspensionMap
!= TodaProp44DecompositionMap
```

The constructor stores the source / target structure only. It does not validate symbolic dimensions and does not assert injectivity.

## Proposition 4.4 first-summand restriction

Phase 48 introduces:

```text
TodaProp44FirstSummandRestrictionStatement
├── decomposition_map: TodaProp44DecompositionMap
└── suspension_map: TodaSuspensionMap
```

Meaning:

```text
Φ|_{π_{i-1}^{n-1}}
=
E: π_{i-1}^{n-1} → π_i^n
```

The rule:

```text
toda_prop44_first_summand_restriction_inference_rule()
```

checks that:

```text
suspension source = first direct-sum summand
suspension target = decomposition target
formula = Eβ + α∘γ
```

No general direct-sum inclusion or projection machinery is introduced.

## Proposition 4.4 suspension injectivity theorem

Phase 48 introduces:

```text
TodaProp44SuspensionInjectiveStatement
└── map: TodaSuspensionMap
```

Meaning:

```text
E: π_{i-1}^{n-1} → π_i^n
is injective
```

The domain rule is:

```text
toda_prop44_suspension_injective_inference_rule()
```

Premises:

```text
TodaProp44IsomorphismStatement(Φ)

TodaProp44FirstSummandRestrictionStatement(Φ,E)
```

Conclusion:

```text
TodaProp44SuspensionInjectiveStatement(E)
```

The rule requires the same decomposition-map instance and checks that the suspension source is the first summand and the suspension target is the decomposition target.

## Phase 48 end-to-end inference

Representative initial premises:

```text
α ∈ π_{2n-1}^n
H(α)=ι_{2n-1}
TodaProp44DecompositionMap
TodaSuspensionMap
```

Fixed-point inference:

```text
round 1
TodaProp44IsomorphismStatement
TodaProp44FirstSummandRestrictionStatement

round 2
TodaProp44SuspensionInjectiveStatement

fixed point
```

Representative result:

```text
Φ:
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
→
π_i^n
is isomorphism

Φ|_{π_{i-1}^{n-1}}
=
E: π_{i-1}^{n-1} → π_i^n

E: π_{i-1}^{n-1} → π_i^n
is injective
```

## Generic map-property boundary after Phase 48

The generic API remains:

```text
IsomorphismStatement(map: MapSymbol)
InjectiveMapStatement(map: MapSymbol)
```

while:

```text
TodaSuspensionMap
!= MapSymbol
```

Therefore Phase 48 intentionally does not derive:

```text
InjectiveMapStatement(EHP_E_MAP)
```

from the instance-aware theorem.

Important:

```text
TodaProp44SuspensionInjectiveStatement
!= InjectiveMapStatement
```

and the instance-aware theorem remains authoritative for the specific source / target pair.

## Phase 48 representative probe

Run:

```powershell
python -m probes.probe_phase48_capabilities
```

Representative report:

```text
given premise count = 4
isomorphism count = 1
restriction count = 1
injectivity count = 1
derived round count = 2
round 1 new step count = 2
round 2 new step count = 1
fixed point = True
```

## Phase 48 scope boundaries

Implemented:

```text
TodaSuspensionMap
instance-aware E source / target
TodaProp44FirstSummandRestrictionStatement
Toda Proposition 4.4 first-summand restriction rule
TodaProp44SuspensionInjectiveStatement
Toda Proposition 4.4 E injectivity theorem rule
cross-instance rejection
invalid-source / invalid-target rejection
provenance
two-round fixed-point integration
representative executable probe
full regression
```

Still not implemented:

```text
generic InjectiveMapStatement bridge
generic map-property type generalization
general direct-sum inclusion machinery
automatic equality reflection through TodaSuspensionMap
general symbolic dimension solver
symbolic map typing solver
stable homotopy group model
general existential witness machinery
higher Toda brackets
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

Focused Phase 48:

```powershell
python -m pytest tests/test_phase48_toda_prop44_e_injectivity_compatibility.py -q
python -m pytest tests/test_phase48_toda_prop44_e_map.py -q
python -m pytest tests/test_phase48_toda_prop44_first_summand_restriction.py -q
python -m pytest tests/test_phase48_toda_prop44_e_injective_theorem.py -q
python -m pytest tests/test_phase48_toda_prop44_e_injective_applicability.py -q
python -m pytest tests/test_phase48_toda_prop44_probe.py -q
```

Verified:

```text
21 passed
22 passed
22 passed
26 passed
22 passed
21 passed
```

Related regressions:

```powershell
python -m pytest tests/test_phase47_toda_prop44_theorem_semantics.py -q
python -m pytest tests/test_phase47_toda_prop44_applicability_compatibility.py -q
python -m pytest tests/test_map_property_rules.py -q
python -m pytest tests/test_inference_rule_pattern.py -q
```

Verified:

```text
22 passed
21 passed
26 passed
438 passed
```

Full suite:

```powershell
python -m pytest -q
```

Verified:

```text
2411 passed in 58.16s
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

Phase 48 is complete.

The Toda Chapter 4 branch now contains:

```text
Toda Lemma 4.1 case semantics
Toda Proposition 4.2 instance-aware EHP exactness
Toda (4.5) stable-range E^(m-n) instance-aware isomorphism
Toda Proposition 4.4 instance-aware decomposition isomorphism
Toda Proposition 4.4 instance-aware suspension E injectivity consequence
```

The next candidate is a concrete low-dimensional calculation:

```text
Phase 49 candidate
π_3^2 = Z{η_2}
```

The planned mathematical route is:

```text
π_2^1 -E→ π_3^2 -H→ π_3^3 -Δ→ π_1^1 -E→ π_2^2
```

using low-dimensional facts and exactness to derive that `H: π_3^2 → π_3^3` is an isomorphism, then transport the generator `ι_3` back to a unique `η_2`.

Phase 49 should begin with a compatibility check and add only the minimum missing facts / theorem semantics required by this concrete calculation.

Important:

```text
concrete generator transport needed by π_3^2
!= general existential witness engine
```
