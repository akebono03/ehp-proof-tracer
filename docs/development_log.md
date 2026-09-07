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

# Phase 51：Toda Proposition 5.1 proof dependency analysis

目的:

```text
Prop.5.1 の actual proof path
+
Phase 49–50 / current code
↓
既に独立導出できる premise と不足 edge を確定する
```

production code は変更しない。

---

## Phase 51-1：actual statement / proof path compatibility

旧 Phase 35 で Prop.5.1 由来の GIVEN fact として使用していた

```text
H(η₂)=ι₃
```

は、現在は Phase 49 の

```text
H isomorphism
↓
η₂ = unique H-preimage of ι₃
↓
H(η₂)=ι₃
```

で独立に導出可能であることを確認。

したがって旧 provenance は Prop.5.1 proof の premise として使用しない。

### 状態

完了

---

## Phase 51-2：current code で既に推論可能な premises

AVAILABLE:

```text
π_3^2=Z{η₂}
H(η₂)=ι₃
π_4^3=Z/2{η₃}
η_n=E^(n-2)η₂ structural definition
Toda (4.5) stable-range E^(m-n) isomorphism
```

PARTIAL:

```text
π_{n+1}^n=Z/2{η_n}, n≥3
higher η_n generator connection
```

MISSING:

```text
finite-cyclic transport through Toda (4.5)
stable (G_1;2) representation / conclusion
direct Δ(ι₅)=±2η₂ conclusion
```

### 状態

完了

---

## Phase 51-3：missing low-dimensional groups

追加の low-dimensional group fact は不要と判断。

既存 base facts / results:

```text
π_2^1=0
π_3^3=Z{ι₃}
π_5^5=Z{ι₅}
π_4^5=0
π_3^2=Z{η₂}
π_4^3=Z/2{η₃}
```

高次は個別 table fact ではなく

```text
π_4^3
+
Toda (4.5)
↓
π_{n+1}^n
```

で transport する方針。

`(G_1;2)` は deferred。

### 状態

完了

---

## Phase 51-4：composition / suspension / Hopf relations

Toda p.39 の scan を確認。

同ページでは proof text に

```text
Δ(ι₅)=±2η₂
```

とある一方、printed Proposition 5.1 line は `±2η₃` となっており内部不整合がある。

`Δ(ι₅)∈π_3^2` の次元と proof text に合わせ、development target は

```text
Δ(ι₅)=±2η₂
```

とする。

確認結果:

```text
H(η₂)=ι₃                 AVAILABLE
H injective               AVAILABLE
new composition relation  NOT REQUIRED
Δ(ι₅)=±2η₂ direct bridge  MISSING
E^(n-3)η₃=η_n             MISSING
finite cyclic transport   MISSING
```

Prop.5.1 の直後の composition isomorphism (5.2) は proof premise ではないため deferred。

### 状態

完了

---

## Phase 51-5：circular dependency check

安全な branch:

```text
Toda Prop.4.2 / independent low-dimensional facts
↓
Phase 49
π_3^2=Z{η₂}, H(η₂)=ι₃
↓
Toda Prop.2.7 minimum consequence
↓
Phase 50
π_4^3=Z/2{η₃}
↓
Toda (4.5)
↓
higher η-family
↓
Prop.5.1 finite-dimensional conclusion
```

循環するため使用禁止:

```text
Prop.5.1 GIVEN
↓
H(η₂)=ι₃
↓
old Phase 35–36 proof trace
↓
Prop.5.1 proof
```

Phase 35–38 の rule / machinery 自体は、Phase 49 derived premise に差し替えれば後で再利用可能。

### 状態

完了

---

## Phase 51-6：minimum implementation roadmap

必要な implementation を4点に限定。

```text
1. Δ(ι₅)=±2η₂ direct bridge
2. Toda (4.5) finite-cyclic transport
3. E^(n-3)η₃=η_n bridge
4. Prop.5.1 finite-dimensional integration / provenance test
```

先取りしない:

```text
additional low-dimensional group table
general sign algebra
general suspension normalization
generic isomorphism transport framework
stable (G_1;2)
composition (5.2)
```

### 状態

完了

---

## Phase 51-7：completion

Phase 51 で確定:

```text
Prop.5.1 finite-dimensional proof target
current independent premises
no additional low-dimensional group facts required
missing Δ direct relation edge
missing finite-cyclic transport edge
missing higher η-family bridge
circular dependency boundary
minimum Phase 52–55 roadmap
```

production code:

```text
変更なし
```

full regression:

```text
not rerun in Phase 51
last known: 2703 passed in 65.69s
```

### 状態

COMPLETE

---

# Phase 51 completion boundary

Completed analysis branch:

```text
Phase 49
π_3^2=Z{η₂}
COMPLETE
↓
Phase 50
π_4^3=Z/2{η₃}
COMPLETE
↓
Phase 51
Toda Proposition 5.1 proof dependency analysis
COMPLETE
```

Minimum next implementation sequence:

```text
Phase 52
Δ(ι₅)=±2η₂ direct bridge
↓
Phase 53
Toda (4.5) finite-cyclic transport
↓
Phase 54
E^(n-3)η₃=η_n bridge
↓
Phase 55
Prop.5.1 finite-dimensional integration / provenance
```

Stable `(G_1;2)=Z/2{η}` is deferred.

---

# Phase 52：`Δ(ι₅)=±2η₂` direct bridge

目的:

```text
Δ(ι₅)=±[ι₂,ι₂]
+
[ι₂,ι₂]=±2η₂
↓
Δ(ι₅)=±2η₂
```

Toda-specific narrow bridge のみを追加し、general up-to-sign algebra は導入しない。

---

## Phase 52-1：current up-to-sign statement compatibility check

確認:

```text
TodaDeltaImageUpToSignStatement
TodaPi32WhiteheadSquareUpToSignStatement
Multiple(2,η₂)
```

をそのまま再利用可能。

新規 statement class は不要。

production code:

```text
変更なし
```

### 状態

完了

---

## Phase 52-2：minimum statement representation

既存 `TodaDeltaImageUpToSignStatement` で:

```text
Δ(ι₅)=±2η₂
```

を structural に保持できることをテスト固定。

追加:

```text
tests/test_phase52_delta_direct_bridge.py
```

この時点の focused:

```text
5 passed
```

full:

```text
2708 passed in 29.36s
```

### 状態

完了

---

## Phase 52-3：specific bridge inference rule

追加:

```text
toda_delta_iota5_two_eta2_up_to_sign_inference_rule()
```

Derived:

```text
Δ(ι₅)=±[ι₂,ι₂]
+
[ι₂,ι₂]=±2η₂
↓
Δ(ι₅)=±2η₂
```

Guard:

```text
Δ source = π_5^5
Δ target = π_3^2
element = ι₅
intermediate = [ι₂,ι₂]
final positive value = 2η₂
```

focused:

```text
10 passed
```

full:

```text
2713 passed in 27.61s
```

### 状態

完了

---

## Phase 52-4：invalid cases / wrong instance rejection

production code 変更なし。

Reject をテスト固定:

```text
wrong Δ source
wrong Δ target
wrong element
wrong Whitehead square
wrong coefficient
wrong η index
```

focused:

```text
16 passed
```

full:

```text
2719 passed in 25.70s
```

### 状態

完了

---

## Phase 52-5：integration with existing Phase 50 chain

Phase 50 representative rule set に Phase 52 bridge rule を追加。

既存の `Im(Δ)=Z{2η₂}` rule は変更せず並列に保持。

Updated rounds:

```text
round 1
H([ι₂,ι₂])=±2ι₃
Δ(ι₅)=±[ι₂,ι₂]
E surjective
η₃=Eη₂

round 2
[ι₂,ι₂]=±2η₂

round 3
Δ(ι₅)=±2η₂
Im(Δ)=Z{2η₂}

round 4
Ker(E)=Z{2η₂}

round 5
π_4^3=Z/2{Eη₂}

round 6
π_4^3=Z/2{η₃}
```

Integration tests:

```text
18 passed
```

full:

```text
2723 passed in 26.52s
```

### 状態

完了

---

## Phase 52-6：probe / provenance / full regression

追加:

```text
probes/probe_phase52_capabilities.py
tests/test_phase52_probe.py
```

Representative output:

```text
Δ(ι₅)=±[ι₂,ι₂]
[ι₂,ι₂]=±2η₂
↓
Δ(ι₅)=±2η₂
```

Provenance:

```text
bridge premise count = 2
bridge premises are derived = True
bridge result is derived = True
given premise count = 11
derived step count = 10
derived round count = 6
fixed point = True
```

probe tests:

```text
8 passed
```

final full regression:

```text
2731 passed in 26.67s
```

### 状態

完了

---

## Phase 52-7：completion

Phase 52 で完成:

```text
existing up-to-sign statement reuse
Δ(ι₅)=±2η₂ minimum representation
Toda-specific direct bridge rule
wrong-instance rejection
Phase 50 chain integration
INFERENCE provenance
representative probe
full regression
```

Generic inference engine:

```text
変更なし
```

Not added:

```text
general up-to-sign transitivity
general sign solver
generic isomorphism transport
Toda (4.5) finite-cyclic transport
higher η-family bridge
Prop.5.1 finite-dimensional integration
stable homotopy model
```

### 状態

COMPLETE

---

# Phase 52 completion boundary

Current branch:

```text
Phase 49
π_3^2=Z{η₂}
COMPLETE
↓
Phase 50
π_4^3=Z/2{η₃}
COMPLETE
↓
Phase 51
Toda Proposition 5.1 proof dependency analysis
COMPLETE
↓
Phase 52
Δ(ι₅)=±2η₂ direct bridge
COMPLETE
```

Remaining finite-dimensional Proposition 5.1 path:

```text
Phase 53
Toda (4.5) finite-cyclic transport
↓
Phase 54
E^(n-3)η₃=η_n bridge
↓
Phase 55
Prop.5.1 finite-dimensional integration / provenance
```

Stable `(G_1;2)=Z/2{η}` remains deferred.

---

# Phase 53：Toda (4.5) finite-cyclic transport

目的:

```text
π_4^3=Z/2{η₃}
+
E^(n-3): π_4^3 ≅ π_{n+1}^n
↓
π_{n+1}^n=Z/2{E^(n-3)η₃}
```

Toda (4.5) の既存 instance-aware isomorphism を使い、Prop.5.1 に必要な finite-cyclic transport だけを実装する。

---

## Phase 53-1：current Toda (4.5) / FiniteCyclicGroup compatibility check

確認:

```text
TodaIteratedSuspensionMap      AVAILABLE
Toda45IsomorphismStatement    AVAILABLE
TodaPrimaryGroup              AVAILABLE
FiniteCyclicGroup             AVAILABLE
IteratedSuspension            AVAILABLE
Relation                      AVAILABLE
```

新規 production representation は不要と判断。

境界:

```text
specific Toda (4.5) transport only
no generic isomorphism transport
no generic generator transport
no η_n normalization
```

### 状態

完了

---

## Phase 53-2：finite-cyclic transport minimum statement representation

既存構造のみで target を保持できることをテスト固定。

```text
π_{n+1}^n=Z/2{E^(n-3)η₃}
```

`E^(n-3)η₃` は `IteratedSuspension` として保持し、`η_n` へ normalize しない。

追加:

```text
tests/test_phase53_finite_cyclic_transport.py
```

focused:

```text
8 passed
```

full:

```text
2739 passed in 26.92s
```

### 状態

完了

---

## Phase 53-3：specific transport inference rule

追加:

```text
toda_45_pi4_3_finite_cyclic_transport_inference_rule()
```

Derived:

```text
π_4^3=Z/2{η₃}
+
Toda45IsomorphismStatement
↓
π_{n+1}^n=Z/2{E^(n-3)η₃}
```

Phase 46 の source degree `ScalarSum(3,1)` と Phase 50 の concrete `4` の表現差は、この specific `π_4^3` guard 内だけで受理する。generic scalar normalization は追加しない。

focused:

```text
14 passed
```

full:

```text
2745 passed in 25.53s
```

### 状態

完了

---

## Phase 53-4：stable-range / wrong-map / wrong-group rejection

production code 変更なし。

Phase 46 と Phase 53 の責務を分離したまま reject を固定。

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

valid chain では:

```text
stable-range premises
↓
Toda45IsomorphismStatement
↓
finite-cyclic transport
```

まで接続することを確認。

focused:

```text
24 passed
```

full:

```text
2755 passed in 25.60s
```

### 状態

完了

---

## Phase 53-5：integration from π_4^3=Z/2{η₃}

Phase 50 の最終 group relation を GIVEN として再投入せず、同一 run 内で derived result のまま利用。

```text
Phase 50
π_4^3=Z/2{η₃}  INFERENCE

Phase 46
Toda (4.5) isomorphism  INFERENCE

↓

Phase 53
π_{n+1}^n=Z/2{E^(n-3)η₃}  INFERENCE
```

transport step の2 premise が両方 derived であることを確認。

追加:

```text
tests/test_phase53_integration.py
```

focused:

```text
6 passed
```

full:

```text
2761 passed in 25.89s
```

### 状態

完了

---

## Phase 53-6：probe / provenance / full regression

追加:

```text
probes/probe_phase53_capabilities.py
tests/test_phase53_probe.py
```

Representative output:

```text
π_4^3 = Z/2{η₃}

Toda (4.5):
E^(n-3): π_4^3 ≅ π_(n+1)^n

↓

π_(n+1)^n = Z/2{E^(n-3)η₃}
```

Provenance:

```text
source group result is derived = True
Toda45 isomorphism is derived = True
transport result is derived = True
transport premise count = 2
transport premises are derived = True
given premise count = 14
derived step count = 11
derived round count = 7
fixed point = True
```

Phase 53 tests:

```text
tests/test_phase53_finite_cyclic_transport.py  24 passed
tests/test_phase53_integration.py               6 passed
tests/test_phase53_probe.py                     8 passed
```

final full regression:

```text
2769 passed in 25.60s
```

### 状態

完了

---

## Phase 53-7：completion

Phase 53 で完成:

```text
existing Toda (4.5) representation reuse
finite-cyclic target minimum representation
specific finite-cyclic transport rule
stable-range branch integration
wrong-instance rejection
Phase 50 derived-result integration
INFERENCE provenance
representative probe
full regression
```

Generic inference engine:

```text
変更なし
```

Not added:

```text
E^(n-3)η₃=η_n
generic isomorphism transport
generic generator transport
generic scalar normalization
generic suspension normalization
Proposition 5.1 finite-dimensional integration
stable homotopy model
```

### 状態

COMPLETE

---

# Phase 53 completion boundary

Current branch:

```text
Phase 49
π_3^2=Z{η₂}
COMPLETE
↓
Phase 50
π_4^3=Z/2{η₃}
COMPLETE
↓
Phase 51
Toda Proposition 5.1 proof dependency analysis
COMPLETE
↓
Phase 52
Δ(ι₅)=±2η₂ direct bridge
COMPLETE
↓
Phase 53
Toda (4.5) finite-cyclic transport
COMPLETE
```

Remaining finite-dimensional Proposition 5.1 path:

```text
Phase 54
E^(n-3)η₃=η_n bridge
↓
Phase 55
Prop.5.1 finite-dimensional integration / provenance
```

Stable `(G_1;2)=Z/2{η}` remains deferred.

---

# 次の Phase

```text
Phase 54
higher η-family bridge
E^(n-3)η₃=η_n
```
