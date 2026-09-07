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

# Phase 58：Toda (5.3) ν′ consequence

対象:

```text
ν′∈{η₃,2ι₄,η₄}_1
```

specialization:

```text
α=η₃
i=4
β=ν′
```

target:

```text
ν′∈π_6^3
H(ν′)=η₅
2ν′=η₃∘η₄∘η₅
```

Phase 57 の Lemma 5.2 proof を再実装せず、その conclusion を concrete specialization として利用する。

---

## Phase 58-1：η-family / bracket specialization compatibility

確認:

```text
TodaBracket
TodaBracketMembershipStatement
HomotopyElement
GeneratorSymbol
TodaEtaFamilyDefinitionStatement
```

で必要な concrete input を表現できる。

確認した重要境界:

```text
Phase 54 symbolic η bridge
→ ScalarSymbol のみ

Phase 58 concrete index
→ dedicated narrow specialization が必要
```

production code:

```text
変更なし
```

### 状態

COMPLETE

---

## Phase 58-2：ν′ minimum specialization representation

追加 statement:

```text
Toda53NuPrimeBracketSpecializationStatement
```

追加 rule:

```text
toda_53_nu_prime_bracket_specialization_inference_rule()
```

入力:

```text
ν′∈{η₃,2ι₄,η₄}_1
```

から:

```text
α=η₃
i=4
β=ν′
```

という Lemma 5.2 specialization data を derived にする。

Toda bracket 自体を `ν′` と同一視せず、membership を出発点とする。

focused:

```text
11 passed
```

### 状態

COMPLETE

---

## Phase 58-3：Lemma 5.2 specialization α=η₃

追加 rule:

```text
toda_53_eta3_twice_zero_inference_rule()
toda_53_nu_prime_lemma52_hopf_inference_rule()
toda_53_nu_prime_lemma52_double_inference_rule()
toda_53_nu_prime_lemma52_membership_inference_rule()
```

Phase 50 derived:

```text
π_4^3=Z/2{η₃}
```

から:

```text
2η₃=0
```

を derived にする。

その上で:

```text
H(ν′)=E²η₃
2ν′=η₃∘Eη₃∘η₅
ν′∈π_6^3
```

を導出。

focused:

```text
14 passed
```

### 状態

COMPLETE

---

## Phase 58-4：H(ν′)=η₅ bridge

追加:

```text
toda_53_eta5_iterated_suspension_bridge_inference_rule()
```

既存 concrete η-family constructor の:

```text
η_5
```

と Toda (5.3) canonical element:

```text
η₅
```

の structural 差を narrow bridge で吸収する。

```text
E²η₃=η₅
```

を derived にし、generic equality transitivity で:

```text
H(ν′)=E²η₃
E²η₃=η₅
↓
H(ν′)=η₅
```

を得る。

focused:

```text
13 passed
```

全体回帰:

```text
3035 passed in 41.19s
```

### 状態

COMPLETE

---

## Phase 58-5：2ν′=η₃∘η₄∘η₅ bridge

追加:

```text
toda_53_eta4_suspension_bridge_inference_rule()
```

既存 constructor の:

```text
η_4
```

と canonical:

```text
η₄
```

の structural 差を narrow bridge で接続し:

```text
Eη₃=η₄
```

を derived にする。

既存 generic rule:

```text
equality_preserved_under_right_composition_inference_rule()
equality_preserved_under_left_composition_inference_rule()
equality_transitivity_inference_rule()
```

を再利用して:

```text
Eη₃=η₄
↓
Eη₃∘η₅=η₄∘η₅
↓
η₃∘(Eη₃∘η₅)=η₃∘(η₄∘η₅)

2ν′=η₃∘(Eη₃∘η₅)
↓
2ν′=η₃∘η₄∘η₅
```

を導出。

composition propagation rule は出力 Relation に再適用できるため unrestricted fixed-point では使わず:

```text
find_inference_match()
apply_inference_match()
```

で one-shot application とする。

focused:

```text
15 passed
```

全体回帰:

```text
3050 passed in 40.79s
```

### 状態

COMPLETE

---

## Phase 58-6：provenance / representative probe / staged same-run

追加:

```text
probes/probe_phase58_capabilities.py
tests/test_phase58_probe.py
```

代表 output:

```text
ν′ ∈ π_6^3
H(ν′) = η₅
2ν′ = η₃∘η₄∘η₅
```

provenance:

```text
nu-prime membership derived = True
H(nu-prime)=eta_5 derived = True
2 nu-prime relation derived = True
all final results are INFERENCE = True
final results are GIVEN = False
```

same-run execution:

```text
fixed-point-safe stages complete = True
composition propagation one-shot = True
shared raw specialization = True
```

focused:

```text
tests/test_phase58_probe.py  9 passed
```

Phase 58 focused:

```text
tests/test_phase58_double_eta4_bridge.py       15 passed
tests/test_phase58_hopf_eta5_bridge.py         13 passed
tests/test_phase58_lemma52_specialization.py   14 passed
tests/test_phase58_nu_prime_specialization.py  11 passed
```

最終全体回帰:

```text
3059 passed in 38.23s
```

### 状態

COMPLETE

---

## Phase 58-7：Phase 58 completion

Phase 58 で完成:

```text
ν′ bracket membership specialization
α=η₃ / i=4 / β=ν′ recognition
2η₃=0 derived from π_4^3=Z/2{η₃}
ν′∈π_6^3
H(ν′)=E²η₃
2ν′=η₃∘Eη₃∘η₅
E²η₃=η₅
H(ν′)=η₅
Eη₃=η₄
one-shot composition propagation
2ν′=η₃∘η₄∘η₅
derived provenance
representative staged same-run
representative probe
full regression
```

generic inference engine:

```text
変更なし
```

追加しなかったもの:

```text
generic concrete η normalization
global η-name normalization
unrestricted fixed-point composition closure
generic Toda-bracket specialization framework
generic Toda-bracket coset algebra
generic inverse-image algebra
generic sign normalization
stable homotopy model
```

最終全体回帰:

```text
3059 passed in 38.23s
```

representative probe:

```powershell
python -m probes.probe_phase58_capabilities
```

### 状態

COMPLETE

---

# Phase 58 completion boundary

最終 capability:

```text
ν′∈{η₃,2ι₄,η₄}_1
↓
ν′∈π_6^3
H(ν′)=η₅
2ν′=η₃∘η₄∘η₅
```

次:

```text
Phase 59
次の concrete Toda consequence の source dependency analysis
```

target は source statement と dependency を確認してから確定する。

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


---

# Phase 59：Toda Proposition 5.3 finite-dimensional result

対象:

```text
η_n² := η_n∘η_{n+1}
π_{n+2}^n=Z/2{η_n²}
(n≥2)
```

stable `(G_2;2)=Z/2{η²}` は Phase 59 に含めない。

## Phase 59-1：dependency / compatibility check

確認した再利用対象:

```text
Phase 50  π_4^3=Z/2{η₃}
Phase 56  η₂∘- : π_i^3≅π_i^2
Phase 55  Proposition 5.1 finite-dimensional result
Phase 58  H(ν′)=η₅
Phase 45  EHP exactness
Phase 48  E injectivity consequence
Phase 46  Toda (4.5)
```

方針:

```text
η_n² は Composition
generic EtaSquare class は追加しない
generic cyclic-generator transport は追加しない
stable branch は deferred
```

### 状態

COMPLETE

---

## Phase 59-2：π_4^2=Z/2{η₂²}

```text
π_4^3=Z/2{η₃}
+
η₂∘- : π_4^3≅π_4^2
↓
π_4^2=Z/2{η₂∘η₃}
```

focused:

```text
15 passed
```

全体回帰:

```text
3074 passed
```

### 状態

COMPLETE

---

## Phase 59-3：n=3 EHP surjectivity / injectivity chain

左 branch:

```text
Δ:π_5^5→π_3^2 injective
↓
H:π_5^3→π_5^5 zero
↓
E:π_4^2→π_5^3 surjective
```

右 branch:

```text
H(ν′)=η₅
+
π_6^5=Z/2{η₅}
↓
H:π_6^3→π_6^5 surjective
↓
Δ:π_6^5→π_4^2 zero
↓
E:π_4^2→π_5^3 injective
```

最終:

```text
E:π_4^2≅π_5^3
```

focused:

```text
13 passed
```

全体回帰:

```text
3087 passed in 94.16s
```

### 状態

COMPLETE

---

## Phase 59-4：π_5^3=Z/2{η₃²}

```text
π_4^2=Z/2{η₂²}
E:π_4^2≅π_5^3
Eη₂²=η₃²
↓
π_5^3=Z/2{η₃²}
```

focused:

```text
18 passed
```

全体回帰:

```text
3105 passed in 101.33s
```

### 状態

COMPLETE

---

## Phase 59-5：n=4 suspension isomorphism

Toda (5.1):

```text
π_6^7=0
```

から E-H exactness により:

```text
E:π_5^3→π_6^4 surjective
```

Phase 48 の structural injectivity instance を narrow bridge で concrete map に接続し:

```text
E:π_5^3→π_6^4 injective
```

したがって:

```text
E:π_5^3≅π_6^4
```

focused:

```text
17 passed
```

全体回帰:

```text
3122 passed in 99.53s
```

### 状態

COMPLETE

---

## Phase 59-6：π_6^4=Z/2{η₄²}

```text
π_5^3=Z/2{η₃²}
E:π_5^3≅π_6^4
Eη₃²=η₄²
↓
π_6^4=Z/2{η₄²}
```

focused:

```text
19 passed
```

全体回帰:

```text
3141 passed in 100.75s
```

### 状態

COMPLETE

---

## Phase 59-7：n>4 stable-range finite-dimensional transport

Toda (4.5):

```text
E^(n-4):π_6^4≅π_{n+2}^n
```

から:

```text
π_{n+2}^n=Z/2{E^(n-4)η₄²}
(n≥5)
```

Phase 46 exponent の structural shape:

```text
ScalarSum(n,ScalarProduct(-1,4))
```

をそのまま保持した。

focused:

```text
18 passed
```

全体回帰:

```text
3159 passed in 110.50s
```

### 状態

COMPLETE

---

## Phase 59-8：integration / provenance / η_n² bridge

追加:

```text
TodaProp53FiniteDimensionalStatement
toda_prop53_higher_eta_squared_bridge_inference_rule()
toda_prop53_higher_eta_squared_finite_cyclic_generator_inference_rule()
toda_prop53_finite_dimensional_integration_inference_rule()
```

導出:

```text
E^(n-4)η₄²=η_n²
```

および:

```text
π_{n+2}^n=Z/2{E^(n-4)η₄²}
↓
π_{n+2}^n=Z/2{η_n²}
```

さらに n=2,3,4 branch と統合:

```text
TodaProp53FiniteDimensionalStatement
```

focused:

```text
18 passed in 19.94s
```

最終全体回帰:

```text
3177 passed in 123.99s
```

### 状態

COMPLETE

---

## Phase 59-9：Phase 59 completion

完成 capability:

```text
η_n² := η_n∘η_{n+1}
π_{n+2}^n=Z/2{η_n²}
(n≥2)
```

branch:

```text
n=2  π_4^2=Z/2{η₂²}
n=3  π_5^3=Z/2{η₃²}
n=4  π_6^4=Z/2{η₄²}
n≥5  π_{n+2}^n=Z/2{η_n²}
```

provenance:

```text
low-dimensional branches are derived
higher transport is derived
higher η-square bridge is derived
final aggregate is INFERENCE
final aggregate is not GIVEN
```

generic inference engine:

```text
変更なし
```

追加しなかったもの:

```text
EtaSquare class
generic cyclic-generator transport
generic suspension/composition normalizer
generic concrete η normalization
global scalar normalization
stable homotopy-group model
stable (G_2;2)=Z/2{η²}
```

representative probe:

```powershell
python -m probes.probe_phase59_capabilities
```

最終全体回帰:

```text
3177 passed in 123.99s
```

### 状態

COMPLETE

---

# Phase 59 completion boundary

最終 capability:

```text
π_{n+2}^n=Z/2{η_n²}
(n≥2)
```

次:

```text
next concrete Toda source statement
↓
dependency analysis
↓
current representation compatibility
↓
minimum implementation
```

stable `(G_1;2)=Z/2{η}` と stable `(G_2;2)=Z/2{η²}` は引き続き deferred。
