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

representative:

```text
Toda Lemma 4.1: n odd
π_{2n-1}^{n} = π_{2n-1}(S^{n};2)
```

```text
Toda Lemma 4.1: n even + Whitehead nonzero
π_{2n-1}^{n} = Z{P(ι_{2n+1})} ⊕ π_{2n-1}(S^{n};2)
```

```text
Toda Lemma 4.1: n even + Whitehead zero
π_{2n-1}^{n} = Z{α} ⊕ π_{2n-1}(S^{n};2)

α conditions:
H(α)=ι_{2n-1}
Eα ∈ π_{2n}(S^{n+1};2)
```

zero-case theorem bundle:

```text
applicable rule count = 3
derived step count = 3
fixed point = True
```

final regression:

```text
tests/test_phase44_toda_lemma41_case_semantics.py
94 passed

tests/test_toda_rules.py
66 passed

tests/test_phase43_toda_lemma41_premise.py
32 passed

tests/test_phase39_primary_component.py
24 passed

tests/test_hopf_rules.py
31 passed

tests/test_expression.py
145 passed

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

Phase 44 で完成:

```text
symbolic generator index
symbolic HomotopyElement dimension
FreeCyclicGroup
DirectSumGroup
PrimaryComponentMembershipStatement
Toda Lemma 4.1 odd case semantics
Toda Lemma 4.1 even / Whitehead nonzero semantics
Toda Lemma 4.1 even / Whitehead zero group semantics
zero-case H(α)=ι_{2n-1}
zero-case Eα ∈ π_{2n}(S^{n+1};2)
case applicability / exclusivity
theorem provenance
same structural α across three conclusions
fixed-point integration
representative executable probe
full regression
```

generic inference engine:

```text
変更なし
```

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

# Phase 44 completion boundary

実装済み:

```text
n odd
→ π_{2n-1}^n = π_{2n-1}(S^n;2)
```

```text
n even
+
[ι_{n-1},ι_{n-1}] != 0
→
π_{2n-1}^n = Z{P(ι_{2n+1})} ⊕ π_{2n-1}(S^n;2)
```

```text
n even
+
[ι_{n-1},ι_{n-1}] = 0
→
π_{2n-1}^n = Z{α} ⊕ π_{2n-1}(S^n;2)
```

with:

```text
H(α)=ι_{2n-1}
Eα ∈ π_{2n}(S^{n+1};2)
```

未実装:

```text
automatic Whitehead zero / nonzero inference
ZERO / INEQUALITY contradiction detection
Whitehead bilinearity / antisymmetry
automatic α existence / uniqueness
general existential witness machinery
PrimaryComponent membership → ordinary membership bridge
Toda Prop.4.2
Toda (4.5)
Toda Prop.4.4
stable homotopy
higher Toda brackets
```

---

# 次の Phase

```text
Phase 45
Toda Proposition 4.2
2-primary EHP exact sequence
```

実装前 compatibility check:

```text
current EHP exactness representation
current E / H / P map terms
PrimaryComponent
TodaPrimaryGroup
PreimageSubgroup
Toda Prop.4.2 exact statement
```

Phase 45 でも:

```text
actual mathematical need
↓
minimum representation
↓
explicit theorem rule
↓
existing generic inference engine
```

を維持する。

Toda (4.5)、Toda Prop.4.4、general Whitehead-product algebra は先取りしない。
