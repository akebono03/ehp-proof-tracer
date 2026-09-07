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

Completed through Phase 55.

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
Phase 51  Toda Proposition 5.1 proof dependency analysis
Phase 52  Δ(ι₅)=±2η₂ direct bridge
Phase 53  Toda (4.5) finite-cyclic transport
Phase 54  higher η-family bridge and finite-cyclic integration
Phase 55  Toda Proposition 5.1 finite-dimensional integration / provenance
```

Current full regression:

```text
2844 passed in 31.12s
```

Representative current probe:

```powershell
python -m probes.probe_phase55_capabilities
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

# Phase 51: Toda Proposition 5.1 proof dependency analysis

Actual finite-dimensional target analyzed:

```text
π_3^2=Z{η₂}
π_{n+1}^n=Z/2{η_n}  (n≥3)
H(η₂)=ι₃
Δ(ι₅)=±2η₂
```

The scan of Toda p.39 contains an internal inconsistency: the proof text has `Δ(ι₅)=±2η₂`, while the printed Proposition 5.1 line has `±2η₃`. The proof text is dimensionally compatible with `Δ(ι₅)∈π_3^2`, so the development target uses `Δ(ι₅)=±2η₂`.

Already available without using Proposition 5.1 as a premise:

```text
Phase 49
π_3^2=Z{η₂}
H(η₂)=ι₃

Phase 50
π_4^3=Z/2{η₃}
[ι₂,ι₂]=±2η₂
Δ(ι₅)=±[ι₂,ι₂]

Phase 46
E^(m-n): π_{n+k}^n → π_{m+k}^m isomorphism
in the stable range
```

No additional low-dimensional group facts were identified as necessary for the finite-dimensional part of Proposition 5.1. The missing implementation has been reduced to:

```text
1. Δ(ι₅)=±2η₂ direct bridge
2. Toda (4.5) finite-cyclic transport
3. E^(n-3)η₃=η_n bridge
4. Proposition 5.1 finite-dimensional integration / provenance
```

Circular-dependency boundary:

```text
SAFE:
Phase 49 / Phase 50 / Toda (4.5) derived results

NOT SAFE AS PROP.5.1 PREMISES:
old Phase 35–36 traces that use H(η₂)=ι₃ as a Prop.5.1 GIVEN fact
```

Stable `(G_1;2)=Z/2{η}` and the post-Proposition-5.1 composition isomorphism (5.2) remain deferred.

Phase 51 made no production-code changes.

---

# Phase 52: `Δ(ι₅)=±2η₂` direct bridge

Target:

```text
Δ(ι₅)=±[ι₂,ι₂]
+
[ι₂,ι₂]=±2η₂
↓
Δ(ι₅)=±2η₂
```

Phase 52 reuses the existing theorem-specific statements:

```text
TodaDeltaImageUpToSignStatement
TodaPi32WhiteheadSquareUpToSignStatement
```

No new up-to-sign representation is added. The conclusion is represented as:

```text
TodaDeltaImageUpToSignStatement(
  map=Δ: π_5^5 → π_3^2,
  element=ι₅,
  positive_value=2η₂,
)
```

Specific rule:

```text
toda_delta_iota5_two_eta2_up_to_sign_inference_rule()
```

Applicability is restricted to:

```text
Δ : π_5^5 → π_3^2
element = ι₅
intermediate value = [ι₂,ι₂]
Whitehead-square value = 2η₂
```

Rejected examples include wrong Δ source / target, wrong element, wrong Whitehead square, wrong coefficient, and wrong η index.

Integrated representative fixed point:

```text
round 1
H([ι_2,ι_2]) = ±2ι_3
Δ(ι_5) = ±[ι_2,ι_2]
E: π_3^2 → π_4^3 is surjective
η₃ = Eη₂

round 2
[ι_2,ι_2] = ±2η₂

round 3
Δ(ι_5) = ±2η₂
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
derived step count = 10
derived round count = 6
fixed point = True
```

Representative probe:

```powershell
python -m probes.probe_phase52_capabilities
```

Phase 52 tests:

```text
tests/test_phase52_delta_direct_bridge.py  16 passed
tests/test_phase52_probe.py                 8 passed
```

Full regression:

```text
2731 passed in 26.67s
```

Phase 52 boundary:

```text
implemented:
  Δ(ι₅)=±2η₂ direct consequence
  theorem-specific direct bridge
  wrong-instance rejection
  Phase 50 chain integration
  provenance
  representative probe

not implemented:
  general up-to-sign transitivity
  general sign solver
  Toda (4.5) finite-cyclic transport
  higher η-family bridge
  Proposition 5.1 finite-dimensional integration
```

---

# Phase 53: Toda (4.5) finite-cyclic transport

Target:

```text
π_4^3=Z/2{η₃}
+
E^(n-3): π_4^3 ≅ π_{n+1}^n
↓
π_{n+1}^n=Z/2{E^(n-3)η₃}
```

Phase 53 reuses the existing structures:

```text
Toda45IsomorphismStatement
TodaIteratedSuspensionMap
FiniteCyclicGroup
IteratedSuspension
Relation
```

No new generic transport representation is introduced.

Specific inference rule:

```text
toda_45_pi4_3_finite_cyclic_transport_inference_rule()
```

The rule is restricted to the concrete source structure:

```text
π_4^3=Z/2{η₃}
```

and a Toda (4.5) iterated suspension isomorphism with target shape:

```text
E^(n-3): π_4^3 → π_{n+1}^n.
```

It preserves the order and transports only the required generator expression:

```text
η₃
↓
E^(n-3)η₃
```

The Phase 46 stable-range branch and the Phase 50 concrete calculation are integrated in one fixed-point run:

```text
Phase 50 derived
π_4^3=Z/2{η₃}

Phase 46 derived
Toda (4.5) isomorphism

↓

Phase 53 derived
π_{n+1}^n=Z/2{E^(n-3)η₃}
```

The final transport step preserves two derived premises; the Phase 50 group result is not reintroduced as GIVEN.

Representative counts:

```text
given premise count = 14
derived step count = 11
derived round count = 7
fixed point = True
```

Representative probe:

```powershell
python -m probes.probe_phase53_capabilities
```

Phase 53 tests:

```text
tests/test_phase53_finite_cyclic_transport.py  24 passed
tests/test_phase53_integration.py               6 passed
tests/test_phase53_probe.py                     8 passed
```

Full regression:

```text
2769 passed in 25.60s
```

Phase 53 boundary:

```text
implemented:
  specific Toda (4.5) finite-cyclic transport
  stable-range branch integration
  wrong-instance rejection
  Phase 50 derived-result integration
  provenance
  representative probe

not implemented:
  E^(n-3)η₃=η_n
  generic isomorphism transport
  generic generator transport
  generic suspension normalization
  Proposition 5.1 finite-dimensional integration
  stable homotopy model
```

---

# Phase 54: higher η-family bridge and finite-cyclic integration

Phase 54 completes the higher η-family connection needed after the Phase 53 Toda (4.5) transport.

The symbolic η-family definition is now representable for symbolic `n`:

```text
η_n = E^(n-2)η₂
```

using the existing:

```text
TodaEtaFamilyDefinitionStatement
IteratedSuspension
ScalarSymbol
ScalarSum
```

For the existing low-dimensional bridge:

```text
η₃ = Eη₂
```

the Phase 54 η-family-specific rule derives:

```text
η_n = E^(n-2)η₂
+
η₃ = Eη₂
↓
E^(n-3)η₃ = η_n
```

Specific rule:

```text
toda_higher_eta_family_bridge_inference_rule()
```

The rule is deliberately narrow. It does not introduce generic iterated-suspension composition, generic suspension normalization, or generic scalar normalization.

The Phase 53 transported finite-cyclic group:

```text
π_{n+1}^n = Z/2{E^(n-3)η₃}
```

is then connected to the higher η-family bridge:

```text
π_{n+1}^n = Z/2{E^(n-3)η₃}
+
E^(n-3)η₃ = η_n
↓
π_{n+1}^n = Z/2{η_n}
```

Specific rule:

```text
toda_higher_eta_finite_cyclic_generator_inference_rule()
```

This is not a generic cyclic-generator rewrite rule. It accepts only the Phase 53 target shape, order `2`, the transported generator `E^(n-3)η₃`, and the matching higher η-family relation.

Applicability tests reject:

```text
concrete higher η-family index
mismatched symbolic index
wrong η_n element structure
wrong η-family definition exponent
wrong η₃ base
wrong suspended η₂ base
reversed η₃ relation
non-equality η₃ relation
```

The Phase 53 and Phase 54 branches are integrated in one fixed-point run. The Phase 53 transported group and the higher η bridge are both derived premises of the final group result.

Representative result:

```text
η_n = E^(n-2)η₂
η₃ = Eη₂
↓
E^(n-3)η₃ = η_n

π_{n+1}^n = Z/2{E^(n-3)η₃}
+
E^(n-3)η₃ = η_n
↓
π_{n+1}^n = Z/2{η_n}
```

Representative counts:

```text
given premise count = 15
derived step count = 13
derived round count = 8
fixed point = True
```

Representative probe:

```powershell
python -m probes.probe_phase54_capabilities
```

Phase 54 tests:

```text
tests/test_phase54_eta_family_bridge.py  20 passed
tests/test_phase54_integration.py         7 passed
tests/test_phase54_probe.py               8 passed
```

Full regression:

```text
2804 passed in 26.50s
```

Phase 54 boundary:

```text
implemented:
  symbolic higher η-family definition
  η-family-specific E^(n-3)η₃=η_n bridge
  applicability / wrong-instance rejection
  Phase 53 transported finite-cyclic integration
  π_{n+1}^n=Z/2{η_n}
  derived provenance
  representative probe
  full regression

not implemented:
  generic iterated-suspension composition
  generic suspension normalization
  generic scalar normalization
  generic cyclic-generator rewrite
  Proposition 5.1 final integration
  stable homotopy model
```

---

# Phase 55: Toda Proposition 5.1 finite-dimensional integration / provenance

Phase 55 integrates the four independently derived finite-dimensional results needed for Toda Proposition 5.1:

```text
π_3^2=Z{η₂}
H(η₂)=ι₃
Δ(ι₅)=±2η₂
π_{n+1}^n=Z/2{η_n}
```

Minimum aggregate representation:

```text
TodaProp51FiniteDimensionalStatement
```

Its four fields preserve the existing representations without introducing a generic conjunction framework:

```text
pi3_2_group_relation
eta2_hopf_relation
delta_iota5_relation
higher_eta_group_relation
```

Specific integration rule:

```text
toda_prop51_finite_dimensional_integration_inference_rule()
```

The rule requires exactly the four Proposition 5.1 finite-dimensional results in their expected structural forms and requires every premise to be `ProofRule.INFERENCE`. Therefore the final Proposition 5.1 result cannot be built by reintroducing one of these results as a GIVEN premise.

Dependency chain:

```text
Phase 49 derived:
  π_3^2=Z{η₂}
  H(η₂)=ι₃

Phase 52 derived:
  Δ(ι₅)=±2η₂

Phase 54 derived:
  π_{n+1}^n=Z/2{η_n}

↓

Toda Proposition 5.1
finite-dimensional result
```

The Phase 55 representative run is rebuilt from the Phase 49 base premises instead of blindly extending the Phase 50 representative premise set. This avoids reintroducing the old Phase 49 results as GIVEN premises.

Circular-dependency checks reject:

```text
GIVEN H(η₂)=ι₃
GIVEN π_3^2=Z{η₂}
GIVEN Δ(ι₅)=±2η₂
GIVEN π_{n+1}^n=Z/2{η_n}
GIVEN Proposition 5.1 result used in place of a missing dependency
pre-direct Δ result Δ(ι₅)=±[ι₂,ι₂]
pre-η-family transported group π_{n+1}^n=Z/2{E^(n-3)η₃}
```

Representative provenance:

```text
pi_3^2 result is derived = True
H(eta_2)=iota_3 is derived = True
Delta(iota_5)=+-2eta_2 is derived = True
higher eta group is derived = True
final Prop.5.1 result is derived = True
final premise count = 4
final premises are derived = True
H(eta_2)=iota_3 is GIVEN premise = False
pi_3^2 result is GIVEN premise = False
Prop.5.1 result is GIVEN premise = False
given premise count = 17
derived step count = 23
derived round count = 14
fixed point = True
```

Representative probe:

```powershell
python -m probes.probe_phase55_capabilities
```

Phase 55 tests:

```text
tests/test_phase55_prop51_finite_dimensional_statement.py      5 passed
tests/test_phase55_prop51_phase49_dependency.py                7 passed
tests/test_phase55_prop51_phase52_phase54_dependency.py        7 passed
tests/test_phase55_prop51_integration.py                       6 passed
tests/test_phase55_prop51_rejection_provenance.py              7 passed
tests/test_phase55_probe.py                                    8 passed
```

Full regression:

```text
2844 passed in 31.12s
```

Phase 55 boundary:

```text
implemented:
  TodaProp51FiniteDimensionalStatement
  Phase 49 dependency connection
  Phase 52 / 54 dependency connection
  finite-dimensional Proposition 5.1 integration rule
  four-derived-premise provenance
  circular-dependency rejection
  non-circular representative run
  representative probe
  full regression

not implemented:
  stable (G_1;2)=Z/2{η}
  stable homotopy-group model
  composition isomorphism (5.2)
  generic cyclic-generator rewrite
  generic scalar normalization
  generic suspension normalization
```

---

# Next development boundary

Phase 55 is complete.

The finite-dimensional part of Toda Proposition 5.1 is now integrated with independently derived provenance. The next concrete Phase is intentionally not fixed here; it should be chosen from an actual mathematical need.

Continue to defer the stable `(G_1;2)=Z/2{η}` conclusion, a stable homotopy-group model, composition isomorphism (5.2), generic cyclic-generator rewriting, generic scalar normalization, and generic suspension normalization until a concrete dependency requires them.
