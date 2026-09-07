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

# Phase 49：π_3^2=Z{η₂}

導出:

```text
H injective
Δ=0
H surjective
H isomorphism
η₂ = unique H-preimage of ι₃
H(η₂)=ι₃
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

# Phase 50：π_4^3=Z/2{η₃}

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

不足 edge を具体化し、Phase 52–55 の順序を決定。

### 状態

COMPLETE

---

# Phase 52：Δ(ι₅)=±2η₂ direct bridge

```text
Δ(ι₅)=±[ι₂,ι₂]
+
[ι₂,ι₂]=±2η₂
↓
Δ(ι₅)=±2η₂
```

generic up-to-sign transitivity は導入しない。

全体回帰:

```text
2731 passed in 26.67s
```

### 状態

COMPLETE

---

# Phase 53：Toda (4.5) finite-cyclic transport

```text
π_4^3=Z/2{η₃}
+
E^(n-3): π_4^3 ≅ π_{n+1}^n
↓
π_{n+1}^n=Z/2{E^(n-3)η₃}
```

全体回帰:

```text
2769 passed in 25.60s
```

### 状態

COMPLETE

---

# Phase 54：higher η-family bridge

```text
η₃=Eη₂
+
η_n=E^(n-2)η₂
↓
E^(n-3)η₃=η_n
```

および:

```text
π_{n+1}^n=Z/2{E^(n-3)η₃}
↓
π_{n+1}^n=Z/2{η_n}
```

全体回帰:

```text
2804 passed in 26.50s
```

### 状態

COMPLETE

---

# Phase 55：Toda Proposition 5.1 finite-dimensional integration

independently derived:

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
η₂∘- : π_i^3 ≅ π_i^2
(i≥3)
```

Phase 56-1〜56-6 で:

```text
π_{i-1}^1=0
Prop.4.4 n=2, α=η₂ specialization
second-summand restriction
Toda52CompositionIsomorphismStatement
representative probe
```

を実装。

最終全体回帰:

```text
2910 passed in 29.17s
```

### 状態

COMPLETE

---

# Phase 57：Toda Lemma 5.2 proof integration

対象:

```text
α∈π_i(S^3)
2α=0
β∈{η₃,2ι₄,Eα}_1
```

canonical target:

```text
H(β)=E²α
2β=η₃∘Eα∘η_{i+1}
β∈π_{i+2}^3
Δ(E²α)=0
```

---

## Phase 57-1：statement / proof index / typing compatibility

確認:

```text
β∈π_{i+2}^3
```

および:

```text
η₃∘Eα∘η_{i+1}
```

が正しい typing を持つ。

source proof ending の `η_{i+2}` は型が合わず、直後の `α=η₃`, `i=4` specialization も `η₅` を与えるため、`η_{i+1}` を canonical target と決定。

production code:

```text
変更なし
```

### 状態

COMPLETE

---

## Phase 57-2：Lemma 4.5 minimum consequence

追加:

```text
toda_lemma45_n4_two_iota3_composition_inference_rule()
```

推論:

```text
α∈π_i(S³)
↓
2ι₃∘α=2α

2α=0
↓ generic zero propagation
2ι₃∘α=0
```

focused:

```text
10 passed
```

全体回帰:

```text
2920 passed in 30.13s
```

### 状態

COMPLETE

---

## Phase 57-3：Proposition 2.6 minimum Hopf-bracket consequence

追加:

```text
TodaProp26HopfBracketConsequenceStatement
toda_prop26_lemma52_hopf_bracket_inference_rule()
```

推論:

```text
β∈{η₃,2ι₄,Eα}_1
E(η₂∘2ι₃)=0
2ι₃∘α=0
↓
H(β) ∈ -Δ^-1(η₂∘2ι₃)∘E²α
```

`PreimageSubgroup` は変更しない。

focused:

```text
14 passed
```

全体回帰:

```text
2934 passed in 30.62s
```

### 状態

COMPLETE

---

## Phase 57-4：Δ^-1(2η₂)=±ι₅ connection

追加:

```text
TodaDeltaPreimageUpToSignStatement
toda_lemma52_delta_two_eta2_preimage_inference_rule()
```

推論:

```text
Δ(ι₅)=±2η₂
↓
Δ^-1(2η₂)=±ι₅
```

Phase 52 derived result を provenance 付きで再利用。

focused:

```text
14 passed
```

全体回帰:

```text
2948 passed in 29.78s
```

### 状態

COMPLETE

---

## Phase 57-5：Prop.1.4 / Prop.1.3 / Cor.3.7 minimum chain

追加 statement:

```text
TodaLemma52BracketCompositionMembershipStatement
TodaLemma52BracketRepresentativeStatement
```

追加 rule:

```text
toda_prop14_lemma52_bracket_transformation_inference_rule()
toda_prop13_lemma52_bracket_transformation_inference_rule()
toda_cor37_lemma52_representative_inference_rule()
```

chain:

```text
β∈{η₃,2ι₄,Eα}_1
↓ Prop.1.4
2β∈η₃∘E{2ι₃,α,2ι_i}

↓ Prop.1.3
2β∈η₃∘-{2ι₄,Eα,2ι_{i+1}}_1

↓ Cor.3.7
explicit representative
```

generic coset algebra は追加しない。

focused:

```text
17 passed
```

全体回帰:

```text
2965 passed in 30.20s
```

### 状態

COMPLETE

---

## Phase 57-6：(2.1) + Lemma 4.5 indeterminacy vanishing

追加:

```text
toda_prop51_eta4_twice_zero_inference_rule()
toda_21_lemma52_suspended_indeterminacy_zero_inference_rule()
toda_lemma45_n4_suspension_zero_reflection_inference_rule()
```

推論:

```text
Prop.5.1
↓
2η₄=0

γ∈π_{i+2}(S⁴)
↓ Toda (2.1)
E(η₃∘γ∘2ι_{i+2})=0

↓ Lemma 4.5
η₃∘γ∘2ι_{i+2}=0
```

focused:

```text
15 passed
```

全体回帰:

```text
2980 passed in 31.13s
```

### 状態

COMPLETE

---

## Phase 57-7：Lemma 5.2 end-to-end integration / provenance / probe

追加 integration rule:

```text
toda_lemma52_prop26_first_zero_inference_rule()
toda_lemma52_hopf_value_inference_rule()
toda_lemma52_double_value_inference_rule()
toda_lemma52_beta_membership_inference_rule()
toda_lemma52_delta_e2_alpha_zero_inference_rule()
```

Phase 57-3 helper の β typing を:

```text
dimension=i
```

から:

```text
dimension=i+2
source=i+2
target=3
```

へ修正。

追加:

```text
probes/probe_phase57_capabilities.py
tests/test_phase57_lemma52_integration.py
tests/test_phase57_probe.py
```

代表 output:

```text
H(β)=E²α
2β=η₃∘Eα∘η_(i+1)
β∈π_(i+2)^3
Δ(E²α)=0
```

provenance:

```text
H(beta)=E^2 alpha derived = True
2 beta relation derived = True
beta membership derived = True
Delta(E^2 alpha)=0 derived = True
all final results are INFERENCE = True
final results are GIVEN = False
fixed point = True
```

representative inference rounds:

```text
18
```

focused:

```text
tests/test_phase57_lemma52_integration.py  13 passed
tests/test_phase57_probe.py                 4 passed
```

関連:

```text
test_phase57_prop26_hopf_bracket.py            14 passed
test_phase57_delta_two_eta2_preimage.py        14 passed
test_phase57_bracket_transformation_chain.py   17 passed
test_phase57_indeterminacy_vanishing.py        15 passed
test_phase57_lemma45_two_iota3.py              10 passed
test_phase55_probe.py                           8 passed
test_toda_rules.py                             66 passed
```

最終全体回帰:

```text
2997 passed in 38.45s
```

### 状態

COMPLETE

---

## Phase 57-8：Phase 57 completion

Phase 57 で完成:

```text
Lemma 5.2 statement / index / typing verification
Lemma 4.5 minimum consequence
Proposition 2.6 minimum consequence
Δ^-1(2η₂)=±ι₅ bridge
Proposition 1.4 / Proposition 1.3 / Corollary 3.7 minimum transformation chain
Toda (2.1) + Lemma 4.5 indeterminacy vanishing
H(β)=E²α
2β=η₃∘Eα∘η_{i+1}
β∈π_{i+2}^3
Δ(E²α)=0
derived provenance
same-run end-to-end integration
representative probe
full regression
```

generic inference engine:

```text
変更なし
```

追加しなかったもの:

```text
generic Toda-bracket coset algebra
generic inverse-image algebra
generic sign normalization
generic Δ-H rewrite framework
full Prop.1.3 formalization
full Prop.1.4 formalization
full Prop.2.6 formalization
full Cor.3.7 formalization
stable homotopy model
```

最終全体回帰:

```text
2997 passed in 38.45s
```

representative probe:

```powershell
python -m probes.probe_phase57_capabilities
```

新規文書:

```text
docs/code_reference.md
```

### 状態

COMPLETE

---

# Phase 57 completion boundary

最終 capability:

```text
α∈π_i(S³)
2α=0
β∈{η₃,2ι₄,Eα}_1
↓
H(β)=E²α
2β=η₃∘Eα∘η_{i+1}
β∈π_{i+2}^3
Δ(E²α)=0
```

次:

```text
Phase 58
Toda (5.3) ν' consequence
```

---

# 文書運用方針

```text
README.md
= current capabilities / current status

docs/design.md
= current architecture / semantics / boundaries

docs/development_log.md
= chronological implementation history

docs/roadmap.md
= future capability dependency

docs/code_reference.md
= 主要ファイルの責務、主要 class / function、コード探索ガイド
```

`code_reference.md` は実装を読むための索引として運用し、細かな helper をすべて機械的に列挙する API reference にはしない。
