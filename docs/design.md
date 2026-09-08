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

Phase 60 までこの原則を維持している。

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

# 47. 将来の proof narrative generation

Phase 60 で次の4種類の情報が揃った。

```text
ProofStep / premises
Expression の構造
InferenceRule / provenance
LiteratureStatement
```

このため将来は proof graph から証明本文を生成する方向へ進める。

目標 pipeline:

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

将来必要になる可能性のある display metadata:

```text
premise role
conclusion role
step heading
equation rendering hint
citation role
narrative template
compression / omission hint
```

ただし current architecture ではこれらを `InferenceRule` にまだ追加しない。Phase 60 の `print_phase60_derivation_chain()` は manual representative であり、自動 proof generator ではない。

generalization 条件:

```text
複数の concrete proof branch
で同じ presentation pattern が反復
↓
安定した display schema を抽出
↓
generic proof narrative generation を実装
```

proof generation が theorem inference の正しさを変更してはならない。presentation layer は proof semantics から分離する。

---

# 48. 次の設計境界

Phase 60 は完了。

次は:

```text
Phase 61
Toda Lemma 5.5 bracket transport
```

target:

```text
β∈π_{t+2}(S^m)
β∘η_{t+2}=0
t>0
↓
{η_{m+2},E³β,η_{t+5}}_3
contains
±(E²β∘E^tν₄)
```

Phase 61 では Phase 60 の:

```text
TodaLemma54Statement
α* specialization provenance
Whitehead correction data
E[ι₄,ι₄]=0
```

を再利用し、α* / ν₄ construction を再実装しない。

stable `(G_1;2)=Z/2{η}`、stable `(G_2;2)=Z/2{η²}`、generic coset/sign/divisibility framework は concrete need が生じるまで保留する。
