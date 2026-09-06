# EHP Proof Tracer 設計

この文書は current architecture、semantics、design boundary を記録する。

historical な実装経緯は `docs/development_log.md`、将来構想は `docs/roadmap.md` に分離する。

---

# 1. 基本設計原則

```text
actual mathematical need
↓
minimum representation
↓
explicit fact / domain rule
↓
existing generic inference engine
```

generic inference engine に数学固有の theorem knowledge を埋め込まない。

```text
representation != typing != theorem knowledge
structural equality != mathematical equality
```

---

# 2. Layer separation

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

Phase 45–50 でも generic inference engine は変更していない。

---

# 3. Expression layer

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

constructor は theorem-aware normalization を行わない。

---

# 4. Symbolic homotopy group layer

```text
PrimaryComponent
TodaPrimaryGroup
PreimageSubgroup
FreeCyclicGroup
FiniteCyclicGroup
DirectSumGroup
```

`FiniteCyclicGroup(order,generator)` は Phase 50 で `Z/2{η₃}` を structural に保持するための minimum representation。

---

# 5. Canonical / instance-aware maps

Canonical:

```text
EHP_E_MAP
EHP_H_MAP
EHP_DELTA_MAP
```

Instance-aware:

```text
TodaSuspensionMap
TodaHopfInvariantMap
TodaDeltaMap
```

```text
specific theorem instance != generic MapSymbol
```

---

# 6. Toda Proposition 4.2

```text
TodaEHPSequence
TodaEHPExactnessWindow
TodaProp42ExactnessStatement
```

Rules:

```text
toda_prop42_e_h_exactness_inference_rule()
toda_prop42_h_delta_exactness_inference_rule()
toda_prop42_delta_e_exactness_inference_rule()
```

---

# 7. Toda Proposition 4.4

Phase 47:

```text
Φ:
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
→ π_i^n
Φ(β,γ)=Eβ+α∘γ
```

Phase 48:

```text
Φ is isomorphism
+
first-summand restriction = E
↓
E injective
```

---

# 8. Phase 49 design

Target:

```text
π_3^2=Z{η₂}
```

`η₂` は GIVEN にせず、H isomorphism による `ι_3` の一意な逆像として theorem-derived に定義する。

No general:

```text
ExistsStatement
UniqueExistsStatement
Witness
InverseMap
```

---

# 9. Phase 50 design objective

Target:

```text
π_4^3=Z/2{η₃}
```

Path:

```text
H([ι_2,ι_2])=±2ι_3
↓
[ι_2,ι_2]=±2η₂
↓
Δ(ι_5)=±[ι_2,ι_2]
↓
Im(Δ)=Z{2η₂}
↓
Ker(E)=Z{2η₂}
```

and:

```text
π_4^5=0
+
E-H exactness
↓
E surjective
```

then:

```text
π_3^2=Z{η₂}
+
Ker(E)=Z{2η₂}
+
E surjective
↓
π_4^3=Z/2{Eη₂}
```

finally:

```text
η₃=Eη₂
↓
π_4^3=Z/2{η₃}
```

---

# 10. Minimum Toda Proposition 2.7 semantics

Only:

```text
H([ι_2,ι_2])=±2ι_3
```

is implemented.

Statement:

```text
TodaProp27HopfInvariantUpToSignStatement
```

This is not a `Relation`; it stores unresolved sign in one theorem-specific statement.

---

# 11. Up-to-sign boundary

Phase 50 also uses:

```text
TodaPi32WhiteheadSquareUpToSignStatement
TodaDeltaImageUpToSignStatement
```

for:

```text
[ι_2,ι_2]=±2η₂
Δ(ι_5)=±[ι_2,ι_2]
```

No generic:

```text
PlusMinus
SignVariable
UpToSignEquality algebra
```

is added.

Sign is forgotten only after passing to generated subgroups:

```text
Z{±2η₂}=Z{2η₂}
```

---

# 12. Phase 50 low-dimensional facts

```text
π_5^5=Z{ι_5}
π_4^5=0
```

providers:

```text
pi_5_5_free_cyclic_fact()
pi_4_5_zero_fact()
```

---

# 13. Image / kernel / surjectivity bridge

Narrow symbolic statements:

```text
TodaDeltaImageFreeCyclicStatement
TodaSuspensionKernelFreeCyclicStatement
TodaSuspensionSurjectiveStatement
```

These are intentionally separate from concrete `GroupMap` subgroup references.

---

# 14. FiniteCyclicGroup

```text
FiniteCyclicGroup
├── order: int
└── generator: Expression
```

Used for:

```text
Z/2{Eη₂}
Z/2{η₃}
```

No general quotient simplifier or first-isomorphism theorem engine is added.

---

# 15. η-family notation

Definition:

```text
η_n=E^(n-2)η₂
```

represented by:

```text
TodaEtaFamilyDefinitionStatement
```

For `n=3` a dedicated bridge derives:

```text
η₃=Eη₂
```

Important:

```text
IteratedSuspension(η₂,1) != Suspension(η₂)
```

No generic suspension normalization is added.

---

# 16. Phase 50 fixed-point integration

```text
given = 11
derived = 9
rounds = 6
fixed point = True
```

Rounds:

```text
1: Prop.2.7 consequence, Δ up-to-sign, E surjective, η₃=Eη₂
2: [ι_2,ι_2]=±2η₂
3: Im(Δ)=Z{2η₂}
4: Ker(E)=Z{2η₂}
5: π_4^3=Z/2{Eη₂}
6: π_4^3=Z/2{η₃}
```

---

# 17. Provenance policy

Every derived Phase 50 conclusion uses:

```text
ProofRule.INFERENCE
```

and preserves:

```text
ProofStep.premises
ProofStep.inference_rule
```

Final `π_4^3=Z/2{η₃}` is not GIVEN.

---

# 18. Applicability policy

Reject:

```text
wrong H instance
wrong Δ instance
wrong exactness window
wrong kernel coefficient
wrong source generator
wrong target group
missing π_3^2 structure
wrong η-family index
```

Also reject accidental sign-specific equalities.

---

# 19. Generic engine boundary after Phase 50

Not added:

```text
general up-to-sign algebra
general quotient simplification
general first-isomorphism theorem engine
general suspension normalization
general symbolic map typing
general symbolic dimension solver
```

---

# 20. Testing principle

For each mathematical layer:

```text
representation
applicability
invalid cases
integration
provenance
representative probe
termination / scope
full regression
```

Phase 50 full regression:

```text
2703 passed in 65.69s
```

---

# 21. Documentation policy

```text
README.md = current capabilities / status
docs/design.md = current architecture / semantics / boundaries
docs/development_log.md = chronological implementation history
docs/roadmap.md = future dependency
```

---

# 22. Next design boundary

Phase 50 completes:

```text
π_3^2=Z{η₂}
↓
π_4^3=Z/2{η₃}
```

Natural next candidate:

```text
Toda Proposition 5.1 proof dependency analysis
```

First identify exact missing premises before adding new theorem semantics.
