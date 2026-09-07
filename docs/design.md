# EHP Proof Tracer 設計

この文書は現在のアーキテクチャ、意味論、設計境界を記録する。

過去の実装経緯は `docs/development_log.md`、将来構想は `docs/roadmap.md` に分離する。

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

Phase 56 まで generic inference engine は theorem-specific branch を追加せず維持している。

---

# 3. 式表現レイヤー

主要構造:

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Sum
├── SmashProduct
├── WhiteheadProduct
├── Composition
├── MapApplication
├── Suspension
├── IteratedSuspension
└── TodaBracket
```

constructor は theorem-aware normalization を行わない。

特に:

```text
IteratedSuspension(x,1) != Suspension(x)
ScalarSum(ScalarProduct(2,2),-1) != 3
```

を structural equality のまま保持する。

必要な concrete theorem branch では専用 bridge / specialization を使う。

---

# 4. ホモトピー群・群構造

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

`FiniteCyclicGroup(order,generator)` は concrete finite-cyclic calculation の最小表現であり、一般 quotient simplifier を意味しない。

---

# 5. 標準写像と instance-aware map

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
```

設計境界:

```text
specific theorem instance
!=
generic MapSymbol
```

---

# 6. Toda Proposition 4.2

instance-aware EHP exactness:

```text
TodaEHPSequence
TodaEHPExactnessWindow
TodaProp42ExactnessStatement
```

rules:

```text
toda_prop42_e_h_exactness_inference_rule()
toda_prop42_h_delta_exactness_inference_rule()
toda_prop42_delta_e_exactness_inference_rule()
```

generic exactness machineryと Toda-specific window semantics を分離する。

---

# 7. Toda Proposition 4.4

Phase 47 で:

```text
Φ:
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
→ π_i^n

Φ(β,γ)=Eβ+α∘γ
```

を `TodaProp44DecompositionMap` で structural に保持する。

`TodaProp44IsomorphismStatement` は specific decomposition instance が同型であることを保持する。

Phase 48 では first summand restriction を:

```text
TodaProp44FirstSummandRestrictionStatement
```

で保持し、同じ instance の suspension injectivity を導出する。

---

# 8. Phase 49 の η₂ 設計

`η₂` を literature GIVEN として final premise にせず:

```text
H:π_3^2→π_3^3 isomorphism
+
π_3^3=Z{ι₃}
↓
η₂ = ι₃ の一意な H-preimage
```

として定義する。

専用 statement:

```text
TodaPi32Eta2DefinitionStatement
```

No general:

```text
ExistsStatement
UniqueExistsStatement
Witness
InverseMap
```

を追加しない。

---

# 9. ±付き relation の境界

現在使用する専用 statement:

```text
TodaProp27HopfInvariantUpToSignStatement
TodaPi32WhiteheadSquareUpToSignStatement
TodaDeltaImageUpToSignStatement
```

一般化しない:

```text
PlusMinus
SignVariable
generic up-to-sign transitivity
general sign solver
```

具体的な theorem dependency が必要な場合だけ専用 bridge を追加する。

---

# 10. Phase 50 finite-cyclic calculation

中心:

```text
H([ι₂,ι₂])=±2ι₃
+
H(η₂)=ι₃
+
H injective
↓
[ι₂,ι₂]=±2η₂
```

```text
Δ(ι₅)=±[ι₂,ι₂]
↓
Δ(ι₅)=±2η₂
```

```text
Im(Δ)=Z{2η₂}
↓
Ker(E)=Z{2η₂}
```

```text
π_3^2=Z{η₂}
+
Ker(E)=Z{2η₂}
+
E surjective
↓
π_4^3=Z/2{Eη₂}
```

η-family notation:

```text
η_n=E^(n-2)η₂
η₃=Eη₂
↓
π_4^3=Z/2{η₃}
```

---

# 11. η-family 設計

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

これは η-family 専用であり:

```text
generic iterated-suspension composition
generic suspension normalization
generic scalar normalization
```

を導入しない。

---

# 12. Toda Proposition 5.1 finite-dimensional integration

専用 aggregate statement:

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

4 premise を `ProofStep.premises` に保持する。

Proposition 5.1 自身を premise として再投入しない。

---

# 13. Phase 56 設計目標

Toda (5.2):

```text
η₂∘- :
π_i^3
≅
π_i^2
    (i≥3)
```

必要 dependency:

```text
Toda Proposition 4.4
H(η₂)=ι₃
π_{i-1}^1=0  (i≥3)
Composition
```

Phase 56 は Toda Lemma 5.2 を使わない。

---

# 14. Phase 56-1 compatibility boundary

既存 object で次を保持できる:

```text
π_{i-1}^1 ⊕ π_i^3 → π_i^2
Eβ+η₂∘γ
π_{i-1}^1=0
```

利用:

```text
TodaProp44DecompositionMap
Composition
TodaPrimaryGroupZeroStatement
```

問題:

```text
generic Prop.4.4 rule:
2n-1

concrete n=2:
3
```

が structural equality では一致しない。

解決方針:

```text
generic scalar normalization を追加しない
↓
n=2, α=η₂ 専用 specialization を追加
```

---

# 15. Phase 56-2 zero theorem semantics

専用 narrow rule:

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

を再利用する。

意図的に受理しない:

```text
i≥2
i≥4
3≥i
concrete 5≥3
```

この Phase では general inequality solver を追加しない。

---

# 16. Phase 56-3 Prop.4.4 specialization

専用 rule:

```text
toda_prop44_eta2_n2_isomorphism_inference_rule()
```

premise:

```text
TodaPi32Eta2DefinitionStatement    INFERENCE
H(η₂)=ι₃                           INFERENCE
TodaProp44DecompositionMap
```

expected map:

```text
Φ:
π_{i-1}^1 ⊕ π_i^3
→
π_i^2

Φ(β,γ)=Eβ+η₂∘γ
```

conclusion:

```text
TodaProp44IsomorphismStatement
```

generic `toda_prop44_isomorphism_inference_rule()` は変更しない。

---

# 17. Phase 56-4 second-summand restriction

専用 statement:

```text
TodaProp44SecondSummandRestrictionStatement
```

field:

```text
decomposition_map
composition
```

専用 rule:

```text
toda_prop44_eta2_second_summand_restriction_inference_rule()
```

導出:

```text
Φ isomorphism
↓
Φ|_{π_i^3}(γ)=η₂∘γ
```

generic:

```text
CompositionMap
LeftCompositionMap
generic map restriction
```

は追加しない。

---

# 18. Phase 56-5 Toda (5.2)

最小 final statement:

```text
Toda52CompositionIsomorphismStatement
```

field:

```text
source_group
target_group
composition
```

target:

```text
source_group = π_i^3
target_group = π_i^2
composition = η₂∘γ
```

専用 rule:

```text
toda_52_eta2_composition_isomorphism_inference_rule()
```

premise は exactly:

```text
π_{i-1}^1=0                  INFERENCE
Prop.4.4 n=2 isomorphism     INFERENCE
second-summand restriction   INFERENCE
```

guard で:

```text
zero group == first summand
restriction.decomposition_map == isomorphism.map
second summand == π_i^3
target == π_i^2
α == η₂
restriction.composition == η₂∘γ
formula == Eβ+η₂∘γ
```

を確認する。

一般化しない:

```text
DirectSumGroup(A,B) + A=0 → B
generic direct-sum simplifier
generic isomorphism restriction theorem
generic composition-map framework
```

---

# 19. Phase 56 provenance 方針

最終 `Toda52CompositionIsomorphismStatement` は:

```text
ProofRule.INFERENCE
```

final premise count:

```text
3
```

すべて derived:

```text
π_{i-1}^1=0
Prop.4.4 n=2 specialization
second-summand restriction
```

rejection:

```text
GIVEN zero statement
GIVEN Prop.4.4 isomorphism
GIVEN restriction
wrong zero group
wrong α
wrong second summand
wrong formula
wrong composition
```

---

# 20. Phase 56 representative run

base premise:

```text
Phase 49 base premises × 6
i≥3
Prop.4.4 decomposition map
```

合計:

```text
given = 8
```

同一 fixed-point run で:

```text
η₂ definition
H(η₂)=ι₃
π_{i-1}^1=0
Prop.4.4 n=2 specialization
second-summand restriction
Toda (5.2)
```

まで導出する。

代表値:

```text
given = 8
derived = 12
rounds = 9
fixed point = True
```

重要:

```text
π_{i-1}^1=0 is GIVEN = False
Prop.4.4 specialization is GIVEN = False
second-summand restriction is GIVEN = False
Toda (5.2) is GIVEN = False
```

---

# 21. Phase 56 testing

focused:

```text
Phase 56-1   6 passed
Phase 56-2  10 passed
Phase 56-3  11 passed
Phase 56-4  13 passed
Phase 56-5  16 passed
Phase 56-6  10 passed
```

full regression:

```text
2910 passed in 29.17s
```

generic inference engine:

```text
変更なし
```

---

# 22. Phase 56 completion boundary

完成:

```text
Prop.4.4 / Composition / zero-group compatibility
π_{i-1}^1=0 narrow theorem semantics
n=2, α=η₂ specialization
second-summand restriction
Toda52CompositionIsomorphismStatement
Toda (5.2) composition isomorphism
applicability
provenance
representative probe
same-run integration
full regression
```

先取りしない:

```text
Toda Lemma 5.2
generic scalar normalization
generic direct-sum reduction
generic composition-map framework
generic isomorphism restriction
stable homotopy model
generic Toda-bracket normalization
```

---

# 23. テスト方針

各数学レイヤーで:

```text
representation
applicability
invalid cases
integration
provenance
representative probe
termination / scope
full regression
```

を確認する。

structural-only Phase では不要な theorem semantics を先取りしない。

---

# 24. ドキュメント方針

```text
README.md
=
current capabilities / status

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

current specification は latest README / design を優先する。

---

# 25. 次の設計境界

次:

```text
Phase 57
Toda Lemma 5.2 proof integration
```

入力 candidate:

```text
α∈π_i(S^3)
2α=0
β∈{η₃,2ι₄,Eα}_1
```

target:

```text
H(β)=E²α
2β=η₃∘Eα∘η_{i+1}
β∈π_{i+2}^3
Δ(E²α)=0
```

ただし source material では Lemma statement と proof ending の η-index に不整合があるため、Phase 57-1 で原典・型・次元を確認してから development target を確定する。

現在確認済み dependency:

```text
Lemma 4.5
Proposition 2.6
Proposition 1.4
Proposition 1.3
Corollary 3.7
(2.1)
```

Phase 57 でも:

```text
actual proof need
↓
minimum consequence
```

の原則を維持し、各 theorem の full formalization は具体的必要がなければ追加しない。
