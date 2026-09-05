# EHP Proof Tracer Roadmap

この roadmap は今後の capability dependency と開発順序を記録する。

実装済み architecture / semantics は `README.md` / `docs/design.md`、実装履歴は `docs/development_log.md` を正本とする。

---

# 1. 基本方針

開発順序:

```text
actual mathematical target
↓
proof dependency check
↓
minimum missing representation
↓
minimum missing theorem / fact semantics
↓
end-to-end inference
↓
representative probe
↓
full regression
```

原則:

```text
必要になった theorem を必要な範囲だけ実装する
```

避ける:

```text
future Phase の先取り
general theorem catalogue の先行構築
general CAS 化
generic inference engine への domain knowledge 混入
```

---

# 2. Completed foundation

Phase 1–38:

```text
abelian-group calculations
generic proof / inference
EHP exactness
ORDER
Suspension
Freudenthal
Composition
Hopf invariant
Toda bracket infrastructure
Toda Prop.2.2
Toda Prop.3.1
actual η_2 equality branch
```

Phase 39–44:

```text
PrimaryComponent
TodaPrimaryGroup
PreimageSubgroup
WhiteheadProduct
Toda Lemma 4.1 premises
Toda Lemma 4.1 case semantics
```

Phase 45–48:

```text
Toda Proposition 4.2 instance-aware EHP exactness
Toda (4.5) stable-range E^(m-n) isomorphism
Toda Proposition 4.4 decomposition isomorphism
Toda Proposition 4.4 suspension E injectivity consequence
```

---

# 3. Phase 49 COMPLETE：`π_3^2 = Z{η_2}`

Target:

```text
π_3^2 = Z{η_2}
```

EHP path:

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

low-dimensional facts:

```text
π_2^1 = 0
π_3^3 = Z{ι_3}
E: π_1^1 → π_2^2 is isomorphism
```

proof:

```text
π_2^1 = 0
+
E-H exact
↓
H injective
```

```text
E: π_1^1 → π_2^2 is isomorphism
↓
E injective
+
Δ-E exact
↓
Δ=0
```

```text
H-Δ exact
+
Δ=0
↓
H surjective
```

```text
H injective
+
H surjective
↓
H isomorphism
```

```text
H isomorphism
+
π_3^3 = Z{ι_3}
↓
ι_3 has a unique preimage under H
↓
denote it by η_2
↓
H(η_2)=ι_3
↓
π_3^2=Z{η_2}
```

important semantic boundary:

```text
η_2
!= initially GIVEN element
```

instead:

```text
η_2
=
name assigned to the unique H-preimage of ι_3
```

representative fixed point:

```text
round 1
H injective
E injective

round 2
Δ=0

round 3
H surjective

round 4
H isomorphism

round 5
define η_2 as unique preimage of ι_3

round 6
H(η_2)=ι_3
π_3^2=Z{η_2}
```

verified:

```text
2557 passed in 56.45s
```

state:

```text
COMPLETE
```

---

# 4. Next central direction：concrete low-dimensional calculations

Phase 49 で Chapter 4 symbolic theorem infrastructure を concrete calculation に接続できた。

今後は theorem representation 自体を増やすことを目的にせず、具体的な低次群を計算し、その証明に不足する theorem / relation を必要最小限追加する。

近い flow:

```text
Phase 49
π_3^2 = Z{η_2}
COMPLETE
↓
Phase 50
π_4^3
↓
Toda Proposition 2.7 dependency
↓
minimum Prop.2.7 semantics
↓
π_4^3 calculation completion
↓
additional low-dimensional groups / relations
↓
Toda Proposition 5.1 proof dependencies
↓
Toda Proposition 5.1 proof completion
```

---

# 5. Phase 50 candidate：concrete `π_4^3`

Next target:

```text
π_4^3
```

現時点で既知の重要 dependency:

```text
Toda Proposition 2.7
```

Phase 50 は compatibility / dependency check から始める。

---

## Phase 50-1：π_4^3 proof dependency compatibility check

確認すること:

```text
π_4^3 calculation の intended proof path
必要な EHP exactness windows
既存 low-dimensional facts
既存 η_2 representation / relation
既存 Suspension / Composition infrastructure
Toda Proposition 2.7 が必要になる exact step
current representation で lossless に表現できる部分
不足する theorem semantics
```

production code は原則変更しない。

目的:

```text
Prop.2.7 が必要
```

という大まかな認識を、

```text
どの premise
+
どの rule
↓
どの conclusion
```

が不足しているかまで具体化すること。

---

## Phase 50-2：minimum Prop.2.7 representation compatibility

Phase 50-1 の結果に基づき、Toda Prop.2.7 全体ではなく `π_4^3` calculation に必要な statement shape を確認する。

actual source text に従って必要 structure を決定する。

---

## Phase 50-3：minimum Toda Prop.2.7 theorem semantics

Phase 50-2 で不足が確定した theorem consequence のみ実装。

禁止:

```text
Prop.2.7 の全 consequence を先取り
general theorem catalogue
unrelated composition refactor
```

---

## Phase 50-4：π_4^3 concrete inference

既存 EHP / low-dimensional facts / Prop.2.7 minimum consequence をつなぎ、`π_4^3` の group structure または必要 generator relation を推論する。

---

## Phase 50-5：applicability / provenance / invalid cases

確認:

```text
correct group instance
correct map instance
correct generator instance
cross-instance rejection
missing-premise rejection
theorem provenance
```

---

## Phase 50-6：representative probe / full regression

追加候補:

```text
probes/probe_phase50_capabilities.py
tests/test_phase50_probe.py
```

end-to-end fixed point を確認する。

---

## Phase 50-7：Phase 50 completion

completion conditions は Phase 50-1 で proof target を確定後に具体化する。

state:

```text
PLANNED
```

---

# 6. Toda Proposition 2.7 boundary

Toda Proposition 2.7 は Phase 50 の具体的証明 dependency として扱う。

方針:

```text
π_4^3 proof
↓
Prop.2.7 の必要 consequence を特定
↓
その consequence のみ実装
```

not:

```text
Prop.2.7 full formalization
↓
あとで π_4^3 に使う
```

この順序を守る。

---

# 7. Later direction：Toda Proposition 5.1 proof completion

Phase 35 では Toda Proposition 5.1 由来の fact を使用して actual relation branch を動かしている。

将来的にはその fact 自体を proof-derived にする。

候補 flow:

```text
必要な低次ホモトピー群
↓
必要な composition / suspension relations
↓
Toda Prop.2.7 等の prior results
↓
Toda Prop.5.1 premises
↓
Toda Prop.5.1 conclusion
```

重要:

```text
Phase 49 では Prop.5.1 の H(η_2)=ι_3 fact を使用せず
η_2 を H isomorphism による一意な逆像として定義した
```

このため later Prop.5.1 proof branch との循環を避けられている。

---

# 8. Deferred generalizations

actual mathematical need が出るまで deferred:

```text
general existential quantification
general witness / uniqueness framework
general inverse-map machinery
general cyclic-generator transport
generic typed map-property framework
general symbolic dimension solver
general symbolic map typing solver
general Whitehead-product algebra
stable homotopy group model
higher Toda brackets
general-purpose CAS normalization
```

---

# 9. Current immediate next step

```text
Phase 50-1
π_4^3 proof dependency compatibility check
```

最初に実装するのではなく、current code / tests と mathematical proof path を照合する。

特に:

```text
Toda Proposition 2.7
```

が `π_4^3` のどの inference edge を埋めるのかを明示する。

その確認後に Phase 50-2 以降へ進む。
