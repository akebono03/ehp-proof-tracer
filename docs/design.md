# EHP Proof Tracer 設計

この文書は現在のアーキテクチャ、意味論、設計境界を記録する。

過去の実装経緯は `docs/development_log.md`、将来構想は `docs/roadmap.md` に分離する。

---

# 1. 基本設計原則

```text
actual mathematical need
↓
minimum representation
↓
explicit fact / domain rule
↓
existing generic inference engine
```

generic inference engine に数学固有の theorem knowledge を埋め込まない。

```text
representation != typing != theorem knowledge
structural equality != mathematical equality
```

---

# 2. レイヤー分離

```text
literature-backed theorem / explicit facts
↓
domain-specific inference rules
↓
generic ProofStep / InferenceRule machinery
↓
expression / statement structures
↓
homotopy / EHP data
↓
abelian-group algebra
```

Phase 45–52 でも generic inference engine は変更していない。

---

# 3. 式表現レイヤー

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
└── IteratedSuspension
```

constructor は theorem-aware normalization を行わない。

---

# 4. 記号的ホモトピー群レイヤー

```text
PrimaryComponent
TodaPrimaryGroup
PreimageSubgroup
FreeCyclicGroup
FiniteCyclicGroup
DirectSumGroup
```

`FiniteCyclicGroup(order,generator)` は Phase 50 で `Z/2{η₃}` を structural に保持するための minimum representation。

---

# 5. 標準写像 / インスタンス対応写像

標準写像:

```text
EHP_E_MAP
EHP_H_MAP
EHP_DELTA_MAP
```

インスタンス対応写像:

```text
TodaSuspensionMap
TodaHopfInvariantMap
TodaDeltaMap
```

```text
specific theorem instance != generic MapSymbol
```

---

# 6. Toda Proposition 4.2

```text
TodaEHPSequence
TodaEHPExactnessWindow
TodaProp42ExactnessStatement
```

Rules:

```text
toda_prop42_e_h_exactness_inference_rule()
toda_prop42_h_delta_exactness_inference_rule()
toda_prop42_delta_e_exactness_inference_rule()
```

---

# 7. Toda Proposition 4.4

Phase 47:

```text
Φ:
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
→ π_i^n
Φ(β,γ)=Eβ+α∘γ
```

Phase 48:

```text
Φ is isomorphism
+
first-summand restriction = E
↓
E injective
```

---

# 8. Phase 49 設計

目的:

```text
π_3^2=Z{η₂}
```

`η₂` は GIVEN にせず、H isomorphism による `ι_3` の一意な逆像として theorem-derived に定義する。

No general:

```text
ExistsStatement
UniqueExistsStatement
Witness
InverseMap
```

---

# 9. Phase 50 設計目標

目的:

```text
π_4^3=Z/2{η₃}
```

推論経路:

```text
H([ι_2,ι_2])=±2ι_3
↓
[ι_2,ι_2]=±2η₂
↓
Δ(ι_5)=±[ι_2,ι_2]
↓
Im(Δ)=Z{2η₂}
↓
Ker(E)=Z{2η₂}
```

and:

```text
π_4^5=0
+
E-H exactness
↓
E surjective
```

then:

```text
π_3^2=Z{η₂}
+
Ker(E)=Z{2η₂}
+
E surjective
↓
π_4^3=Z/2{Eη₂}
```

finally:

```text
η₃=Eη₂
↓
π_4^3=Z/2{η₃}
```

---

# 10. Toda Proposition 2.7 の最小意味論

実装対象:

```text
H([ι_2,ι_2])=±2ι_3
```

のみを実装する。

文:

```text
TodaProp27HopfInvariantUpToSignStatement
```

これは `Relation` ではなく、未確定の符号を定理専用の1文に保持する。

---

# 11. ±付き等式の設計境界

Phase 50 also uses:

```text
TodaPi32WhiteheadSquareUpToSignStatement
TodaDeltaImageUpToSignStatement
```

for:

```text
[ι_2,ι_2]=±2η₂
Δ(ι_5)=±[ι_2,ι_2]
```

一般化して追加しないもの:

```text
PlusMinus
SignVariable
UpToSignEquality algebra
```

は追加しない。

符号を捨てるのは生成部分群へ移った後だけとする:

```text
Z{±2η₂}=Z{2η₂}
```

---

# 12. Phase 50 低次元 fact

```text
π_5^5=Z{ι_5}
π_4^5=0
```

提供関数:

```text
pi_5_5_free_cyclic_fact()
pi_4_5_zero_fact()
```

---

# 13. 像 / 核 / 全射性 bridge

限定的な記号的文:

```text
TodaDeltaImageFreeCyclicStatement
TodaSuspensionKernelFreeCyclicStatement
TodaSuspensionSurjectiveStatement
```

これらは concrete な `GroupMap` の部分群参照とは意図的に分離する。

---

# 14. FiniteCyclicGroup

```text
FiniteCyclicGroup
├── order: int
└── generator: Expression
```

用途:

```text
Z/2{Eη₂}
Z/2{η₃}
```

No general quotient simplifier or first-isomorphism theorem engine は追加しない。

---

# 15. η-family 記法

定義:

```text
η_n=E^(n-2)η₂
```

表現:

```text
TodaEtaFamilyDefinitionStatement
```

`n=3` では専用 bridge により次を導出する:

```text
η₃=Eη₂
```

重要:

```text
IteratedSuspension(η₂,1) != Suspension(η₂)
```

No generic suspension normalization は追加しない。

---

# 16. Phase 50 fixed-point 統合

```text
given = 11
derived = 9
rounds = 6
fixed point = True
```

各 round:

```text
1: Prop.2.7 consequence, Δ up-to-sign, E surjective, η₃=Eη₂
2: [ι_2,ι_2]=±2η₂
3: Im(Δ)=Z{2η₂}
4: Ker(E)=Z{2η₂}
5: π_4^3=Z/2{Eη₂}
6: π_4^3=Z/2{η₃}
```

---

# 17. provenance 方針

Phase 50 のすべての導出結果は次を使う:

```text
ProofRule.INFERENCE
```

また次を保持する:

```text
ProofStep.premises
ProofStep.inference_rule
```

最終結果 `π_4^3=Z/2{η₃}` は GIVEN ではない。

---

# 18. 適用条件方針

reject 対象:

```text
wrong H instance
wrong Δ instance
wrong exactness window
wrong kernel coefficient
wrong source generator
wrong target group
missing π_3^2 structure
wrong η-family index
```

意図しない符号固定の等式も reject する。

---

# 19. Phase 50 後の generic engine 境界

追加しないもの:

```text
general up-to-sign algebra
general quotient simplification
general first-isomorphism theorem engine
general suspension normalization
general symbolic map typing
general symbolic dimension solver
```

---

# 20. テスト方針

各数学レイヤーで確認するもの:

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

Phase 50 全体回帰:

```text
2703 passed in 65.69s
```

---

# 21. ドキュメント方針

```text
README.md = current capabilities / status
docs/design.md = current architecture / semantics / boundaries
docs/development_log.md = chronological implementation history
docs/roadmap.md = future dependency
```

---

# 22. Phase 51 依存関係分析の設計

Phase 51 is analysis-only. No production-code representation or inference rule は追加しない。

Proposition 5.1 の有限次元側の目標:

```text
π_3^2=Z{η₂}
π_{n+1}^n=Z/2{η_n}  (n≥3)
H(η₂)=ι₃
Δ(ι₅)=±2η₂
```

Toda p.39 has an internal notation inconsistency between the proof text and the printed proposition line. The proof text uses `Δ(ι₅)=±2η₂`, which is compatible with the target group `π_3^2`; this is the development target.

既存の独立依存関係:

```text
Phase 49:
π_3^2=Z{η₂}
H(η₂)=ι₃

Phase 50:
π_4^3=Z/2{η₃}
[ι₂,ι₂]=±2η₂
Δ(ι₅)=±[ι₂,ι₂]

Phase 46:
Toda (4.5) stable-range E^(m-n) isomorphism
```

追加の低次元ホモトピー群 table は不要とする。

---

# 23. Phase 51 不足 edge の境界

不足している最小実装:

```text
1. specific direct bridge
   Δ(ι₅)=±[ι₂,ι₂]
   +
   [ι₂,ι₂]=±2η₂
   ↓
   Δ(ι₅)=±2η₂

2. finite cyclic transport through Toda (4.5)
   π_4^3=Z/2{η₃}
   +
   E^(n-3): π_4^3 ≅ π_{n+1}^n
   ↓
   π_{n+1}^n=Z/2{E^(n-3)η₃}

3. η-family-specific suspension bridge
   E^(n-3)η₃=η_n

4. finite-dimensional Proposition 5.1 integration
   with provenance / circular-dependency rejection
```

Δ の direct bridge は定理専用のままとし、一般の ± 付き推移律や符号 solver は追加しない。

finite-cyclic transport は具体的な Toda (4.5) の必要範囲に限定し、後続 Phase で必要になるまでは一般の同型 transport framework を追加しない。

higher η bridge は η-family 専用に限定し、任意の `Suspension` / `IteratedSuspension` を normalize しない。

---

# 24. Proposition 5.1 の循環依存回避方針

安全に使える premise:

```text
Phase 49 proof-derived H(η₂)=ι₃
Phase 49 π_3^2=Z{η₂}
Phase 50 π_4^3=Z/2{η₃}
Toda Proposition 2.7 minimum consequence
Toda Proposition 4.2 exactness
Toda (4.5) stable-range isomorphism
η-family definition
```

Proposition 5.1 の premise として使用禁止:

```text
old literature GIVEN H(η₂)=ι₃ attributed to Proposition 5.1
old Phase 35–36 proof traces that depend on that GIVEN fact
```

Phase 35–38 inference machinery may later be reused only after replacing the old Proposition-5.1 GIVEN provenance with the independently derived Phase 49 result.

---

# 25. stable 結論の保留境界

The stable conclusion

```text
(G_1;2)=Z/2{η}
```

は意図的に保留する。有限次元 Proposition 5.1 branch のために stable homotopy-group model は導入しない。

Proposition 5.1 に続く composition isomorphism (5.2) も現在の proof target の外とする。

---

# 26. Phase 52 direct bridge 設計

目的:

```text
Δ(ι₅)=±[ι₂,ι₂]
+
[ι₂,ι₂]=±2η₂
↓
Δ(ι₅)=±2η₂
```

新しい statement class は追加せず、次を再利用する:

```text
TodaDeltaImageUpToSignStatement
TodaPi32WhiteheadSquareUpToSignStatement
```

The target is represented by the existing `TodaDeltaImageUpToSignStatement` with:

```text
map = Δ : π_5^5 → π_3^2
element = ι₅
positive_value = 2η₂
```

専用推論ルール:

```text
toda_delta_iota5_two_eta2_up_to_sign_inference_rule()
```

guard は次の Toda instance の完全一致を要求する:

```text
source = π_5^5
target = π_3^2
element = ι₅
first positive value = [ι₂,ι₂]
Whitehead-square statement = [ι₂,ι₂]=±2η₂
```

したがって、この rule は ± 付き等式の一般推移律ではない。

次の不正ケースを reject する:

```text
wrong Δ source
wrong Δ target
wrong element
wrong Whitehead square
wrong coefficient
wrong η-family index
```

統合方針:

```text
existing Phase 50 image rule remains unchanged
+
Phase 52 direct bridge is added in parallel
```

Thus round 3 contains both:

```text
Δ(ι₅)=±2η₂
Im(Δ)=Z{2η₂}
```

代表実行の件数:

```text
given = 11
derived = 10
rounds = 6
fixed point = True
```

provenance 要件:

```text
Δ(ι₅)=±[ι₂,ι₂]  INFERENCE
[ι₂,ι₂]=±2η₂     INFERENCE
↓
Δ(ι₅)=±2η₂       INFERENCE
```

generic inference engine は変更しない。

Phase 52 全体回帰:

```text
2731 passed in 26.67s
```

---

# 27. Phase 53 finite-cyclic transport 設計

目的:

```text
π_4^3=Z/2{η₃}
+
E^(n-3): π_4^3 ≅ π_{n+1}^n
↓
π_{n+1}^n=Z/2{E^(n-3)η₃}
```

既存表現だけを再利用する。

```text
Toda45IsomorphismStatement
TodaIteratedSuspensionMap
FiniteCyclicGroup
IteratedSuspension
Relation
```

新しい transport 用 group class や generic isomorphism transport framework は追加しない。

専用 rule:

```text
toda_45_pi4_3_finite_cyclic_transport_inference_rule()
```

適用対象は次に限定する。

```text
source group relation = π_4^3=Z/2{η₃}
Toda (4.5) source sphere = 3
source degree = 4 または既存 Phase 46 の ScalarSum(3,1)
target = π_{n+1}^n
exponent = n-3 の既存 symbolic tree
```

`ScalarSum(3,1)` と concrete `4` の差は、この specific `π_4^3` guard 内だけで受理する。generic scalar normalization は導入しない。

generator transport は:

```text
η₃
↓
IteratedSuspension(η₃,n-3)
```

までとする。

```text
E^(n-3)η₃=η_n
```

への接続は Phase 54 の責務であり、Phase 53 では行わない。

---

# 28. Phase 53 stable-range / applicability 設計

Toda (4.5) の stable range は Phase 46 の責務を維持する。

```text
stable-range premises
+
TodaIteratedSuspensionMap
↓
Toda45IsomorphismStatement
```

Phase 53 rule 自体は inequality を再評価せず、導出済み `Toda45IsomorphismStatement` を premise とする。

現在の scalar inequality は structural representation であり、一般の数値 inequality solver は導入しない。

Phase 53 で reject を固定した対象:

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

---

# 29. Phase 53 integration / provenance 設計

Phase 50 の最終 result を GIVEN として再投入しない。

同一 fixed-point run 内で:

```text
Phase 50 premises
↓
π_4^3=Z/2{η₃}  INFERENCE

Phase 46 stable-range premises
↓
Toda45IsomorphismStatement  INFERENCE

両者
↓
π_{n+1}^n=Z/2{E^(n-3)η₃}  INFERENCE
```

transport step の2 premise は両方とも `ProofRule.INFERENCE` であることを要求する。

代表実行の件数:

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

generic inference engine は変更していない。

---

---

# 30. Phase 54 higher η-family bridge 設計

目的:

```text
η_n=E^(n-2)η₂
+
η₃=Eη₂
↓
E^(n-3)η₃=η_n
```

Phase 54-2 で `TodaEtaFamilyDefinitionStatement` を symbolic `n` に対応させる。

対応範囲:

```text
index = int | ScalarSymbol
η_n:
  dimension = n
  source = n+1
  target = n
  generator family = η
  generator index = n

definition:
  η_n = IteratedSuspension(η₂,n-2)
```

既存の concrete `n=2`, `n=3` の表現は維持する。

一般の scalar expression 全体へ index 型を広げず、Phase 54 で必要な `ScalarSymbol` のみ追加する。

---

# 31. Phase 54 η-family-specific bridge

専用推論ルール:

```text
toda_higher_eta_family_bridge_inference_rule()
```

受理する premise は次に限定する。

```text
TodaEtaFamilyDefinitionStatement
  index = symbolic n
  element = η_n
  iterated_suspension = E^(n-2)η₂

Relation
  η₃ = Eη₂
```

導出:

```text
E^(n-3)η₃=η_n
```

結論側の `n-3` は Phase 53 の transported generator と同じ structural tree:

```text
ScalarSum(
  left=n,
  right=ScalarProduct(
    left=-1,
    right=3,
  ),
)
```

を使う。

これにより一般の scalar normalization を追加せず Phase 53 と structural equality で接続する。

追加しないもの:

```text
E^a(E^b x)=E^(a+b)x の一般則
generic IteratedSuspension composition
generic suspension normalization
generic scalar normalization
```

---

# 32. Phase 54 applicability / rejection 設計

valid case:

```text
symbolic η_n definition
+
η₃=Eη₂
```

reject を固定する対象:

```text
concrete higher η-family index
mismatched symbolic index
wrong η_n element structure
wrong η-family definition exponent
wrong η₃ base
wrong suspended η₂ base
reversed η₃ relation
non-equality η₃ relation
```

Phase 54-4 では production code を変更せず、既存 narrow guard の適用範囲を regression test で固定する。

---

# 33. Phase 54 finite-cyclic integration 設計

Phase 53 result:

```text
π_{n+1}^n=Z/2{E^(n-3)η₃}
```

Phase 54 bridge:

```text
E^(n-3)η₃=η_n
```

から:

```text
π_{n+1}^n=Z/2{η_n}
```

を導出する。

専用推論ルール:

```text
toda_higher_eta_finite_cyclic_generator_inference_rule()
```

guard は次を要求する。

```text
target group = π_{n+1}^n
order = 2
generator = E^(n-3)η₃
bridge = E^(n-3)η₃=η_n
```

したがって一般の

```text
G=Z/m{x}
+
x=y
↓
G=Z/m{y}
```

という cyclic-generator rewrite は追加していない。

---

# 34. Phase 54 integration / provenance 設計

Phase 53 の最終 relation を GIVEN として再投入しない。

同一 fixed-point run 内で:

```text
Phase 50 premises
↓
π_4^3=Z/2{η₃}  INFERENCE

Phase 46 stable-range premises
↓
Toda45IsomorphismStatement  INFERENCE

両者
↓
π_{n+1}^n=Z/2{E^(n-3)η₃}  INFERENCE
```

並行して:

```text
η_n=E^(n-2)η₂  GIVEN
η₃=Eη₂         INFERENCE
↓
E^(n-3)η₃=η_n  INFERENCE
```

最後に:

```text
π_{n+1}^n=Z/2{E^(n-3)η₃}  INFERENCE
+
E^(n-3)η₃=η_n              INFERENCE
↓
π_{n+1}^n=Z/2{η_n}         INFERENCE
```

最終 step の2 premise は両方とも `ProofRule.INFERENCE` であることを要求する。

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

generic inference engine は変更していない。

---

# 35. Phase 54 representative probe

追加:

```text
probes/probe_phase54_capabilities.py
tests/test_phase54_probe.py
```

代表出力:

```text
η_n = E^(n-2)η₂
η₃ = Eη₂
↓
E^(n-3)η₃ = η_n

π_(n+1)^n = Z/2{E^(n-3)η₃}
+
E^(n-3)η₃ = η_n
↓
π_(n+1)^n = Z/2{η_n}
```

provenance:

```text
source group result is derived = True
transport result is derived = True
higher eta bridge is derived = True
final group result is derived = True
final premise count = 2
final premises are derived = True
given premise count = 15
derived step count = 13
derived round count = 8
fixed point = True
```

---

# 36. Phase 54 completion boundary

Phase 54 で完成:

```text
symbolic higher η-family definition
η-family-specific E^(n-3)η₃=η_n bridge
wrong-instance rejection
Phase 53 finite-cyclic transport との統合
π_{n+1}^n=Z/2{η_n}
INFERENCE provenance
representative probe
full regression
```

追加していないもの:

```text
generic iterated-suspension composition
generic suspension normalization
generic scalar normalization
generic cyclic-generator rewrite
Proposition 5.1 final integration
stable homotopy model
```

---

# 37. 次の設計境界

Phase 54 は完了。

次:

```text
Phase 55
Toda Proposition 5.1 finite-dimensional integration / provenance
```

Phase 55 で利用可能な独立導出済み結果:

```text
π_3^2=Z{η₂}
H(η₂)=ι₃
Δ(ι₅)=±2η₂
π_{n+1}^n=Z/2{η_n}
```

Phase 55 でも Proposition 5.1 自身を premise として再投入せず、循環依存を避けた provenance を確認する。

引き続き先取りしない:

```text
stable (G_1;2)=Z/2{η}
stable homotopy-group model
generic cyclic-generator rewrite
generic scalar normalization
generic suspension normalization
```
