# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The project separates mathematical theorem knowledge, explicit facts, the generic inference engine, and algebraic calculation.

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
!= typing
!= theorem knowledge
```

```text
structural equality
!= mathematical equality
```

---

# Current status

Completed through Phase 56.

```text
Phase 1–27   generic proof / algebra / Toda-bracket foundation
Phase 28–38  actual H / Prop.2.2 / Prop.3.1 equality branch
Phase 39     PrimaryComponent minimum representation
Phase 40     TodaPrimaryGroup minimum representation
Phase 41     PreimageSubgroup minimum representation
Phase 42     WhiteheadProduct minimum representation
Phase 43     Toda Lemma 4.1 premise representation
Phase 44     Toda Lemma 4.1 case semantics
Phase 45     Toda Proposition 4.2 2-primary EHP exactness
Phase 46     Toda (4.5) stable-range iterated-suspension isomorphism
Phase 47     Toda Proposition 4.4 decomposition isomorphism
Phase 48     Toda Proposition 4.4 suspension injectivity consequence
Phase 49     π_3^2 = Z{η₂}
Phase 50     π_4^3 = Z/2{η₃}
Phase 51     Toda Proposition 5.1 proof dependency analysis
Phase 52     Δ(ι₅)=±2η₂ direct bridge
Phase 53     Toda (4.5) finite-cyclic transport
Phase 54     higher η-family bridge
Phase 55     Toda Proposition 5.1 finite-dimensional integration / provenance
Phase 56     Toda (5.2) composition isomorphism
```

Current full regression:

```text
2910 passed in 29.17s
```

Representative current probe:

```powershell
python -m probes.probe_phase56_capabilities
```

---

# Core architecture

```text
literature-backed theorem / explicit facts
↓
domain-specific inference rules
↓
generic ProofStep / InferenceRule machinery
↓
expression / statement structures
↓
homotopy / EHP data
↓
abelian-group algebra
```

The generic inference engine remains theorem-agnostic.

---

# Core structural layer

Homotopy-group and group structures include:

```text
PrimaryComponent(i,n,p)          → π_i(S^n;p)
TodaPrimaryGroup(i,n)            → π_i^n
PreimageSubgroup(f,A)            → f^-1(A)
FreeCyclicGroup(generator)       → Z{generator}
FiniteCyclicGroup(order,generator)
DirectSumGroup(summands)
```

Canonical symbolic maps:

```text
EHP_E_MAP     → E
EHP_H_MAP     → H
EHP_DELTA_MAP → Δ
```

Instance-aware maps include:

```text
TodaSuspensionMap
TodaHopfInvariantMap
TodaDeltaMap
TodaIteratedSuspensionMap
```

Expression structures used by the current Toda branch include:

```text
HomotopyElement
Multiple
Sum
Composition
MapApplication
Suspension
IteratedSuspension
SmashProduct
WhiteheadProduct
TodaBracket
```

Constructors do not perform theorem-aware normalization.

---

# Toda Proposition 4.2 exactness

The current instance-aware EHP exactness layer uses:

```text
TodaEHPSequence
TodaEHPExactnessWindow
TodaProp42ExactnessStatement
```

with the three domain rules:

```text
toda_prop42_e_h_exactness_inference_rule()
toda_prop42_h_delta_exactness_inference_rule()
toda_prop42_delta_e_exactness_inference_rule()
```

The generic inference engine does not contain Toda-specific exactness logic.

---

# Toda Proposition 4.4

Phase 47 represents the decomposition

```text
Φ:
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
→
π_i^n

Φ(β,γ)=Eβ+α∘γ
```

and derives an instance-aware isomorphism when the Proposition 4.4 hypotheses match.

Phase 48 extracts the first-summand restriction and derives the corresponding suspension injectivity consequence.

Phase 56 reuses the same decomposition structure for the concrete specialization `n=2`, `α=η₂`.

---

# Phase 49: `π_3^2 = Z{η₂}`

The EHP fragment is:

```text
π_2^1 -E→ π_3^2 -H→ π_3^3 -Δ→ π_1^1 -E→ π_2^2
```

Low-dimensional inputs include:

```text
π_2^1 = 0
π_3^3 = Z{ι_3}
E: π_1^1 → π_2^2 is an isomorphism
```

The engine derives:

```text
H injective
Δ=0
H surjective
H isomorphism
```

Then `η₂` is defined as the unique Hopf preimage of `ι_3`:

```text
H isomorphism
+
π_3^3=Z{ι_3}
↓
η₂ = unique H-preimage of ι_3
↓
H(η₂)=ι_3
↓
π_3^2=Z{η₂}
```

`η₂` is therefore theorem-derived rather than a final GIVEN result.

---

# Phase 50: `π_4^3 = Z/2{η₃}`

The current branch uses:

```text
H([ι_2,ι_2])=±2ι_3
↓
[ι_2,ι_2]=±2η₂
```

and:

```text
Δ(ι_5)=±[ι_2,ι_2]
↓
Δ(ι_5)=±2η₂
```

Together with EHP exactness:

```text
π_5^5 -Δ→ π_3^2 -E→ π_4^3
π_3^2 -E→ π_4^3 -H→ π_4^5
```

the implementation derives:

```text
Im(Δ)=Z{2η₂}
Ker(E)=Z{2η₂}
E: π_3^2→π_4^3 surjective
```

and hence:

```text
π_4^3=Z/2{Eη₂}
```

The η-family notation then gives:

```text
η₃=Eη₂
↓
π_4^3=Z/2{η₃}
```

No general quotient simplifier, sign solver, or suspension normalizer is introduced.

---

# Higher η-family and Toda Proposition 5.1

The η-family structural definition is:

```text
η_n=E^(n-2)η₂
```

The Phase 54 η-family-specific bridge derives:

```text
η₃=Eη₂
+
η_n=E^(n-2)η₂
↓
E^(n-3)η₃=η_n
```

Toda (4.5) finite-cyclic transport gives:

```text
π_4^3=Z/2{η₃}
+
E^(n-3): π_4^3 ≅ π_{n+1}^n
↓
π_{n+1}^n=Z/2{E^(n-3)η₃}
```

Combining the two yields:

```text
π_{n+1}^n=Z/2{η_n}
```

Phase 55 integrates the four independently derived finite-dimensional Proposition 5.1 results:

```text
π_3^2=Z{η₂}
H(η₂)=ι₃
Δ(ι₅)=±2η₂
π_{n+1}^n=Z/2{η_n}
↓
Toda Proposition 5.1 finite-dimensional result
```

The final Proposition 5.1 result is derived from four `ProofRule.INFERENCE` premises and is not reintroduced as a GIVEN premise.

The stable conclusion

```text
(G_1;2)=Z/2{η}
```

remains deferred.

---

# Phase 56: Toda (5.2) composition isomorphism

Phase 56 implements:

```text
η₂∘- :
π_i^3
≅
π_i^2
    (i≥3)
```

equivalently:

```text
α ↦ η₂∘α : π_i^3 ≅ π_i^2
```

## Phase 56-1: compatibility check

The existing representation is sufficient for:

```text
π_{i-1}^1 ⊕ π_i^3 → π_i^2
Eβ + η₂∘γ
π_{i-1}^1=0
```

using:

```text
TodaProp44DecompositionMap
Composition
TodaPrimaryGroupZeroStatement
```

The existing generic Proposition 4.4 rule does not directly match the concrete `n=2` data because structural `2*2-1` is not automatically normalized to `3`.

No generic scalar normalization was added.

## Phase 56-2: zero first summand

Specific rule:

```text
i≥3
↓
π_{i-1}^1=0
```

using the existing:

```text
ScalarGreaterEqualStatement
TodaPrimaryGroupZeroStatement
```

The rule remains intentionally narrow.

## Phase 56-3: Proposition 4.4 specialization

A dedicated specialization rule connects independently derived Phase 49 results:

```text
η₂ definition            INFERENCE
H(η₂)=ι₃                 INFERENCE
+
Φ(β,γ)=Eβ+η₂∘γ
↓
Φ:
π_{i-1}^1 ⊕ π_i^3
≅
π_i^2
```

The generic Proposition 4.4 rule remains unchanged.

## Phase 56-4: second-summand restriction

Minimum dedicated statement:

```text
TodaProp44SecondSummandRestrictionStatement
```

and rule:

```text
Φ:
π_{i-1}^1 ⊕ π_i^3 ≅ π_i^2
↓
Φ|_{π_i^3}(γ)=η₂∘γ
```

No generic composition-map framework was added.

## Phase 56-5: Toda (5.2)

Minimum final statement:

```text
Toda52CompositionIsomorphismStatement
```

The final rule requires exactly three derived premises:

```text
π_{i-1}^1=0                    INFERENCE
Prop.4.4 n=2 specialization    INFERENCE
second-summand restriction     INFERENCE
↓
η₂∘- : π_i^3 ≅ π_i^2          INFERENCE
```

No generic direct-sum reduction or generic isomorphism restriction theorem was added.

## Phase 56-6: representative fixed point

Representative input:

```text
Phase 49 base premises × 6
i≥3
Prop.4.4 decomposition map
```

Therefore:

```text
given premise count = 8
```

The same fixed-point run derives:

```text
η₂ definition
H(η₂)=ι₃
π_{i-1}^1=0
Prop.4.4 n=2 specialization
second-summand restriction
Toda (5.2)
```

Representative provenance:

```text
pi_(i-1)^1=0 is derived = True
Prop.4.4 n=2 specialization is derived = True
second-summand restriction is derived = True
Toda (5.2) result is derived = True

final rule = Toda 5.2 eta_2 composition isomorphism
final premise count = 3
final premises are derived = True

pi_(i-1)^1=0 is GIVEN premise = False
Prop.4.4 specialization is GIVEN premise = False
second-summand restriction is GIVEN premise = False
Toda (5.2) result is GIVEN premise = False

given premise count = 8
derived step count = 12
derived round count = 9
fixed point = True
```

Representative probe:

```powershell
python -m probes.probe_phase56_capabilities
```

---

# Phase 56 tests

Focused Phase 56 suites:

```text
tests/test_phase56_prop44_composition_compatibility.py        6 passed
tests/test_phase56_pi_i_minus_1_1_zero.py                    10 passed
tests/test_phase56_prop44_eta2_specialization.py             11 passed
tests/test_phase56_prop44_second_summand_restriction.py      13 passed
tests/test_phase56_toda52_composition_isomorphism.py         16 passed
tests/test_phase56_probe.py                                  10 passed
```

Related regression suites remained green, including Phase 47, Phase 48, and Phase 49 probe tests.

Full regression:

```text
2910 passed in 29.17s
```

---

# Phase 56 completion boundary

Implemented:

```text
current Prop.4.4 / Composition / zero-group compatibility check
π_{i-1}^1=0 for i≥3 narrow theorem semantics
Prop.4.4 n=2, α=η₂ specialization
second-summand restriction γ ↦ η₂∘γ
Toda52CompositionIsomorphismStatement
zero first summand → Toda (5.2)
derived provenance
same-run representative integration
representative probe
full regression
```

Not implemented:

```text
generic scalar normalization
generic direct-sum simplification
generic composition-map framework
generic isomorphism-restriction framework
Toda Lemma 5.2
stable (G_1;2)=Z/2{η}
stable homotopy-group model
generic Toda-bracket normalization
```

The generic inference engine is unchanged.

---

# Documentation

- `README.md` — current capabilities and status
- `docs/design.md` — current architecture, semantics, and boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capability dependency

Historical limitations in the development log describe the state at that time. Current behavior is defined by the latest README and design documents.

---

# Next development boundary

Phase 56 is complete.

The next concrete phase is:

```text
Phase 57
Toda Lemma 5.2 proof integration
```

Current proof target:

```text
α∈π_i(S^3)
2α=0
β∈{η₃,2ι₄,Eα}_1
```

with target conclusions:

```text
H(β)=E²α
2β=η₃∘Eα∘η_{i+1}
β∈π_{i+2}^3
Δ(E²α)=0
```

The source material contains an index inconsistency between the displayed Lemma 5.2 statement and the proof ending for the final η-index. Phase 57-1 must verify the original statement, proof indices, and typing before implementation.

Dependencies currently identified for the proof are:

```text
Lemma 4.5
Proposition 2.6
Proposition 1.4
Proposition 1.3
Corollary 3.7
(2.1)
```

Only the minimum consequences required by the actual Lemma 5.2 proof should be implemented.
