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

Phase 58 までこの原則を維持している。

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

Phase 58 でも generic inference engine の変更は行っていない。

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

# 34. テスト方針

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

repeatable rule については:

```text
fixed-point-safe か
one-shot / staged execution が必要か
```

も確認する。

---

# 35. 文書運用方針

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

# 36. 次の設計境界

Phase 58 は完了。

次は source material の次の concrete consequence を確認してから Phase 59 の target を確定する。

```text
next source statement
↓
dependency analysis
↓
current representation compatibility
↓
minimum implementation
```

stable homotopy model、generic Toda-bracket coset algebra、generic normalization は concrete need が生じるまで保留する。
