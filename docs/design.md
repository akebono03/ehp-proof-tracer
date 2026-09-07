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

Phase 45–52 でも generic inference engine は変更していない。

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

# 22. Phase 51 dependency-analysis design

Phase 51 is analysis-only. No production-code representation or inference rule is added.

Finite-dimensional Proposition 5.1 target:

```text
π_3^2=Z{η₂}
π_{n+1}^n=Z/2{η_n}  (n≥3)
H(η₂)=ι₃
Δ(ι₅)=±2η₂
```

Toda p.39 has an internal notation inconsistency between the proof text and the printed proposition line. The proof text uses `Δ(ι₅)=±2η₂`, which is compatible with the target group `π_3^2`; this is the development target.

Existing independent dependencies:

```text
Phase 49:
π_3^2=Z{η₂}
H(η₂)=ι₃

Phase 50:
π_4^3=Z/2{η₃}
[ι₂,ι₂]=±2η₂
Δ(ι₅)=±[ι₂,ι₂]

Phase 46:
Toda (4.5) stable-range E^(m-n) isomorphism
```

No additional low-dimensional group table is required.

---

# 23. Phase 51 missing-edge boundary

Minimum missing implementation:

```text
1. specific direct bridge
   Δ(ι₅)=±[ι₂,ι₂]
   +
   [ι₂,ι₂]=±2η₂
   ↓
   Δ(ι₅)=±2η₂

2. finite cyclic transport through Toda (4.5)
   π_4^3=Z/2{η₃}
   +
   E^(n-3): π_4^3 ≅ π_{n+1}^n
   ↓
   π_{n+1}^n=Z/2{E^(n-3)η₃}

3. η-family-specific suspension bridge
   E^(n-3)η₃=η_n

4. finite-dimensional Proposition 5.1 integration
   with provenance / circular-dependency rejection
```

The direct Δ bridge must remain theorem-specific. Do not add general up-to-sign transitivity or a sign solver.

The finite-cyclic transport should be scoped to the concrete Toda (4.5) need. Do not add a generic isomorphism-transport framework unless later phases require it.

The higher η bridge should remain η-family-specific. Do not normalize arbitrary `Suspension` / `IteratedSuspension` expressions.

---

# 24. Circular dependency policy for Proposition 5.1

Safe premises:

```text
Phase 49 proof-derived H(η₂)=ι₃
Phase 49 π_3^2=Z{η₂}
Phase 50 π_4^3=Z/2{η₃}
Toda Proposition 2.7 minimum consequence
Toda Proposition 4.2 exactness
Toda (4.5) stable-range isomorphism
η-family definition
```

Unsafe as Proposition 5.1 premises:

```text
old literature GIVEN H(η₂)=ι₃ attributed to Proposition 5.1
old Phase 35–36 proof traces that depend on that GIVEN fact
```

Phase 35–38 inference machinery may later be reused only after replacing the old Proposition-5.1 GIVEN provenance with the independently derived Phase 49 result.

---

# 25. Deferred stable boundary

The stable conclusion

```text
(G_1;2)=Z/2{η}
```

is intentionally deferred. No stable homotopy-group model is introduced for the finite-dimensional Proposition 5.1 branch.

The composition isomorphism following Proposition 5.1, equation (5.2), is also outside the current proof target.

---

# 26. Phase 52 direct-bridge design

Target:

```text
Δ(ι₅)=±[ι₂,ι₂]
+
[ι₂,ι₂]=±2η₂
↓
Δ(ι₅)=±2η₂
```

No new statement class is required. Reuse:

```text
TodaDeltaImageUpToSignStatement
TodaPi32WhiteheadSquareUpToSignStatement
```

The target is represented by the existing `TodaDeltaImageUpToSignStatement` with:

```text
map = Δ : π_5^5 → π_3^2
element = ι₅
positive_value = 2η₂
```

Specific inference rule:

```text
toda_delta_iota5_two_eta2_up_to_sign_inference_rule()
```

The guard requires the exact Toda instance:

```text
source = π_5^5
target = π_3^2
element = ι₅
first positive value = [ι₂,ι₂]
Whitehead-square statement = [ι₂,ι₂]=±2η₂
```

Therefore the rule is not a generic transitivity principle for up-to-sign equalities.

Invalid cases are rejected for:

```text
wrong Δ source
wrong Δ target
wrong element
wrong Whitehead square
wrong coefficient
wrong η-family index
```

Integration policy:

```text
existing Phase 50 image rule remains unchanged
+
Phase 52 direct bridge is added in parallel
```

Thus round 3 contains both:

```text
Δ(ι₅)=±2η₂
Im(Δ)=Z{2η₂}
```

Representative counts:

```text
given = 11
derived = 10
rounds = 6
fixed point = True
```

Provenance requirement:

```text
Δ(ι₅)=±[ι₂,ι₂]  INFERENCE
[ι₂,ι₂]=±2η₂     INFERENCE
↓
Δ(ι₅)=±2η₂       INFERENCE
```

The generic inference engine remains unchanged.

Phase 52 full regression:

```text
2731 passed in 26.67s
```

---

# 27. Phase 53 finite-cyclic transport 設計

目的:

```text
π_4^3=Z/2{η₃}
+
E^(n-3): π_4^3 ≅ π_{n+1}^n
↓
π_{n+1}^n=Z/2{E^(n-3)η₃}
```

既存表現だけを再利用する。

```text
Toda45IsomorphismStatement
TodaIteratedSuspensionMap
FiniteCyclicGroup
IteratedSuspension
Relation
```

新しい transport 用 group class や generic isomorphism transport framework は追加しない。

Specific rule:

```text
toda_45_pi4_3_finite_cyclic_transport_inference_rule()
```

適用対象は次に限定する。

```text
source group relation = π_4^3=Z/2{η₃}
Toda (4.5) source sphere = 3
source degree = 4 または既存 Phase 46 の ScalarSum(3,1)
target = π_{n+1}^n
exponent = n-3 の既存 symbolic tree
```

`ScalarSum(3,1)` と concrete `4` の差は、この specific `π_4^3` guard 内だけで受理する。generic scalar normalization は導入しない。

Generator transport は:

```text
η₃
↓
IteratedSuspension(η₃,n-3)
```

までとする。

```text
E^(n-3)η₃=η_n
```

への接続は Phase 54 の責務であり、Phase 53 では行わない。

---

# 28. Phase 53 stable-range / applicability 設計

Toda (4.5) の stable range は Phase 46 の責務を維持する。

```text
stable-range premises
+
TodaIteratedSuspensionMap
↓
Toda45IsomorphismStatement
```

Phase 53 rule 自体は inequality を再評価せず、導出済み `Toda45IsomorphismStatement` を premise とする。

現在の scalar inequality は structural representation であり、一般の数値 inequality solver は導入しない。

Phase 53 で reject を固定した対象:

```text
wrong stable-range structure
wrong suspension-range instance
wrong source sphere
wrong source degree
wrong target degree
wrong exponent
wrong source group
wrong cyclic order
wrong generator
```

---

# 29. Phase 53 integration / provenance 設計

Phase 50 の最終 result を GIVEN として再投入しない。

同一 fixed-point run 内で:

```text
Phase 50 premises
↓
π_4^3=Z/2{η₃}  INFERENCE

Phase 46 stable-range premises
↓
Toda45IsomorphismStatement  INFERENCE

両者
↓
π_{n+1}^n=Z/2{E^(n-3)η₃}  INFERENCE
```

transport step の2 premise は両方とも `ProofRule.INFERENCE` であることを要求する。

Representative counts:

```text
given = 14
derived = 11
rounds = 7
fixed point = True
```

Full regression:

```text
2769 passed in 25.60s
```

Generic inference engine は変更していない。

---

# 30. 次の設計境界

Phase 53 は完了。

次の実装順序:

```text
Phase 54  E^(n-3)η₃=η_n bridge
Phase 55  Proposition 5.1 finite-dimensional integration / provenance
```

Phase 54 では、higher η-family の定義

```text
η_n=E^(n-2)η₂  (n>=3)
```

と `η₃=Eη₂` を使い、必要な η-family-specific bridge だけを追加する。

先取りしない:

```text
generic suspension normalization
generic iterated-suspension composition algebra
generic generator transport
stable homotopy model
```
