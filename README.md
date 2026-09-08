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

Completed through Phase 62.

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
```

Latest repository-wide regression:

```text
3550 passed in 411.22s
```

Phase 62 focused / applicability / provenance / integration / probe regression has been verified.

Representative current probe:

```powershell
python -m probes.probe_phase62_capabilities
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

# Documentation

- `README.md` — current capabilities and status
- `docs/design.md` — current architecture, semantics, and boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capability dependency
- `docs/code_reference.md` — module responsibilities and major classes / functions

---

# Next development boundary

Phase 62 is complete.

The next mathematical target is:

```text
Phase 63
Toda (5.6) ν₄ decomposition
```

Target:

```text
(α,β)
↦
Eα+ν₄∘β
:
π_{i-1}^3 ⊕ π_i^7
≅
π_i^4
```

The intended dependency is:

```text
Phase 47
Toda Proposition 4.4 decomposition semantics
+
Phase 60
ν₄∈π_7^4
H(ν₄)=ι₇
↓
n=4, α=ν₄ specialization
↓
Toda (5.6)
```

Phase 63 should reuse the existing Proposition 4.4 decomposition infrastructure and add only the minimum ν₄ specialization required by Toda (5.6). Stable ν / η³, generic sign solving, generic Toda-bracket algebra, automatic proof narrative generation, and theorem-repository infrastructure remain deferred until concrete need.
