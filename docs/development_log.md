# ehp_proof 開発記録

current specification は `README.md` / `docs/design.md` を優先する。

---

# Phase 1–27 概要

Phase 1–17 で abelian-group calculation、generic inference、EHP、ORDER、Suspension、Freudenthal、Composition、Hopf invariant、additive / homomorphism / subgroup / modulo / symbolic scalar / indeterminacy reasoning を整備。

Phase 18–27 で unstable Toda bracket、indexed notation、typed homotopy elements、structured generators、theorem / generator facts、actual η₃ / ν′ / ν₇ typing、および actual ε₃ Toda chain を実装。

### 状態

完了

---

# Phase 28–38 概要

Phase 28–29 で map injectivity / isomorphism / actual H facts を整備。

Phase 30–34 で Toda Prop.2.2、SmashProduct、Barratt–Hilton prerequisites、Toda Prop.3.1 theorem rules を実装。

Phase 35–38 で actual equality branch:

```text
H((2ι₂)η₂)=4ι₃
H(4η₂)=4ι₃
↓
H((2ι₂)η₂)=H(4η₂)
↓
Injective(H)
↓
(2ι₂)η₂=4η₂
```

を completion。

generic inference engine はこの branch で変更しなかった。

### 状態

完了

---

# Phase 39–44 概要

Phase 39:

```text
PrimaryComponent
```

Phase 40:

```text
TodaPrimaryGroup
```

Phase 41:

```text
PreimageSubgroup
```

Phase 42:

```text
WhiteheadProduct
```

Phase 43:

```text
Toda Lemma 4.1 zero / nonzero premise vocabulary
```

Phase 44:

```text
Toda Lemma 4.1 three-case theorem semantics
```

zero case では:

```text
π_{2n-1}^n = Z{α} ⊕ π_{2n-1}(S^n;2)
H(α)=ι_{2n-1}
Eα ∈ π_{2n}(S^{n+1};2)
```

まで推論可能にした。

### 状態

完了

---

# Phase 45 概要

Toda Proposition 4.2 の symbolic EHP exactness を instance-aware に実装。

追加:

```text
EHP_E_MAP
EHP_DELTA_MAP
TodaEHPSequence
TodaEHPExactnessWindow
TodaProp42ExactnessStatement
```

rules:

```text
toda_prop42_e_h_exactness_inference_rule()
toda_prop42_h_delta_exactness_inference_rule()
toda_prop42_delta_e_exactness_inference_rule()
toda_prop42_exactness_to_generic_inference_rule()
```

generic exactness bridge により既存 zero-composition reasoning と接続。

generic inference engine は変更なし。

### 状態

完了

---

# Phase 46 概要

Toda (4.5):

```text
n ≥ k+2
m ≥ n
↓
E^(m-n):
π_{n+k}^n
→
π_{m+k}^m
is isomorphism
```

を instance-aware symbolic theorem として実装。

### 状態

完了

---

# Phase 47 概要

Toda Proposition 4.4 decomposition:

```text
Φ:
π_{i-1}^{n-1}
⊕
π_i^{2n-1}
→
π_i^n
```

```text
Φ(β,γ)=Eβ+α∘γ
```

under:

```text
α ∈ π_{2n-1}^n
H(α)=±ι_{2n-1}
```

を representation + theorem semantics として実装。

### 状態

完了

---

# Phase 48 概要

Toda Proposition 4.4 consequence:

```text
Φ is isomorphism
Φ|_{π_{i-1}^{n-1}}=E
↓
E: π_{i-1}^{n-1} → π_i^n is injective
```

instance-aware suspension map:

```text
TodaSuspensionMap
```

restriction statement:

```text
TodaProp44FirstSummandRestrictionStatement
```

injectivity theorem:

```text
TodaProp44SuspensionInjectiveStatement
```

completion full suite:

```text
2411 passed in 58.16s
```

### 状態

完了

---

# Phase 49：concrete EHP calculation `π_3^2 = Z{η_2}`

目的:

Toda Proposition 4.2 の exactness infrastructure を具体的な低次ホモトピー群計算へ接続する。

対象:

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

最終目標:

```text
π_3^2 = Z{η_2}
```

---

## Phase 49-1：current exactness → injective / surjective compatibility check

production code 変更なし。

確認:

```text
InjectiveMapStatement(EHP_H_MAP)
IsomorphismStatement(EHP_E_MAP)
```

は generic に表現可能。

ただし generic map property は source / target group instance を保持しない。

また current generic API には:

```text
SurjectiveMapStatement
```

が存在しないことを確認。

`TodaProp42ExactnessStatement` は source / middle / target instance を保持する。

結論:

```text
Phase 49 concrete calculation では
instance-aware Toda-specific map properties を使う
```

追加:

```text
tests/test_phase49_concrete_pi3_2_compatibility.py
```

verified:

```text
20 passed
```

### 状態

完了

---

## Phase 49-2：low-dimensional facts

追加:

```text
TodaPrimaryGroupZeroStatement
TodaSuspensionIsomorphismStatement
```

追加 module:

```text
low_dimensional_facts.py
```

facts:

```text
π_2^1 = 0
π_3^3 = Z{ι_3}
E: π_1^1 → π_2^2 is isomorphism
```

specific E isomorphism は generic `IsomorphismStatement(EHP_E_MAP)` と distinct。

追加:

```text
tests/test_phase49_low_dimensional_facts.py
```

verified:

```text
19 passed
```

### 状態

完了

---

## Phase 49-3：exactness + zero-left ⇒ H injective

追加:

```text
TodaHopfInvariantMap
```

representative:

```text
H: π_3^2 → π_3^3
```

追加:

```text
TodaHopfInvariantInjectiveStatement
```

rule:

```text
toda_exactness_zero_left_implies_hopf_injective_inference_rule()
```

premises:

```text
π_2^1 = 0
π_2^1 -E→ π_3^2 -H→ π_3^3 exact
```

conclusion:

```text
H: π_3^2 → π_3^3 is injective
```

cross-instance zero group を reject。

追加:

```text
tests/test_phase49_hopf_injectivity.py
```

verified:

```text
21 passed
```

full suite:

```text
2471 passed in 68.78s
```

### 状態

完了

---

## Phase 49-4：E injective ⇒ Δ=0 ⇒ H surjective

追加:

```text
TodaDeltaMap
TodaSuspensionInjectiveStatement
TodaDeltaZeroStatement
TodaHopfInvariantSurjectiveStatement
```

rule 1:

```text
toda_suspension_isomorphism_implies_injective_inference_rule()
```

```text
E: π_1^1 → π_2^2 is isomorphism
↓
E injective
```

rule 2:

```text
toda_exactness_injective_right_implies_delta_zero_inference_rule()
```

```text
E injective
+
π_3^3 -Δ→ π_1^1 -E→ π_2^2 exact
↓
Δ: π_3^3 → π_1^1 = 0
```

rule 3:

```text
toda_exactness_zero_delta_implies_hopf_surjective_inference_rule()
```

```text
Δ=0
+
π_3^2 -H→ π_3^3 -Δ→ π_1^1 exact
↓
H: π_3^2 → π_3^3 is surjective
```

追加:

```text
tests/test_phase49_delta_hopf_surjectivity.py
```

verified:

```text
26 passed
```

full suite:

```text
2497 passed in 64.87s
```

### 状態

完了

---

## Phase 49-5：H injective + surjective ⇒ H isomorphism

追加:

```text
TodaHopfInvariantIsomorphismStatement
```

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

same H-map instance を guard で要求。

追加:

```text
tests/test_phase49_hopf_isomorphism.py
```

verified:

```text
17 passed
```

full suite:

```text
2514 passed in 92.67s
```

### 状態

完了

---

## Phase 49-6：minimum generator transport across isomorphism

重要な設計修正:

```text
η_2 を既知の GIVEN element として置かない
```

mathematical semantics:

```text
H: π_3^2 → π_3^3 is isomorphism
+
π_3^3 = Z{ι_3}
↓
ι_3 の逆像が一意に存在
↓
その一意な元を η_2 と命名
```

追加:

```text
TodaPi32Eta2DefinitionStatement
```

fields:

```text
map
element
image
```

rule:

```text
toda_pi3_2_define_eta2_inference_rule()
```

次:

```text
TodaPi32Eta2DefinitionStatement
↓
H(η_2)=ι_3
```

rule:

```text
toda_pi3_2_eta2_hopf_relation_inference_rule()
```

generator transport:

```text
H isomorphism
+
π_3^3 = Z{ι_3}
+
η_2 is the unique H-preimage of ι_3
↓
π_3^2 = Z{η_2}
```

rule:

```text
toda_pi3_2_free_cyclic_generator_inference_rule()
```

general existential / witness / inverse-map machinery は追加しない。

既存 Toda Prop.5.1 由来の `H(η_2)=ι_3` fact は premise に使わない。

追加:

```text
tests/test_phase49_generator_transport.py
```

verified:

```text
20 passed
```

full suite:

```text
2534 passed in 60.93s
```

### 状態

完了

---

## Phase 49-7：representative probe / full regression / completion

追加:

```text
probes/probe_phase49_capabilities.py
tests/test_phase49_probe.py
```

initial GIVEN:

```text
π_2^1 = 0
π_3^3 = Z{ι_3}
E: π_1^1 → π_2^2 is isomorphism

π_2^1 -E→ π_3^2 -H→ π_3^3 exact
π_3^2 -H→ π_3^3 -Δ→ π_1^1 exact
π_3^3 -Δ→ π_1^1 -E→ π_2^2 exact
```

end-to-end fixed point:

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

counts:

```text
given premise count = 6
derived step count = 8
derived round count = 6
fixed point = True
```

focused verified:

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

final full regression:

```text
2557 passed in 56.45s
```

### 状態

完了

---

# Phase 49 completion boundary

Phase 49 で完成:

```text
π_2^1 = 0
+
E-H exact
↓
H injective
```

```text
E: π_1^1 → π_2^2 isomorphism
↓
E injective
+
Δ-E exact
↓
Δ=0
```

```text
H-Δ exact
+
Δ=0
↓
H surjective
```

```text
H injective
+
H surjective
↓
H isomorphism
```

```text
H isomorphism
+
π_3^3=Z{ι_3}
↓
ι_3 の一意な逆像を η_2 と命名
↓
H(η_2)=ι_3
↓
π_3^2=Z{η_2}
```

generic inference engine:

```text
変更なし
```

generic map-property API:

```text
generalization なし
```

general existential framework:

```text
未導入
```

### 状態

COMPLETE

---

# 次の Phase

```text
Phase 50
concrete π_4^3 calculation
```

最初:

```text
Phase 50-1
π_4^3 proof dependency compatibility check
```

既知の次 dependency:

```text
Toda Proposition 2.7
```

方針:

```text
actual π_4^3 proof dependency
↓
minimum Toda Prop.2.7 semantics
↓
concrete calculation completion
```

Toda Proposition 2.7 全体の general theorem catalogue を先取りしない。
