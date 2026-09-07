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
representation != typing != theorem knowledge
structural equality != mathematical equality
```

The implementation strategy is to formalize only the minimum theorem consequences required by concrete homotopy-group calculations while preserving explicit provenance.

---

# Current status

Completed through Phase 57.

```text
Phase 1–27   generic proof / algebra / Toda-bracket foundation
Phase 28–38  actual H / Prop.2.2 / Prop.3.1 equality branch
Phase 39     PrimaryComponent
Phase 40     TodaPrimaryGroup
Phase 41     PreimageSubgroup
Phase 42     WhiteheadProduct
Phase 43     Toda Lemma 4.1 premise representation
Phase 44     Toda Lemma 4.1 case semantics
Phase 45     Toda Proposition 4.2 2-primary EHP exactness
Phase 46     Toda (4.5) stable-range iterated-suspension isomorphism
Phase 47     Toda Proposition 4.4 decomposition isomorphism
Phase 48     Toda Proposition 4.4 suspension injectivity consequence
Phase 49     π_3^2 = Z{η₂}
Phase 50     π_4^3 = Z/2{η₃}
Phase 51     Toda Proposition 5.1 dependency analysis
Phase 52     Δ(ι₅)=±2η₂ direct bridge
Phase 53     Toda (4.5) finite-cyclic transport
Phase 54     higher η-family bridge
Phase 55     Toda Proposition 5.1 finite-dimensional integration
Phase 56     Toda (5.2) composition isomorphism
Phase 57     Toda Lemma 5.2 end-to-end integration
```

Current full regression:

```text
2997 passed in 38.45s
```

Representative current probe:

```powershell
python -m probes.probe_phase57_capabilities
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

Core expression structures include:

```text
HomotopyElement
GeneratorSymbol
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

Core group / map structures include:

```text
PrimaryComponent
TodaPrimaryGroup
PreimageSubgroup
FreeCyclicGroup
FiniteCyclicGroup
DirectSumGroup
TodaSuspensionMap
TodaHopfInvariantMap
TodaDeltaMap
TodaIteratedSuspensionMap
TodaProp44DecompositionMap
```

Canonical map symbols:

```text
EHP_E_MAP     → E
EHP_H_MAP     → H
EHP_DELTA_MAP → Δ
```

Constructors do not perform theorem-aware normalization.

---

# Concrete branch through Proposition 5.1

Phase 49 derives:

```text
H injective
Δ=0
H surjective
H isomorphism
↓
η₂ = unique H-preimage of ι₃
↓
H(η₂)=ι₃
↓
π_3^2=Z{η₂}
```

Phase 50 derives:

```text
[ι₂,ι₂]=±2η₂
Δ(ι₅)=±2η₂
Ker(E)=Z{2η₂}
E surjective
↓
π_4^3=Z/2{η₃}
```

Phase 54 connects the higher η-family:

```text
η_n=E^(n-2)η₂
η₃=Eη₂
↓
E^(n-3)η₃=η_n
↓
π_{n+1}^n=Z/2{η_n}
```

Phase 55 integrates the finite-dimensional Proposition 5.1 result:

```text
π_3^2=Z{η₂}
H(η₂)=ι₃
Δ(ι₅)=±2η₂
π_{n+1}^n=Z/2{η_n}
↓
Toda Proposition 5.1 finite-dimensional result
```

The stable conclusion `(G_1;2)=Z/2{η}` remains deferred.

---

# Phase 56: Toda (5.2)

Phase 56 implements:

```text
η₂∘- : π_i^3 ≅ π_i^2
(i≥3)
```

via:

```text
i≥3
↓
π_{i-1}^1=0

H(η₂)=ι₃
↓
Prop.4.4, n=2, α=η₂
↓
Φ: π_{i-1}^1 ⊕ π_i^3 ≅ π_i^2

Φ|_{π_i^3}(γ)=η₂∘γ
↓
η₂∘- : π_i^3 ≅ π_i^2
```

No generic direct-sum simplifier or generic isomorphism-restriction framework was added.

---

# Phase 57: Toda Lemma 5.2

For:

```text
α ∈ π_i(S^3)
2α = 0
β ∈ {η₃,2ι₄,Eα}_1
```

the canonical conclusions are:

```text
H(β)=E²α
2β=η₃∘Eα∘η_{i+1}
β∈π_{i+2}^3
Δ(E²α)=0
```

The implementation uses `η_{i+1}`. The proof-ending occurrence of `η_{i+2}` is not used because it is incompatible with the typing and with the following `α=η₃` specialization.

## Phase 57 dependency

```text
Lemma 4.5
Proposition 2.6
Δ(ι₅)=±2η₂
Proposition 1.4
Proposition 1.3
Corollary 3.7
Toda (2.1)
Proposition 5.1 finite-dimensional result
```

Only the minimum consequences required by Lemma 5.2 are formalized.

## Hopf branch

```text
2α=0
↓ Lemma 4.5
2ι₃∘α=0

Proposition 2.6
↓
H(β) ∈ -Δ^-1(η₂∘2ι₃)∘E²α

Δ(ι₅)=±2η₂
↓
Δ^-1(2η₂)=±ι₅

integration
↓
H(β)=E²α
```

## Double-value branch

```text
β∈{η₃,2ι₄,Eα}_1
↓ Proposition 1.4
2β∈η₃∘E{2ι₃,α,2ι_i}

↓ Proposition 1.3
2β∈η₃∘-{2ι₄,Eα,2ι_{i+1}}_1

↓ Corollary 3.7
explicit representative
```

Indeterminacy vanishes through:

```text
γ∈π_{i+2}(S⁴)
↓ Toda (2.1)
E(η₃∘γ∘2ι_{i+2})=0
↓ Lemma 4.5, n=4 injectivity
η₃∘γ∘2ι_{i+2}=0
```

and the final conclusion is:

```text
2β=η₃∘Eα∘η_{i+1}
```

Bracket typing also yields `β∈π_{i+2}^3`, and the Hopf relation gives `Δ(E²α)=0`.

---

# Phase 57 provenance and tests

Representative probe reports:

```text
H(beta)=E^2 alpha derived = True
2 beta relation derived = True
beta membership derived = True
Delta(E^2 alpha)=0 derived = True
all final results are INFERENCE = True
final results are GIVEN = False
fixed point = True
```

Representative inference rounds:

```text
18
```

Focused Phase 57 suites:

```text
tests/test_phase57_lemma45_two_iota3.py              10 passed
tests/test_phase57_prop26_hopf_bracket.py            14 passed
tests/test_phase57_delta_two_eta2_preimage.py        14 passed
tests/test_phase57_bracket_transformation_chain.py   17 passed
tests/test_phase57_indeterminacy_vanishing.py        15 passed
tests/test_phase57_lemma52_integration.py            13 passed
tests/test_phase57_probe.py                           4 passed
```

Related regression:

```text
tests/test_phase55_probe.py                           8 passed
tests/test_toda_rules.py                             66 passed
```

Full regression:

```text
2997 passed in 38.45s
```

---

# Phase 57 completion boundary

Implemented:

```text
Lemma 5.2 statement / typing verification
Lemma 4.5 minimum consequence
Proposition 2.6 minimum consequence
Δ^-1(2η₂)=±ι₅ bridge
Proposition 1.4 / Proposition 1.3 / Corollary 3.7 minimum chain
Toda (2.1) + Lemma 4.5 indeterminacy vanishing
H(β)=E²α
2β=η₃∘Eα∘η_{i+1}
β∈π_{i+2}^3
Δ(E²α)=0
derived provenance
same-run integration
representative probe
full regression
```

Not implemented:

```text
full generic Proposition 1.3 formalization
full generic Proposition 1.4 formalization
full generic Proposition 2.6 formalization
full generic Corollary 3.7 formalization
generic Toda-bracket coset algebra
generic inverse-image algebra
generic sign normalization
generic Δ-H rewrite framework
generic scalar normalization
stable homotopy-group model
```

The generic inference engine is unchanged.

---

# Documentation

- `README.md` — current capabilities and status
- `docs/design.md` — current architecture, semantics, and boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capability dependency
- `docs/code_reference.md` — module responsibilities and major classes / functions

---

# Next development boundary

Phase 58:

```text
Toda (5.3) ν' consequence
```

Planned specialization:

```text
α=η₃∈π_4(S^3)
ν'∈{η₃,2ι₄,η₄}_1
```

Use the already-derived Lemma 5.2 result without reimplementing its proof:

```text
ν'∈π_6^3
H(ν')=η₅
2ν'=η₃∘η₄∘η₅
```

Phase 58 should remain a specialization / consequence phase.
