# ehp_proof 開発記録

現在の仕様は `README.md` / `docs/design.md` を優先する。

---

# Phase 1–27 概要

可換群計算、汎用推論、EHP、ORDER、Suspension、Freudenthal、Composition、Hopf 不変量、加法、準同型、部分群、modulo、記号的 scalar、不定性推論、unstable Toda bracket、型付き要素、生成元 fact を整備。

### 状態

COMPLETE

---

# Phase 28–38 概要

Toda Proposition 2.2、Barratt–Hilton、actual H branch を接続し:

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

まで完成。

### 状態

COMPLETE

---

# Phase 39–48 概要

```text
39 PrimaryComponent
40 TodaPrimaryGroup
41 PreimageSubgroup
42 WhiteheadProduct
43 Toda Lemma 4.1 premise representation
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

導出:

```text
H injective
Δ=0
H surjective
H isomorphism
η₂ = unique H-preimage of ι_3
H(η₂)=ι_3
π_3^2=Z{η₂}
```

代表実行:

```text
given = 6
derived = 8
rounds = 6
fixed point = True
```

全体回帰:

```text
2557 passed in 56.45s
```

### 状態

COMPLETE

---

# Phase 50：`π_4^3=Z/2{η₃}`

依存:

```text
H([ι₂,ι₂])=±2ι₃
H(η₂)=ι₃
H injective
Δ(ι₅)=±[ι₂,ι₂]
π_5^5=Z{ι₅}
π_4^5=0
EHP exactness
```

導出:

```text
[ι₂,ι₂]=±2η₂
Δ(ι₅)=±2η₂
Im(Δ)=Z{2η₂}
Ker(E)=Z{2η₂}
E surjective
π_4^3=Z/2{Eη₂}
η₃=Eη₂
π_4^3=Z/2{η₃}
```

代表実行:

```text
given = 11
derived = 9
rounds = 6
fixed point = True
```

全体回帰:

```text
2703 passed in 65.69s
```

### 状態

COMPLETE

---

# Phase 51：Toda Proposition 5.1 dependency analysis

有限次元 target:

```text
π_3^2=Z{η₂}
π_{n+1}^n=Z/2{η_n}
H(η₂)=ι₃
Δ(ι₅)=±2η₂
```

不足 edge を:

```text
1. Δ(ι₅)=±2η₂ direct bridge
2. Toda (4.5) finite-cyclic transport
3. E^(n-3)η₃=η_n bridge
4. Proposition 5.1 finite-dimensional integration / provenance
```

に限定した。

旧 literature GIVEN `H(η₂)=ι₃` を Proposition 5.1 の premise として再利用しない方針を確定。

### 状態

COMPLETE

---

# Phase 52：Δ(ι₅)=±2η₂ direct bridge

導出:

```text
Δ(ι₅)=±[ι₂,ι₂]
+
[ι₂,ι₂]=±2η₂
↓
Δ(ι₅)=±2η₂
```

一般の up-to-sign transitivity は導入せず Toda-specific direct bridge に限定。

代表実行:

```text
given = 11
derived = 10
rounds = 6
fixed point = True
```

全体回帰:

```text
2731 passed in 26.67s
```

### 状態

COMPLETE

---

# Phase 53：Toda (4.5) finite-cyclic transport

導出:

```text
π_4^3=Z/2{η₃}
+
E^(n-3): π_4^3 ≅ π_{n+1}^n
↓
π_{n+1}^n=Z/2{E^(n-3)η₃}
```

代表実行:

```text
given = 14
derived = 11
rounds = 7
fixed point = True
```

全体回帰:

```text
2769 passed in 25.60s
```

### 状態

COMPLETE

---

# Phase 54：higher η-family bridge

structural definition:

```text
η_n=E^(n-2)η₂
```

bridge:

```text
η₃=Eη₂
+
η_n=E^(n-2)η₂
↓
E^(n-3)η₃=η_n
```

finite-cyclic integration:

```text
π_{n+1}^n=Z/2{E^(n-3)η₃}
+
E^(n-3)η₃=η_n
↓
π_{n+1}^n=Z/2{η_n}
```

代表実行:

```text
given = 15
derived = 13
rounds = 8
fixed point = True
```

全体回帰:

```text
2804 passed in 26.50s
```

### 状態

COMPLETE

---

# Phase 55：Toda Proposition 5.1 finite-dimensional integration / provenance

有限次元側で independently derived:

```text
π_3^2=Z{η₂}
H(η₂)=ι₃
Δ(ι₅)=±2η₂
π_{n+1}^n=Z/2{η_n}
```

追加:

```text
TodaProp51FiniteDimensionalStatement
toda_prop51_finite_dimensional_integration_inference_rule()
```

最終 rule は4 premise をすべて `ProofRule.INFERENCE` として要求。

代表 run は Phase 49 base premise から組み直し、Phase 49 result を GIVEN として再投入しない。

代表 provenance:

```text
pi_3^2 result is derived = True
H(eta_2)=iota_3 is derived = True
Delta(iota_5)=+-2eta_2 is derived = True
higher eta group is derived = True
final Prop.5.1 result is derived = True
final premise count = 4
final premises are derived = True
H(eta_2)=iota_3 is GIVEN premise = False
pi_3^2 result is GIVEN premise = False
Prop.5.1 result is GIVEN premise = False
given premise count = 17
derived step count = 23
derived round count = 14
fixed point = True
```

全体回帰:

```text
2844 passed in 31.12s
```

### 状態

COMPLETE

---

# Phase 56：Toda (5.2) composition isomorphism

目標:

```text
η₂∘- :
π_i^3
≅
π_i^2
    (i≥3)
```

---

## Phase 56-1：Prop.4.4 / Composition / zero-group compatibility check

確認:

```text
π_{i-1}^1 ⊕ π_i^3 → π_i^2
Eβ+η₂∘γ
π_{i-1}^1=0
```

は既存:

```text
TodaProp44DecompositionMap
Composition
TodaPrimaryGroupZeroStatement
```

で表現可能。

ただし generic Prop.4.4 rule では concrete `3` と structural `2*2-1` が直接一致しない。

production code:

```text
変更なし
```

追加:

```text
tests/test_phase56_prop44_composition_compatibility.py
```

focused:

```text
6 passed
```

全体回帰:

```text
2850 passed in 28.58s
```

### 状態

COMPLETE

---

## Phase 56-2：`π_{i-1}^1=0 (i≥3)`

追加 rule:

```text
toda_pi_i_minus_1_1_zero_inference_rule()
```

推論:

```text
i≥3
↓
π_{i-1}^1=0
```

既存:

```text
ScalarGreaterEqualStatement
TodaPrimaryGroupZeroStatement
```

を再利用。

一般 inequality solver は追加しない。

追加:

```text
tests/test_phase56_pi_i_minus_1_1_zero.py
```

focused:

```text
10 passed
```

全体回帰:

```text
2860 passed in 28.04s
```

### 状態

COMPLETE

---

## Phase 56-3：Prop.4.4 specialization to `n=2, α=η₂`

追加 rule:

```text
toda_prop44_eta2_n2_isomorphism_inference_rule()
```

接続:

```text
TodaPi32Eta2DefinitionStatement    INFERENCE
H(η₂)=ι₃                           INFERENCE
TodaProp44DecompositionMap
↓
TodaProp44IsomorphismStatement
```

concrete result:

```text
Φ:
π_{i-1}^1 ⊕ π_i^3
≅
π_i^2

Φ(β,γ)=Eβ+η₂∘γ
```

generic Prop.4.4 rule は変更しない。

追加:

```text
tests/test_phase56_prop44_eta2_specialization.py
```

focused:

```text
11 passed
```

全体回帰:

```text
2871 passed in 28.45s
```

### 状態

COMPLETE

---

## Phase 56-4：second-summand restriction

追加:

```text
TodaProp44SecondSummandRestrictionStatement
toda_prop44_eta2_second_summand_restriction_inference_rule()
```

導出:

```text
Φ isomorphism
↓
Φ|_{π_i^3}(γ)=η₂∘γ
```

generic composition-map framework は追加しない。

追加:

```text
tests/test_phase56_prop44_second_summand_restriction.py
```

focused:

```text
13 passed
```

全体回帰:

```text
2884 passed in 29.62s
```

### 状態

COMPLETE

---

## Phase 56-5：zero first summand → composition isomorphism (5.2)

追加:

```text
Toda52CompositionIsomorphismStatement
toda_52_eta2_composition_isomorphism_inference_rule()
```

3 derived premises:

```text
π_{i-1}^1=0                  INFERENCE
Prop.4.4 n=2 isomorphism     INFERENCE
second-summand restriction   INFERENCE
```

から:

```text
η₂∘- : π_i^3 ≅ π_i^2
```

を導出。

rejection:

```text
GIVEN zero
GIVEN isomorphism
GIVEN restriction
wrong first zero group
wrong composition
```

追加:

```text
tests/test_phase56_toda52_composition_isomorphism.py
```

focused:

```text
16 passed
```

全体回帰:

```text
2900 passed in 28.79s
```

### 状態

COMPLETE

---

## Phase 56-6：applicability / provenance / representative probe

production semantics:

```text
変更なし
```

追加:

```text
probes/probe_phase56_capabilities.py
tests/test_phase56_probe.py
```

initial GIVEN:

```text
Phase 49 base premises × 6
i≥3
Prop.4.4 decomposition map
```

合計:

```text
given premise count = 8
```

同一 run で:

```text
η₂ definition
H(η₂)=ι₃
π_{i-1}^1=0
Prop.4.4 n=2 specialization
second-summand restriction
Toda (5.2)
```

まで導出。

probe:

```text
pi_(i-1)^1=0 is derived = True
Prop.4.4 n=2 specialization is derived = True
second-summand restriction is derived = True
Toda (5.2) result is derived = True
final rule = Toda 5.2 eta_2 composition isomorphism
final premise count = 3
final premises are derived = True
pi_(i-1)^1=0 is GIVEN premise = False
Prop.4.4 specialization is GIVEN premise = False
second-summand restriction is GIVEN premise = False
Toda (5.2) result is GIVEN premise = False
given premise count = 8
derived step count = 12
derived round count = 9
fixed point = True
```

focused:

```text
tests/test_phase56_probe.py
10 passed
```

最終全体回帰:

```text
2910 passed in 29.17s
```

### 状態

COMPLETE

---

## Phase 56-7：Phase 56 completion

Phase 56 で完成:

```text
Prop.4.4 / Composition / zero-group compatibility
π_{i-1}^1=0 narrow theorem semantics
Prop.4.4 n=2, α=η₂ specialization
second-summand restriction
Toda52CompositionIsomorphismStatement
Toda (5.2) composition isomorphism
derived provenance
same-run end-to-end integration
representative probe
full regression
```

最終 capability:

```text
i≥3
↓
π_{i-1}^1=0

η₂ definition
H(η₂)=ι₃
↓
Φ:
π_{i-1}^1 ⊕ π_i^3 ≅ π_i^2

Φ|_{π_i^3}(γ)=η₂∘γ
↓
η₂∘- : π_i^3 ≅ π_i^2
```

generic inference engine:

```text
変更なし
```

追加しなかったもの:

```text
generic scalar normalization
generic direct-sum reduction
generic composition-map framework
generic isomorphism-restriction framework
Toda Lemma 5.2
stable homotopy model
generic Toda-bracket normalization
```

### 状態

COMPLETE

---

# Phase 56 completion boundary

最終全体回帰:

```text
2910 passed in 29.17s
```

representative probe:

```powershell
python -m probes.probe_phase56_capabilities
```

次:

```text
Phase 57
Toda Lemma 5.2 proof integration
```

---

# Phase 57 candidate

対象:

```text
α∈π_i(S^3)
2α=0
β∈{η₃,2ι₄,Eα}_1
```

target candidate:

```text
H(β)=E²α
2β=η₃∘Eα∘η_{i+1}
β∈π_{i+2}^3
Δ(E²α)=0
```

source material では Lemma statement と proof ending に η-index 不整合があるため、Phase 57-1 で原典・型・次元を確認する。

現在確認している依存:

```text
Lemma 4.5
Proposition 2.6
Proposition 1.4
Proposition 1.3
Corollary 3.7
(2.1)
```

候補分割:

```text
Phase 57-1
Lemma 5.2 statement / proof index / typing compatibility check

Phase 57-2
Lemma 4.5 minimum consequence needed for 2ι₃∘α=0

Phase 57-3
Proposition 2.6 minimum Hopf-invariant Toda-bracket consequence

Phase 57-4
Δ^-1(2η₂)=±ι₅ connection using independently derived Δ relation

Phase 57-5
Proposition 1.4 / Proposition 1.3 / Corollary 3.7 minimum bracket transformation chain

Phase 57-6
(2.1) + Lemma 4.5 indeterminacy-vanishing bridge

Phase 57-7
Lemma 5.2 end-to-end integration / provenance / representative probe

Phase 57-8
completion
```

実装原則:

```text
actual proof need
↓
minimum consequence
```

各 theorem の full formalization、generic Toda-bracket CAS normalization、generic coset algebra、stable homotopy model は先取りしない。

---

# 文書運用方針

```text
README.md
=
current capabilities / current status

docs/design.md
=
current architecture / semantics / boundaries

docs/development_log.md
=
chronological implementation history

docs/roadmap.md
=
future capability dependency
```
