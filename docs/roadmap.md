# EHP Proof Tracer ロードマップ

## 1. この文書の役割

```text
README.md
=
現在の機能 / 現在の状態

docs/design.md
=
現在の設計 / semantics / boundary

docs/development_log.md
=
時系列の開発記録

docs/roadmap.md
=
今後の機能依存関係 / Phase 計画
```

---

# 2. Phase 48 完了時点

完了済みの流れ:

```text
Phase 28  map injectivity / isomorphism / equality reflection
Phase 29  actual H facts / typing / isomorphism
Phase 30  Toda Prop.2.2 right
Phase 31  SmashProduct minimum representation
Phase 32  Toda Prop.2.2 left
Phase 33  Barratt–Hilton prerequisites
Phase 34  Toda Prop.3.1 Barratt–Hilton theorem rules
Phase 35  actual H((2ι₂)η₂) calculation
Phase 36  actual H(4η₂) calculation
Phase 37  actual H-side equality closure
Phase 38  Injective(H) reflection
Phase 39  PrimaryComponent minimum representation
Phase 40  TodaPrimaryGroup minimum representation
Phase 41  PreimageSubgroup minimum representation
Phase 42  WhiteheadProduct minimum representation
Phase 43  Toda Lemma 4.1 premise minimum representation
Phase 44  Toda Lemma 4.1 case semantics
Phase 45  Toda Proposition 4.2 2-primary EHP exact sequence
Phase 46  Toda (4.5) stable-range E^(m-n) isomorphism
Phase 47  Toda Proposition 4.4 decomposition isomorphism
Phase 48  Toda Proposition 4.4 suspension E injectivity consequence
```

Phase 48 直前に記録されている full regression:

```text
2277 passed in 55.61s
```

Phase 48 の focused test / probe は current tree に存在する。
Phase 48 completion の document 更新時には、Phase 48 実装後の最新 full-suite count を記録する。

代表 probe:

```powershell
python -m probes.probe_phase48_capabilities
```

---

# 3. 現在の基本方針

今後は Toda の theorem catalogue を本の順番どおり先に実装するのではなく、具体的なホモトピー群計算を進め、その途中で本当に必要になった theorem / fact だけを導入する。

基本の流れ:

```text
実際に計算したいホモトピー群
↓
現在の推論でどこまで進むか確認
↓
最初に不足する theorem / fact を特定
↓
compatibility check
↓
必要最小限の representation
↓
必要最小限の theorem semantics
↓
既存 inference engine に接続
↓
具体的計算を end-to-end で完了
```

重要:

```text
使いそうな theorem
!=
今すぐ実装すべき theorem
```

```text
具体的計算で必要になった theorem
=
実装候補へ昇格
```

---

# 4. Phase 46：Toda (4.5) 完了

Toda (4.5):

```text
n ≥ k+2
m ≥ n
```

のとき:

```text
E^(m-n):
π_{n+k}^n
→
π_{m+k}^m
```

は同型。

実装済みの層:

```text
ScalarGreaterEqualStatement
↓
TodaIteratedSuspensionMap
↓
Toda45IsomorphismStatement
```

applicability では:

```text
n ≥ k+2
m ≥ n
source = π_{n+k}^n
target = π_{m+k}^m
exponent = m-n
```

を同一 symbolic instance として guard-aware に確認する。

代表的な推論:

```text
3 GIVEN premises
↓
1 Toda45IsomorphismStatement
↓
fixed point
```

generic map-property bridge は type boundary のため未導入。

---

# 5. Phase 47：Toda Proposition 4.4 完了

Toda Proposition 4.4:

```text
α ∈ π_{2n-1}^n
H(α)=±ι_{2n-1}
```

のとき:

```text
Φ:
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
→
π_i^n

Φ(β,γ)=Eβ+α∘γ
```

は同型。

実装済み:

```text
TodaPrimaryGroupMembershipStatement
DirectSumGroup with TodaPrimaryGroup summands
TodaProp44DecompositionMap
TodaProp44IsomorphismStatement
```

applicability では:

```text
membership degree = 2n-1
same α
H(α)=±ι_{2n-1}
source first = π_{i-1}^{n-1}
source second = π_i^{2n-1}
target = π_i^n
formula = Eβ+α∘γ
```

を同一 symbolic instance として確認する。

---

# 6. Phase 48：Toda Proposition 4.4 の帰結 E 単射 完了

目的:

```text
Toda Proposition 4.4 decomposition isomorphism
↓
first direct-sum summand restriction
↓
E: π_{i-1}^{n-1} → π_i^n is injective
```

Phase 48 では generic `EHP_E_MAP` の injectivity と specific Toda suspension instance を混同しない。

実装済み representation:

```text
TodaSuspensionMap
├── source_group: TodaPrimaryGroup
└── target_group: TodaPrimaryGroup
```

代表:

```text
E:
π_{i-1}^{n-1}
→
π_i^n
```

first-summand restriction theorem:

```text
TodaProp44FirstSummandRestrictionStatement
```

意味:

```text
Φ|_{π_{i-1}^{n-1}}
=
E: π_{i-1}^{n-1} → π_i^n
```

injectivity consequence:

```text
TodaProp44SuspensionInjectiveStatement
```

意味:

```text
E: π_{i-1}^{n-1} → π_i^n
is injective
```

end-to-end:

```text
α ∈ π_{2n-1}^n
H(α)=±ι_{2n-1}
TodaProp44DecompositionMap
TodaSuspensionMap
↓
TodaProp44IsomorphismStatement
+
TodaProp44FirstSummandRestrictionStatement
↓
TodaProp44SuspensionInjectiveStatement
↓
fixed point
```

重要な boundary:

```text
TodaProp44SuspensionInjectiveStatement
!= InjectiveMapStatement(EHP_E_MAP)
```

Phase 48 では以下を導入しない:

```text
generic InjectiveMapStatement bridge
generic map-property type generalization
general direct-sum inclusion machinery
automatic equality reflection through TodaSuspensionMap
```

代表 probe:

```powershell
python -m probes.probe_phase48_capabilities
```

状態:

```text
COMPLETE
```

---

# 7. 次の中心方針：具体的な低次ホモトピー群計算

Phase 48 までで Chapter 4 の symbolic theorem infrastructure がかなり整った。

次は theorem representation 自体を増やすより、具体的な低次ホモトピー群を実際に計算し、必要な theorem / fact をその都度追加していく。

近い流れ:

```text
Phase 49
π_3^2 = Z{η_2}
↓
次の concrete calculation
π_4^3
↓
Toda Prop.2.7 が必要
↓
Prop.2.7 を必要最小限実装
↓
π_4^3 calculation completion
↓
さらに必要な低次群 / relation を計算
↓
Toda Prop.5.1 の証明依存を埋める
↓
Toda Prop.5.1 proof completion
```

この流れを当面の開発ストーリーとする。

---

# 8. Phase 49：concrete EHP calculation `π_3^2 = Z{η_2}`

次の concrete target:

```text
π_3^2 = Z{η_2}
```

使用する完全列:

```text
π_2^1
-E→
π_3^2
-H→
π_3^3
-Δ→
π_1^1
-E→
π_2^2
```

必要な低次元 fact:

```text
π_2^1 = 0
π_3^3 = Z{ι_3}
E: π_1^1 → π_2^2 is isomorphism
```

数学的な証明経路:

```text
π_2^1 = 0
+
E-H exact
↓
Ker(H)=Im(E)=0
↓
H injective
```

次に:

```text
E: π_1^1 → π_2^2 is isomorphism
↓
E injective
+
Δ-E exact
↓
Im(Δ)=Ker(E)=0
↓
Δ=0
```

さらに:

```text
H-Δ exact
+
Δ=0
↓
Im(H)=Ker(Δ)=π_3^3
↓
H surjective
```

したがって:

```text
H: π_3^2 → π_3^3
is isomorphism
```

さらに:

```text
π_3^3 = Z{ι_3}
```

から、`H` の逆像として一意な `η_2` を取り:

```text
H(η_2)=ι_3
```

を満たす `η_2 ∈ π_3^2` を得る。

最終結論:

```text
π_3^2 = Z{η_2}
```

---

# 9. Phase 49 の分割案

```text
Phase 49-1
current exactness → injective / surjective compatibility check

Phase 49-2
low-dimensional facts required by the calculation
π_2^1 = 0
π_3^3 = Z{ι_3}
E: π_1^1 → π_2^2 is isomorphism

Phase 49-3
exactness + zero left term
→ H injective

Phase 49-4
right-side E injective + exactness
→ Δ = 0
→ H surjective

Phase 49-5
H injective + H surjective
→ instance-aware H isomorphism

Phase 49-6
minimum generator transport across isomorphism
H(η_2)=ι_3
→ π_3^2 = Z{η_2}

Phase 49-7
representative probe / final regression / completion
```

重要な scope boundary:

```text
π_3^2 のための generator transport
!=
general existential quantification engine
```

```text
π_3^2 のための uniqueness
!=
general witness / uniqueness framework
```

具体的必要がない限り general existential machinery は導入しない。

---

# 10. Phase 50 candidate：concrete calculation `π_4^3`

Phase 49 完了後の次の concrete target 候補:

```text
π_4^3
```

この計算では Toda Proposition 2.7 が必要になることが判明している。

したがって Prop.2.7 は単なる将来候補ではなく、次の concrete calculation に対する既知の依存関係として扱う。

依存関係:

```text
π_4^3 を計算したい
↓
current inference で進める
↓
Prop.2.7 が必要になる地点で停止
↓
Toda Prop.2.7 compatibility check
↓
Prop.2.7 の必要部分だけ minimum representation
↓
Prop.2.7 theorem semantics
↓
π_4^3 calculation を再開
↓
π_4^3 calculation completion
```

Prop.2.7 を本全体の theorem catalogue として先に一般化しすぎない。

Phase 50 の細分化は、Phase 49 completion 後に `π_4^3` の実際の証明を確認して決める。

現時点の候補:

```text
Phase 50-1
π_4^3 proof dependency compatibility check

Phase 50-2
Toda Prop.2.7 minimum representation check

Phase 50-3
Toda Prop.2.7 minimum theorem semantics

Phase 50-4
Prop.2.7 を concrete π_4^3 calculation に接続

Phase 50-5
remaining exactness / injectivity / group facts

Phase 50-6
π_4^3 end-to-end representative proof

Phase 50-7
final regression / completion
```

重要:

```text
Prop.2.7
=
KNOWN UPCOMING DEPENDENCY
for concrete calculation of π_4^3
```

---

# 11. Toda Proposition 5.1 へ向かう流れ

Phase 49 の直後に Toda Proposition 5.1 を一気に証明するとは固定しない。

まず低次ホモトピー群を実際に計算し、Prop.5.1 の証明に必要な dependency を concrete calculation を通じて揃える。

推奨する流れ:

```text
Phase 49
π_3^2 = Z{η_2}
↓
Phase 50 candidate
π_4^3 calculation
└─ requires Toda Prop.2.7
↓
必要な次の low-dimensional calculations
↓
Prop.5.1 proof dependency analysis
↓
不足する Toda theorem / relation を concrete need に応じて追加
↓
Toda Proposition 5.1 proof completion
```

このとき、Prop.5.1 を単なる GIVEN theorem として登録するのではなく、可能な限り既存の Chapter 1–4 infrastructure と concrete low-dimensional facts から導出することを目標にする。

以前の Phase 35 では Prop.5.1 側の結果を使う方向で actual calculation を進めていた。

将来的には:

```text
低次元群計算
+
必要な Chapter 1–4 theorem
+
EHP exactness
+
map injectivity / isomorphism
+
composition / suspension / Hopf invariant
↓
Toda Prop.5.1 を導出
↓
既存 Phase 35–38 の branch と再接続
```

という形を目標とする。

---

# 12. Toda calculation backlog

以下は具体的計算で使う可能性が高い Toda の事項。

```text
Toda Lemma 1.1
Toda Proposition 1.2
Toda Proposition 1.3 の下の式
Toda Proposition 1.4
Toda Proposition 1.5
Toda Proposition 1.6
Toda (2.1)
Toda Proposition 2.3
Toda Proposition 2.5 の 2-primary case
Toda Proposition 2.6
Toda Proposition 2.7
Toda Corollary 3.7
Toda Lemma 4.3
Toda Lemma 4.5
```

ただし、すべてを同じ status にはしない。

## 12.1 現在の known upcoming dependency

```text
Toda Proposition 2.7
```

status:

```text
KNOWN UPCOMING DEPENDENCY
```

理由:

```text
π_4^3 の concrete calculation で必要
```

したがって Phase 50 candidate で concrete need に合わせて導入する。

## 12.2 その他の backlog

```text
Toda Lemma 1.1
Toda Proposition 1.2
Toda Proposition 1.3 の下の式
Toda Proposition 1.4
Toda Proposition 1.5
Toda Proposition 1.6
Toda (2.1)
Toda Proposition 2.3
Toda Proposition 2.5 の 2-primary case
Toda Proposition 2.6
Toda Corollary 3.7
Toda Lemma 4.3
Toda Lemma 4.5
```

status:

```text
DEFERRED UNTIL CONCRETE NEED
```

実装方針:

```text
concrete homotopy-group calculation
↓
identify first missing theorem / fact
↓
compatibility check
↓
minimum representation
↓
minimum theorem semantics
↓
complete the concrete calculation
```

Toda の目次順に theorem を大量実装しない。

同じ theorem が複数の actual calculation に共通することが分かった場合、その時点で独立 Phase に昇格させる。

特に:

```text
Toda (2.1)
```

は将来的に reusable foundation になる可能性があるが、現時点では concrete need が出るまで保留する。

---

# 13. Capability matrix

| capability | 状態 | Phase |
|---|---|---|
| map injectivity / equality reflection | IMPLEMENTED | 28 |
| actual H facts / typing | IMPLEMENTED | 29 |
| Toda Prop.2.2 right | IMPLEMENTED | 30 |
| SmashProduct | IMPLEMENTED | 31 |
| Toda Prop.2.2 left | IMPLEMENTED | 32 |
| ScalarExpression tree | IMPLEMENTED | 33 |
| parity → symbolic sign evaluation | IMPLEMENTED | 33 |
| symbolic IteratedSuspension exponent | IMPLEMENTED | 33 |
| Toda Prop.3.1 Barratt–Hilton | IMPLEMENTED | 34 |
| actual `H((2ι₂)η₂)=4ι₃` | IMPLEMENTED | 35 |
| `H(4η₂)=4ι₃` | IMPLEMENTED | 36 |
| `H((2ι₂)η₂)=H(4η₂)` | IMPLEMENTED | 37 |
| `(2ι₂)η₂=4η₂` | IMPLEMENTED | 38 |
| p-primary component `π_i(S^n;p)` | IMPLEMENTED | 39 |
| Toda subgroup `π_i^n` | IMPLEMENTED | 40 |
| `E^{-1}(π_{2n}(S^{n+1};2))` preimage group | IMPLEMENTED | 41 |
| Whitehead product `[a,b]` | IMPLEMENTED | 42 |
| Toda Lemma 4.1 premise zero / nonzero representation | IMPLEMENTED | 43 |
| symbolic `ι_{n-1}` / `ι_{2n±1}` | IMPLEMENTED | 44 |
| symbolic free cyclic group `Z{α}` | IMPLEMENTED | 44 |
| symbolic direct-sum group | IMPLEMENTED | 44 |
| primary-component membership statement | IMPLEMENTED | 44 |
| Toda Lemma 4.1 odd case | IMPLEMENTED | 44 |
| Toda Lemma 4.1 even / Whitehead nonzero case | IMPLEMENTED | 44 |
| Toda Lemma 4.1 even / Whitehead zero case | IMPLEMENTED | 44 |
| zero-case `H(α)=ι_{2n-1}` | IMPLEMENTED | 44 |
| zero-case `Eα∈π_{2n}(S^{n+1};2)` | IMPLEMENTED | 44 |
| symbolic E / H / Δ map terms | IMPLEMENTED | 45 |
| symbolic Toda EHP long sequence | IMPLEMENTED | 45 |
| instance-aware exactness window | IMPLEMENTED | 45 |
| Toda Prop.4.2 E-H exactness | IMPLEMENTED | 45 |
| Toda Prop.4.2 H-Δ exactness | IMPLEMENTED | 45 |
| Toda Prop.4.2 Δ-E exactness | IMPLEMENTED | 45 |
| Toda exactness → generic exactness bridge | IMPLEMENTED | 45 |
| Toda Prop.4.2 → zero-composition reuse | IMPLEMENTED | 45 |
| Toda (4.5) `E^(m-n)` isomorphism | IMPLEMENTED | 46 |
| Toda Prop.4.4 decomposition isomorphism | IMPLEMENTED | 47 |
| Toda Prop.4.4 `E` injectivity consequence | IMPLEMENTED | 48 |
| concrete calculation `π_3^2 = Z{η_2}` | NEXT | 49 |
| concrete calculation `π_4^3` | PLANNED | 50 candidate |
| Toda Prop.2.7 | KNOWN UPCOMING DEPENDENCY | 50 candidate |
| Toda Prop.5.1 proof dependency analysis | PLANNED | after low-dimensional calculations |
| Toda Prop.5.1 proof completion | PLANNED | later |
| stable homotopy | PLANNED | later |
| higher Toda bracket | DEFERRED | concrete need |

---

# 14. 長期 dependency

既存 actual equality branch:

```text
Phase 29
actual H equality-reflection foundation
↓
Phase 30
Toda Prop.2.2 right COMPLETE
↓
Phase 31
SmashProduct COMPLETE
↓
Phase 32
Toda Prop.2.2 left COMPLETE
↓
Phase 33
Barratt–Hilton prerequisites COMPLETE
↓
Phase 34
Toda Prop.3.1 Barratt–Hilton COMPLETE
↓
Phase 35
actual H((2ι₂)η₂)=4ι₃ COMPLETE
↓
Phase 36
H(4η₂)=4ι₃ COMPLETE
↓
Phase 37
H((2ι₂)η₂)=H(4η₂) COMPLETE
↓
Phase 38
Injective(H) reflection COMPLETE
↓
(2ι₂)η₂=4η₂ COMPLETE
```

Chapter 4 branch:

```text
Toda (4.2)
Serre finiteness
↓
Phase 39
PrimaryComponent π_i(S^n;p) COMPLETE
↓
Phase 40
TodaPrimaryGroup π_i^n COMPLETE
↓
Phase 41
PreimageSubgroup COMPLETE
↓
Phase 42
WhiteheadProduct COMPLETE
↓
Phase 43
Toda Lemma 4.1 premise representation COMPLETE
↓
Phase 44
Toda Lemma 4.1 case semantics COMPLETE
↓
Phase 45
Toda Prop.4.2 2-primary EHP exact sequence COMPLETE
↓
Phase 46
Toda (4.5)
stable-range E^(m-n) isomorphism COMPLETE
↓
Phase 47
Toda Prop.4.4
π_i^n decomposition isomorphism COMPLETE
↓
Phase 48
Toda Prop.4.4 consequence
E is injective COMPLETE
```

今後の concrete calculation branch:

```text
Phase 49
π_3^2 = Z{η_2}
↓
Phase 50 candidate
π_4^3
↓
Toda Prop.2.7
必要最小限を導入
↓
π_4^3 calculation completion
↓
次の low-dimensional calculations
↓
Prop.5.1 proof dependency analysis
↓
必要な backlog theorem を順次昇格
↓
Toda Prop.5.1 proof completion
↓
既存 Phase 35–38 branch と再接続
```

---

# 15. 現在の deferred boundary

未実装:

```text
automatic compound parity inference
general symbolic scalar simplification
general SmashProduct typing / algebra / normalization
symbolic suspension source / target arithmetic
Toda (2.1) general rule set
universal arbitrary-map equality congruence
automatic identity semantics from ι notation
Toda (4.2) Serre finiteness fact
Toda (4.3) evaluated definition
automatic Whitehead-product zero inference
automatic Whitehead-product nonzero inference
ZERO / INEQUALITY contradiction detection
Whitehead-product bilinearity
Whitehead-product antisymmetry
general existential quantification / witness objects
automatic α existence / uniqueness
PrimaryComponent membership → ordinary membership bridge
symbolic map typing solver
general symbolic dimension solver
automatic symbolic image/kernel group construction
instance-aware generic ExactnessStatement
general symbolic inequality solver
automatic numeric inequality validation
generic map-property type generalization
Toda45IsomorphismStatement → IsomorphismStatement bridge
generic injectivity consequence for TodaIteratedSuspensionMap
stable homotopy group model
stable Toda brackets
higher Toda brackets
```

ただし、これらのうち concrete calculation で直接必要になったものは、その時点で deferred から active dependency へ昇格する。

---

# 16. 開発原則

今後も以下を維持する。

```text
actual mathematical need
↓
compatibility check
↓
minimum representation
↓
minimum theorem semantics
↓
existing generic inference engine
↓
representative end-to-end proof
```

避けるもの:

```text
Toda の theorem catalogue を先に大量実装する
general CAS を作る
concrete need のない general existential machinery を作る
必要性のない generic map-property type generalization を行う
将来 Phase の機能を先取りする
```

優先するもの:

```text
具体的な群を1つ計算する
↓
不足を特定する
↓
最小限追加する
↓
その群の証明を完成させる
```

---

# 17. Testing principle

各 layer で以下を確認する。

1. representation
2. structural distinction
3. applicability
4. invalid-case behavior
5. typing compatibility
6. integration
7. provenance
8. representative scenario
9. scope
10. full regression
11. executable probe

Phase completion では必ず:

```text
focused pytest
related regression
full pytest
representative probe
```

を確認する。
