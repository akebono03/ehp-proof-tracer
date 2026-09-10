# EHP Proof Tracer 設計

この文書は現在のアーキテクチャ、意味論、設計境界を記録する。

過去の実装経緯は `docs/development_log.md`、将来構想は `docs/roadmap.md`、主要ファイルの責務は `docs/code_reference.md` に分離する。

---

# 1. 基本設計原則

```text
実際の数学的必要
↓
不足している最小表現
↓
必要な explicit fact / domain rule
↓
既存 generic inference engine
```

generic inference engine に数学固有の theorem knowledge を埋め込まない。

```text
representation != typing != theorem knowledge
structural equality != mathematical equality
```

Phase 71 までこの原則を維持している。

---

# 2. レイヤー分離

```text
文献由来 theorem / explicit facts
↓
domain-specific inference rules
↓
ProofStep / InferenceRule
↓
expression / statement structures
↓
homotopy / EHP data
↓
abelian-group algebra
```

主要責務:

```text
expression.py
= 式の構造

proof.py
= generic proof / inference

relation_rules.py
= generic relation propagation

homotopy_groups.py
= homotopy / Toda group and map data

toda_rules.py
= Toda-specific theorem knowledge

probes/
= representative end-to-end capability demonstration
```

詳細は `docs/code_reference.md` を参照する。

---

# 3. 式表現レイヤー

主要構造:

```text
Expression
Zero
HomotopyElement
GeneratorSymbol
Multiple
Sum
SmashProduct
WhiteheadProduct
Composition
MapApplication
Suspension
IteratedSuspension
TodaBracket
```

constructor は theorem-aware normalization を行わない。

例えば:

```text
IteratedSuspension(x,1)
```

と:

```text
Suspension(x)
```

を structural に自動同一視しない。

同様に symbolic scalar の一般 CAS normalization も行わない。

---

# 4. structural equality と mathematical equality

Python dataclass の equality は syntax tree の一致を表す。

```text
同じ syntax
→ structural equality
```

数学的に同値だが syntax が異なる場合は:

```text
explicit Relation
+
explicit inference rule
```

で接続する。

Phase 58 でも:

```text
η_4 != η₄
η_5 != η₅
```

を structural equality のまま保持し、必要な concrete branch だけ dedicated bridge で接続する。

---

# 5. ホモトピー群・群構造

現在の主な structural object:

```text
PrimaryComponent
TodaPrimaryGroup
PreimageSubgroup
FreeCyclicGroup
FiniteCyclicGroup
DirectSumGroup
```

`TodaPrimaryGroup(i,n)` は Toda 記法 `π_i^n` を保持する。

`PreimageSubgroup` は subgroup inverse image であり、specific value の `Δ^-1(x)` を表す generic object ではない。

`FiniteCyclicGroup(order,generator)` は concrete finite-cyclic calculation の最小表現であり、一般 quotient simplifier を意味しない。

---

# 6. 標準写像と instance-aware map

標準写像:

```text
EHP_E_MAP
EHP_H_MAP
EHP_DELTA_MAP
```

instance-aware map:

```text
TodaSuspensionMap
TodaHopfInvariantMap
TodaDeltaMap
TodaIteratedSuspensionMap
TodaProp44DecompositionMap
```

設計境界:

```text
specific theorem instance
!=
generic MapSymbol
```

---

# 7. generic inference engine

中心 object:

```text
Relation
ProofStep
PremisePattern
PatternVariable
InferenceRule
InferenceMatch
InferenceRunResult
```

実行:

```text
available ProofStep
↓
premise matching
↓
bindings
↓
match_guard
↓
conclusion_builder / conclusion_pattern
↓
ProofRule.INFERENCE
↓
fixed-point iteration
```

provenance は:

```text
ProofStep.premises
ProofStep.inference_rule
```

に保持する。

Phase 60 でも generic inference engine の推論機構自体は変更していない。

---

# 8. generic relation rule と theorem-specific rule の境界

`relation_rules.py` に置くもの:

```text
x=0, y=x → y=0
equality symmetry
equality transitivity
equality preservation under composition
suspension preserves equality / zero
integer multiple の generic structural bridge
```

`toda_rules.py` に置くもの:

```text
Toda Lemma 4.5
Toda Proposition 2.6
Toda Proposition 4.4
Toda Proposition 5.1
Toda Lemma 5.2
Toda (5.3) concrete specialization bridges
```

判断基準:

```text
数学 theorem 固有の知識か？
YES → domain-specific module

一般 relation mechanics か？
YES → generic relation / proof module
```

---

# 9. ±付き relation の境界

現在の dedicated statement family は concrete theorem branch で必要な ± 情報だけを保持する。

代表:

```text
TodaProp27HopfInvariantUpToSignStatement
TodaPi32WhiteheadSquareUpToSignStatement
TodaDeltaImageUpToSignStatement
TodaDeltaPreimageUpToSignStatement
```

一般化しない:

```text
PlusMinus
SignVariable
generic up-to-sign transitivity
general sign solver
```

---

# 10. η-family 設計

structural definition:

```text
TodaEtaFamilyDefinitionStatement
η_n=E^(n-2)η₂
```

Phase 54 の専用 bridge:

```text
η_n=E^(n-2)η₂
+
η₃=Eη₂
↓
E^(n-3)η₃=η_n
```

Phase 54 の symbolic bridge は `ScalarSymbol` を対象とし、concrete index を一般化しない。

Phase 58 では concrete need に限定して:

```text
Eη₃=η₄
E²η₃=η₅
```

を narrow bridge で導出する。

既存 concrete constructor は `n>=4` で:

```text
η_4
η_5
```

という structural name を持つ。一方 Toda (5.3) の canonical concrete expression は:

```text
η₄
η₅
```

を用いる。

これを global constructor 変更で統一せず、dimension / source / target / `GeneratorSymbol` identity を確認する dedicated bridge で接続する。

一般の suspension / scalar / η-name normalizer は追加しない。

---

# 11. Toda Proposition 5.1 finite-dimensional integration

専用 aggregate:

```text
TodaProp51FiniteDimensionalStatement
```

保持:

```text
pi3_2_group_relation
eta2_hopf_relation
delta_iota5_relation
higher_eta_group_relation
```

rule:

```text
toda_prop51_finite_dimensional_integration_inference_rule()
```

必要 premise:

```text
π_3^2=Z{η₂}        INFERENCE
H(η₂)=ι₃           INFERENCE
Δ(ι₅)=±2η₂         INFERENCE
π_{n+1}^n=Z/2{η_n} INFERENCE
```

Proposition 5.1 自身を premise として再投入しない。

---

# 12. Toda (5.2)

Phase 56 の target:

```text
η₂∘- : π_i^3 ≅ π_i^2
(i≥3)
```

専用 statement:

```text
Toda52CompositionIsomorphismStatement
```

依存:

```text
π_{i-1}^1=0
Prop.4.4 n=2 specialization
second-summand restriction
```

一般化しない:

```text
DirectSumGroup(A,B) + A=0 → B
generic isomorphism restriction theorem
generic composition-map framework
```

---

# 13. Phase 57 の設計目標

Toda Lemma 5.2:

```text
α∈π_i(S^3)
2α=0
β∈{η₃,2ι₄,Eα}_1
```

から:

```text
H(β)=E²α
2β=η₃∘Eα∘η_{i+1}
β∈π_{i+2}^3
Δ(E²α)=0
```

を derived provenance 付きで導出する。

---

# 14. Lemma 5.2 index 方針

canonical target は:

```text
η_{i+1}
```

とする。

理由:

```text
Eα : S^(i+1) → S^4
η_{i+1} : S^(i+2) → S^(i+1)
```

なので:

```text
η₃∘Eα∘η_{i+1}
:
S^(i+2) → S^3
```

となり `2β` と一致する。

また `α=η₃`, `i=4` specialization は:

```text
2ν′=η₃∘η₄∘η₅
```

となる。

---

# 15. Phase 57-2：Lemma 4.5 minimum consequence

```text
α∈π_i(S³)
↓
2ι₃∘α=2α

2α=0
↓ generic zero propagation
2ι₃∘α=0
```

Lemma 4.5 全体の generic formalization は行わない。

---

# 16. Phase 57-3：Proposition 2.6 minimum consequence

専用 statement:

```text
TodaProp26HopfBracketConsequenceStatement
```

Lemma 5.2 specialization:

```text
β∈{η₃,2ι₄,Eα}_1
+
E(η₂∘2ι₃)=0
+
2ι₃∘α=0
↓
H(β) ∈ -Δ^-1(η₂∘2ι₃)∘E²α
```

`PreimageSubgroup` は変更しない。

---

# 17. Phase 57-4：Δ inverse bridge

専用 statement:

```text
TodaDeltaPreimageUpToSignStatement
```

```text
Δ(ι₅)=±2η₂
↓
Δ^-1(2η₂)=±ι₅
```

これは concrete inverse-image consequence。

---

# 18. Phase 57-5：bracket transformation chain

専用 statement:

```text
TodaLemma52BracketCompositionMembershipStatement
TodaLemma52BracketRepresentativeStatement
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

TodaBracket を generic coset algebra へ拡張しない。

---

# 19. Phase 57-6：indeterminacy vanishing

Phase 55 の higher η relation から:

```text
2η₄=0
```

を derived にする。

任意の:

```text
γ∈π_{i+2}(S⁴)
```

について:

```text
E(η₃∘γ∘2ι_{i+2})=0
```

を Toda (2.1) の narrow consequence として導出。

Lemma 4.5, `n=4` の suspension injectivity から:

```text
η₃∘γ∘2ι_{i+2}=0
```

を得る。

---

# 20. Phase 57-7：end-to-end integration

Phase 55 provenance と Phase 57 rule family を接続する。

最終:

```text
H(β)=E²α
2β=η₃∘Eα∘η_{i+1}
β∈π_{i+2}^3
Δ(E²α)=0
```

すべて:

```text
ProofRule.INFERENCE
```

final results:

```text
GIVEN = False
```

representative run:

```text
18 inference rounds
FIXED_POINT
```

---

# 21. Phase 57 の sign 処理

Phase 57 では generic sign normalizer を導入しない。

必要箇所のみ、order-two η-family fact と `2α=0` を theorem-specific guard に利用する。

```text
concrete proof need
↓
narrow sign consequence
```

---

# 22. Phase 57 provenance 方針

重要中間結果を final GIVEN として再投入しない。

特に:

```text
2ι₃∘α=0
Prop.2.6 consequence
Δ^-1(2η₂)=±ι₅
bracket transformations
indeterminacy zero
H(β)=E²α
2β=...
β membership
Δ(E²α)=0
```

は inference chain で導出する。

probe:

```text
all final results are INFERENCE = True
final results are GIVEN = False
fixed point = True
```

---

# 23. Phase 57 testing

```text
test_phase57_lemma45_two_iota3.py              10 passed
test_phase57_prop26_hopf_bracket.py            14 passed
test_phase57_delta_two_eta2_preimage.py        14 passed
test_phase57_bracket_transformation_chain.py   17 passed
test_phase57_indeterminacy_vanishing.py        15 passed
test_phase57_lemma52_integration.py            13 passed
test_phase57_probe.py                           4 passed
```

関連:

```text
test_phase55_probe.py                           8 passed
test_toda_rules.py                             66 passed
```

full regression:

```text
2997 passed in 38.45s
```

---

# 24. Phase 57 completion boundary

完成:

```text
Lemma 5.2 statement / typing verification
Lemma 4.5 minimum consequence
Proposition 2.6 minimum consequence
Δ inverse minimum bridge
Proposition 1.4 / 1.3 / Cor.3.7 minimum chain
indeterminacy vanishing
end-to-end integration
provenance
representative probe
full regression
```

先取りしない:

```text
generic Toda-bracket coset algebra
generic inverse-image algebra
generic sign normalization
generic Δ-H rewrite framework
full theorem formalization beyond actual proof need
stable homotopy model
```

---

# 25. Phase 58 の設計目標

Toda (5.3) の concrete specialization:

```text
ν′∈{η₃,2ι₄,η₄}_1
```

を出発点とし、Phase 57 の Lemma 5.2 result を再利用する。

specialization:

```text
α=η₃
i=4
β=ν′
```

最終 target:

```text
ν′∈π_6^3
H(ν′)=η₅
2ν′=η₃∘η₄∘η₅
```

Toda bracket 自体と `ν′` を同一視せず:

```text
ν′∈{η₃,2ι₄,η₄}_1
```

という membership を theorem input とする。

---

# 26. Phase 58-2：ν′ specialization recognition

専用 statement:

```text
Toda53NuPrimeBracketSpecializationStatement
```

保持:

```text
nu_prime
alpha
lemma52_index
bracket_membership
```

dedicated rule:

```text
toda_53_nu_prime_bracket_specialization_inference_rule()
```

は exactly:

```text
ν′∈{η₃,2ι₄,η₄}_1
```

を認識し:

```text
α=η₃
i=4
β=ν′
```

という Lemma 5.2 specialization data を derived にする。

generic Toda-bracket specialization framework は追加しない。

---

# 27. Phase 58-3：Lemma 5.2 concrete specialization

Phase 50 の derived result:

```text
π_4^3=Z/2{η₃}
```

から:

```text
2η₃=0
```

を derived にする。

専用 rule family:

```text
toda_53_eta3_twice_zero_inference_rule()
toda_53_nu_prime_lemma52_hopf_inference_rule()
toda_53_nu_prime_lemma52_double_inference_rule()
toda_53_nu_prime_lemma52_membership_inference_rule()
```

raw conclusion:

```text
H(ν′)=E²η₃
2ν′=η₃∘Eη₃∘η₅
ν′∈π_6^3
```

Phase 57 proof 本体を再実装しない。

---

# 28. Phase 58-4：H(ν′)=η₅ bridge

concrete η-family definition を利用して:

```text
E²η₃=η₅
```

を narrow bridge で導出する。

専用 rule:

```text
toda_53_eta5_iterated_suspension_bridge_inference_rule()
```

その後は generic:

```text
equality_transitivity_inference_rule()
```

で:

```text
H(ν′)=E²η₃
E²η₃=η₅
↓
H(ν′)=η₅
```

を導出する。

Phase 54 symbolic bridge は変更しない。

---

# 29. Phase 58-5：2ν′ relation bridge

concrete η-family definition を利用して:

```text
Eη₃=η₄
```

を narrow bridge で導出する。

専用 rule:

```text
toda_53_eta4_suspension_bridge_inference_rule()
```

その後は generic relation mechanics:

```text
equality_preserved_under_right_composition_inference_rule(η₅)
equality_preserved_under_left_composition_inference_rule(η₃)
equality_transitivity_inference_rule()
```

を利用して:

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

を得る。

---

# 30. repeatable composition rule の execution scope

composition equality propagation は:

```text
Relation
↓
Relation
```

であり、同じ rule を出力へ再適用できる。

例:

```text
a=b
↓
a∘η₅=b∘η₅
↓
(a∘η₅)∘η₅=(b∘η₅)∘η₅
↓
...
```

したがって unrestricted fixed-point closure に入れると distinct expression が無限に増え得る。

Phase 58 では:

```text
find_inference_match()
+
apply_inference_match()
```

による one-shot application を使う。

設計原則:

```text
fixed-point-safe rule
→ fixed-point runner

repeatable scope-sensitive rule
→ staged / one-shot execution
```

これは generic engine の変更ではなく execution scope の選択である。

---

# 31. Phase 58-6：provenance / representative staged same-run

代表 builder:

```text
probes/probe_phase58_capabilities.py
```

は1つの representative scenario 内で:

```text
Phase 50 derived π_4^3
↓
2η₃=0

ν′ bracket membership
↓
Phase 58 specialization
↓
Phase 58-3 raw conclusions

η₅ bridge
↓
H(ν′)=η₅

η₄ bridge
↓
one-shot composition propagation
↓
2ν′=η₃∘η₄∘η₅
```

を接続する。

fixed-point-safe stage は `FIXED_POINT` に到達し、composition propagation のみ one-shot とする。

最終:

```text
ν′∈π_6^3
H(ν′)=η₅
2ν′=η₃∘η₄∘η₅
```

すべて:

```text
ProofRule.INFERENCE
```

final GIVEN:

```text
False
```

---

# 32. Phase 58 testing

```text
test_phase58_nu_prime_specialization.py       11 passed
test_phase58_lemma52_specialization.py        14 passed
test_phase58_hopf_eta5_bridge.py              13 passed
test_phase58_double_eta4_bridge.py            15 passed
test_phase58_probe.py                          9 passed
```

関連:

```text
test_relation_rules.py                        50 passed
test_toda_rules.py                            66 passed
```

full regression:

```text
3059 passed in 38.23s
```

---

# 33. Phase 58 completion boundary

完成:

```text
ν′ bracket membership specialization
α=η₃ / i=4 / β=ν′ recognition
2η₃=0 derived from π_4^3=Z/2{η₃}
raw Lemma 5.2 specialization
E²η₃=η₅ narrow bridge
H(ν′)=η₅
Eη₃=η₄ narrow bridge
one-shot composition propagation
2ν′=η₃∘η₄∘η₅
derived provenance
representative staged same-run
representative probe
full regression
```

先取りしない:

```text
generic concrete η normalization
global η-name normalization
unrestricted fixed-point composition closure
generic Toda-bracket specialization framework
generic Toda-bracket coset algebra
stable homotopy model
```

---

# 34. Phase 59：Toda Proposition 5.3 finite-dimensional result

Phase 59 の target:

```text
η_n² := η_n∘η_{n+1}
π_{n+2}^n=Z/2{η_n²}
(n≥2)
```

`η_n²` の専用 expression class は追加しない。

```text
η_n²
=
Composition(η_n,η_{n+1})
```

## 34.1 n=2 finite-cyclic transport

Phase 56 の Toda (5.2) と Phase 50 の `π_4^3=Z/2{η₃}` を再利用する。

```text
η₂∘- : π_4^3≅π_4^2
π_4^3=Z/2{η₃}
↓
π_4^2=Z/2{η₂²}
```

一般 cyclic-generator transport は追加せず、Toda (5.2) instance 専用 rule に限定する。

## 34.2 n=3 EHP chain

左 branch:

```text
Proposition 5.1
↓
Δ:π_5^5→π_3^2 injective
↓ exactness
H:π_5^3→π_5^5 zero
↓ exactness
E:π_4^2→π_5^3 surjective
```

右 branch:

```text
H(ν′)=η₅
+
π_6^5=Z/2{η₅}
↓
H:π_6^3→π_6^5 surjective
↓ exactness
Δ:π_6^5→π_4^2 zero
↓ exactness
E:π_4^2→π_5^3 injective
```

統合:

```text
E:π_4^2≅π_5^3
```

## 34.3 concrete η-square suspension bridge

必要な concrete bridge のみ追加する。

```text
Eη₂²=η₃²
Eη₃²=η₄²
```

constructor-aware global normalization はしない。

## 34.4 n=4 suspension isomorphism

```text
π_6^7=0
+
E-H exactness
↓
E:π_5^3→π_6^4 surjective
```

Phase 48 の structural source:

```text
π_(6-1)^(4-1)
```

は global scalar simplifier で `π_5^3` に変換せず、Phase 59-5 専用 bridge で concrete map に接続する。

最終:

```text
E:π_5^3≅π_6^4
```

## 34.5 n≥5 stable-range finite-dimensional transport

Phase 46 の Toda (4.5) を再利用する。

```text
E^(n-4):π_6^4≅π_{n+2}^n
```

Phase 46 の exponent は structural に:

```text
ScalarSum(
  n,
  ScalarProduct(-1,4),
)
```

として保持する。数学的に同じ `ScalarSum(n,-4)` へ global normalize しない。

まず:

```text
π_{n+2}^n=Z/2{E^(n-4)η₄²}
```

を導出する。

## 34.6 higher η-square bridge

Phase 59-8 で theorem-specific に:

```text
E^(n-4)η₄²=η_n²
```

を導出する。

`η_{n+1}` は generic family constructor を拡張せず、必要な symbolic `HomotopyElement` を局所的に構成する。

## 34.7 finite-dimensional aggregate

専用 aggregate:

```text
TodaProp53FiniteDimensionalStatement
```

保持:

```text
pi4_2_group_relation
pi5_3_group_relation
pi6_4_group_relation
higher_eta_squared_group_relation
higher_range
```

統合 premise:

```text
π_4^2=Z/2{η₂²}                 INFERENCE
π_5^3=Z/2{η₃²}                 INFERENCE
π_6^4=Z/2{η₄²}                 INFERENCE
π_{n+2}^n=Z/2{η_n²}, n≥5       INFERENCE
```

aggregate result も `ProofRule.INFERENCE`。

stable `(G_2;2)=Z/2{η²}` は含めない。

---

# 35. Phase 59 testing

Phase 59 completion 時点の focused integration:

```text
test_phase59_prop53_integration.py  18 passed
```

Phase 59-7 focused:

```text
test_phase59_eta4_squared_stable_transport.py  18 passed
```

最終 full regression:

```text
3177 passed in 123.99s
```

---

# 36. Phase 59 completion boundary

完成:

```text
π_4^2=Z/2{η₂²}
E:π_4^2≅π_5^3
π_5^3=Z/2{η₃²}
E:π_5^3≅π_6^4
π_6^4=Z/2{η₄²}
π_{n+2}^n=Z/2{E^(n-4)η₄²}, n≥5
E^(n-4)η₄²=η_n²
π_{n+2}^n=Z/2{η_n²}, n≥5
TodaProp53FiniteDimensionalStatement
derived provenance
representative probe
full regression
```

先取りしない:

```text
EtaSquare class
generic cyclic-generator transport
generic suspension-of-composition normalization
generic concrete η normalization
global scalar normalization
stable homotopy-group model
stable (G_2;2)=Z/2{η²}
```

---

# 37. テスト方針

各数学レイヤーで:

```text
representation
applicability
invalid cases
integration
provenance
representative probe
termination / execution scope
full regression
```

を確認する。

structural arithmetic を使う Phase では、数学的同値だけでなく syntax tree の shape も regression で固定する。

---

# 38. 文書運用方針

```text
README.md
= current capabilities / status

docs/design.md
= current architecture / semantics / boundaries

docs/development_log.md
= chronological implementation history

docs/roadmap.md
= future capability dependency

docs/code_reference.md
= 主要 module / class / function の責務と探索ガイド
```

current specification は latest README / design を優先する。

---

# 39. Phase 60：Toda Lemma 5.4 設計目標

Phase 60 の target:

```text
ν₄∈π_7^4
H(ν₄)=ι₇
2Eν₄=E²ν′
```

主要 dependency:

```text
Phase 58
ν′∈π_6^3
H(ν′)=η₅
2ν′=η₃∘η₄∘η₅

Phase 59
π_{n+2}^n=Z/2{η_n²}
```

Theorem 3.6、Toda (5.4)、Toda (4.8)、Whitehead correction はすべて Lemma 5.4 に必要な consequence のみに限定する。

---

# 40. Toda (5.4) の最小 value-set semantics

Phase 60-2 で追加する専用 statement:

```text
Toda54BracketUpToSignStatement
```

意味:

```text
bracket = {±positive_value}
```

対象:

```text
{η_n,2ι_(n+1),η_(n+1)}_t
=
{±E^(n-3)ν′}
```

一般化しない:

```text
generic set-valued expression
generic coset equality
generic sign variable
generic up-to-sign transitivity
```

Phase 60-3 の indeterminacy は:

```text
Toda54IndeterminacyGeneratorStatement
```

で theorem-specific に:

```text
Indeterminacy(B)=<x>
```

を保持する。

Toda (4.7) と Proposition 5.3 から:

```text
<η_n∘η_(n+1)∘η_(n+2)>
```

を導出し、Phase 58 の:

```text
2ν′=η₃∘η₄∘η₅
```

を narrow suspension transport して:

```text
2E^(n-3)ν′
=
η_n∘η_(n+1)∘η_(n+2)
```

を得る。

したがって:

```text
Indeterminacy(B)=<2E^(n-3)ν′>
```

となる。

---

# 41. bracket inclusion と t=0 bridge

Phase 60-4 は既存:

```text
TodaBracketMembershipStatement
```

を再利用する。

ν′ の bracket definition、Proposition 1.3、Toda (1.15) から:

```text
E^(n-3)ν′
∈
{η_n,2ι_(n+1),η_(n+1)}_t
```

を theorem-specific rule で導出する。

Phase 60-5 では Toda (3.2) から:

```text
E:π_(n+2)^n→π_(n+3)^(n+1)
```

の `n≥3` surjectivity を専用 consequence として導出し、Toda (1.15) と接続する。

`t=0` は current representation では unindexed `TodaBracket` として保持する。

一般の indexed bracket equivalence や generic bracket-index normalization は追加しない。

---

# 42. Theorem 3.6 specialization と α*

Phase 60-6 は Theorem 3.6 全体を formalize しない。

専用 statement:

```text
Toda36Lemma54SpecializationStatement
```

保持:

```text
α=η₂
β=2ι₃
α*
α*∈π_7^4
-2Eα*∈{η₅,2ι₆,η₆}_3
```

Phase 60-5 Toda (5.4) の `n=5,t=3` specialization と接続して:

```text
2Eα*=±E²ν′
```

を:

```text
TodaLemma54DoubleSuspensionUpToSignStatement
```

で保持する。

この statement は Lemma 5.4 専用であり、generic sign equality object ではない。

---

# 43. Hopf parity と Whitehead correction

Phase 60-7 の専用 statement:

```text
TodaLemma54HopfOddMultipleStatement
```

意味:

```text
H(α*)=(2s+1)ι₇
```

field:

```text
alpha_star
parameter=s
generator=ι₇
```

`s` を Phase 60-8 の correction へそのまま渡す。

Phase 60-8 では:

```text
TodaLemma54WhiteheadCorrectionDataStatement
TodaLemma54Nu4BranchFormula
TodaLemma54Nu4ConstructionStatement
```

を使用する。

Whitehead data:

```text
H[ι₄,ι₄]=(-1)^u2ι₇
E[ι₄,ι₄]=0
```

positive branch:

```text
ν₄=α* - (-1)^u s[ι₄,ι₄]
```

negative branch:

```text
ν₄=-α* + (-1)^u(s+1)[ι₄,ι₄]
```

`Multiple.coefficient` を symbolic sign product 全般へ拡張せず、branch formula を theorem-specific descriptor として保持する。

両 branch から:

```text
ν₄∈π_7^4
H(ν₄)=ι₇
2Eν₄=E²ν′
```

を derived にする。

一般化しない:

```text
generic Whitehead Hopf algebra
generic symbolic coefficient simplifier
generic piecewise theorem engine
generic sign solver
```

---

# 44. Lemma 5.4 aggregate と literature metadata

Phase 60-9 の最終 aggregate:

```text
TodaLemma54Statement
```

保持:

```text
nu4
membership
hopf_relation
double_suspension_relation
literature_statements
```

premise:

```text
ν₄∈π_7^4        INFERENCE
H(ν₄)=ι₇        INFERENCE
2Eν₄=E²ν′       INFERENCE
```

aggregate 自身も:

```text
ProofRule.INFERENCE
```

であり Lemma 5.4 を `GIVEN` として再投入しない。

`proof.py` に追加した generic metadata:

```text
LiteratureStatement
```

field:

```text
reference: LiteratureReference
statement: str
```

責務:

```text
LiteratureReference
= 文献のどこか

LiteratureStatement
= その場所で利用する数学 statement
```

これは theorem knowledge を generic inference engine に入れるものではない。

Phase 60-10 probe では `LiteratureStatement` に保存した statement に加え、probe-local な locator→usage mapping を使って:

```text
Reference
Locator
Author
Source
Year
Used in: Phase 60-x ...
Statement
```

を表示する。

`Used in` は current Phase 60 representative display metadata であり、`LiteratureStatement` schema には入れない。

Phase 60-10 ではさらに probe-local presentation として:

```text
print_phase60_derivation_chain()
```

を追加した。表示順は:

```text
Result
↓
Proof-style derivation
↓
Provenance / integration
↓
Literature statements used
↓
Completion boundary
```

とする。

`Proof-style derivation` は current `ProofStep` graph から自動生成しているわけではない。Phase 60 の推論意味論を壊さずに、人間が Toda の証明順を読めるよう probe に手書きした presentation-only layer である。

---

# 45. Phase 60 testing / representative probe

representative probe:

```powershell
python -m probes.probe_phase60_capabilities
```

最終表示:

```text
ν₄ ∈ π_7^4
H(ν₄) = ι₇
2Eν₄ = E²ν′
```

provenance:

```text
ν₄ membership derived = True
H(ν₄)=ι₇ derived = True
2Eν₄=E²ν′ derived = True
final aggregate derived = True
final aggregate is GIVEN = False
all final premises are INFERENCE = True
fixed point = True
```

literature display:

```text
Literature statements used
Used in:
Statement:
```

focused final suites:

```text
test_phase60_toda36_specialization.py       20 passed
test_phase60_toda48_hopf_parity.py          18 passed
test_phase60_nu4_whitehead_correction.py     19 passed
test_phase60_lemma54_integration.py          20 passed
test_phase60_probe.py                        16 passed
```

最終 full regression:

```text
3334 passed in 132.72s
```

---

# 46. Phase 60 completion boundary

完成:

```text
Toda (5.4) t≥1 up-to-sign bracket value
Toda (5.4) t=0 bridge
Theorem 3.6 Lemma 5.4 specialization
2Eα*=±E²ν′
H(α*)=(2s+1)ι₇
Whitehead correction branches
ν₄∈π_7^4
H(ν₄)=ι₇
2Eν₄=E²ν′
TodaLemma54Statement
LiteratureStatement
reference statement display
Used in display
representative probe
full regression
```

先取りしない:

```text
generic Toda-bracket coset algebra
generic sign solver
generic divisibility framework
generic existential witness framework
generic Whitehead correction algebra
full Theorem 3.6 formalization
full Toda (4.8) formalization
theorem statement repository / search
Toda Lemma 5.5
```

---

# 47. Phase 61：Toda Lemma 5.5 設計

Phase 61 target:

```text
β∈π_(t+2)(S^m)
β∘η_(t+2)=0
t>0
↓
{η_(m+2),E³β,η_(t+5)}_3
contains
±(E²β∘E^tν₄)
```

基本方針:

```text
Phase 60 の α* / ν₄ provenance を再利用
↓
Lemma 5.5 に必要な minimum consequence のみ追加
↓
generic sign / bracket algebra は追加しない
```

## 47.1 contains-up-to-sign semantics

追加:

```text
TodaLemma55BracketContainsUpToSignStatement
```

意味:

```text
bracket contains x or -x
```

これは Phase 60 の:

```text
Toda54BracketUpToSignStatement
= bracket value set is {±x}
```

とは区別する。Lemma 5.5 は bracket 全体を `{±x}` と同定しないため、既存 Phase 60 statement の流用は意味を強くしすぎる。

field は:

```text
bracket
positive_value
```

のみとし、`β / m / t / ν₄` は expression tree から検査する。

## 47.2 α* bracket inclusion

Phase 60 の derived:

```text
Toda36Lemma54SpecializationStatement
```

を provenance anchor として利用し、Lemma 5.5 hypotheses:

```text
β∈π_(t+2)(S^m)
β∘η_(t+2)=0
t≥1
```

から:

```text
{η_(m+2),E³β,η_(t+5)}_3
contains
±(E²β∘E^tα*)
```

を theorem-specific rule で導出する。

`α*` を新規 `GIVEN` として再投入しない。full Theorem 3.6 formalization も行わない。

## 47.3 ν₄ suspension correction

Phase 60 の:

```text
TodaLemma54Nu4ConstructionStatement
```

には:

```text
alpha_star
nu4
whitehead_data
positive_branch
negative_branch
```

が保持される。

さらに:

```text
whitehead_data.suspension_zero_relation
= E[ι₄,ι₄]=0
```

を利用して、`t≥1` のもとで:

```text
E^tν₄=±E^tα*
```

を導出する。

専用 statement:

```text
TodaLemma55SuspensionUpToSignStatement
```

を用い、generic sign solver / symbolic Whitehead correction algebra は追加しない。

## 47.4 α* → ν₄ composition bridge

入力:

```text
bracket contains ±(E²β∘E^tα*)
E^tν₄=±E^tα*
```

結論:

```text
bracket contains ±(E²β∘E^tν₄)
```

ここでも generic up-to-sign transitivity を追加しない。Lemma 5.5 専用 bridge として実装する。

## 47.5 final aggregate

追加:

```text
TodaLemma55Statement
```

保持:

```text
nu4
lemma54_statement
beta_membership
beta_eta_zero_relation
t_range
bracket_inclusion
literature_statements
```

`lemma54_statement` を nested に保持することで:

```text
Lemma 5.4 で構成された ν₄
=
Lemma 5.5 final inclusion の ν₄
```

を theorem-level provenance で固定する。

final integration は derived `TodaLemma54Statement` と derived final inclusion を要求する。

## 47.6 literature provenance

Phase 61 direct literature:

```text
Toda Lemma 5.5
Toda Lemma 5.5 proof
```

を `LiteratureStatement` として保持する。

Phase 60 literature は:

```text
TodaLemma55Statement
└─ lemma54_statement
   └─ literature_statements
```

から継承する。

`Used in:` は Phase 60 と同じく probe-local display metadata とし、`LiteratureStatement` schema は変更しない。

## 47.7 hypotheses と derived theorem dependency の境界

Lemma 5.5 の theorem hypotheses:

```text
β membership
β∘η_(t+2)=0
t≥1
```

は `ProofRule.GIVEN` でよい。

一方、derived spine:

```text
Phase 60 α*
Phase 60 ν₄ construction
Phase 60 Lemma 5.4 aggregate
Phase 61 α* bracket inclusion
Phase 61 suspension bridge
Phase 61 ν₄ bracket inclusion
Phase 61 Lemma 5.5 aggregate
```

は `ProofRule.INFERENCE` を維持する。

「hypothesis が GIVEN」と「final theorem result を GIVEN に戻す」は区別する。

## 47.8 provenance acyclicity

Phase 61-7 regression では final aggregate から premise ancestry を走査し:

```text
final step が自分自身の ancestor ではない
final conclusion が ancestor conclusions に存在しない
```

ことを確認する。

また:

```text
Phase 61-5 → Phase 61-3 / 61-4
Phase 61-3 → Phase 60 Theorem 3.6 specialization
Phase 61-4 → Phase 60 ν₄ construction
Phase 61-6 → Phase 60 Lemma 5.4 aggregate
```

への provenance reachability を regression で固定する。

## 47.9 representative probe

`probes/probe_phase61_capabilities.py` は Phase 61-6 integration builder を再利用する。

表示:

```text
Result
Proof-style derivation
Provenance / integration
Literature statements used
Phase 61 completion boundary
```

Phase 61 aggregate では theorem dependencies と hypotheses が混在するため、Phase 60 の `all final premises are INFERENCE` 表示を流用せず:

```text
theorem dependencies are INFERENCE = True
Lemma 5.5 hypotheses remain GIVEN = True
```

と分離する。

proof-style derivation は Phase 60 と同様に presentation-only の hand-authored output であり、自動 proof narrative generator ではない。

## 47.10 Phase 61 completion boundary

実装:

```text
contains-up-to-sign semantics
α* bracket inclusion
E^tν₄=±E^tα*
α*→ν₄ composition bridge
TodaLemma55Statement
literature-aware provenance
applicability rejection
acyclic provenance regression
representative proof-style probe
```

追加しない:

```text
generic Toda-bracket containment algebra
generic up-to-sign transitivity
generic sign solver
generic Whitehead correction algebra
full Theorem 3.6 formalization
automatic proof narrative generation
Toda (5.5) ν-family calculation
```

---

# 48. 将来の proof narrative generation

Phase 60 と Phase 61 で、手書きの proof-style representative が2つ蓄積した。

現在利用可能な情報:

```text
ProofStep / premises
Expression の構造
InferenceRule / provenance
LiteratureStatement
probe-local Used in metadata
```

将来 target:

```text
ProofStep graph
↓
目的 conclusion へ至る dependency path の選択
↓
同種 step の圧縮 / grouping
↓
式連鎖の生成
↓
利用箇所への literature citation 挿入
↓
InferenceRule ごとの narrative template 適用
↓
自然言語の接続
↓
console / Markdown / LaTeX 出力
```

Phase 61 は特に:

```text
explicit hypotheses
+ inherited theorem provenance
+ local bridge
+ final aggregate
```

という display pattern を追加した。これが今後の concrete proof でも反復するかを確認してから generic schema に抽象化する。

proof narrative generation が inference semantics を変更してはならない。presentation layer は proof semantics から分離する。

---

# 49. 次の設計境界

Phase 61 implementation は完了。

次は:

```text
Phase 62
ν-family / Toda (5.5)
```

finite-dimensional target:

```text
ν_n:=E^(n-4)ν₄
(n≥4)

n≥5:
2ν_n=E^(n-3)ν′
4ν_n=η_n³
```

最初に確認する dependency:

```text
Lemma 5.4
2Eν₄=E²ν′

Phase 58
2ν′=η₃∘η₄∘η₅

η-family / η² transport
Composition / IteratedSuspension
```

stable `ν` / `η³` branch は stable homotopy model が必要なら finite-dimensional branch と分離する。

generic sign solver、generic Toda-bracket algebra、automatic proof narrative generator、theorem repository は concrete need が生じるまで保留する。

---

# 50. Phase 62：ν-family / Toda (5.5) finite-dimensional 設計

Phase 62 の finite-dimensional target:

```text
ν_n:=E^(n-4)ν₄
(n≥4)

n≥5:
2ν_n=E^(n-3)ν′
4ν_n=η_n³
```

stable:

```text
ν:=E^∞ν₄
4ν=η³
```

は separate deferred boundary とする。

---

# 51. ν-family definition semantics

追加:

```text
TodaNuFamilyDefinitionStatement
```

保持:

```text
index
element
iterated_suspension
```

helper:

```text
toda_nu_family_definition_statement(n)
```

意味:

```text
ν_n:=E^(n-4)ν₄
```

concrete boundary:

```text
n≥4
```

symbolic `n-4` は:

```text
ScalarSum(n,-4)
```

として保持する。

一般 scalar normalization は導入しない。

---

# 52. double-value transport semantics

専用 rule:

```text
toda_55_nu_family_double_suspension_transport_inference_rule()
```

premise:

```text
TodaLemma54Statement                INFERENCE
TodaNuFamilyDefinitionStatement
ScalarGreaterEqualStatement(n,5)
```

Lemma 5.4 の exact relation:

```text
2Eν₄=E²ν′
```

を確認し:

```text
2ν_n=E^(n-3)ν′
```

を導出する。

これは Toda (5.5) 専用 transport であり、generic suspension exponent algebra ではない。

---

# 53. 4ν_n=η_n³ bridge

新しい Toda-specific theorem rule は追加しない。

generic relation mechanics:

```text
equality_preserved_under_multiple_inference_rule(2)
nested_integer_multiple_inference_rule(2,2,ν_n)
equality_symmetry_inference_rule()
equality_transitivity_inference_rule()
```

を staged に使う。

```text
2ν_n=E^(n-3)ν′
↓ ×2
2(2ν_n)=2E^(n-3)ν′

2(2ν_n)=4ν_n
↓
4ν_n=2E^(n-3)ν′
```

Phase 60:

```text
2E^(n-3)ν′
=
η_n∘η_(n+1)∘η_(n+2)
```

と transitivity で:

```text
4ν_n=η_n³
```

を得る。

`η_n³` は dedicated expression class ではなく right-associated `Composition`。

---

# 54. Phase 62 applicability boundary

区別:

```text
ν-family definition:
n≥4

Toda (5.5) finite-dimensional relations:
n≥5
```

`n=4` は family definition として valid だが Toda (5.5) relation transport には不適用。

explicit input:

```text
ν-family definition  GIVEN
n≥5                  GIVEN
```

theorem dependency:

```text
Lemma 5.4            INFERENCE
2ν_n relation        INFERENCE
4ν_n relation        INFERENCE
```

---

# 55. Toda (5.5) finite-dimensional aggregate

追加:

```text
Toda55NuFamilyFiniteDimensionalStatement
```

保持:

```text
nu_family_definition
lemma54_statement
n_range
double_nu_relation
quadruple_nu_relation
literature_statements
```

integration:

```text
toda_55_nu_family_finite_dimensional_integration_inference_rule()
```

direct premises:

```text
TodaLemma54Statement                INFERENCE
TodaNuFamilyDefinitionStatement     GIVEN
ScalarGreaterEqualStatement(n,5)    GIVEN
2ν_n=E^(n-3)ν′                      INFERENCE
4ν_n=η_n³                           INFERENCE
```

final aggregate:

```text
INFERENCE
```

Lemma 5.4 を nested に保持し Phase 60 literature provenance を切らない。

---

# 56. Phase 62 literature provenance

direct literature:

```text
Toda (5.5)
Equation (5.5)
```

finite-dimensional clause のみを direct statement とする。

stable clause:

```text
4ν=η³
```

は Phase 62 aggregate に含めない。

Phase 60 literature は:

```text
Toda55NuFamilyFiniteDimensionalStatement
└─ lemma54_statement
   └─ literature_statements
```

から継承する。

---

# 57. Phase 62 non-circular provenance

actual `ProofStep.premises` graph を identity ベースで確認する。

```text
Toda (5.5) aggregate
↓
Phase 62-3
↓
Phase 60 Lemma 5.4
```

および:

```text
Toda (5.5) aggregate
↓
Phase 62-4
↓
Phase 60 triple-η transport
↓
Phase 58 2ν′ relation
```

を ancestor reachability で固定する。

non-circular conditions:

```text
final aggregate not in ancestors(final aggregate)
final aggregate not in ancestors(2ν_n relation)
final aggregate not in ancestors(4ν_n relation)
final aggregate conclusion absent from ancestor conclusions
```

generic semantic cycle detector は追加しない。

---

# 58. Phase 62 representative probe

追加:

```text
probes/probe_phase62_capabilities.py
```

表示:

```text
Result
Proof-style derivation
Provenance / integration
Literature statements used
Phase 62 completion boundary
```

theorem logic は focused integration builder を再利用し、probe 側へ複製しない。

proof-style derivation は presentation-only の hand-authored output。

---

# 59. Phase 62 completion boundary

完成:

```text
TodaNuFamilyDefinitionStatement
ν_n:=E^(n-4)ν₄
n≥4
2ν_n=E^(n-3)ν′, n≥5
4ν_n=η_n³, n≥5
Toda55NuFamilyFiniteDimensionalStatement
Toda (5.5) direct literature
Phase 60 inherited literature
applicability regression
acyclic provenance regression
representative proof-style probe
```

先取りしない:

```text
stable ν:=E^∞ν₄
4ν=η³
stable homotopy-group model
generic ν-family framework
generic suspension exponent algebra
generic η-cube class
automatic proof narrative generation
Toda (5.6)
```

最終 full regression:

```text
3550 passed in 411.22s
```

---

# 60. 次の設計境界

Phase 63:

```text
Toda (5.6)
```

target:

```text
(α,β)
↦
Eα+ν₄∘β
:
π_{i-1}^3 ⊕ π_i^7
≅
π_i^4
```

dependency:

```text
Phase 47 Proposition 4.4 decomposition
+
Phase 60 ν₄ / H(ν₄)=ι₇
↓
n=4, α=ν₄ specialization
```

generic direct-sum framework extension、generic specialization engine、stable ν、automatic proof narrative generation は先取りしない。



---

# 61. Phase 63：Toda (5.6) ν₄ decomposition

Phase 63 target:

```text
(α,β)
↦
Eα+ν₄∘β
:
π_{i-1}^3 ⊕ π_i^7
≅
π_i^4
```

依存:

```text
Phase 47 Proposition 4.4 decomposition
+
Phase 60 Toda Lemma 5.4
ν₄∈π_7^4
H(ν₄)=ι₇
```

Phase 47 generic rule 自体は変更しない。

理由は `n=4` specialization で:

```text
2n-1
n-1
ι_(2n-1)
```

と concrete:

```text
7
3
ι₇
```

が structural equality では一致しないため。

これを generic scalar / generator normalizer で吸収せず、Toda (5.6) 専用 bridge で接続する。

---

# 62. Phase 63-2：ν₄ specialization premise bridge

追加:

```text
Toda56Nu4Prop44SpecializationStatement
```

保持:

```text
lemma54_statement
n=4
alpha=ν₄
TodaPrimaryGroupMembershipStatement(ν₄, π_7^4)
H(ν₄)=ι₇
```

rule:

```text
toda_56_nu4_prop44_specialization_inference_rule()
```

Phase 60 の:

```text
HomotopyGroupMembershipStatement(ν₄,7,4)
```

を Phase 47 compatible な:

```text
TodaPrimaryGroupMembershipStatement(ν₄, π_7^4)
```

へ narrow conversion する。

generic membership normalization は追加しない。

specialization 自体は:

```text
ProofRule.INFERENCE
```

とする。

---

# 63. Phase 63-3：Toda Proposition 4.4 decomposition specialization

既存:

```text
DirectSumGroup
TodaPrimaryGroup
TodaProp44DecompositionMap
TodaProp44IsomorphismStatement
```

を再利用する。

concrete symbolic map:

```text
source:
π_(i-1)^3 ⊕ π_i^7

target:
π_i^4

formula:
Eα+ν₄∘β
```

内部の Phase 47 field 名では:

```text
decomposition_map.beta  = 表示上の α
decomposition_map.gamma = 表示上の β
```

となる。

map instance は structural input として:

```text
TodaProp44DecompositionMap GIVEN
```

とし、この map が isomorphism であるという theorem result は:

```text
TodaProp44IsomorphismStatement INFERENCE
```

とする。

---

# 64. Phase 63-4：Toda (5.6) map / isomorphism semantics

追加:

```text
Toda56Nu4DecompositionIsomorphismStatement
```

保持:

```text
prop44_isomorphism
```

map / source / target / formula は二重保存せず:

```text
statement
↓
prop44_isomorphism
↓
map
↓
source_group / target_group / formula
```

と辿る。

recognition rule:

```text
toda_56_nu4_decomposition_isomorphism_inference_rule()
```

は Phase 63-3 derived `TodaProp44IsomorphismStatement` のみを premise にする。

---

# 65. Phase 63-5：applicability / provenance

actual `ProofStep.premises` graph を identity ベースで確認する。

主要 provenance:

```text
Toda56Nu4DecompositionIsomorphismStatement
↓
TodaProp44IsomorphismStatement
↓
Toda56Nu4Prop44SpecializationStatement
↓
TodaLemma54Statement
↓
Phase 60 derived ν₄ facts
```

別 branch:

```text
TodaProp44IsomorphismStatement
↓
TodaProp44DecompositionMap GIVEN
```

確認:

```text
GIVEN Lemma 5.4 rejected
GIVEN specialization rejected
GIVEN Prop.4.4 isomorphism rejected
final graph acyclic
final conclusion absent from ancestors
upstream branches do not depend on final
```

---

# 66. Phase 63-6：literature-aware aggregate

追加:

```text
Toda56Nu4DecompositionStatement
```

保持:

```text
decomposition_isomorphism
lemma54_statement
literature_statements
```

integration:

```text
toda_56_nu4_decomposition_integration_inference_rule()
```

direct premises:

```text
Toda56Nu4DecompositionIsomorphismStatement  INFERENCE
TodaLemma54Statement                        INFERENCE
```

final aggregate:

```text
INFERENCE
```

direct literature:

```text
Toda (5.6)
Equation (5.6)
```

statement:

```text
(α,β)↦Eα+ν₄∘β
π_(i-1)^3⊕π_i^7≅π_i^4
```

Phase 60 literature は:

```text
Toda56Nu4DecompositionStatement
└─ lemma54_statement
   └─ literature_statements
```

として inherited provenance を保持する。

---

# 67. Phase 63-7：representative probe

追加:

```text
probes/probe_phase63_capabilities.py
```

表示:

```text
Result
Proof-style derivation
Provenance / integration
Literature statements used
Phase 63 completion boundary
```

representative derivation:

```text
Phase 60 Lemma 5.4
↓
Phase 63-2 ν₄ specialization
↓
Phase 63-3 Proposition 4.4 specialization
↓
Phase 63-4 Toda (5.6) semantics
↓
Phase 63-6 literature-aware aggregate
```

proof-style derivation は引き続き presentation-only の hand-authored output。

---

# 68. Phase 63 completion boundary

完成:

```text
Toda56Nu4Prop44SpecializationStatement
Toda56Nu4DecompositionIsomorphismStatement
Toda56Nu4DecompositionStatement
n=4 / α=ν₄ specialization
π_(i-1)^3 ⊕ π_i^7 ≅ π_i^4
(α,β)↦Eα+ν₄∘β
Toda (5.6) direct literature
Phase 60 inherited literature
applicability regression
acyclic provenance regression
representative proof-style probe
```

重要境界:

```text
theorem dependency = INFERENCE
structural decomposition map = GIVEN
```

先取りしない:

```text
generic Proposition 4.4 specialization framework
generic scalar normalization
generic membership normalization
generic direct-sum simplification
stable ν:=E^∞ν₄
stable 4ν=η³
automatic proof narrative generation
later Toda consequences after Equation (5.6)
```

最終 full regression:

```text
3657 passed in 939.47s
```

---


# 69. Phase 64：performance stabilization

Phase 64 は数学 capability を追加する Phase ではない。

目的:

```text
既存 semantics
+
provenance
+
test coverage
を維持したまま
regression performance を安定化する
```

性能改善でも:

```text
推測で最適化しない
↓
pytest --durations
↓
cProfile
↓
重複計算を特定
↓
最小変更
↓
same-machine benchmark
↓
full regression
```

を原則とする。

current-machine baseline:

```text
3657 passed in 259.11s
```

---

# 70. Phase 64：deterministic builder caching

Phase 57–63 の一部 builder は:

```text
no-arg
deterministic
returned graph を caller が mutate しない
```

ため:

```text
lru_cache(maxsize=1)
```

で同一 proof graph の再構築を避ける。

identity-based provenance regression がある Phase では、同一 nested `ProofStep` graph の再利用とも整合する。

---

# 71. Phase 64：premise-binding rematch elimination

profiling で:

```text
recursive premise search
↓
merged bindings を計算
↓
bindings を破棄
↓
same premises を再 binding
```

という重複を確認した。

private helper:

```text
_find_all_matching_premise_bindings()
```

で:

```text
matched premises
+
merged bindings
```

を同時に返す。

`find_all_matching_premises()` の public behavior は維持し、`find_inference_matches_for_rule()` が既存 bindings を再利用する。

変更しない:

```text
matching semantics
binding consistency
guard evaluation
conclusion generation
provenance
fixed-point semantics
```

agenda/worklist や premise-type indexing は導入しない。

---

# 72. Phase 64：algebra crosscheck precomputation

`tests/test_algebra.py` の exhaustive crosscheck は:

```text
finite explicit enumeration
vs
presentation / integer-lattice calculation
```

という independent regression oracle を維持する。

coverage は削減しない。

維持:

```text
group case set
matrix entry ranges
checked-count lower bounds
enumeration-vs-presentation comparison
```

再利用:

```text
same image_subgroup()
same image_lattice_basis()
same kernel_lattice_basis()
shared kernel lattice for kernel/image presentation
```

production `GroupMap` cache は追加しない。

理由:

```text
GroupMap mutable
matrix mutable
```

であり、cache invalidation semantics の変更は Phase 64 の最小変更を超えるため。

---

# 73. Phase 64 completion boundary

same-machine progression:

```text
259.11s
↓
150.42s
↓
81.79s
↓
43.54s
↓
42.67s
↓
40.69s
↓
29.97s
```

final:

```text
3657 passed in 29.97s
```

baseline から約 88.4% 短縮。

algebra:

```text
109 passed in 7.46s
```

Phase 64 では追加しない:

```text
new Toda theorem semantics
agenda/worklist inference engine
premise-type index
global proof cache
global GroupMap cache
SNF/HNF algorithm replacement
coverage reduction
automatic proof narrative generation
```

数学的 frontier は Phase 63 Toda (5.6) のまま。

---

# 74. 次の設計境界

Phase 64 は COMPLETE。

次の数学 Phase は Equation (5.6) 後の concrete Toda statement / consequence を source から確認し:

```text
source statement
↓
dependency analysis
↓
current representation compatibility
↓
minimum implementation
```

の順で進める。

Phase 64 で deferred とした performance architecture も、再び concrete bottleneck になるまで追加しない。


次 Phase は Equation (5.6) の後に続く concrete Toda statement / consequence を確認し、まず:

```text
source statement
↓
dependency analysis
↓
current representation compatibility
↓
minimum implementation
```

の順で進める。

Phase 63 で deferred とした generic framework は、次の concrete theorem で実際に必要になるまで追加しない。


---

# 75. Phase 65：Toda Proposition 5.6 finite-dimensional integration

Phase 65 の設計目標は、Toda Proposition 5.6 の有限次元部分を、既存 Phase 58–63 の provenance を切らずに導出・統合することである。

最終 target:

```text
π_5^2=Z/2{η₂³}
π_6^3=Z/4{ν′}
π_7^4=Z{ν₄}⊕Z/4{Eν′}
π_(n+3)^n=Z/8{ν_n}
(n≥5)
```

設計方針:

```text
concrete proof need
↓
theorem-specific narrow rule
↓
existing generic inference mechanics
```

を維持し、Phase 65 でも generic order solver / generic quotient solver / generic specialization engine は追加しない。

---

# 76. Phase 65 の推論と Toda 証明の関係

current engine は Toda の証明文を単に順番通り表示するだけではない。

実行モデル:

```text
GIVEN facts / hypotheses
+
formalized InferenceRule
↓
premise matching
↓
applicable rule selection
↓
new ProofStep
↓
fixed-point / staged execution
```

したがって final conclusion 自体を `GIVEN` として検算しているわけではない。

一方で、現在どの `InferenceRule` を formalize するか、どの theorem consequence が必要かの設計は Toda の proof dependency を人間が読んで決めている。

現在地:

```text
proof-rule inventory
= human-guided from Toda

rule application / derived-step construction
= automatic

proof-strategy discovery from an arbitrary goal
= not yet automatic
```

---

# 77. Phase 65-3：Equation (5.7) / EHP chain

Phase 65 では:

```text
H(ν′∘η₆)=η₅²
π_7^5=Z/2{η₅²}
```

から:

```text
H:π_7^3→π_7^5 surjective
```

を導出する。

使用する EHP segment:

```text
π_7^3 ─H→ π_7^5 ─Δ→ π_5^2 ─E→ π_6^3 ─H→ π_6^5
```

exactness から:

```text
H surjective
↓
Δ=0
↓
E:π_5^2→π_6^3 injective
```

を導出する。

probe では完全列を縦に分割せず、この connected sequence の形で表示する。

---

# 78. Phase 65 order semantics boundary

Phase 65 の具体的 order derivation:

```text
ord(η₃³)=2
2ν′=η₃³
↓
ord(ν′)=4
```

および:

```text
π_6^3=Z/4{ν′}
E² injective
↓
ord(E²ν′)=4

2ν₅=E²ν′
↓
ord(ν₅)=8
```

は theorem-specific rule とする。

追加しない:

```text
generic exact-order solver
generic order transport under arbitrary injective maps
generic ord(kx) arithmetic
```

複数 independent branches で同一 generic need が繰り返し現れるまで generalize しない。

---

# 79. Phase 65 quotient / cardinality boundary

n=5 branch:

```text
π_8^5/E²π_6^3≅Z/2
E²:π_6^3→π_8^5 injective
π_6^3=Z/4{ν′}
↓
|E²π_6^3|=4
↓
|π_8^5|=8
```

および:

```text
ord(ν₅)=8
↓
π_8^5=Z/8{ν₅}
```

は Proposition-5.6-specific rule で扱う。

`QuotientGroup` の concrete algebra layer を symbolic Toda group に無理に流用しない。

追加しない:

```text
generic symbolic quotient object
generic subgroup-cardinality solver
generic extension solver
```

---

# 80. Phase 65 stable transport boundary

Toda (4.5):

```text
E^(n-5):π_8^5≅π_(n+3)^n
```

により:

```text
π_(n+3)^n=Z/8{E^(n-5)ν₅}
```

を導出する。

その後:

```text
ν₅=Eν₄
ν_n=E^(n-4)ν₄
↓
E^(n-5)ν₅=ν_n
```

を dedicated ν-family bridge で接続する。

generic:

```text
E^a(E^b x)=E^(a+b)x
```

normalizer は追加しない。

---

# 81. Phase 65 aggregate

final aggregate:

```text
TodaProp56FiniteDimensionalStatement
```

は次を保持する。

```text
π_5^2 group relation
π_6^3 group relation
π_7^4 group relation
π_8^5 group relation
higher ν group relation
n≥6 scope
Toda Proposition 5.6 literature
```

direct theorem premises はすべて independently derived `ProofRule.INFERENCE` とし、scope のみ `GIVEN` とする。

final aggregate 自身も:

```text
ProofRule.INFERENCE
```

である。

---

# 82. Phase 65 proof-style presentation

`probes/probe_phase65_capabilities.py` は Phase 65-9 integration builder を representative fixture として再利用する。

display order:

```text
Result
Proof-style derivation
EHP exact sequence used
Provenance / integration
Literature statements used
Phase 65 completion boundary
```

EHP display:

```text
π_7^3 ─H→ π_7^5 ─Δ→ π_5^2 ─E→ π_6^3 ─H→ π_6^5
```

proof-style derivation は presentation-only。

```text
ProofStep graph → automatic proof text
```

ではない。

---

# 83. provenance の永続性

`ProofStep` は実行中に:

```text
conclusion
premises
inference_rule
```

を保持し、final conclusion から ancestor graph を復元できる。

Phase 65-10 では:

```text
final aggregate is INFERENCE
direct theorem dependencies are INFERENCE
final graph is acyclic
final conclusion is absent from ancestors
upstream branches do not depend on final aggregate
```

を regression で固定する。

ただし current provenance は persistent storage ではない。

```text
program run
↓
ProofStep graph exists in memory

program exit
↓
graph is not automatically persisted

next run
↓
inference is reconstructed
```

Phase 64 以降の `@lru_cache(maxsize=1)` は同一 process 内の deterministic builder 再利用であり、永続 database ではない。

---

# 84. Proof Repository / Derived Fact Database の導入条件

persistent repository は現時点では実装しない。

理由:

```text
schema を先に固定
↓
後続 stem で必要構造が増える
↓
早期設計が proof development を拘束する
```

目安:

```text
7-stem 程度まで concrete calculations を蓄積
↓
最小 repository を設計 / 実装するには十分

8–10 stem
↓
複数 generator
extension
複数 derivation
primary decomposition
Toda bracket indeterminacy
等を実例で検証
↓
schema を拡張 / 安定化
```

最小 repository candidate:

```text
DerivedFact
  conclusion
  scope
  group / generator information
  proof provenance
  dependencies
  literature metadata
```

重要な境界:

```text
repository
!=
answer-only cache

repository
=
derived conclusion
+
why it is true
+
what it depends on
```

---

# 85. Phase 65 completion boundary

完成:

```text
Toda Proposition 5.6 finite-dimensional result
Equation (5.7)
EHP connected-sequence display
ord(ν′)=4
π_6^3=Z/4{ν′}
π_7^4 decomposition
π_8^5 quotient / E² injectivity
ord(ν₅)=8
π_8^5=Z/8{ν₅}
Toda (4.5) n≥6 transport
π_(n+3)^n=Z/8{ν_n}, n≥5
TodaProp56FiniteDimensionalStatement
representative proof-style probe
full provenance regression
```

final regression:

```text
3841 passed in 31.82s
```

deferred:

```text
stable ν
stable 4ν=η³
stable (G_3;2)=Z/8{ν}
Equation (5.8)
automatic proof narrative generation
persistent Proof Repository
```

次の数学 Phase は next concrete Toda source statement / consequence から開始する。

---

# 86. Phase 66：Toda Equation (5.8) 設計

Phase 66 target:

```text
Δ(ι₉)=±(2ν₄-Eν′)=±[ι₄,ι₄]
```

基本方針:

```text
Phase 65 の π_7^4 decomposition を再利用
+
Phase 60 の Whitehead correction provenance を再利用
↓
Equation (5.8) 専用の最小 statement / bridge
↓
literature-aware aggregate
```

generic `±` algebra は導入しない。

---

# 87. `2ν₄-Eν′` の表現

新しい subtraction expression は追加しない。

既存:

```text
Sum
Multiple
Suspension
```

で:

```text
2ν₄-Eν′
```

を:

```text
Sum(
  left=Multiple(
    coefficient=2,
    expression=ν₄,
  ),
  right=Multiple(
    coefficient=-1,
    expression=Eν′,
  ),
)
```

として保持する。

設計境界:

```text
subtraction notation
!=
new subtraction AST
```

---

# 88. Phase 66-3：Δ(ι₉)=±(2ν₄-Eν′)

既存:

```text
TodaDeltaImageUpToSignStatement
```

を再利用する。

入力:

```text
π_7^4=Z{ν₄}⊕Z/4{Eν′}
INFERENCE
```

から:

```text
Δ:π_9^9→π_7^4

Δ(ι₉)=±(2ν₄-Eν′)
```

を theorem-specific rule で導出する。

Phase 65 aggregate 全体ではなく、必要な `π_7^4` relation のみを直接 premise とし、
不要な branch を provenance に取り込まない。

---

# 89. Phase 66-4：Whitehead-square connection

Phase 52 の `ι₂` 専用 statement を流用しない。

Equation (5.8) 専用:

```text
Toda58WhiteheadSquareUpToSignStatement
```

を追加する。

意味:

```text
whitehead_square
=
± positive_value
```

concrete instance:

```text
[ι₄,ι₄]
=
±(2ν₄-Eν′)
```

Phase 60 の:

```text
TodaLemma54WhiteheadCorrectionDataStatement
```

から `[ι₄,ι₄]` object を再利用する。

---

# 90. Phase 66-5：concrete up-to-sign bridge

premise:

```text
Δ(ι₉)=±x

[ι₄,ι₄]=±x

x=2ν₄-Eν′
```

から:

```text
Δ(ι₉)=±[ι₄,ι₄]
```

を Equation (5.8) 専用 rule で導出する。

追加しない:

```text
A=±X
B=±X
→
A=±B
```

という generic transitivity rule。

rule は:

```text
Δ source = π_9^9
Δ target = π_7^4
element = ι₉
whitehead square = [ι₄,ι₄]
common positive representative = 2ν₄-Eν′
```

を concrete に検証する。

---

# 91. Phase 66 object provenance

conclusion builder では可能な限り upstream object を再利用する。

```text
Phase 66-3:
  ν₄
  Eν′
  Δ map
  ι₉

Phase 66-4:
  Phase 60 [ι₄,ι₄]

Phase 66-5:
  Δ map      is Phase 66-3 map
  ι₉         is Phase 66-3 element
  [ι₄,ι₄]   is Phase 66-4 Whitehead object
```

重要:

```text
structural equality
!=
Python object identity
```

両者を test で区別する。

---

# 92. Phase 66 applicability / provenance regression

Phase 66-6 では production code を変更しない。

横断的に:

```text
GIVEN shortcut rejection
wrong statement-type rejection
wrong Δ instance rejection
acyclic ancestry
upstream independence
cross-Phase object reuse
```

を固定する。

主要 ancestor:

```text
final → Phase 66-3
final → Phase 66-4
Phase 66-3 → Phase 65 π_7^4
Phase 66-4 → Phase 60 Whitehead data
```

---

# 93. Phase 66 literature-aware aggregate

最終 aggregate:

```text
Toda58EquationStatement
```

保持:

```text
delta_nu_relation
whitehead_nu_relation
delta_whitehead_relation
literature_statements
```

直接 premise:

```text
Phase 66-3 result  INFERENCE
Phase 66-4 result  INFERENCE
Phase 66-5 result  INFERENCE
```

aggregate 自身:

```text
ProofRule.INFERENCE
```

direct literature:

```text
Toda (5.8)
Equation (5.8)
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
```

---

# 94. proof record documentation

Phase 66-8 から:

```text
docs/proof_records.md
```

を正式に開始する。

責務:

```text
representative mathematical result
proof-style derivation
machine provenance
literature
GIVEN / INFERENCE boundary
representation boundary
representative probe
regression status
```

この文書は persistent Proof Repository ではない。

```text
curated human-readable proof record
!=
serialized proof graph database
```

将来 automatic proof narrative generation の human-reviewed reference corpus とする。

---

# 95. 文書運用方針

Phase 66 completion 以後は文書の役割をより明確に分離する。

```text
README.md
= current status / current capability

docs/design.md
= current architecture / semantics / design boundary
  既存設計を削らず、重要な新設計を追記

docs/development_log.md
= chronological history
  原則として削除せず追記

docs/code_reference.md
= current code navigation
  主要 class / rule / probe entry point を追記

docs/proof_records.md
= representative proofs
  proof record を追記

docs/roadmap.md
= future-oriented plan
  完了 Phase の詳細は保持せず圧縮
```

完了 Phase の詳細履歴は `development_log.md` に置く。

roadmap は:

```text
完了済み milestone summary
+
現在地
+
次の Phase
+
planned / deferred
```

に集中する。

---

# 96. Phase 66 completion boundary

完成:

```text
2ν₄-Eν′ expression compatibility
Δ(ι₉)=±(2ν₄-Eν′)
[ι₄,ι₄]=±(2ν₄-Eν′)
Δ(ι₉)=±[ι₄,ι₄]
Toda58WhiteheadSquareUpToSignStatement
Toda58EquationStatement
Equation (5.8) literature metadata
applicability / wrong-instance / provenance regression
representative proof-style probe
docs/proof_records.md foundation
```

final regression:

```text
3970 passed in 31.96s
```

deferred:

```text
generic PlusMinus
generic sign solver
generic up-to-sign transitivity
automatic proof narrative generation
persistent Proof Repository
past proof-record backfill
stable ν / η³
stable homotopy-group model
```

---

# 96. Phase 67：Toda Lemma 5.7 設計

Phase 67 target:

```text
E²α ∈ 2ι₅∘π_(i+2)(S⁵)
→
E(η₂∘α)=0

特に:
E(η₂∘ν′)=0
Δ(ν₅)=±(η₂∘ν′)
```

基本方針:

```text
Toda Lemma 5.7 の実際の proof need
↓
minimum hypothesis semantics
↓
既存 Lemma 4.5 / Proposition 5.1 / Lemma 5.4 / Toda (5.2) / Proposition 5.6 / exactness を再利用
↓
concrete Delta consequence
```

generic image algebra や generic cyclic-image solver は追加しない。

# 97. Lemma 5.7 hypothesis の minimum semantics

専用 statement:

```text
TodaLemma57TwoIota5ImageMembershipStatement
```

field:

```text
element
source_group
```

意味:

```text
element ∈ 2ι₅∘source_group
```

これは generic image object ではない。

追加しない:

```text
generic ImageMembership
generic map image
existential witness
generic composition-image algebra
```

# 98. symbolic α と concrete ν′ の typing boundary

Toda Lemma 5.7 の α は:

```text
α∈π_i(S³)
```

であり、数学的 index `i` は source sphere dimension から読む。

Phase 57 symbolic α は:

```text
dimension=i
source=i
target=3
```

だったが、canonical concrete ν′ は:

```text
dimension=3
source=6
target=3
```

である。

したがって Phase 67 general guard は:

```text
i = alpha.source
```

を用いる。

重要:

```text
HomotopyElement.dimension
!=
always the π_i group index
```

という既存 representation reality を守り、ν′ を Phase 67 用に作り直さない。

# 99. General Lemma 5.7 branch

Phase 67-3:

```text
E²α ∈ 2ι₅∘π_(i+2)(S⁵)
↓
E²(η₂∘α)=η₄∘E²α
```

Phase 55 / Proposition 5.1 consequence:

```text
2η₄=0
```

より:

```text
E²(η₂∘α)=0
```

Phase 67-4 では Toda Lemma 4.5 の今回必要な n=3 consequence のみ追加:

```text
E²(η₂∘α)=0
↓
E(η₂∘α)=0
```

all-n reflection framework は追加しない。

# 100. ν′ specialization の再利用設計

Phase 60 Lemma 5.4:

```text
2Eν₄=E²ν′
```

ν-family definition:

```text
ν₅=Eν₄
```

から:

```text
E²ν′ ∈ 2ι₅∘π_8(S⁵)
```

を専用 bridge で `INFERENCE` として導出する。

その後 general Lemma 5.7 branch を再利用して:

```text
E(η₂∘ν′)=0
```

を得る。

設計原則:

```text
specialization
→ hypothesis を derived にする
→ general theorem chain を再利用
```

ν′ 専用に general proof を複製しない。

# 101. Toda (5.2) + Proposition 5.6 concrete transport

Phase 56:

```text
η₂∘- : π_i^3≅π_i^2
```

Phase 65:

```text
π_6^3=Z/4{ν′}
```

から:

```text
π_6^2=Z/4{η₂∘ν′}
```

を concrete theorem-specific rule で導出する。

generic finite-cyclic generator transport は追加しない。

# 102. concrete Toda (4.4) exactness boundary

既存 `toda_prop42_delta_e_exactness_inference_rule()` は symbolic scalar shape を前提とするため、今回の concrete:

```text
π_8^5 ─Δ→ π_6^2 ─E→ π_7^3
```

を generic rule 側へ無理に合わせない。

Phase 67 は narrow bridge で exactness window を認識し:

```text
TodaProp42ExactnessStatement
```

を derived にする。

設計原則:

```text
existing generic/symbolic rule の applicability を広げる
より
concrete theorem instance の minimum bridge
```

を優先する。

# 103. Delta surjectivity semantics

追加:

```text
TodaDeltaSurjectiveStatement
```

理由:

```text
E(η₂∘ν′)=0
π_6^2=Z/4{η₂∘ν′}
```

なので concrete target 上で E は zero。

exactness:

```text
Im Δ = Ker E = π_6^2
```

から Δ surjective を得る。

generic map-zero solver / first-isomorphism theorem engine は追加しない。

# 104. Delta generator consequence と canonical ν₅

Phase 65:

```text
π_8^5=Z/8{ν₅}
```

と Δ surjective から source generator の image が target generator を生成する。

final:

```text
Δ(ν₅)=±(η₂∘ν′)
```

は既存:

```text
TodaDeltaImageUpToSignStatement
```

で保持する。

canonical `ν₅` は手書きせず:

```text
toda_nu_family_definition_statement(5).element
```

を利用する。

Phase 67 開発中に `"ν₅"` と existing canonical `"ν_5"` の name mismatch が guard failure を起こしたため、family factory reuse を設計境界として固定する。

# 105. Phase 67 provenance / non-circularity

final:

```text
Δ(ν₅)=±(η₂∘ν′)
```

の ancestor graph は次を reach する:

```text
Phase 60 Lemma 5.4
Phase 67 ν′ image hypothesis
Phase 67 E(η₂ν′)=0
Phase 56 Toda (5.2)
Phase 65 Proposition 5.6
Phase 67 π_6^2
Toda (4.4) exactness
Phase 67 Δ surjectivity
Phase 65 π_8^5
```

Phase 67-8 で:

```text
graph is acyclic
final is not its own ancestor
final conclusion absent from ancestors
intermediate branches do not depend on final
```

を固定する。

さらに:

```text
Toda58EquationStatement
```

が final ancestor に存在しないことを確認する。

したがって:

```text
source ordering
!=
machine proof dependency
```

を明示的に守る。

# 106. Phase 67 proof-style display

`probes/probe_phase67_capabilities.py` は Phase 67-7 focused builder を再利用する。

表示:

```text
Toda Lemma 5.7 result
Proof-style derivation
Provenance / integration
Literature / source
Proof record
Phase 67 completion boundary
```

`print_phase67_derivation_chain()` は hand-authored presentation layer。

```text
ProofStep graph → automatic narrative
```

はまだ実装しない。

# 107. Phase 67 completion boundary

完成:

```text
minimum image-membership semantics
general Lemma 5.7 chain
n=3 Lemma 4.5 reflection
ν′ specialization
π_6^2 concrete transport
concrete Toda (4.4) exactness
Delta surjectivity
Δ(ν₅)=±(η₂∘ν′)
provenance / non-circularity regression
representative probe
proof record
```

追加しない:

```text
generic ImageMembership
generic existential witness
generic cyclic-image solver
generic sign / ± algebra
generic all-n Lemma 4.5 reflection
generic exactness solver
automatic proof narrative generation
persistent Proof Repository
```

final regression:

```text
4102 passed in 32.75s
```
---

# 108. Phase 68：Toda Proposition 5.8 finite-dimensional 設計目標

Phase 68 の target:

```text
π_6^2=Z/4{η₂ν′}
π_7^3=Z/2{ν′η₆}
π_8^4=Z/2{ν₄η₇}⊕Z/2{Eν′η₇}
π_9^5=Z/2{ν₅η₈}
π_(n+4)^n=0
(n≥6)
```

stable conclusion:

```text
(G_4;2)=0
```

は Phase 68 aggregate に含めない。

Phase 68 は Proposition 5.8 の finite-dimensional statement のみを統合する。

---

# 109. Phase 68 の dependency 方針

主要 upstream:

```text
Phase 60
Toda Lemma 5.4
ν₄ / Whitehead correction

Phase 62
ν-family

Phase 63
Toda (5.6) decomposition

Phase 65
Proposition 5.6
Equation (5.7)
π_7^4 decomposition

Phase 66
Toda (5.8)

Phase 67
Lemma 5.7
π_6^2=Z/4{η₂ν′}
```

Phase 68 では source ordering をそのまま machine dependency としない。

```text
source ordering
!=
machine proof dependency
```

特に Toda (5.9) は `π_7^3` を利用して導出し、`π_7^3` の premise には戻さない。

---

# 110. π_7^3 branch

Phase 67:

```text
π_6^2=Z/4{η₂ν′}
E(η₂ν′)=0
```

concrete E-H exactness:

```text
π_6^2 --E--> π_7^3 --H--> π_7^5
```

から:

```text
H injective
```

を導出する。

Phase 65 Equation (5.7):

```text
H(ν′η₆)=η₅²
```

と Proposition 5.3:

```text
π_7^5=Z/2{η₅²}
```

から:

```text
H surjective
```

を得る。

したがって:

```text
H:π_7^3≅π_7^5
↓
π_7^3=Z/2{ν′η₆}
```

generic injective/surjective → isomorphism mechanics は既存を利用し、group conclusion は theorem-specific rule とする。

---

# 111. π_8^4 decomposition

Toda (5.6), `i=8`:

```text
π_7^3⊕π_8^7≅π_8^4
(α,β)↦Eα+ν₄β
```

を再利用する。

input:

```text
π_7^3=Z/2{ν′η₆}
π_8^7=Z/2{η₇}
```

concrete bridge:

```text
E(ν′η₆)=Eν′η₇
```

から:

```text
π_8^4
=
Z/2{ν₄η₇}
⊕
Z/2{Eν′η₇}
```

を導出する。

generic direct-sum finite-cyclic transport は追加しない。

---

# 112. Δ(η₉) と π_9^5 branch

Phase 66:

```text
Δ(ι₉)=±(2ν₄-Eν′)
```

を利用する。

Proposition 2.5 の今回必要な concrete consequence のみ:

```text
Δ(η₉)
=
±((2ν₄-Eν′)η₇)
```

として接続する。

Phase 68 の `π_8^4` decomposition により:

```text
2ν₄η₇=0
```

かつ `Eν′η₇` は order two なので sign は無視できる。

最終:

```text
Δ(η₉)=Eν′η₇
```

generic distribution / sign normalizer は追加しない。

π_9^5 では Phase 66 decomposition の free component を利用して:

```text
Δ:π_9^9→π_7^4 injective
```

を導出し、exactness から:

```text
H:π_9^5→π_9^9 zero
E:π_8^4→π_9^5 surjective
```

を得る。

さらに:

```text
Δ(η₉)=Eν′η₇
```

から:

```text
ker(E)=Z/2{Eν′η₇}
```

を concrete branch で識別し:

```text
π_9^5=Z/2{ν₅η₈}
```

を導出する。

generic quotient solver / cyclic-image solver は追加しない。

---

# 113. Toda (5.9)

Phase 68 は:

```text
η₃ν₄=ν′η₆
```

を dedicated consequence として導出する。

Phase 60:

```text
H(ν₄)=ι₇
```

から concrete Hopf bridge:

```text
H(η₃ν₄)=η₅²
```

を得る。

Phase 65:

```text
H(ν′η₆)=η₅²
```

Phase 68 で既に:

```text
H:π_7^3→π_7^5
```

が injective / isomorphism なので:

```text
η₃ν₄=ν′η₆
```

を導出する。

Toda source proof にある追加 order argument を再実装せず、既に独立導出済みの stronger map property を再利用する。

---

# 114. η_nν_(n+1)=0 と ν_nη_(n+3)=0

Toda (5.9) を double suspension:

```text
η₅ν₆=E²ν′η₈
```

Phase 62 / Phase 65:

```text
2ν₅=E²ν′
```

Phase 68:

```text
π_9^5=Z/2{ν₅η₈}
```

したがって:

```text
η₅ν₆
=
2ν₅η₈
=
0
```

higher transport:

```text
η_nν_(n+1)=0
(n≥5)
```

Phase 68-9 ではまず concrete specialization:

```text
η₆ν₇=0
```

を導出する。

Toda Proposition 3.1 の two Barratt-Hilton formulas は structural に sign を含む。

今回の specialization では raw formulas は:

```text
η₂∧ν₄ = -η₆ν₇
η₂∧ν₄ = +ν₆η₉
```

となるため、literal positive equality:

```text
η₆ν₇=ν₆η₉
```

を generic normalization で作らない。

zero consequence に必要なのは:

```text
η₆ν₇=0
↓
ν₆η₉=0
```

のみであり、`±0=0` を theorem-specific guard 内で扱う。

higher transport:

```text
ν_nη_(n+3)=0
(n≥6)
```

へ進む。

---

# 115. shifted η representation

current helper:

```text
toda_eta_family_definition_statement(n)
```

は:

```text
int
ScalarSymbol
```

のみを index として受理する。

したがって:

```text
ScalarSum(n,3)
```

を helper に渡して:

```text
η_(n+3)
```

を作ることはしない。

Phase 68 では必要な shifted occurrence を rule 内で局所的に:

```text
HomotopyElement
+
GeneratorSymbol(family="η", index=n+3)
```

として構成する。

helper API を symbolic scalar expression 全般へ拡張しない。

---

# 116. concrete family display-name boundary

Phase 68-10 で:

```text
η₈
η_8
```

の display name 差が structural equality guard を失敗させた。

対処:

```text
upstream derived generator object を再利用
+
dimension / source / target / GeneratorSymbol を検証
```

とする。

current rule:

```text
表示文字列
```

を数学的 identity として扱わない。

同様の generic η-name normalizer は追加しない。

---

# 117. π_10^6 と Toda (4.5) transport

concrete exactness:

```text
π_9^5 --E--> π_10^6 --H--> π_10^11
```

foundation:

```text
π_10^11=0
```

から:

```text
E:π_9^5→π_10^6 surjective
```

を得る。

Phase 68:

```text
π_9^5=Z/2{ν₅η₈}
ν₆η₉=0
```

より:

```text
π_10^6=0
```

を theorem-specific consequence として導出する。

Toda (4.5):

```text
E^(n-6):π_10^6≅π_(n+4)^n
```

を再利用し:

```text
π_(n+4)^n=0
(n≥6)
```

へ transport。

generic zero-group isomorphism transport は追加しない。

---

# 118. Proposition 5.8 aggregate

Phase 68-11 で追加:

```text
TodaProp58FiniteDimensionalStatement
```

保持:

```text
pi6_2_group_relation
pi7_3_group_relation
pi8_4_group_relation
pi9_5_group_relation
higher_four_stem_zero
higher_range
literature_statements
```

integration premise:

```text
π_6^2=Z/4{η₂ν′}                     INFERENCE
π_7^3=Z/2{ν′η₆}                     INFERENCE
π_8^4=Z/2{ν₄η₇}⊕Z/2{Eν′η₇}         INFERENCE
π_9^5=Z/2{ν₅η₈}                     INFERENCE
π_(n+4)^n=0                         INFERENCE
n≥6                                 GIVEN
```

final:

```text
TodaProp58FiniteDimensionalStatement
ProofRule.INFERENCE
```

stable `(G_4;2)=0` は aggregate に含めない。

---

# 119. Phase 68 provenance / non-circularity

Phase 68-12 は production code を変更せず regression のみ追加。

確認:

```text
5 branch はすべて INFERENCE
n≥6 は GIVEN
aggregate は INFERENCE

final reaches all branches
branches do not reach final
final is not its own ancestor
final conclusion absent from ancestors
```

dependency boundary:

```text
Phase 66 / Toda (5.8)
  π_7^3 ancestors に存在しない
  π_8^4 ancestors に存在しない
  π_9^5 / higher branch で必要箇所にのみ存在

Toda (5.9)
  π_7^3 ancestors に存在しない
  final aggregate に依存しない
```

source order と machine dependency を分離する。

---

# 120. Phase 68 representative probe

module:

```text
probes/probe_phase68_capabilities.py
```

representative fixture:

```text
tests/test_phase68_prop58_integration.py
build_phase68_11_data()
```

を再利用する。

表示順:

```text
Toda Proposition 5.8 finite-dimensional result
Proof-style derivation
Provenance / integration
Literature statements used
Phase 68 representative probe boundary
```

proof-style derivation は presentation-only。

```text
ProofStep graph
→ automatic narrative generation
```

ではない。

Phase 68-13 では proof record を probe 実装から分離し、documentation Phase 68-14 で `docs/proof_records.md` へ記録する。

---

# 121. Phase 68 completion boundary

完成:

```text
π_6^2=Z/4{η₂ν′}
π_7^3=Z/2{ν′η₆}
π_8^4=Z/2{ν₄η₇}⊕Z/2{Eν′η₇}
Δ(η₉)=Eν′η₇
π_9^5=Z/2{ν₅η₈}
Toda (5.9): η₃ν₄=ν′η₆
η_nν_(n+1)=0, n≥5
ν_nη_(n+3)=0, n≥6
π_10^6=0
π_(n+4)^n=0, n≥6
TodaProp58FiniteDimensionalStatement
applicability / provenance / non-circularity regression
representative proof-style probe
formal proof record
```

追加しない:

```text
stable (G_4;2)=0
generic shifted-family framework
generic η-name normalization
generic sign solver
generic smash-product normalization
generic cyclic-image solver
generic zero-group solver
generic zero-group isomorphism transport
automatic proof narrative generation
persistent Proof Repository
stable homotopy-group model
```

final regression:

```text
4343 passed in 28.06s
```

---

# 122. Phase 69 source dependency

Toda Equation (5.10):

```text
Δ(ι₁₁)=ν₅η₈
```

の machine dependency は source order をそのまま theorem aggregate dependency にしない。

必要な既存 branch:

```text
Phase 68-10
π_10^6=0
INFERENCE

Phase 68-6
π_9^5=Z/2{ν₅η₈}
INFERENCE

foundational fact
π_11^11=Z{ι₁₁}
GIVEN
```

Phase 68 Proposition 5.8 aggregate は prerequisite shortcut として使わない。

---

# 123. Phase 69 concrete Δ-E exactness

対象 window:

```text
π_11^11 --Δ--> π_9^5 --E--> π_10^6
```

既存 symbolic Proposition 4.2 rule は symbolic scalar tree と concrete integer dimension が structural equality で一致しない場合がある。

Phase 69 では global scalar / dimension normalizer を導入せず:

```text
toda_eq510_concrete_delta_e_exactness_inference_rule()
```

という narrow concrete bridge を追加する。

```text
structural exactness window  GIVEN
↓
concrete exactness           INFERENCE
```

---

# 124. Phase 69 Δ-surjectivity

Phase 68 derived:

```text
π_10^6=0
INFERENCE
```

と Phase 69 concrete exactness から:

```text
E:π_9^5→π_10^6=0
↓
ker(E)=π_9^5
↓ exactness
Im(Δ)=π_9^5
↓
Δ:π_11^11→π_9^5 surjective
```

を導出する。

既存:

```text
TodaDeltaSurjectiveStatement
```

を再利用し、新規 statement class は追加しない。

rule:

```text
toda_eq510_delta_surjective_inference_rule()
```

---

# 125. Phase 69 generator-image consequence

premises:

```text
Δ:π_11^11→π_9^5 surjective       INFERENCE
π_11^11=Z{ι₁₁}                   GIVEN
π_9^5=Z/2{ν₅η₈}                  INFERENCE
```

conclusion:

```text
Δ(ι₁₁)=ν₅η₈
INFERENCE
```

rule:

```text
toda_eq510_delta_iota11_inference_rule()
```

source generator は foundational fact として保持する。

target generator は Phase 68-6 の `FiniteCyclicGroup.generator` object を直接再利用する。

```text
display-equivalent name
!=
structural identity
```

という既存境界を守る。

---

# 126. Phase 69 order-two sign boundary

```text
π_9^5=Z/2{ν₅η₈}
```

なので:

```text
-(ν₅η₈)=ν₅η₈
```

したがって Toda (5.10) は up-to-sign statement ではなく通常の:

```text
Relation(..., RelationType.EQUALITY)
```

として保持する。

generic sign algebra は追加しない。

---

# 127. Phase 69 provenance / non-circularity

final direct premises:

```text
Δ surjective              INFERENCE
π_11^11=Z{ι₁₁}           GIVEN
π_9^5=Z/2{ν₅η₈}          INFERENCE
```

ancestor graph:

```text
final
→ Δ surjective
→ π_10^6=0

final
→ Δ surjective
→ concrete exactness
→ structural exactness window

final
→ π_9^5

final
→ π_11^11 foundational fact
```

禁止する dependency:

```text
final
→ Phase 68 Proposition 5.8 aggregate
→ π_9^5
```

Phase 69-4 regression で:

```text
final is not its own ancestor
final conclusion absent from ancestors
Phase 68 aggregate absent from final ancestors
```

を固定する。

---

# 128. Phase 69 representative probe

module:

```text
probes/probe_phase69_capabilities.py
```

representative fixture:

```text
tests/test_phase69_delta_iota11.py
build_phase69_3_data()
```

表示:

```text
Toda Equation (5.10) result
Proof-style derivation
EHP exact sequence used
Provenance / integration
Literature / source
Related previously derived result
Phase 69 representative probe boundary
```

proof-style derivation は hand-authored presentation-only。

```text
ProofStep graph
→ automatic narrative generation
```

ではない。

Toda Equation (5.11):

```text
Δ(η₉)=Eν′η₇
```

は Phase 68 で derived 済みなので再実装しない。

---

# 129. Phase 69 completion boundary

完成:

```text
π_11^11 --Δ--> π_9^5 --E--> π_10^6
concrete exactness

π_10^6=0
↓
Δ:π_11^11→π_9^5 surjective

π_11^11=Z{ι₁₁}
π_9^5=Z/2{ν₅η₈}
↓
Δ(ι₁₁)=ν₅η₈

applicability / provenance / non-circularity regression
representative probe
formal proof record
```

追加しない:

```text
stable (G_4;2)=0
generic concrete-dimension normalizer
generic exactness solver
generic cyclic-image solver
generic zero-target solver
generic sign / ± algebra
automatic proof narrative generation
persistent Proof Repository
stable homotopy-group model
```

final regression:

```text
4422 passed in 30.54s
```

---

# 130. Phase 70 source / dependency boundary

Toda Proposition 5.9 finite-dimensional target:

```text
π_7^2=Z/2{η₂ν′η₆}
π_8^3=Z/2{ν′η₆²}
π_9^4=Z/2{ν₄η₇²}⊕Z/2{Eν′η₇²}
π_10^5=Z/2{ν₅η₈²}
π_11^6=Z{Δι₁₃}
π_(n+5)^n=0
(n≥7)
```

stable:

```text
(G_5;2)=0
```

は Phase 70 scope に含めない。

Phase 69 aggregate を shortcut premise にせず、必要な concrete derived branch を直接再利用する。

---

# 131. Phase 70 execution-scope design

Phase 70-3 以降の concrete multi-step branch は:

```text
find_inference_match()
↓
apply_inference_match()
```

による staged one-shot inference を優先する。

理由:

```text
repeatable Relation→Relation rule
+
large shared object graph
↓
unrestricted fixed-point exploration
↓
combinatorial slowdown risk
```

これは generic inference engine の変更ではない。

heavy deterministic builder は必要に応じて:

```python
@lru_cache(maxsize=1)
```

を使用して、同一 process 内の object graph を再利用する。

---

# 132. Phase 70 π_7^2 / π_8^3 branch

derived:

```text
π_7^2=Z/2{η₂ν′η₆}

π_8^3=Z/2{ν′η₆²}
```

両 branch は independently derived `ProofStep` として保持する。

後続 aggregate に final theorem statement を `GIVEN` として再投入しない。

---

# 133. Phase 70 π_9^4 decomposition

derived:

```text
π_9^4
=
Z/2{ν₄η₇²}
⊕
Z/2{Eν′η₇²}.
```

既存 Toda (5.6) decomposition semantics と ν / η family relation を再利用する。

新しい generic direct-sum decomposition framework は追加しない。

---

# 134. Phase 70 Δ(η₉²) / E-surjectivity

supporting derived results:

```text
Δ(η₉²)=Eν′η₇²

E:π_9^4→π_10^5
surjective
```

dependency direction:

```text
π_9^4
↓
Phase 70-5 support
↓
π_10^5
```

Phase 70-5 support を `π_9^4` の ancestor にしない。

---

# 135. Phase 70 π_10^5

derived:

```text
π_10^5=Z/2{ν₅η₈²}.
```

proof structure:

```text
π_9^4 decomposition
+
Δ(η₉²)=Eν′η₇²
+
E-surjectivity
↓
second summand is killed by E

E(ν₄η₇²)=ν₅η₈²
↓
π_10^5=Z/2{ν₅η₈²}.
```

generic quotient / image solver は追加しない。

---

# 136. Phase 70 display-name identity boundary

Phase 70-7 compatibility で:

```text
η_9
η₉
```

の dataclass equality mismatch が確認された。

設計方針:

```text
display name
!=
mathematical identity
```

theorem-specific guard では必要に応じて:

```text
dimension
source
target
GeneratorSymbol
expression tree
```

を比較する。

global η-name normalizer は追加しない。

---

# 137. Phase 70 E(ν₅η₈²)=0 / Δ(η₁₁)

Phase 70-7 derives:

```text
E(ν₅η₈²)=0
Δ(η₁₁)=ν₅η₈².
```

これらは sibling consequences。

重要:

```text
Δ(η₁₁)=ν₅η₈²
```

を `π_11^6` calculation の prerequisite にしない。

---

# 138. Phase 70 Delta-kernel representation

Phase 70-8 の concrete need により:

```text
TodaDeltaKernelFreeCyclicStatement
```

を追加する。

意味:

```text
ker(Δ)=FreeCyclicGroup(...)
```

対象は Proposition 5.9 の concrete branch。

generic arbitrary-map kernel theorem / solver には一般化しない。

---

# 139. Phase 70 π_11^6

non-circular proof:

```text
E(ν₅η₈²)=0
π_10^5=Z/2{ν₅η₈²}
↓
H:π_11^6→π_11^11 injective

π_11^11=Z{ι₁₁}
π_9^5=Z/2{ν₅η₈}
Δ(ι₁₁)=ν₅η₈
↓
ker Δ=Z{2ι₁₁}

Toda Proposition 2.7:
H(Δι₁₃)=±2ι₁₁
↓
π_11^6=Z{Δι₁₃}.
```

禁止:

```text
π_12^7=0
↓
π_11^6
```

`π_12^7=0` は後続 Phase 70-9 で導出する。

---

# 140. Phase 70 π_12^7=0

Phase 70-9:

```text
π_13^13=Z{ι₁₃}
π_11^6=Z{Δι₁₃}
↓
Δ:π_13^13→π_11^6 surjective
```

concrete exactness:

```text
π_13^13 --Δ--> π_11^6 --E--> π_12^7
```

より `E` は zero。

一方:

```text
π_11^6 --E--> π_12^7 --H--> π_12^13
```

と:

```text
π_12^13=0
```

から `E` は surjective。

したがって:

```text
π_12^7=0.
```

generic zero-map / zero-target / exactness solver は追加しない。

---

# 141. Phase 70 higher five-stem transport

Toda (4.5):

```text
E^(n-7):
π_12^7
≅
π_(n+5)^n
```

for `n≥7`。

base:

```text
π_12^7=0
```

から:

```text
π_(n+5)^n=0
(n≥7)
```

を theorem-specific transport rule で導出する。

generic zero-group isomorphism transport は追加しない。

---

# 142. Phase 70 finite-dimensional aggregate

statement:

```text
TodaProp59FiniteDimensionalStatement
```

保持:

```text
pi7_2_group_relation
pi8_3_group_relation
pi9_4_group_relation
pi10_5_group_relation
pi11_6_group_relation
higher_five_stem_zero
higher_range
literature_statements
```

direct premise boundary:

```text
π_7^2 relation        INFERENCE
π_8^3 relation        INFERENCE
π_9^4 relation        INFERENCE
π_10^5 relation       INFERENCE
π_11^6 relation       INFERENCE
π_(n+5)^n=0           INFERENCE
n≥7                    GIVEN
```

aggregate:

```text
ProofRule.INFERENCE
```

stable `(G_5;2)=0` を aggregate に含めない。

---

# 143. Phase 70 provenance / non-circular regression

Phase 70-11 は production code を変更せず provenance regression のみ追加。

確認:

```text
aggregate INFERENCE
aggregate not GIVEN

six mathematical branches INFERENCE
n≥7 GIVEN

seven direct premises exact
aggregate reaches all branches
aggregate not self-ancestor
aggregate conclusion absent from ancestors
branches do not depend on aggregate
```

expected ordering:

```text
π_7^2
→
π_8^3
→
π_9^4
→
π_10^5
→
π_11^6
→
higher zero
```

backward-flow regression:

```text
Phase 70-5 support ↛ π_9^4
Phase 70-7 suspension zero ↛ π_10^5
Phase 70-7 Δ(η₁₁) ↛ π_10^5
Phase 70-7 Δ(η₁₁) ↛ π_11^6
Phase 69 Δ(ι₁₁) ↛ π_9^4
Phase 69 Δ(ι₁₁) ↛ π_10^5
```

---

# 144. Phase 70 representative probe

module:

```text
probes/probe_phase70_capabilities.py
```

representative fixture:

```text
tests/test_phase70_prop59_integration.py
build_phase70_10_data()
```

表示:

```text
Toda Proposition 5.9 finite-dimensional result
Proof-style derivation
Provenance / integration
Literature statements used
Phase 70 representative probe boundary
```

proof-style derivation は hand-authored presentation-only。

```text
ProofStep graph
→ automatic narrative generation
```

ではない。

---

# 145. Phase 70 completion boundary

完成:

```text
π_7^2=Z/2{η₂ν′η₆}
π_8^3=Z/2{ν′η₆²}
π_9^4=Z/2{ν₄η₇²}⊕Z/2{Eν′η₇²}
Δ(η₉²)=Eν′η₇²
E:π_9^4→π_10^5 surjective
π_10^5=Z/2{ν₅η₈²}
E(ν₅η₈²)=0
Δ(η₁₁)=ν₅η₈²
π_11^6=Z{Δι₁₃}
π_12^7=0
π_(n+5)^n=0, n≥7
TodaProp59FiniteDimensionalStatement
applicability / provenance / non-circularity regression
representative proof-style probe
formal proof record
```

追加しない:

```text
stable (G_5;2)=0
generic concrete-dimension normalizer
generic exactness solver
generic cyclic-image solver
generic zero-target solver
generic zero-map solver
generic zero-group isomorphism transport
generic sign / ± algebra
generic η-name normalization
automatic proof narrative generation
persistent Proof Repository
stable homotopy-group model
```

final regression:

```text
4752 passed in 30.85s
```

---

# 146. Phase 71 Toda (5.12) representation

Phase 71 target:

```text
Δ:
π_(n+7)^(2n+1)
→
π_(n+5)^n

injective for n=4,5,6
```

existing map-property representation:

```text
TodaDeltaInjectiveStatement
map: TodaDeltaMap
```

で3 concrete case を表現できるため、generic range-valued injectivity statement は追加しない。

three-case aggregate のみ新規に:

```text
Toda512DeltaInjectivityStatement
```

を追加する。

保持:

```text
n4_injectivity
n5_injectivity
n6_injectivity
literature_statements
```

設計意図:

```text
three independently derived concrete facts
↓
one literature-aware theorem aggregate
```

であり、symbolic `n∈{4,5,6}` solver ではない。

---

# 147. Phase 71 n=4 injectivity branch

target:

```text
Δ:π_11^9→π_9^4
```

dependencies:

```text
Proposition 5.3 higher η-square family
π_11^9=Z/2{η₉²}

Phase 70
π_9^4
=
Z/2{ν₄η₇²}
⊕
Z/2{Eν′η₇²}

Phase 70
Δ(η₉²)=Eν′η₇²
```

source is cyclic order two and its nonzero generator maps to a nonzero order-two summand generator.

専用 rule:

```text
toda_512_n4_delta_injective_inference_rule()
```

generic cyclic-map injectivity solver は追加しない。

---

# 148. Phase 71 n=5 injectivity branch

target:

```text
Δ:π_12^11→π_10^5
```

dependencies:

```text
Proposition 5.1 higher η-family
π_12^11=Z/2{η₁₁}

Phase 70
π_10^5=Z/2{ν₅η₈²}

Phase 70
Δ(η₁₁)=ν₅η₈²
```

重要な source semantics:

```text
π_12^11=Z/2{η₁₁}
```

は Proposition 5.1 の:

```text
π_(n+1)^n=Z/2{η_n}
```

の `n=11` instance。

Proposition 5.3 higher η-square family ではない。

専用 rule:

```text
toda_512_n5_delta_injective_inference_rule()
```

既存 symbolic family statement を theorem-specific guard で concrete instance として確認する。

generic theorem specialization engine は追加しない。

---

# 149. Phase 71 n=6 injectivity branch

target:

```text
Δ:π_13^13→π_11^6
```

dependencies:

```text
π_13^13=Z{ι₁₃}
GIVEN

π_11^6=Z{Δι₁₃}
INFERENCE
```

source free generator:

```text
ι₁₃
```

target free generator:

```text
Δι₁₃
```

なので generator-to-generator property から concrete injectivity を導く。

専用 rule:

```text
toda_512_n6_delta_injective_inference_rule()
```

Phase 70 にある同 map の surjectivity statement は premise にしない。

理由:

```text
source free group
+
target free group generated by Δι₁₃
```

だけで injectivity branch の direct provenance が十分だからである。

generic free-cyclic map solver は追加しない。

---

# 150. Phase 71 three-case aggregate

aggregate:

```text
Toda512DeltaInjectivityStatement
```

literature:

```text
toda_512_delta_injectivity_literature_statements()
```

integration:

```text
toda_512_delta_injectivity_integration_inference_rule()
```

direct premises:

```text
n=4 injectivity  INFERENCE
n=5 injectivity  INFERENCE
n=6 injectivity  INFERENCE
```

final:

```text
Toda512DeltaInjectivityStatement
ProofRule.INFERENCE
```

integration rule は upstream group structure を再検証しない。

各 concrete branch がそれぞれの rule で applicability を検証済みだからである。

---

# 151. Phase 71 literature metadata

aggregate に structured literature metadata を保持:

```text
Author:
H. Toda

Title:
Composition Methods in Homotopy Groups of Spheres

Year:
1962

Label:
Toda (5.12)

Locator:
Equation (5.12)
```

literature metadata は theorem-search semantics ではない。

generic theorem repository は追加しない。

---

# 152. Phase 71 provenance / non-circularity

production code を変更せず dedicated regression で確認:

```text
final aggregate
→ exactly n=4,n=5,n=6

aggregate reaches all three branches
aggregate reaches each branch upstream facts
```

acyclicity:

```text
aggregate not self-ancestor
aggregate conclusion absent from ancestors

n=4 branch not self-ancestor
n=5 branch not self-ancestor
n=6 branch not self-ancestor
```

cross-branch isolation:

```text
n=4 does not depend on n=5 or n=6
n=5 does not depend on n=4 or n=6
n=6 does not depend on n=4 or n=5
```

reverse dependency rejection:

```text
no branch depends on final aggregate
```

GIVEN / INFERENCE boundary:

```text
n=4 direct dependencies = INFERENCE
n=5 direct dependencies = INFERENCE

n=6:
π_13^13 = GIVEN
π_11^6  = INFERENCE
```

---

# 153. Phase 71 representative probe

module:

```text
probes/probe_phase71_capabilities.py
```

representative fixture:

```text
tests/test_phase71_applicability_provenance.py
build_phase71_6_data()
```

display:

```text
Toda (5.12) Delta injectivity
Proof-style derivation
Provenance / integration
Literature statements used
Phase 71 representative probe boundary
```

proof-style derivation:

```text
hand-authored presentation code
```

であり:

```text
ProofStep graph
→ automatic narrative generation
```

ではない。

Python 3.10 compatibility のため、複数行 f-string expression を避け、表示用 boolean は事前計算してから f-string に渡す。

---

# 154. Phase 71 completion boundary

完成:

```text
TodaDeltaInjectiveStatement
Toda512DeltaInjectivityStatement

Δ:π_11^9→π_9^4 injective
Δ:π_12^11→π_10^5 injective
Δ:π_13^13→π_11^6 injective

Toda (5.12) aggregate
structured literature metadata
applicability regression
provenance / non-circularity regression
representative proof-style probe
sixth formal proof record
```

追加しない:

```text
Toda Lemma 5.10
generic Toda-bracket coset algebra
generic modulo-subgroup normalization
generic cyclic-map injectivity solver
generic free-cyclic map solver
generic theorem specialization engine
automatic proof narrative generation
persistent Proof Repository
stable homotopy-group model
```

final regression:

```text
4886 passed in 29.25s
```

Phase 64 performance stabilization level is retained.

