# ehp_proof 開発記録

current specification は `README.md` / `docs/design.md` を優先する。

---

# Phase 1–27 概要

abelian-group calculation、generic inference、EHP、ORDER、Suspension、Freudenthal、Composition、Hopf invariant、additive / homomorphism / subgroup / modulo / symbolic scalar / indeterminacy reasoning、unstable Toda bracket、typed elements、generator facts を整備。

### 状態

COMPLETE

---

# Phase 28–38 概要

Toda Prop.2.2、Barratt–Hilton、actual H branch を接続し:

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

### 状態

COMPLETE

---

# Phase 39–48 概要

```text
39 PrimaryComponent
40 TodaPrimaryGroup
41 PreimageSubgroup
42 WhiteheadProduct
43 Toda Lemma 4.1 premise vocabulary
44 Toda Lemma 4.1 case semantics
45 Toda Proposition 4.2 EHP exactness
46 Toda (4.5) stable-range isomorphism
47 Toda Proposition 4.4 decomposition
48 Toda Proposition 4.4 E injectivity
```

### 状態

COMPLETE

---

# Phase 49：`π_3^2=Z{η₂}`

EHP:

```text
π_2^1 -E→ π_3^2 -H→ π_3^3 -Δ→ π_1^1 -E→ π_2^2
```

Derived:

```text
H injective
Δ=0
H surjective
H isomorphism
η₂ = unique H-preimage of ι_3
H(η₂)=ι_3
π_3^2=Z{η₂}
```

Representative:

```text
given = 6
derived = 8
rounds = 6
fixed point = True
```

Full regression:

```text
2557 passed in 56.45s
```

### 状態

COMPLETE

---

# Phase 50：`π_4^3=Z/2{η₃}`

目的:

Phase 49 の `π_3^2=Z{η₂}` を concrete EHP calculation に接続する。

---

## Phase 50-1：proof dependency compatibility

確認した EHP windows:

```text
π_5^5 -Δ→ π_3^2 -E→ π_4^3
π_3^2 -E→ π_4^3 -H→ π_4^5
```

Required:

```text
π_5^5=Z{ι_5}
π_4^5=0
Toda Proposition 2.7 minimum consequence
```

必要な Prop.2.7 consequence:

```text
H([ι_2,ι_2])=±2ι_3
```

### 状態

完了

---

## Phase 50-2：up-to-sign representation compatibility

`Relation` では unresolved `±` を1 statement に lossless に保持できないことを確認。

general `PlusMinus` は導入せず theorem-specific statement を採用。

### 状態

完了

---

## Phase 50-3：minimum Prop.2.7 theorem semantics

追加:

```text
TodaProp27HopfInvariantUpToSignStatement
```

actual:

```text
H([ι_2,ι_2])=±2ι_3
```

focused:

```text
18 passed
```

### 状態

完了

---

## Phase 50-4a：Whitehead square

Derived:

```text
H([ι_2,ι_2])=±2ι_3
+
H(η₂)=ι_3
+
H injective
↓
[ι_2,ι_2]=±2η₂
```

focused:

```text
14 passed
```

full:

```text
2589 passed in 62.06s
```

### 状態

完了

---

## Phase 50-4b：low-dimensional Δ facts

追加:

```text
π_5^5=Z{ι_5}
π_4^5=0
TodaDeltaImageUpToSignStatement
```

Derived:

```text
Δ(ι_5)=±[ι_2,ι_2]
```

focused:

```text
22 passed
```

full:

```text
2611 passed in 64.75s
```

### 状態

完了

---

## Phase 50-4c：exactness bridge

追加:

```text
TodaDeltaImageFreeCyclicStatement
TodaSuspensionKernelFreeCyclicStatement
TodaSuspensionSurjectiveStatement
```

Derived:

```text
Im(Δ)=Z{2η₂}
Ker(E)=Z{2η₂}
E: π_3^2→π_4^3 surjective
```

focused:

```text
18 passed
```

full:

```text
2629 passed in 61.36s
```

### 状態

完了

---

## Phase 50-4d：finite cyclic conclusion

追加:

```text
FiniteCyclicGroup
```

Derived:

```text
π_3^2=Z{η₂}
+
Ker(E)=Z{2η₂}
+
E surjective
↓
π_4^3=Z/2{Eη₂}
```

focused:

```text
17 passed
```

full:

```text
2646 passed in 61.38s
```

### 状態

完了

---

## Phase 50-4e：η-family notation

Definition:

```text
η_n=E^(n-2)η₂
```

For n=3:

```text
η₃=Eη₂
```

Then:

```text
π_4^3=Z/2{Eη₂}
↓
π_4^3=Z/2{η₃}
```

途中 `η3` / `η₃` mismatch をテストで検出し修正。

focused:

```text
16 passed
```

full:

```text
2662 passed in 66.78s
```

### 状態

完了

---

## Phase 50-5：applicability / provenance

production code 変更なし。

確認:

```text
wrong H instance reject
wrong Δ instance reject
wrong exactness window reject
missing π_3^2 structure reject
wrong η index rejects only notation final
sign-specific equality not invented
final result is INFERENCE
```

focused:

```text
14 passed
```

full:

```text
2676 passed in 67.57s
```

### 状態

完了

---

## Phase 50-6：representative probe / final regression

追加:

```text
probes/probe_phase50_capabilities.py
tests/test_phase50_probe.py
```

central output:

```text
H([ι_2,ι_2]) = ±2ι_3
[ι_2,ι_2] = ±2η₂
Δ(ι_5) = ±[ι_2,ι_2]
Im(Δ) = Z{2η₂}
Ker(E) = Z{2η₂}
E: π_3^2 → π_4^3 is surjective
π_4^3 = Z/2{Eη₂}
η₃ = Eη₂
π_4^3 = Z/2{η₃}
```

counts:

```text
given premise count = 11
derived step count = 9
round count = 6
fixed point = True
```

probe tests:

```text
27 passed
```

final full regression:

```text
2703 passed in 65.69s
```

### 状態

完了

---

## Phase 50-7：completion

Phase 50 で完成:

```text
minimum Toda Prop.2.7 consequence
up-to-sign theorem-specific semantics
π_5^5=Z{ι_5}
π_4^5=0
[ι_2,ι_2]=±2η₂
Δ(ι_5)=±[ι_2,ι_2]
Im(Δ)=Z{2η₂}
Ker(E)=Z{2η₂}
E surjective
FiniteCyclicGroup
π_4^3=Z/2{Eη₂}
η_n=E^(n-2)η₂
η₃=Eη₂
π_4^3=Z/2{η₃}
applicability
provenance
representative probe
full regression
```

Generic inference engine:

```text
変更なし
```

### 状態

COMPLETE

---

# Phase 50 completion boundary

Current concrete branch:

```text
Phase 49
π_3^2=Z{η₂}
COMPLETE
↓
Phase 50
π_4^3=Z/2{η₃}
COMPLETE
```

Still outside:

```text
full Toda Proposition 2.7 formalization
general sign algebra
general quotient simplification
general first-isomorphism theorem
general suspension normalization
Toda Proposition 5.1 proof completion
stable homotopy
higher Toda brackets
```

---

# 次の Phase

```text
Phase 51 candidate
Toda Proposition 5.1 proof dependency analysis
```

最初に actual proof path と current code / tests を照合し、不足 dependency を確定する。
