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

Completed through Phase 72.

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
Phase 61     Toda Lemma 5.5 bracket transport and literature-aware provenance
Phase 62     Toda (5.5) finite-dimensional ν-family integration
Phase 63     Toda (5.6) ν₄ decomposition isomorphism
Phase 64     performance stabilization
Phase 65     Toda Proposition 5.6 finite-dimensional computation
Phase 66     Toda Equation (5.8) integration / proof record foundation
Phase 67     Toda Lemma 5.7 integration / Delta generator consequence
Phase 68     Toda Proposition 5.8 finite-dimensional computation
Phase 69     Toda Equation (5.10): Δ(ι₁₁)=ν₅η₈
Phase 70     Toda Proposition 5.9 finite-dimensional computation
Phase 71     Toda Equation (5.12): Δ injective for n=4,5,6
Phase 72     Toda Lemma 5.10: Δ(ι₁₃)∈{ν₆,η₉,2ι₁₀} mod 2π₁₁(S⁶)
```

Latest repository-wide regression:

```text
4990 passed in 70.11s
```

Phase 64 same-machine baseline:

```text
3657 passed in 259.11s
```

The Phase 64 final regression is approximately 88.4% faster than the same-machine baseline while preserving the same 3657-test coverage.

Phase 72 mathematical capability and regression verification are complete. Repository-wide wall time is machine-dependent because development is performed on two PCs; the latest recorded home-laptop run is 4990 passed in 70.11s.

Representative current probe:

```powershell
python -m probes.probe_phase72_capabilities
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

# Phase 61: Toda Lemma 5.5 bracket transport

Phase 61 proves the Toda Lemma 5.5 consequence:

```text
β ∈ π_(t+2)(S^m)
β∘η_(t+2)=0
t>0
↓
{η_(m+2),E³β,η_(t+5)}_3
contains
±(E²β∘E^tν₄)
```

The implementation reuses the Phase 60 `α*` / `ν₄` provenance and does not reconstruct Lemma 5.4.

## Minimum contains-up-to-sign semantics

Phase 61 introduces:

```text
TodaLemma55BracketContainsUpToSignStatement
```

with:

```text
bracket
positive_value
```

Its meaning is:

```text
bracket contains x or -x
```

This is intentionally weaker than the Phase 60 `Toda54BracketUpToSignStatement`, which represents a bracket value set of the form `{±x}`. No generic sign object or generic bracket-containment algebra is added.

## α* bracket inclusion

Using the derived Phase 60 Theorem 3.6 specialization together with the Lemma 5.5 hypotheses:

```text
β ∈ π_(t+2)(S^m)
β∘η_(t+2)=0
t≥1
```

Phase 61 derives:

```text
{η_(m+2),E³β,η_(t+5)}_3
contains
±(E²β∘E^tα*)
```

The `α*` is not reintroduced as a `GIVEN`; it is reused from the derived Phase 60 provenance.

## ν₄ suspension correction

Phase 60 stores the two Whitehead-correction branches:

```text
ν₄=α* - (-1)^u s[ι₄,ι₄]
```

and:

```text
ν₄=-α* + (-1)^u(s+1)[ι₄,ι₄].
```

Together with:

```text
E[ι₄,ι₄]=0
t>0
```

Phase 61 derives the theorem-specific up-to-sign suspension consequence:

```text
E^tν₄=±E^tα*
```

This is stored in:

```text
TodaLemma55SuspensionUpToSignStatement
```

No generic Whitehead-correction algebra or generic up-to-sign transitivity is introduced.

## α* → ν₄ composition bridge

Phase 61 combines:

```text
bracket contains ±(E²β∘E^tα*)
```

with:

```text
E^tν₄=±E^tα*
```

to derive:

```text
{η_(m+2),E³β,η_(t+5)}_3
contains
±(E²β∘E^tν₄).
```

The bridge is Lemma-5.5-specific. The generic relation engine is unchanged.

## Final aggregate and literature-aware provenance

The final theorem-level aggregate is:

```text
TodaLemma55Statement
```

It retains:

```text
ν₄
TodaLemma54Statement
β membership
β∘η_(t+2)=0
t≥1
final bracket inclusion
literature statements
```

The final integration explicitly requires the derived `TodaLemma54Statement`, so the `ν₄` occurring in Lemma 5.5 remains connected to the Lemma 5.4 construction.

Phase 61 records direct literature statements for:

```text
Toda Lemma 5.5
Toda Lemma 5.5 proof
```

while Phase 60 literature remains inherited through the nested Lemma 5.4 aggregate.

## Applicability and provenance regression

Phase 61 verifies rejection of, among other cases:

```text
wrong β group
wrong β∘η premise
t≥0
α* used as the final ν₄ representative
Lemma 5.4 aggregate replaced by GIVEN
final ν₄ inclusion replaced by GIVEN
```

The final provenance graph is also checked to be acyclic.

The theorem hypotheses remain explicit `GIVEN` inputs:

```text
β membership
β∘η_(t+2)=0
t≥1
```

while the theorem dependency spine remains derived:

```text
Phase 60 Theorem 3.6 α*      INFERENCE
Phase 60 ν₄ construction     INFERENCE
Phase 60 Lemma 5.4 aggregate INFERENCE
Phase 61 α* inclusion        INFERENCE
Phase 61 suspension bridge   INFERENCE
Phase 61 ν₄ inclusion        INFERENCE
Phase 61 Lemma 5.5 aggregate INFERENCE
```

## Representative probe

Run:

```powershell
python -m probes.probe_phase61_capabilities
```

The probe displays:

```text
Result
Proof-style derivation
Provenance / integration
Literature statements used
Phase 61 completion boundary
```

Representative machine checks include:

```text
Lemma 5.4 aggregate derived = True
alpha-star bracket inclusion derived = True
E^tν₄=±E^tα* derived = True
final ν₄ bracket inclusion derived = True
final aggregate derived = True
final aggregate is GIVEN = False
theorem dependencies are INFERENCE = True
Lemma 5.5 hypotheses remain GIVEN = True
fixed point = True
```

The proof-style derivation remains a hand-authored presentation layer, not automatic proof-text generation. Phase 61 provides a second concrete proof-display example after Phase 60, which will help stabilize a future generic proof-narrative schema.

## Phase 61 focused tests

Verified focused suites include:

```text
tests/test_phase61_lemma55_statement.py                   8 passed
tests/test_phase61_lemma55_alpha_star_inclusion.py       13 passed
tests/test_phase61_lemma55_nu4_suspension.py             16 passed
tests/test_phase61_lemma55_nu4_composition.py            14 passed
tests/test_phase61_lemma55_integration.py                20 passed
tests/test_phase61_lemma55_applicability_provenance.py   15 passed
tests/test_phase61_probe.py                              16 passed
```

Related Phase 60 / Toda regression also passed during Phase 61 development. The final repository-wide Phase 61 regression count should be recorded after:

```powershell
python -m pytest -q
```

## Phase 61 representation boundary

Phase 61 deliberately does not add:

```text
generic Toda-bracket containment algebra
generic up-to-sign transitivity
generic sign solver
generic Whitehead correction algebra
full Theorem 3.6 formalization
automatic proof narrative generation
Toda (5.5) ν-family calculation
```

---

# Phase 62: Toda (5.5) finite-dimensional ν-family

Phase 62 implements the finite-dimensional ν-family branch of Toda (5.5).

The family notation is:

```text
ν_n:=E^(n-4)ν₄
(n≥4)
```

represented by:

```text
TodaNuFamilyDefinitionStatement
```

The stable notation:

```text
ν:=E^∞ν₄
```

and the stable relation:

```text
4ν=η³
```

remain deferred.

## Double-value transport

Phase 60 independently derived:

```text
2Eν₄=E²ν′
```

For symbolic `n≥5`, Phase 62 introduces the theorem-specific rule:

```text
toda_55_nu_family_double_suspension_transport_inference_rule()
```

and derives:

```text
2ν_n=E^(n-3)ν′
```

The rule requires the actual derived `TodaLemma54Statement`; replacing Lemma 5.4 by a `GIVEN` shortcut is rejected.

## η-cube bridge

Phase 62 does not add a new theorem-specific rule for the second relation.

Instead it reuses generic relation mechanics:

```text
equality_preserved_under_multiple_inference_rule(2)
nested_integer_multiple_inference_rule(2,2,ν_n)
equality_symmetry_inference_rule()
equality_transitivity_inference_rule()
```

in a staged one-shot chain:

```text
2ν_n=E^(n-3)ν′
↓ ×2
4ν_n=2E^(n-3)ν′
```

Phase 60 already derives:

```text
2E^(n-3)ν′
=
η_n∘η_(n+1)∘η_(n+2)
```

therefore:

```text
4ν_n
=
η_n∘η_(n+1)∘η_(n+2)
=
η_n³
```

No dedicated `EtaCube` class is introduced.

## Applicability boundary

The family definition and Toda (5.5) relation have different finite-dimensional ranges:

```text
ν_n definition:
n≥4

Toda (5.5) relations:
n≥5
```

Thus `ν₄` is a valid family definition instance, but the Phase 62 Toda (5.5) transport rule does not apply at `n=4`.

## Final aggregate

Phase 62 adds:

```text
Toda55NuFamilyFiniteDimensionalStatement
toda_55_nu_family_literature_statements()
toda_55_nu_family_finite_dimensional_integration_inference_rule()
```

The final aggregate preserves:

```text
ν-family definition
Toda Lemma 5.4 aggregate
n≥5
2ν_n=E^(n-3)ν′
4ν_n=η_n³
Toda (5.5) literature
```

Its direct provenance boundary is:

```text
Toda Lemma 5.4 aggregate  INFERENCE
ν-family definition       GIVEN
n≥5                       GIVEN
2ν_n relation             INFERENCE
4ν_n relation             INFERENCE
↓
Toda (5.5) aggregate      INFERENCE
```

Phase 60 literature remains inherited through the nested Lemma 5.4 aggregate.

## Non-circular provenance

The final aggregate is regression-tested to reach:

```text
Phase 62-3 double-value transport
Phase 62-4 quadruple-value bridge
Phase 60 Lemma 5.4
Phase 60 triple-η transport
Phase 58 2ν′ relation
```

The final aggregate is not an ancestor of itself or of either derived Toda (5.5) relation, and its final conclusion does not already occur among its ancestors.

## Representative probe

Run:

```powershell
python -m probes.probe_phase62_capabilities
```

The probe displays:

```text
Result
Proof-style derivation
Provenance / integration
Literature statements used
Phase 62 completion boundary
```

Representative machine checks include:

```text
Lemma 5.4 aggregate derived = True
nu-family definition is GIVEN = True
n>=5 applicability is GIVEN = True
2ν_n=E^(n-3)ν′ derived = True
Phase 60 triple-eta transport derived = True
4ν_n=η_n³ derived = True
final aggregate derived = True
final aggregate is GIVEN = False
theorem dependencies are INFERENCE = True
definition / applicability remain GIVEN = True
fixed point = True
```

The proof-style derivation remains a hand-authored presentation layer and is not automatic proof-text generation.

## Phase 62 focused tests

```text
tests/test_phase62_nu_family_definition.py               9 passed
tests/test_phase62_nu_family_double_transport.py        14 passed
tests/test_phase62_nu_family_eta_cube_bridge.py         13 passed
tests/test_phase62_applicability_provenance.py          17 passed
tests/test_phase62_toda55_integration.py                24 passed
tests/test_phase62_toda55_applicability_provenance.py   19 passed
tests/test_phase62_probe.py                             18 passed
```

Final repository-wide regression:

```text
3550 passed in 411.22s
```

## Phase 62 representation boundary

Phase 62 deliberately does not add:

```text
stable ν:=E^∞ν₄
stable 4ν=η³
stable homotopy-group model
generic ν-family framework
generic suspension exponent algebra
generic η-cube class
automatic proof narrative generation
Toda (5.6)
```


---

# Phase 63: Toda (5.6) ν₄ decomposition isomorphism

Phase 63 specializes the existing Toda Proposition 4.4 decomposition theorem to:

```text
n=4
α=ν₄
ν₄∈π_7^4
H(ν₄)=ι₇
```

The final capability is:

```text
Φ:
π_{i-1}^3 ⊕ π_i^7
→
π_i^4

Φ(α,β)=Eα+ν₄∘β

Φ is an isomorphism.
```

Equivalently:

```text
π_{i-1}^3 ⊕ π_i^7
≅
π_i^4

(α,β)↦Eα+ν₄∘β
```

## Phase 63 dependency

```text
Phase 47
Toda Proposition 4.4 decomposition semantics
+
Phase 60
Toda Lemma 5.4
ν₄∈π_7^4
H(ν₄)=ι₇
↓
Phase 63-2
n=4, α=ν₄ specialization premises
↓
Phase 63-3
concrete Proposition 4.4 decomposition specialization
↓
Phase 63-4
Toda (5.6) map / isomorphism semantics
↓
Phase 63-6
literature-aware final aggregate
```

Phase 63 deliberately does not add generic scalar normalization, generic membership normalization, a generic Proposition 4.4 specialization framework, or generic direct-sum simplification.

## Phase 63 provenance boundary

The theorem-side spine remains derived:

```text
ν₄ membership                         INFERENCE
H(ν₄)=ι₇                              INFERENCE
2Eν₄=E²ν′                             INFERENCE
Toda Lemma 5.4 aggregate              INFERENCE
ν₄ / Prop.4.4 specialization          INFERENCE
Prop.4.4 specialization isomorphism   INFERENCE
Toda (5.6) semantics                  INFERENCE
Toda (5.6) final aggregate            INFERENCE
```

The concrete decomposition-map instance remains structural input:

```text
TodaProp44DecompositionMap            GIVEN
```

This distinction is intentional:

```text
theorem knowledge
!=
structural map instance
```

Phase 63 provenance regression verifies ancestor reachability to Phase 60, rejection of GIVEN replacements for derived theorem results, and acyclicity of the final `ProofStep` graph.

## Phase 63 literature provenance

Direct literature:

```text
Toda (5.6)
Equation (5.6)
```

with statement:

```text
(α,β)↦Eα+ν₄∘β
:
π_{i-1}^3 ⊕ π_i^7 ≅ π_i^4
```

The Phase 60 Toda Lemma 5.4 literature is preserved as inherited provenance through the nested `lemma54_statement`.

## Phase 63 representative probe

```powershell
python -m probes.probe_phase63_capabilities
```

The probe displays:

```text
Result
Proof-style derivation
Provenance / integration
Literature statements used
Phase 63 completion boundary
```

Representative machine checks include:

```text
nu_4 membership derived = True
H(nu_4)=iota_7 derived = True
2E nu_4=E^2 nu-prime derived = True
Lemma 5.4 aggregate derived = True
nu_4 specialization derived = True
decomposition map is GIVEN = True
Prop.4.4 specialization isomorphism derived = True
Toda (5.6) semantics derived = True
final aggregate derived = True
final aggregate is GIVEN = False
theorem dependencies are INFERENCE = True
structural decomposition map remains GIVEN = True
fixed point = True
```

The proof-style derivation remains a hand-authored presentation layer and is not automatic proof-text generation.

## Phase 63 focused tests

```text
tests/test_phase63_nu4_prop44_specialization.py              15 passed
tests/test_phase63_prop44_decomposition_specialization.py    19 passed
tests/test_phase63_toda56_semantics.py                       17 passed
tests/test_phase63_applicability_provenance.py               20 passed
tests/test_phase63_toda56_integration.py                     19 passed
tests/test_phase63_probe.py                                  17 passed
```

Final repository-wide regression:

```text
3657 passed in 939.47s
```

## Phase 63 representation boundary

Phase 63 deliberately does not add:

```text
generic Proposition 4.4 specialization framework
generic scalar normalization
generic membership normalization
generic direct-sum simplification
stable ν:=E^∞ν₄
stable 4ν=η³
automatic proof narrative generation
later Toda consequences after Equation (5.6)
```

---


# Phase 64: performance stabilization

Phase 64 adds no new Toda theorem semantics. Its purpose is to reduce repository-wide regression time while preserving mathematical semantics, provenance, API behavior, and test coverage.

The optimization policy is:

```text
measure
↓
identify repeated work
↓
apply the minimum safe change
↓
same-machine before / after benchmark
↓
full regression
```

Absolute timings from different machines are not used as evidence of code-level optimization.

## Same-machine baseline

The Phase 64 current-machine baseline was:

```text
3657 passed in 259.11s
```

The final Phase 64 regression is:

```text
3657 passed in 29.97s
```

This is approximately an 88.4% reduction in full-regression time.

## Deterministic representative-builder caching

Phase 64 first identified deterministic no-argument test / probe builders that repeatedly reconstructed the same proof graph.

Where callers only inspect the returned graph and do not mutate it, these builders are cached with:

```text
lru_cache(maxsize=1)
```

Representative same-machine progression:

```text
259.11s
↓
150.42s
↓
81.79s
↓
43.54s
```

The cache preserves identity-based provenance checks because repeated consumers receive the same nested `ProofStep` graph.

No theorem semantics were changed.

## Inference-engine profiling

`cProfile` showed that premise matching, rather than duplicate-result classification, dominated representative inference cost.

Before the Phase 64-5 optimization, the Phase 63 representative profile included approximately:

```text
3,789,332 function calls
1.670s total

find_inference_matches
1.534s cumulative

find_all_matching_premises
0.792s cumulative

match_inference_rule_bindings
31,506 calls
0.364s cumulative
```

The recursive premise search already computed merged variable bindings, but those bindings were discarded and recomputed for the same premise assignment.

## Premise-binding rematch elimination

Phase 64 introduces the private helper:

```text
_find_all_matching_premise_bindings()
```

The recursive search now preserves:

```text
matched premises
+
merged variable bindings
```

and `find_inference_matches_for_rule()` reuses those bindings.

The public behavior of `find_all_matching_premises()` remains unchanged.

After the change, the Phase 63 representative profile became approximately:

```text
2,805,851 function calls
1.185s total
```

The representative inference path improved from approximately:

```text
1.670s
↓
1.185s
```

while preserving inference semantics and provenance.

## Algebra crosscheck optimization

After test/probe caching and the inference fix, the dominant remaining tests were:

```text
test_finite_exactness_presentation_crosscheck
test_finite_presentation_crosscheck
```

These tests intentionally compare:

```text
finite explicit enumeration
vs
presentation / integer-lattice calculation
```

Phase 64 does not reduce their mathematical coverage.

The exhaustive crosschecks now reuse already-computed values for the same map, including:

```text
image_subgroup()
image_lattice_basis()
kernel_lattice_basis()
shared kernel lattice used by kernel / image presentation calculations
```

The finite exactness crosscheck also precomputes the `f` image data and `g` kernel data once per map instead of recomputing them for every pair.

The final algebra regression is:

```text
109 passed in 7.46s
```

Representative final slow-test timings:

```text
test_finite_presentation_crosscheck
about 5.2s

test_finite_exactness_presentation_crosscheck
about 0.82s
```

The exhaustive group sets, matrix-entry ranges, and checked-count thresholds remain unchanged.

## Phase 64 completion boundary

Implemented:

```text
same-machine performance baseline
pytest duration profiling
deterministic builder caching
inference-engine profiling
premise-binding rematch elimination
algebra crosscheck repeated-enumeration elimination
algebra crosscheck lattice precomputation
final before / after regression measurement
```

Not implemented:

```text
agenda/worklist inference architecture
premise-type indexing
global proof-result cache
global GroupMap lattice cache
Smith normal form algorithm replacement
Hermite normal form algorithm replacement
parallel pytest requirement
test coverage reduction
new Toda theorem semantics
automatic proof narrative generation
```

Current mathematical frontier therefore remains Phase 63:

```text
π_{i-1}^3 ⊕ π_i^7
≅
π_i^4

(α,β)↦Eα+ν₄∘β
```

# Phase 65: Toda Proposition 5.6 finite-dimensional computation

Phase 65 completes the finite-dimensional part of Toda Proposition 5.6.

The final derived capability is:

```text
π_5^2 = Z/2{η₂³}
π_6^3 = Z/4{ν′}
π_7^4 = Z{ν₄} ⊕ Z/4{Eν′}
π_(n+3)^n = Z/8{ν_n}, n≥5
```

where:

```text
ν_n := E^(n-4)ν₄
```

for `n≥4`.

The Proposition 5.6 aggregate is not reintroduced as a `GIVEN`. Its finite-dimensional group relations are built from independently derived Phase 65 branches and stored as an `INFERENCE` result with explicit `ProofStep` provenance.

## π_5^2 branch

Phase 65 first combines Toda (5.2) with the already-derived η-family result to obtain:

```text
π_5^2 = Z/2{η₂³}
```

with:

```text
η₂³ = η₂∘η₃∘η₄.
```

## Equation (5.7) and π_6^3

Phase 65 derives the concrete Toda (5.7) consequence:

```text
H(ν′∘η₆)=η₅².
```

Together with:

```text
π_7^5=Z/2{η₅²}
```

this yields surjectivity of:

```text
H:π_7^3→π_7^5.
```

The relevant EHP exact sequence is displayed as one connected segment:

```text
π_7^3 ─H→ π_7^5 ─Δ→ π_5^2 ─E→ π_6^3 ─H→ π_6^5
```

Exactness gives:

```text
H surjective
↓
Δ=0
↓
E:π_5^2→π_6^3 injective.
```

Using the independently derived relations:

```text
2ν′=η₃³
ord(η₃³)=2
```

Phase 65 obtains:

```text
ord(ν′)=4
π_6^3=Z/4{ν′}.
```

No generic exact-order solver is introduced.

## π_7^4 decomposition

Toda (5.6), specialized to `i=7`, gives:

```text
π_6^3 ⊕ π_7^7 ≅ π_7^4
(α,β) ↦ Eα+ν₄∘β.
```

Using:

```text
π_6^3=Z/4{ν′}
π_7^7=Z{ι₇}
```

Phase 65 derives:

```text
π_7^4=Z{ν₄}⊕Z/4{Eν′}.
```

## n=5 branch

From Toda (5.6), Phase 65 derives:

```text
π_8^5 / E²π_6^3 ≅ Z/2
E²:π_6^3→π_8^5 injective.
```

Since:

```text
π_6^3=Z/4{ν′}
```

injectivity gives:

```text
ord(E²ν′)=4.
```

The `n=5` specialization of Toda (5.5) gives:

```text
2ν₅=E²ν′,
```

hence:

```text
ord(ν₅)=8.
```

Combining the order-four image with the order-two quotient yields:

```text
|π_8^5|=8,
```

and therefore:

```text
π_8^5=Z/8{ν₅}.
```

No generic quotient-cardinality solver is introduced.

## n≥6 transport

Toda (4.5) transports the `n=5` result:

```text
E^(n-5):π_8^5 ≅ π_(n+3)^n.
```

Phase 65 first derives:

```text
π_(n+3)^n
=
Z/8{E^(n-5)ν₅}.
```

The ν-family definition gives the dedicated bridge:

```text
E^(n-5)ν₅=ν_n.
```

Thus:

```text
π_(n+3)^n=Z/8{ν_n}
(n≥6).
```

Together with the concrete `n=5` branch:

```text
π_(n+3)^n=Z/8{ν_n}
(n≥5).
```

## Proposition 5.6 aggregate

The final finite-dimensional aggregate stores:

```text
π_5^2=Z/2{η₂³}
π_6^3=Z/4{ν′}
π_7^4=Z{ν₄}⊕Z/4{Eν′}
π_8^5=Z/8{ν₅}
π_(n+3)^n=Z/8{ν_n}, n≥6
n≥6 scope
Toda Proposition 5.6 literature metadata
```

The final aggregate itself is:

```text
ProofRule.INFERENCE
```

and its theorem dependencies remain derived.

## Representative proof-style probe

Run:

```powershell
python -m probes.probe_phase65_capabilities
```

The probe displays:

```text
Result
Proof-style derivation
EHP exact sequence used
Provenance / integration
Literature statements used
Phase 65 completion boundary
```

The EHP sequence is intentionally kept connected:

```text
π_7^3 ─H→ π_7^5 ─Δ→ π_5^2 ─E→ π_6^3 ─H→ π_6^5
```

The proof-style derivation is still hand-authored presentation code. It is not yet generated automatically from the `ProofStep` graph.

## Provenance meaning

The current system does more than replay a textual proof order.

Given explicit facts and already-formalized inference rules, the engine searches applicable rules and constructs new `ProofStep` objects until the selected inference stage reaches a fixed point.

Each derived step stores:

```text
conclusion
premises
inference rule
```

so the proof graph can be traced backward from the final conclusion.

However, this proof graph is currently in-memory unless reconstructed by the test / probe builder. A later program invocation normally performs the inference again.

`@lru_cache(maxsize=1)` is used for deterministic expensive builders so repeated use inside the same Python process does not reconstruct the same proof graph.

Persistent proof-result storage remains deferred.

## Phase 65 regression

Focused probe / provenance regression:

```text
tests/test_phase65_probe.py        21 passed
tests/test_phase65_provenance.py   12 passed
```

Final repository-wide regression:

```text
3841 passed in 31.82s
```

Phase 64 performance stabilization therefore remains effective while the Phase 65 theorem/test coverage is added.

## Phase 65 completion boundary

Implemented:

```text
Toda Proposition 5.6 finite-dimensional branch
π_5^2=Z/2{η₂³}
Equation (5.7) consequence
E:π_5^2→π_6^3 injectivity
ord(ν′)=4
π_6^3=Z/4{ν′}
π_7^4=Z{ν₄}⊕Z/4{Eν′}
π_8^5/E²π_6^3≅Z/2
E² injectivity
ord(ν₅)=8
π_8^5=Z/8{ν₅}
Toda (4.5) transport
π_(n+3)^n=Z/8{ν_n}, n≥5
finite-dimensional Proposition 5.6 aggregate
representative proof-style probe
full provenance regression
```

Deferred:

```text
stable ν
stable 4ν=η³
stable (G_3;2)=Z/8{ν}
Equation (5.8)
automatic proof narrative generation
persistent Proof Repository / Derived Fact Database
```

---


# Phase 69: Toda Equation (5.10)

Phase 69 implements the concrete source equation:

```text
Δ(ι₁₁)=ν₅η₈
```

The implementation deliberately reuses the Phase 68 derived branches directly rather than treating the Proposition 5.8 aggregate as a new `GIVEN` prerequisite.

## Concrete Δ-E exactness and surjectivity

The structural EHP segment is:

```text
π_11^11 --Δ--> π_9^5 --E--> π_10^6
```

The structural window remains `GIVEN`. Phase 69 derives the concrete Proposition 4.2 exactness statement as `INFERENCE`.

Phase 68 already derived:

```text
π_10^6=0
```

so:

```text
E:π_9^5→π_10^6 = 0
↓
ker(E)=π_9^5
↓ exactness
Im(Δ)=π_9^5
↓
Δ:π_11^11→π_9^5 is surjective
```

The surjectivity result is `INFERENCE`.

## Generator consequence

The source group is retained as a foundational fact:

```text
π_11^11=Z{ι₁₁}
GIVEN
```

Phase 68 independently derived:

```text
π_9^5=Z/2{ν₅η₈}
INFERENCE
```

Together with Δ-surjectivity:

```text
Δ:π_11^11→π_9^5
surjective
INFERENCE
```

Phase 69 derives:

```text
Δ(ι₁₁)=ν₅η₈
INFERENCE
```

Since the target is order two, the possible sign is immaterial.

## Provenance / non-circularity

The final direct premises are exactly:

```text
Δ surjective              INFERENCE
π_11^11=Z{ι₁₁}           GIVEN
π_9^5=Z/2{ν₅η₈}          INFERENCE
```

Regression verifies:

```text
final is INFERENCE
final is not GIVEN
final is not its own ancestor
final conclusion is absent from ancestors
Δ-surjective branch does not depend on final
π_9^5 branch does not depend on final
Phase 68 aggregate is not a direct premise
Phase 68 aggregate is not an ancestor of final
```

The Phase 68 aggregate is therefore not used as a shortcut prerequisite.

## Representation boundary

Phase 69 adds only theorem-specific rules required by Equation (5.10):

```text
toda_eq510_concrete_delta_e_exactness_inference_rule()
toda_eq510_delta_surjective_inference_rule()
toda_eq510_delta_iota11_inference_rule()
```

It does not add:

```text
generic concrete-dimension normalizer
generic exactness solver
generic cyclic-image solver
generic zero-target solver
generic sign / ± algebra
stable (G_4;2)=0
automatic proof narrative generation
persistent Proof Repository
```

The target generator object from the Phase 68 `π_9^5` branch is reused directly instead of rebuilding a display-equivalent expression.

## Representative probe

Run:

```powershell
python -m probes.probe_phase69_capabilities
```

The probe displays:

```text
Toda Equation (5.10) result
Proof-style derivation
EHP exact sequence used
Provenance / integration
Literature / source
Related previously derived result
Phase 69 representative probe boundary
```

Toda Equation (5.11):

```text
Δ(η₉)=Eν′η₇
```

was already derived in Phase 68 and is not reimplemented in Phase 69.

The proof-style derivation remains hand-authored presentation code. It is not yet generated automatically from the `ProofStep` graph.

## Phase 69 regression

Focused Phase 69 suite:

```text
79 passed in 1.53s
```

Representative probe test:

```text
22 passed in 1.18s
```

Final repository-wide regression:

```text
4422 passed in 30.54s
```

Phase 64 performance stabilization therefore remains effective while Phase 69 theorem and provenance coverage is added.

## Phase 69 completion boundary

Implemented:

```text
Toda Equation (5.10)
π_11^11 --Δ--> π_9^5 --E--> π_10^6 concrete exactness
Δ:π_11^11→π_9^5 surjective
π_11^11=Z{ι₁₁} foundational source fact
π_9^5=Z/2{ν₅η₈} Phase 68 derived branch reuse
Δ(ι₁₁)=ν₅η₈
applicability / provenance / non-circularity regression
representative proof-style probe
formal proof record
```

Still deferred:

```text
stable (G_4;2)=0
generic concrete-dimension normalization
generic exactness solver
generic cyclic-image / zero-target solver
generic sign / ± algebra
automatic proof narrative generation
persistent Proof Repository
stable homotopy-group model
```

---


# Phase 70: Toda Proposition 5.9 finite-dimensional result

Phase 70 implements the finite-dimensional part of Toda Proposition 5.9.

The final capability is:

```text
π_7^2=Z/2{η₂ν′η₆}

π_8^3=Z/2{ν′η₆²}

π_9^4
=
Z/2{ν₄η₇²}
⊕
Z/2{Eν′η₇²}

π_10^5=Z/2{ν₅η₈²}

π_11^6=Z{Δι₁₃}

π_(n+5)^n=0
(n≥7)
```

The stable conclusion:

```text
(G_5;2)=0
```

is not included in Phase 70.

## Phase 70 branch structure

Phase 70 is implemented as separate derived branches before final integration.

```text
Phase 70-2
π_7^2=Z/2{η₂ν′η₆}

Phase 70-3
π_8^3=Z/2{ν′η₆²}

Phase 70-4
π_9^4=
Z/2{ν₄η₇²}
⊕
Z/2{Eν′η₇²}

Phase 70-5
Δ(η₉²)=Eν′η₇²
E:π_9^4→π_10^5 surjective

Phase 70-6
π_10^5=Z/2{ν₅η₈²}

Phase 70-7
E(ν₅η₈²)=0
Δ(η₁₁)=ν₅η₈²

Phase 70-8
π_11^6=Z{Δι₁₃}

Phase 70-9
π_12^7=0
π_(n+5)^n=0, n≥7

Phase 70-10
Toda Proposition 5.9 aggregate integration

Phase 70-11
provenance / non-circular regression

Phase 70-12
representative proof-style probe
```

## π_10^5 derivation

Phase 70 derives:

```text
π_9^4
=
Z/2{ν₄η₇²}
⊕
Z/2{Eν′η₇²}
```

and:

```text
Δ(η₉²)=Eν′η₇².
```

Thus the second direct summand is the kernel contribution for suspension.

Together with:

```text
E:π_9^4→π_10^5
surjective
```

and:

```text
E(ν₄η₇²)=ν₅η₈²
```

Phase 70 obtains:

```text
π_10^5=Z/2{ν₅η₈²}.
```

## π_11^6 derivation

Phase 70-7 derives:

```text
E(ν₅η₈²)=0.
```

Since:

```text
π_10^5=Z/2{ν₅η₈²},
```

the concrete E-H exactness branch implies:

```text
H:π_11^6→π_11^11
```

is injective.

Phase 69 and the previous finite-dimensional branch provide:

```text
π_11^11=Z{ι₁₁}
π_9^5=Z/2{ν₅η₈}
Δ(ι₁₁)=ν₅η₈.
```

Therefore:

```text
ker(
  Δ:π_11^11→π_9^5
)
=
Z{2ι₁₁}.
```

The concrete Toda Proposition 2.7 consequence gives:

```text
H(Δι₁₃)=±2ι₁₁.
```

Hence:

```text
π_11^6=Z{Δι₁₃}.
```

The later result:

```text
π_12^7=0
```

is not used as a premise for this calculation.

## Higher five-stem zero

From:

```text
π_13^13=Z{ι₁₃}
π_11^6=Z{Δι₁₃}
```

Phase 70 obtains:

```text
Δ:π_13^13→π_11^6
surjective.
```

Using concrete Δ-E and E-H exactness together with:

```text
π_12^13=0,
```

the suspension map:

```text
E:π_11^6→π_12^7
```

is both zero and surjective. Therefore:

```text
π_12^7=0.
```

Toda (4.5) then gives:

```text
E^(n-7):
π_12^7
≅
π_(n+5)^n
```

for `n≥7`, so:

```text
π_(n+5)^n=0
(n≥7).
```

## Proposition 5.9 aggregate

Phase 70 adds:

```text
TodaProp59FiniteDimensionalStatement
```

and integrates exactly these direct premises:

```text
π_7^2 relation                INFERENCE
π_8^3 relation                INFERENCE
π_9^4 relation                INFERENCE
π_10^5 relation               INFERENCE
π_11^6 relation               INFERENCE
π_(n+5)^n=0                   INFERENCE
n≥7                           GIVEN
```

The aggregate itself is:

```text
ProofRule.INFERENCE
```

and is not reintroduced as a `GIVEN`.

## Provenance / non-circularity

Phase 70-11 verifies:

```text
final aggregate is INFERENCE
final aggregate is not GIVEN

all six mathematical branches are INFERENCE
n≥7 remains GIVEN

final direct premise count = 7
final reaches all six branches
final is not its own ancestor
final conclusion is absent from ancestors
branches do not depend on final
```

The principal machine dependency order is:

```text
π_7^2
→
π_8^3
→
π_9^4
→
π_10^5
→
π_11^6
→
π_12^7=0
→
π_(n+5)^n=0.
```

Supporting results are prevented from flowing backward.

For example:

```text
Phase 70-5 E-surjectivity
→ π_10^5
but not → π_9^4

Phase 70-7 E(ν₅η₈²)=0
→ π_11^6
but not → π_10^5

Phase 70-7 Δ(η₁₁)=ν₅η₈²
is not used to derive π_10^5
and is not used to derive π_11^6.
```

Thus:

```text
source ordering
!=
machine proof dependency
```

remains explicit.

## Structural identity boundary

During Phase 70, a concrete compatibility issue appeared between display names such as:

```text
η_9
η₉
```

The final rule guards do not use display-name equality as mathematical identity.

They validate the relevant structural data instead:

```text
dimension
source
target
GeneratorSymbol
expression tree
```

This preserves the existing rule:

```text
structural equality
!=
mathematical equality
```

without introducing a generic η-name normalizer.

## Representative probe

Run:

```powershell
python -m probes.probe_phase70_capabilities
```

The probe displays:

```text
Toda Proposition 5.9 finite-dimensional result
Proof-style derivation
Provenance / integration
Literature statements used
Phase 70 representative probe boundary
```

Representative proof-style sections include:

```text
π_10^5
π_11^6
higher five-stem zero
```

The probe explicitly states:

```text
The proof-style derivation above is hand-authored presentation code.
It is not yet generated automatically from the ProofStep graph.
```

## Phase 70 regression

Phase 70-12 probe:

```text
29 passed in 1.52s
```

Phase 70 aggregate + provenance + probe:

```text
93 passed in 1.65s
```

Final repository-wide regression:

```text
4752 passed in 30.85s
```

Phase 64 performance stabilization remains effective while Proposition 5.9 theorem, provenance, and probe coverage are added.

## Phase 70 completion boundary

Implemented:

```text
π_7^2=Z/2{η₂ν′η₆}
π_8^3=Z/2{ν′η₆²}
π_9^4=Z/2{ν₄η₇²}⊕Z/2{Eν′η₇²}
Δ(η₉²)=Eν′η₇²
E:π_9^4→π_10^5 surjective
π_10^5=Z/2{ν₅η₈²}
E(ν₅η₈²)=0
Δ(η₁₁)=ν₅η₈²
π_11^6=Z{Δι₁₃}
π_12^7=0
π_(n+5)^n=0, n≥7
TodaProp59FiniteDimensionalStatement
applicability / provenance / non-circularity regression
representative proof-style probe
formal proof record
```

Still deferred:

```text
stable (G_5;2)=0
generic concrete-dimension normalization
generic exactness solver
generic cyclic-image / zero-target solver
generic zero-map solver
generic zero-group isomorphism transport
generic sign / ± algebra
generic η-name normalization
automatic proof narrative generation
persistent Proof Repository
stable homotopy-group model
```


---

# Phase 71: Toda Equation (5.12) Delta injectivity

Toda (5.12) states:

```text
Δ:
π_(n+7)^(2n+1)
→
π_(n+5)^n

is injective for n=4,5,6.
```

Phase 71 formalizes the three concrete cases independently and then integrates them into one literature-aware aggregate.

## n=4 branch

Phase 71 reuses:

```text
Toda Proposition 5.3:
π_11^9=Z/2{η₉²}

Phase 70:
π_9^4
=
Z/2{ν₄η₇²}
⊕
Z/2{Eν′η₇²}

Δ(η₉²)=Eν′η₇²
```

Therefore the nonzero generator of the source maps to a nonzero order-two direct-summand generator in the target:

```text
Δ:
π_11^9
→
π_9^4

injective.
```

The final statement is:

```text
TodaDeltaInjectiveStatement
```

with:

```text
source = π_11^9
target = π_9^4
```

and is derived as `ProofRule.INFERENCE`.

## n=5 branch

Phase 71 reuses:

```text
Toda Proposition 5.1:
π_12^11=Z/2{η₁₁}

Phase 70:
π_10^5=Z/2{ν₅η₈²}
Δ(η₁₁)=ν₅η₈²
```

Hence:

```text
Δ:
π_12^11
→
π_10^5

injective.
```

The source family is specifically the Proposition 5.1 higher η-family, not Proposition 5.3.

The final statement is again:

```text
TodaDeltaInjectiveStatement
```

and is derived as `ProofRule.INFERENCE`.

## n=6 branch

Phase 71 reuses:

```text
π_13^13=Z{ι₁₃}       GIVEN
π_11^6=Z{Δι₁₃}       INFERENCE
```

Since the source free generator maps to the target free generator:

```text
ι₁₃
↦
Δι₁₃
```

the map:

```text
Δ:
π_13^13
→
π_11^6
```

is injective.

This branch deliberately does not use the already-derived Phase 70 surjectivity statement as a premise. The two free-cyclic group facts suffice directly.

## Toda (5.12) aggregate

Phase 71 adds:

```text
Toda512DeltaInjectivityStatement
toda_512_delta_injectivity_literature_statements()
toda_512_delta_injectivity_integration_inference_rule()
```

The aggregate stores exactly:

```text
n=4:
Δ:π_11^9→π_9^4 injective

n=5:
Δ:π_12^11→π_10^5 injective

n=6:
Δ:π_13^13→π_11^6 injective
```

Its direct provenance boundary is:

```text
n=4 injectivity  INFERENCE
n=5 injectivity  INFERENCE
n=6 injectivity  INFERENCE
↓
Toda (5.12) aggregate  INFERENCE
```

Literature metadata:

```text
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Equation (5.12)
```

## Phase 71 provenance / non-circularity

Dedicated regression verifies:

```text
aggregate direct premises
=
exactly the n=4,n=5,n=6 injectivity steps

aggregate reaches all three branches

each branch reaches its own upstream facts

aggregate is not its own ancestor

aggregate conclusion does not occur in its ancestors

each branch is acyclic

no branch depends on another Phase 71 branch

no branch depends on the final aggregate
```

The `GIVEN` / `INFERENCE` boundary is preserved:

```text
n=4 upstream = INFERENCE
n=5 upstream = INFERENCE

n=6:
π_13^13 = GIVEN
π_11^6  = INFERENCE
```

Wrong map, wrong generator, wrong group, wrong order, and inappropriate `GIVEN` substitutions are rejected by the Phase 71 focused tests.

## Representative probe

Run:

```powershell
python -m probes.probe_phase71_capabilities
```

The probe displays:

```text
Toda (5.12) Delta injectivity
Proof-style derivation
Provenance / integration
Literature statements used
Phase 71 representative probe boundary
```

The displayed proof-style derivation is hand-authored presentation code.

It is not yet generated automatically from the `ProofStep` graph.

## Phase 71 regression

Focused / staged results include:

```text
Phase 71-2 n=4:
19 passed

Phase 71-3 n=5:
20 passed

Phase 71-4 n=6:
19 passed

Phase 71-5 integration:
19 passed

Phase 71-6 provenance:
30 passed

Phase 71-7 probe:
27 passed
```

Latest repository-wide regression:

```text
4886 passed in 29.25s
```

Phase 64 performance stabilization remains effective while the Phase 71 theorem, provenance, literature, and probe coverage are added.

## Phase 71 completion boundary

Implemented:

```text
TodaDeltaInjectiveStatement
Toda512DeltaInjectivityStatement

Δ:π_11^9→π_9^4 injective
Δ:π_12^11→π_10^5 injective
Δ:π_13^13→π_11^6 injective

Toda (5.12) three-case integration
literature-aware aggregate
applicability regression
provenance / non-circularity regression
representative proof-style probe
sixth formal proof record
```

Still deferred:

```text
Toda Lemma 5.10
generic Toda-bracket coset algebra
generic modulo-subgroup bracket normalization
generic cyclic-map injectivity solver
generic free-cyclic map solver
automatic proof narrative generation
persistent Proof Repository
stable homotopy-group model
```

---

# Phase 72: Toda Lemma 5.10

Phase 72 formalizes the concrete Toda Lemma 5.10 conclusion:

```text
Δ(ι₁₃)
∈
{ν₆,η₉,2ι₁₀}
mod 2π₁₁(S⁶)
```

The implementation deliberately avoids a generic Toda-bracket coset algebra. The theorem is represented and inferred with narrow Phase 72 statements and rules only.

## Phase 72 representation

Minimum statement representation:

```text
TodaLemma510BracketModuloStatement
```

with fields representing:

```text
element
bracket
ambient_group
modulus
```

For Lemma 5.10 this is:

```text
element       = Δ(ι₁₃)
bracket       = {ν₆,η₉,2ι₁₀}
ambient_group = π₁₁(S⁶)
modulus       = 2
```

No generic `Coset`, generic modulo-subgroup normalizer, or generic quotient theorem layer is added.

## Phase 72 core proof integration

Toda's proof is represented by two main branches before final modulo integration.

Hopf / exactness branch:

```text
Phase 69 / Toda (5.10)
Δ(ι₁₁)=ν₅η₈

+ Proposition 2.6 consequence
↓
H{ν₆,η₉,2ι₁₀} contains 2ι₁₁

Phase 70
H(Δι₁₃)=±2ι₁₁

+ E-H exactness
π₁₀(S⁵) --E--> π₁₁(S⁶) --H--> π₁₁(S¹¹)
↓
Δι₁₃ ∈ {ν₆,η₉,2ι₁₀} + Eπ₁₀(S⁵)
```

The first draft of Phase 72-3 incorrectly used Phase 71 n=6 Delta injectivity as a direct prerequisite. After the full Toda proof was supplied, Phase 72-3 was revised so that Phase 71 injectivity is not part of the Lemma 5.10 ancestry.

## Phase 72 indeterminacy / modulo integration

Toda bracket indeterminacy branch:

```text
Phase 59 / Proposition 5.3
π₁₁⁹=Z/2{η₉²}

Phase 68
ν₆η₉=0

Phase 70
π₁₁⁶=Z{Δι₁₃}
↓
Indeterminacy
=ν₆∘π₁₁⁹ + 2π₁₁⁶
=2π₁₁⁶
```

Suspension-image branch:

```text
Phase 70
π₁₀⁵=Z/2{ν₅η₈²}
π₁₁⁶=Z{Δι₁₃}
↓
Eπ₁₀(S⁵) ⊂ 2π₁₁(S⁶)
```

Final integration:

```text
Δι₁₃ ∈ bracket + Eπ₁₀(S⁵)
Indeterminacy = 2π₁₁(S⁶)
Eπ₁₀(S⁵) ⊂ 2π₁₁(S⁶)
↓
Δι₁₃
∈
{ν₆,η₉,2ι₁₀}
mod 2π₁₁(S⁶)
```

The final statement is `ProofRule.INFERENCE`, not `GIVEN`.

## Phase 72 provenance / non-circularity

Dedicated regression verifies:

```text
final direct premises
= exactly core / indeterminacy / suspension-image branches

Phase 59 provenance reachable
Phase 68 ν₆η₉=0 reachable
Phase 69 Δι₁₁=ν₅η₈ reachable
Phase 70 H(Δι₁₃)=±2ι₁₁ reachable
Phase 70 E-H exactness reachable
Phase 70 π₁₀⁵ / π₁₁⁶ reachable

Phase 71 n=6 Delta injectivity reachable = False

final graph acyclic
final conclusion absent from ancestors
three direct branch graphs acyclic
GIVEN shortcut rejected
wrong bracket / modulus / group / indeterminacy generator / suspension map rejected
```

## Representative probe

Run:

```powershell
python -m probes.probe_phase72_capabilities
```

The probe displays:

```text
Toda Lemma 5.10 result
Proof-style derivation
Representative source objects
Provenance / integration
Phase 72 representative probe boundary
```

It explicitly reports:

```text
final modulo statement derived = True
final modulo statement is GIVEN = False
core branch derived = True
indeterminacy branch derived = True
suspension-image branch derived = True
exact three direct premises = True
final graph acyclic = True
Phase 71 Delta injectivity absent from ancestry = True
```

The proof-style derivation remains hand-authored presentation code. It is not yet generated automatically from the `ProofStep` graph.

## Phase 72 regression

Focused / staged results include:

```text
Phase 72-2 minimum statement:
10 passed

Phase 72-3 initial core:
16 passed

Phase 72-3 revised proof-faithful core:
19 passed

Phase 72-4 modulo / indeterminacy integration:
22 passed

Phase 72-5 provenance / non-circularity:
31 passed

Phase 72-6 representative probe:
22 passed
```

Latest repository-wide regression on the home laptop:

```text
4990 passed in 70.11s
```

Wall-clock regression time is tracked per machine because the project is developed on two PCs.

## Phase 72 completion boundary

Implemented:

```text
TodaLemma510BracketModuloStatement
TodaLemma510HopfBracketContainsStatement
TodaLemma510BracketPlusSuspensionImageStatement
TodaLemma510SuspensionImageInDoubleStatement

toda_lemma510_hopf_bracket_contains_inference_rule()
toda_lemma510_exactness_core_inference_rule()
toda_lemma510_indeterminacy_inference_rule()
toda_lemma510_suspension_image_in_double_inference_rule()
toda_lemma510_modulo_integration_inference_rule()

Toda Lemma 5.10 end-to-end inference
applicability regression
provenance / non-circularity regression
representative proof-style probe
seventh formal proof record
```

Still deferred:

```text
generic Toda-bracket coset algebra
generic modulo-subgroup bracket normalization
generic quotient normalization
generic finite-subgroup solver
automatic proof narrative generation
persistent Proof Repository
stable homotopy-group model
higher Toda brackets unless concretely required
```

---

# Documentation

- `README.md` — current capabilities and status
- `docs/design.md` — current architecture, semantics, and boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capability dependency
- `docs/code_reference.md` — module responsibilities and major classes / functions

---

# Next development boundary

Phase 72 is complete.

The next mathematical Phase is:

```text
Phase 73
Toda Proposition 5.11
The group π_(n+6)^n
```

Source targets:

```text
ν_n² := ν_n∘ν_(n+3),  n≥4

π_8^2  = Z/2{η₂ν′η₆²}
π_9^3  = 0
π_10^4 = Z/8{ν₄²}
π_(n+6)^n = Z/2{ν_n²},  n≥5
(G_6;2)=Z/2{ν²}
```

Start with:

```text
Phase 73-1
source statement / proof dependency / representation compatibility analysis
```

The proof introduces the intermediate Toda Equation (5.13):

```text
Δ(ν₉)=±2ν₄²
Δ(η₁₁²)=0
Δ(η₁₃)=0
```

Before implementation, inspect the current representations for `ν_n²`, the Phase 72 Lemma 5.10 result, Proposition 2.5 composition with Delta, Proposition 1.4 bracket composition, and the n=4,5,6 EHP exactness branches.

The following remain separate later milestones:

```text
automatic proof narrative generation
persistent Proof Repository
stable homotopy branch
higher Toda brackets beyond concrete need
```
