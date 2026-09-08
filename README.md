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

Completed through Phase 60.

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
Phase 58     Toda (5.3) ν′ consequence
Phase 59     Toda Proposition 5.3 finite-dimensional result
Phase 60     Toda Lemma 5.4 / ν₄ construction and literature-aware provenance
```

Current full regression:

```text
3334 passed in 132.72s
```

Representative current probe:

```powershell
python -m probes.probe_phase60_capabilities
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

Phase 57 completion regression:

```text
2997 passed in 38.45s
```

---

# Phase 58: Toda (5.3) ν′ consequence

Phase 58 specializes the already-derived Lemma 5.2 result. The Phase 57 proof chain is not reimplemented.

The starting membership is:

```text
ν′∈{η₃,2ι₄,η₄}_1
```

This is a membership statement: `ν′` is chosen as an element of the indexed Toda bracket. The bracket itself is not identified structurally with `ν′`.

The specialization is:

```text
α=η₃
i=4
β=ν′
```

Using the independently derived:

```text
π_4^3=Z/2{η₃}
↓
2η₃=0
```

Phase 58-3 derives the raw Lemma 5.2 specialization:

```text
ν′∈π_6^3
H(ν′)=E²η₃
2ν′=η₃∘Eη₃∘η₅
```

## Hopf-value normalization

The existing η-family definitions give the concrete Phase 58 bridge:

```text
E²η₃=η₅
```

and generic equality transitivity gives:

```text
H(ν′)=E²η₃
E²η₃=η₅
↓
H(ν′)=η₅
```

## Double-value normalization

The concrete η-family bridge gives:

```text
Eη₃=η₄
```

The existing generic composition-preservation rules are applied once:

```text
Eη₃=η₄
↓ right composition by η₅
Eη₃∘η₅=η₄∘η₅

↓ left composition by η₃
η₃∘(Eη₃∘η₅)
=
η₃∘(η₄∘η₅)
```

and generic equality transitivity gives:

```text
2ν′=η₃∘Eη₃∘η₅
↓
2ν′=η₃∘η₄∘η₅
```

The composition-preservation rules are repeatable `Relation → Relation` rules, so the Phase 58 representative flow applies them one-shot with `find_inference_match()` / `apply_inference_match()` instead of putting them into unrestricted fixed-point closure.

## Structural η-name boundary

The existing concrete η-family constructor uses:

```text
η_4
η_5
```

for concrete indices `n>=4`, while the Toda (5.3) branch uses canonical displayed elements:

```text
η₄
η₅
```

Phase 58 does not change the constructor globally. Dedicated narrow bridges validate dimension / source / target / generator identity and produce the canonical concrete conclusion.

No generic η-name normalizer is added.

---

# Phase 58 provenance and tests

Representative probe:

```powershell
python -m probes.probe_phase58_capabilities
```

reports:

```text
ν′ ∈ π_6^3
H(ν′) = η₅
2ν′ = η₃∘η₄∘η₅
```

Provenance / integration:

```text
nu-prime membership derived = True
H(nu-prime)=eta_5 derived = True
2 nu-prime relation derived = True
all final results are INFERENCE = True
final results are GIVEN = False
```

Same-run execution:

```text
fixed-point-safe stages complete = True
composition propagation one-shot = True
shared raw specialization = True
```

Focused Phase 58 suites:

```text
tests/test_phase58_nu_prime_specialization.py       11 passed
tests/test_phase58_lemma52_specialization.py        14 passed
tests/test_phase58_hopf_eta5_bridge.py              13 passed
tests/test_phase58_double_eta4_bridge.py            15 passed
tests/test_phase58_probe.py                          9 passed
```

Related regression:

```text
tests/test_relation_rules.py                        50 passed
tests/test_toda_rules.py                            66 passed
```

Final full regression:

```text
3059 passed in 38.23s
```

---

# Phase 58 completion boundary

Implemented:

```text
ν′∈{η₃,2ι₄,η₄}_1 specialization recognition
α=η₃, i=4, β=ν′ specialization
2η₃=0 from derived π_4^3=Z/2{η₃}
ν′∈π_6^3
H(ν′)=E²η₃
2ν′=η₃∘Eη₃∘η₅
E²η₃=η₅ concrete bridge
H(ν′)=η₅
Eη₃=η₄ concrete bridge
one-shot generic composition propagation
2ν′=η₃∘η₄∘η₅
derived provenance
representative staged same-run
representative probe
full regression
```

Not implemented:

```text
generic concrete η normalization
global η_4 / η₄ or η_5 / η₅ normalization
unrestricted fixed-point composition closure
generic Toda-bracket specialization framework
generic Toda-bracket coset algebra
generic inverse-image algebra
generic sign normalization
generic Δ-H rewrite framework
stable homotopy-group model
```

The generic inference engine remains unchanged.

---

# Phase 59: Toda Proposition 5.3 finite-dimensional result

Phase 59 proves the finite-dimensional part of Toda Proposition 5.3 without introducing a stable homotopy-group model.

Notation:

```text
η_n² := η_n∘η_{n+1}
```

The final capability is:

```text
π_{n+2}^n = Z/2{η_n²}
(n≥2)
```

The proof is implemented by separate finite-dimensional branches.

## n=2

```text
π_4^3=Z/2{η₃}
+
η₂∘- : π_4^3 ≅ π_4^2
↓
π_4^2=Z/2{η₂²}
```

## n=3

Using Proposition 5.1, EHP exactness, and the Phase 58 consequence `H(ν′)=η₅`:

```text
Δ:π_5^5→π_3^2 injective
↓
H:π_5^3→π_5^5 zero
↓
E:π_4^2→π_5^3 surjective
```

and:

```text
H(ν′)=η₅
+
π_6^5=Z/2{η₅}
↓
H:π_6^3→π_6^5 surjective
↓
Δ:π_6^5→π_4^2 zero
↓
E:π_4^2→π_5^3 injective
```

therefore:

```text
E:π_4^2≅π_5^3
Eη₂²=η₃²
↓
π_5^3=Z/2{η₃²}
```

## n=4

```text
π_6^7=0
+
π_5^3 --E--> π_6^4 --H--> π_6^7 exact
↓
E:π_5^3→π_6^4 surjective
```

Phase 48 gives the corresponding injectivity consequence. A narrow structural bridge identifies the concrete source `π_5^3`. Hence:

```text
E:π_5^3≅π_6^4
Eη₃²=η₄²
↓
π_6^4=Z/2{η₄²}
```

## n≥5

Toda (4.5) gives:

```text
E^(n-4):π_6^4≅π_{n+2}^n
```

so Phase 59 first derives:

```text
π_{n+2}^n=Z/2{E^(n-4)η₄²}
```

and then uses the theorem-specific bridge:

```text
E^(n-4)η₄²=η_n²
```

to obtain:

```text
π_{n+2}^n=Z/2{η_n²}
```

The four branches are aggregated into:

```text
TodaProp53FiniteDimensionalStatement
```

All group conclusions used by the aggregate are independently derived `ProofRule.INFERENCE` steps. The final aggregate is not reintroduced as `GIVEN`.

## Phase 59 representation boundary

`η_n²` remains an ordinary `Composition`:

```text
η_n² = Composition(η_n,η_{n+1})
```

The implementation does not add:

```text
EtaSquare class
generic cyclic-generator transport
generic suspension-of-composition normalization
generic η-name normalization
generic scalar normalization
stable homotopy-group model
```

The stable conclusion:

```text
(G_2;2)=Z/2{η²}
```

remains deferred.

## Phase 59 provenance and tests

Representative probe:

```powershell
python -m probes.probe_phase59_capabilities
```

Focused completion integration:

```text
tests/test_phase59_prop53_integration.py  18 passed
```

Final full regression:

```text
3177 passed in 123.99s
```


---

# Phase 60: Toda Lemma 5.4 / ν₄ construction

Phase 60 proves the finite-dimensional Toda Lemma 5.4 target:

```text
ν₄ ∈ π_7^4
H(ν₄) = ι₇
2Eν₄ = E²ν′
```

The proof reuses the independently derived Phase 58 and Phase 59 results rather than reintroducing Lemma 5.4 as a given fact.

## Toda (5.4)

Phase 60 first derives the bracket value:

```text
{η_n,2ι_(n+1),η_(n+1)}_t
=
{±E^(n-3)ν′}
```

for `n≥3` and `0≤t≤n-2`.

For `t≥1`, the indeterminacy is reduced theorem-specifically:

```text
Toda (4.7) + Proposition 5.3
↓
Indeterminacy = <η_n∘η_(n+1)∘η_(n+2)>

Phase 58:
2ν′=η₃∘η₄∘η₅
↓
2E^(n-3)ν′=η_n∘η_(n+1)∘η_(n+2)

↓
Indeterminacy = <2E^(n-3)ν′>
```

The inclusion

```text
E^(n-3)ν′ ∈ {η_n,2ι_(n+1),η_(n+1)}_t
```

uses the `ν′` bracket definition, Toda Proposition 1.3, and Toda (1.15).

The `t=0` branch uses Toda (3.2) suspension surjectivity together with Toda (1.15). No generic Toda-bracket coset algebra is introduced.

## Theorem 3.6 specialization

Phase 60 specializes Toda Theorem 3.6 to the Lemma 5.4 branch:

```text
α = η₂
β = 2ι₃
t = 1
```

Using derived order-two information, the specialization produces an element:

```text
α* ∈ π_7^4
```

with:

```text
2Eα* ∈ -{η₅,2ι₆,η₆}_3
```

Toda (5.4), specialized to `n=5,t=3`, gives:

```text
{η₅,2ι₆,η₆}_3 = {±E²ν′}
```

and therefore:

```text
2Eα* = ±E²ν′
```

The implementation does not add a generic existential-witness framework or a generic sign solver.

## Hopf invariant parity

Phase 58 gives:

```text
H(ν′)=η₅
```

and Proposition 5.1 gives:

```text
π_6^5=Z/2{η₅}
```

Together with `2Eα*=±E²ν′`, the Toda (4.8) consequence used in Lemma 5.4 yields:

```text
H(α*)=(2s+1)ι₇
```

The symbolic integer `s` is retained in the theorem-specific statement needed by the Whitehead correction. No generic divisibility or parity solver is added.

## Whitehead correction and ν₄

Phase 60 records the Lemma 5.4 Whitehead facts:

```text
H[ι₄,ι₄]=(-1)^u 2ι₇
E[ι₄,ι₄]=0
```

and keeps the two sign branches explicitly.

If:

```text
2Eα*=+E²ν′
```

use:

```text
ν₄=α* - (-1)^u s[ι₄,ι₄]
```

If:

```text
2Eα*=-E²ν′
```

use:

```text
ν₄=-α* + (-1)^u(s+1)[ι₄,ι₄]
```

Both branches derive:

```text
ν₄∈π_7^4
H(ν₄)=ι₇
2Eν₄=E²ν′
```

The final results are integrated into:

```text
TodaLemma54Statement
```

and the aggregate itself is an independently derived `ProofRule.INFERENCE` result.

## Literature-aware provenance

Phase 60 adds:

```text
LiteratureStatement
```

next to the existing `LiteratureReference` metadata.

A literature statement records:

```text
reference
statement text
```

so the representative probe can display not only which theorem was cited, but also what statement was used.

The Phase 60 probe additionally displays a Phase-specific `Used in:` map, for example:

```text
[Toda Theorem 3.6]
Used in:
  - Phase 60-6: α=η₂, β=2ι₃, t=1 specialization
  - Phase 60-6: α*∈π_7^4 and 2Eα* bracket consequence
Statement:
  ...
```

The representative probe also contains a proof-style derivation section that displays the mathematical chain in proof order, for example:

```text
ν′ ∈ {η₃, 2ι₄, η₄}_1
↓ suspend by E^(n-3)
E^(n-3)ν′
∈ E^(n-3){η₃, 2ι₄, η₄}_1
⊂ (-1)^(n-3){η_n, 2ι_(n+1), η_(n+1)}_(n-2)
  [Toda Proposition 1.3]
⊂ (-1)^(n-3){η_n, 2ι_(n+1), η_(n+1)}_t
  [Toda (1.15), 1 ≤ t ≤ n-2]
```

This proof-style section is currently hand-authored presentation code in the Phase 60 probe. It is not yet generated automatically from the `ProofStep` graph. The long-term direction is to derive such equation chains and natural-language proof narratives from structured proof data, inference-rule display metadata, and literature statements.

This keeps theorem usage human-readable without introducing a theorem repository or automatic theorem search.

## Phase 60 provenance and tests

Representative probe:

```powershell
python -m probes.probe_phase60_capabilities
```

Representative output verifies:

```text
ν₄ membership derived = True
H(ν₄)=ι₇ derived = True
2Eν₄=E²ν′ derived = True
final aggregate derived = True
final aggregate is GIVEN = False
all final premises are INFERENCE = True
fixed point = True
```

The probe also prints:

```text
Literature statements used
Reference / locator / author / source / year
Used in: Phase 60-x ...
Statement: ...
```

Focused Phase 60 completion tests include:

```text
tests/test_phase60_toda36_specialization.py            20 passed
tests/test_phase60_toda48_hopf_parity.py               18 passed
tests/test_phase60_nu4_whitehead_correction.py          19 passed
tests/test_phase60_lemma54_integration.py               20 passed
tests/test_phase60_probe.py                             16 passed
```

Final full regression:

```text
3334 passed in 132.72s
```

## Phase 60 representation boundary

Phase 60 deliberately does not add:

```text
generic Toda-bracket coset algebra
generic sign solver
generic divisibility framework
generic existential witness framework
generic Whitehead correction algebra
full Theorem 3.6 formalization
full Toda (4.8) formalization
theorem statement repository / search
```

These remain deferred until a concrete later proof requires them.

## Future proof narrative generation

The current inference engine already stores the ingredients needed for future proof-text generation:

```text
ProofStep graph
+ structural Expression objects
+ InferenceRule provenance
+ LiteratureStatement metadata
```

The intended future direction is:

```text
ProofStep graph
↓
proof-chain selection / compression
↓
equation-chain generation
↓
citation insertion at the step where it is used
↓
rule-specific narrative templates
↓
console / Markdown / LaTeX proof output
```

The Phase 60 `Proof-style derivation` is a manual representative of this intended output, not the automatic generator itself. Generic proof-narrative generation remains deferred until several concrete proof branches reveal a stable display schema.

---

# Documentation

- `README.md` — current capabilities and status
- `docs/design.md` — current architecture, semantics, and boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capability dependency
- `docs/code_reference.md` — module responsibilities and major classes / functions

---

# Next development boundary

Phase 60 is complete.

The next target is:

```text
Phase 61
Toda Lemma 5.5 bracket transport
```

The intended dependency is:

```text
Phase 60 Lemma 5.4 provenance
+
α* bracket inclusion
+
E[ι₄,ι₄]=0
↓
E^tν₄=±E^tα*
↓
Toda Lemma 5.5
```

Phase 61 should reuse the Phase 60 proof objects and must not reimplement the construction of `α*` or `ν₄`.

Stable `(G_1;2)=Z/2{η}`, stable `(G_2;2)=Z/2{η²}`, a general stable homotopy-group model, generic Toda-bracket coset algebra, generic sign solving, and theorem-repository infrastructure remain deferred until a concrete proof branch requires them.
