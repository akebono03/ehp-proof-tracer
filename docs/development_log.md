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
