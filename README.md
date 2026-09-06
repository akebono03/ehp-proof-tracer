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

Completed through Phase 50.

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
Phase 49  concrete EHP calculation π_3^2 = Z{η₂}
Phase 50  concrete EHP calculation π_4^3 = Z/2{η₃}
```

Current full regression:

```text
2703 passed in 65.69s
```

Representative Phase 50 probe:

```powershell
python -m probes.probe_phase50_capabilities
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

```text
PrimaryComponent(i,n,p) → π_i(S^n;p)
TodaPrimaryGroup(i,n) → π_i^n
PreimageSubgroup(f,A) → f^-1(A)
FreeCyclicGroup(generator) → Z{generator}
FiniteCyclicGroup(order,generator) → Z/order{generator}
DirectSumGroup(summands) → structural direct sum
```

Canonical symbolic maps:

```text
EHP_E_MAP     → E
EHP_H_MAP     → H
EHP_DELTA_MAP → Δ
```

Instance-aware maps:

```text
TodaSuspensionMap(source_group,target_group)
TodaHopfInvariantMap(source_group,target_group)
TodaDeltaMap(source_group,target_group)
```

---

# Toda Proposition 4.2 exactness

```text
TodaEHPSequence
TodaEHPExactnessWindow
TodaProp42ExactnessStatement(window)
```

Rules:

```text
toda_prop42_e_h_exactness_inference_rule()
toda_prop42_h_delta_exactness_inference_rule()
toda_prop42_delta_e_exactness_inference_rule()
```

`TodaProp42ExactnessStatement` remains the authoritative instance-aware result.

---

# Phase 49: `π_3^2 = Z{η₂}`

EHP fragment:

```text
π_2^1 -E→ π_3^2 -H→ π_3^3 -Δ→ π_1^1 -E→ π_2^2
```

Low-dimensional facts:

```text
π_2^1 = 0
π_3^3 = Z{ι_3}
E: π_1^1 → π_2^2 is isomorphism
```

Derived:

```text
H injective
Δ=0
H surjective
H isomorphism
```

`η₂` is theorem-derived, not GIVEN:

```text
H isomorphism
+
π_3^3=Z{ι_3}
↓
ι_3 has a unique preimage
↓
denote it by η₂
↓
H(η₂)=ι_3
↓
π_3^2=Z{η₂}
```

---

# Phase 50: `π_4^3 = Z/2{η₃}`

Required EHP windows:

```text
π_5^5 -Δ→ π_3^2 -E→ π_4^3 exact
π_3^2 -E→ π_4^3 -H→ π_4^5 exact
```

Additional low-dimensional facts:

```text
π_5^5 = Z{ι_5}
π_4^5 = 0
```

Minimum Toda Proposition 2.7 consequence:

```text
H([ι_2,ι_2]) = ±2ι_3
```

Using Phase 49:

```text
H(η₂)=ι_3
H injective
↓
[ι_2,ι_2]=±2η₂
```

Specific Δ relation:

```text
Δ(ι_5)=±[ι_2,ι_2]
```

Therefore:

```text
π_5^5=Z{ι_5}
+
Δ(ι_5)=±[ι_2,ι_2]
+
[ι_2,ι_2]=±2η₂
↓
Im(Δ)=Z{2η₂}
```

Exactness gives:

```text
Im(Δ)=Z{2η₂}
+
Δ-E exact
↓
Ker(E)=Z{2η₂}
```

and:

```text
π_4^5=0
+
E-H exact
↓
E: π_3^2 → π_4^3 is surjective
```

Then:

```text
π_3^2=Z{η₂}
+
Ker(E)=Z{2η₂}
+
E surjective
↓
π_4^3=Z/2{Eη₂}
```

---

# η-family notation

Definition:

```text
η_n=E^(n-2)η₂
```

For `n=3`:

```text
η₃=Eη₂
```

So:

```text
π_4^3=Z/2{Eη₂}
+
η₃=Eη₂
↓
π_4^3=Z/2{η₃}
```

`IteratedSuspension(η₂,1)` and `Suspension(η₂)` remain structurally distinct; no generic normalization is added.

---

# Phase 50 representative fixed point

```text
round 1
H([ι_2,ι_2]) = ±2ι_3
Δ(ι_5) = ±[ι_2,ι_2]
E: π_3^2 → π_4^3 is surjective
η₃ = Eη₂

round 2
[ι_2,ι_2] = ±2η₂

round 3
Im(Δ) = Z{2η₂}

round 4
Ker(E) = Z{2η₂}

round 5
π_4^3 = Z/2{Eη₂}

round 6
π_4^3 = Z/2{η₃}

fixed point
```

Counts:

```text
given premise count = 11
derived step count = 9
derived round count = 6
fixed point = True
```

---

# Phase 50 tests

```text
tests/test_phase50_prop27_theorem_semantics.py       18 passed
tests/test_phase50_pi3_2_whitehead_square.py        14 passed
tests/test_phase50_low_dimensional_delta_facts.py    22 passed
tests/test_phase50_pi4_3_exactness_bridge.py         18 passed
tests/test_phase50_pi4_3_finite_cyclic.py            17 passed
tests/test_phase50_eta_family_notation.py            16 passed
tests/test_phase50_applicability_provenance.py       14 passed
tests/test_phase50_probe.py                          27 passed
```

Full regression:

```text
2703 passed in 65.69s
```

---

# Phase 50 completion boundary

Implemented:

```text
minimum Toda Proposition 2.7 consequence
up-to-sign theorem-specific semantics
π_5^5=Z{ι_5}
π_4^5=0
[ι_2,ι_2]=±2η₂
Δ(ι_5)=±[ι_2,ι_2]
Im(Δ)=Z{2η₂}
Ker(E)=Z{2η₂}
E: π_3^2 → π_4^3 surjective
FiniteCyclicGroup minimum representation
π_4^3=Z/2{Eη₂}
η_n=E^(n-2)η₂
η₃=Eη₂
π_4^3=Z/2{η₃}
applicability / invalid-case rejection
provenance
representative probe
full regression
```

Still outside Phase 50:

```text
general up-to-sign equality algebra
general quotient simplification
general first-isomorphism theorem engine
general suspension normalization
full Toda Proposition 2.7 formalization
Toda Proposition 5.1 proof completion
stable homotopy group model
higher Toda brackets
```

---

# Documentation

- `README.md` — current capabilities and status
- `docs/design.md` — current architecture, semantics, and boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capability dependency

Current behavior is defined by the latest README and design documents.

---

# Next development boundary

Phase 50 is complete.

Next candidate:

```text
Phase 51
Toda Proposition 5.1 proof dependency analysis
```

Start with dependency analysis, not implementation:

```text
actual Prop.5.1 proof dependency
↓
minimum missing representation / theorem semantics
↓
concrete proof completion
```
