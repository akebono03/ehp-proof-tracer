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

# Phase 39：PrimaryComponent minimum representation

追加:

```text
PrimaryComponent(group_dimension,sphere_dimension,prime)
```

representative:

```text
π_i(S^n;p)
```

structural group term として concrete `AbelianGroup`、membership、Toda group と分離。

verified:

```text
tests/test_phase39_primary_component.py
24 passed
```

### 状態

完了

---

# Phase 40：TodaPrimaryGroup minimum representation

追加:

```text
TodaPrimaryGroup(group_dimension,sphere_dimension)
```

representative:

```text
π_i^n
```

`PrimaryComponent` と distinct。

Toda (4.3) evaluated definition は未導入。

verified:

```text
tests/test_phase40_toda_primary_group.py
24 passed
```

### 状態

完了

---

# Phase 41：PreimageSubgroup minimum representation

追加:

```text
PreimageSubgroup(map,subgroup)
```

representative:

```text
E^-1(π_{2n}(S^{n+1};2))
```

membership equivalence や Toda (4.3) evaluation は未導入。

verified:

```text
tests/test_phase41_preimage_subgroup.py
36 passed
```

### 状態

完了

---

# Phase 42：WhiteheadProduct minimum representation

追加:

```text
WhiteheadProduct(left,right)
```

representative:

```text
[ι₄,ι₄]
```

structural distinction:

```text
WhiteheadProduct
!= Composition
!= SmashProduct
```

verified:

```text
tests/test_phase42_whitehead_product.py
36 passed

full suite
1831 passed
```

### 状態

完了

---

# Phase 43：Toda Lemma 4.1 premise minimum representation

追加:

```text
RelationType.INEQUALITY
```

zero premise:

```text
[ι₄,ι₄] = 0
```

nonzero premise:

```text
[ι₄,ι₄] != 0
```

important:

```text
premise representation
!= theorem case semantics
```

verified:

```text
tests/test_phase43_toda_lemma41_premise.py
32 passed

tests/test_relation_rules.py
50 passed

full suite
1863 passed
```

### 状態

完了

---

# Phase 44：Toda Lemma 4.1 case semantics

目的:

Toda Lemma 4.1 の3ケースを symbolic premise から theorem-derived group structure へ接続する。

---

## Phase 44-1：compatibility check

既存 infrastructure を確認。

利用可能:

```text
OddScalarStatement
EvenScalarStatement
TodaPrimaryGroup
PrimaryComponent
ScalarSymbol
ScalarSum
ScalarProduct
```

不足を確認:

```text
symbolic ι_{n-1}
symbolic free cyclic group
symbolic direct sum
```

production code 変更なし。

### 状態

完了

---

## Phase 44-2：odd case

追加:

```text
toda_lemma41_odd_case_inference_rule()
```

premise:

```text
n odd
```

conclusion:

```text
π_{2n-1}^n = π_{2n-1}(S^n;2)
```

### 状態

完了

---

## Phase 44-3：symbolic generator / group decomposition representation

変更:

```text
GeneratorSymbol.index
int | None
→ ScalarValue | None
```

変更:

```text
HomotopyElement.dimension
int
→ ScalarValue
```

追加:

```text
FreeCyclicGroup
DirectSumGroup
```

representable:

```text
ι_{n-1}
ι_{2n+1}
Z{P(ι_{2n+1})}
Z{α}
Z{...} ⊕ π_{2n-1}(S^n;2)
```

`source` / `target` symbolic typing は未導入。

### 状態

完了

---

## Phase 44-4：even + Whitehead nonzero case

追加:

```text
toda_lemma41_even_nonzero_case_inference_rule()
```

premises:

```text
n even
[ι_{n-1},ι_{n-1}] != 0
```

conclusion:

```text
π_{2n-1}^n
=
Z{P(ι_{2n+1})}
⊕
π_{2n-1}(S^n;2)
```

generic matcher を拡張せず `match_guard` を使用。

### 状態

完了

---

## Phase 44-5：even + Whitehead zero case

追加:

```text
toda_lemma41_even_zero_case_inference_rule()
```

premises:

```text
n even
[ι_{n-1},ι_{n-1}] = 0
```

conclusion:

```text
π_{2n-1}^n
=
Z{α}
⊕
π_{2n-1}(S^n;2)
```

当初の `α` は minimum generator structure のみ。

### 状態

完了

---

## Phase 44-6：provenance / applicability / representative probe

3主要 rule を同一 rule set で確認。

```text
odd
→ odd rule only

even + nonzero
→ nonzero rule only

even + zero
→ zero rule only
```

各 scenario:

```text
one derived group conclusion
one derived round
fixed point
exact premise provenance
```

追加:

```text
probes/probe_phase44_capabilities.py
```

この時点の full regression:

```text
1926 passed
```

### 状態

完了

---

## Phase 44-6a：α-condition representation compatibility check

Toda Lemma 4.1 zero case の α 条件:

```text
H(α)=ι_{2n-1}
Eα ∈ π_{2n}(S^{n+1};2)
```

について current representation を確認。

確認結果:

```text
H(α)=ι_{2n-1}
→ existing Relation + MapApplication(EHP_H_MAP,α) で lossless
```

```text
Eα ∈ π_{2n}(S^{n+1})
→ HomotopyGroupMembershipStatement で lossless
```

一方 2-primary membership を lossless に結ぶ statement が不足。

production code 変更なし。

verified:

```text
tests/test_phase44_toda_lemma41_case_semantics.py
73 passed

full suite
1936 passed
```

### 状態

完了

---

## Phase 44-6b：PrimaryComponent membership minimum representation

追加:

```text
PrimaryComponentMembershipStatement
├── element: Expression
└── component: PrimaryComponent
```

これにより:

```text
Eα ∈ π_{2n}(S^{n+1};2)
```

を lossless に表現可能。

既存 `PrimaryComponent` / `HomotopyGroupMembershipStatement` は変更しない。

verified:

```text
tests/test_phase44_toda_lemma41_case_semantics.py
80 passed

full suite
1943 passed
```

### 状態

完了

---

## Phase 44-6c：zero-case α conditions theorem semantics

追加:

```text
toda_lemma41_even_zero_h_alpha_inference_rule()
```

conclusion:

```text
H(α)=ι_{2n-1}
```

追加:

```text
toda_lemma41_even_zero_suspension_primary_inference_rule()
```

conclusion:

```text
Eα ∈ π_{2n}(S^{n+1};2)
```

既存 group rule と合わせて:

```text
same premises
├── π_{2n-1}^n = Z{α} ⊕ π_{2n-1}(S^n;2)
├── H(α)=ι_{2n-1}
└── Eα ∈ π_{2n}(S^{n+1};2)
```

を1 round で導出。

3 conclusion の `α` は structural equality で同一。

generic inference engine は変更しない。

verified:

```text
tests/test_phase44_toda_lemma41_case_semantics.py
88 passed

full suite
1951 passed
```

### 状態

完了

---

## Phase 44-6d：representative probe update / final regression

Phase 44 probe を zero-case α conditions まで拡張。

final regression:

```text
tests/test_phase44_toda_lemma41_case_semantics.py
94 passed

full suite
1957 passed in 75.54s
```

probe:

```powershell
python -m probes.probe_phase44_capabilities
```

正常完走。

### 状態

完了

---

## Phase 44-7：Phase 44 completion

Phase 44 completion status:

```text
tests/test_phase44_toda_lemma41_case_semantics.py
94 passed

full suite
1957 passed in 75.54s
```

### 状態

完了

---

# Phase 45：Toda Proposition 4.2 — 2-primary EHP exact sequence

目的:

Toda Proposition 4.2 の3つの exact sequence を symbolic `(i,n)` instance を保持したまま theorem-level に表現し、既存 generic exactness infrastructure に接続する。

対象:

```text
π_i^n
-E→
π_{i+1}^{n+1}
-H→
π_{i+1}^{2n+1}
```

```text
π_{i+1}^{n+1}
-H→
π_{i+1}^{2n+1}
-Δ→
π_{i-1}^n
```

```text
π_{i+1}^{2n+1}
-Δ→
π_{i-1}^n
-E→
π_i^{n+1}
```

---

## Phase 45-1：compatibility check

production code 変更なし。

確認:

```text
PrimaryComponent
→ symbolic dimensions を保持可能

TodaPrimaryGroup
→ symbolic dimensions を保持可能

PreimageSubgroup
→ existing structural group connection usable

ExactnessStatement
→ symbolic map pair は保持可能

EHPSegment
→ repository-backed concrete AbelianGroup / GroupMap layer
→ symbolic Toda theorem sequence に直接流用しない

EHP_H_MAP
→ existing canonical H

canonical symbolic E
→ 未実装

canonical symbolic P
→ 未実装

MapTypingFact
→ concrete int dimensions
```

verified:

```text
tests/test_phase45_toda_prop42_compatibility.py
18 passed

full suite
1975 passed in 66.68s
```

### 状態

完了

---

## Phase 45-2：2-primary EHP sequence minimum representation

追加:

```text
EHP_E_MAP
EHP_DELTA_MAP
```

existing:

```text
EHP_H_MAP
```

追加:

```text
TodaEHPSequence
├── terms
└── maps
```

invariant:

```text
len(terms) = len(maps) + 1
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

sequence は representation only。

```text
TodaEHPSequence
!= exactness theorem
```

Phase 45-1 の obsolete E absence test を削除。

verified:

```text
tests/test_phase45_toda_prop42_sequence.py
19 passed

tests/test_phase45_toda_prop42_compatibility.py
17 passed

full suite
1993 passed in 72.54s
```

### 状態

完了

---

## Phase 45-3：Prop.4.2 exactness-instance compatibility check

production code 変更なし。

確認:

```text
ExactnessStatement(E,H)
ExactnessStatement(H,Δ)
ExactnessStatement(Δ,E)
```

の3 position は区別可能。

一方:

```text
(i,n) の E-H
(j,m) の E-H
```

は generic `ExactnessStatement` 単体では区別不能。

理由:

```text
ExactnessStatement
=
map pair + is_exact

group triple / symbolic indices
=
保持しない
```

結論:

```text
position identification
✅

symbolic Prop.4.2 instance identification
❌
```

verified:

```text
tests/test_phase45_toda_prop42_exactness_compatibility.py
17 passed

full suite
2010 passed in 74.69s
```

### 状態

完了

---

## Phase 45-4：minimum Prop.4.2 exactness-instance representation

追加:

```text
TodaEHPExactnessWindow
├── source_term
├── middle_term
├── target_term
├── first_map
└── second_map
```

これにより:

```text
same E-H map pair
+
different group terms
```

を structural に区別可能。

3 windows:

```text
E-H
H-Δ
Δ-E
```

を `TodaEHPSequence` から lossless に構築可能。

重要:

```text
TodaEHPExactnessWindow
!= ExactnessStatement
```

and:

```text
window
!= exactness theorem
```

verified:

```text
tests/test_phase45_toda_prop42_exactness_instance.py
18 passed

full suite
2028 passed in 72.62s
```

### 状態

完了

---

## Phase 45-5：Toda Proposition 4.2 theorem semantics

追加:

```text
TodaProp42ExactnessStatement(window)
```

意味:

```text
the supplied instance-aware window is exact
by Toda Proposition 4.2
```

追加:

```text
toda_prop42_e_h_exactness_inference_rule()
toda_prop42_h_delta_exactness_inference_rule()
toda_prop42_delta_e_exactness_inference_rule()
```

各 rule は `match_guard` で:

```text
map order
symbolic group dimensions
```

を確認。

当初、test で `find_applicable_inference_rules()` を使い exactly-one rule を期待したため1 failure。

原因:

```text
find_applicable_inference_rules()
=
premise-pattern level candidate search

find_inference_match()
=
match_guard-aware actual inference match
```

3 rules は同じ premise type:

```text
TodaEHPExactnessWindow
```

を持つため pattern-level では3候補になる。

production code は変更せず、test を `find_inference_match()` ベースへ修正。

verified:

```text
tests/test_phase45_toda_prop42_theorem_semantics.py
16 passed

tests/test_toda_rules.py
66 passed

tests/test_ehp_rules.py
26 passed

full suite
2044 passed in 68.62s
```

### 状態

完了

---

## Phase 45-6：generic exactness bridge / representative probe / final regression

追加:

```text
toda_prop42_exactness_to_generic_inference_rule()
```

bridge:

```text
TodaProp42ExactnessStatement(window)
↓
ExactnessStatement(
  first_map=window.first_map,
  second_map=window.second_map,
  is_exact=True,
)
```

重要:

```text
TodaProp42ExactnessStatement
=
instance-aware authoritative theorem result
```

```text
ExactnessStatement
=
instance-lossy generic projection
```

existing generic EHP rule を再利用:

```text
E-H exact
→ H∘E = 0

H-Δ exact
→ Δ∘H = 0

Δ-E exact
→ E∘Δ = 0
```

representative end-to-end:

```text
TodaEHPExactnessWindow
↓
TodaProp42ExactnessStatement
↓
ExactnessStatement
↓
EHPZeroCompositionStatement
```

追加:

```text
probes/probe_phase45_capabilities.py
```

representative fixed-point:

```text
round 1
3 theorem exactness statements

round 2
3 generic exactness statements

round 3
3 zero-composition statements

fixed point
```

verified:

```text
tests/test_phase45_toda_prop42_bridge.py
16 passed

tests/test_phase45_toda_prop42_theorem_semantics.py
16 passed

tests/test_phase45_toda_prop42_exactness_instance.py
18 passed

tests/test_phase45_toda_prop42_exactness_compatibility.py
17 passed

tests/test_phase45_toda_prop42_sequence.py
19 passed

tests/test_phase45_toda_prop42_compatibility.py
17 passed

tests/test_toda_rules.py
66 passed

tests/test_ehp_rules.py
26 passed

tests/test_inference_rule_pattern.py
438 passed

full suite
2060 passed in 70.48s
```

probe:

```powershell
python -m probes.probe_phase45_capabilities
```

正常完走。

### 状態

完了

---

## Phase 45-7：Phase 45 completion

Phase 45 で完成:

```text
canonical symbolic E / H / Δ
TodaEHPSequence
TodaEHPExactnessWindow
TodaProp42ExactnessStatement
Toda Prop.4.2 E-H exactness semantics
Toda Prop.4.2 H-Δ exactness semantics
Toda Prop.4.2 Δ-E exactness semantics
instance-aware theorem exactness
guard-aware applicability
theorem provenance
Toda exactness → generic ExactnessStatement bridge
existing generic zero-composition reuse
3-round fixed-point integration
representative executable probe
full regression
```

generic inference engine:

```text
変更なし
```

Phase 45 completion status:

```text
full suite
2060 passed in 70.48s
```

### 状態

完了

---

# Phase 45 completion boundary

実装済み:

```text
π_i^n
-E→
π_{i+1}^{n+1}
-H→
π_{i+1}^{2n+1}
is exact
```

```text
π_{i+1}^{n+1}
-H→
π_{i+1}^{2n+1}
-Δ→
π_{i-1}^n
is exact
```

```text
π_{i+1}^{2n+1}
-Δ→
π_{i-1}^n
-E→
π_i^{n+1}
is exact
```

with generic consequences:

```text
H∘E = 0
Δ∘H = 0
E∘Δ = 0
```

未実装:

```text
symbolic map typing solver
general symbolic dimension solver
automatic symbolic image/kernel group construction
instance-aware generic ExactnessStatement
Toda (4.5)
Toda Prop.4.4
Toda Prop.4.4 E injectivity consequence
stable homotopy
general Whitehead algebra
automatic Whitehead zero / nonzero solver
general existential witness machinery
higher Toda brackets
```

---

# 次の Phase

```text
Phase 46 candidate
Toda (4.5)
stable-range E^(m-n) isomorphism
```

実装前 compatibility check:

```text
IteratedSuspension
map isomorphism representation
TodaPrimaryGroup
symbolic scalar inequality representation
symbolic domain / codomain compatibility
Toda (4.5) exact statement
```

Phase 46 でも:

```text
actual mathematical need
↓
compatibility check
↓
minimum representation
↓
theorem rule
↓
existing generic inference engine
```

を維持する。

Toda Prop.4.4 は先取りしない。


---

# Phase 46：Toda (4.5) stable-range E^(m-n) isomorphism

目的:

Toda (4.5):

```text
n ≥ k+2
m ≥ n
```

のもとで:

```text
E^(m-n):
π_{n+k}^n
→
π_{m+k}^m
```

が isomorphism であることを、symbolic instance を保持した theorem semantics として表現する。

Toda Prop.4.4 は Phase 46 では先取りしない。

---

## Phase 46-1：Toda (4.5) compatibility check

production code 変更なし。

確認:

```text
TodaPrimaryGroup
→ n+k / m+k symbolic dimensions を保持可能

ScalarSum / ScalarProduct
→ n+k / m+k / m-n を structural に保持可能

IteratedSuspension.exponent
→ symbolic ScalarValue を保持可能

IteratedSuspension
→ element-level expression
→ map-level source / target は保持しない

IsomorphismStatement
→ map: MapSymbol のみ
→ source / target Toda group instance を保持しない

MapTypingFact
→ concrete int dimensions

n ≥ k+2 / m ≥ n
→ current scalar statement では未表現
```

focused:

```text
tests/test_phase46_toda_45_compatibility.py
18 passed
```

Phase 46-2 実装後、greater-equal absence test 1件を obsolete として削除。

最終:

```text
tests/test_phase46_toda_45_compatibility.py
17 passed
```

### 状態

完了

---

## Phase 46-2：stable-range premise minimum representation

追加:

```text
ScalarGreaterEqualStatement
├── left: ScalarValue
└── right: ScalarValue
```

representable:

```text
n ≥ k+2
m ≥ n
```

important:

```text
inequality representation
!= inequality solver
```

`evaluate()` / `is_true` / `solve()` は追加しない。

verified:

```text
tests/test_phase46_toda_45_stable_range_premise.py
11 passed

tests/test_scalar_rules.py
18 passed
```

この時点の full regression:

```text
2088 passed in 72.56s
```

### 状態

完了

---

## Phase 46-3：E^(m-n) map / source-target minimum representation

追加:

```text
TodaIteratedSuspensionMap
├── exponent: ScalarValue
├── source_group: TodaPrimaryGroup
└── target_group: TodaPrimaryGroup
```

representative:

```text
E^(m-n):
π_{n+k}^n
→
π_{m+k}^m
```

important:

```text
TodaIteratedSuspensionMap
!= IteratedSuspension
!= MapSymbol
```

constructor は dimension compatibility を solve しない。

verified:

```text
tests/test_phase46_toda_45_suspension_map.py
15 passed

tests/test_phase46_toda_45_compatibility.py
17 passed

tests/test_phase46_toda_45_stable_range_premise.py
11 passed

tests/test_phase40_toda_primary_group.py
24 passed

tests/test_phase45_toda_prop42_sequence.py
19 passed

tests/test_phase45_toda_prop42_exactness_instance.py
18 passed

tests/test_phase33_barratt_hilton.py
73 passed

full suite
2103 passed in 69.58s
```

### 状態

完了

---

## Phase 46-4：Toda (4.5) isomorphism theorem semantics

追加:

```text
Toda45IsomorphismStatement
└── map: TodaIteratedSuspensionMap
```

追加:

```text
toda_45_isomorphism_inference_rule()
```

premises:

```text
n ≥ k+2
m ≥ n
E^(m-n): π_{n+k}^n → π_{m+k}^m
```

conclusion:

```text
Toda45IsomorphismStatement(map)
```

`match_guard` で:

```text
k+2
m ≥ n relation
source π_{n+k}^n
target π_{m+k}^m
exponent m-n
```

の同一 symbolic instance を確認。

general inequality evaluation は行わない。

verified:

```text
tests/test_phase46_toda_45_theorem_semantics.py
14 passed

tests/test_phase46_toda_45_compatibility.py
17 passed

tests/test_phase46_toda_45_stable_range_premise.py
11 passed

tests/test_phase46_toda_45_suspension_map.py
15 passed

tests/test_toda_rules.py
66 passed

tests/test_inference_rule_pattern.py
438 passed

full suite
2117 passed in 68.55s
```

### 状態

完了

---

## Phase 46-5：applicability / invalid cases / provenance / generic isomorphism compatibility

production code 変更なし。

確認:

```text
valid instance
→ exactly one Toda45IsomorphismStatement

missing premise
→ reject

different n / k / m instance
→ reject

derived theorem
→ all three premises preserved

derived theorem
→ inference_rule preserved

one-round fixed point
```

generic compatibility:

```text
IsomorphismStatement.map
=
MapSymbol

InjectiveMapStatement.map
=
MapSymbol

TodaIteratedSuspensionMap
!= MapSymbol
```

したがって:

```text
Toda45IsomorphismStatement
→ IsomorphismStatement
```

bridge は Phase 46 では追加しない。

generic injectivity consequence も追加しない。

verified:

```text
tests/test_phase46_toda_45_applicability_compatibility.py
16 passed

tests/test_phase46_toda_45_compatibility.py
17 passed

tests/test_phase46_toda_45_stable_range_premise.py
11 passed

tests/test_phase46_toda_45_suspension_map.py
15 passed

tests/test_phase46_toda_45_theorem_semantics.py
14 passed

tests/test_map_property_rules.py
26 passed

tests/test_map_facts.py
54 passed

tests/test_toda_rules.py
66 passed

tests/test_inference_rule_pattern.py
438 passed

full suite
2133 passed in 73.15s
```

### 状態

完了

---

## Phase 46-6：representative probe / final regression

追加:

```text
probes/probe_phase46_capabilities.py
```

追加:

```text
tests/test_phase46_toda_45_probe.py
```

representative output:

```text
n ≥ k+2
m ≥ n

E^(m-n): π_{n+k}^{n} → π_{m+k}^{m}

E^(m-n): π_{n+k}^{n} → π_{m+k}^{m} is isomorphism
```

provenance / fixed point:

```text
theorem isomorphism count = 1
premise count = 3
derived round count = 1
fixed point = True
```

verified:

```text
tests/test_phase46_toda_45_probe.py
10 passed

tests/test_phase46_toda_45_applicability_compatibility.py
16 passed

tests/test_phase46_toda_45_theorem_semantics.py
14 passed

tests/test_phase46_toda_45_suspension_map.py
15 passed

tests/test_phase46_toda_45_stable_range_premise.py
11 passed

tests/test_phase46_toda_45_compatibility.py
17 passed

tests/test_toda_rules.py
66 passed

tests/test_map_property_rules.py
26 passed

tests/test_inference_rule_pattern.py
438 passed

full suite
2143 passed in 64.31s
```

probe:

```powershell
python -m probes.probe_phase46_capabilities
```

正常完走。

### 状態

完了

---

## Phase 46-7：Phase 46 completion

Phase 46 で完成:

```text
ScalarGreaterEqualStatement
symbolic n ≥ k+2
symbolic m ≥ n
TodaIteratedSuspensionMap
symbolic exponent m-n
source π_{n+k}^n
target π_{m+k}^m
Toda45IsomorphismStatement
Toda (4.5) theorem semantics
guard-aware applicability
invalid-case rejection
cross-instance rejection
theorem provenance
one-round fixed-point integration
representative executable probe
full regression
```

generic inference engine:

```text
変更なし
```

generic map-property API:

```text
変更なし
```

Phase 46 completion status:

```text
full suite
2143 passed in 64.31s
```

### 状態

完了

---

# Phase 46 completion boundary

実装済み:

```text
n ≥ k+2
m ≥ n

E^(m-n):
π_{n+k}^n
→
π_{m+k}^m

is isomorphism by Toda (4.5)
```

instance-aware theorem:

```text
Toda45IsomorphismStatement(
  map=TodaIteratedSuspensionMap(...)
)
```

未実装:

```text
general symbolic inequality solver
automatic numeric inequality validation
general symbolic dimension solver
symbolic map typing solver
generic map-property type generalization
Toda45IsomorphismStatement → IsomorphismStatement bridge
generic InjectiveMapStatement consequence
Toda Prop.4.4
Toda Prop.4.4 E injectivity consequence
stable homotopy
general Whitehead algebra
automatic Whitehead zero / nonzero solver
general existential witness machinery
higher Toda brackets
```

---

# 次の Phase

```text
Phase 47 candidate
Toda Proposition 4.4
decomposition-isomorphism compatibility check
```

最初に current representation との compatibility を確認する。

特に:

```text
TodaPrimaryGroup
PrimaryComponent
PreimageSubgroup
DirectSumGroup
Toda Prop.4.4 の exact decomposition statement
必要な instance-aware isomorphism object
Toda (4.5) との依存
後続 E injectivity consequence
```

を確認する。

Phase 47 の compatibility check より前に generic map-property API を拡張しない。

---

# Phase 47：Toda Proposition 4.4 decomposition isomorphism

目的:

Toda Proposition 4.4:

```text
α ∈ π_{2n-1}^n
H(α)=±ι_{2n-1}
```

のもとで:

```text
Φ:
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
→
π_i^n

Φ(β,γ)=Eβ+α∘γ
```

が isomorphism であることを symbolic instance を保持して theorem-level に表現する。

`E` injectivity consequence は Phase 47 では先取りしない。

---

## Phase 47-1：Toda Proposition 4.4 compatibility check

production code 変更なし。

確認:

```text
TodaPrimaryGroup
→ individual source / target terms を lossless

ScalarSum / ScalarProduct
→ i-1 / n-1 / 2n-1 を lossless

Suspension / Composition / Sum
→ Eβ+α∘γ を lossless

Relation + MapApplication(H,...)
→ H(α)=±ι_{2n-1} を lossless
```

不足:

```text
DirectSumGroup に TodaPrimaryGroup summand がない
TodaPrimaryGroup membership statement がない
instance-aware decomposition map がない
instance-aware Proposition 4.4 isomorphism statement がない
```

generic `IsomorphismStatement(map: MapSymbol)` は Proposition 4.4 instance を保持できないことを確認。

verified:

```text
tests/test_phase47_toda_prop44_compatibility.py
25 passed

full suite
2168 passed in 69.31s
```

### 状態

完了

---

## Phase 47-2：decomposition source / target minimum representation

変更:

```text
DirectSumGroup.summands

FreeCyclicGroup | PrimaryComponent
→
FreeCyclicGroup | PrimaryComponent | TodaPrimaryGroup
```

これにより:

```text
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
```

を source として lossless に表現可能。

target:

```text
π_i^n
```

は existing `TodaPrimaryGroup` を再利用。

Phase 44 direct-sum representation への regression を確認。

verified:

```text
tests/test_phase47_toda_prop44_decomposition_groups.py
17 passed

tests/test_phase47_toda_prop44_compatibility.py
24 passed

full suite
2184 passed in 64.39s
```

### 状態

完了

---

## Phase 47-3：Proposition 4.4 decomposition map minimum representation

追加:

```text
TodaProp44DecompositionMap
├── source_group
├── target_group
├── alpha
├── beta
├── gamma
└── formula
```

representative:

```text
Φ:
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
→
π_i^n

Φ(β,γ)=Eβ+α∘γ
```

formula は existing:

```text
Suspension
Composition
Sum
```

を再利用。

important:

```text
TodaProp44DecompositionMap
!= MapSymbol
!= TodaIteratedSuspensionMap
```

constructor は formula validity や group compatibility を検査しない。

verified:

```text
tests/test_phase47_toda_prop44_decomposition_map.py
27 passed

tests/test_phase47_toda_prop44_decomposition_groups.py
17 passed

tests/test_phase47_toda_prop44_compatibility.py
23 passed

full suite
2210 passed in 68.14s
```

### 状態

完了

---

## Phase 47-4a：TodaPrimaryGroup membership minimum representation

追加:

```text
TodaPrimaryGroupMembershipStatement
├── element: Expression
└── group: TodaPrimaryGroup
```

representative:

```text
α ∈ π_{2n-1}^n
```

existing:

```text
PrimaryComponentMembershipStatement
```

とは distinct。

constructor は membership truth や element dimension を検証しない。

verified:

```text
tests/test_phase47_toda_prop44_toda_membership.py
15 passed

tests/test_phase47_toda_prop44_compatibility.py
22 passed

full suite
2224 passed in 55.25s
```

### 状態

完了

---

## Phase 47-4b：Toda Proposition 4.4 theorem semantics

追加:

```text
TodaProp44IsomorphismStatement(map)
```

追加:

```text
toda_prop44_isomorphism_inference_rule()
```

premises:

```text
α ∈ π_{2n-1}^n
H(α)=±ι_{2n-1}
TodaProp44DecompositionMap(...)
```

conclusion:

```text
TodaProp44IsomorphismStatement(map)
```

`match_guard` で:

```text
membership degree
same α
H map
±ι_{2n-1}
source first / second summands
target
formula Eβ+α∘γ
```

を同一 symbolic instance として確認。

positive / negative Hopf の双方を受理。

generic inference engine は変更しない。

verified:

```text
tests/test_phase47_toda_prop44_theorem_semantics.py
22 passed

tests/test_phase47_toda_prop44_toda_membership.py
15 passed

tests/test_phase47_toda_prop44_decomposition_map.py
27 passed

tests/test_phase47_toda_prop44_decomposition_groups.py
17 passed

tests/test_phase47_toda_prop44_compatibility.py
20 passed

full suite
2244 passed in 58.85s
```

### 状態

完了

---

## Phase 47-5：applicability / invalid cases / provenance

production code 変更なし。

確認:

```text
positive Hopf instance
→ exactly one theorem

negative Hopf instance
→ exactly one theorem

different n mixing
→ reject

different α mixing
→ reject

different i / n / α theorem instances
→ structurally distinct
```

generic boundary:

```text
TodaProp44IsomorphismStatement
!= IsomorphismStatement
!= Toda45IsomorphismStatement
```

existing:

```text
isomorphism_implies_injective_inference_rule()
```

は `TodaProp44IsomorphismStatement` に match しない。

Phase 47 では:

```text
generic InjectiveMapStatement
E injectivity consequence
```

を生成しないことを確認。

verified:

```text
tests/test_phase47_toda_prop44_applicability_compatibility.py
21 passed

full suite
2265 passed in 56.15s
```

### 状態

完了

---

## Phase 47-6：representative probe / final regression

追加:

```text
probes/probe_phase47_capabilities.py
tests/test_phase47_toda_prop44_probe.py
```

representative output:

```text
α ∈ π_{2n-1}^{n}
H(α) = ι_(2n-1)

Φ: π_{i-1}^{n-1} ⊕ π_{i}^{2n-1} → π_{i}^{n}
Φ(β,γ) = Eβ + α∘γ

Φ: π_{i-1}^{n-1} ⊕ π_{i}^{2n-1} → π_{i}^{n} is isomorphism
```

provenance / fixed point:

```text
theorem isomorphism count = 1
premise count = 3
derived round count = 1
fixed point = True
```

verified:

```text
tests/test_phase47_toda_prop44_probe.py
12 passed

tests/test_phase47_toda_prop44_applicability_compatibility.py
21 passed

tests/test_phase47_toda_prop44_theorem_semantics.py
22 passed

tests/test_phase47_toda_prop44_toda_membership.py
15 passed

tests/test_phase47_toda_prop44_decomposition_map.py
27 passed

tests/test_phase47_toda_prop44_decomposition_groups.py
17 passed

tests/test_phase47_toda_prop44_compatibility.py
20 passed

tests/test_toda_rules.py
66 passed

tests/test_map_property_rules.py
26 passed

tests/test_inference_rule_pattern.py
438 passed

full suite
2277 passed in 55.61s
```

probe:

```powershell
python -m probes.probe_phase47_capabilities
```

正常完走。

### 状態

完了

---

## Phase 47-7：Phase 47 completion

Phase 47 で完成:

```text
TodaPrimaryGroupMembershipStatement
DirectSumGroup TodaPrimaryGroup summands
symbolic Proposition 4.4 source / target
TodaProp44DecompositionMap
structural Eβ+α∘γ formula
TodaProp44IsomorphismStatement
Toda Proposition 4.4 theorem semantics
positive / negative Hopf applicability
guard-aware applicability
invalid-case rejection
cross-instance rejection
theorem provenance
one-round fixed-point integration
representative executable probe
full regression
```

generic inference engine:

```text
変更なし
```

generic map-property API:

```text
変更なし
```

Phase 47 completion status:

```text
full suite
2277 passed in 55.61s
```

### 状態

完了

---

# Phase 47 completion boundary

実装済み:

```text
α ∈ π_{2n-1}^n
H(α)=±ι_{2n-1}

Φ:
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
→
π_i^n

Φ(β,γ)=Eβ+α∘γ

is isomorphism by Toda Proposition 4.4
```

instance-aware theorem:

```text
TodaProp44IsomorphismStatement(
  map=TodaProp44DecompositionMap(...)
)
```

未実装:

```text
general symbolic dimension solver
symbolic map typing solver
generic map-property type generalization
Toda45IsomorphismStatement → IsomorphismStatement bridge
TodaProp44IsomorphismStatement → IsomorphismStatement bridge
generic InjectiveMapStatement consequence for Toda-specific maps
Toda Proposition 4.4 E injectivity consequence
stable homotopy
general Whitehead algebra
automatic Whitehead zero / nonzero solver
general existential witness machinery
higher Toda brackets
```

---

# 次の Phase

```text
Phase 48 candidate
Toda Proposition 4.4 consequence
E injective
```

最初に compatibility check を行う。

特に:

```text
injective とする E の exact instance
source / target の instance-aware representation
TodaProp44IsomorphismStatement からの consequence rule
existing generic InjectiveMapStatement との compatibility
decomposition map と E map の区別
```

を確認する。

Phase 48 でも actual need に必要な最小変更だけを行い、generic map-property API を先に generalize しない。

---

# Phase 48：Toda Proposition 4.4 consequence — E injective

目的:

Toda Proposition 4.4 の decomposition isomorphism から、第一 direct-sum summand 上の suspension

```text
E: π_{i-1}^{n-1} → π_i^n
```

が injective であることを symbolic `(i,n)` instance を保ったまま導出する。

generic `MapSymbol` property と specific Toda suspension map を混同しない。

---

## Phase 48-1：current injectivity / E-map representation compatibility check

production code 変更なし。

確認:

```text
EHP_E_MAP
= MapSymbol("E")

InjectiveMapStatement(EHP_E_MAP)
= representable
```

一方 generic injectivity statement は source / target group を保持しないため:

```text
E: π_{i-1}^{n-1} → π_i^n
```

という specific `(i,n)` instance を lossless に保持できない。

Phase 47 theorem 側には decomposition map を通して first summand / target instance が残ることを確認。

追加:

```text
tests/test_phase48_toda_prop44_e_injectivity_compatibility.py
```

verified:

```text
21 passed
full suite 2298 passed in 59.00s
```

### 状態

完了

---

## Phase 48-2：instance-aware E map minimum representation

追加:

```text
TodaSuspensionMap
├── source_group: TodaPrimaryGroup
└── target_group: TodaPrimaryGroup
```

representative:

```text
E: π_{i-1}^{n-1} → π_i^n
```

important:

```text
TodaSuspensionMap
!= MapSymbol
!= EHP_E_MAP
!= Suspension
!= TodaIteratedSuspensionMap
!= TodaProp44DecompositionMap
```

constructor は typing / injectivity を判定しない。

追加:

```text
tests/test_phase48_toda_prop44_e_map.py
```

verified:

```text
22 passed
full suite 2320 passed in 54.79s
```

### 状態

完了

---

## Phase 48-3：Prop.4.4 first-summand embedding / restriction semantics

一般的な direct-sum inclusion machinery は導入せず、Prop.4.4 に必要な domain-specific minimum semantics を追加。

追加:

```text
TodaProp44FirstSummandRestrictionStatement
├── decomposition_map: TodaProp44DecompositionMap
└── suspension_map: TodaSuspensionMap
```

追加 rule:

```text
toda_prop44_first_summand_restriction_inference_rule()
```

meaning:

```text
Φ|_{π_{i-1}^{n-1}}
= E: π_{i-1}^{n-1} → π_i^n
```

`match_guard` で:

```text
first summand
suspension source
suspension target
formula Eβ+α∘γ
```

を確認。

追加:

```text
tests/test_phase48_toda_prop44_first_summand_restriction.py
```

verified:

```text
22 passed
full suite 2342 passed in 59.14s
```

### 状態

完了

---

## Phase 48-4：Toda Prop.4.4 ⇒ E injective theorem semantics

追加:

```text
TodaProp44SuspensionInjectiveStatement
└── map: TodaSuspensionMap
```

追加 rule:

```text
toda_prop44_suspension_injective_inference_rule()
```

premises:

```text
TodaProp44IsomorphismStatement(Φ)
TodaProp44FirstSummandRestrictionStatement(Φ,E)
```

conclusion:

```text
TodaProp44SuspensionInjectiveStatement(E)
```

rule は same decomposition-map instance、first-summand source、target compatibility を guard-aware に確認。

generic `InjectiveMapStatement(EHP_E_MAP)` は生成しない。

追加:

```text
tests/test_phase48_toda_prop44_e_injective_theorem.py
```

verified:

```text
26 passed
full suite 2368 passed in 60.20s
```

### 状態

完了

---

## Phase 48-5：applicability / invalid cases / provenance

production code 変更なし。

確認:

```text
valid instance
→ exactly one specific E injectivity

missing isomorphism
→ reject

missing restriction
→ reject

cross-i
→ reject

cross-n
→ reject

cross-α
→ reject

different decomposition map
→ reject

wrong E source / target
→ reject

second summand as E source
→ reject
```

provenance:

```text
ProofRule.INFERENCE
exact two premises
inference_rule preserved
```

generic boundary:

```text
TodaProp44SuspensionInjectiveStatement
!= InjectiveMapStatement(EHP_E_MAP)
```

追加:

```text
tests/test_phase48_toda_prop44_e_injective_applicability.py
```

verified:

```text
22 passed
full suite 2390 passed in 58.57s
```

### 状態

完了

---

## Phase 48-6：representative probe / full regression

追加:

```text
probes/probe_phase48_capabilities.py
tests/test_phase48_toda_prop44_probe.py
```

representative initial GIVEN:

```text
α ∈ π_{2n-1}^n
H(α)=ι_{2n-1}
TodaProp44DecompositionMap
TodaSuspensionMap
```

end-to-end fixed point:

```text
round 1
TodaProp44IsomorphismStatement
TodaProp44FirstSummandRestrictionStatement

round 2
TodaProp44SuspensionInjectiveStatement

fixed point
```

representative result:

```text
Φ: π_{i-1}^{n-1} ⊕ π_i^{2n-1} → π_i^n
Φ(β,γ)=Eβ+α∘γ

Φ is isomorphism
Φ|_{π_{i-1}^{n-1}} = E
E: π_{i-1}^{n-1} → π_i^n is injective
```

verified:

```text
tests/test_phase48_toda_prop44_probe.py
21 passed

full suite
2411 passed in 58.16s
```

probe:

```powershell
python -m probes.probe_phase48_capabilities
```

### 状態

完了

---

## Phase 48-7：Phase 48 completion

Phase 48 で完成:

```text
TodaSuspensionMap
instance-aware suspension source / target
TodaProp44FirstSummandRestrictionStatement
Toda Proposition 4.4 first-summand restriction semantics
TodaProp44SuspensionInjectiveStatement
Toda Proposition 4.4 suspension injectivity theorem semantics
invalid-case rejection
cross-instance rejection
theorem provenance
two-round fixed-point integration
representative executable probe
full regression
```

generic inference engine:

```text
変更なし
```

generic map-property API:

```text
変更なし
```

Phase 48 completion status:

```text
full suite
2411 passed in 58.16s
```

### 状態

完了

---

# Phase 48 completion boundary

実装済み:

```text
Toda Proposition 4.4 decomposition isomorphism
↓
first-summand restriction
↓
E: π_{i-1}^{n-1} → π_i^n is injective
```

instance-aware theorem:

```text
TodaProp44SuspensionInjectiveStatement(
  map=TodaSuspensionMap(...)
)
```

未実装:

```text
generic InjectiveMapStatement bridge
generic map-property type generalization
general direct-sum inclusion machinery
automatic equality reflection through TodaSuspensionMap
general symbolic dimension solver
symbolic map typing solver
stable homotopy
general existential witness machinery
higher Toda brackets
```

---

# 次の Phase

```text
Phase 49 candidate
concrete EHP calculation
π_3^2 = Z{η_2}
```

最初に compatibility check を行う。

対象 path:

```text
π_2^1 -E→ π_3^2 -H→ π_3^3 -Δ→ π_1^1 -E→ π_2^2
```

低次 facts と exactness から `H: π_3^2 → π_3^3` isomorphism を導き、`ι_3` を source generator `η_2` へ transport できるか確認する。

一般的 existential witness machinery は先取りしない。

