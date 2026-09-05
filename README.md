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
!= typing
!= theorem knowledge
```

```text
structural equality
!= mathematical equality
```

---

# Current status

Completed through Phase 49.

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
Phase 49  concrete EHP calculation π_3^2 = Z{η_2}
```

Current full regression:

```text
2557 passed in 56.45s
```

Representative Phase 49 probe:

```powershell
python -m probes.probe_phase49_capabilities
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

# Toda Chapter 4 structural layer

Structural group terms:

```text
PrimaryComponent(i,n,p) → π_i(S^n;p)
TodaPrimaryGroup(i,n) → π_i^n
PreimageSubgroup(f,A) → f^-1(A)
FreeCyclicGroup(generator) → Z{generator}
DirectSumGroup(summands) → structural direct sum
```

Canonical symbolic EHP maps:

```text
EHP_E_MAP     → E
EHP_H_MAP     → H
EHP_DELTA_MAP → Δ
```

Instance-aware Toda maps:

```text
TodaSuspensionMap(source_group,target_group)
TodaHopfInvariantMap(source_group,target_group)
TodaDeltaMap(source_group,target_group)
```

Important:

```text
TodaSuspensionMap != EHP_E_MAP
TodaHopfInvariantMap != EHP_H_MAP
TodaDeltaMap != EHP_DELTA_MAP
```

---

# Toda Proposition 4.2 exactness

Structural representations:

```text
TodaEHPSequence
TodaEHPExactnessWindow
```

Instance-aware exactness theorem:

```text
TodaProp42ExactnessStatement(window)
```

Rules:

```text
toda_prop42_e_h_exactness_inference_rule()
toda_prop42_h_delta_exactness_inference_rule()
toda_prop42_delta_e_exactness_inference_rule()
```

The generic bridge:

```text
toda_prop42_exactness_to_generic_inference_rule()
```

is intentionally instance-lossy.

Therefore `TodaProp42ExactnessStatement` remains the authoritative theorem result for a specific Toda EHP window.

---

# Toda (4.5)

Phase 46 represents the stable-range isomorphism:

```text
E^(m-n):
π_{n+k}^n → π_{m+k}^m
```

under:

```text
n ≥ k+2
m ≥ n
```

as an instance-aware theorem statement.

---

# Toda Proposition 4.4

Phase 47 represents:

```text
Φ:
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
→ π_i^n

Φ(β,γ)=Eβ+α∘γ
```

under:

```text
α ∈ π_{2n-1}^n
H(α)=±ι_{2n-1}
```

and derives `TodaProp44IsomorphismStatement`.

Phase 48 adds:

```text
TodaProp44FirstSummandRestrictionStatement
```

meaning:

```text
Φ|_{π_{i-1}^{n-1}}
=
E: π_{i-1}^{n-1} → π_i^n
```

then derives:

```text
TodaProp44SuspensionInjectiveStatement
```

Important:

```text
TodaProp44SuspensionInjectiveStatement
!= InjectiveMapStatement(EHP_E_MAP)
```

---

# Phase 49: concrete `π_3^2 = Z{η_2}` calculation

Target EHP fragment:

```text
π_2^1
-E→ π_3^2
-H→ π_3^3
-Δ→ π_1^1
-E→ π_2^2
```

Low-dimensional facts:

```text
π_2^1 = 0
π_3^3 = Z{ι_3}
E: π_1^1 → π_2^2 is isomorphism
```

Phase 49-specific statements include:

```text
TodaPrimaryGroupZeroStatement
TodaSuspensionIsomorphismStatement
TodaSuspensionInjectiveStatement
TodaHopfInvariantInjectiveStatement
TodaDeltaZeroStatement
TodaHopfInvariantSurjectiveStatement
TodaHopfInvariantIsomorphismStatement
TodaPi32Eta2DefinitionStatement
```

---

# Phase 49 proof

First:

```text
π_2^1 = 0
+
π_2^1 -E→ π_3^2 -H→ π_3^3 exact
↓
H: π_3^2 → π_3^3 is injective
```

Rule:

```text
toda_exactness_zero_left_implies_hopf_injective_inference_rule()
```

Next:

```text
E: π_1^1 → π_2^2 is isomorphism
↓
E: π_1^1 → π_2^2 is injective
```

Rule:

```text
toda_suspension_isomorphism_implies_injective_inference_rule()
```

Then:

```text
E injective
+
π_3^3 -Δ→ π_1^1 -E→ π_2^2 exact
↓
Δ: π_3^3 → π_1^1 = 0
```

Rule:

```text
toda_exactness_injective_right_implies_delta_zero_inference_rule()
```

Then:

```text
π_3^2 -H→ π_3^3 -Δ→ π_1^1 exact
+
Δ=0
↓
H: π_3^2 → π_3^3 is surjective
```

Rule:

```text
toda_exactness_zero_delta_implies_hopf_surjective_inference_rule()
```

Then:

```text
H injective
+
H surjective
↓
H: π_3^2 → π_3^3 is isomorphism
```

Rule:

```text
toda_hopf_injective_surjective_implies_isomorphism_inference_rule()
```

---

# Definition of `η_2`

The central semantic point is:

```text
η_2
!=
an initially GIVEN element
```

Instead:

```text
H: π_3^2 → π_3^3 is isomorphism
+
π_3^3 = Z{ι_3}
↓
ι_3 has a unique preimage under H
↓
denote that unique preimage by η_2
```

This is represented by:

```text
TodaPi32Eta2DefinitionStatement
```

and derived by:

```text
toda_pi3_2_define_eta2_inference_rule()
```

The isomorphism supplies existence and uniqueness:

```text
surjective → existence
injective → uniqueness
```

No general existential, witness, uniqueness, or inverse-map framework is introduced.

From the definition:

```text
H(η_2)=ι_3
```

is derived by:

```text
toda_pi3_2_eta2_hopf_relation_inference_rule()
```

Finally:

```text
H isomorphism
+
π_3^3 = Z{ι_3}
+
η_2 is the unique H-preimage of ι_3
↓
π_3^2 = Z{η_2}
```

by:

```text
toda_pi3_2_free_cyclic_generator_inference_rule()
```

This is a concrete generator transport rule for the actual `π_3^2` calculation, not a general cyclic-generator transport framework.

---

# Phase 49 end-to-end inference

Initial GIVEN premises:

```text
π_2^1 = 0
π_3^3 = Z{ι_3}
E: π_1^1 → π_2^2 is isomorphism

π_2^1 -E→ π_3^2 -H→ π_3^3 exact
π_3^2 -H→ π_3^3 -Δ→ π_1^1 exact
π_3^3 -Δ→ π_1^1 -E→ π_2^2 exact
```

Fixed-point result:

```text
round 1
H: π_3^2 → π_3^3 is injective
E: π_1^1 → π_2^2 is injective

round 2
Δ: π_3^3 → π_1^1 = 0

round 3
H: π_3^2 → π_3^3 is surjective

round 4
H: π_3^2 → π_3^3 is isomorphism

round 5
ι_3 has a unique preimage under H;
denote it by η_2

round 6
H(η_2)=ι_3
π_3^2 = Z{η_2}

fixed point
```

Counts:

```text
given premise count = 6
derived step count = 8
derived round count = 6
fixed point = True
```

---

# Phase 49 tests

Focused:

```text
tests/test_phase49_concrete_pi3_2_compatibility.py  20 passed
tests/test_phase49_low_dimensional_facts.py         19 passed
tests/test_phase49_hopf_injectivity.py              21 passed
tests/test_phase49_delta_hopf_surjectivity.py       26 passed
tests/test_phase49_hopf_isomorphism.py              17 passed
tests/test_phase49_generator_transport.py           20 passed
tests/test_phase49_probe.py                         23 passed
```

Related:

```text
tests/test_phase45_toda_prop42_theorem_semantics.py
16 passed
```

Full regression:

```text
2557 passed in 56.45s
```

---

# Phase 49 completion boundary

Implemented:

```text
low-dimensional facts required by π_3^2
instance-aware E/H/Δ map semantics needed by the calculation
H injective
E injective
Δ=0
H surjective
H isomorphism
η_2 theorem-derived naming as the unique H-preimage of ι_3
H(η_2)=ι_3
π_3^2=Z{η_2}
cross-instance rejection
provenance
six-round fixed-point integration
representative probe
full regression
```

Still outside Phase 49:

```text
general existential quantification
general witness / uniqueness framework
general inverse-map machinery
general cyclic-generator transport
generic map-property type generalization
general symbolic dimension solver
symbolic map typing solver
Toda Proposition 2.7
concrete π_4^3 calculation
stable homotopy group model
higher Toda brackets
```

---

# Documentation

- `README.md` — current capabilities and status
- `docs/design.md` — current architecture, semantics, and boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capability dependency

Historical limitations in the development log describe the state at that time.

Current behavior is defined by the latest README and design documents.

---

# Next development boundary

Phase 49 is complete.

Next:

```text
Phase 50
concrete π_4^3 calculation
```

Start with:

```text
Phase 50-1
π_4^3 proof dependency compatibility check
```

Known expected dependency:

```text
Toda Proposition 2.7
```

The rule remains:

```text
actual π_4^3 proof dependency
↓
minimum Toda Prop.2.7 semantics
```

not:

```text
full Prop.2.7 theorem catalogue first
```
