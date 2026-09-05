# EHP Proof Tracer 設計

この文書は EHP Proof Tracer の current architecture、semantics、design boundary を記録する。

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

重要な区別:

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

Phase 45–49 でも generic inference engine は変更していない。

---

# 3. Expression layer

主要 expression:

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

必要な数学的同値は proof-level statement / `Relation` として導出する。

---

# 4. Scalar-expression layer

minimum scalar tree:

```text
ScalarExpression
├── ScalarSymbol
├── ScalarSum
├── ScalarProduct
└── ScalarPower
```

`ScalarValue` により integer / symbolic scalar expression を共通に扱う。

general-purpose CAS は導入しない。

---

# 5. Symbolic homotopy group layer

Toda Chapter 4 で用いる主な group structures:

```text
PrimaryComponent
TodaPrimaryGroup
PreimageSubgroup
FreeCyclicGroup
DirectSumGroup
```

representatives:

```text
PrimaryComponent(i,n,p)
→ π_i(S^n;p)

TodaPrimaryGroup(i,n)
→ π_i^n

FreeCyclicGroup(α)
→ Z{α}
```

これらは concrete `AbelianGroup` calculation layer とは別。

---

# 6. WhiteheadProduct and Toda Lemma 4.1

`WhiteheadProduct(left,right)` により:

```text
[ι_{n-1},ι_{n-1}]
```

を structural に保持する。

Whitehead zero / nonzero premise:

```text
RelationType.ZERO
RelationType.INEQUALITY
```

Toda Lemma 4.1 は:

```text
n odd
n even + Whitehead nonzero
n even + Whitehead zero
```

の3ケースを domain rules で分離する。

zero case では同じ premises から:

```text
π_{2n-1}^n = Z{α} ⊕ π_{2n-1}(S^n;2)
H(α)=ι_{2n-1}
Eα ∈ π_{2n}(S^{n+1};2)
```

を別々の rules で導出する。

generic `InferenceRule` は 1 rule = 1 conclusion を維持する。

---

# 7. Canonical EHP maps

canonical symbolic map terms:

```text
EHP_E_MAP
EHP_H_MAP
EHP_DELTA_MAP
```

これらは `MapSymbol`。

意味:

```text
EHP_E_MAP     → E
EHP_H_MAP     → H
EHP_DELTA_MAP → Δ
```

symbolic source / target typing は `MapSymbol` 自体には持たせない。

---

# 8. Instance-aware Toda maps

specific source / target instance が必要な場合、generic `MapSymbol` と分離して Toda-specific map object を用いる。

現在:

```text
TodaSuspensionMap
├── source_group: TodaPrimaryGroup
└── target_group: TodaPrimaryGroup

TodaHopfInvariantMap
├── source_group: TodaPrimaryGroup
└── target_group: TodaPrimaryGroup

TodaDeltaMap
├── source_group: TodaPrimaryGroup
└── target_group: TodaPrimaryGroup
```

重要:

```text
TodaSuspensionMap != EHP_E_MAP
TodaHopfInvariantMap != EHP_H_MAP
TodaDeltaMap != EHP_DELTA_MAP
```

generic operation symbol と specific theorem instance を混同しない。

---

# 9. TodaEHPSequence

```text
TodaEHPSequence
├── terms
└── maps
```

representative:

```text
π_i^n
-E→
π_{i+1}^{n+1}
-H→
π_{i+1}^{2n+1}
-Δ→
π_{i-1}^n
-E→
π_i^{n+1}
```

重要:

```text
TodaEHPSequence
!= exactness theorem
```

sequence object に theorem truth を埋め込まない。

---

# 10. TodaEHPExactnessWindow

```text
TodaEHPExactnessWindow
├── source_term
├── middle_term
├── target_term
├── first_map
└── second_map
```

目的:

```text
A --f→ B --g→ C
```

を source / middle / target instance を失わず保持する。

重要:

```text
TodaEHPExactnessWindow
!= ExactnessStatement
```

and:

```text
window representation
!= exactness theorem
```

---

# 11. Toda Proposition 4.2 theorem semantics

instance-aware theorem result:

```text
TodaProp42ExactnessStatement(window)
```

rules:

```text
toda_prop42_e_h_exactness_inference_rule()
toda_prop42_h_delta_exactness_inference_rule()
toda_prop42_delta_e_exactness_inference_rule()
```

valid windows:

```text
E-H
H-Δ
Δ-E
```

rule guard は map order と symbolic dimension structure を確認する。

---

# 12. Generic exactness bridge

```text
toda_prop42_exactness_to_generic_inference_rule()
```

conclusion:

```text
ExactnessStatement(
  first_map=window.first_map,
  second_map=window.second_map,
  is_exact=True,
)
```

これは intentionally instance-lossy。

したがって:

```text
TodaProp42ExactnessStatement
=
authoritative instance-aware theorem
```

generic projection は existing generic zero-composition machinery を再利用するための bridge。

---

# 13. Toda (4.5)

Phase 46 で stable-range iterated suspension isomorphism を instance-aware に表現。

```text
E^(m-n):
π_{n+k}^n
→
π_{m+k}^m
```

condition:

```text
n ≥ k+2
m ≥ n
```

conclusion:

```text
Toda45IsomorphismStatement
```

generic `IsomorphismStatement(MapSymbol)` への自動 bridge は追加しない。

---

# 14. Toda Proposition 4.4 decomposition

Phase 47 の representation:

```text
TodaProp44DecompositionMap
```

source:

```text
π_{i-1}^{n-1}
⊕
π_i^{2n-1}
```

target:

```text
π_i^n
```

formula:

```text
Eβ+α∘γ
```

theorem statement:

```text
TodaProp44IsomorphismStatement
```

premises include:

```text
α ∈ π_{2n-1}^n
H(α)=±ι_{2n-1}
```

---

# 15. Toda Proposition 4.4 first-summand restriction

Phase 48 representation:

```text
TodaProp44FirstSummandRestrictionStatement
├── decomposition_map
└── suspension_map
```

意味:

```text
Φ|_{π_{i-1}^{n-1}}
=
E: π_{i-1}^{n-1} → π_i^n
```

一般的な direct-sum inclusion / projection machinery は導入しない。

---

# 16. Toda Proposition 4.4 suspension injectivity

statement:

```text
TodaProp44SuspensionInjectiveStatement
└── map: TodaSuspensionMap
```

meaning:

```text
E: π_{i-1}^{n-1} → π_i^n
is injective
```

rule:

```text
toda_prop44_suspension_injective_inference_rule()
```

premises:

```text
TodaProp44IsomorphismStatement
TodaProp44FirstSummandRestrictionStatement
```

same decomposition-map instance を guard で要求する。

重要:

```text
TodaProp44SuspensionInjectiveStatement
!= InjectiveMapStatement(EHP_E_MAP)
```

---

# 17. Phase 49 design objective

concrete target:

```text
π_3^2 = Z{η_2}
```

EHP fragment:

```text
π_2^1
-E→
π_3^2
-H→
π_3^3
-Δ→
π_1^1
-E→
π_2^2
```

Phase 49 の設計原則:

```text
concrete low-dimensional calculation
↓
minimum missing facts / theorem consequences
```

not:

```text
general map-property framework first
general existential framework first
```

---

# 18. Phase 49 low-dimensional fact layer

explicit facts:

```text
π_2^1 = 0
π_3^3 = Z{ι_3}
E: π_1^1 → π_2^2 is isomorphism
```

new statement structures:

```text
TodaPrimaryGroupZeroStatement
TodaSuspensionIsomorphismStatement
```

`π_3^3 = Z{ι_3}` は既存 `Relation` + `FreeCyclicGroup` で表現する。

fact providers:

```text
pi_2_1_zero_fact()
pi_3_3_free_cyclic_fact()
e_pi_1_1_to_pi_2_2_isomorphism_fact()
```

重要:

```text
TodaSuspensionIsomorphismStatement
!= IsomorphismStatement(EHP_E_MAP)
```

specific source / target instance を保持するため。

---

# 19. Phase 49 specific map-property layer

specific Toda map properties:

```text
TodaSuspensionInjectiveStatement
└── map: TodaSuspensionMap

TodaHopfInvariantInjectiveStatement
└── map: TodaHopfInvariantMap

TodaHopfInvariantSurjectiveStatement
└── map: TodaHopfInvariantMap

TodaHopfInvariantIsomorphismStatement
└── map: TodaHopfInvariantMap

TodaDeltaZeroStatement
└── map: TodaDeltaMap
```

これらは generic map-property types に自動変換しない。

---

# 20. Exactness + zero-left ⇒ H injective

rule:

```text
toda_exactness_zero_left_implies_hopf_injective_inference_rule()
```

premises:

```text
TodaPrimaryGroupZeroStatement(π_2^1)

TodaProp42ExactnessStatement(
  π_2^1 -E→ π_3^2 -H→ π_3^3
)
```

conclusion:

```text
TodaHopfInvariantInjectiveStatement(
  H: π_3^2 → π_3^3
)
```

guard checks:

```text
first_map = E
second_map = H
zero group = exactness source
```

---

# 21. E isomorphism ⇒ E injective

rule:

```text
toda_suspension_isomorphism_implies_injective_inference_rule()
```

premise:

```text
TodaSuspensionIsomorphismStatement(E-instance)
```

conclusion:

```text
TodaSuspensionInjectiveStatement(same E-instance)
```

Phase 48 の theorem-specific `TodaProp44SuspensionInjectiveStatement` とは別。

---

# 22. Δ-E exactness + E injective ⇒ Δ=0

rule:

```text
toda_exactness_injective_right_implies_delta_zero_inference_rule()
```

premises:

```text
TodaSuspensionInjectiveStatement(
  E: π_1^1 → π_2^2
)

TodaProp42ExactnessStatement(
  π_3^3 -Δ→ π_1^1 -E→ π_2^2
)
```

conclusion:

```text
TodaDeltaZeroStatement(
  Δ: π_3^3 → π_1^1
)
```

数学的意味:

```text
Im(Δ)=Ker(E)
E injective
↓
Ker(E)=0
↓
Δ=0
```

---

# 23. H-Δ exactness + Δ=0 ⇒ H surjective

rule:

```text
toda_exactness_zero_delta_implies_hopf_surjective_inference_rule()
```

premises:

```text
TodaDeltaZeroStatement(
  Δ: π_3^3 → π_1^1
)

TodaProp42ExactnessStatement(
  π_3^2 -H→ π_3^3 -Δ→ π_1^1
)
```

conclusion:

```text
TodaHopfInvariantSurjectiveStatement(
  H: π_3^2 → π_3^3
)
```

数学的意味:

```text
Im(H)=Ker(Δ)
Δ=0
↓
Ker(Δ)=π_3^3
↓
H surjective
```

---

# 24. H injective + surjective ⇒ H isomorphism

rule:

```text
toda_hopf_injective_surjective_implies_isomorphism_inference_rule()
```

premises:

```text
TodaHopfInvariantInjectiveStatement(H-instance)
TodaHopfInvariantSurjectiveStatement(H-instance)
```

conclusion:

```text
TodaHopfInvariantIsomorphismStatement(H-instance)
```

guard:

```text
injectivity.map == surjectivity.map
```

cross-instance mixing を reject する。

---

# 25. `η_2` theorem-derived definition

Phase 49 で最も重要な semantic boundary:

```text
η_2
!= initially GIVEN element
```

Instead:

```text
H: π_3^2 → π_3^3 is isomorphism
+
π_3^3 = Z{ι_3}
↓
ι_3 has a unique preimage under H
↓
denote it by η_2
```

statement:

```text
TodaPi32Eta2DefinitionStatement
├── map: TodaHopfInvariantMap
├── element: HomotopyElement
└── image: HomotopyElement
```

rule:

```text
toda_pi3_2_define_eta2_inference_rule()
```

The word "unique" is justified by the isomorphism premise:

```text
surjective → existence
injective → uniqueness
```

No general existential / witness / uniqueness engine is added.

---

# 26. `H(η_2)=ι_3`

rule:

```text
toda_pi3_2_eta2_hopf_relation_inference_rule()
```

premise:

```text
TodaPi32Eta2DefinitionStatement
```

conclusion:

```text
Relation(
  H(η_2),
  ι_3,
  EQUALITY,
)
```

This relation is theorem-derived from the definition.

It is not imported from the pre-existing Toda Prop.5.1 fact, avoiding circularity with the later theorem branch.

---

# 27. Generator transport

rule:

```text
toda_pi3_2_free_cyclic_generator_inference_rule()
```

premises:

```text
TodaHopfInvariantIsomorphismStatement(
  H: π_3^2 → π_3^3
)

π_3^3 = Z{ι_3}

TodaPi32Eta2DefinitionStatement(
  η_2 is the unique preimage of ι_3
)
```

conclusion:

```text
π_3^2 = Z{η_2}
```

This rule is intentionally concrete.

```text
specific generator transport for π_3^2
!= general cyclic-generator transport theorem
```

---

# 28. Phase 49 fixed-point integration

Initial GIVEN:

```text
1. π_2^1 = 0
2. π_3^3 = Z{ι_3}
3. E: π_1^1 → π_2^2 is isomorphism
4. E-H exact
5. H-Δ exact
6. Δ-E exact
```

rule set:

```text
toda_exactness_zero_left_implies_hopf_injective_inference_rule()
toda_suspension_isomorphism_implies_injective_inference_rule()
toda_exactness_injective_right_implies_delta_zero_inference_rule()
toda_exactness_zero_delta_implies_hopf_surjective_inference_rule()
toda_hopf_injective_surjective_implies_isomorphism_inference_rule()
toda_pi3_2_define_eta2_inference_rule()
toda_pi3_2_eta2_hopf_relation_inference_rule()
toda_pi3_2_free_cyclic_generator_inference_rule()
```

rounds:

```text
round 1
H injective
E injective

round 2
Δ=0

round 3
H surjective

round 4
H isomorphism

round 5
unique H-preimage of ι_3 named η_2

round 6
H(η_2)=ι_3
π_3^2=Z{η_2}

fixed point
```

counts:

```text
given = 6
derived = 8
round_count = 6
```

---

# 29. Phase 49 provenance policy

Every derived Phase 49 result uses:

```text
ProofRule.INFERENCE
```

and preserves:

```text
ProofStep.premises
ProofStep.inference_rule
```

No intermediate mathematical conclusion is silently inserted as `GIVEN`.

In particular:

```text
η_2 definition
H(η_2)=ι_3
π_3^2=Z{η_2}
```

are all inference-derived.

---

# 30. Phase 49 applicability policy

reject invalid cases including:

```text
wrong zero group
wrong exactness map order
cross-instance E map
cross-instance Δ map
cross-instance H injectivity / surjectivity
wrong π_3^3 target generator
wrong H source / target
```

The rules are deliberately narrow and do not attempt to solve arbitrary exact sequences.

---

# 31. Generic map-property boundary after Phase 49

generic API remains conceptually:

```text
InjectiveMapStatement(map: MapSymbol)
IsomorphismStatement(map: MapSymbol)
```

Phase 49 does not generalize that API to arbitrary typed maps.

Instead specific Toda statements retain source / target instances.

Important:

```text
instance-aware Toda theorem result
!= instance-lossy generic map property
```

---

# 32. Existential / uniqueness boundary

Phase 49 needs exactly one concrete naming step:

```text
ι_3 has a unique preimage under H;
denote it by η_2
```

Not implemented:

```text
ExistsStatement
UniqueExistsStatement
Witness
InverseMap
general named-witness introduction
general inverse-image selection
```

The dedicated `TodaPi32Eta2DefinitionStatement` is the minimum semantic structure for the concrete proof.

---

# 33. Phase 49 probe

executable:

```powershell
python -m probes.probe_phase49_capabilities
```

central output:

```text
H: π_3^2 → π_3^3 is injective
E: π_1^1 → π_2^2 is injective
Δ: π_3^3 → π_1^1 = 0
H: π_3^2 → π_3^3 is surjective
H: π_3^2 → π_3^3 is isomorphism
ι_3 has a unique preimage under H;
denote it by η₂
H(η₂) = ι_3
π_3^2 = Z{η₂}
```

fixed-point:

```text
round 1 new step count = 2
round 2 new step count = 1
round 3 new step count = 1
round 4 new step count = 1
round 5 new step count = 1
round 6 new step count = 2
fixed point = True
```

---

# 34. Phase 49 tests

focused:

```text
tests/test_phase49_concrete_pi3_2_compatibility.py  20 passed
tests/test_phase49_low_dimensional_facts.py         19 passed
tests/test_phase49_hopf_injectivity.py              21 passed
tests/test_phase49_delta_hopf_surjectivity.py       26 passed
tests/test_phase49_hopf_isomorphism.py              17 passed
tests/test_phase49_generator_transport.py           20 passed
tests/test_phase49_probe.py                         23 passed
```

related:

```text
tests/test_phase45_toda_prop42_theorem_semantics.py
16 passed
```

full:

```text
2557 passed in 56.45s
```

---

# 35. Phase 49 completion boundary

implemented:

```text
low-dimensional π_3^2 facts
instance-aware H map
instance-aware Δ map
specific E injectivity
specific H injectivity
specific Δ zero
specific H surjectivity
specific H isomorphism
η_2 theorem-derived definition
H(η_2)=ι_3
π_3^2=Z{η_2}
cross-instance rejection
provenance
representative probe
full regression
```

not implemented:

```text
general existential quantification
general witness / uniqueness system
general inverse-map machinery
general cyclic-generator transport
generic map-property type generalization
general symbolic dimension solver
symbolic map typing solver
stable homotopy group model
Toda Proposition 2.7
π_4^3 calculation
higher Toda brackets
```

---

# 36. 次の設計境界

次:

```text
Phase 50
concrete π_4^3 calculation
```

first step:

```text
Phase 50-1
π_4^3 proof dependency compatibility check
```

expected dependency:

```text
Toda Proposition 2.7
```

Phase 50 でも:

```text
actual concrete proof dependency
↓
minimum theorem semantics
```

を守る。

Toda Proposition 2.7 全体を先に general theorem catalogue として実装しない。
